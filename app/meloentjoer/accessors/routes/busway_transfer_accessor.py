from app.meloentjoer.accessors.entity.BuswayTransfer import BuswayTransfer
from app.meloentjoer.common.databases.ModelBase import ModelBase
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.config import general_config as __config
from sqlalchemy import String, Column

__logger = logger_factory.create_logger(__name__)


def index(busway_transfer):
    """
    :type busway_transfer:BuswayTransfer
    :param busway_transfer:
    :return:
    """
    return '.'.join([busway_transfer.from_station, busway_transfer.to_station])


class BuswayTransferModel(ModelBase):
    __tablename__ = "BuswayTransferModel"
    index = Column(String, primary_key=True)
    from_busway_station = Column(String)
    to_busway_station = Column(String)

    def __init__(self):
        self.from_busway_station = None
        self.to_busway_station = None

    def to_busway_transfer(self):
        busway_transfer = BuswayTransfer()
        busway_transfer.from_station = self.from_busway_station
        busway_transfer.to_station = self.to_busway_station
        return busway_transfer

    def from_busway_transfer(self, busway_transfer):
        """
        :type busway_transfer: BuswayTransfer
        """
        self.index = index(busway_transfer)
        self.from_busway_station = busway_transfer.from_station
        self.to_busway_station = busway_transfer.to_station


busway_transfer_session = PostgresAccessorBase(BuswayTransferModel, __config.get_database_url())


def reset():
    busway_transfer_session.query(BuswayTransferModel).delete()
    busway_transfer_session.commit()


def get_busway_transfer(busway_transfer):
    """
    :type busway_transfer: BuswayTransfer
    :param busway_transfer:
    :return:
    """
    raw_busway_transfer = busway_transfer_session.query(BuswayTransferModel).filter(
        BuswayTransferModel.index == index(busway_transfer)).first()
    if raw_busway_transfer:
        return raw_busway_transfer.to_busway_transfer()
    return None


def upset_busway_transfer(busway_transfer):
    """
    :type busway_transfer:BuswayTransfer
    :param busway_transfer:
    :return:
    """
    raw_busway_transfer = get_busway_transfer(busway_transfer)
    """:type :BuswayTransferModel"""
    if not raw_busway_transfer:
        raw_busway_transfer = BuswayTransferModel()
        raw_busway_transfer.from_busway_transfer(busway_transfer)
        busway_transfer_session.add(raw_busway_transfer)
    busway_transfer_session.commit()


def get_all_busway_transfers():
    """
    :rtype :list[BuswayTransfer]
    :return:
    """
    raw_busway_transfer_list = busway_transfer_session.query(BuswayTransferModel).all()
    busway_transfer_list = [busway_transfer.to_busway_transfer() for busway_transfer in raw_busway_transfer_list]
    return busway_transfer_list
