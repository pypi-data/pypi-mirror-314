# okmodule: a very simple modular implementation

## Installation

```shell
pip install okmodule
```

## Usage

```python
from okmodule import Module, Command


class MyModule(Module):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def main(self):
        return self.x + self.y


class Blastn(Command):
    def __init__(self, query, db, out):
        self.query = query
        self.db = db
        self.out = out

    def args(self):
        return [
            '-query', self.query,
            '-db', self.db,
            '-out', self.out
        ]


my_module = MyModule(1, 2)
print(my_module())

blastn = Blastn('foo', 'bar', 'baz')
blastn()
```