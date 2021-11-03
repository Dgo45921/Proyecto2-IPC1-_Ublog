from flask import Flask, jsonify, request, json
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS

from User import User
from Post import Post
from Like import Like

Lista_Posts = []
Cantidad_Posts = 1
ListaOrdenadaPosts = []

Lista_Usuarios = [User("Darwin Arevalo", "M", "admin", "admin@ipc1.com", "admin@ipc1", 0, 1)]
Cantidad_Usuarios = 2

Lista_Likes = []
Cantidad_Likes = 0
id_logueado = -1

logueado = False

app = Flask(__name__)
CORS(app)


@app.route('/')
def Index():
    return "corriendo"


# MODULO DE USUARIOS -------------------------------------------------------------------------------

@app.route('/ModificaUser', methods=["PUT"])
def ModificarUser():
    num_en_password = False
    global Cantidad_Usuarios
    global Lista_Usuarios, Lista_Posts
    name = request.json['name']
    gender = request.json['gender']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    id = int(request.json['id'])
    oldusername = request.json['oldusername']
    special_characters = "@#$%^&*()-+?_=,<>/"" "
    indiceuser = -1

    for caracter in password:
        if caracter.isdigit():
            num_en_password = True
            break

    for i in range(len(Lista_Usuarios)):
        if Lista_Usuarios[i].getId() == id:
            indiceuser = i
            break

    for i in range(0, indiceuser, 1):
        if Lista_Usuarios[i].getUsername() == username or Lista_Usuarios[i].getEmail() == email:
            return jsonify({'estado': "repetido"})

    print("Acaba el primer ciclo")

    for i in range(indiceuser + 1, len(Lista_Usuarios), 1):
        if Lista_Usuarios[i].getUsername() == username or Lista_Usuarios[i].getEmail() == email:
            return jsonify({'estado': "repetido"})

    if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
            c in special_characters for c in password) and len(password) >= 8 and num_en_password:
        for i in range(len(Lista_Usuarios)):
            if Lista_Usuarios[i].getId() == id:
                Lista_Usuarios[i].setName(name)
                Lista_Usuarios[i].setGender(gender)
                Lista_Usuarios[i].setUsername(username)
                Lista_Usuarios[i].setEmail(email)
                Lista_Usuarios[i].setPassword(password)

                for j in range(len(Lista_Posts)):
                    if Lista_Posts[j].getNameAuthor() == oldusername:
                        Lista_Posts[j].setNameAuthor(username)

                return jsonify({'estado': "Success"})
    else:
        print("no podemos agregar al usuario")
        return jsonify({'estado': "Fallo"})


@app.route('/Crear_Usuario', methods=["POST"])
def CrearUsuario():
    num_en_password = False
    global Cantidad_Usuarios
    global Lista_Usuarios
    name = request.json['name']
    gender = request.json['gender']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    special_characters = "@#$%^&*()-+?_=,<>/"" "

    for caracter in password:
        if caracter.isdigit():
            num_en_password = True
            break

    for usuario in Lista_Usuarios:
        if usuario.getUsername() == username or usuario.getEmail() == email:
            return jsonify({'estado': "repetido"})

    if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
            c in special_characters for c in password) and len(password) >= 8 and num_en_password:
        NuevoUser = User(name, gender, username, email, password, 0, Cantidad_Usuarios)
        Lista_Usuarios.append(NuevoUser)
        Cantidad_Usuarios += 1
        return jsonify({'estado': "exito"})
    else:
        print("no podemos agregar al usuario")
        return jsonify({'estado': "fallo"})


@app.route('/VerUsuarios')
def VerUsuarios():
    global Lista_Usuarios
    datos = []
    for usuario in Lista_Usuarios:
        objeto = {
            'name': usuario.getName(),
            'gender': usuario.getGender(),
            'username': usuario.getUsername(),
            'email': usuario.getEmail(),
            'password': usuario.getPassword(),
            'id': usuario.getId(),
            'num_posts': usuario.getCantidadPosts()
        }
        datos.append(objeto)
    return jsonify(datos)


@app.route('/LoginUser', methods=["POST"])
def LoginUser():
    global id_logueado, logueado
    encontrado = False
    username = request.json['username']
    password = request.json['password']

    if username == "admin" and password == "admin@ipc1":
        return jsonify({'user': "admin",
                        'id': 0})

    for user in Lista_Usuarios:
        if user.getUsername() == username and user.getPassword() == password:
            id_logueado = user.getId()
            encontrado = True

    if encontrado:
        return jsonify({'user': username,
                        'id': id_logueado})
    else:
        return jsonify({'user': "null"})


