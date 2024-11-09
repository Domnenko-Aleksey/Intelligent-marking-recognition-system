import os
import pandas as pd
import faiss


class Faiss:
    def __init__(self, config, model_emb):
        self.config = config
        self.model_emb = model_emb
        self.df = None
        self.faiss_db = faiss.IndexFlatL2(1024)


    def createDb(self):
        path = self.config.train_text_dir
        text_list = []
        for filename in sorted(os.listdir(path)):
            name = filename.split('.')[0]
            text_path = path + '/' + filename
            with open(text_path, 'r', encoding='utf-8') as file:
                text = file.readline().replace('"', '').replace('\n', '')
                text_list.append([name, text])
                emb = self.model_emb.encode(text)
                self.faiss_db.add(emb)

        self.df = pd.DataFrame(text_list, columns=['Name', 'Text'])


    def search(self, emb):
        return self.faiss_db.search(emb, 10)