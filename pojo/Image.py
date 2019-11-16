class Work:
    __id = None
    __artist = None
    __artist_name = None
    __name = None
    __created = None
    __description = None
    __tags = []
    __forks = 0
    __likes = 0
    __allow_download = False
    __allow_sketch = False
    __allow_fork = False
    __address = None

    def set_address(self, address):
        self.__address = address
        return

    def set_id(self, id):
        self.__id = id
        return

    def set_artist(self, artist):
        self.__artist = artist
        return

    def set_artist_name(self, artist_name):
        self.__artist_name = artist_name
        return

    def set_name(self, name):
        self.__name = name
        return

    def set_created(self, created):
        self.__created = created
        return

    def set_description(self, description):
        self.__description = description
        return

    def set_tags(self, tags):
        self.__tags = tags
        return

    def set_forks(self, forks):
        self.__forks = forks
        return

    def set_likes(self, likes):
        self.__likes = likes
        return

    def set_allow_download(self, allow_download):
        self.__allow_download = allow_download
        return

    def set_allow_sketch(self, allow_sketch):
        self.__allow_sketch = allow_sketch
        return

    def set_allow_fork(self, allow_fork):
        self.__allow_fork = allow_fork
        return

    def get_id(self):
        return self.__id

    def get_artist(self):
        return self.__artist

    def get_artist_name(self):
        return self.__artist_name

    def get_name(self):
        return self.__name

    def get_created(self):
        return self.__created

    def get_description(self):
        return self.__description

    def get_tags(self):
        return self.__tags

    def get_forks(self):
        return self.__forks

    def get_likes(self):
        return self.__likes

    def get_allow_download(self):
        return self.__allow_download

    def get_allow_sketch(self):
        return self.__allow_sketch

    def get_allow_fork(self):
        return self.__allow_fork

    def get_address(self):
        return self.__address
