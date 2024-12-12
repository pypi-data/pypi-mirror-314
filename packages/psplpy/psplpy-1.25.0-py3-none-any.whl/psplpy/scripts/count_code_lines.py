from psplpy.file_utils import *


def count_file(file_path: Path, encoding='utf-8', non_empty: bool = False, non_comment: bool = False) -> int:
    lines = file_path.read_text(encoding=encoding).splitlines()
    if non_empty:
        lines = [line for line in lines if line.strip()]
    if non_comment:
        comment_lines = ''
        comment_list = []
        multiline_comment_flag = False
        new_lines = []
        for i in range(len(lines)):
            if i == 0:
                previous_line = ''
            else:
                previous_line = lines[i - 1].strip()
            line = lines[i].strip()
            if multiline_comment_flag:
                # if the multiline comment head had been found in the previous line,
                # next we should find the tail of this comment, once we find it, this multiline comment will over
                comment_lines += lines[i] + '\n'
                if line[-3:] in ['"""', "'''"]:
                    multiline_comment_flag = False
                    comment_list.append((comment_lines[:-1], file_path, i))
                    comment_lines = ''
            else:
                head_length = 0
                if line[:3] in ['"""', "'''"]:
                    head_length = 3
                elif line[:4] in ['r"""', "r'''", 'f"""', "f'''", 'u"""', "u'''"]:
                    head_length = 4
                if head_length:  # if found the multiline comment head
                    has_multiline = False
                    # if equals, that means this line just has the multiline comment head, it must be the beginning
                    if len(line) == head_length:
                        has_multiline = True
                    # if not equals, but the last 3 chars not in them, that means the multiline comment
                    # not just one line, otherwise, the multiline comment only one line
                    elif line[-3:] not in ['"""', "'''"]:
                        has_multiline = True
                    if has_multiline:
                        # if this string turns out to have multiline, but it's previous line's last char in them,
                        # that means this multiline string is a function's parameter, not a comment
                        if (not previous_line) or previous_line[-1] not in ['[', '(', ',']:
                            multiline_comment_flag = True
                            comment_lines += lines[i] + '\n'
                        else:  # because it's a function's parameter, so it's the real code
                            new_lines.append(line)
                    else:  # has not multiline, just a single line comment, continue
                        comment_list.append((lines[i], file_path, i))
                elif line[0] == '#':  # is a single line comment, continue
                    comment_list.append((lines[i], file_path, i))
                elif line[0] in ('"', "'"):
                    if (not previous_line) or previous_line[-1] not in ['[', '(', ',']:
                        comment_list.append((lines[i], file_path, i))
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
        lines = new_lines
        for comment in comment_list:
            content, path, lineno = comment
            print(f'{path}, {lineno}, {"=" * 50}')
            print(content)
    return len(lines)


def count_dir(project_dir: str | Path, encoding: str = 'utf-8') -> tuple[int, int, int]:
    files = [file for file in get_file_paths(project_dir) if file.suffix == '.py']
    print(f'Total files：{len(files)}')
    count = 0
    for file in files:
        count += count_file(file, encoding)
    print(f'Total lines: {count}')
    non_empty_count = 0
    for file in files:
        non_empty_count += count_file(file, encoding, non_empty=True)
    print(f'After excluded empty lines: {non_empty_count}')
    non_comment_count = 0
    for file in files:
        non_comment_count += count_file(file, encoding, non_empty=True, non_comment=True)
    print(f'After excluded comment lines: {non_comment_count}')
    return count, non_empty_count, non_comment_count


if __name__ == '__main__':
    project_dir = Path(__file__).parent.parent.parent
    print(project_dir)
    count_dir('/usr/local/lib/python3.10/site-packages/django/utils')
