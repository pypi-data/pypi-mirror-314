"""
Nome do Módulo: etl_sap_inventory_entry.py
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
from .model.inventory_entries import InventoryEntry, InventoryEntryItem  # Ajuste a importação para o novo modelo

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
        entries = page.get("value", [])

        if len(entries) > 0:
            with Session(DWE.engine) as db_session:

                for entry in entries:
                    entry_data = {k: v for k, v in entry.items() if k not in "odata.etag"}

                    # Inserindo a ordem na tabela 'Order'
                    entry_obj = InventoryEntry(**entry_data)
                    db_session.merge(entry_obj)

                    # Processando itens relacionados à ordem
                    if 'DocumentLines' in entry:  # Certificando-se de que 'order_items' existe
                        document_line = entry['DocumentLines']
                        for item in document_line:
                            item['DocNum'] = entry['DocNum']  # Garantir que DocNum seja passado para OrderItem
                            item_obj = InventoryEntryItem(**item)  # Usando o dicionário diretamente
                            db_session.merge(item_obj)

                db_session.commit()

