import pathlib
import select
import sys
from typing import Any, Callable, Literal, TextIO, TypeVar, Union, cast
import click
from contextlib import nullcontext

FC = TypeVar("FC", bound=Union[Callable[..., Any], click.Command])


class Input:
    def __init__(
        self,
        name: str = "input",
        flag="i",
        help="Input File Path",
    ):
        self.name = name
        self.flag = flag
        self.help = help

    def option(
        self, file_or_dir: Literal["file", "dir"] = "file"
    ) -> Callable[[FC], FC]:
        return click.option(
            f"--{self.name}",
            f"-{self.flag}",
            type=click.Path(
                exists=True if file_or_dir == "file" else False,
                path_type=pathlib.Path,
                readable=True,
                dir_okay=file_or_dir == "dir",
                file_okay=file_or_dir == "file",
            ),
            help=f"{self.help}, defaults to STDIN if not specified",
            default=None,
        )

    def open(self, arg: pathlib.Path | None, immediate: bool = False) -> TextIO:
        if arg is None:
            if immediate and not select.select([sys.stdin], [], [], 0.0)[0]:
                raise click.ClickException(
                    f"No input provided. Either use '--{self.name}/-{self.flag}' or pipe input through STDIN."
                )

            # Wrap stdin in nullcontext to prevent closing
            return cast(TextIO, nullcontext(sys.stdin))
        else:
            return arg.open()


class Output:
    def __init__(
        self,
        name: str = "output",
        flag="o",
        help="Output File Path",
    ):
        self.name = name
        self.flag = flag
        self.help = help

    def option(
        self, file_or_dir: Literal["file", "dir"] = "file"
    ) -> Callable[[FC], FC]:
        return click.option(
            f"--{self.name}",
            f"-{self.flag}",
            type=click.Path(
                path_type=pathlib.Path,
                writable=True,
                dir_okay=file_or_dir == "dir",
                file_okay=file_or_dir == "file",
            ),
            help=f"{self.help}, defaults to STDOUT if not specified",
            default=None,
        )

    def open(self, arg: pathlib.Path | None) -> TextIO:
        if arg is None:
            # Wrap stdout in nullcontext to prevent closing
            return cast(TextIO, nullcontext(sys.stdout))
        else:
            return arg.open("w")
