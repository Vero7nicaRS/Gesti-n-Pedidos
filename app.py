from flask import Flask, request
from productos import Producto, ProductosTreeBST # Árbol de productos
from lista_enlazada_pedidos import LineaPedido, ListaPedidos, Pedido # Lista enlazada de pedidos

app = Flask(__name__)

# Se crean las variables para almacenar un árbol de productos y un listado de pedidos
arbol_productos = ProductosTreeBST()
lista_pedidos = ListaPedidos()

siguiente_id_producto = 1
siguiente_id_pedido = 1

@app.route('/') # Vamos a crear un endpoint raíz.
def home(): # Cada vez que alguien llame a este endpoint muestre el mensaje "Hello word"
    return "Hello world!" 

# ---------------------------------------------------------- ENDPOINTS----------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------- ENDPOINT PRODUCTOS  ----------------------------------------------------------
# A) Crear un producto.

# Método POST --> añadir un producto al árbol de productos
# Estructura:
# POST /productos
# Body JSON:
# {
#   "nombre": "Falda",
#   "precio": 13
# }
@app.route('/productos', methods=['POST'])
def post_producto():
    global siguiente_id_producto 
    # Se obtiene los datos del JSON.
    data = request.get_json()

    nombre_producto = data.get("nombre")
    precio_producto = data.get("precio")

    if nombre_producto is None or precio_producto is None:
        return {
            "message": "ERROR: Los campos 'nombre_producto' y 'precio_producto' son obligatorios."
        }, 400
    
    # Se crea un producto 
    producto = Producto(producto_id=siguiente_id_producto, 
                        nombre_producto=nombre_producto, 
                        precio_producto=precio_producto)
    
    # Se inserta el producto en el árbol de productos.
    arbol_productos.insertar(producto)
    # Se incrementa el identificador del producto para que se pueda 
    # usar el identificador correcto cuando se añada un nuevo producto
    siguiente_id_producto += 1

    return {
        "message": f"Se ha añadido el producto correctamente",
        "producto": producto.to_dict()
    }, 201


# B) Consultar información de producto por ID.

# Método GET  --> visualizar un producto al árbol de productos
# Estructura:
# GET /productos/<id_producto>
# Body JSON: Vacío.
@app.route('/productos/<int:id_producto>/', methods=['GET'])
def get_producto(id_producto):

    # Se busca el identificador del producto en el árbol de productos existentes.
    producto = arbol_productos.buscar(id_producto)
    if producto is None:
        return{
            "message": f"El producto '{id_producto}' no se ha encontrado"
        }, 404
    else:
        return{
            "message": f"El producto '{id_producto}' se ha encontrado",
            "producto": producto.to_dict()
        }, 200
# ---------------------------------------------------------- END POINT PRODUCTOS  ----------------------------------------------------------



# ---------------------------------------------------------- ENDPOINT PEDIDOS  ----------------------------------------------------------
# C) Crear nuevo pedido.

# Método POST --> añadir un pedido   
# Estructura:
# POST /productos
# Body JSON: (ejemplo)
# {
#   "nombre_cliente": "Pepe",
#   "lista_pedidos": [
#       {"id_producto": 4, "cantidad": 20},
#       {"id_producto": 2, "cantidad": 8},
#    ]
# }
@app.route('/pedidos', methods=['POST'])
def post_pedido():
    global siguiente_id_pedido 
    # Se obtiene los datos del JSON.
    data = request.get_json()

    nombre_cliente = data.get("nombre_cliente")
    lista_pedidos_json = data.get("lista_pedidos", [])

    # Se comprueba que se hayan enviado los datos correctos por el body JSON
    if nombre_cliente is None or not lista_pedidos_json:
        return {
            "message": "ERROR: Los campos 'nombre_cliente' y 'lista_pedidos' son obligatorios."
        }, 400
    
    res_lista_pedidos = []
    # Se recorre la lista de pedidos para añadirlo a una "Lista[LíneaPedido]"
    for linea in lista_pedidos_json:
         # {"id_producto": 4, "cantidad": 20},
        id_producto = linea.get("id_producto")
        cantidad_producto = linea.get("cantidad")

        # Se comprueba que se hayan obtenido los datos correctos en la línea de pedidos
        if id_producto is None or cantidad_producto is None:
            return {
                "message": "ERROR: Los campos 'id_producto' y 'cantidad_producto' "
                            " son obligatorios en la línea de pedidos."
            }, 400
        # Se busca si el identificador del producto existe en el árbol de los productos
        producto = arbol_productos.buscar(producto_id=id_producto)
        if producto is None:
            return {
                "message": f"ERROR: El producto '{id_producto}' no ha sido encontrado en los productos existentes "
            }, 404
        
        # Se crea la lista con todas las líneas de pedidos.
        linea_pedido = LineaPedido(producto_id= id_producto, cantidad= cantidad_producto)
        res_lista_pedidos.append(linea_pedido)

    # Se crea el pedido.
    pedido = Pedido(pedido_id = siguiente_id_pedido,
                    nombre_cliente = nombre_cliente,
                    lista_pedidos = res_lista_pedidos)
    
    # Se añade el pedido a la lista de pedidos existentes.
    lista_pedidos.agregar_pedido(pedido)
    # Se incrementa el identificador del pedido para que se pueda 
    # usar el identificador correcto cuando se añada un nuevo pedido
    siguiente_id_pedido += 1

    return {
        "message": f"Se ha añadido el pedido correctamente",
        "pedido": pedido.to_dict()
    }, 201




