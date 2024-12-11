from _typeshed import Incomplete
from dojo.actions import SleepAction as SleepAction
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.actions.gmxV2.keeper_actions.models import GmxExecuteOrder as GmxExecuteOrder, GmxKeeperAction as GmxKeeperAction
from dojo.environments import AAVEv3Env as AAVEv3Env, UniswapV3Env as UniswapV3Env
from dojo.environments.gmxV2 import GmxV2Env as GmxV2Env
from dojo.observations import AAVEv3Observation as AAVEv3Observation, GmxV2Observation as GmxV2Observation, UniswapV3Observation as UniswapV3Observation
from dojo.policies.base_policy import BasePolicy as BasePolicy
from typing import Any, Literal

logger: Incomplete

def backtest_run(env: UniswapV3Env | AAVEv3Env | GmxV2Env, policies: list[BasePolicy[Any, Any, Any]], *, output_file: str | None = None, dashboard_server_port: int | None = None, transaction_order: Literal['market_first', 'agent_first', 'fee'] = 'market_first', auto_close: bool = True, simulation_status_bar: bool = False, simulation_title: str = 'no title', simulation_description: str = 'no description') -> None: ...
