import pygame as pg
import random
import json
from gui_elements import *
from structures import *

''' 
La clase Menu esta encaragada de Manejar el ingreso a otras activdades de
una interfaz grafica, o de lo contratrio salir de la misma 
'''
class Menu(object):

    ''' Método inicializador del MEnu '''
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.avaliable = True
        self.basic_config()

    ''' Dibuja todos los botoes existentes en el Menu '''
    def draw_menu(self):
        for button in self.buttons:
            button.draw_button(self.screen)

    ''' Configuración principal de la clase menu '''
    def basic_config(self):
        # Agrega todos los botones
        self.buttons.append(Button('Pilas - Solitario', self.screen.get_width()//2 - 123, 300, 250, 45))
        self.buttons.append(Button('Árboles - Recorridos', self.screen.get_width()//2 - 125, 300 + 60, 250, 45))
        self.buttons.append(Button('Grafos - Dikjstra', self.screen.get_width()//2 - 125, 300 + 120 , 250, 45))
        self.buttons.append(Button('Salir', self.screen.get_width()//2 - 125, 300 + 180 , 250, 45))
        for button in self.buttons: # Cambia el font de cada boton por individual
            button.font = pg.font.Font(None, 32)

'''
La Actividad de árboles permite al usuario jugfar con una forma visual
de una estructura de arbol Nario o Binario, dando la posibilidad de añadir 
una cantidad deseada de nodos y pover ver los distintos tipos dfe recorridos
de cada uno de estos aárboles
'''
class ActividadArboles(object):

    ''' Método inicializador de la Actividad de árboles '''
    def __init__(self, screen):
        self.screen = screen
        self.base_font = pg.font.Font(None, 24)
        self.tree_type = ComboBox('Tipo Arbol', self.screen.get_width()-130, 10, 120, 32)
        self.traversal_type = ComboBox('Tipo recorrido', self.screen.get_width()-260, 10, 120, 32)
        self.avaliable = False
        self.buttons = []
        self.text_fields = []
        self.tree = NAryTree()
        self.binary_tree = BinaryTree()
        self.dim_btns()
    
    ''' Anáde un dodo al arbol usando los valores habidos en los inputs '''
    def add_node(self):
        father, value, nodes = None, None, None
        data = [nodes, value, father] # Genera una lista cpn los valores del combo box
        for i in range(len(self.text_fields)):
            if self.tree_type.selected_item == 'Binarios' and i == 2: # Verifica si se utilizara el padre
                pass
            else:
                try:
                    data[i] = int(self.text_fields[i].input)
                except:
                    self.text_fields[1].input = ""
                    self.text_fields[2].input = ""
                    return
                    
        if self.tree_type.selected_item == 'Generales': # Agrega un nodo al arbol Nario
            if self.tree.len < data[0]-1:
                self.tree.insert_child(self.tree.root, data[2], data[1])
        elif self.tree_type.selected_item == 'Binarios': # Agrega un valor al arbol binario
            self.binary_tree.insert_node(self.binary_tree.root, data[1])
            self.binary_tree.len += 1
        self.text_fields[1].input = ""
        self.text_fields[2].input = ""
        
    ''' Dibuja el arbol con los nodos existentes en la clase arbol '''
    def draw_tree(self):
        xDelta, yDelta = 100, 60 # Inicialización de las deltas
        xCooordenate = self.screen.get_width()//2 # Coordenada X inicial
        def dfs(node, level, xCoordenate, xDelta, r): # Funcion recursiva
            x, y = xCoordenate, 60*(level+1)
            for i in range(len(node.child)): # dibujado de las lineas y llamado recursivo
                if i % 2 == 0 and i > 0:
                    pg.draw.line(self.screen, (0,0,0), (x,y), ((x - xDelta*(i-1)), y+(yDelta)), 3)
                    dfs(node.child[i], level+1, x-(xDelta*(i-1)), xDelta-(xDelta*0.20), r-1)
                else:
                    pg.draw.line(self.screen, (0,0,0), (x,y), ((x + xDelta*i), y+(yDelta)), 3)
                    dfs(node.child[i], level+1, x+(xDelta*i), xDelta-(xDelta*0.20), r-1)

            if len(node.child) == 0 and level > 0: # Dibujado de los circulos
                pg.draw.circle(self.screen, (215, 205, 165), (x, y), r)
                pg.draw.circle(self.screen, (0,0,0), (x, y), r, 2)
            else:
                pg.draw.circle(self.screen, (173, 216, 230), (x, y), r)
                pg.draw.circle(self.screen, (0,0,0), (x, y), r, 2)

            node_value = self.base_font.render(str(node.data), True, (0,0,0)) 
            self.screen.blit(node_value, (x - node_value.get_width()//2,y-node_value.get_height()//2 ))
        dfs(self.tree.root, 0, xCooordenate, xDelta, 25)

    ''' Dibuja ina instancia de árbol binario en una interfaz '''
    def draw_binary_tree(self):
        xDelta, yDelta = 150, 60 #Definición de deltas
        xCoordenate = self.screen.get_width()//2 # PRimera coordenada de dibujado (mitad de la pantalla)
        def dfs(node: self.binary_tree.Node, level, xCoordenate, xDelta, r): 
            x, y = xCoordenate, yDelta*(level+1) # Se selecciona el nivel de Y dependiendo del nivel

            if node.left: # Dibujado de lineas4
                pg.draw.line(self.screen, (0,0,0), (x,y), (x - xDelta, y + yDelta), 3)
            if node.right:
                pg.draw.line(self.screen, (0,0,0), (x,y), (x + xDelta, y + yDelta), 3)

            if node.left != None: # Llamados recursivos
                dfs(node.left, level+1, xCoordenate - xDelta, xDelta-(xDelta*0.45), r-1)
            if node.right != None:
                dfs(node.right, level+1, xCoordenate + xDelta, xDelta-(xDelta*0.45), r-1)

            if node.left == None and node.right == None and node != self.binary_tree.root: # Dibujado de circulos (Nodos)
                pg.draw.circle(self.screen, (215, 205, 165), (x, y), r)
                pg.draw.circle(self.screen, (0,0,0), (x, y), r, 2)
            else:
                pg.draw.circle(self.screen, (173, 216, 230), (x, y), r)
                pg.draw.circle(self.screen, (0,0,0), (x, y), r, 2)

            node_value = self.base_font.render(str(node.data), True, (0,0,0)) # Se dibuja el valor del nodo en el circulo
            self.screen.blit(node_value, (x - node_value.get_width()//2,y-node_value.get_height()//2 ))
        dfs(self.binary_tree.root, 0, xCoordenate, xDelta, 25) 

    def show_traversal(self):
        temp_font = pg.font.Font(None, 24)
        if self.tree_type.selected_item == 'Binarios':
            ''' Valida que tipo de recorrido buca el usuario '''
            if self.traversal_type.selected_item == 'Inorder':
                self.binary_tree.inorder()
            elif self.traversal_type.selected_item == 'Preorder':
                self.binary_tree.preorder()
            elif self.traversal_type.selected_item == 'Postorder':
                self.binary_tree.postorder()
            elif self.traversal_type.selected_item == 'Level order':
                self.binary_tree.level_order_traversal()
        self.imprimir_recorrido(temp_font) # Imprime el recorrido en un cuadro de texto
    
    ''' Dibuja un cuadro de texto con el recorrido de un árbol '''
    def imprimir_recorrido(self, font):
        txt = font.render(self.traversal_type.selected_item + ' = ' + str(self.binary_tree.traversal), True, (0,0,0))
        pg.draw.rect(self.screen, (255,255,243), (self.screen.get_width()//2 - txt.get_width()//2 - 15, self.screen.get_height()-100, 
                                                    txt.get_width() + 30, 32), 0)
        pg.draw.rect(self.screen, (0,0,0), (self.screen.get_width()//2 - txt.get_width()//2 -15, self.screen.get_height()-100, 
                                                    txt.get_width() + 30, 32), 2)
        self.screen.blit(txt, (self.screen.get_width()//2 - txt.get_width()//2, self.screen.get_height()-100 + txt.get_height()//2))

    ''' . b los elelemntos pertenecientes del menu en la pantalla '''
    def draw_menu(self):
        ''' Dibuja el árbol Nario o Binario dependiendo de lo seleccionado '''
        if self.tree_type.selected_item == 'Generales' and self.tree.root != None:
            self.draw_tree()
        elif self.tree_type.selected_item == 'Binarios' and self.binary_tree.root != None:
            self.draw_binary_tree()
        ''' Dibuja los Combo Box en la pantalla '''
        self.tree_type.deploy(self.screen)
        self.traversal_type.deploy(self.screen)

        if self.tree_type.selected_item != self.tree_type.name:
            for text_field in self.text_fields:
                if text_field.name == 'Nodo padre' and self.tree_type.selected_item == 'Binarios':
                    pass
                else:
                    text_field.draw_text_field(self.screen)
                    temp = text_field.font.render(text_field.name, True, (0,0,0))
                    self.screen.blit(temp, (text_field.hitbox.w + 15, text_field.hitbox.y + temp.get_height()//2))
        ''' Dibuja los botones en la interfaz '''
        for button in self.buttons:
            button.draw_button(self.screen)
        if self.tree.root != None or self.binary_tree.root != None:
            self.show_traversal()

    ''' Maneja los eventos que llegas a los inputs y botones de la actividad '''
    def event_manager(self, event):
        if event.type == pg.KEYDOWN:
            for text_field in self.text_fields:
                if text_field.active:
                    if event.key == pg.K_BACKSPACE:
                        text_field.input = text_field.input[:-1]
                    elif event.key == pg.K_RETURN:
                        self.add_node()
                    else:
                        text_field.input += event.unicode 
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for t_field in self.text_fields:
                if t_field.hitbox.collidepoint(pg.mouse.get_pos()):
                    t_field.active = True
                else :
                    t_field.active = False
            if self.buttons[0].hitbox.collidepoint(pg.mouse.get_pos()):
                    self.avaliable = False 
            if self.tree_type.size.collidepoint(pg.mouse.get_pos()):
                if self.tree_type.deployed:
                    self.tree_type.deployed = False
                else:
                    self.tree_type.deployed = True
            if self.traversal_type.size.collidepoint(pg.mouse.get_pos()):
                if self.traversal_type.deployed:
                    self.traversal_type.deployed = False
                else:
                    self.traversal_type.deployed = True
            if self.traversal_type.deployed:
                self.traversal_type.select_item()
            if self.tree_type.deployed:
                self.tree_type.select_item()
    
    ''' .Crea las dimensiones iniciales de los inputs de la actividad '''
    def dim_btns(self):
        self.tree_type.options.append('Generales')
        self.tree_type.options.append('Binarios')
        self.traversal_type.options.append('Inorder')
        self.traversal_type.options.append('Preorder')
        self.traversal_type.options.append('Postorder')
        self.traversal_type.options.append('Level order')
        self.text_fields.append(TextFeild('Cantidad nodos', 10, 10, 50, 32))
        self.text_fields.append(TextFeild('Valor', 10, 52, 50, 32))
        self.text_fields.append(TextFeild('Nodo padre', 10, 94, 50, 32))
        self.buttons.append(Button("Salir", 10, self.screen.get_height()-42, 100, 32))

'''
La actividad de Solitario permite al usuario interactuar con una estructura de Pila
donde, entregadas unas pilas de cartas, el usuario podrá buscar ordenar estas cartas
en una sola pila, siguiendo un orden descendiente de las cartas
'''
class Solitario(object):

    class MouseManiupulator():

        ''' Método inicializador de la clase MouseManiupulator '''
        def __init__(self, screen):
            self.deck = []
            self.screen = screen
            self.hitboxes = []
            self.card = None
            self.coords = None

        ''' Se encarga de toar y dejar la carta en un stack seleccionado desde la interfaz '''
        def take_card(self, stack: list, coord: list):
            if len(stack) == 0 and self.card == None: # Retorno anticipado
                return
            if self.card == None: # Toma la carta si no hay una carta tomada aun
                self.card = stack[len(stack)-1]
                self.coords = coord[len(coord)-1]
                stack.pop()
            else: # Se encarga de agregar la carta al stack
                if len(stack) == 0 or self.deck.index(self.card) < self.deck.index(stack[len(stack)-1]) or self.deck.index(stack[len(stack)-1]) == len(self.deck)-1 or self.card == self.deck[len(self.deck)-1]:
                    stack.append(self.card)
                    temp = coord[len(coord)-1]
                    self.coords = (temp[0], temp[1]+25)
                    coord.append(self.coords)
                    self.card = None
                    self.coords = None

        ''' Crea las dimensiones de la hitbox de los stacks '''
        def build_hitboxes(self, juego):
            self.hitboxes.clear()
            cards_delta, x_delta = 25, 90
            for i in range(len(juego)):
                self.hitboxes.append(pg.Rect(450 - (x_delta * i), 50,
                                            80, 120 + (cards_delta * (len(juego[i])-1))))

    ''' Método inicializador de la clase Solitario '''
    def __init__(self, screen):
        self.screen = screen
        self.baraja = Baraja()
        self.avaliable = False
        self.won = False
        self.mouse_manipulation = self.MouseManiupulator(self.screen)
        self.buttons = []
        self.mazo = defaultdict(list)
        self.coor_cards = defaultdict(list)
        self.fill_deck()
        self.basic_config()

    ''' Se encarga de dibujar los elementos usados en la actividad Solitario '''
    def draw(self):
        ''' Verifica si el usuario gano '''
        for i in range(len(self.mazo)):
            if len(self.mazo[i]) == len(self.mouse_manipulation.deck):
                self.won = True
        ''' Imprime las cartas del juego '''
        for i in range(len(self.mazo)):
            for j in range(len(self.mazo[i])):
                self.screen.blit(self.mazo[i][j], self.coor_cards[i][j])
        ''' Muestra las hitboxes de los stacks '''
        for hitbox in self.mouse_manipulation.hitboxes:
            pg.draw.rect(self.screen, (0,0,0), hitbox, 2)
        ''' Muestra la carta tomada por el usuario '''
        if self.mouse_manipulation.card != None:
            self.mouse_manipulation.coords = pg.mouse.get_pos()
            self.screen.blit(self.mouse_manipulation.card, self.mouse_manipulation.coords)
        ''' Imprime los botones en la interfaz '''
        for i in range(1, len(self.buttons)):
            self.buttons[i].draw_button(self.screen)
        ''' Muestra la pantalla de ganador si se cumple la condicion '''
        if self.won:
            self.winner_screen()
            
    ''' Manejador de eventos de la actividad de Solitario '''        
    def event_manager(self, event: pg.event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            ''' Maneja los eventos de las hitboxes de los stacks '''
            for i in range(len(self.mazo)):
                if self.mouse_manipulation.hitboxes[i].collidepoint(pg.mouse.get_pos()) and not self.won:
                    self.mouse_manipulation.take_card(self.mazo[i], self.coor_cards[i])
                    self.mouse_manipulation.build_hitboxes(self.mazo)
            ''' Maneja los botones de la actividad'''
            if self.buttons[1].hitbox.collidepoint(pg.mouse.get_pos()):
                self.avaliable = False
            if self.buttons[2].hitbox.collidepoint(pg.mouse.get_pos()) or self.buttons[0].hitbox.collidepoint(pg.mouse.get_pos()):
                self.__init__(self.screen)
                self.avaliable = True

    ''' Se encarga de mostrat la pantalla de ganador de juego '''
    def winner_screen(self):
        temp_font = pg.font.Font(None, 50) # Fuente temporal
        text = temp_font.render('Ganaste!', True, (0,0,0))
        pg.draw.rect(self.screen, (255,255,243), (200, 225, self.screen.get_width()-400, self.screen.get_height()-450), 0)
        pg.draw.rect(self.screen, (0,0,0), (200, 225, self.screen.get_width()-400, self.screen.get_height()-450), 2)
        pg.draw.rect(self.screen, (255,255,255), self.buttons[0].hitbox, 0)
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, self.screen.get_height()//2 - 45))
        self.buttons[0].draw_button(self.screen)

    ''' Hardcodea las cordenadas y la primera hitbox de los stacks y las cartas '''
    def fill_deck(self):
        stack = 0
        deltaX, deltaY = 0, 0
        for i in range(self.baraja.len):
            if i == 0:
                self.mazo[stack].append(self.baraja.tail.data)
                self.coor_cards[stack].append((self.screen.get_width()-350, 50))
                deltaX += 90
                stack += 1
            elif (i-1)%3 == 0 and i > 1:
                self.mazo[stack].append(self.baraja.tail.data)
                self.coor_cards[stack].append((self.screen.get_width()-350-deltaX, 50+deltaY))
                deltaY = 0
                deltaX += 90
                stack += 1
            else:
                self.mazo[stack].append(self.baraja.tail.data)
                self.coor_cards[stack].append((self.screen.get_width()-350-deltaX, 50+deltaY))
                deltaY += 25
            self.baraja.pop_node()
        self.mouse_manipulation.build_hitboxes(self.mazo) # Constrruye las hitboxes de los stacks dependiendomsu pos
        self.baraja.recortar_sprite() # Recorta nuevamente el stack de cartas

    ''' Configuración básica de la actividad de cartas de solitario '''
    def basic_config(self):
        for i in range(len(self.mazo)):
            self.mouse_manipulation.deck.extend(self.mazo[i])
        self.mouse_manipulation.deck.reverse()
        self.buttons.append(Button('Aceptar', self.screen.get_width()//2 - 50, self.screen.get_height()//2 + 20, 100, 32))
        self.buttons.append(Button('Salir', self.screen.get_width()- 110, self.screen.get_height()-42, 100, 32))
        self.buttons.append(Button('Recoger', self.screen.get_width()- 110, self.screen.get_height()-84, 100, 32))

'''
La actividad de Grafos y ciudades permite al usuario ubicarse en un mapa de Colombia, 
siendo este representado por un grafo donde cada una de las ciudades visibles en el mapa 
es un vertice, y cada una de los posibles desplazamientos entre ciudades son sus aristas
'''
class GrafosCiudades:

    ''' Método inicializador de la clase GrafosCiudades '''
    def __init__(self, screen):
        self.screen = screen
        self.avaliable = False
        self.aristas_mostradas = False
        self.background = pg.image.load('mapa_col.png')
        self.contenido_ciudades = Grafo()
        self.origen = ComboBox('Ciudad Origen', 10, 10, 140, 32)
        self.destino = ComboBox('Ciudad Destino', 160, 10, 140, 32)
        self.botones = []
        self.keys = {}
        self.lista_coordenadas = []
        self.basic_config()

    ''' Se encarga de dibujar los elementos requeridos en la pantalla '''
    def draw(self):
        ''' Dibuja el mapa de colombia en la pantalla '''
        self.screen.blit(self.background, (0,0))
        ''' Dibuja la totalidad de los botones de la actividad '''
        for boton in self.botones:
            boton.draw_button(self.screen)
        ''' Dibuja las aristas del grafo si el usuario lo requiere '''
        if self.aristas_mostradas:
            self.draw_conections()
        ''' Dibyujado de los vertices del grafo '''
        self.draw_graph()
        ''' Dibuja el Dijkstra si se tienen las condiciones necesarias '''
        if len(self.contenido_ciudades.camino) > 1:
            self.draw_dijkstra() 
        ''' Dibujado de los Combo Box '''
        self.origen.deploy(self.screen)
        self.destino.deploy(self.screen)

    ''' Dibuja todos los vertices de un grafo '''
    def draw_graph(self):
        tempo_font = pg.font.Font(None, 24) # Fuente temporal
        for i in range(len(self.lista_coordenadas)):
            txt = tempo_font.render(self.origen.options[i], True, (255,255,255))
            pg.draw.circle(self.screen, (0,255,255), self.lista_coordenadas[i], 5, 0)
            pg.draw.circle(self.screen, (0,0,0), self.lista_coordenadas[i], 5, 2)
            self.screen.blit(txt, (self.lista_coordenadas[i][0] - txt.get_width()//2, self.lista_coordenadas[i][1] - 20))
    
    ''' Dibuja el camino más corto entre 2 vertices de un grafo '''
    def draw_dijkstra(self):
        temp_font, costo = pg.font.Font(None, 24), 0
        for i in range(len(self.contenido_ciudades.camino)-1):
            x1 = self.contenido_ciudades.vertices[self.contenido_ciudades.camino[i]]
            x2 = self.contenido_ciudades.vertices[self.contenido_ciudades.camino[i+1]]
            pg.draw.line(self.screen, (255,0,0), x1.coordenadas, x2.coordenadas, 5)
            costo += x2.distancia
            for arista in x1.vecinos:
                if arista[0] == x2.id:
                    txt = temp_font.render(str(arista[1]), True, (0,0,0))
            self.screen.blit(txt, (x1.coordenadas[0] - (x1.coordenadas[0] - x2.coordenadas[0])//2, 
                                    x1.coordenadas[1] - (x1.coordenadas[1] - x2.coordenadas[1])//2))
        self.mostrar_camino(costo, temp_font)
    
    ''' Dibuja el camino más corto en un recuadro de texto '''
    def mostrar_camino(self, costo, font):
        ciudades = [] # Genera una lista que tendra el nombre de las ciudades
        for v in self.contenido_ciudades.camino:
            ciudades.append(self.contenido_ciudades.vertices[v].name) # Agrega el nombre de la ciudad 
        recorrido = font.render('Camino: ' + str(ciudades) + '  Costo: ' + str(costo), True,(0,0,0))
        pg.draw.rect(self.screen, (255,255,243), (45, self.screen.get_height()-52, recorrido.get_width()+20, 32), 0)
        pg.draw.rect(self.screen, (0,0,0), (45, self.screen.get_height()-52, recorrido.get_width()+20, 32), 2)
        self.screen.blit(recorrido, (55, self.screen.get_height()-(52 - recorrido.get_height()//2))) 

    ''' Dibuja las intersecciones  internas del grafo '''
    def draw_conections(self):
        for v in self.contenido_ciudades.vertices:
            for destino in self.contenido_ciudades.vertices[v].vecinos:
                pg.draw.line(self.screen, (13,20,114), self.contenido_ciudades.vertices[v].coordenadas, 
                                self.contenido_ciudades.vertices[destino[0]].coordenadas, 1)

    ''' Maneja los eventos ocurridos dentro de la actividad de grafos '''
    def event_manager(self, e):
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            ''' Maneja los eventos generados por los botones '''
            if self.botones[0].hitbox.collidepoint(pg.mouse.get_pos()):
                if self.aristas_mostradas:
                    self.aristas_mostradas = False
                else:
                    self.aristas_mostradas = True
            if self.botones[1].hitbox.collidepoint(pg.mouse.get_pos()):
                if self.origen.selected_item != self.origen.name:
                    self.contenido_ciudades.dijkstra(self.keys[self.origen.selected_item])
                    if self.destino.selected_item != self.destino.name:
                        self.contenido_ciudades.camino_vertice(self.keys[self.destino.selected_item], self.keys[self.destino.selected_item])
            if self.botones[2].hitbox.collidepoint(pg.mouse.get_pos()):
                self.avaliable = False
                self.__init__(self.screen)
            ''' Maneja los eventos generados por los Combo Box '''
            if self.origen.size.collidepoint(pg.mouse.get_pos()):
                if self.origen.deployed:
                    self.origen.deployed = False
                else:
                    self.origen.deployed = True
            if self.destino.size.collidepoint(pg.mouse.get_pos()):
                if self.destino.deployed:
                    self.destino.deployed = False
                else:
                    self.destino.deployed = True      
            if self.origen.deployed:
                self.origen.select_item()
            if self.destino.deployed:
                self.destino.select_item()
                if self.origen.selected_item != self.origen.name and self.destino.selected_item != self.destino.name:
                    if not self.destino.deployed:
                        self.contenido_ciudades.camino_vertice(self.keys[self.origen.selected_item], self.keys[self.destino.selected_item])

    ''' Métodod de configuración básica de la actividad de grafos '''
    def basic_config(self):
        self.background = pg.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.botones.append(Button('Aristas', 310, 10, 90, 32))
        self.botones.append(Button('Dijsktra', 410, 10, 90, 32))
        self.botones.append(Button('Salir', self.screen.get_width()-130, self.screen.get_height()-53, 90, 32))
        self.read_json()
        self.lista_coordenadas.append((70,110)) # San Andres
        self.lista_coordenadas.append((250,410)) # Armeria
        self.lista_coordenadas.append((300,160)) # Barranquilla
        self.lista_coordenadas.append((390,320)) # Bucaramanga
        self.lista_coordenadas.append((340,400)) # Bogotá
        self.lista_coordenadas.append((200,450)) # Cali
        self.lista_coordenadas.append((270,180)) # Cartagena
        self.lista_coordenadas.append((430,260)) # Cúcuta
        self.lista_coordenadas.append((560,750)) # Leticia 
        self.lista_coordenadas.append((260,340)) # Medellin
        self.lista_coordenadas.append((250,240)) # Monteria
        self.lista_coordenadas.append((270,480)) # Neiva
        self.lista_coordenadas.append((235,380)) # Pereira
        self.lista_coordenadas.append((165,540)) # Pasto
        self.lista_coordenadas.append((400,135)) # Riohacha
        self.lista_coordenadas.append((345,140)) # Santa Marta
        self.lista_coordenadas.append((390,180)) # Valledupar
        self.lista_coordenadas.append((350,430)) # Villavicencio
        i  = 0
        for v in self.contenido_ciudades.vertices:
            self.contenido_ciudades.vertices[v].coordenadas = self.lista_coordenadas[i]
            i += 1
        for valor in self.keys.keys():
            self.origen.options.append(valor)
            self.destino.options.append(valor)
    
    ''' Método de lectura del JSON y adicion de ponderados aleatorios '''
    def read_json(self):
        with open('ciudades.json') as data: # Creamos data con el contenido del jsoon
            ciudades = json.load(data)
            
            for ciudad in ciudades: # Agregamos los vertices al grafo
                self.contenido_ciudades.agregar_vertice(ciudad.get('name'), ciudad.get('id'))
                self.keys[ciudad.get('name')] = ciudad.get('id') # Guerdamos datos necesarios para Combo Box

            for ciudad in ciudades:  # Agregamos las aristas de cada vertice
                for destino in ciudad.get('destinations'):
                    p = random.randint(1, 12) # Ponderado aleatorio
                    self.contenido_ciudades.generar_arista(ciudad.get('id'), destino, p)