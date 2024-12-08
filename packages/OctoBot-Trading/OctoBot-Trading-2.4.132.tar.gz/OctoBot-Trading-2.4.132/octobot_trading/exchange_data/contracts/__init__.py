#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from octobot_trading.exchange_data.contracts import margin_contract
from octobot_trading.exchange_data.contracts.margin_contract import (
    MarginContract,
)

from octobot_trading.exchange_data.contracts import future_contract
from octobot_trading.exchange_data.contracts.future_contract import (
    FutureContract,
)

from octobot_trading.exchange_data.contracts import contract_factory
from octobot_trading.exchange_data.contracts.contract_factory import (
    update_contracts_from_positions,
    update_future_contract_from_dict,
    create_default_future_contract,
)

__all__ = [
    "MarginContract",
    "FutureContract",
    "update_contracts_from_positions",
    "update_future_contract_from_dict",
    "create_default_future_contract",
]
