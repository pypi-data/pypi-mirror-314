from _typeshed import Incomplete
from dojo import money as money
from dojo.actions.aaveV3 import AAVEv3FullLiquidation as AAVEv3FullLiquidation, BaseAaveAction as BaseAaveAction
from dojo.actions.uniswapV3 import LowLevelUniswapV3Trade as LowLevelUniswapV3Trade, UniswapV3Action as UniswapV3Action, UniswapV3Quote as UniswapV3Quote
from dojo.agents import MarketAgent as MarketAgent
from dojo.dataloaders.formats import Event as Event, UniswapV3Burn as UniswapV3Burn, UniswapV3Mint as UniswapV3Mint, UniswapV3Swap as UniswapV3Swap
from dojo.market_models.base_market_model import BaseMarketModel as BaseMarketModel
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation
from dojo.observations.uniswapV3 import UniswapV3Observation as UniswapV3Observation

class UniswapV3ReplayModel(BaseMarketModel[UniswapV3Action, UniswapV3Observation]):
    DEFAULT_GAS: int
    replay_events: Incomplete
    def __init__(self, market_agent: MarketAgent, replay_events: list[Event]) -> None: ...
    def predict(self, obs: UniswapV3Observation, agents_actions: list[UniswapV3Action]) -> list[UniswapV3Action]: ...

class AaveV3DefaultModel(BaseMarketModel[BaseAaveAction, AAVEv3Observation]):
    DEFAULT_GAS: int
    tracked_users: Incomplete
    def __init__(self, market_agent: MarketAgent) -> None: ...
    def predict(self, obs: AAVEv3Observation, agents_actions: list[BaseAaveAction]) -> list[BaseAaveAction]: ...
