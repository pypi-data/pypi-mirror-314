from dojo.observations.aaveV3 import *
from dojo.observations.uniswapV3 import *
from _typeshed import Incomplete
from datetime import datetime
from decimal import Decimal
from dojo import money as money
from dojo.actions.aaveV3 import AAVEv3Borrow as AAVEv3Borrow, AAVEv3BorrowToHealthFactor as AAVEv3BorrowToHealthFactor, AAVEv3FlashLoan as AAVEv3FlashLoan, AAVEv3FlashLoanSimple as AAVEv3FlashLoanSimple, AAVEv3FullLiquidation as AAVEv3FullLiquidation, AAVEv3Liquidation as AAVEv3Liquidation, AAVEv3Repay as AAVEv3Repay, AAVEv3RepayAll as AAVEv3RepayAll, AAVEv3RepayToHealthFactor as AAVEv3RepayToHealthFactor, AAVEv3Supply as AAVEv3Supply, AAVEv3Withdraw as AAVEv3Withdraw, AAVEv3WithdrawAll as AAVEv3WithdrawAll, BaseAaveAction as BaseAaveAction
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.config.data.aave_config import aave_supported_tokens as aave_supported_tokens
from dojo.dataloaders import AaveV3Loader as AaveV3Loader
from dojo.environments.base_environments import BaseEnvironment as BaseEnvironment
from dojo.market_models.aaveV3 import AaveV3DefaultModel as AaveV3DefaultModel
from dojo.money.format import to_machine_format as to_machine_format
from dojo.network.constants import MAX_UINT256 as MAX_UINT256
from dojo.utils.debug_errors import debug_aave_error as debug_aave_error
from enum import Enum
from typing import Literal
from web3.types import PendingTx as PendingTx

logger: Incomplete

class AaveV3MarketModelType(Enum):
    DEFAULT = 'default'

class AAVEv3Env(BaseEnvironment[BaseAaveAction, AAVEv3Observation]):
    AgentT = BaseAgent[AAVEv3Observation]
    obs: Incomplete
    market_model: Incomplete
    def __init__(self, chain: Chain, agents: list[AgentT], block_range: tuple[int, int], backend_type: Literal['forked', 'local', 'live'] = 'forked', port: int | None = None, token_data: dict[str, dict[datetime, Decimal]] | None = None, market_impact: Literal['default'] = 'default') -> None: ...
    def initialize_state(self) -> None: ...
    def setup_contracts_forked(self) -> list[str]: ...
    def initReserves(self, treasury_address: str) -> None: ...
    def configureReserves(self) -> None: ...
    aave_sim_tokens: Incomplete
    ReservesConfig: Incomplete
    def setup_contracts_local(self) -> list[str]: ...
