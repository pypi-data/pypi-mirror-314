from sqlalchemy import Column, String, DateTime
from at_common_models.base import Base

class NewsStockModel(Base):
    __tablename__ = "news_stocks"

    news_id = Column(String(40), primary_key=True, nullable=False)
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    published_at = Column(DateTime, nullable=False, index=True)

    def __str__(self):
        return f"<NewsStock(news_id={self.news_id}, symbol={self.symbol})>"

    def __repr__(self):
        return f"<NewsStock(news_id={self.news_id}, symbol={self.symbol})>"
