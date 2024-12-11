from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.aaveV3 import AAVEv3Borrow as AAVEv3Borrow, AAVEv3FullLiquidation as AAVEv3FullLiquidation, AAVEv3Supply as AAVEv3Supply, BaseAaveAction as BaseAaveAction
from dojo.agents import MarketAgent as MarketAgent
from dojo.market_models.base_market_model import BaseMarketModel as BaseMarketModel
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation

@dataclass
class _TokenAndAmount:
    token_name: str
    amount: Decimal
    def __init__(self, token_name, amount) -> None: ...

@dataclass
class _UserData:
    collaterals: list[_TokenAndAmount]
    borrows: list[_TokenAndAmount]
    def __init__(self, collaterals, borrows) -> None: ...

class AaveV3DefaultModel(BaseMarketModel[BaseAaveAction, AAVEv3Observation]):
    DEFAULT_GAS: int
    userdata: Incomplete
    def __init__(self, market_agent: MarketAgent) -> None: ...
    def predict(self, obs: AAVEv3Observation, agents_actions: list[BaseAaveAction]) -> list[BaseAaveAction]: ...
