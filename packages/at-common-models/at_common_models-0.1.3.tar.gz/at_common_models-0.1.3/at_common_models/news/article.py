from sqlalchemy import Column, String, Text, DateTime
from at_common_models.base import Base

class NewsArticleModel(Base):
    __tablename__ = "news_articles"

    id = Column(String(40), primary_key=True, nullable=False)
    source = Column(String(256), nullable=False)
    headline = Column(String(8196), nullable=False)
    summary = Column(Text(length=65535), nullable=False, default='')
    url = Column(String(512), nullable=True, default=None)
    published_at = Column(DateTime, nullable=False, index=True)

    def __str__(self):
        return f"<NewsArticle(id={self.id}, headline={self.headline})>"

    def __repr__(self):
        return f"<NewsArticle(id={self.id}, headline={self.headline})>"