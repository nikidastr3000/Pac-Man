import pygame

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f'{self.x} {self.y}'

class Button():
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color, action = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action  # Function to call when clicked.

    def draw(self, screen):
        # Change the button color if the mouse is hovered over it
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Draw the button rectangle
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw the text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center = self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        # Check if a mouse event occurred within the bounds of the button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # LMB
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
