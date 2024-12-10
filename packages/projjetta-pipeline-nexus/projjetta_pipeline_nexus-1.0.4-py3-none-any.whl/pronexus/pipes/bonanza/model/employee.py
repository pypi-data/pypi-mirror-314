from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB

class Employee(SBB):
    __tablename__ = 'sap_employee'

    EmployeeID = Column('EmployeeID', Integer, primary_key=True)
    LastName = Column('LastName', String)
    FirstName = Column('FirstName', String)
    MiddleName = Column('MiddleName', String)
    Gender = Column('Gender', String)
    JobTitle = Column('JobTitle', String)
    Salary = Column('Salary', Float)
    SalaryUnit = Column('SalaryUnit', String)
    EmployeeCosts = Column('EmployeeCosts', Float)
    EmployeeCostUnit = Column('EmployeeCostUnit', String)
    Department = Column('Department', String)
    Branch = Column('Branch', String)
    WorkStreet = Column('WorkStreet', String)
    WorkBlock = Column('WorkBlock', String)
    WorkZipCode = Column('WorkZipCode', String)
    WorkCity = Column('WorkCity', String)
    WorkCounty = Column('WorkCounty', String)
    WorkCountryCode = Column('WorkCountryCode', String)
    WorkStateCode = Column('WorkStateCode', String)
    Manager = Column('Manager', String)
    SalesPersonCode = Column('SalesPersonCode', Integer)
    OfficePhone = Column('OfficePhone', String)
    MobilePhone = Column('MobilePhone', String)
    eMail = Column('eMail', String)
    StartDate = Column('StartDate', DateTime)
    StatusCode = Column('StatusCode', String)
    CreateDate = Column('CreateDate', DateTime)
    UpdateDate = Column('UpdateDate', DateTime)
    Religion = Column('Religion', String)
    PartnerReligion = Column('PartnerReligion', String)
    MartialStatus = Column('MartialStatus', String)
    Position = Column('Position', String)
    ProfessionStatus = Column('ProfessionStatus', String)
    EducationStatus = Column('EducationStatus', String)
    Active = Column('Active', String)



    def __repr__(self):
        return f"<Employee(employee_id='{self.EmployeeID}', last_name='{self.LastName}', first_name='{self.FirstName}')>"

class EmployeePosition(SBB):


    __tablename__ = 'sap_employee_position'

    PositionID = Column('PositionID', Integer, primary_key=True)
    Name = Column('Name', String)
    Description = Column('Description', String)



    def __repr__(self):
        return f"<EmployeePosition(PositionID='{self.PositionID}', Description='{self.Description}')>"