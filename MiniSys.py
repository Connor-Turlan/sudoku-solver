import pygame
import Object


c_black = (0, 0, 0)
c_white = (255, 255, 255)


def recolour_image(img, col=255):
    # inverts an image.
    img.lock()

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            rgba = img.get_at((x, y))
            if rgba[3] == 0:
                continue
            rgba = (col, col, col, rgba[3])
            img.set_at((x, y), rgba)

    img.unlock()
    return img


class MiniRender:
    def __init__(self, w, h, flags=0):
        pygame.init()
        self.active = True
        self.screen = pygame.display.set_mode((w, h), flags)
        self.local_x, self.local_y = (0, 0)
        self.clock = pygame.time.Clock()
        self.elements = []
        self.background = (96, 96, 96)
        self.quit_ev = False
        self.tick_rate = 60

    def add_element(self, element):
        self.elements.append(element)

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)

    def set_background(self, col=(0, 0, 0)):
        self.background = col

    def close(self):
        self.quit_ev = True

    def do_draw(self):
        self.screen.fill(self.background)
        for element in self.elements:
            element.draw(self.screen)

        pygame.display.flip()

    def loop(self):
        # events
        for event in pygame.event.get():
            if self.quit_ev:
                exit()
                return False
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            for element in self.elements:
                element.handle_event(event)

        # updates
        for element in self.elements:
            element.update()

        # draw
        self.do_draw()
        self.clock.tick(self.tick_rate)
        return True

    def mainloop(self):
        running = True
        while running:
            running = self.loop()

        pygame.quit()
        print('close.')
