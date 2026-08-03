# MarkdownParser

A Markdown-to-HTML converter written from scratch in Python, with no external parsing libraries.

## Supported syntax

- Headings (`#` through `######`)
- Paragraphs and blank-line breaks
- Line breaks (trailing double-space)
- Bullet lists (`* `)

## Usage

```bash
python markdownparser.py [input.md] [output.html]
```

Defaults to reading `sample.md` and writing `sample.html` if no arguments are given. Both files are included in this repo so you can see the expected output.
