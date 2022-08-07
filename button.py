import pygame
import Object
import MiniSys
import panel


c_inactive = (128, 128, 128)
c_highlighted = (198, 198, 198)
c_active = (210, 210, 210)
c_text = (255, 255, 255)


class Button(Object.Object):
    def __init__(self, panel_name, x, y, w, h, text='', function=None):
        super().__init__(panel_name)
        # set the state of the button.
        self.active = 0
        self.pad_x = self.pad_y = 5

        # create the rect and set the init colour.
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.colour = c_inactive

        # set the text.
        self.text = self.font = self.font_font = self.font_size = self.surf = None
        self.set_text(text, True)
        self.set_font('Arial', 20, True)
        self.font_colour = c_text
        self.get_render()

        # set the function.
        self.function_active = self.function = None
        self.set_function(function)

    def set_text(self, text, setup=False):
        self.pad_y = 5
        self.pad_x = 5
        self.text = text
        if not setup:
            self.get_render()

    def set_image(self, image, scale=1.0):
        self.pad_y = 0
        self.pad_x = 0
        image_surf = pygame.image.load(image)
        self.surf = pygame.transform.scale(image_surf, (int(self.rect.w*scale), int(self.rect.h*scale)))
        MiniSys.recolour_image(self.surf, 255)

    def set_font(self, font, font_size=20, setup=False):
        self.font_font = font
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_font, self.font_size, True)
        if not setup:
            self.get_render()

    def get_render(self):
        self.surf = self.font.render(self.text, True, self.font_colour)

    def set_function(self, func=None):
        if func is not None:
            self.function_active = True
        else:
            self.function_active = False

        self.function = func

    def align(self, align='left', pad=5):
        self.pad_y = pad
        surf = self.surf.get_rect()
        # align surface to the left of object.
        if align == 'left':
            self.pad_x = pad
        # align surface to middle of object, at top.
        elif align == 'middle':
            self.pad_x = (self.rect.w - surf.w)//2
        # align surface to centre of object, in centre of object.
        elif align == 'centre':
            self.pad_x = (self.rect.w - surf.w)//2
            self.pad_y = (self.rect.h - surf.h)//2
        # align surface to the right of object.
        elif align == 'right':
            self.pad_x = (self.rect.w - surf.w) - pad

    def handle_event(self, event):
        if self.function_active:
            # change our x & y to match our actual position on-screen.
            x, y = self.rect.x, self.rect.y
            self.rect.x += self.panel.local_x
            self.rect.y += self.panel.local_y

            # when the mouse is moved check if we are hovering over the button.
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.active = 1
                else:
                    self.active = 0

            # if the button is clicked, change the colour/trigger the function.
            if event.type == pygame.MOUSEBUTTONDOWN and self.panel.active:
                if self.active == 1:
                    self.active = 2
                    if self.function is not None:
                        self.function()

            # change the colour of the button to match the state.
            if self.active == 0:
                self.colour = c_inactive
            elif self.active == 1:
                self.colour = c_highlighted
            else:
                self.colour = c_active

            # reset our rect to what it was before.
            self.rect.x, self.rect.y = x, y

    def draw(self, canvas):
        # if the panel is live, check the state.
        if self.panel.active:
            pygame.draw.rect(canvas, self.colour, self.rect)
            canvas.blit(self.surf, (self.rect.x+self.pad_x, self.rect.y+self.pad_y))


if __name__ == '__main__':
    # create a testing function.
    def test():
        print("Hello, World!")

    # create the renderer.
    mini = MiniSys.MiniRender(500, 500)

    # create a main panel.
    Main = panel.Panel(0, 0, 500, 500)
    mini.add_element(Main)

    # create a button with text 'Click Me!!'.
    button_test = Button(Main, 20, 20, 200, 50, 'Click Me!!')
    button_test.set_font('Times New Roman', 40)
    button_test.set_function(test)
    mini.add_element(button_test)

    # === mainloop! ===
    mini.mainloop()
