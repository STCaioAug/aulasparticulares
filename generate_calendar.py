import os
import sys
from datetime import datetime, timedelta, date, time
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from models import Lesson, Student

# Definir a data de início para 07/04/2025 (hoje) e a data final como 15/12/2025
start_date = date(2025, 4, 7)
end_date = date(2025, 12, 15)

# IDs dos alunos (de acordo com a consulta ao banco)
MARIA_ID = 3
JOAO_ID = 4
FELIPE_ID = 1

# Configuração das aulas fixas
# Formato: (aluno_id, dia_da_semana (0=Segunda, 6=Domingo), hora_inicio, hora_fim, matéria)
FIXED_CLASSES = [
    # Maria - aulas às segundas e quartas às 14:00
    (MARIA_ID, 0, time(14, 0), time(15, 30), "Matemática"),  # Segunda
    (MARIA_ID, 2, time(14, 0), time(15, 30), "Física"),      # Quarta
    
    # João - aulas às segundas e sextas às 16:00
    (JOAO_ID, 0, time(16, 0), time(17, 30), "Química"),      # Segunda
    (JOAO_ID, 4, time(16, 0), time(17, 30), "Biologia"),     # Sexta
]

# Aula extra para o Felipe em 07/04/2025
EXTRA_CLASSES = [
    (FELIPE_ID, date(2025, 4, 7), time(18, 0), time(19, 30), "Reforço de Matemática")
]

def create_app():
    # Importar app do módulo principal
    from app import app
    return app

def generate_lessons():
    app = create_app()
    with app.app_context():
        print("Gerando calendário de aulas...")
        
        # Limpar aulas existentes (opcional, comentado por segurança)
        # db.session.query(Lesson).delete()
        # db.session.commit()
        
        # Gerar aulas fixas
        current_date = start_date
        lessons_count = 0
        
        while current_date <= end_date:
            # Verificar dia da semana (0 = Segunda, 6 = Domingo)
            weekday = current_date.weekday()
            
            # Procurar por aulas fixas para este dia da semana
            for student_id, day, start_time, end_time, subject in FIXED_CLASSES:
                if day == weekday:
                    # Criar aula
                    lesson = Lesson(
                        student_id=student_id,
                        date=current_date,
                        start_time=start_time,
                        end_time=end_time,
                        subject=subject,
                        status="scheduled"
                    )
                    db.session.add(lesson)
                    lessons_count += 1
            
            # Avançar para o próximo dia
            current_date += timedelta(days=1)
        
        # Adicionar aulas extras
        for student_id, extra_date, start_time, end_time, subject in EXTRA_CLASSES:
            if start_date <= extra_date <= end_date:
                lesson = Lesson(
                    student_id=student_id,
                    date=extra_date,
                    start_time=start_time,
                    end_time=end_time,
                    subject=subject,
                    status="scheduled",
                    topic="Aula Extra"
                )
                db.session.add(lesson)
                lessons_count += 1
        
        # Salvar no banco de dados
        db.session.commit()
        print(f"Calendário gerado com sucesso! {lessons_count} aulas cadastradas.")

if __name__ == "__main__":
    generate_lessons()