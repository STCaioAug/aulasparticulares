from app import app, db
from sqlalchemy import Column, String, text
from flask import Flask

# Adicionar a coluna 'whatsapp' à tabela 'student'
def add_whatsapp_column():
    with app.app_context():
        # Verificar se a coluna já existe
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('student')]
        
        if 'whatsapp' not in columns:
            # Adicionar a coluna através de SQL nativo usando text()
            db.session.execute(text('ALTER TABLE student ADD COLUMN whatsapp VARCHAR(255);'))
            db.session.commit()
            print("Coluna 'whatsapp' adicionada com sucesso à tabela 'student'.")
        else:
            print("A coluna 'whatsapp' já existe na tabela 'student'.")

if __name__ == "__main__":
    add_whatsapp_column()