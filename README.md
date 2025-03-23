# Python CPU Instruction Set Simulator

## CLI interactive mode commands

- help

- registers
  - `RA`
    - print current contents of RA
  - `RA = n`
    - write to RA
    - accept decimal, hexadecimal, binary
  - extend to allow changing PC?
  - allow full register dump
- flags
  - allow setting flags?
- memory
  - `mem[address]`
    - print current contents of memory at address
  - `mem[address] = n`
    - write to memory at address
    - accept decimal, hexadecimal, binary
  - allow entire memory dump
- disassembly
  - `dis RA`
  - `dis mem[addr]`
  - dump value within memory or register as an instruction
- step
  - allow running one (or more) instructions
  - `step [n]`
  - allow step until next breakpoint
- set breakpoint
  - conditional breakpoints?
- exit / quit / stop / halt


## GDB - aligned commands
- `info` `i`
  - `registers` `r`
  - `break` `b`
  - `memory` `m`

- `step` `s`
  - `N` - number of instructions to step
- `continue` `c` - run until next breakpoint is hit

- `break` `b`
  - `int` - when PC = val
  - `if cond`
- `delete` `d`
  - `n` - delete breakpoint with ID `n`
- `enable` `e`
  - `n` - enable breakpoint with ID `n`
- `disable`
  - `n` - disable breakpoint with ID `n`

- `quit` `q`
- `help`

- `disassemble` `dis`
  - register name
  - address (hex)
- `print` `p`
  - format specifier?
  - register name
  - memory address

TODO - consider implementing assembler with debug symbols
