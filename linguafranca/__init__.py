from typing import Protocol, runtime_checkable

@runtime_checkable
class Command(Protocol):
	tagged: bool = True
