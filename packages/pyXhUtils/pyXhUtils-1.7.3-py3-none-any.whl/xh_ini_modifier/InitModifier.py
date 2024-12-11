import configparser
import io
from dataclasses import dataclass
from typing import Callable, Generator, List

import yaml

import xh_functional
from xh_functional import Stream


@dataclass
class OpenSSLConfigMetaRow:
    type: str
    state: str
    section: str
    key: str
    value: str


@dataclass
class OpenSSLConfigMeta:
    type: str
    root_path: str
    name: str
    done: bool
    openssl_cnf: List[OpenSSLConfigMetaRow]
    data: dict


class OpenSSLConfigLoader:
    @staticmethod
    def load(file: str) -> Generator[OpenSSLConfigMeta, None, None]:
        with open(file) as f:
            data = yaml.safe_load(f)
            for meta in data:
                try:
                    yield OpenSSLConfigMeta(meta["type"], meta["root_path"], meta["name"],
                                            meta["done"] if "done" in meta else False,
                                            [
                                                OpenSSLConfigMetaRow(row['type'], row["state"], row['section'], row['key'],
                                                                     row['value'] if row['state'] == "present" else "")
                                                for row in meta["openssl_cnf"]
                                            ],
                                            meta
                                            )
                except Exception as e:
                    raise Exception(f"Failed to load meta: {meta}") from e

    @staticmethod
    def load_as_list(file: str) -> List[OpenSSLConfigMeta]:
        return list(OpenSSLConfigLoader.load(file))

    @staticmethod
    def load_as_stream(file: str) -> Stream[OpenSSLConfigMeta, OpenSSLConfigMeta]:
        return Stream(OpenSSLConfigLoader.load_as_list(file))


class IniFile:
    @staticmethod
    def batch_rename_section(parser: configparser.ConfigParser, replace_with: Callable[[str], str]):
        sections = parser.sections()
        for section in sections:
            new_section = replace_with(section)
            parser.add_section(new_section)
            parser[new_section] = parser[section]
            parser.remove_section(section)

    @staticmethod
    def upsert_value(parser: configparser.ConfigParser, section: str, key: str, value: str):
        if section not in parser:
            parser.add_section(section)
        parser[section][key] = value

    @staticmethod
    def rm_value(parser: configparser.ConfigParser, section: str, key: str):
        if section not in parser:
            return False
        else:
            parser.remove_option(section, key)

    @staticmethod
    def modify(file_name: str, config: OpenSSLConfigMeta, persist: bool = True) -> str:
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read(file_name)

        IniFile.batch_rename_section(parser, lambda section: section.strip())
        ip_index = 0
        dns_index = 0
        for row in config.openssl_cnf:
            if row.state == "present":
                if row.type == "alt_names":
                    if row.key == "ip":
                        IniFile.upsert_value(parser, row.section, f"IP.{ip_index}", row.value)
                        ip_index += 1
                    elif row.key == "dns":
                        IniFile.upsert_value(parser, row.section, f"DNS.{dns_index}", row.value)
                        dns_index += 1
                    else:
                        raise Exception(f"Unknown key: {row.key}")
                else:
                    IniFile.upsert_value(parser, row.section, row.key, row.value)
            elif row.state == "remove":
                IniFile.rm_value(parser, row.section, row.key)

        IniFile.batch_rename_section(parser, lambda section: f" {section} ")

        if persist:
            with open(file_name, "w") as f:
                parser.write(f)

        with io.StringIO() as f:
            parser.write(f)
            f.seek(0)
            return f.read()


if __name__ == '__main__':
    config = [
        config
        for config in OpenSSLConfigLoader.load(".config.yaml")
        if not config.done and config.name == "ca"][0]
    print(IniFile.modify("openssl.cnf", config))
