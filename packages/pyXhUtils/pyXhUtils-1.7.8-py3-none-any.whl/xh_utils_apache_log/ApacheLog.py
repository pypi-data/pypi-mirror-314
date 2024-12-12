import datetime as dt
import re
import typing
import urllib
import urllib.parse
from dataclasses import dataclass
from enum import Enum

from xh_utils_string import findStartEnd


class LogLineIndex(Enum):
    Raw = 0
    IpAddress = 1
    Identd = 2
    UserId = 3
    ReceivedAt = 4
    Url = 5
    StatusCode = 6
    ReturnSize = 7
    Referer = 8
    Agent = 9


@dataclass(frozen=True)
class UrlMeta:
    method: str
    path: str
    params: dict
    potocol: str
    metaStr: str

    @staticmethod
    def extractUrlMetaSlient(metaStr: str) -> typing.Union['UrlMeta', None]:
        try:
            return UrlMeta.extractUrlMeta(metaStr)
        except:
            return None

    @staticmethod
    def extractUrlMeta(metaStr: str) -> 'UrlMeta':
        method = ""
        path = ""
        param = dict()
        potocol = ""

        line = metaStr if type(metaStr) is not tuple else metaStr[0]

        if line not in ['-', "\\n"]:
            # v1 => method
            # v2 => path
            # v3 => potocol
            v1, v2, v3 = line.split(" ")
            method = urllib.parse.unquote(v1)
            vPath = v2.split("?")

            url = None
            if re.match(urllib.parse.unquote_plus(vPath[0]), "[a-zA-Z0-9]{4}"):
                url = urllib.parse.unquote_plus(url)
            else:
                url = urllib.parse.unquote_plus(vPath[0])

            path = url

            v5d = {
                (urllib.parse.unquote(pair[0]), urllib.parse.unquote(pair[1])) if len(pair) == 2 else (
                    urllib.parse.unquote(pair[0]), "")
                for paramStr in vPath[1].split("&") if len(paramStr) > 0
                for pair in [paramStr.split("=")]

            } if len(vPath) == 2 else {}

            param = v5d
            potocol = urllib.parse.unquote(v3)
        return UrlMeta(method, path, param, potocol, metaStr)


@dataclass(frozen=True)
class LogLine:
    ipAddress: str
    identd: str
    userId: str
    receivedAt: dt.datetime
    url: str
    status_code: int
    return_size: int
    referer: str
    agent: str
    raw: str

    def unquotedRaw(self) -> str:
        msg = self.raw
        iStart, iEnd, url = findStartEnd(msg, "\"", "\"", "\\", inclusive=False, startSearchFrom=0)
        msg = msg[:iStart] + urllib.parse.unquote(url) + msg[iEnd:]
        return msg

    # def dict(self):
    #     return {field.name: str(getattr(self, field.name)) for field in fields(self)}

    @staticmethod
    def read_log_lines(line: str):
        try:
            result = []
            result.append(line)

            I_IP = 0
            I_IID = 1
            I_UID = 2
            I_DATE = 3
            I_URL_S = 4
            I_URL_E = 5
            I_STATUS_S = 6
            I_STATUS_E = 7
            I_LENGTH = 8
            I_REFERER_S = 9
            I_REFERER_E = 10
            I_AGENT_S = 11
            I_AGENT_E = 12

            varIndex = 0
            buf = ""
            for c in line:
                if varIndex in [I_IP, I_IID, I_UID, I_STATUS_E, I_LENGTH] and c == " ":
                    if varIndex in [I_STATUS_E, I_LENGTH]:
                        result.append(buf)
                    else:
                        result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_DATE] and c == "[":
                    buf = ""
                elif varIndex in [I_DATE] and c == "]":
                    result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_URL_S, I_REFERER_S, I_AGENT_S] and c == "\"":
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_URL_E] and c == "\"":
                    if buf[-1] == "\\":  # escaping
                        buf += c
                        continue

                    result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_REFERER_E, I_AGENT_E] and c == "\"":
                    result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_STATUS_S] and c == " ":
                    varIndex += 1
                else:
                    buf += c
            return result
        except Exception:
            print(line)
            raise

    @staticmethod
    def from_line(result) -> 'LogLine':
        # dt.datetime.strptime(, "%d/%b/%Y:%H:%M:%S %z")
        ipaddress = result[LogLineIndex.IpAddress.value],
        identd = result[LogLineIndex.Identd.value],
        user_id = result[LogLineIndex.UserId.value],
        received_at = result[LogLineIndex.ReceivedAt.value],
        url = result[LogLineIndex.Url.value],
        status_code = result[LogLineIndex.StatusCode.value],
        return_size = result[LogLineIndex.ReturnSize.value],
        referer = result[LogLineIndex.Referer.value],
        agent = result[LogLineIndex.Agent.value],
        raw = result[LogLineIndex.Raw.value]
        return LogLine(
            ipaddress if type(ipaddress) is not tuple else ipaddress[0],
            identd if type(identd) is not tuple else identd[0],
            user_id if type(user_id) is not tuple else user_id[0],
            dt.datetime.strptime(received_at, "%d/%b/%Y:%H:%M:%S %z")
            if type(received_at) is not tuple
            else dt.datetime.strptime(received_at[0], "%d/%b/%Y:%H:%M:%S %z"),
            url if type(url) is not tuple else url[0],
            int(status_code) if type(status_code) is not tuple else int(status_code[0]),
            int(return_size) if type(return_size) is not tuple else int(return_size[0]),
            referer if type(referer) is not tuple else referer[0],
            agent if type(agent) is not tuple else agent[0],
            raw
        )

    @staticmethod
    def read_log_lines_and_parse(line) -> 'LogLine':
        return LogLine.from_line(LogLine.read_log_lines(line))
