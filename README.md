# WDIFF HTML

Uses [GNU wdiff][wdiff] to generate a word based *diff* from plain text files.

The results are modified to use HTML `<ins>` and `<del>` tags and can be
wrapped in a full HTML document.


# Installation

Use pip:

```
pip install [--user] wdiffhtml
```

Or clone the source and use `setup.py`:

```
git clone https://github.com/brutus/wdiffhtml.git
cd wdiffhtml
python setup.py install [--user]
```


# Usage

`wdiffhtml` writes to _STDOUT_. To get a plain diff which uses `<ins>` and
`<del>` tags to mark changes use:

```
wdiffhtml text_org.txt text_new.txt
```

To create a HTML file for viewing, use the `--wrap-with-html` option:

```
wdiffhtml --wrap-with-html text_org.txt text_new.txt > mydiff.html
```

You can use your own HTML template, CSS and / or Javascript to wrap the output.
There are command line options to set the files on fly, or you can create them
in your data directory (`~/.local/share/wdiffhtml/`) so they get used
automatically.

See `wdiffhtml --help` for more informations.


# Contact

__wdiffhtml__ is at home at https://github.com/brutus/wdiffhtml


[wdiff]: https://www.gnu.org/software/wdiff/wdiff.html
