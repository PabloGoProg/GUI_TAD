import pygame as pg, sys
from structures import *
from gui_elements import *
from pg_activities import *

class MainRun:
            
    def __init__(self, w, h):
        pg.init()
        self.display = pg.display.set_mode((w,h))
        self.display_clock = pg.time.Clock()
        self.menu = Menu(self.display)
        self.tree_activity = ActividadArboles(self.display)
        self.solitario = Solitario(self.display)
        self.grafos = GrafosCiudades(self.display)
        self.run()

    def run(self):
        while True:
            self.display.fill((255,255,255))

            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if self.tree_activity.avaliable:
                        self.tree_activity.event_manager(e)
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    if self.menu.avaliable:
                        if self.menu.buttons[0].hitbox.collidepoint(pg.mouse.get_pos()):
                            self.solitario.avaliable = True
                            self.menu.avaliable = False
                            self.grafos.avaliable = False
                        if self.menu.buttons[1].hitbox.collidepoint(pg.mouse.get_pos()):
                            self.tree_activity.avaliable = True
                            self.menu.avaliable = False
                            self.grafos.avaliable = False
                        if self.menu.buttons[2].hitbox.collidepoint(pg.mouse.get_pos()):
                            self.grafos.avaliable = True
                            self.menu.avaliable = False
                            self.solitario.avaliable = False
                            self.tree_activity.avaliable = False
                        if self.menu.buttons[3].hitbox.collidepoint(pg.mouse.get_pos()) and self.menu.avaliable:
                            pg.quit()
                            sys.exit()
                    elif self.tree_activity.avaliable:
                        self.tree_activity.event_manager(e)                
                    elif self.solitario.avaliable:
                        self.solitario.event_manager(e)
                    elif self.grafos.avaliable:
                        self.grafos.event_manager(e)
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            if not self.solitario.avaliable and not self.tree_activity.avaliable and not self.grafos.avaliable:
                self.menu.avaliable = True

            if self.menu.avaliable:
                self.menu.draw_menu()

            if self.tree_activity.avaliable:
                self.tree_activity.draw_menu()
            
            if self.solitario.avaliable:
                self.solitario.draw()
    
            if self.grafos.avaliable:
                self.grafos.draw()

            pg.display.update()
            self.display_clock.tick(60)