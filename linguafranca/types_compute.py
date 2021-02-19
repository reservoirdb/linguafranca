from dataclasses import dataclass

from . import TxnResult

@dataclass(frozen = True)
class ComputeClusterRef(str):
	pass

@dataclass
class ComputeCluster(TxnResult):
	pass
