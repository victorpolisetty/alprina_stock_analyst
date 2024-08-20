# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains the rounds of AlprinaStockAnalystAbciApp."""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
)

from packages.victorpolisetty.skills.alprina_stock_analyst.payloads import (
    CollectStockDataPayload,
    AggregateFinancialReportPayload,
    RegistrationPayload,
    ResetAndPausePayload,
)


class Event(Enum):
    """AlprinaStockAnalystAbciApp Events"""

    NOT_TRIGGERED = "not_triggered"
    NO_MAJORITY = "no_majority"
    RESET_TIMEOUT = "reset_timeout"
    ROUND_TIMEOUT = "round_timeout"
    DONE = "done"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class CollectStockDataRound(AbstractRound):
    """CalculatePositionHealthRound"""

    payload_class = CollectStockDataPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: CollectStockDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CollectStockDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class AggregateFinancialReportRound(AbstractRound):
    """CollectPositionsRound"""

    payload_class = AggregateFinancialReportPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: AggregateFinancialReportPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AggregateFinancialReportPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class RegistrationRound(AbstractRound):
    """RegistrationRound"""

    payload_class = RegistrationPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: RegistrationPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: RegistrationPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class ResetAndPauseRound(AbstractRound):
    """ResetAndPauseRound"""

    payload_class = ResetAndPausePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: ResetAndPausePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: ResetAndPausePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class AlprinaStockAnalystAbciApp(AbciApp[Event]):
    """AlprinaStockAnalystAbciApp"""

    initial_round_cls: AppState = RegistrationRound
    initial_states: Set[AppState] = {RegistrationRound}
    transition_function: AbciAppTransitionFunction = {
        RegistrationRound: {
            Event.DONE: CollectStockDataRound
        },
        CollectStockDataRound: {
            Event.DONE: AggregateFinancialReportRound,
            Event.ROUND_TIMEOUT: ResetAndPauseRound,
            Event.NO_MAJORITY: ResetAndPauseRound
        },
        AggregateFinancialReportRound: {
            Event.DONE: ResetAndPauseRound,
            Event.ROUND_TIMEOUT: ResetAndPauseRound,
            Event.NO_MAJORITY: ResetAndPauseRound
        },
        ResetAndPauseRound: {
            Event.DONE: CollectStockDataRound,
            Event.NO_MAJORITY: ResetAndPauseRound,
            Event.RESET_TIMEOUT: ResetAndPauseRound
        }
    }
    final_states: Set[AppState] = set()
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: Set[str] = []
    db_pre_conditions: Dict[AppState, Set[str]] = {
        RegistrationRound: [],
    }
    db_post_conditions: Dict[AppState, Set[str]] = {}
