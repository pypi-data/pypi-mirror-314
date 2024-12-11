import re
from datetime import timedelta
from typing import Dict, List, Optional

from .object import InvalidNameError


class Expression:
    """
    Root base class for all model-checker expressions. Provides
    pythonic magic-method sugar for expression definitions.

    """

    def model_names(self):
        raise NotImplementedError()

    def as_json(self):
        raise NotImplementedError()

    def one_of(self, *values):
        return BinOp("in", self, list(values))

    def __gt__(self, other):
        return BinOp(">", self, Expression.from_py(other))

    def __ge__(self, other):
        return BinOp(">=", self, Expression.from_py(other))

    def __eq__(self, other):
        return BinOp("==", self, Expression.from_py(other))

    def __lt__(self, other):
        return BinOp("<", self, Expression.from_py(other))

    def __le__(self, other):
        return BinOp("<=", self, Expression.from_py(other))

    def __add__(self, other):
        return BinOp("+", self, Expression.from_py(other))

    def __sub__(self, other):
        return BinOp("-", self, Expression.from_py(other))

    @classmethod
    def from_py(cls, value):
        """Creates an :py:Expression: from a given python `value`."""
        if isinstance(value, Expression):
            return value
        elif any(isinstance(value, T) for T in (float, int, list, str, timedelta)):
            return Value(value)
        else:
            raise RuntimeError("invalid expression for bounds checking", value)

    def top_json(self) -> Dict[str, object]:
        """Creates a top-level expression that can be passed to the model
        checker runtime.
        """
        return {
            "root": self.as_json(),
            "required_data": [{"name": mn} for mn in self.model_names()],
        }


class Function(Expression):
    def __init__(self, op, args):
        self.op = op
        self.args = [Expression.from_py(a) for a in args]

    def model_names(self):
        return [mn for a in self.args for mn in a.model_names()]

    def as_json(self):
        return {
            "node": "fn",
            "fn": self.op,
            "arguments": [a.as_json() for a in self.args],
        }


class BinOp(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = Expression.from_py(left)
        self.right = Expression.from_py(right)

    def model_names(self):
        return [mn for a in (self.left, self.right) for mn in a.model_names()]

    def as_json(self):
        return {
            "node": "binop",
            "op": self.op,
            "left": self.left.as_json(),
            "right": self.right.as_json(),
        }


class Variable(Expression):
    """Declares a model variable that can be used as an :py:Expression: in the
    model checker. Variables are identified by their `model_name`, a `position`
    of either `"input"` or `"output"`, and the tensor `index`.
    """

    def __init__(self, model_name, position, index):
        self.model_name = model_name
        self.position = position
        self.index = index

    def model_names(self):
        return [self.model_name]

    def __getitem__(self, index):
        assert isinstance(index, int)
        return Variable(self.model_name, self.position, [*self.index, index])

    def as_json(self):
        return {
            "node": "variable",
            "variant_id": {"name": self.model_name},
            "position": self.position,
            "key": self.index,
        }


def value_to_node(value):
    if isinstance(value, int):
        return {"node": "literal", "integer": value}
    if isinstance(value, str):
        return {"node": "literal", "timedelta": value}
    if isinstance(value, timedelta):
        seconds = int(value.total_seconds())
        assert seconds >= 1
        return {"node": "literal", "timedelta": f"{seconds}s"}
    if isinstance(value, float):
        return {"node": "literal", "float": value}
    if isinstance(value, list):
        return {"node": "literal", "list": [value_to_node(i) for i in value]}
    if isinstance(value, Expression):
        return value.as_json()
    raise RuntimeError("invalid type", type(value))


class Value(Expression):
    def __init__(self, value):
        self.value = value

    def model_names(self):
        return []

    def as_json(self):
        return value_to_node(self.value)


def is_prom_primitive(v):
    return isinstance(v, int) or isinstance(v, float)


class Aggregate:
    def __init__(
        self,
        name: str,
        promql_agg: str,
        inner_expression: Expression,
        duration: timedelta,
        bucket_size: Optional[timedelta],
    ):
        self.name = name
        self.promql_agg = promql_agg
        self.inner_expression = inner_expression
        self.duration = duration
        self.bucket_size = bucket_size

    def expression(self):
        args = [self.inner_expression, self.duration]
        if self.bucket_size is not None:
            args.append(self.bucket_size)
        return Function(self.name, args)

    def promql(self, gauge_name):
        return f"{self.promql_agg} by (pipeline_id) (pipeline_gauge:{gauge_name})"

    def __gt__(self, other):
        assert is_prom_primitive(other)
        return Alert(">", self, other)

    def __ge__(self, other):
        assert is_prom_primitive(other)
        return Alert(">=", self, other)

    def __eq__(self, other):
        assert is_prom_primitive(other)
        return Alert("==", self, other)

    def __lt__(self, other):
        assert is_prom_primitive(other)
        return Alert("<", self, other)

    def __le__(self, other):
        assert is_prom_primitive(other)
        return Alert("<=", self, other)


class Alert:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def promql(self, gauge_name):
        return f"{self.left.promql(gauge_name)} {self.op} {self.right}"


class DefinedFunction:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        return Function(self.name, args)


class DefinedAggregate:
    def __init__(self, name: str, promql_agg):
        self.name = name
        self.promql_agg = promql_agg

    def __call__(
        self,
        expression: Expression,
        duration: timedelta,
        bucket_size: Optional[timedelta] = None,
    ):
        return Aggregate(self.name, self.promql_agg, expression, duration, bucket_size)


class Variables:
    def __init__(self, model, position):
        self.model = model
        self.position = position

    def __getitem__(self, index):
        assert isinstance(index, int)
        return Variable(self.model, self.position, [index])


def instrument(
    values: Dict[str, Expression], gauges: List[str], validations: List[str]
):
    return {
        "values": {name: e.top_json() for name, e in values.items()},
        "gauges": gauges,
        "validations": [] if len(gauges) > 0 else validations,
    }


# Cache for the validation regex
_dns_req = None


def dns_compliant(name: str):
    """Returns true if a string is compliant with DNS label name requirement to
    ensure it can be a part of a full DNS host name
    """
    global _dns_req
    if not _dns_req:
        # https://en.wikipedia.org/wiki/Domain_Name_System
        _dns_req = re.compile("^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]*$")

    return len(name) < 64 and _dns_req.match(name) is not None and name[-1] != "-"


def require_dns_compliance(name: str):
    """Validates that 'name' complies with DNS naming requirements or raises an exception"""
    if not dns_compliant(name):
        raise InvalidNameError(
            name, "must be DNS-compatible (ASCII alpha-numeric plus dash (-))"
        )
