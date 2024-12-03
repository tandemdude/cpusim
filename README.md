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
