import os
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Definição do modelo base para o SQLAlchemy
class Base(DeclarativeBase):
    pass

# Instância do banco
db = SQLAlchemy(model_class=Base)

# Criação da aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tutoring_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tutoring.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o SQLAlchemy com a aplicação
db.init_app(app)

# Processador de contexto para usar o ano atual no template
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Contexto da aplicação (muito importante no Replit)
with app.app_context():
    import models
    from routes import register_routes
    from models import Lesson  # Importa seu modelo aqui corretamente

    db.create_all()
    register_routes(app)

# 🔹 Rota para relatório semanal
@app.route("/weekly-report")
def weekly_report():
    today = datetime.today()
    start = today - timedelta(days=today.weekday())  # Segunda-feira
    end = start + timedelta(days=6)  # Domingo
    return redirect(url_for('reports', start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d')))

# 🔹 Rota para o calendário
@app.route("/calendar")
def calendar():
    lessons = Lesson.query.all()
    events = []

    for lesson in lessons:
        events.append({
            'title': f"{lesson.student.name} - {lesson.subject}",
            'start': f"{lesson.date}T{lesson.start_time}",
            'end': f"{lesson.date}T{lesson.end_time}",
            'url': url_for('edit_lesson', id=lesson.id),  # <-- Isso torna clicável
            'color': '#0d6efd' if lesson.status == 'scheduled' else (
                '#198754' if lesson.status == 'completed' else '#dc3545'
            ),
        })

    return render_template("calendar.html", calendar_events=events)
