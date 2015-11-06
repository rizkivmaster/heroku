from app.meloentjoer.common.behavioral.Accessor import Accessor


class BusEstimationAccessor(Accessor):
    def add_sample(self, origin, destination, delta):
        """
        :type origin: str
        :type destination: str
        :type delta: float
        :param origin:
        :param destination:
        :param delta:
        :return:
        """

    def predict_eta(self, origin, destination):
        """
        :type origin: str
        :type destination: str
        :param: station name:String
        :param: station name:string
        :return: seconds prediction (float)
        """
