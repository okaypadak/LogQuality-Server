from flask import Flask
from controller.GitRepoController import get_route, post_route
from controller.ProjeAnalysisController import upload

app = Flask(__name__)

# GET metodu için route
app.register_blueprint(get_route)

# POST metodu için route
app.register_blueprint(post_route, url_prefix='/api')

app.register_blueprint(upload)


if __name__ == "__main__":
    app.run(debug=True)
