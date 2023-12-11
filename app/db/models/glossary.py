"""ROBERT"""
from sqlalchemy import Column, VARCHAR, Text, Integer, JSON
from sqlalchemy import func
from app.db.models import TbBase
from app.db.common import Session


class TbGlossary(TbBase):
    __tablename__ = "tb_glossary"
    code = Column(VARCHAR(255), primary_key=True)
    content = Column(Text, nullable=False)

    def dict(self):
        return {
            "code": self.code,
            "content": self.content,
        }


class TbMarketReport(TbBase):

    __tablename__ = "tb_market_report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report = Column(JSON)

    @classmethod
    def latest(cls):
        with Session() as session:
            latest_report = session.query(cls).order_by(cls.id.desc()).first()
<<<<<<< HEAD
=======
            print(latest_report)
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
            return latest_report.report