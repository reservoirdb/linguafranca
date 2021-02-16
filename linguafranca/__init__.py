from typing import Protocol, runtime_checkable

@runtime_checkable
class Command(Protocol):
	tagged: bool = True

@runtime_checkable
class TxnResult(Protocol):
	tagged: bool = True
