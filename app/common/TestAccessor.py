__author__ = 'traveloka'

from PostgreBase import *


class NewModel(Base):
    __tablename__ = 'NewModel'
    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name


class NewModelAccessor:

    def add_new_mode(self):
        pass

    def get_all(self):
        pass


class NewModelPostgresAccessor(PostgresAccessorBase, NewModelAccessor):
    
    def __init__(self):
        super(NewModelPostgresAccessor, self).__init__(NewModel, 'sqlite:///new_model.db')

    def add_new_mode(self, instance):
        self.add(instance)
        self.commit()

    def get_all(self):
        return self.query(NewModel).all()
