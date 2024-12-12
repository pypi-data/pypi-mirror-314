from sqlalchemy import Column, String, DateTime, DECIMAL, BIGINT
from at_common_models.base import Base

class DailyCandlestickModel(Base):
    __tablename__ = "stock_daily_candlesticks"

    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    time = Column(DateTime, primary_key=True, nullable=False, index=True)
    open = Column(DECIMAL(10, 3), nullable=False)
    high = Column(DECIMAL(10, 3), nullable=False)
    low = Column(DECIMAL(10, 3), nullable=False)
    close = Column(DECIMAL(10, 3), nullable=False)
    volume = Column(BIGINT, nullable=False)

    def __str__(self):
        return f"<CandlestickDaily(symbol={self.symbol}, time={self.time})>"

    def __repr__(self):
        return f"<CandlestickDaily(symbol={self.symbol}, time={self.time})>"
