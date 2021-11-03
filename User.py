class User:
    def __init__(self, name, gender, username, email, password, cantidadposts, id):
        self.name = name
        self.gender = gender
        self.username = username
        self.email = email
        self.password = password
        self.cantidadposts = cantidadposts
        self.id = id

    # metodos getter

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def getId(self):
        return self.id

    def getCantidadPosts(self):
        return self.cantidadposts

    # metodos setter

    def setName(self, name):
        self.name = name

    def setGender(self, gender):
        self.gender = gender

    def setUsername(self, username):
        self.username = username

    def setEmail(self, email):
        self.email = email

    def setPassword(self, password):
        self.password = password

    def setCantidadPosts(self, cantidadposts):
        self.cantidadposts = cantidadposts