@app.route('/CreaPost', methods=["POST"])
def CreaPost():
    global Lista_Posts, Cantidad_Posts, Lista_Usuarios
    type = request.json['type']
    url = request.json['url']
    date = request.json['date']
    category = request.json['category']
    author = request.json['author']

    if type == "videos":
        embed = "https://www.youtube.com/embed/"
        urlvideo = embed + get_yt_video_id(url)
        nuevopost = Post(type, urlvideo, date, category, 0, Cantidad_Posts, author)
        Lista_Posts.append(nuevopost)
        Cantidad_Posts += 1
        for user in Lista_Usuarios:
            if author == user.getUsername():
                user.setCantidadPosts(user.getCantidadPosts() + 1)
                break

        return jsonify({'estado': "Success"})

    else:
        nuevopost = Post(type, url, date, category, 0, Cantidad_Posts, author)
        Lista_Posts.append(nuevopost)
        Cantidad_Posts += 1
        for user in Lista_Usuarios:
            if author == user.getUsername():
                user.setCantidadPosts(user.getCantidadPosts() + 1)
                break

        return jsonify({'estado': "Success"})


@app.route('/VerPosts')
def PostsCreados():
    global Lista_Posts
    datos = []
    for post in Lista_Posts:
        objeto = {
            'type': post.getType(),
            'url': post.getUrl(),
            'date': post.getDate(),
            'category': post.getCategory(),
            'likes': post.getLikes(),
            'id': post.getId(),
            'author': post.getNameAuthor()
        }
        datos.append(objeto)
    return jsonify(datos)


@app.route('/DarLike', methods=["POST"])
def DarLike():
    global Lista_Likes, Cantidad_Likes, Lista_Posts
    idpost = int(request.json['idpost'])
    authorlike = int(request.json['idauthor'])
    IndiceDelLike = -1
    PostLikeado = False
    nuevo_like = Like(authorlike, idpost)
    nuevo_like.getIdAuthor()
    indicedelpost = -1

    for i in range(len(Lista_Posts)):
        if Lista_Posts[i].getId() == idpost:
            indicedelpost = i

    for i in range(len(Lista_Likes)):
        if Lista_Likes[i].getIdAuthor() == authorlike and Lista_Likes[i].getIdPost() == idpost:
            IndiceDelLike = i
            PostLikeado = True
            break

    if PostLikeado:
        print("ya likeado")
        Lista_Posts[indicedelpost].setLikes(Lista_Posts[indicedelpost].getLikes() - 1)
        Lista_Likes.remove(Lista_Likes[IndiceDelLike])

    else:
        print("aun no likeado")
        Lista_Likes.append(nuevo_like)
        Lista_Posts[indicedelpost].setLikes(Lista_Posts[indicedelpost].getLikes() + 1)

    return "RECIBIDO"


@app.route('/VerLikes')
def VerLikes():
    global Lista_Likes
    datos = []
    for laik in Lista_Likes:
        objeto = {
            'AuthorId': laik.getIdAuthor(),
            'PostId': laik.getIdPost()
        }
        datos.append(objeto)
    return jsonify(datos)


@app.route('/Ranking')
def Ranking():
    global Lista_Posts, ListaOrdenadaPosts
    ListaOrdenadaPosts = sorted(Lista_Posts, key=lambda likes: likes.getLikes(), reverse=True)
    datos = []
    for post in ListaOrdenadaPosts:
        objeto = {
            'type': post.getType(),
            'url': post.getUrl(),
            'date': post.getDate(),
            'category': post.getCategory(),
            'likes': post.getLikes(),
            'id': post.getId(),
            'author': post.getNameAuthor()
        }
        datos.append(objeto)
    return jsonify(datos)


@app.route('/MisPosts', methods=["POST"])
def MisPosts():
    usernamesolicitado = request.json['usernameauthor']

    global Lista_Posts, ListaOrdenadaPosts
    ListaOrdenadaPosts = sorted(Lista_Posts, key=lambda likes: likes.getLikes(), reverse=True)
    datos = []
    for i in range(len(ListaOrdenadaPosts)):
        objeto = {
            'type': ListaOrdenadaPosts[i].getType(),
            'url': ListaOrdenadaPosts[i].getUrl(),
            'date': ListaOrdenadaPosts[i].getDate(),
            'category': ListaOrdenadaPosts[i].getCategory(),
            'likes': ListaOrdenadaPosts[i].getLikes(),
            'author': ListaOrdenadaPosts[i].getNameAuthor(),
            'posicion': i + 1
        }
        if usernamesolicitado == ListaOrdenadaPosts[i].getNameAuthor():
            datos.append(objeto)

    return jsonify(datos)


