from dataclasses import dataclass

from .types_compute import *

from . import Command

@dataclass
class CreateComputeCluster(Command):
	name: ComputeClusterRef

@dataclass
class DeleteComputeCluster(Command):
	name: ComputeClusterRef
