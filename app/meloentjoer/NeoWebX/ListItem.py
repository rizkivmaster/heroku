import Renderable


class ListItemContainer(object, Renderable):
    def __init__(self, renderer, inner_renderable):
        """
        :type renderer: Renderable
        :type inner_renderable: Renderable
        :param renderer:
        :param inner_renderable:
        :return:
        """
        self.renderer = renderer
        self.item = inner_renderable

    def render(self):
        inner_element = self.inn
        return self.renderer.render()

