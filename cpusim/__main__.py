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
import argparse
import typing as t

from cpusim.common import parser
from cpusim.frontend import cli

root_parser = argparse.ArgumentParser()
root_subparsers = root_parser.add_subparsers(dest="command")

root_parser.add_argument("file", action="store", metavar="FILE", help="the .dat file to simulate")

cli_parser = root_subparsers.add_parser(
    "cli",
    help="simulate a .dat file in CLI mode",
)
cli_parser.add_argument(
    "--arch",
    "-a",
    action="store",
    choices=["1a", "1d"],
    help="the SimpleCPU architecture version to use - defaults to '1a'",
    default="1a",
)
cli_parser.add_argument(
    "--steps",
    "-s",
    action="store",
    nargs=1,
    type=int,
    metavar="N",
    help="the number of steps (instructions) to simulate",
)
cli_parser.add_argument(
    "--interactive",
    "-i",
    action="store_true",
    help="run in interactive mode - you will be able to run debug commands and step through instructions one-by-one",
)

gui_parser = root_subparsers.add_parser(
    "gui",
    help="simulate a .dat file in GUI mode",
)
gui_parser.add_argument(
    "--arch",
    "-a",
    action="store",
    choices=["1a", "1d"],
    help="the SimpleCPU architecture version to use - defaults to '1a'",
    default="1a",
)


class CliArguments(argparse.Namespace):
    file: str
    command: t.Literal["cli", "gui"]
    arch: t.Literal["1a", "1d"] | None
    steps: int | None
    interactive: bool


args = root_parser.parse_args(namespace=CliArguments())

file = args.file if args.file.endswith(".dat") else (args.file + ".dat")
with open(file) as f:
    machine_code = parser.parse_dat_file(f.read())

if args.command == "cli":
    cli.run_cli(args, machine_code)
