import abc
from _typeshed import Incomplete
from decimal import Decimal
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import UniswapV3Observation as UniswapV3Observation

class UniswapV3Agent(BaseAgent[UniswapV3Observation], metaclass=abc.ABCMeta):
    def get_liquidity_ownership_tokens(self) -> list[int]: ...
    def total_wealth(self, obs: UniswapV3Observation, unit_token: str) -> float: ...

class TotalWealthAgent(UniswapV3Agent):
    unit_token: Incomplete
    def __init__(self, initial_portfolio: dict[str, Decimal], unit_token: str, name: str | None = None) -> None: ...
    def reward(self, obs: UniswapV3Observation) -> float: ...