# ------------------ rutas para el administrador-------------------------------------


@app.route('/RecibirPosts', methods=["POST"])
def RecibirPosts():
    try:
        global Lista_Posts, Cantidad_Posts
        contenido = request.json['content']
        posts = json.loads(contenido)
        images = posts['images']
        videos = posts['videos']

        for i in range(len(images)):
            NuevaImagen = Post("images", images[i]["url"], images[i]["date"], images[i]["category"], 0, Cantidad_Posts,
                               images[i]["author"])
            Lista_Posts.append(NuevaImagen)
            Cantidad_Posts += 1

            for j in range(len(Lista_Usuarios)):
                if images[i]["author"] == Lista_Usuarios[j].getUsername():
                    Lista_Usuarios[j].setCantidadPosts(Lista_Usuarios[j].getCantidadPosts() + 1)
                    break

        for i in range(len(videos)):
            NuevoVideo = Post("videos", "https://www.youtube.com/embed/" + get_yt_video_id(videos[i]["url"]),
                              videos[i]["date"], videos[i]["category"], 0, Cantidad_Posts, videos[i]["author"])
            Lista_Posts.append(NuevoVideo)
            Cantidad_Posts += 1

            for j in range(len(Lista_Usuarios)):
                if images[i]["author"] == Lista_Usuarios[j].getUsername():
                    Lista_Usuarios[j].setCantidadPosts(Lista_Usuarios[j].getCantidadPosts() + 1)
                    break

        return jsonify({'estado': "Success"})
    except:
        return jsonify({'estado': "Fallo"})


@app.route('/RecibirUsers', methods=["POST"])
def RecibirUsers():
    try:
        global Lista_Usuarios, Cantidad_Usuarios
        contenido = request.json['content']
        users = json.loads(contenido)
        for i in range(len(users)):
            NuevoUser = User(users[i]['name'], users[i]['gender'].upper(), users[i]['username'], users[i]['email'],
                             users[i]['password'], 0, Cantidad_Usuarios)
            Lista_Usuarios.append(NuevoUser)
            Cantidad_Usuarios += 1

        return jsonify({'estado': "Success"})
    except:
        return jsonify({'estado': "Fallo"})


@app.route('/TablaUsuarios')
def TablaUsuarios():
    global Lista_Usuarios, Lista_Posts
    datos = []

    for i in range(1, len(Lista_Usuarios)):
        posts = []
        for post in Lista_Posts:
            if post.getNameAuthor() == Lista_Usuarios[i].getUsername():
                post = {
                    'type': post.getType(),
                    'likes': post.getLikes(),
                    'idpost': post.getId(),
                    'url': post.getUrl(),
                    'date': post.getDate(),
                    'category': post.getCategory(),
                    'author': post.getNameAuthor()
                }
                posts.append(post)

        objeto = {
            'name': Lista_Usuarios[i].getName(),
            'gender': Lista_Usuarios[i].getGender(),
            'username': Lista_Usuarios[i].getUsername(),
            'email': Lista_Usuarios[i].getEmail(),
            'password': Lista_Usuarios[i].getPassword(),
            'id': Lista_Usuarios[i].getId(),
            'posts': posts,
            'cantidad_posts': Lista_Usuarios[i].getCantidadPosts()
        }
        datos.append(objeto)

    return jsonify(datos)


@app.route('/DeleteUser/<int:id>', methods=["DELETE"])
def DeleteUser(id):
    print("Hey el id es:", id)
    global Lista_Usuarios, Cantidad_Usuarios, Lista_Posts, Lista_Likes, Cantidad_Posts, Cantidad_Likes
    usuario_a_eliminar = None
    posts_a_eliminar = []
    likes_a_eliminar = []
    posts_a_quitar_like = []
    username = ""
    for user in Lista_Usuarios:
        if user.getId() == id:
            usuario_a_eliminar = user
            username = user.getUsername()
            break
    Lista_Usuarios.remove(usuario_a_eliminar)

    for post in Lista_Posts:
        if post.getNameAuthor() == username:
            posts_a_eliminar.append(post)

    for like in Lista_Likes:
        if like.getIdAuthor() == id:
            likes_a_eliminar.append(like)

    for i in range(len(posts_a_eliminar)):
        Lista_Posts.remove(posts_a_eliminar[i])

    for i in range(len(likes_a_eliminar)):
        for j in range(len(Lista_Posts)):
            if likes_a_eliminar[i].getIdPost() == Lista_Posts[j].getId():
                posts_a_quitar_like.append(j)
        Lista_Likes.remove(likes_a_eliminar[i])

    for i in range(len(posts_a_quitar_like)):
        Lista_Posts[posts_a_quitar_like[i]].setLikes(Lista_Posts[posts_a_quitar_like[i]].getLikes() - 1)

    return jsonify({"estado": "exito"})


