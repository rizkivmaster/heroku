__author__ = 'traveloka'


class BusETAEstimator:
    def __init__(self):
        self.estimator_dictionary = dict()

    def __get_key(self, origin, destination):
        return "{0}_{1}".format(origin, destination)

    def add_sample(self, origin, destination, delta):
        key = self.__get_key(origin, destination)
        delta = float(delta)
        if key in self.estimator_dictionary:
            delta_mean, sample_size = self.estimator_dictionary[key]
            new_delta_mean = (delta+(sample_size*delta_mean))/(sample_size+1)
            self.estimator_dictionary[key] = (new_delta_mean, sample_size+1)
        else:
            self.estimator_dictionary[key] = (delta, 1)

    # params: station name:String, station name:string
    # return: seconds prediction (float)
    def predict_eta(self, origin, destination):
        key = self.__get_key(origin, destination)
        if key in self.estimator_dictionary:
            estimator = self.estimator_dictionary[key]
            return int(estimator[0])
        else:
            return None
