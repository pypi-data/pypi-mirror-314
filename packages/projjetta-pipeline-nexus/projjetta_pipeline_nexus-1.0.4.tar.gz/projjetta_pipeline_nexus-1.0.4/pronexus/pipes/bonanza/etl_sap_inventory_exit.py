"""
Nome do Módulo: etl_sap_inventory_exit.py
Descrição: Este módulo contém as rotinas para importação de dados das ordens (Orders) da Bonanza.
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
from .model.inventory_exits import InventoryExit, InventoryExitItem  # Ajuste a importação para o novo modelo

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 * 3 if load_full else 30)))  # TODO: Ajustar AQUI!!!
    logger.debug(f"Load base date: {load_base_date} ...")

    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET,
        "InventoryGenEntries",  # Alterar para o endpoint correto
        api_filter=f"(CreationDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select="DocNum,DocEntry,CardCode,DocDate,DocDueDate,DocumentStatus,Comments,NumAtCard,DocCurrency,DocRate,DiscountPercent,TotalDiscount,VatSum,DocTotal,SalesPersonCode,ContactPersonCode,PaymentMethod,ShipToCode,UpdateDate,CreationDate,ClosingDate,Reference1,Reference2,PaymentBlock,PaymentBlockEntry,DocumentSubType,Series,TaxDate,U_NCF,CancelStatus,FiscalDocNum,DocumentLines"  # Inclua os campos necessários
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        exits = page.get("value", [])

        if len(exits) > 0:
            with Session(DWE.engine) as db_session:

                for exit in exits:
                    exist_data = {k: v for k, v in exit.items() if k not in "odata.etag"}

                    # Inserindo a ordem na tabela 'Order'
                    exist_obj = InventoryExit(**exist_data)
                    db_session.merge(exist_obj)

                    # Processando itens relacionados à ordem
                    if 'DocumentLines' in exit:  # Certificando-se de que 'order_items' existe
                        document_line = exit['DocumentLines']
                        for item in document_line:
                            item['DocNum'] = exit['DocNum']  # Garantir que DocNum seja passado para OrderItem
                            item_obj = InventoryExitItem(**item)  # Usando o dicionário diretamente
                            db_session.merge(item_obj)

                db_session.commit()

