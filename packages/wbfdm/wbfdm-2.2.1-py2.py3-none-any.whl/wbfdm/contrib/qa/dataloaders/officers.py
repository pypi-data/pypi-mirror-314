from typing import Iterator

from django.db import connections
from jinjasql import JinjaSql  # type: ignore
from wbcore.contrib.dataloader.dataloaders import Dataloader
from wbcore.contrib.dataloader.utils import dictfetchall
from wbfdm.dataloaders.protocols import OfficersProtocol
from wbfdm.dataloaders.types import OfficerDataDict


class RKDOfficersDataloader(OfficersProtocol, Dataloader):
    def officers(
        self,
    ) -> Iterator[OfficerDataDict]:
        lookup = {k: v for k, v in self.entities.values_list("dl_parameters__officers__parameters", "id")}

        sql = """
            SELECT
                CONCAT(designation.Code, '-', ROW_NUMBER() OVER (ORDER BY officer.OfficerRank)) as id,
                designation.Code as external_identifier,
                designation.Title as position,
                CONCAT(
                    officer.Prefix,
                    ' ',
                    officer.FirstName,
                    ' ',
                    officer.LastName,
                    CASE
                        WHEN officer.Suffix IS NOT NULL THEN CONCAT(', ', officer.Suffix)
                        ELSE ''
                    END
                ) as name,
                officer.Age as age,
                officer.Sex as sex,
                CONVERT(DATE, designation.DesgStartDt) as start
            FROM RKDFndCmpOffTitleChg AS designation
            JOIN RKDFndCmpOfficer AS officer
                ON designation.Code = officer.Code
                AND designation.OfficerID = officer.Officerid

            WHERE
                designation.Code in (
                {% for instrument in instruments %}
                    {{instrument}} {% if not loop.last %}, {% endif %}
                {% endfor %})
                AND DesgEndDt IS NULL

            ORDER BY
                officer.OfficerRank
        """
        query, bind_params = JinjaSql(param_style="format").prepare_query(sql, {"instruments": lookup.keys()})
        with connections["qa"].cursor() as cursor:
            cursor.execute(
                query,
                bind_params,
            )
            for row in dictfetchall(cursor):
                row["instrument_id"] = lookup[row["external_identifier"]]
                yield row
