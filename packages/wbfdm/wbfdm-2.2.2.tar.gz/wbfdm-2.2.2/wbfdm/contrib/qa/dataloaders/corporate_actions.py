from datetime import date
from typing import Iterator

from django.db import connections
from jinjasql import JinjaSql  # type: ignore
from wbcore.contrib.dataloader.dataloaders import Dataloader
from wbcore.contrib.dataloader.utils import dictfetchall
from wbfdm.dataloaders.protocols import CorporateActionsProtocol
from wbfdm.dataloaders.types import CorporateActionDataDict


class DatastreamCorporateActionsDataloader(CorporateActionsProtocol, Dataloader):
    def corporate_actions(
        self,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> Iterator[CorporateActionDataDict]:
        lookup = {k: v for k, v in self.entities.values_list("dl_parameters__corporate_actions__parameters", "id")}

        sql = """
            SELECT
                InfoCode as external_identifier,
                CONCAT(InfoCode, '_', CONVERT(DATE, EffectiveDate)) as id,
                CONVERT(DATE, EffectiveDate) as valuation_date,
                'qa-ds2' as source,
                ActionTypeCode as action_code,
                EventStatusCode as event_code,
                NumOldShares as old_shares,
                NumNewShares as new_shares,
                ISOCurrCode as currency

            FROM Ds2CapEvent
            WHERE (
                {% for instrument in instruments %}
                    InfoCode = {{instrument}} {% if not loop.last %} OR {% endif %}
                {% endfor %}
            )
            {% if from_date %} AND EffectiveDate >= {{ from_date }} {% endif %}
            {% if to_date %} AND EffectiveDate <= {{ to_date }} {% endif %}

            ORDER BY EffectiveDate DESC
        """

        query, bind_params = JinjaSql(param_style="format").prepare_query(
            sql,
            {
                "instruments": self.entities.values_list("dl_parameters__corporate_actions__parameters", flat=True),
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
