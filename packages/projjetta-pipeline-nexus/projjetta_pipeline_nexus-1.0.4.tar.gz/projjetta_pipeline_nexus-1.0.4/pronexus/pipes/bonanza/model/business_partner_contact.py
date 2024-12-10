from typing import List
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .sap_model import (
    SapBonanzaBase as SBB
)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class BusinessPartnerContactAddress(SBB):
    __tablename__ = 'sap_business_partner_contact_address'
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    CardCode = Column("CardCode", String, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_business_partner_contact.CardCode'))
    AddressName = Column('AddressName', String)
    Street = Column('Street', String, nullable=True)
    Block = Column('Block', String, nullable=True)
    ZipCode = Column('ZipCode', String, nullable=True)
    City = Column('City', String, nullable=True)
    # County = Column('County', String, nullable=True)
    Country = Column('Country', String)
    State = Column('State', String, nullable=True)
    # FederalTaxID = Column('FederalTaxID', String)
    # TaxCode = Column('TaxCode', String, nullable=True)
    BuildingFloorRoom = Column('BuildingFloorRoom', String, nullable=True)
    AddressType = Column('AddressType', String)
    AddressName2 = Column('AddressName2', String, nullable=True)
    AddressName3 = Column('AddressName3', String, nullable=True)
    TypeOfAddress = Column('TypeOfAddress', String, nullable=True)
    StreetNo = Column('StreetNo', String, nullable=True)
    # BPCode = Column('BPCode', String)
    RowNum = Column('RowNum', Integer)
    GlobalLocationNumber = Column('GlobalLocationNumber', String, nullable=True)
    Nationality = Column('Nationality', String, nullable=True)
    TaxOffice = Column('TaxOffice', String, nullable=True)
    # GSTIN = Column('GSTIN', String, nullable=True)
    # GstType = Column('GstType', String, nullable=True)
    CreateDate = Column('CreateDate', DateTime)
    CreateTime = Column('CreateTime', String)  # Hora como string
    # MYFType = Column('MYFType', String)
    # TaasEnabled = Column('TaasEnabled', String)
    # U_CTX_INKEY = Column('U_CTX_INKEY', String, nullable=True)
    # U_Name = Column('U_Name', String, nullable=True)
    # U_ContactName = Column('U_ContactName', String, nullable=True)
    # U_PhoneNo = Column('U_PhoneNo', String, nullable=True)
    # U_IsVisibleOnWebshop = Column('U_IsVisibleOnWebshop', String)
    # U_PROVR = Column('U_PROVR', String, nullable=True)
    # U_MUNIR = Column('U_MUNIR', String, nullable=True)

    # Define relationship with Card
    BusinessPartnerContact = relationship("BusinessPartnerContact", back_populates="BPAddresses")

    def __repr__(self):
        return f"<BPAddresses(address_name='{self.AddressName}', card_code='{self.CardCode}')>"
    

class BusinessPartnerContact(SBB):
    
    # Atributos
    __tablename__ = 'sap_business_partner_contact'

    # Campos
    CardCode = Column('CardCode', String, primary_key=True)
    CardName = Column('CardName', String)
    CardType = Column('CardType', String)
    Phone1 = Column('Phone1', String)
    Phone2 = Column('Phone2', String)
    Fax = Column('Fax', String)
    Country = Column('Country', String)
    BPAddresses = relationship("BusinessPartnerContactAddress", back_populates='BusinessPartnerContact', cascade='all, delete-orphan')
    CreateDate = Column('CreateDate', DateTime)
    UpdateDate = Column('UpdateDate', DateTime)

    def __repr__(self):
        return f"<Card(card_code='{self.CardCode}', card_name='{self.CardName}')>"
    

