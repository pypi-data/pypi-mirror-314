# okreport: simple report automatic rendering

## Installation

```shell
pip install python-okreport
```

## Usage

```python
from okreport import Var, Paragraph, Report

class ResultX(Var):
    def parse(self, result, conf, env):  # noqa
        return result['x']
    
    
class ResultY(Var):
    def parse(self, result, conf, env):  # noqa
        return result['y']
    
    
class ResultSum(Var):
    def parse(self, result, conf, env):  # noqa
        return result['x'] + result['y']

class ConfX(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['x']


class ConfY(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['y']


class ConfSum(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['x'] + conf['y']
    
    
class ResultParagraph(Paragraph):
    """
    In result, x = {{ x }}, y = {{ y }}, sum is {{ sum }}.
    """
    x = ResultX()
    y = ResultY()
    sum = ResultSum()


class ConfParagraph(Paragraph):
    """
    In conf, x = {{ x }}, y = {{ y }}, sum is {{ sum }}.
    """
    x = ConfX()
    y = ConfY()
    sum = ConfSum()


class MyReport(Report):
    """
    {{ p1 }}
    {{ p2 }}
    """
    p1 = ResultParagraph()
    p2 = ConfParagraph()


result = {'x': 1, 'y': 2}
conf = {'x': 3, 'y': 4}
my_report = MyReport()
text = my_report.render(result, conf, None)
print(text)
```