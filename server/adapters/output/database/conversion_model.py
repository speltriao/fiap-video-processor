from sqlalchemy import Column, DateTime, Integer, String

from server.adapters.output.database import Base


class ConversionModel(Base):
    __tablename__ = "tb_conversion"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    s3_link = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    finished_date = Column(DateTime, nullable=False)
