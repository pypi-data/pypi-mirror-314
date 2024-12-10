from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB


class Invoice(SBB):
    __tablename__ = 'sap_invoice'

    DocNum = Column('DocNum', Integer,  primary_key=True)
    DocEntry = Column('DocEntry', Integer, nullable=False)
    CardCode = Column('CardCode', String, nullable=False)
    DocDate = Column('DocDate', DateTime, nullable=False)
    DocDueDate = Column('DocDueDate', DateTime, nullable=True)
    DocumentStatus = Column('DocumentStatus', String, nullable=False)
    NumAtCard = Column('NumAtCard', String, nullable=True)
    DocCurrency = Column('DocCurrency', String, nullable=False)
    DocRate = Column('DocRate', Float, nullable=True)
    DiscountPercent = Column('DiscountPercent', Float, nullable=True)
    TotalDiscount = Column('TotalDiscount', Float, nullable=True)
    VatSum = Column('VatSum', Float, nullable=True)
    DocTotal = Column('DocTotal', Float, nullable=False)
    SalesPersonCode = Column('SalesPersonCode', Integer, nullable=True)
    ContactPersonCode = Column('ContactPersonCode', Integer, nullable=True)
    PaymentMethod = Column('PaymentMethod', String, nullable=True)
    ShipToCode = Column('ShipToCode', String, nullable=True)
    CreationDate = Column('CreationDate', DateTime, nullable=True)
    UpdateDate = Column('UpdateDate', DateTime, nullable=True)
    ClosingDate = Column('ClosingDate', DateTime, nullable=True)
    Reference1 = Column('Reference1', String, nullable=True)
    Reference2 = Column('Reference2', String, nullable=True)
    PaymentBlock = Column('PaymentBlock', String, nullable=True)
    PaymentBlockEntry = Column('PaymentBlockEntry', Integer, nullable=True)
    DocumentSubType = Column('DocumentSubType', String, nullable=True)
    Series = Column('Series', Integer, nullable=True)
    TaxDate = Column('TaxDate', DateTime, nullable=True)
    PaidToDate = Column('PaidToDate', Integer, nullable=True)
    PaidToDateFC = Column('PaidToDateFC', Integer, nullable=True)
    PaidToDateSys = Column('PaidToDateSys', Integer, nullable=True)
    U_NCF = Column('U_NCF', String, nullable=True)
    CancelStatus = Column('CancelStatus', String, nullable=False)
    FiscalDocNum = Column('FiscalDocNum', String, nullable=True)


    # Relacionamento com invoice Items
    invoice_item = relationship("InvoiceItem", back_populates="invoice")

    def __repr__(self):
        return f"<invoice(invoice_id='{self.invoiceID}', card_code='{self.CardCode}', doc_total='{self.DocTotal}')>"


class InvoiceItem(SBB):
    __tablename__ = 'sap_invoice_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    DocNum = Column(Integer, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_invoice.DocNum'))
    LineNum = Column('LineNum', Integer)
    ItemCode = Column('ItemCode', String)
    Description = Column('Description', String)
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
    GrossProfitTotal = Column('GrossProfitTotal', Float)
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

    # Relacionamento com invoice
    invoice = relationship("Invoice", back_populates="invoice_item")

    def __repr__(self):
        return f"<invoiceItem(item_code='{self.ItemCode}', quantity='{self.Quantity}', line_total='{self.LineTotal}')>"
