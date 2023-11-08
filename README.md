# *PIT STOP BLOG*
#### Centurión - Filiberti

### Descripción:
Creacion de un miniblog desarrollado en Flask, utilizando las herramientas aprendidas en todo el año. Este blog contiene modelos de base de datos, schemas y vistas, para hacer uso a través de endpoints.


### Requisitos previos:

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Instrucciones de uso:


1. Clona el repositorio de la aplicación:
```
git clone https://github.com/juanjcenturion/pit_stop-blog.git
```

2. Crea tu archivo ".env" guiandote con el .env.example

3. Ejecuta la aplicacion con Docker Compose, esto creará contenedores para la aplicacion Flask y una Base de datos MySQL:
```
sudo docker-compose up -d
```

### Template:

El unico template disponible es: **'/register'**

### EndPoints:

Usuarios:

    GET /user: Obtiene todos los usuarios de la base de datos.
    GET /user/<user_id>: Obtiene un usuario específico de la base de datos por su ID.
    POST /user: Crea un nuevo usuario en la base de datos.
    PUT /user/<user_id>: Actualiza la información de un usuario específico de la base de datos por su ID.
    DELETE /user/<user_id>: Elimina un usuario específico de la base de datos por su ID.

Categorías:

    GET /category: Obtiene todas las categorías de la base de datos.
    GET /category/<category_id>: Obtiene una categoría específica de la base de datos por su ID.
    POST /category: Crea una nueva categoría en la base de datos.
    PUT /category/<category_id>: Actualiza la información de una categoría específica de la base de datos por su ID.
    DELETE /category/<category_id>: Elimina una categoría específica de la base de datos por su ID.

Publicaciones:

    GET /post: Obtiene todas las publicaciones de la base de datos.
    GET /post/<post_id>: Obtiene una publicación específica de la base de datos por su ID.
    POST /post: Crea una nueva publicación en la base de datos.
    PUT /post/<post_id>: Actualiza la información de una publicación específica de la base de datos por su ID.
    DELETE /post/<post_id>: Elimina una publicación específica de la base de datos por su ID.

Comentarios:

    POST /comment: Crea un nuevo comentario en la base de datos.
    DELETE /comment/<comment_id>: Elimina un comentario específico de la base de datos por su ID.

Inicio de sesión:

    GET /login


