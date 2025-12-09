# --------------------------------------------------------------------------------
#                                     PRODUCTOS.PY
#
# Los productos deben ser almacenados en un árbol binario de búsqueda (BST) 
# para permitir búsquedas eficientes.
# --------------------------------------------------------------------------------

# ------------------------------------------------------------
#                           PRODUCTO
# Se define la estructura de "Producto", compuesto por
# un identificador, nombre y precio. 
# ------------------------------------------------------------
class Producto:
    def __init__(self, producto_id: int, nombre_producto: str, precio_producto: float):
        self.id = producto_id
        self.nombre = nombre_producto
        self.precio = precio_producto

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio
        }
# ------------------------------------------------------------
#                           NODEPRODUCTO 
# Es el nodo "Producto" del árbol BST
# ------------------------------------------------------------
class NodeProducto:
    def __init__(self, producto: Producto): 
        self.value = producto # Propio valor (el valor que le pasamos para inicializarlo)
        self.left = None # Es posible que tenga un Hijo izquierdo
        self.right = None # ... Hijo derecho

# ------------------------------------------------------------
#                           PRODUCTOSTREEBST 
# Es el árbol BST
# -------------------------------------------------------------
class ProductosTreeBST:
    def __init__(self):
        self.root = None # Raíz del árbol

    # Inserción de un nuevo Producto (nodo) en el árbol
    def insertar(self, producto: Producto):
        self.root = self.insertar_rec(self.root, producto)

    # Inserción en el árbol (recursividad)    
    # En el árbol binario se tiene una ordenación.
    # Si el valor es más pequeño, nos vamos a la izquierda.
    # Si el valor es más grande, nos vamos  a la derecha

    # insert(Raíz donde le vamos a insertar el nuevo nodo y el valor del nuevo nodo)
    def insertar_rec(self, nodo: NodeProducto, producto: Producto): 
        if nodo is None: # Raíz no definida, significa que el nuevo nodo insertado será la raíz.
            return NodeProducto(producto) 
        if producto.id < nodo.value.id: 
            # Si el valor que se quiere insertar es más pequeño que el nodo actual, 
            # significa que se añadirá en su parte izquierda. 
            # Por tanto, se va a insertar su hijo izquierdo
            nodo.left = self.insertar_rec(nodo.left, producto)
            
        else: 
            # Si el valor que se quiere insertar es más grande que el nodo actual,
            # significa que se añadirá en su parte derecha.
            # Por tanto, se va a insertar su hijo derecho.
            nodo.right = self.insertar_rec(nodo.right, producto)
        return nodo
    
    # Buscar producto por un determinado identificador
    def buscar(self, producto_id: int) -> Producto | None :
        # Se busca un producto por su identificador (ID).
        # Devuelve como redultado:
        # - Producto: el propio producto.
        # - None: si no se ha encontrado.
        node = self.buscar_rec(self.root, producto_id)
        if node is None:
            return None 
        else:
            return node.value

    def buscar_rec(self, node:NodeProducto, producto_id: int) -> NodeProducto | None:

        # Si no hay nada, significa que estámos en un árbol vacío
        if node is None:
            return None
        
        # Si se ha encontrado un nodo con ese identificador, se devuelve el producto
        if node.value.id == producto_id:
            return node
        
        # Si el identificador es más pequeño que el nodo, 
        # significa que hay que buscar en la parte IZQUIERDA.
        if producto_id < node.value.id:
            return self.buscar_rec(node.left,producto_id)

        # Si el identificador es más grande que el nodo,
        # significa que hay que buscar en la parte DERECHA.
        if producto_id > node.value.id:
            return self.buscar_rec(node.right,producto_id)
        

#   Recorrer el árbol en "in order"
    def recorrido_inorder(self) -> list[Producto]:
        result = []
        self.recorrido_inorder_rec(self.root, result)
        return result
    
    def recorrido_inorder_rec(self, node: NodeProducto, result: list):
        if node is not None:
            self.recorrido_inorder_rec(node.left, result)
            result.append(node.value)
            self.recorrido_inorder_rec(node.right, result)

        
