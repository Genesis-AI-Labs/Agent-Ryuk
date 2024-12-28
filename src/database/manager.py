from sqlalchemy import create_engine, Column, String, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class ResearchItemDB(Base):
    """Database model for research items"""
    __tablename__ = 'research_items'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)
    abstract = Column(String)
    url = Column(String, nullable=False)
    published_date = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    tags = Column(JSON)
    citation_count = Column(Integer)
    references = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_item(self, research_item):
        """Add a new research item to the database"""
        session = self.Session()
        try:
            db_item = ResearchItemDB(
                id=research_item.id,
                title=research_item.title,
                authors=research_item.authors,
                abstract=research_item.abstract,
                url=research_item.url,
                published_date=research_item.published_date,
                source=research_item.source,
                tags=research_item.tags,
                citation_count=research_item.citation_count,
                references=research_item.references
            )
            session.merge(db_item)  # merge instead of add to handle updates
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_recent_items(self, hours=24):
        """Get items from the last n hours"""
        session = self.Session()
        try:
            items = session.query(ResearchItemDB)\
                .filter(ResearchItemDB.published_date >= datetime.utcnow() - timedelta(hours=hours))\
                .all()
            return items
        finally:
            session.close()