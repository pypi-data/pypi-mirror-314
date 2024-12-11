from .checks import DefinedAggregate, DefinedFunction

abs = DefinedFunction("abs")
count = DefinedAggregate("count", "sum")
