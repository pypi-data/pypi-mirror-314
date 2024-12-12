# jsonexpr for Python

This document describes using jsonexpr with Python.
For the language overview, see the [main page](https://github.com/markuskimius/jsonexpr).


## Installation

```sh
pip3 install jsonexpr
```

Python 3.8 and later are supported.


## Example

```python
import jsonexpr

compiled = jsonexpr.compile("""
    PRINT("I have " + LEN(grades) + " students");
    PRINT("Alice's grade is " + grades.alice);
""")

compiled.setSymbols({
    "grades" : {
        "alice" : "A",
        "bob"   : "B",
    }
});

result = compiled.eval()
```

Output:

```
I have 2 students
Alice's grade is A
```


## License

[Apache 2.0](https://github.com/markuskimius/jsonexpr/blob/main/LICENSE)