@app.route('/ModificaUserAdmin/<int:idrecibido>', methods=["PUT"])
def EditUserAdmin(idrecibido):
    num_en_password = False
    global Cantidad_Usuarios
    global Lista_Usuarios, Lista_Posts
    name = request.json['name']
    gender = request.json['gender']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    id = idrecibido
    special_characters = "@#$%^&*()-+?_=,<>/"" "
    indiceuser = -1
    oldusername = ""

    for caracter in password:
        if caracter.isdigit():
            num_en_password = True
            break

    for i in range(len(Lista_Usuarios)):
        if Lista_Usuarios[i].getId() == id:
            indiceuser = i
            break

    oldusername = Lista_Usuarios[indiceuser].getUsername()

    for i in range(0, indiceuser, 1):
        if Lista_Usuarios[i].getUsername() == username or Lista_Usuarios[i].getEmail() == email:
            return jsonify({'estado': "repetido"})

    print("Acaba el primer ciclo")

    for i in range(indiceuser + 1, len(Lista_Usuarios), 1):
        if Lista_Usuarios[i].getUsername() == username or Lista_Usuarios[i].getEmail() == email:
            return jsonify({'estado': "repetido"})

    if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
            c in special_characters for c in password) and len(password) >= 8 and num_en_password:
        for i in range(len(Lista_Usuarios)):
            if Lista_Usuarios[i].getId() == id:
                Lista_Usuarios[i].setName(name)
                Lista_Usuarios[i].setGender(gender)
                Lista_Usuarios[i].setUsername(username)
                Lista_Usuarios[i].setEmail(email)
                Lista_Usuarios[i].setPassword(password)

                for j in range(len(Lista_Posts)):
                    if Lista_Posts[j].getNameAuthor() == oldusername:
                        Lista_Posts[j].setNameAuthor(username)

                return jsonify({'estado': "Success"})
    else:
        print("no podemos agregar al usuario")
        return jsonify({'estado': "Fallo"})


@app.route('/ObtenerUsuario', methods=["POST"])
def ObtieneUser():
    global Lista_Usuarios
    idabuscar = int(request.json['userid'])
    user = None

    for i in range(len(Lista_Usuarios)):
        if Lista_Usuarios[i].getId() == idabuscar:
            user = Lista_Usuarios[i]
            break

    datosuser = {
        'name': user.getName(),
        'gender': user.getGender(),
        'username': user.getUsername(),
        'email': user.getEmail(),
        'password': user.getPassword(),
        'cant_posts': user.getCantidadPosts(),
        'id': user.getId()
    }

    return jsonify(datosuser)


@app.route('/DeletePost/<int:id>', methods=["DELETE"])
def DeletePost(id):
    print("Hey el id es:", id)
    global Lista_Usuarios, Cantidad_Usuarios, Lista_Posts, Lista_Likes, Cantidad_Posts, Cantidad_Likes
    Indices_de_likes_a_eliminar = []
    AuthorPost = ""

    for post in Lista_Posts:
        if post.getId() == id:
            Lista_Posts.remove(post)
            AuthorPost = post.getNameAuthor()
            break

    for i in range(len(Lista_Likes)):
        if Lista_Likes[i].getIdPost() == id:
            Indices_de_likes_a_eliminar.append(i)

    print(Indices_de_likes_a_eliminar)
    for i in range(len(Indices_de_likes_a_eliminar)):
        Lista_Likes.remove(Lista_Likes[Indices_de_likes_a_eliminar[i]])

    for i in range(len(Lista_Usuarios)):
        if Lista_Usuarios[i].getUsername() == AuthorPost:
            Lista_Usuarios[i].setCantidadPosts(Lista_Usuarios[i].getCantidadPosts() - 1)
            break

    return jsonify({"estado": "exito"})


