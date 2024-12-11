from dojo.actions.base_action import BaseAction as BaseAction
from dojo.agents import MarketAgent as MarketAgent
from dojo.market_models import BaseMarketModel as BaseMarketModel
from dojo.observations import BaseObservation as BaseObservation
from typing import Any, TypeVar

Action = TypeVar('Action', bound=BaseAction[Any])

class NoMarket(BaseMarketModel[Action, Any]):
    def __init__(self, market_agent: MarketAgent) -> None: ...
    def predict(self, obs: BaseObservation, agents_actions: list[Action]) -> list[Action]: ...
