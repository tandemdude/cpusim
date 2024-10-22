# -*- coding: utf-8 -*-
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

root_parser = argparse.ArgumentParser()
root_subparsers = root_parser.add_subparsers(dest="command")

dis_parser = root_subparsers.add_parser(
    "dis",
    help="disassemble a .dat file and inspect its assembly code",
    epilog="NOTE: this may not correctly disassemble the '.data' directives if a value has the same format as a valid instruction"
)
dis_parser.add_argument(
    "file",
    action="store",
    nargs=1,
    metavar="FILE",
    help="the .dat file to disassemble"
)

cli_parser = root_subparsers.add_parser(
    "cli",
    help="simulate a given .dat file in CLI mode"
)
cli_parser.add_argument(
    "file",
    action="store",
    nargs=1,
    metavar="FILE",
    help="the .dat file to simulate"
)
cli_parser.add_argument(
    "--steps",
    "-s",
    action="store",
    nargs=1,
    type=int,
    help="the number of steps (instructions) to simulate"
)
cli_parser.add_argument(
    "--breakpoints",
    "-b",
    action="store",
    nargs="*",
    type=int,
    help="line numbers where breakpoints will be placed"
)
cli_parser.add_argument(
    "--interactive",
    "-i",
    action="store_true",
    help="run in interactive mode - you will be able to run debug commands and step through instructions one-by-one"
)

gui_parser = root_subparsers.add_parser(
    "gui",
    help="simulate a given .dat file in GUI mode"
)
gui_parser.add_argument(
    "file",
    action="store",
    nargs=1,
    metavar="FILE",
    help="the .dat file to simulate"
)

args = root_parser.parse_args()
