from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from dojo.common.constants import Chain as Chain
from dojo.config.data.gmx_tokens.arbitrum import ARBITRUM_TOKENS as ARBITRUM_TOKENS
from dojo.config.data.gmx_tokens.avalanche import AVALANCHE_TOKENS as AVALANCHE_TOKENS
from dojo.config.deployments import get_all_gmx_markets as get_all_gmx_markets
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS

@dataclass
class MarketVenue:
    index_token: str
    long_token: str
    short_token: str
    def all_tokens(self) -> list[str]: ...
    @property
    def market_key(self) -> str: ...
    def __init__(self, index_token, long_token, short_token) -> None: ...

@dataclass
class Token(DataClassJsonMixin):
    symbol: str
    address: str
    decimals: int
    is_synthetic: bool = ...
    def __init__(self, *generated_args, symbol, address, decimals, is_synthetic=..., **generated_kwargs) -> None: ...

@dataclass
class Market(DataClassJsonMixin):
    long_token: Token
    short_token: Token
    market_token: Token
    index_token: Token = ...
    @property
    def market_key(self) -> str: ...
    def __init__(self, *generated_args, long_token, short_token, market_token, index_token=..., **generated_kwargs) -> None: ...
