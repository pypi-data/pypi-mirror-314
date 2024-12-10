"""
Nome do Módulo: etl_service_calls.py
Descrição: Este módulo contém as rotinas para importação de dados de chamadas de serviço da Bonanza.
Autor: Beatriz Amorim - Projjetta
Data: 2024-10-16
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
from .model.ServiceCalls import ServiceCall, ServiceCallActivity

def run_pipeline(**kwargs):
    """ Executar a extração de chamadas de serviço """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 * 10 if load_full else 7)))  # Ajuste da data base de carga
    logger.debug(f"Load base date: {load_base_date} ...")

    # Cria as tabelas se não existirem
    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    # Conexão com a API
    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET,
        "ServiceCalls",
        #api_filter=f"(CreationDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select="ServiceCallID,Subject,CustomerCode,CustomerName,ContactCode,ContractID,ResolutionDate,ResolutionTime,Origin,ItemCode,Status,Priority,CallType,ProblemType,AssigneeCode,Description,TechnicianCode,Resolution,CreationDate,CreationTime,Responder,UpdatedTime,ResponseByTime,ResponseByDate,ResolutionOnDate,ResponseOnTime,ResponseOnDate,ClosingTime,AssignedDate,Queue,ResponseAssignee,EntitledforService,ResolutionOnTime,AssignedTime,ClosingDate,Series,DocNum,HandWritten,PeriodIndicator,StartDate,StartTime,EndDueDate,EndTime,Duration,DurationType,Reminder,ReminderPeriod,ReminderType,Location,AddressName,AddressType,Street,City,Room,State,Country,CustomerRefNo,ProblemSubType,AttachmentEntry,ServiceBPType,UpdateDate,SupplementaryCode,U_GB_ValorReclam,U_GB_ValorRecon,ServiceCallActivities"
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    # Processamento dos dados extraídos
    for page in requested_data:
        service_calls = page.get("value", [])

        if len(service_calls) > 0:
            with Session(DWE.engine) as db_session:

                for service_call in service_calls:
                    # Remover o campo 'odata.etag' se presente
                    service_call_data = {k: v for k, v in service_call.items() if k != "odata.etag"}

                    # Inserindo a chamada de serviço na tabela 'ServiceCall'
                    service_call_obj = ServiceCall(**service_call_data)
                    db_session.merge(service_call_obj)

                    # Processando atividades relacionadas à chamada de serviço
                    if 'ServiceCallActivities' in service_call:
                        activities = service_call['ServiceCallActivities']
                        for activity in activities:
                            # Adicionando explicitamente o ServiceCallID ao dicionário de atividades
                            activity['ServiceCallID'] = service_call['ServiceCallID']
                            activity_obj = ServiceCallActivity(**activity)
                            db_session.merge(activity_obj)

                db_session.commit()


