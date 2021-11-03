class Post:
    def __init__(self, type, url, date, category, likes, id, nameauthor):
        self.type = type
        self.url = url
        self.date = date
        self.category = category
        self.likes = likes
        self.id = id
        self.nameauthor = nameauthor

    # metodos getter

    def getType(self):
        return self.type

    def getUrl(self):
        return self.url

    def getDate(self):
        return self.date

    def getCategory(self):
        return self.category

    def getLikes(self):
        return self.likes

    def getId(self):
        return self.id


    def getNameAuthor(self):
        return self.nameauthor

    # metodos setter

    def setType(self, type):
        self.type = type

    def setUrl(self, url):
        self.url = url

    def setDate(self, date):
        self.date = date

    def setId(self, id):
        self.id = id

    def setLikes(self, likes):
        self.likes = likes

    def setNameAuthor(self, nameauthor):
        self.nameauthor = nameauthor

    def setCategory(self, category):
        self.category = category

