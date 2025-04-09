from app import db
from datetime import datetime


# Tabela de associação entre alunos e responsáveis
student_guardian = db.Table('student_guardian',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('guardian_id', db.Integer, db.ForeignKey('guardian.id'), primary_key=True)
)


class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(255))  # Campo para armazenar número do WhatsApp
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com alunos (muitos para muitos)
    students = db.relationship('Student', 
                             secondary=student_guardian,
                             lazy='subquery',
                             backref=db.backref('guardians', lazy=True))
    
    def __repr__(self):
        return f'<Guardian {self.name}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(20))
    school = db.Column(db.String(100))
    # Removido o guardian_id pois agora usamos relacionamento muitos-para-muitos
    whatsapp = db.Column(db.String(255))  # Campo para armazenar número do WhatsApp
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Manter o relacionamento principal para compatibilidade com o código existente
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'), nullable=True)
    guardian = db.relationship('Guardian', 
                              foreign_keys=[guardian_id],
                              backref=db.backref('primary_students', lazy=True))
    
    # Relationship with lessons
    lessons = db.relationship('Lesson', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name}>'


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    homework = db.Column(db.Text)
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid
    payment_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lesson {self.subject} - {self.date}>'


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with guardian
    guardian = db.relationship('Guardian', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.amount} - {self.payment_date}>'
