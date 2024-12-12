import enum
import locale
import math
import os

import colorama
from colorama import Fore, Style


KILOBYTE = pow(2, 10)
MEGABYTE = pow(2, 20)
GIGABYTE = pow(2, 30)
TERABYTE = pow(2, 40)


def format_size(size: int) -> str:
    if size >= TERABYTE:
        return locale.str(round(size / TERABYTE, 1)) + "T"
    if size >= GIGABYTE:
        return locale.str(round(size / GIGABYTE, 1)) + "G"
    if size >= MEGABYTE:
        return locale.str(round(size / MEGABYTE, 1)) + "M"
    if size >= KILOBYTE:
        return locale.str(round(size / KILOBYTE, 1)) + "K"
    return str(size)


class SortBy(enum.Enum):
    NAME = 1
    FILECOUNT = 2
    SIZE = 3


class OutputLine:
    text: str = ""
    colors: dict[int, str]

    def __init__(self, text: str = "", colors: dict[int, str] | None = None):
        self.text = text
        self.colors = colors or {}
        self.append_color(Style.RESET_ALL)

    @property
    def colored(self):
        text = self.text
        for pos in sorted(self.colors, reverse=True):
            text = text[:pos] + self.colors[pos] + text[pos:]
        return text

    @property
    def length(self):
        return len(self.text)

    def append(self, text: str, color: str = ""):
        if color:
            self.append_color(color)
        self.text += text
        if color:
            self.append_color(Style.RESET_ALL)

    def append_color(self, color: str):
        pos = len(self.text)
        if pos in self.colors:
            self.colors[pos] += color
        else:
            self.colors[pos] = color

    def clone(self):
        return OutputLine(text=self.text, colors=self.colors.copy())

    def truncate(self, max_length: int):
        if max_length >= len(self.text):
            return self
        return OutputLine(
            text=self.text[:max_length - 3] + "...",
            colors={k: v for k, v in self.colors.items() if k <= max_length - 3},
        )


class Node:
    children: "list[Node]"
    parent: str | None = None

    def __init__(self, root: str, files: list[str], dirs: list[str], root_fd: int, count_dirs: bool):
        self.root_size = sum(self.get_file_size(name, root_fd) for name in files)
        self.root_filecount = len(files)
        self.root_dircount = len(dirs)
        if len(root) > 1:
            self.root = root.rstrip("/")
        else:
            self.root = root
        self.basename = self.root.strip("/").split("/")[-1]
        self.children = []
        self.count_dirs = count_dirs
        parent = self.root[:-len(self.basename)]
        if len(parent) > 1:
            parent = parent.rstrip("/")
        if parent != self.root:
            self.parent = parent

    def __str__(self):
        return f"Node[root={self.root}, parent={self.parent}, basename={self.basename}]"

    @property
    def descendant_count(self) -> int:
        total = len(self.children)
        for child in self.children:
            total += child.descendant_count
        return total

    @property
    def filecount(self):
        fc = self.root_filecount + sum(c.filecount for c in self.children)
        if self.count_dirs:
            fc += self.root_dircount
        return fc

    @property
    def size(self):
        return self.root_size + sum(c.size for c in self.children)

    def get_file_size(self, name: str, root_fd: int):
        try:
            return os.stat(name, dir_fd=root_fd).st_size
        except FileNotFoundError:
            # Probably means a broken symlink
            return 0

    def is_parent_of(self, path: str):
        return "/".join(path.split("/")[:-1]) == self.root

    def prepare(
        self,
        depth: int = 0,
        max_depth: int | None = None,
        min_filecount: int | None = None,
        prefix: str = "",
        is_last_child: bool = False,
        sort_by: SortBy = SortBy.NAME,
        reverse: bool = False,
        show_sizes: bool = False,
    ) -> "PreparedNode":
        line = OutputLine()

        if depth:
            line.append(prefix)
            if is_last_child:
                line.append("└───")
            else:
                line.append("├───")

        line.append(f"[{str(self.filecount).rjust(6)}]  ")
        line.append(self.basename, color=Fore.LIGHTWHITE_EX + Style.BRIGHT)

        children = self.sort_and_filter_children(
            sort_by=sort_by,
            reverse=reverse,
            min_filecount=min_filecount,
            max_depth=max_depth,
            depth=depth,
        )

        not_shown = 0
        if max_depth and max_depth == depth + 1:
            not_shown = self.descendant_count
        elif len(self.children) > len(children):
            not_shown = len(self.children) - len(children)
        if not_shown == 1:
            line.append(" (1 child not shown)", color=Fore.LIGHTBLACK_EX)
        elif not_shown > 1:
            line.append(f" ({not_shown} children not shown)", color=Fore.LIGHTBLACK_EX)

        if not depth:
            child_prefix = ""
        elif is_last_child:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        return PreparedNode(
            col1=line,
            size=self.size,
            show_sizes=show_sizes,
            children=[
                child.prepare(
                    max_depth=max_depth,
                    min_filecount=min_filecount,
                    prefix=child_prefix,
                    is_last_child=idx == len(children) - 1,
                    sort_by=sort_by,
                    reverse=reverse,
                    show_sizes=show_sizes,
                    depth=depth + 1,
                ) for idx, child in enumerate(children)
            ],
        )

    def sort_and_filter_children(
        self,
        sort_by: SortBy,
        reverse: bool,
        depth: int,
        min_filecount: int | None,
        max_depth: int | None = None,
    ):
        def sort_func(child: "Node"):
            match sort_by:
                case SortBy.NAME:
                    return child.basename
                case SortBy.FILECOUNT:
                    return child.filecount
                case SortBy.SIZE:
                    return child.size

        if max_depth is not None and max_depth <= depth + 1:
            return []

        children = self.children

        if min_filecount:
            children = [c for c in children if c.filecount >= min_filecount]

        return sorted(children, key=sort_func, reverse=reverse)