@app.route('/EditPost/<int:id>', methods=["PUT"])
def EditPost(id):
    global Lista_Posts, Lista_Usuarios
    print("Hey el id es ", id)
    type = request.json['type']
    url = request.json['url']
    category = request.json['category']
    author = request.json['author']
    date = request.json['date']
    old_author = ""
    index_old_author = -1
    index_new_author = -1
    index_post = -1
    Existent_User = False
    for i in range(len(Lista_Usuarios)):
        if Lista_Usuarios[i].getUsername() == author:
            Existent_User = True
            index_new_author = i
            break

    if Existent_User:
        for i in range(len(Lista_Posts)):
            if Lista_Posts[i].getId() == id:
                index_post = i
                old_author = Lista_Posts[index_post].getNameAuthor()
                break

        for i in range(len(Lista_Usuarios)):
            if Lista_Usuarios[i].getUsername() == old_author:
                index_old_author = i
                break
        if type == "videos":
            embed = "https://www.youtube.com/embed/"
            urlvideo = embed + get_yt_video_id(url)
            Lista_Posts[index_post].setUrl(urlvideo)
        else:
            Lista_Posts[index_post].setUrl(url)

        Lista_Posts[index_post].setNameAuthor(author)
        Lista_Posts[index_post].setDate(date)
        Lista_Posts[index_post].setCategory(category)
        Lista_Posts[index_post].setType(type)
        Lista_Usuarios[index_old_author].setCantidadPosts(Lista_Usuarios[index_old_author].getCantidadPosts() - 1)
        Lista_Usuarios[index_new_author].setCantidadPosts(Lista_Usuarios[index_new_author].getCantidadPosts() + 1)
        return jsonify({"estado": "exito"})

    else:
        return jsonify({"estado": "NonExistent"})


@app.route('/InfoPost/<int:id>')
def InfoPost(id):
    global Lista_Posts
    print("Hey el id es ", id)
    posthallado = None

    for post in Lista_Posts:
        if post.getId() == id:
            posthallado = post
            break

    datospost = {
        'type': posthallado.getType(),
        'url': posthallado.getUrl(),
        'date': posthallado.getDate(),
        'category': posthallado.getCategory(),
        'Likes': posthallado.getLikes(),
        'id': posthallado.getId(),
        'author': posthallado.getNameAuthor()
    }
    return jsonify(datospost)


@app.route('/TopUsers')
def TopUsers():
    global Lista_Usuarios
    ListaUsers = []
    for i in range(len(Lista_Usuarios)):
        if i > 0:
            ListaUsers.append(Lista_Usuarios[i])

    UsersOrdenados = sorted(ListaUsers, key=lambda numposts: numposts.getCantidadPosts(), reverse=True)
    Ordenados = []
    if len(UsersOrdenados) < 5 or len(UsersOrdenados) == 0:
        return jsonify({"data": "NoData"})


    elif len(UsersOrdenados) == 6 or len(UsersOrdenados) > 5:
        for i in range(0, 5, 1):
            User = {
                'username': UsersOrdenados[i].getUsername(),
                'CanPosts': UsersOrdenados[i].getCantidadPosts()
            }
            if UsersOrdenados[i].getUsername() != "admin":
                Ordenados.append(User)
        return jsonify({"data": Ordenados})


@app.route('/TopPosts')
def TopPosts():
    global Lista_Posts
    ListaPosts = []
    for i in range(len(Lista_Posts)):
         ListaPosts.append(Lista_Posts[i])

    PostsOrdenados = sorted(ListaPosts, key=lambda numposts: numposts.getLikes(), reverse=True)
    Ordenados = []
    if len(PostsOrdenados) < 5 or len(PostsOrdenados) == 0:
        return jsonify({"data": "NoData"})


    elif len(PostsOrdenados) == 6 or len(PostsOrdenados) > 5:
        for i in range(0, 5, 1):
            Post = {
                'id': PostsOrdenados[i].getId(),
                'likes': PostsOrdenados[i].getLikes()
            }
            Ordenados.append(Post)
        return jsonify({"data": Ordenados})


# ------------------ Funciones externas------------------------------
def get_yt_video_id(input_link):
    if input_link.startswith(('youtu', 'www')):
        input_link = 'https://' + input_link

    try:
        query = urlparse(input_link)

        if 'youtube' in query.hostname:
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                return query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            return query.path[1:]
        elif 'youtube' in query.hostname:
            return query.path[1:]
        else:
            raise ValueError
    except:
        return input_link


if __name__ == '__main__':
    app.run(debug=True)
