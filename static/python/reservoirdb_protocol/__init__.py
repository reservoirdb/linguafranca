from dataclasses import dataclass
from typing_extensions import Protocol

class Command(Protocol):
	pass

class TxnResult(Protocol):
	pass

@dataclass
class TaggedCommand:
	type: str
	params: Command

@dataclass
class TaggedTxnResult:
	type: str
	data: TxnResult
