"""
Nome do Módulo: etl_sap_employee.py
Descrição: Este módulo contém as rotinas para importação de dados dos funcionario da Bonanza.
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
from .model.employee import Employee


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
        "EmployeesInfo",
        #api_filter=f"(ActivityDate ge '{load_base_date}')",
        api_select=(
                    "EmployeeID,LastName,FirstName,MiddleName,Gender,JobTitle,Salary,SalaryUnit,"
                    "EmployeeCosts,EmployeeCostUnit,Department,Branch,WorkStreet,WorkBlock,"
                    "WorkZipCode,WorkCity,WorkCounty,WorkCountryCode,WorkStateCode,Manager,"
                    "SalesPersonCode,OfficePhone,MobilePhone,eMail,StartDate,StatusCode,"
                    "CreateDate,UpdateDate,Religion,PartnerReligion,MartialStatus,Position,"
                    "ProfessionStatus,EducationStatus,Active"
        )
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        employees = page.get("value", [])

        if len(employees) > 0:
            with Session(DWE.engine) as db_session:

                for employee in employees:
                    employee_data = {k: v for k, v in employee.items() if k not in "odata.etag"}

                    # Inserindo o activity na tabela 'Activity'
                    employee_obj = Employee(**employee_data)
                    db_session.merge(employee_obj)

                db_session.commit()
