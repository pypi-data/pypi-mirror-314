# Filez4Eva

Shift scans, photos, and other files into structured folders for permanent safekeeping
---

<a href="https://www.flaticon.com/free-icons/elephant" title="elephant icons">Elephant icon created by Flat Icons - Flaticon</a>

I keep files named and organized in a certain way in DropBox. This tool names new files correctly and puts them in the right directory.

## Installation

It's best to install using `pipx`. See [the pipx site](https://pypa.github.io/pipx/) if you need it. Then:

```bash
pipx install filez4eva
```

## Usage

The directory pattern for account documents is:

```
~/Dropbox/accounts/<year>/<account>/<date>-<part>.<extension>
```

Where:

- `year` is the year of the document, typically from the date
- `account` is the name of the account, all lower case, hyphen separated
- `date` is the date on the document in `YYYYMMDD` format
- `part` is the textual part of the name of the document, often starting with the account name, all lower case, hyphen separated
- `extension` is the original filename extension, often `pdf`

I have my browsers etc. set to download new files to Desktop, then it's easy to run Filez4Eva on a file on the desktop using tab completion.

```
filez4eva ~/Desktop/123456789SomeFileIDownloaded.pdf
```

Filez4Eva will ask a series of questions, then move the file.

Note the `part` supports tab-completion, where it looks up all the files previously stored under that account, in any year. So it's easy to reproduce names of periodic files such as financial statements or invoices.

---

Copyright (C) 2023 by Francis Potter. Licensed under the MIT license.

