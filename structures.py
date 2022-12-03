from collections import defaultdict
import pygame as pg

'''
    La baraja de cartas representa una estructura de cola para
    efectos practicos de este proyecto
'''

class Baraja:

    class Node:

        ''' Metodo inicializadora de Nodo '''
        def __init__(self, data):
            self.data = data
            self.next = None

    ''' Metodo inicializador de Baraja/Pila '''
    def __init__(self):
        self.sprite_cartas = "cards.jpg"
        self.head = None
        self.tail = None
        self.len = 0
        self.recortar_sprite()

    def append_node(self, data): 
        new_node = self.Node(data)
        if self.len == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = self.tail.next
        self.len += 1

    def pop_node(self):
        if self.len <= 1:
            self.head = None
            self.tail = None
            self.len = 0
            return
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
        cur.next = None
        self.tail = cur
        self.len -= 1

    def print(self):
        arr = []
        cur = self.head
        while cur != None:
            arr.append(cur.data)
            cur = cur.next
        print(arr, self.len)
            
    def recortar_sprite(self):
        baraja = pg.image.load(self.sprite_cartas)
        baraja = pg.transform.scale(baraja, (560, 240))

        for y in range(0, 240, 120):
            for x in range(0, 560, 80):
                curr_image = pg.Surface((80,120)).convert_alpha()
                curr_image.blit(baraja, (0,0), (x, y, 80, 120))
                self.append_node(curr_image)
    
        temp_val = self.head.data    
        self.head = self.head.next
        as_node = self.Node(temp_val)
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
        as_node.next = self.tail
        cur.next = as_node
        

class NAryTree(object):

    class Node(object):

        ''' Clase inicializzadora del nodo '''
        def __init__(self, data) -> None:
            self.data = data
            self.child = []

    ''' Clase inicializadora del arbol n-ario'''
    def __init__(self):
        self.root = None
        self.len = 0
        self.traversal = []
    
    ''' Método de incersion de un nodo '''
    def insert_child(self, root, parent, data):
        new_child = self.Node(data) # Crea el nodo que se va a insertar
        if not self.root:
            self.root = new_child
        else:
            if root.data == parent and len(root.child) < 3:
                if not self.non_equals(data) and data != parent: # Valida si el nodo ya existe dentro del padre
                    root.child.append(new_child)
                    self.len += 1
                else:
                    print('Nodo repetido')
            else:
                l = len(root.child) # Toma la cantidad de hijos para el llamado recursivo
                for i in range(l):
                    self.insert_child(root.child[i], parent, data) # Llamado recursivo

    ''' Método que valida la existencia previa de un nodo buscado '''
    def non_equals(self, data):
        temp = self.level_order_traversal()
        for level in temp:
            if data in level:
                return True
        return False

    def inorder(self):
        inorder = []
        def traversal(node):
            if node != None:
                traversal(node.left)
                inorder.append(node.data)
                traversal(node.right)
        traversal(self.root)
        self.traversal = inorder

    def preorder(self):
        preorder = []
        def traversal(node):
            if node != None:
                preorder.append(node.data)
                traversal(node.left)
                traversal(node.right)
        traversal(self.root)
        self.traversal = preorder
    
    def postorder(self):
        postorder = []
        def traversal(node):
            if node != None:
                traversal(node.left)
                traversal(node.right)
                postorder.append(node.data)
        traversal(self.root)
        self.traversal = postorder
        
    ''' Recorre un arbol N-Ario de forma recursiva en base a su profundidad '''    
    def level_order_traversal(self):
        route = defaultdict(list) # Crea el manejador de datos

        def dfs(node, level): # Funcion encargada de añadir los valores al manejador
            route[level].append(node.data)
            for child in node.child: 
                dfs(child,level+1) # LLamado recursivo p[or cada hijo

        dfs(self.root, 0) # Primer llamado
        self.traversal = [ans for k,ans in sorted(route.items())] 
        return [ans for k,ans in sorted(route.items())] 


