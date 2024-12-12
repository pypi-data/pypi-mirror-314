def repeat_str(char, count):
    return ''.join(list(map(lambda a: char, range(0, count))))


def findStartEnd(line: str, start: int, end: int, escape: str = '\\', inclusive: bool = True,
                 startSearchFrom: int = 0) -> (int, int, str):
    start_index: int = -1
    end_index: int = -1
    mode = 0
    for i, c in enumerate(line[startSearchFrom:]):
        if mode == 0 and c == start:
            start_index = i
            mode += 1
            continue
        if mode == 1 and c == end:
            if escape == '':
                end_index = i
                break
            else:
                if line[i - 1] != escape:
                    end_index = i
                    break
    start_index = startSearchFrom + start_index
    end_index = startSearchFrom + end_index
    return start_index, end_index, line[start_index + 1:end_index + 1] if inclusive else line[start_index:end_index]


if __name__ == "__main__":
    print(repeat_str('a', 10))
