from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB

class Item(SBB):
    __tablename__ = 'sap_item'

    ItemCode = Column('ItemCode', String, primary_key=True)
    ItemName = Column('ItemName', String)
    ForeignName = Column('ForeignName', String, nullable=True)
    ItemsGroupCode = Column('ItemsGroupCode', Integer)
    CustomsGroupCode = Column('CustomsGroupCode', Integer, default=-1)
    PurchaseItem = Column('PurchaseItem', String)
    SalesItem = Column('SalesItem', String)
    SalesUnit = Column('SalesUnit', String)
    SalesItemsPerUnit = Column('SalesItemsPerUnit', Float, default=0.0)
    InventoryItem = Column('InventoryItem', String)
    DesiredInventory = Column('DesiredInventory', Float, default=0.0)
    MaxInventory = Column('MaxInventory', Float, default=0.0)
    MinInventory = Column('MinInventory', Float, default=0.0)
    CreateDate = Column('CreateDate', DateTime)
    UpdateDate = Column('UpdateDate', DateTime)

    # Relacionamento com a tabela ItemPrice e ItemWarehouseInfo
    item_prices = relationship("ItemPrice", back_populates="item", cascade="all, delete-orphan")
    warehouses = relationship("ItemWarehouseInfo", back_populates="item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Item(item_code='{self.ItemCode}', item_name='{self.ItemName}')>"


class ItemPrice(SBB):
    __tablename__ = 'item_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ItemCode = Column(String, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_item.ItemCode'))
    PriceList = Column('PriceList', Integer)
    Price = Column('Price', Float)
    Currency = Column('Currency', String)
    BasePriceList = Column('BasePriceList', Integer, nullable=True)
    Factor = Column('Factor', Float, nullable=True)

    # Back reference to the Item table
    item = relationship("Item", back_populates="item_prices")

    def __repr__(self):
        return f"<ItemPrice(price_list='{self.PriceList}', price='{self.Price}', currency='{self.Currency}')>"

class ItemWarehouseInfo(SBB):
    __tablename__ = 'item_warehouse_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ItemCode = Column(String, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_item.ItemCode'))
    WarehouseCode = Column('WarehouseCode', String)
    MinimalStock = Column('MinimalStock', Float, nullable=True)
    MaximalStock = Column('MaximalStock', Float, nullable=True)
    MinimalOrder = Column('MinimalOrder', Float, nullable=True)
    StandardAveragePrice = Column('StandardAveragePrice', Float)
    Locked = Column('Locked', String)
    InventoryAccount = Column('InventoryAccount', String, nullable=True)
    CostAccount = Column('CostAccount', String, nullable=True)
    TransferAccount = Column('TransferAccount', String, nullable=True)
    RevenuesAccount = Column('RevenuesAccount', String, nullable=True)
    VarienceAccount = Column('VarienceAccount', String, nullable=True)
    DecreasingAccount = Column('DecreasingAccount', String, nullable=True)
    IncreasingAccount = Column('IncreasingAccount', String, nullable=True)
    ReturningAccount = Column('ReturningAccount', String, nullable=True)
    ExpensesAccount = Column('ExpensesAccount', String, nullable=True)
    #EURevenuesAccount = Column('EURevenuesAccount', String, nullable=True)
    #EUExpensesAccount = Column('EUExpensesAccount', String, nullable=True)
    ForeignRevenueAcc = Column('ForeignRevenueAcc', String, nullable=True)
    ForeignExpensAcc = Column('ForeignExpensAcc', String, nullable=True)
    ExemptIncomeAcc = Column('ExemptIncomeAcc', String, nullable=True)
    PriceDifferenceAcc = Column('PriceDifferenceAcc', String, nullable=True)
    InStock = Column('InStock', Float, default=0.0)
    Committed = Column('Committed', Float, default=0.0)
    Ordered = Column('Ordered', Float, default=0.0)
    CountedQuantity = Column('CountedQuantity', Float, default=0.0)
    WasCounted = Column('WasCounted', String)
    UserSignature = Column('UserSignature', Integer)
    Counted = Column('Counted', Float, default=0.0)
    

    item = relationship("Item", back_populates="warehouses")

    def __repr__(self):
        return f"<ItemWarehouseInfo(warehouse_code='{self.WarehouseCode}', in_stock='{self.InStock}')>"