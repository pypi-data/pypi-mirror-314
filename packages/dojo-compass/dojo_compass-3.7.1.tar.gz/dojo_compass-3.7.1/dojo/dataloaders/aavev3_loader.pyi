from _typeshed import Incomplete
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.dataloaders.base_loader import BaseLoader as BaseLoader

class AaveV3Loader(BaseLoader):
    file_paths: Incomplete
    def __init__(self, chain: Chain, block_range: tuple[int, int]) -> None: ...
