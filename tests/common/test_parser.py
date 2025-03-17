from cpusim.common import parser

EXAMPLE_FILE = """
0000 0000000000000001
0001 0000000000000010
0002 0000000000000011
0003 0000000000000100
0004 0000000000000101
0005 0000000000000110
0006 0000000000000111
0007 0000000000001000
"""


def test_parses_file_correctly() -> None:
    lines = parser.parse_dat_file(EXAMPLE_FILE)
    assert len(lines) == 8
    assert lines == [1, 2, 3, 4, 5, 6, 7, 8]
