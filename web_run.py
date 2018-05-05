from anirec.views import app
# from flask_debugtoolbar import DebugToolbarExtension

# toolbar = DebugToolbarExtension(app)

if __name__ == "__main__":
    app.run("0.0.0.0",port=4003)