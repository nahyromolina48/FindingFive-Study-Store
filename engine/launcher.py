import gunicorn.app.wsgiapp as wsgi
from main import app

if __name__ == '__main__':
    # runs on localhosts
    wsgi.run()
