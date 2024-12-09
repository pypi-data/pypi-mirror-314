from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, JSON, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SuperTab(Base):
    __tablename__ = 'super_tab'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by = Column(Integer, nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    unique_identifier = Column(String(16), nullable=False)
    level = Column(Integer, default=0, nullable=False)
    is_current_tab = Column(Boolean, default=False, nullable=False)
    tab_info = Column(JSON, nullable=False)
    parent_tab_id = Column(Integer, nullable=True)
    order = Column(Integer, nullable=False)
    last_opened = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "unique_identifier": self.unique_identifier,
            "level": self.level,
            "tab_info": self.tab_info,
            "parent_tab_id": self.parent_tab_id,
            "order": self.order,
        }

    def __repr__(self):
        return json.dumps(self.to_dict())
