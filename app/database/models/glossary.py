"""ROBERT"""
from sqlalchemy import Column, VARCHAR, Text
from app.database.models import TbBase



class TbGlossary(TbBase):
    __tablename__ = "tb_glossary"
    code = Column(VARCHAR(255), primary_key=True)
    content = Column(Text, nullable=False)

    def dict(self):
        return {
            "code": self.code,
            "content": self.content,
        }
