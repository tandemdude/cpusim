# Copyright (c) 2024-present tandemdude
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__all__ = ["root_parser"]

import argparse
import typing as t

from cpusim.frontend.cli.interactive import converters


def _default_parser_args(description: str) -> dict[str, t.Any]:
    return {
        "help": description,
        "description": description,
        "exit_on_error": False,
        "add_help": False,
    }


class _CustomHelpAction(argparse.Action):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        kwargs.setdefault("nargs", 0)
        super().__init__(*args, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | t.Sequence[t.Any] | None,
        option_string: str | None = None,
    ) -> None:
        parser.print_help()
        namespace.help = True

    @classmethod
    def add_to(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-h", "--help", action=cls)


root_args = _default_parser_args("SimpleCPU assembly debugger (adb)")
del root_args["help"]

root_parser = argparse.ArgumentParser(prog="(idb)", **root_args)
_CustomHelpAction.add_to(root_parser)

subparsers = root_parser.add_subparsers(title="commands", dest="command")

# quit command
quit_parser = subparsers.add_parser("quit", **_default_parser_args("Quit the simulation"))
_CustomHelpAction.add_to(quit_parser)

# info command
info_parser = subparsers.add_parser("info", **_default_parser_args("Show information about simulation state"))
_CustomHelpAction.add_to(info_parser)

info_parser.add_argument(
    "item",
    metavar="ITEM",
    type=str,
    choices=["registers", "breakpoints", "memory", "flags"],
    help="The item to show state for",
)

# step command
step_parser = subparsers.add_parser("step", **_default_parser_args("Step the simulation by one or more instructions"))
_CustomHelpAction.add_to(step_parser)

step_parser.add_argument(
    "number", metavar="N", type=int, nargs="?", default=1, help="The number of instructions to step - defaults to 1"
)

# continue command
continue_parser = subparsers.add_parser(
    "continue", **_default_parser_args("Continue the simulation until a breakpoint triggers, or the CPU halts")
)
_CustomHelpAction.add_to(continue_parser)

# breakpoint command
breakpoint_parser = subparsers.add_parser("breakpoint", **_default_parser_args("Manage simulation breakpoints"))
_CustomHelpAction.add_to(breakpoint_parser)

breakpoint_subparsers = breakpoint_parser.add_subparsers(title="subcommands", dest="breakpoint_subcommand")

# - breakpoint create command
breakpoint_create_parser = breakpoint_subparsers.add_parser(
    "create", **_default_parser_args("Create a new program-counter or conditional breakpoint")
)
_CustomHelpAction.add_to(breakpoint_create_parser)

grp = breakpoint_create_parser.add_mutually_exclusive_group(required=True)
grp.add_argument(
    "--expr", nargs=argparse.REMAINDER, help="The conditional breakpoint expression", dest="breakpoint_create_expr"
)
grp.add_argument(
    "--line",
    metavar="PC",
    type=converters.number_string_to_int,
    help="The value of the program counter to set the breakpoint for",
    dest="breakpoint_create_line",
)

# - breakpoint delete command
breakpoint_delete_parser = breakpoint_subparsers.add_parser("delete", **_default_parser_args("Delete a breakpoint"))
_CustomHelpAction.add_to(breakpoint_delete_parser)

breakpoint_delete_parser.add_argument("id", metavar="ID", type=int, help="Breakpoint ID")

# - breakpoint enable command
breakpoint_enable_parser = breakpoint_subparsers.add_parser("enable", **_default_parser_args("Enable a breakpoint"))
_CustomHelpAction.add_to(breakpoint_enable_parser)

breakpoint_enable_parser.add_argument("id", metavar="ID", type=int, help="Breakpoint ID")

# - breakpoint disable command
breakpoint_disable_parser = breakpoint_subparsers.add_parser("disable", **_default_parser_args("Disable a breakpoint"))
_CustomHelpAction.add_to(breakpoint_disable_parser)

breakpoint_disable_parser.add_argument("id", metavar="ID", type=int, help="Breakpoint ID")

# disassemble command
disassemble_parser = subparsers.add_parser(
    "disassemble", **_default_parser_args("Disassemble the value at the given address/register")
)
_CustomHelpAction.add_to(disassemble_parser)

disassemble_parser.add_argument(
    "target", metavar="TARGET", type=converters.parse_address_or_register, help="Target address or register"
)

# print command
print_parser = subparsers.add_parser("print", **_default_parser_args("Print the value at the given address/register"))
_CustomHelpAction.add_to(print_parser)

print_parser.add_argument(
    "target", metavar="TARGET", type=converters.parse_address_or_register, help="Target address or register"
)


class Arguments(argparse.Namespace):
    help: bool | None
    command: t.Literal["quit", "info", "step", "continue", "breakpoint", "disassemble", "print"] | None
    item: t.Literal["registers", "breakpoints", "memory", "flags"] | None
    number: int | None
    breakpoint_subcommand: t.Literal["create", "delete", "enable", "disable"] | None
    breakpoint_create_expr: list[str] | None
    breakpoint_create_line: int | None
    id: int | None
    target: converters.Address | converters.Register | None


def parse_args(args: list[str]) -> Arguments:
    return root_parser.parse_args(args, namespace=Arguments())
