from typing import Optional, TypeVar

T = TypeVar("T")


# Removes the Optional wrapper.
def unwrap(v: Optional[T]) -> T:
    """Simple function to placate pylance"""
    if v:
        return v
    raise Exception("Expected a value in forced unwrap")
