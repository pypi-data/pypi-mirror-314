from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation
from typing import Literal

BaseAaveAction = BaseAction[AAVEv3Observation]

@dataclass
class AAVEv3Supply(BaseAaveAction):
    token: str
    amount: Decimal
    def __init__(self, token, amount, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Withdraw(BaseAaveAction):
    token: str
    amount: Decimal
    def __init__(self, token, amount, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3WithdrawAll(BaseAaveAction):
    token: str
    def __init__(self, token, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Borrow(BaseAaveAction):
    token: str
    amount: Decimal
    mode: Literal['stable', 'variable']
    def __init__(self, token, amount, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3BorrowToHealthFactor(BaseAaveAction):
    token: str
    factor: float
    mode: Literal['stable', 'variable']
    def __init__(self, token, factor, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Repay(BaseAaveAction):
    token: str
    amount: Decimal
    mode: Literal['stable', 'variable']
    def __init__(self, token, amount, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3RepayAll(BaseAaveAction):
    token: str
    mode: Literal['stable', 'variable']
    def __init__(self, token, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3RepayToHealthFactor(BaseAaveAction):
    token: str
    factor: float
    mode: Literal['stable', 'variable']
    def __init__(self, token, factor, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Liquidation(BaseAaveAction):
    collateral: str
    debt: str
    user: str
    debtToCover: int
    receiveAToken: bool = ...
    def __init__(self, collateral, debt, user, debtToCover, receiveAToken=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FullLiquidation(BaseAaveAction):
    collateral: str
    debt: str
    user: str
    receiveAToken: bool = ...
    def __init__(self, collateral, debt, user, receiveAToken=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FlashLoanSimple(BaseAaveAction):
    token: str
    amount: Decimal
    receiver: str
    params: bytes
    def __init__(self, token, amount, receiver, params, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FlashLoan(BaseAaveAction):
    tokens: list[str]
    amounts: list[Decimal]
    modes: list[Literal['none', 'stable', 'variable']]
    receiver: str
    params: bytes
    def __init__(self, tokens, amounts, modes, receiver, params, *, agent, gas=..., gas_price=...) -> None: ...