# D) Consultar información de pedido por ID.

# Método GET  --> visualizar un pedido 
# Estructura:
# GET /pedidos/<id_pedido>
# Body JSON: Vacío.

@app.route('/pedidos/<int:id_pedido>/', methods=['GET'])
def get_pedido(id_pedido):
    # Se busca el identificador del pedido en la lista de pedidos existentes.
    pedido = lista_pedidos.buscar_pedido(id_pedido)
    if pedido is None:
        return{
            "message": f"El pedido '{id_pedido}' no se ha encontrado"
        }, 404
    else:
        return{
            "message": f"El pedido '{id_pedido}' se ha encontrado",
            "pedido": pedido.to_dict()
        }, 200

# E) Actualizar un pedido existente

# Método PUT  --> modificar un pedido existente
# Estructura:
# PUT /pedidos/<id_pedido>
# Body JSON: {
#   "nombre_cliente": "Pepe",
#   "lista_pedidos": {
#       {"id_producto": 4, "cantidad": 20},
#       {"id_producto": 2, "cantidad": 8},
#    }
# }
@app.route('/pedidos/<int:id_pedido>/', methods=['PUT'])
def put_pedido(id_pedido):

    # Se obtiene los datos del JSON.
    data = request.get_json()

    nombre_cliente = data.get("nombre_cliente")
    lista_pedidos_json = data.get("lista_pedidos", [])

     # Se comprueba que se hayan enviado los datos correctos por el body JSON
    if nombre_cliente is None or not lista_pedidos_json:
        return {
            "message": "ERROR: Los campos 'nombre_cliente' y 'lista_pedidos' son obligatorios."
        }, 400
    
    res_lista_pedidos = []

    for linea in lista_pedidos_json:
        id_producto = linea.get("id_producto")
        cantidad_producto = linea.get("cantidad")

        if id_producto is None or cantidad_producto is None:
            return {
                "message": "ERROR: Los campos 'id_producto' y 'cantidad' "
                           "son obligatorios en cada línea de pedido."
            }, 400
        
        producto = arbol_productos.buscar(id_producto)
        if producto is None:
            return {
                "message": f"ERROR: El producto '{id_producto}' no ha sido encontrado en los productos existentes."
            }, 400
        
        linea_pedido = LineaPedido(producto_id=id_producto, cantidad=cantidad_producto)
        res_lista_pedidos.append(linea_pedido)

    act_pedido = Pedido(pedido_id=id_pedido, 
                        nombre_cliente=nombre_cliente,
                        lista_pedidos=res_lista_pedidos
                        )
    actualizado = lista_pedidos.actualizar_pedido(pedido_id=id_pedido, pedido=act_pedido)

    if actualizado is True:
        return {
            "message": f"El pedido '{id_pedido}' ha sido actualizado correctamente.",
            "pedido": act_pedido.to_dict()
        }, 200
    else:
        return {
            "message": f"El pedido '{id_pedido}' no se ha actualizado correctamente.",
            "pedido": act_pedido.to_dict()
        }, 404
    
# F) Eliminar un pedido.

# Método DELETE  --> eliminar un pedido existente
# Estructura:
# DELETE /pedidos/<id_pedido>
# Body JSON: Vacío.

@app.route('/pedidos/<int:id_pedido>/', methods=['DELETE'])
def delete_pedido(id_pedido):
    # Se busca el identificador del pedido en la lista de pedidos existentes.
    eliminado = lista_pedidos.eliminar_pedido(id_pedido)
    if eliminado is True:
        return{
            "message": f"El pedido '{id_pedido}' se ha eliminado correctamente."
        }, 200
    else:
        return{
            "message": f"El pedido '{id_pedido}' no se ha eliminado correctamente."
        }, 404

# G) Listar todos los pedidos.

# Método GET  --> obtener todos los pedidos existentes 
# Estructura:
# GET /pedidos
# Body JSON: Vacío.

@app.route('/pedidos', methods=['GET'])
def get_todos_pedidos():
    # Se obtienen todos los pedidos del listado
    listado_pedidos = lista_pedidos.listar_pedidos()
    if not listado_pedidos :
        return{
            "message": f"No hay ninguna lista de pedidos existentes."
        }, 200
    else:
        return{
            "message": f"Se ha encontrado una lista de pedidos.",
            "listado_pedidos": [p.to_dict() for p in listado_pedidos] 
        }, 200
# ---------------------------------------------------------- END ENDPOINT PEDIDOS  ----------------------------------------------------------


if __name__ == '__main__':  # Va al final
    app.run(debug=True)