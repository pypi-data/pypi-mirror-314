"""
Nome do Módulo: etl_sap_business_partner_supplier_contact.py
Descrição: Este módulo contém as rotinas para importação de dados dos contatos da bonanza.
Autor: Carlos Valdir Botolotti - Projjetta
Data: 2024-10-03
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
from .model.business_partner_contact import BusinessPartnerContact, BusinessPartnerContactAddress

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 7))) # TODO: Ajustar AQUI!!!
    logger.debug(f"Load base date: {load_base_date} ...")

    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET, 
        "BusinessPartners",
        api_filter=f"CardType eq 'S' and (CreateDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select="CardCode,CardName,CardType,Phone1,Phone2,Fax,Country,BPAddresses,CreateDate,UpdateDate"
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        contacts = page.get("value", [])

        if len(contacts) > 0:

            with Session(DWE.engine) as db_session: 
            
                for contact in contacts:
                    dc = copy.deepcopy(contact)
                    dc["BPAddresses"] = [BusinessPartnerContactAddress(**ic) for ic in contact.get("BPAddresses", [])]
                    bpc = BusinessPartnerContact(**{_ : dc[_] for _ in dc if not _ in "odata.etag"})
                    db_session.merge(bpc)

                db_session.commit()