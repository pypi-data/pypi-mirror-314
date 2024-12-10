"""
Nome do Módulo: etl_sap_journal_entry.py
Descrição: Este módulo contém as rotinas para importação de dados das entradas de diário (Journal Entries) da Bonanza.
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
from .model.journal_entry import JournalEntry, JournalEntryLine  # Ajuste a importação para o novo modelo

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 30)))  # Ajuste conforme necessário
    logger.debug(f"Load base date: {load_base_date} ...")

    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET,
        "JournalEntries",  # Endpoint correto para Journal Entries
        api_filter=f"(ReferenceDate ge '{load_base_date}')",
        api_select=(
                    "JdtNum,ReferenceDate,Memo,Reference,Reference2,TransactionCode,ProjectCode,TaxDate,"
                    "Indicator,UseAutoStorno,StornoDate,VatDate,Series,StampTax,DueDate,AutoVAT,Number,"
                    "FolioNumber,FolioPrefixString,ReportEU,Report347,Printed,LocationCode,OriginalJournal,"
                    "Original,BaseReference,BlockDunningLetter,AutomaticWT,WTSum,WTSumSC,WTSumFC,"
                    "SignatureInputMessage,SignatureDigest,CertificationNumber,PrivateKeyVersion,Corisptivi,"
                    "Reference3,DocumentType,DeferredTax,BlanketAgreementNumber,OperationCode,"
                    "ResidenceNumberType,ECDPostingType,ExposedTransNumber,PointOfIssueCode,Letter,"
                    "FolioNumberFrom,FolioNumberTo,IsCostCenterTransfer,ReportingSectionControlStatementVAT,"
                    "ExcludeFromTaxReportControlStatementVAT,AdjustTransaction,AttachmentEntry,"
                    "JournalEntryLines"
                    )
                        )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        journal_entries = page.get("value", [])

        if len(journal_entries) > 0:
            with Session(DWE.engine) as db_session:

                for journal_entry in journal_entries:
                    journal_entry_data = {k: v for k, v in journal_entry.items() if k not in "odata.etag"}

                    # Inserindo a entrada de diário na tabela 'JournalEntry'
                    journal_entry_obj = JournalEntry(**journal_entry_data)
                    db_session.merge(journal_entry_obj)

                    # Processando as linhas associadas à entrada de diário
                    if 'JournalEntryLines' in journal_entry:
                        journal_entry_lines = journal_entry['JournalEntryLines']
                        for line in journal_entry_lines:
                            line['JdtNum'] = journal_entry['JdtNum']  # Garantir que JdtNum seja passado para JournalEntryLine
                            line_obj = JournalEntryLine(**line)  # Usando o dicionário diretamente
                            db_session.merge(line_obj)

                db_session.commit()
