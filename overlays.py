from settings import *
from utilities import *


class TitleScreen:

    def __init__(self, game):
        self.game = game

        
    def update(self):
        pass

    def draw(self, surface):
        pass


class WinScreen:

    def __init__(self, game):
        self.game = game
        
    def update(self):
        pass

    def draw(self, surface):
        pass


class LoseScreen:

    def __init__(self, game):
        self.game = game

        
    def update(self):
        pass

    def draw(self, surface):
        pass


class LevelCompleteScreen:

    def __init__(self, game):
        self.game = game
        
    def update(self):
        pass

    def draw(self, surface):
        pass


class PauseScreen:

    def __init__(self, game):
        self.game = game
        
    def update(self):
        pass

    def draw(self, surface):
        pass


class HUD:

    def __init__(self, game):
        self.game = game
        
    def update(self):
        pass

    def draw(self, surface):
        pass


# Used for level editing
class Grid:

    def __init__(self, game, color=(125, 125, 125)):
        self.game = game
        self.on = False

        self.color = color
        self.font = pygame.font.Font(None, 16)

    def toggle(self):
        self.on = not self.on

    def draw(self, surface, offset_x=0, offset_y=0):
        if self.on:
            width = surface.get_width()
            height = surface.get_height()
            
            for x in range(0, width + GRID_SIZE, GRID_SIZE):
                adj_x = x - offset_x % GRID_SIZE
                pygame.draw.line(surface, self.color, [adj_x, 0], [adj_x, height], 1)

            for y in range(0, height + GRID_SIZE, GRID_SIZE):
                adj_y = y - offset_y % GRID_SIZE
                pygame.draw.line(surface, self.color, [0, adj_y], [width, adj_y], 1)

            for x in range(0, width + GRID_SIZE, GRID_SIZE):
                for y in range(0, height + GRID_SIZE, GRID_SIZE):
                    adj_x = x - offset_x % GRID_SIZE + 4
                    adj_y = y - offset_y % GRID_SIZE + 4
                    disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
                    disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
                    
                    point = f'({disp_x}, {disp_y})'
                    text = self.font.render(point, True, self.color)
                    surface.blit(text, [adj_x, adj_y])
