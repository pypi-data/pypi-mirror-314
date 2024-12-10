"""
Nome do Módulo: etl_sap_activity_type.py
Descrição: Este módulo contém as rotinas para importação de dados das atividades (Activity) da Bonanza.
Autor: Beatriz Amorim - Projjetta
Data: 2024-10-17
"""

import copy
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ...library.database import (
    DW_ENGINE as DWE
)

from .sap_api import (
    SapApiRequestMethod as SAM,
    SapApiConnection as SAC,
    SapApiPaginationRequest as SPR,
    sap_formatted_query_date as FQD
)

from .model.sap_model import SapBonanzaBase
from .model.activities import ActivityType


def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 7)))
    logger.debug(f"Load base date: {load_base_date} ...")

    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET,
        "ActivityTypes",
        #api_filter=f"(ActivityDate ge '{load_base_date}')",
        api_select="Code,Name"
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        activities = page.get("value", [])

        if len(activities) > 0:
            with Session(DWE.engine) as db_session:

                for activity in activities:
                    activity_data = {k: v for k, v in activity.items() if k not in "odata.etag"}

                    # Inserindo o activity na tabela 'Activity'
                    activity_obj = ActivityType(**activity_data)
                    db_session.merge(activity_obj)

                db_session.commit()
