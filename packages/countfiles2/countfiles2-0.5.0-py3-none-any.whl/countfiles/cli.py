import argparse

from countfiles import __version__
from countfiles.node import SortBy, Tree


def cli():
    parser = argparse.ArgumentParser(prog="countfiles", description="Show accumulated number of files per directory.")

    parser.add_argument("path", type=str, default=".", nargs="?")
    parser.add_argument(
        "--max-depth", "-d", type=int,
        help="Iterate all the way, but only show directories down to this depth."
    )
    parser.add_argument(
        "--min-filecount", "-m", type=int,
        help="Iterate all the way, but only show directories with this number of files or more."
    )
    parser.add_argument("--sizes", "-s", action="store_true", help="Also show the total size of every directory.")
    parser.add_argument("--count-dirs", "-c", action="store_true", help="Also include directories in the file counts.")
    parser.add_argument("--reverse", "-r", action="store_true", help="Reverse result sorting.")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--no-hidden", action="store_true", help="Ignore hidden files and folders.")
    parser.add_argument("--version", "-V", action="version", version="%(prog)s " + __version__)
    parser.add_argument(
        "--symlinks",
        "-ln",
        action="store_true",
        help="Follow symlinks (will throw exception if an infinite recursion is detected).",
    )

    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument("--sort-count", "-sc", action="store_true", help="Sort results by file count.")
    sort_group.add_argument("--sort-size", "-ss", action="store_true", help="Sort results by total size.")

    args = parser.parse_args()

    sort_by = SortBy.NAME
    if args.sort_count:
        sort_by = SortBy.FILECOUNT
    elif args.sort_size:
        sort_by = SortBy.SIZE

    tree = Tree(
        path=args.path,
        count_dirs=args.count_dirs,
        show_sizes=args.sizes,
        max_depth=args.max_depth,
        min_filecount=args.min_filecount,
        color=not args.no_color,
        sort_by=sort_by,
        reverse=args.reverse,
        symlinks=args.symlinks,
        hidden=not args.no_hidden,
    )
    print(str(tree))


if __name__ == "__main__":
    cli()
