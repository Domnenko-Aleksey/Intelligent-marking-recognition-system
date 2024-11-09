import sys
import base64
from cryptography import fernet
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from paddleocr import PaddleOCR, draw_ocr
sys.path.append('classes')
import config
from Core import Core
from Yolo import Yolo
from ModelBgeM3 import ModelBgeM3
from Faiss import Faiss
from webapp import webapp



CORE = Core(config)
CORE.yolo = Yolo(config)
CORE.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)
model_emb = ModelBgeM3(config)
CORE.model_emb = model_emb
CORE.faiss = Faiss(config, model_emb)
CORE.faiss.createDb()
print('FAISS DataFrame:', CORE.faiss.df)
print('FAISS DataBase, total:', CORE.faiss.faiss_db.ntotal)



@aiohttp_jinja2.template('main.html')
async def router(request):
    CORE.initial(request)
    CORE.post = await request.post()  # Ждём получение файлов методом POST

    r = webapp.router(CORE)

    """
    # Обработка редиректа
    if r and 'redirect' in r:
        return web.HTTPFound(r['redirect'])
    """   
    # Обработка ajax
    if r and 'ajax' in r:
        return web.HTTPOk(text=r['ajax'])


    return {'content': CORE.content}



app = web.Application(client_max_size=1024**100)



aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([
    web.static('/templates', 'templates'),
    web.static('/files', 'files'),
    web.get('/{url:.*}', router),
    web.post('/{url:.*}', router),
])

if __name__ == '__main__':
    web.run_app(app, port=9999)

