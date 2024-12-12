#!/bin/bash

##############################################################################
# jsonexpr test code
# https://github.com/markuskimius/jsonexpr
#
# Copyright (c)2024 Mark K. Kim
# Released under the Apache license 2.0
# https://github.com/markuskimius/jsonexpr/blob/master/LICENSE
##############################################################################

##############################################################################
# BOOTSTRAP
#
# Include ../lib in the search path then call python3 or python.
# (Thanks to https://unix.stackexchange.com/questions/20880)
#
if "true" : '''\'
then
    export PYTHONPATH="$(dirname $0)/../lib:$PYTHONPATH"
    pythoncmd=python

    if command -v python3 >/dev/null; then
        pythoncmd=python3
    fi

    exec "$pythoncmd" "$0" "$@"
    exit 127
fi
'''

##############################################################################
# PYTHON CODE BEGINS HERE

import sys
import json
import errno
import jsonexpr as je

def main():
    compiled = je.compile("""
        PRINT("I have " + LEN(grades) + " students");
        PRINT("Alice's grade is " + grades.alice);
    """)

    compiled.setSymbols({
        "grades" : {
            "alice" : "A",
            "bob"   : "B",
        }
    })

    result = compiled.eval()
    # print(type(result), result)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit(errno.EOWNERDEAD)

