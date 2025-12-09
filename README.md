# Estructura de datos avanzadas
# ----------------------------------------

----------
OBJETIVOS
----------
Desarrollar una API que permita gestionar los productos y los pedidos realizados 
por los clientes de una tienda online.

Los productos se almacenan utilizando un árbol binario de búsqueda (BST), mientras 
que los pedidos se guardan en una lista enlazada, donde cada nodo representa un 
pedido completo.

Este proyecto se ha implementado utilizando Flask y Python.

-----------
INSTALACIÓN
-----------

1. Crear un entorno virtual (recomendado)

python -m venv venv


2. Activarlo

venv\Scripts\activate


3. Instalar dependencias

pip install -r requirements.txt


4. Ejecutarlo

python app.py

-----------
ENDPOINTS
-----------

PRODUCTOS
---------
- POST /productos
Crea un nuevo producto.

    Body:

        {
            "nombre": "Vestido",
            "precio": 12.25
        }

- GET /productos/{id}

Obtiene la información de un producto por su identificador.



PEDIDOS
-------

- POST /pedidos
Crea un nuevo pedido.

        Body:
            {
                "nombre_cliente": "Pepe",
                "lista_pedidos": [
                    {"id_producto": 1, "cantidad": 2},
                    {"id_producto": 3, "cantidad": 8}
                ]
            }

- GET /pedidos/{id}

Obtiene la información de un pedido por su identificador.

- PUT /pedidos/{id}

Modifica un pedido existente.

        Body:
            {
                "nombre_cliente": "Laura",
                "lista_pedidos": [
                    {"id_producto": 2, "cantidad": 5}
                ]
            }


- DELETE /pedidos/{id}

Elimina un pedido existente.

- GET /pedidos

Obtiene el listado completo de pedidos existentes.
