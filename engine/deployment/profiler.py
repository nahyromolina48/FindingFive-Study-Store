from werkzeug.middleware.profiler import ProfilerMiddleware
from main import app

app.wsgi_app= ProfilerMiddleware(app.wsgi_app,restrictions=[15])
app.run(host='0.0.0.0', port=12100, debug=True)
