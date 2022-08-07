class Object:
    def __init__(self, parent):
        parent.add_element(self)
        self.panel = parent

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, canvas):
        pass


if __name__ == '__main__':
    print('obj')
    obj = Object()
