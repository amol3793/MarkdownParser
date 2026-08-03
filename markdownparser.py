import argparse
import sys


def read_lines(file_name):
    try:
        with open(file_name) as f:
            return f.readlines()
    except IOError as e:
        sys.exit("Could not read %s: %s" % (file_name, e))


def parse_heading(line):
    if not line.lstrip(' ').startswith('#'):
        return line
    i = 1
    while i < len(line) and line[i] == '#':
        i += 1
    hash_count = i
    return "<h" + str(hash_count) + ">" + line[:-1].replace("#", "", hash_count) + " </h" + str(hash_count) + ">" + "\n"


def parse_paragraph_breaks(lines):
    """Turns blank lines into <p>/</p><p>/</p> markers, tracking open-paragraph state."""
    open_para_flag = 0
    for idx, line in enumerate(lines):
        if line.lstrip(' ').startswith('\n'):
            if open_para_flag == 0:
                lines[idx] = line.replace('\n', '<p>', 1)
                open_para_flag = 1
            elif open_para_flag == 1:
                lines[idx] = line.replace('\n', '</p><p>', 1)
            else:
                lines[idx] = line.replace('\n', '</p>', 1)
    return open_para_flag


def parse_line_break(line):
    if line[0:-1].endswith('  '):
        return line[0:-3] + "<br/>"
    return line


def parse_bullet_list(lines, idx, bullet_list_flag):
    line = lines[idx]
    if not line.lstrip().startswith('* '):
        return line, bullet_list_flag

    next_is_bullet = idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith('* ')

    if bullet_list_flag == 0:
        line = '<ul>\n<li>' + line.replace('*', "", 1) + '</li>'
    else:
        line = '<li>' + line.replace('*', "", 1) + '</li>'

    if next_is_bullet:
        bullet_list_flag = 1
    else:
        bullet_list_flag = 0
        line = line + '</ul>'

    return line, bullet_list_flag


def parse_bold(line):
    if line.count('**') <= 1:
        return line
    result_string = ''
    for word in line.split():
        if word.startswith('**') and word.endswith('**') and len(word) > 4:
            result_string += '<strong>' + word.replace('**', '', 2) + '</strong> '
        else:
            result_string += word + " "
    return result_string


def parse_italic(line):
    if line.count('_') <= 1:
        return line
    result_string = ''
    for word in line.split():
        if word.startswith('_') and word.endswith('_') and len(word) > 2:
            result_string += '<em>' + word.replace('_', '', 2) + '</em> '
        else:
            result_string += word + ' '
    return result_string


def markdown_to_html(lines):
    lines = list(lines)
    open_para_flag = parse_paragraph_breaks(lines)

    bullet_list_flag = 0
    for idx in range(len(lines)):
        lines[idx] = parse_heading(lines[idx])
        lines[idx] = parse_line_break(lines[idx])
        lines[idx], bullet_list_flag = parse_bullet_list(lines, idx, bullet_list_flag)
        lines[idx] = parse_bold(lines[idx])
        lines[idx] = parse_italic(lines[idx])

    if open_para_flag == 1:
        lines.append('</p>')

    return ''.join(lines)


def markdown_parser(input_file, output_file):
    lines = read_lines(input_file)
    html = markdown_to_html(lines)
    with open(output_file, 'w') as f:
        f.write(html)


def main():
    arg_parser = argparse.ArgumentParser(description="Convert a Markdown file to HTML.")
    arg_parser.add_argument('input', nargs='?', default='sample.md', help="input Markdown file (default: sample.md)")
    arg_parser.add_argument('output', nargs='?', default='sample.html', help="output HTML file (default: sample.html)")
    args = arg_parser.parse_args()
    markdown_parser(args.input, args.output)


if __name__ == '__main__':
    main()
