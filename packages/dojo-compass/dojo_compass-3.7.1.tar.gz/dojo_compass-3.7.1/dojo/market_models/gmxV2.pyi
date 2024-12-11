from _typeshed import Incomplete
from collections import defaultdict
from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction as BaseGmxAction
from dojo.agents import MarketAgent as MarketAgent
from dojo.market_models.base_market_model import BaseMarketModel as BaseMarketModel
from dojo.observations.gmxV2 import GmxV2Observation as GmxV2Observation

class GmxV2ReplayModel(BaseMarketModel[BaseGmxAction, GmxV2Observation]):
    replay_events: Incomplete
    def __init__(self, market_agent: MarketAgent, replay_events: defaultdict[int, list[BaseGmxAction]] | None = None) -> None: ...
    def predict(self, obs: GmxV2Observation, agents_actions: list[BaseGmxAction]) -> list[BaseGmxAction]: ...
