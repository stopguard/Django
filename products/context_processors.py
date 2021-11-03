from datetime import datetime


def today(request):
    return {'today': datetime.now(), }
