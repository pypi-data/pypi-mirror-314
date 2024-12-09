# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Explain Node

This is a SQL Query Execution Plan Node.

This writes out a query plan
"""

from typing import Generator

from opteryx.models import QueryProperties
from opteryx.operators import BasePlanNode
from opteryx.operators import OperatorType


class ExplainNode(BasePlanNode):
    operator_type = OperatorType.PRODUCER

    def __init__(self, properties: QueryProperties, **config):
        super().__init__(properties=properties)
        self._query_plan = config.get("query_plan")

    @property
    def name(self):  # pragma: no cover
        return "Explain"

    @property  # pragma: no cover
    def config(self):
        return ""

    @classmethod
    def from_json(cls, json_obj: str) -> "BasePlanNode":  # pragma: no cover
        raise NotImplementedError()

    def execute(self) -> Generator:
        if self._query_plan:
            yield from self._query_plan.explain()
