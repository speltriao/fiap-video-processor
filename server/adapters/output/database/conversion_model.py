from sqlalchemy import Column, DateTime, Integer, String

from server.adapters.output.database import Base


class ConversionModel(Base):
    __tablename__ = "tb_conversion"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_size = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
