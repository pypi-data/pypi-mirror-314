from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB


class InventoryExit(SBB):
    __tablename__ = 'sap_inventory_exit'

    DocNum = Column('DocNum', Integer,  primary_key=True)
    DocEntry = Column('DocEntry', Integer)
    CardCode = Column('CardCode', String)
    DocDate = Column('DocDate', DateTime)
    DocDueDate = Column('DocDueDate', DateTime)
    DocumentStatus = Column('DocumentStatus', String)
    Comments = Column('Comments', String)
    NumAtCard = Column('NumAtCard', String)
    DocCurrency = Column('DocCurrency', String)
    DocRate = Column('DocRate', Float)
    DiscountPercent = Column('DiscountPercent', Float)
    TotalDiscount = Column('TotalDiscount', Float)
    VatSum = Column('VatSum', Float)
    DocTotal = Column('DocTotal', Float)
    SalesPersonCode = Column('SalesPersonCode', Integer)
    ContactPersonCode = Column('ContactPersonCode', Integer)
    PaymentMethod = Column('PaymentMethod', String)
    ShipToCode = Column('ShipToCode', String)
    CreationDate = Column('CreationDate', DateTime)
    UpdateDate = Column('UpdateDate', DateTime)
    ClosingDate = Column('ClosingDate', DateTime)
    Reference1 = Column('Reference1', String)
    Reference2 = Column('Reference2', String)
    PaymentBlock = Column('PaymentBlock', String)
    PaymentBlockEntry = Column('PaymentBlockEntry', Integer)
    DocumentSubType = Column('DocumentSubType', String)
    Series = Column('Series', Integer)
    TaxDate = Column('TaxDate', DateTime)
    U_NCF = Column('U_NCF', String)
    CancelStatus = Column('CancelStatus', String)
    FiscalDocNum = Column('FiscalDocNum', String)


    inventory_item = relationship("InventoryExitItem", back_populates="inventory")

    def __repr__(self):
        return f"<entry(inventory_doc='{self.DocNum}', card_code='{self.CardCode}', doc_total='{self.DocTotal}')>"


class InventoryExitItem(SBB):
    __tablename__ = 'sap_inventory_exit_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    DocNum = Column(Integer, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_inventory_exit.DocNum'))
    LineNum = Column('LineNum', Integer)
    ItemCode = Column('ItemCode', String)
    Quantity = Column('Quantity', Float)
    Volume = Column('Volume', Float)
    VolumeUnit = Column('VolumeUnit',Float)
    OpenQuantity = Column('OpenQuantity', Float)
    Price = Column('Price', Float)
    PriceAfterVAT = Column('PriceAfterVAT', Float)
    LineTotal = Column('LineTotal', Float)
    DiscountPercent = Column('DiscountPercent', Float)
    CommisionPercent = Column('CommisionPercent', Float)
    VatGroup = Column('VatGroup', String)
    VatSum = Column('VatSum', Float)
    Currency = Column('Currency', String)
    Rate = Column('Rate', Float)
    WarehouseCode = Column('WarehouseCode', String)
    TaxStatus = Column('TaxStatus', String)
    ProjectCode = Column('ProjectCode', String)
    BaseEntry = Column('BaseEntry', Integer)
    BaseLine = Column('BaseLine', Integer)
    BaseType = Column('BaseType', Integer)
    NetTaxAmount = Column('NetTaxAmount', Integer)
    NetTaxAmountFC = Column('NetTaxAmountFC', Integer)
    NetTaxAmountSC = Column('NetTaxAmountSC', Integer)
    TaxPercentagePerRow = Column('TaxPercentagePerRow', Integer)
    TaxTotal = Column('TaxTotal', Integer)
    GrossBuyPrice = Column('GrossBuyPrice', Integer)

    inventory = relationship("InventoryExit", back_populates="inventory_item")

    def __repr__(self):
        return f"<inventory_item(item_code='{self.ItemCode}', quantity='{self.Quantity}', line_total='{self.LineTotal}')>"
