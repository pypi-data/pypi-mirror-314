from datetime import date
from itertools import batched  # type: ignore
from typing import Iterator

from django.db import connections
from jinjasql import JinjaSql  # type: ignore
from wbcore.contrib.dataloader.dataloaders import Dataloader
from wbcore.contrib.dataloader.utils import dictfetchall
from wbfdm.dataloaders.protocols import AdjustmentsProtocol
from wbfdm.dataloaders.types import AdjustmentDataDict


class DatastreamAdjustmentsDataloader(AdjustmentsProtocol, Dataloader):
    def adjustments(self, from_date: date, to_date: date) -> Iterator[AdjustmentDataDict]:
        lookup = {k: v for k, v in self.entities.values_list("dl_parameters__adjustments__parameters", "id")}

        sql = """
            SELECT
                InfoCode as external_identifier,
                CONCAT(InfoCode, '_', CONVERT(DATE, AdjDate)) as id,
                CONVERT(DATE, AdjDate) as adjustment_date,
                CONVERT(DATE, EndAdjDate) as adjustment_end_date,
                'qa-ds2' as source,
                AdjFactor as adjustment_factor,
                CumAdjFactor as cumulative_adjustment_factor

            FROM Ds2Adj
            WHERE
            AdjType = 2
            AND (
                {% for instrument in instruments %}
                    InfoCode = {{instrument}} {% if not loop.last %} OR {% endif %}
                {% endfor %}
            )
            {% if from_date %} AND AdjDate >= {{ from_date }} {% endif %}
            {% if to_date %} AND AdjDate <= {{ to_date }} {% endif %}

            ORDER BY AdjDate DESC
        """
        for batch in batched(lookup.keys(), 1000):
            query, bind_params = JinjaSql(param_style="format").prepare_query(
                sql,
                {
                    "instruments": batch,
                    "from_date": from_date,
                    "to_date": to_date,
                },
            )
            with connections["qa"].cursor() as cursor:
                cursor.execute(
                    query,
                    bind_params,
                )
                for row in dictfetchall(cursor):
                    row["instrument_id"] = lookup[row["external_identifier"]]
                    yield row
