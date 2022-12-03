import pygame as pg

class BasicConfig(object):
    
    def __init__(self):
        self.font = pg.font.Font(None, 24)

class ComboBox(BasicConfig):

    def __init__(self, name, l, t, w, h):
        super().__init__()
        self.name = name
        self.options = []
        self.combo_rects = []
        self.size = pg.Rect(l,t,w,h)
        self.selected_item = self.name
        self.deployed = False

    def deploy(self, screen: pg.display):
        temp_rect = self.size.copy()
        temp_text = self.font.render(self.selected_item, True, (0,0,0))
        if temp_rect.collidepoint(pg.mouse.get_pos()):
            temp_rect = pg.draw.rect(screen, (0,255,0), self.size, 2)
        else:
            temp_rect = pg.draw.rect(screen, (0,0,0), self.size, 2)
        screen.blit(temp_text, (self.size.centerx - temp_text.get_width()//2, self.size.centery - temp_text.get_height()//2))
        if self.deployed:
            yDelta = self.size.h
            pg.draw.rect(screen, (255,255,243), (self.size.x, self.size.y + self.size.h, self.size.w, self.size.h + (len(self.options)-1) * yDelta), 0)
            for i in range(len(self.options)):
                temp_rect.y += yDelta
                if len(self.combo_rects) < len(self.options):
                    self.combo_rects.append(temp_rect)
                if temp_rect.collidepoint(pg.mouse.get_pos()):
                    temp_rect = pg.draw.rect(screen, (0,255,0), temp_rect, 2)
                else:
                    temp_rect = pg.draw.rect(screen, (0,0,0), temp_rect, 2)
                temp_text = self.font.render(self.options[i], True, (0,0,0))
                screen.blit(temp_text, (temp_rect.centerx - temp_text.get_width()//2, temp_rect.centery - temp_text.get_height()//2))

    def select_item(self):
        for option in self.combo_rects:
            if option.collidepoint(pg.mouse.get_pos()):
                self.selected_item = self.options[self.combo_rects.index(option)]
                self.deployed = False

class Button(BasicConfig):

    def __init__(self, name, l, t, w, h):
        super().__init__()
        self.name = name
        self.hitbox = pg.Rect(l, t, w, h)

    def draw_button(self, screen: pg.display):
        text = self.font.render(self.name, True, (0,0,0))
        if self.hitbox.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, (0,255,0), self.hitbox, 2)
        else:
            pg.draw.rect(screen, (0,0,0), self.hitbox, 2)
        screen.blit(text, (self.hitbox.centerx - text.get_width()//2, self.hitbox.centery - text.get_height()//2))
        
class TextFeild(BasicConfig):
    def __init__(self, name, l, t, w, h):
        super().__init__()
        self.name = name
        self.input = ""
        self.hitbox = pg.Rect(l, t, w, h)
        self.active = False

    def draw_text_field(self, screen):
        text_surface = self.font.render(self.input, True, (0,0,0))
        if self.hitbox.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, (0,255,0), self.hitbox, 2)
        else:
            pg.draw.rect(screen, (0,0,0), self.hitbox, 2)
        screen.blit(text_surface, (self.hitbox.centerx - text_surface.get_width()//2, self.hitbox.centery - text_surface.get_height()//2))
    
