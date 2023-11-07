# Python Imports.
from datetime import datetime, timedelta

# Framework Imports.
from flask.views import MethodView
from flask import request, jsonify, render_template
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import generate_password_hash, check_password_hash

# Own imports
from app import database as db, app
from app.models.models import (
    User,
    Category,
    Comment,
    Post,
)
from app.schemas.schemas import (
    UserSchema,
    ShowUsersBasicSchema,
    CategorySchema,
    PostSchema,
    CommentSchema,
)


class UsersAPI(MethodView):
    @jwt_required()
    def get(self, user_id=None):
        additional_info = get_jwt()
        # Paginado Usuarios
        page = request.args.get("page", 1, type=int)  # Def Value = 1
        can = request.args.get("can", 20, type=int)  # Def Value = 20
        users = db.session.query(User).paginate(page=page, per_page=can)
        # Show all results whit paginate.
        if additional_info["is_admin"]:
            if user_id is None:
                results = UserSchema().dump(users, many=True)
            # Only selected for ID.
            else:
                user = User.query.get(user_id)
                results = UserSchema().dump(user)
            return jsonify(results)
        else:
            if user_id is None:
                results = ShowUsersBasicSchema().dump(users, many=True)
            # Only selected for ID.
            else:
                user = User.query.get(user_id)
                results = ShowUsersBasicSchema().dump(user)
            return jsonify(results), 200

    def post(self):
        # Create User based in UserSchema
        user_json = UserSchema().load(request.json)
        username = user_json.get("username")
        password_hash = user_json.get("password_hash")
        is_admin = user_json.get("is_admin")

        # Hashed password gerator
        password_hash = generate_password_hash(
            password_hash, method="pbkdf2", salt_length=16
        )

        # New User Data
        new_user = User(
            username=username, password_hash=password_hash, is_admin=is_admin
        )

        # Add to DB new user.
        db.session.add(new_user)
        db.session.commit()

        # Confirmation of created user
        return jsonify({"Usuario nuevo creado": username}), 200

    def put(self, user_id):
        user = User.query.get(user_id)
        user_json = UserSchema().load(request.json)
        username = user_json.get("username")
        password_hash = user_json.get("password_hash")
        is_admin = user_json.get("is_admin")
        if username is None:
            # If only change the password
            password_hash = generate_password_hash(
                password_hash, method="pbkdf2", salt_length=16
            )
            user.is_admin = is_admin
            user.password_hash = password_hash
            db.session.commit()
            return (
                jsonify(
                    mensaje=f"Modificaste la contraseña de: {user.username}"
                ),
                201,
            )
        elif password_hash is None:
            # If only change the Username
            user.is_admin = is_admin
            user.username = username
            db.session.commit()
            return (
                jsonify(
                    mensaje=f"Modificaste nombre de usuario a: {user.username}"
                ),
                201,
            )
        else:
            # Modify everything
            user.username = username
            password_hash = generate_password_hash(
                password_hash, method="pbkdf2", salt_length=16
            )
            user.password_hash = password_hash
            user.is_admin = is_admin
            db.session.commit()
            return (
                jsonify(
                    mensaje=f"Modificaste nombre de usuario y contraseña de: {user.username}"
                ),
                201,
            )

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(mensaje=f"Borraste el Usuario {user_id}")


app.add_url_rule("/user", view_func=UsersAPI.as_view("user"))
app.add_url_rule("/user/<user_id>", view_func=UsersAPI.as_view("user_for_id"))


class CategoriesAPI(MethodView):
    def get(self, category_id=None):
        if category_id is None:
            categories = Category.query.all()
            result = CategorySchema(exclude=("id",)).dump(categories, many=True)

        else:
            category = Category.query.get(category_id)
            posts = Post.query.filter_by(category_id=category_id).all()
            post_schemas = []
            for post in posts:
                post_schema = PostSchema(
                    exclude=(
                        "id",
                        "content",
                        "author_id",
                        "category_id",
                        "date",
                    )
                ).dump(post)
                post_schemas.append(post_schema)

            result = {
                "category": CategorySchema(exclude=("id",)).dump(category),
                "posts": post_schemas,
            }
        return (jsonify(result), 200)

    def post(self):
        category_json = CategorySchema().load(request.json)
        name = category_json.get("name")
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return (
            jsonify(f"Nueva Categoria agregada: {new_category}"),
            201,
        )

    def put(self, category_id):
        category = Category.query.get(category_id)
        category_json = CategorySchema().load(request.json)
        name = category_json.get("name")
        category.name = name
        db.session.commit()
        return (jsonify(f"Nombre de categoria cambiado a: {name}"), 201)

    def delete(self, category_id):
        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()
        return (jsonify(mensaje=f"Borraste la categoria: {category}"), 200)


app.add_url_rule("/category", view_func=CategoriesAPI.as_view("category"))
app.add_url_rule(
    "/category/<category_id>",
    view_func=CategoriesAPI.as_view("category_for_id"),
)


class PostsAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            posts = Post.query.all()
            result = PostSchema(exclude=("id",)).dump(posts, many=True)
        else:
            post = Post.query.get(post_id)
            result = PostSchema(exclude=("id",)).dump(post)
        return (jsonify(result), 200)

    def post(self):
        post_json = PostSchema().load(request.json)
        title = post_json.get("title")
        content = post_json.get("content")
        date = post_json.get("date")
        author_id = post_json.get("author_id")
        category_id = post_json.get("category_id")
        nuevo_post = Post(
            title=title,
            content=content,
            date=date,
            author_id=author_id,
            category_id=category_id,
        )
        db.session.add(nuevo_post)
        db.session.commit()
        return (jsonify(f"Nuevo Post agregado: {title}"), 201)

    def put(self, post_id):
        post = Post.query.get(post_id)
        post_json = PostSchema().load(request.json)
        title = post_json.get("title")
        content = post_json.get("content")
        category_id = post_json.get("category_id")
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if category_id is not None:
            post.category_id = category_id

        db.session.commit()
        return (jsonify(f"Publicación editada: {post.title}"), 201)

    def delete(self, post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return (jsonify(mensaje=f"Eliminaste el Post: {post}"), 200)


app.add_url_rule("/post", view_func=PostsAPI.as_view("post"))
app.add_url_rule("/post/<post_id>", view_func=PostsAPI.as_view("post_for_id"))


class CommentAPI(MethodView):
    def post(self):
        comment_json = CommentSchema().load(request.json)
        content = comment_json.get("content")
        date = comment_json.get("date")
        author_id = comment_json.get("author_id")
        post_id = comment_json.get("post_id")
        new_comment = Comment(
            content=content, date=date, author_id=author_id, post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()
        return (jsonify(f"Nuevo comentario agregado: {content}"), 201)

    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return (jsonify(f"Eliminaste el Comentario: {comment}"), 200)


app.add_url_rule("/comment", view_func=CommentAPI.as_view("comment"))
app.add_url_rule(
    "/comment/<comment_id>", view_func=CommentAPI.as_view("comment_for_id")
)


class registerView(MethodView):
    def get(self):
        return render_template("register.html")

    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )
        nuevo_usuario = User(username=username, password_hash=password_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return render_template("register.html")


app.add_url_rule("/register", view_func=registerView.as_view("register"))

