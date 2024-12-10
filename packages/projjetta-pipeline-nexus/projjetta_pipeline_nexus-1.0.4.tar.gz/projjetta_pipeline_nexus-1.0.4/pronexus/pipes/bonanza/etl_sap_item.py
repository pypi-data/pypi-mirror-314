"""
Nome do Módulo: etl_sap_item.py
Descrição: Este módulo contém as rotinas para importação de dados dos items (Produtos) da bonanza.
Autor: Carlos Valdir Botolotti / Beatriz Amorim - Projjetta
Data: 2024-10-09
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
from .model.item import Item,ItemPrice,ItemWarehouseInfo

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 30))) # TODO: Ajustar AQUI!!!
    logger.debug(f"Load base date: {load_base_date} ...")

    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)


    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET, 
        "Items",
        api_filter=f"(CreateDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select="ItemCode,ItemName,ForeignName,ItemsGroupCode,CustomsGroupCode,PurchaseItem,SalesItem,SalesUnit,SalesItemsPerUnit,InventoryItem,DesiredInventory,MaxInventory,MinInventory,ItemPrices,ItemWarehouseInfoCollection,CreateDate,UpdateDate"
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        items = page.get("value", [])

        if len(items) > 0:
            with Session(DWE.engine) as db_session:
                
                for item in items:
                    item_data = {k: v for k, v in item.items() if k not in "odata.etag"}
                    
                    # Inserindo o item na tabela 'Item'
                    item_obj = Item(**item_data)
                    db_session.merge(item_obj)

                    # Processando preços relacionados ao item
                    if 'ItemPrices' in item:  # Certificando-se de que 'ItemPrices' existe
                        item_prices = item['ItemPrices']
                        for price in item_prices:
                            # Adicionando explicitamente o ItemCode ao dicionário de preços
                            price['ItemCode'] = item['ItemCode']  # Garantir que ItemCode seja passado para ItemPrice
                            price_obj = ItemPrice(**price)  # Usando o dicionário diretamente
                            db_session.merge(price_obj)

                    if 'ItemWarehouseInfoCollection' in item:
                        warehouses = item['ItemWarehouseInfoCollection']
                        for warehouse in warehouses:
                            warehouse['ItemCode'] = item['ItemCode']
                            warehouse_obj = ItemWarehouseInfo(**warehouse)
                            db_session.merge(warehouse_obj)

                db_session.commit()