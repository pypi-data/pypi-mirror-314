from sqlalchemy.orm import DeclarativeBase

class SapBonanzaBase(DeclarativeBase):
    """ Classe base para tabelas do SAP da Bonanza """
    __table_args__ = {'schema': 'bonanza'}

    def __init__(self, **kwargs):
        # super().__init__(kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