class BinaryTree(object):

    class Node:

        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None

    def __init__(self) -> None:
        self.root = None
        self.len = 0
        self.traversal = []

    ''' Realiza la insercion de un nodo dentro de un arbol binario '''
    def insert_node(self, root: Node, data):
        if self.root == None:
            self.root = self.Node(data)
            return
        if data < root.data:
            if root.left is None:
                if not self.non_equals(data):
                    root.left = self.Node(data)
            else:
                self.insert_node(root.left, data)
        else:
            if root.right is None:
                if not self.non_equals(data):
                    root.right = self.Node(data)
            else:
                self.insert_node(root.right, data)
    
    ''' Método que valida la existencia previa de un nodo buscado '''
    def non_equals(self, data):
        temp = self.level_order_traversal()
        for level in temp:
            if data in level:
                return True
        return False

    ''' Realiza el recorrido inorder de un arbol binario '''
    def inorder(self):
        inorder = []
        def traversal(node):
            if node != None:
                traversal(node.left)
                inorder.append(node.data)
                traversal(node.right)
        traversal(self.root)
        self.traversal = inorder

    ''' Realiza el recorrido preorder de un arbol binario '''
    def preorder(self):
        preorder = []
        def traversal(node):
            if node != None:
                preorder.append(node.data)
                traversal(node.left)
                traversal(node.right)
        traversal(self.root)
        self.traversal = preorder
    
    ''' Realiza el recorrido postorder de un arbol binario'''
    def postorder(self):
        postorder = []
        def traversal(node):
            if node != None:
                traversal(node.left)
                traversal(node.right)
                postorder.append(node.data)
        traversal(self.root)
        self.traversal = postorder

    ''' Recorrido por amplitud de un arbol binario'''
    def level_order_traversal(self):
        route = defaultdict(list) # Crea el manejador de datos

        def dfs(node, level): # Funcion encargada de añadir los valores al manejador
            route[level].append(node.data)
            if node.left != None:
                dfs(node.left, level+1)
            if node.right != None:
                dfs(node.right, level+1)

        dfs(self.root, 0) # Primer llamado
        self.traversal = [ans for k,ans in sorted(route.items())] 
        return [ans for k,ans in sorted(route.items())] 


class Grafo:

    class Vertice:

        ''' Método constructor de la clase vertice '''
        def __init__(self, name, id):
            self.name = name
            self.id = id # id --> Nombre o diferenciador del grafo
            self.coordenadas = None
            self.predecesor = None
            self.distancia = float('inf')
            self.visitado = False
            self.vecinos = []
        
        ''' Añade un id de un vertice de id (v) distinto como un vecino '''
        def agregar_vecino(self, v, p):
            if not v in self.vecinos:
                self.vecinos.append((v, p)) # Añadimos el id del vertice como vecino
    
    ''' Método constructor de la clase grafo '''
    def __init__(self):
        self.vertices = {}
        self.camino =[]

    ''' Añade o actualiza un vertice con cierto idn (v) '''
    def agregar_vertice(self, n, v):
        if not v in self.vertices:
            self.vertices[v] = self.Vertice(n,v) # Añadimos el vertice al diccionario
    
    def generar_arista(self, a, b, p):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregar_vecino(b, p)
            self.vertices[b].agregar_vecino(a, p)

    def minimo(self, lista):
        if len(lista) > 0:
            min = self.vertices[lista[0]].distancia
            v = lista[0]
            for element in lista:
                if min > self.vertices[element].distancia:
                    min = self.vertices[element].distancia
                    v = element 
            return v
    
    def camino_vertice(self, a, b):
        camino = []
        actual = b
        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].predecesor
        self.camino =  camino

    def dijkstra(self, a):
        if a in self.vertices:
            self.vertices[a].distancia = 0
            actual = a
            no_visitados = []

            for v in self.vertices:
                if v != a:
                    self.vertices[v].distancia = float('inf') # Todas las distancias como infinito
                self.vertices[v].visitado = False
                self.vertices[v].predecesor = None # Predecesores nulos
                no_visitados.append(v) # Añadir nodos a no visitados

            while len(no_visitados) > 0:
                for arista in self.vertices[actual].vecinos:
                    if self.vertices[arista[0]].visitado == False:
                        if self.vertices[actual].distancia + arista[1] < self.vertices[arista[0]].distancia:
                            self.vertices[arista[0]].distancia = self.vertices[actual].distancia + arista[1]
                            self.vertices[arista[0]].predecesor = actual

                self.vertices[actual].visitado = True
                no_visitados.remove(actual)
                actual = self.minimo(no_visitados)
        else:
            return False


