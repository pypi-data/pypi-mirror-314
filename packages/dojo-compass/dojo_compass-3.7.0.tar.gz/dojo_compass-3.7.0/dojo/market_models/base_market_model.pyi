import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.agents import MarketAgent as MarketAgent
from dojo.observations import BaseObservation as BaseObservation
from typing import Any, Generic, TypeVar

Action = TypeVar('Action', bound=BaseAction[Any])
Observation = TypeVar('Observation', bound=BaseObservation)

class BaseMarketModel(ABC, Generic[Action, Observation], metaclass=abc.ABCMeta):
    agent: Incomplete
    def __init__(self, market_agent: MarketAgent) -> None: ...
    @abstractmethod
    def predict(self, obs: Observation, agents_actions: list[Action]) -> list[Action]: ...
