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

"""This package contains round behaviours of AlprinaStockAnalystAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast, Optional
from openai import OpenAI

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.victorpolisetty.skills.alprina_stock_analyst.models import Params
from packages.victorpolisetty.skills.alprina_stock_analyst.rounds import (
    SynchronizedData,
    AlprinaStockAnalystAbciApp,
    CollectStockDataRound,
    AggregateFinancialReportRound,
    RegistrationRound,
    ResetAndPauseRound,
)
from packages.victorpolisetty.skills.alprina_stock_analyst.rounds import (
    CollectStockDataPayload,
    AggregateFinancialReportPayload,
    RegistrationPayload,
    ResetAndPausePayload,
)

client: Optional[OpenAI] = None
client.api_key = ("sk-proj-3KHs33H4LRpeHnegSLZugqdyaeFwhGESZQ9a7eIrlvyIP5v8iIwWRsSUfscai5eNsNvAMNS"
                  "-0ST3BlbkFJ3vG7By89lA5FopiC3sngc-g-hlo7-bF_rH98ey1lXKehYZy-tLW9CPLPmli74q86rczN6yIFMA")


class AlprinaStockAnalystBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the alprina_stock_analyst skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class CollectStockDataBehaviour(AlprinaStockAnalystBaseBehaviour):
    """CalculatePositionHealthBehaviour"""

    matching_round: Type[AbstractRound] = CollectStockDataRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        # if self.context.price_api.is_retries_exceeded():
        #     # now we need to wait and see if the other agents progress the round, otherwise we should restart?
        #     with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
        #         yield from self.wait_until_round_end()
        #     self.set_done()
        #     return

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            self.context.logger.info("Inside the CollectStockData Behaviour")

            prompt = ("What do you expect the stock price of Tesla to be one week from today, based on historical "
                      "price data")
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                n=1,
                timeout=120,
                stop=None,
            )


            # api_specs = self.context.price_api.get_spec()
            # response = yield from self.get_http_response(
            #     method=api_specs["method"],
            #     url=api_specs["url"],
            #     headers=api_specs["headers"],
            #     parameters=api_specs["parameters"],
            # )
            # observation = self.context.price_api.process_response(response)

        if response:
            self.context.logger.info("The prompt given to ChatGPT is: " + prompt)
            self.context.logger.info("Response from ChatGPT is: " + response.choices[0].message.content)

            payload = CollectStockDataPayload(self.context.agent_address, response)
            with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
                yield from self.send_a2a_transaction(payload)
                yield from self.wait_until_round_end()
            self.set_done()
        else:
            self.context.logger.error(
                f"Could not get response from ChatGPT"
            )
            # yield from self.sleep(
            #     self.context.price_api.retries_info.suggested_sleep_time
            # )
            # self.context.price_api.increment_retries()


class AggregateFinancialReportBehaviour(AlprinaStockAnalystBaseBehaviour):
    """Aggregate one financial report."""

    matching_round = AggregateFinancialReportRound

    # def aggregate(self, observations: List[float]) -> float:
    #     """Aggregates a list of observations."""
    #     aggregator = getattr(statistics, self.params.observation_aggregator_function)
    #     return aggregator(observations)

    def async_act(self) -> Generator:
        """
        Do the action.

        Steps:
        - Run the script to compute the estimate starting from the shared observations.
        - Build an estimate transaction and send the transaction and wait for it to be mined.
        - Wait until ABCI application transitions to the next round.
        - Go to the next behaviour (set done event).
        """

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            self.context.logger.info("Inside the AggregateFinancialReport Behaviour")
            # estimate = self.aggregate(self.synchronized_data.observations)
            # self.context.logger.info(
            #     "Got estimate of %s price in %s: %s, Using aggregator method: %s",
            #     self.context.price_api.currency_id,
            #     self.context.price_api.convert_id,
            #     estimate,
            #     self.params.observation_aggregator_function,
            #
            payload = AggregateFinancialReportPayload(self.context.agent_address, ...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class RegistrationBehaviour(AlprinaStockAnalystBaseBehaviour):
    """RegistrationBehaviour"""

    matching_round: Type[AbstractRound] = RegistrationRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = RegistrationPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ResetAndPauseBehaviour(AlprinaStockAnalystBaseBehaviour):
    """ResetAndPauseBehaviour"""

    matching_round: Type[AbstractRound] = ResetAndPauseRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ResetAndPausePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class AlprinaStockAnalystRoundBehaviour(AbstractRoundBehaviour):
    """AlprinaStockAnalystRoundBehaviour"""

    initial_behaviour_cls = RegistrationBehaviour
    abci_app_cls = AlprinaStockAnalystAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        CollectStockDataBehaviour,
        AggregateFinancialReportBehaviour,
        RegistrationBehaviour,
        ResetAndPauseBehaviour,
    ]
