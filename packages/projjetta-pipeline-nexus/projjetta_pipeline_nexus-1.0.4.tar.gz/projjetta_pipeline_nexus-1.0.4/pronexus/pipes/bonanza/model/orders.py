from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB


class Order(SBB):
    __tablename__ = 'sap_order'

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
    CancelStatus = Column('CancelStatus', String, nullable=False)
    FiscalDocNum = Column('FiscalDocNum', String, nullable=True)


    # Relacionamento com Order Items
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(order_id='{self.OrderID}', card_code='{self.CardCode}', doc_total='{self.DocTotal}')>"


class OrderItem(SBB):
    __tablename__ = 'sap_order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    DocNum = Column(Integer, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_order.DocNum'))
    LineNum = Column('LineNum', Integer)
    ItemCode = Column('ItemCode', String, nullable=False)
    Description = Column('Description', String, nullable=True)
    Quantity = Column('Quantity', Float, nullable=False)
    Volume = Column('Volume', Float, nullable=False)
    VolumeUnit = Column('VolumeUnit', Float, nullable=False)
    OpenQuantity = Column('OpenQuantity', Float, nullable=True)
    Price = Column('Price', Float, nullable=False)
    PriceAfterVAT = Column('PriceAfterVAT', Float, nullable=False)
    LineTotal = Column('LineTotal', Float, nullable=False)
    DiscountPercent = Column('DiscountPercent', Float, nullable=True)
    CommisionPercent = Column('CommisionPercent', Float, nullable=True)
    VatGroup = Column('VatGroup', String, nullable=True)
    VatSum = Column('VatSum', Float, nullable=True)
    GrossProfitTotal = Column('GrossProfitTotal', Float, nullable=True)
    Currency = Column('Currency', String, nullable=True)
    Rate = Column('Rate', Float, nullable=True)
    WarehouseCode = Column('WarehouseCode', String, nullable=True)
    TaxStatus = Column('TaxStatus', String, nullable=True)
    ProjectCode = Column('ProjectCode', String, nullable=True)
    BaseEntry = Column('BaseEntry', Integer, nullable=True)
    BaseLine = Column('BaseLine', Integer, nullable=True)
    BaseType = Column('BaseType', Integer, nullable=True)
    NetTaxAmount = Column('NetTaxAmount', Integer)
    NetTaxAmountFC = Column('NetTaxAmountFC', Integer)
    NetTaxAmountSC = Column('NetTaxAmountSC', Integer)
    TaxPercentagePerRow = Column('TaxPercentagePerRow', Integer)
    TaxTotal = Column('TaxTotal', Integer)
    GrossBuyPrice = Column('GrossBuyPrice', Integer)

    # Relacionamento com Order
    order = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(item_code='{self.ItemCode}', quantity='{self.Quantity}', line_total='{self.LineTotal}')>"
