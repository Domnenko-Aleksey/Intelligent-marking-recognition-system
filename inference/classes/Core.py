class Core:
    def __init__(self, config):
        self.config = config

        # Models
        self.model_emb = False
        self.model_faiss = False


    # Инициализация при открытии страниы
    def initial(self, request):
        self.file = False  # Полученый файл
        self.post = False  # объект post
        self.tag_title = ''  # Тег title
        self.tag_description = ''  # Метатег descripton
        self.content = ''  # Основное содержимое
        self.request = request  #  # request aiohttp
        self.p = request.path[1:].split('/')  # Список элементов пути
        i = len(self.p)
        while i < 7:
            self.p.append('')
            i += 1


    def debug(self, text):
        if (self.config.debug):
            print(text)
        

