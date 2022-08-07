import Object
import pygame


class Panel(Object.Object):
    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)

        self.active = True
        self.canvas = pygame.Surface((w, h))
        self.rect = self.canvas.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.local_x = self.panel.local_x + x
        self.local_y = self.panel.local_y + y
        self.elements = []

        self.colour = (0, 0, 0)

    def enable(self, state=1):
        if state == 0:
            self.hide()
        elif state == 1:
            self.show()

    def show(self):
        self.active = True

    def hide(self):
        self.active = False

    def add_element(self, e):
        self.elements.append(e)

    def add_elements(self, elements):
        for e in elements:
            self.add_element(e)

    def set_colour(self, col = (0, 0, 0)):
        self.colour = col

    def handle_event(self, event):
        for element in self.elements:
            element.handle_event(event)

    def update(self):
        if self.panel.active:
            for element in self.elements:
                element.update()

    def draw(self, canvas):
        if self.panel.active and self.active:
            self.canvas.fill(self.colour)
            for element in self.elements:
                element.draw(self.canvas)
            canvas.blit(self.canvas, (self.rect.x, self.rect.y))
