import pygame as pg, sys
from structures import *
from gui_elements import *
from pg_activities import *

'''
LA clase MainRun es la clase principal de la interfaz, en esta se
guardan todas las actividades solicitadas, además de el ciclo principal del juego
'''
class MainRun:
            
    def __init__(self, w, h):

        ''' Método constructor de la clase MainRun '''
        pg.init()
        self.display = pg.display.set_mode((w,h))
        self.display_clock = pg.time.Clock()
        self.menu = Menu(self.display)
        self.tree_activity = ActividadArboles(self.display)
        self.solitario = Solitario(self.display)
        self.grafos = GrafosCiudades(self.display)
        self.run()

    ''' Ciclo principal de la interfaz, encargado de recibir los eventos y pintar las actividades '''
    def run(self):
        while True:
            self.display.fill((255,255,255))

            for e in pg.event.get():
                ''' Manejo de los inputs de teclas '''
                if e.type == pg.KEYDOWN:
                    if self.tree_activity.avaliable:
                        self.tree_activity.event_manager(e) # Inputs de actividad árbol
                    elif self.grafos.avaliable:
                        self.grafos.event_manager(e)
                ''' Manejo de los inputs del mouse '''
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    ''' Manejador de botones del Menu '''
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

            ''' Pinta las actividades si es que estas estan disponibles '''
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