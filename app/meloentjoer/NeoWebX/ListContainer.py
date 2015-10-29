import Renderable


class ListContainer(list, Renderable):
    def __init__(self, renderer):
        """
        :type renderer: Renderable
        :param renderer:
        :return:
        """
        super(ListContainer, self).__init__()
        self.renderer = renderer

    def render(self):
        pass
