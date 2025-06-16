from flask import Flask
from app.crudAlunos import alunos_bp
from app.crudProfessores import professores_bp
from app.crudAtividades import atividades_bp
from app.crudTurmas import turmas_bp

app = Flask(__name__)

# Registra os Blueprints
app.register_blueprint(alunos_bp, url_prefix="/api")
app.register_blueprint(professores_bp, url_prefix="/api")
app.register_blueprint(atividades_bp, url_prefix="/api")
app.register_blueprint(turmas_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