class PreparedNode:
    def __init__(self, col1: OutputLine, size: int, show_sizes: bool, children: "list[PreparedNode]"):
        self.col1 = col1
        self.size = size
        self.show_sizes = show_sizes
        self.children = children

    @property
    def max_width(self):
        width = self.col1.length
        if self.show_sizes:
            width += 10
        return max([width, *[c.max_width for c in self.children]])

    def output(self, columns: int) -> list[OutputLine]:
        line = self.col1.clone().truncate(columns)
        lines = [line]

        if self.show_sizes:
            remaining_columns = columns - line.length
            line.append(f" [{format_size(self.size).rjust(7)}]".rjust(remaining_columns))

        for child in self.children:
            lines.extend(child.output(columns=columns))

        return lines


class Tree:
    _root: "Node"

    def __init__(
        self,
        path: str,
        count_dirs: bool = False,
        show_sizes: bool = False,
        max_depth: int | None = None,
        min_filecount: int | None = None,
        color: bool = True,
        sort_by: SortBy = SortBy.NAME,
        reverse: bool = False,
        symlinks: bool = False,
        hidden: bool = True,
    ):
        self.path = os.path.realpath(path)
        self.basename = path.rstrip("/").split("/")[-1]
        self.count_dirs = count_dirs
        self.show_sizes = show_sizes
        self.max_depth = max_depth
        self.min_filecount = min_filecount
        self.color = color
        self.sort_by = sort_by
        self.reverse = reverse
        self.symlinks = symlinks
        self.hidden = hidden

    def __str__(self):
        if self.color:
            colorama.init()
        prepared_root = self.root.prepare(
            max_depth=self.max_depth,
            min_filecount=self.min_filecount,
            sort_by=self.sort_by,
            reverse=self.reverse,
            show_sizes=self.show_sizes,
        )
        lines = prepared_root.output(columns=self.get_output_width(prepared_root))
        if self.color:
            return "\n".join(line.colored for line in lines)
        return "\n".join(line.text for line in lines)

    @property
    def root(self) -> "Node":
        if hasattr(self, "_root"):
            return self._root

        nodes: "dict[str, Node]" = {}
        seen_inodes: list[int] = []

        for root, dirs, files, root_fd in os.fwalk(self.path, follow_symlinks=self.symlinks):
            if not self.hidden:
                if root != self.path and os.path.basename(root).startswith("."):
                    continue
                files = [f for f in files if not f.startswith(".")]
                dirs = [d for d in dirs if not d.startswith(".")]

            if self.symlinks and os.path.islink(root):
                root_inode = os.lstat(root).st_ino
                if root_inode in seen_inodes:
                    raise RuntimeError(
                        f"Infinite recursion detected for symlink {root}; try again without --symlinks."
                    )

                seen_inodes.append(root_inode)
                target = os.path.realpath(os.path.join(os.path.dirname(root), os.readlink(root)))

                if target.startswith(self.path):
                    # Link target is already included in the selection and
                    # we don't want to count its contents twice:
                    continue

            node = Node(root=root, files=files, dirs=dirs, root_fd=root_fd, count_dirs=self.count_dirs)
            nodes[node.root] = node

            if not hasattr(self, "_root"):
                self._root = node
            if node.parent and node.parent in nodes:
                nodes[node.parent].children.append(node)

        return self._root

    def get_output_width(self, root: PreparedNode):
        try:
            max_width = os.get_terminal_size().columns
        except OSError:
            max_width = 80
        real_width = root.max_width
        if real_width >= max_width:
            return max_width
        return math.ceil(real_width / 10) * 10
