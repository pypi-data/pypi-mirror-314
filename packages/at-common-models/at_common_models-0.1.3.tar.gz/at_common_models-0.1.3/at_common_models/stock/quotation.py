from sqlalchemy import Column, String, Float, BIGINT, DateTime
from at_common_models.base import Base

class QuotationModel(Base):
    __tablename__ = "stock_quotations"

    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    volume = Column(BIGINT, nullable=False)
    previous_close = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    day_low = Column(Float, nullable=False)
    day_high = Column(Float, nullable=False)
    share_outstanding = Column(BIGINT, nullable=False)
    pe = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __str__(self):
        return f"<Quotation(symbol={self.symbol}, price={self.price})>"

    def __repr__(self):
        return f"<Quotation(symbol={self.symbol}, price={self.price})>"