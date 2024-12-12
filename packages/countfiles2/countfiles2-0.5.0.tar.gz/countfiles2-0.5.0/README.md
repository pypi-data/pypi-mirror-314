# countfiles

Like `tree` on Linux, but for number of files.

## Installation

```shell
pip install countfiles2
```

(The package name `countfiles` was taken.)

## The basics

```shell
$ countfiles --help
usage: countfiles [-h] [--max-depth MAX_DEPTH] [--min-filecount MIN_FILECOUNT] [--sizes] [--count-dirs] [--reverse] [--no-color] [--no-hidden] [--version] [--symlinks] [--sort-count | --sort-size] [path]

Show accumulated number of files per directory.

positional arguments:
  path

options:
  -h, --help            show this help message and exit
  --max-depth MAX_DEPTH, -d MAX_DEPTH
                        Iterate all the way, but only show directories down to this depth.
  --min-filecount MIN_FILECOUNT, -m MIN_FILECOUNT
                        Iterate all the way, but only show directories with this number of files or more.
  --sizes, -s           Also show the total size of every directory.
  --count-dirs, -c      Also include directories in the file counts.
  --reverse, -r         Reverse result sorting.
  --no-color
  --no-hidden           Ignore hidden files and folders.
  --version, -V         show program's version number and exit
  --symlinks, -ln       Follow symlinks (will throw exception if an infinite recursion is detected).
  --sort-count, -sc     Sort results by file count.
  --sort-size, -ss      Sort results by total size.
```

## Example output

```shell
$ countfiles --sizes --max-depth 4
[  5498]  countfiles                                         [  73.8M]
├───[    27]  .git                                           [  58.7K]
│   ├───[     0]  branches                                   [      0]
│   ├───[    13]  hooks                                      [    23K]
│   ├───[     1]  info                                       [    240]
│   ├───[     3]  logs                                       [    537]
│   │   └───[     2]  refs (3 children not shown)            [    358]
│   ├───[     2]  objects                                    [  33.5K]
│   │   ├───[     0]  info                                   [      0]
│   │   └───[     2]  pack                                   [  33.5K]
│   └───[     2]  refs                                       [     73]
│       ├───[     1]  heads                                  [     41]
│       ├───[     1]  remotes (1 child not shown)            [     32]
│       └───[     0]  tags                                   [      0]
├───[   121]  .mypy_cache                                    [   7.8M]
│   └───[   119]  3.11                                       [   7.8M]
│       ├───[     4]  _typeshed                              [   132K]
│       ├───[     4]  collections                            [ 818.3K]
│       ├───[     6]  countfiles                             [  44.2K]
│       ├───[     2]  curses                                 [    38K]
│       ├───[    16]  email                                  [ 313.4K]
│       ├───[    18]  importlib (2 children not shown)       [ 339.6K]
│       ├───[     4]  os                                     [ 412.6K]
│       ├───[     2]  sys                                    [ 157.1K]
│       └───[     2]  zipfile                                [ 100.9K]
├───[  5329]  .venv                                          [  65.9M]
│   ├───[    15]  bin                                        [  19.6M]
│   ├───[     0]  include                                    [      0]
│   │   └───[     0]  python3.11                             [      0]
│   ├───[  5312]  lib                                        [  46.3M]
│   │   └───[  5312]  python3.11 (596 children not shown)    [  46.3M]
│   └───[     1]  share                                      [     2K]
│       └───[     1]  man (1 child not shown)                [     2K]
├───[     3]  build                                          [     7K]
│   ├───[     0]  bdist.linux-x86_64                         [      0]
│   └───[     3]  lib                                        [     7K]
│       └───[     3]  countfiles                             [     7K]
└───[    12]  src                                            [  40.2K]
    ├───[     6]  countfiles                                 [  35.3K]
    │   └───[     3]  __pycache__                            [  23.1K]
    └───[     6]  countfiles2.egg-info                       [   4.9K]
```
