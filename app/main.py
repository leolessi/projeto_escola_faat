from flask import Flask
from flasgger import Swagger
from crudAlunos import alunos_bp
from crudProfessores import professores_bp
from crudAtividades import atividades_bp
from crudTurmas import turmas_bp
from crudPagamentos import pagamentos_bp
from crudPresencas import presencas_bp
from crudAtividadeAluno import atividade_aluno_bp
from crudUsuarios import usuarios_bp

import logging

logging.basicConfig(
    filename="escola_infantil.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(professores_bp, url_prefix="/api")
app.register_blueprint(atividades_bp, url_prefix="/api")
app.register_blueprint(turmas_bp, url_prefix="/api")
app.register_blueprint(alunos_bp, url_prefix="/api")
app.register_blueprint(pagamentos_bp, url_prefix="/api")
app.register_blueprint(presencas_bp, url_prefix="/api")
app.register_blueprint(atividade_aluno_bp, url_prefix="/api")
app.register_blueprint(usuarios_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
