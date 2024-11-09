from aiohttp import web
from webapp import ajax
from webapp import mainpage


def router(CORE):
    CORE.debug('PATH: /webapp/webapp.py')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'ajax': ajax.ajax,
    }

    # Если функция не существует - 404
    if (CORE.p[0] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[CORE.p[0]](CORE)