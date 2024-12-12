from sqlalchemy import Column, String, DateTime, Text
from at_common_models.base import Base

class OverviewModel(Base):
    __tablename__ = "stock_overviews"

    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    exchange = Column(String(16), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text(), nullable=True, default='')
    currency = Column(String(3), nullable=False)
    country = Column(String(16), nullable=False, default='')
    address = Column(String(256), nullable=False, default='')
    sector = Column(String(32), nullable=False, default='')
    industry = Column(String(128), nullable=False, default='')
    ceo = Column(String(256), nullable=False, default='')
    ipo_date = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f"<Overview(symbol={self.symbol}, name={self.name})>"

    def __repr__(self):
        return f"<Overview(symbol={self.symbol}, name={self.name})>"