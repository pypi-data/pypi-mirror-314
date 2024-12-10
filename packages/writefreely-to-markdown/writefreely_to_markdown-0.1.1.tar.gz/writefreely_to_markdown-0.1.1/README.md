# Writefreely to Markdown

The default writefreely export only embed metadata in files, which is hard to be used for other blogging software.

This script converts writefreely exported JSON files into CommonMark based markdown

## Usage

### Exporting files from your blog

1. Go to your blog website and log in
1. Click `customize` button in the top left corner
1. Hover over your logo on top left, and click export
1. Click JSON or prettified (They are the same), and download.

### Install and run this program

I recommend using `pipx`, since you usually only need this software once:

```bash
pipx run writefreely-to-markdown --help
```

Otherwise, you can either run the script file at `./writefreely_to_markdown/main.py` directly, or install using `pip install writefreely-to-markdown`

Check out the usage and run the program again, the generated markdown files are in `./exported` by default.
