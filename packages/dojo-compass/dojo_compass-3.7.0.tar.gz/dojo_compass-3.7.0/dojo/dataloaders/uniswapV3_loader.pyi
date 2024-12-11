from _typeshed import Incomplete
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.dataloaders.base_loader import BaseLoader as BaseLoader
from dojo.dataloaders.exceptions import MissingIngestedData as MissingIngestedData
from dojo.dataloaders.formats import Event as Event, UniswapV3Burn as UniswapV3Burn, UniswapV3Collect as UniswapV3Collect, UniswapV3Initialize as UniswapV3Initialize, UniswapV3Mint as UniswapV3Mint, UniswapV3Swap as UniswapV3Swap
from dojo.utils import disk_cache as disk_cache

class UniswapV3Loader(BaseLoader):
    pools: Incomplete
    def __init__(self, chain: Chain, block_range: tuple[int, int], pools: list[str]) -> None: ...
