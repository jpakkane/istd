# Import std test system

An experiment to see if `import std` could be implemented in a simple
single-command kind of way.

To use this do something like:

    ./builder.py src -- -std=c++23

to build in the regular way and:

    ./builder.py srcistd -- -std=c++23 (/std:c++latest with VS)

to use `import std`.

Flags after `--` are passed directly to the compiler command line.
