# --------------------------------------------------------------------------------
#                                     PEDIDOS.PY
#
# Los pedidos deben ser almacenados en una lista enlazada, 
# donde cada nodo representa un pedido que contiene varios productos.
# --------------------------------------------------------------------------------

from typing import Optional
from productos import Producto

# Producto --> (Id_producto, nombre_producto, precio)

#        Producto_id                  Cantidad
#  1 --> (1, "Pantalón", 5€)             34       
#  2 --> (2, "Camiseta", 10€)             9
#  5 --> (5, "Vestido",  14€)            20

class LineaPedido:
    def __init__(self, producto_id: int, cantidad: int):
       self.producto_id = producto_id
       self.cantidad = cantidad
    
    
    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
        }
#   Id_pedido       Nombre_cliente     Lista_pedidos
#       15              Juan          LineaPedido(1, 8)       --> El producto 1 era: (1, "Pantalón", 5€)    
#       28              Laura         LineaPedido(2, 8)       --> El producto 2 era: (2, "Camiseta", 10€)
#       03              Pepe          LineaPedido(5, 1)       --> El producto 5 era: (5, "Vestido",  14€) 
class Pedido:
    def __init__(self, pedido_id: int, nombre_cliente: str, lista_pedidos: list[LineaPedido]):
        self.id = pedido_id
        self.nombre_cliente = nombre_cliente
        self.lista_pedidos = lista_pedidos

    def to_dict(self):
        return {
            "pedido_id": self.id,
            "nombre_cliente": self.nombre_cliente,
            "lista_productos": [ item.to_dict() for item in self.lista_pedidos]
        }   
    

class NodoPedido:
    def __init__(self, pedido:Pedido):
        self.pedido = pedido 
        self.siguiente = None 
    

class ListaPedidos:
    def __init__(self):
        self.cabeza = None 

    # Agregar un pedido (se añade al final)
    def agregar_pedido (self, pedido: Pedido):
        nuevo_pedido = NodoPedido(pedido)
        # Si la lista está vacía, significa que este pedido será el primero de la lista.
        if self.cabeza is None:
            self.cabeza = nuevo_pedido
        else:

            # La lista contiene elementos, se reccorre hasta llegar al final de la lista  (final del nodo)
            # para añadirlo como último.
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_pedido
    
    # Buscar un pedido por su identificador (id)
    def buscar_pedido (self, pedido_id: int) -> Pedido | None:
        if self.cabeza is None:
            return None 
        else:
            actual = self.cabeza
            encontrado = False
            res = None
            # Mientras que haya elementos y no se haya encontrado el "pedido", se sigue buscando.
            while actual is not None and encontrado is False:
                if actual.pedido.id == pedido_id:
                    encontrado = True
                    res = actual.pedido
                actual = actual.siguiente
            
            return res 
    
    # Actualizar todos los datos de un pedido dado un identificador
    def actualizar_pedido(self, pedido_id: int, pedido: Pedido) -> bool:
        pedido_antiguo = self.buscar_pedido(pedido_id)
        if pedido_antiguo is None:
            res = False
        else:
            pedido_antiguo.nombre_cliente = pedido.nombre_cliente
            pedido_antiguo.lista_pedidos = pedido.lista_pedidos
            res = True 

        return res


    # Eliminar pedido dado un identificador
    def eliminar_pedido(self, pedido_id: int) -> bool:
        if self.cabeza is None:
            return False 
        else:
            actual = self.cabeza
            encontrado = False
            anterior = None 
            
            # Mientras que haya elementos y no se haya encontrado el "pedido", se sigue buscando.
            while actual is not None and encontrado is False:
                if actual.pedido.id == pedido_id:
                    encontrado = True
                    # Si se ha encontrado el "pedido" se comprueba si está el primero de la lista o no.
                    if anterior is None:           # Si es el primero, se borra de la lista
                        self.cabeza = actual.siguiente
                    else:                          # Si no es el primero, significa que tiene nodos anteriores,
                                               # por tanto, se indica que el nodo anterior apunte al siguiente 
                                               # del que se va a borrar.
                        anterior.siguiente = actual.siguiente
                anterior = actual
                actual = actual.siguiente
                
        return encontrado

    # Devuelve la lista con todos los pedidos que hay existentes.
    def listar_pedidos(self) -> list[Pedido]:
        # Se crea una lista vacía de pedidos para almacenar todos los pedidos.
        lista_pedidos = [] 
        actual = self.cabeza
        # Se recorren todos los pedidos y se van añadiendo a la lista de pedidos
        while actual is not None:
            lista_pedidos.append(actual.pedido)
            actual = actual.siguiente
        return lista_pedidos

