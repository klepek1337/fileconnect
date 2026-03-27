# FileConnect

**FileConnect** is a simple but powerful tool that generates a full folder structure and merges file contents into one readable output file.
Perfect for sending projects to AI, documentation, code review, backups, or archiving.

## Why use FileConnect?

Because copying files manually is slow and messy.

FileConnect:

* generates a **tree structure** of a folder
* merges **all text files into one file**
* respects **.gitignore**
* skips **large and binary files**
* creates a **clean readable output**
* works **fast and offline**
* written in **Go → single executable**
* no installation needed

It is extremely useful for:

* sending projects to ChatGPT / AI
* documentation
* code review
* backups
* project snapshots
* analyzing repositories
* sharing code with someone in one file

## Features

Program has 3 modes:

1. **Merge selected files**
2. **Generate folder structure**
3. **Generate folder structure + all file contents**

Output example:

```
### Folder structure: project ###

├── main.go
├── go.mod
└── utils/
    └── files.go

### FILE CONTENTS ###

### File contents: main.go ###
package main
...
```

## How to run

### Run from source

```
go run .
```

### Build executable

```
go build
```

Then run:

```
fileconnect.exe
```

## How to use

After starting the program:

```
Select mode:
1 - Merge files
2 - Generate folder structure
3 - Merge files and folder structure
```

For modes **2** and **3**:

* choose folder
* choose output file
* program generates result

## Requirements

* Go installed (for building)
* Windows / Linux

## Summary

FileConnect turns an entire project into **one clean readable file** in seconds.
If you work with code, AI, documentation, or large projects — this tool saves a lot of time.

---
