import abc
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import AAVEv3Observation as AAVEv3Observation

class AAVEv3Agent(BaseAgent[AAVEv3Observation], metaclass=abc.ABCMeta): ...
