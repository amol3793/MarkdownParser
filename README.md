# MarkdownParser

A Markdown-to-HTML converter written from scratch in Python, with no external parsing libraries.

## Supported syntax

- Headings (`#` through `######`)
- Paragraphs and blank-line breaks
- Line breaks (trailing double-space)
- Bullet lists (`* `)

## Usage

```bash
python markdownparser.py
```

The script reads `sample.md` in the current directory and writes the converted markup to `sample.html`. Both files are included in this repo so you can see the expected output.
