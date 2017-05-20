import pygame
import traceback
import sys


class ControllerDisplay:

    def __init__(self, name, switch_labels):
        pygame.init()
        pygame.display.init()

        self.screen = pygame.display.set_mode((500, 280), pygame.locals.RESIZABLE)
        self.font = pygame.font.SysFont('Courier', 20)
        pygame.display.set_caption('QuadStick: ' + name)

        self.row_height = 30
        self.paused = False
        self.ready = False
        self.switch_labels = switch_labels

    def draw(self, demands, switchval):
        self._show_demand(demands, 0, -1, 'Pitch')
        self._show_demand(demands, 1, -1, 'Roll')
        self._show_demand(demands, 2, +1, 'Yaw')
        self._show_demand(demands, 3, +1, 'Throttle')

        self._show_switch(switchval, 0)
        self._show_switch(switchval, 1)
        self._show_switch(switchval, 2)

        pygame.display.flip()

    def clear(self):
        '''
        Clears the display.
        '''
        self.screen.fill((0, 0, 0))

    def error(self):
        '''
        Displays the most recent exception as an error message, and waits for ESC to quit.
        '''
        while True:

            self.clear()
            tb = traceback.format_exc()
            self._draw_label_in_row('ERROR', 0, color=(255, 0, 0))

            self._display(tb)
            print(tb, file=sys.stderr)
            pygame.display.flip()

            if not self.running():
                pygame.quit()
                sys.exit()

    def _show_switch(self, switchval, index):

        x = 200
        y = 180 + index * 30
        r = 10

        # Draw a white ring around the button
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), r, 1)

        # Draw a white or black disk inside the ring depending on switch state
        pygame.draw.circle(self.screen, (255, 255, 255) if switchval == index else (0, 0, 0), (x, y), r - 3)

        self._draw_label(self.switch_labels[index], y - 10)

    def _show_demand(self, demands, index, sign, label):

        # color for no-demand baseline
        color = (0, 0, 255)

        demand = sign * demands[index]

        if demand > 0:
            color = (0, 255, 0)

        if demand < 0:
            color = (255, 0, 0)

        w = 100  # width of rectangle for maximum demand
        h = 20

        x = 250
        y = 20 + index * 30

        # Erase previous
        pygame.draw.rect(self.screen, (0, 0, 0), (x - w - 1, y, 2 * w, h))

        # Draw a white hollow rectangle to represent the limits
        pygame.draw.rect(self.screen, (255, 255, 255), (x - w - 1, y, 2 * w, h), 1)

        # Special handling for throttle
        '''
        if index == 3:
            x -= w
            w += w
        '''

        # Draw a colorful filled rectangle to represent the demand
        pygame.draw.rect(self.screen, color, (x, y, x + (demand / 100) * w, h))

        # Draw a label for the axis
        self._draw_label(label, y)

        # self._draw_label(str(label) + "->" + "      ", y, (0, 0, 0))
        # self._draw_label(str(label) + "->" + str(demand), y)

    def _draw_label_in_row(self, text, row, color=(255, 255, 255)):

        self._draw_label(text, row * self.row_height, color)

    def _draw_label(self, text, y, color=(255, 255, 255)):

        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey((0, 0, 0))

        self.screen.blit(surface, (20, y))

    def display(self, msg):

        row = 1
        for line in msg.split('\n'):
            self._draw_label_in_row(line, row)
            row += 1

        pygame.display.flip()


    def running(self):
        '''
        Returns True if the QuadStick is running, False otherwise. Run can be terminated by hitting
        ESC.
        '''

        self.keys = pygame.event.get()

        for event in self.keys:
            if event.type == pygame.locals.QUIT:
                return False

            elif event.type == pygame.locals.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.locals.RESIZABLE)

            elif (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                return False

        return True