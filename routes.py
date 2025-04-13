from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date, timedelta
from app import db
from models import Student, Guardian, Lesson, Payment

def register_routes(app):
    # Dashboard
    @app.route('/')
    def dashboard():
        # Count statistics for dashboard
        student_count = Student.query.count()
        guardian_count = Guardian.query.count()
        
        # Get upcoming lessons (next 7 days)
        today = date.today()
        week_later = today + timedelta(days=7)
        upcoming_lessons = Lesson.query.filter(
            Lesson.date >= today,
            Lesson.date <= week_later,
            Lesson.status != 'cancelled'
        ).order_by(Lesson.date, Lesson.start_time).all()
        
        # Get total payments for this month
        first_day = date(today.year, today.month, 1)
        if today.month == 12:
            last_day = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(today.year, today.month + 1, 1) - timedelta(days=1)
        
        payments = Payment.query.filter(
            Payment.payment_date >= first_day,
            Payment.payment_date <= last_day
        ).all()
        
        total_payments = sum(payment.amount for payment in payments)
        
        # Dados da agenda semanal
        agenda_semana = {
            "segunda": {
                "fixed": [
                    {"aluno": "Maria", "horario": "15h00–16h30", "local": "Apto 111, Torre 1"},
                    {"aluno": "João", "horario": "16h40–17h40", "local": "Apto 91, Torre 2"}
                ],
                "extra": [
                    {"aluno": "Pietro", "horario": "17h30–19h00", "data": "14/04", "obs": "Química"}
                ]
            },
            "terca": {
                "fixed": [
                    {"aluno": "Lourenço", "horario": "15h30–17h00"},
                    {"aluno": "Gabi", "horario": "17h00–18h00"}
                ],
                "extra": [
                    {"aluno": "Lourenço", "horario": "14h30–16h00", "data": "08/04"},
                    {"aluno": "João Couto", "horario": "16h00–17h00", "data": "08/04"},
                    {"aluno": "Maria", "horario": "18h30–19h30", "data": "08/04"}
                ]
            },
            "quarta": {
                "fixed": [
                    {"aluno": "Lorenzo", "horario": "14h30–15h30", "obs": "1ª aula"},
                    {"aluno": "Otavio (Filho da Gisele)", "horario": "15h30–17h00"},
                    {"aluno": "Pietro", "horario": "17h30–19h00"}
                ],
                "extra": [
                    {"aluno": "Pietro", "horario": "17h30–19h00", "data": "09/04", "obs": "Geometria"},
                    {"aluno": "Pietro", "horario": "17h30–19h00", "data": "23/04", "obs": "Física"}
                ]
            },
            "quinta": {
                "fixed": [
                    {"aluno": "Pedro / Carol", "horario": "15h00–17h00"}
                ],
                "extra": [
                    {"aluno": "Felipe", "horario": "17h30–19h00", "data": "24/04", "obs": "Química"}
                ]
            },
            "sexta": {
                "fixed": [
                    {"aluno": "Lourenço", "horario": "14h30–16h00"},
                    {"aluno": "Gui / Pedrão", "horario": "16h00–17h30"}
                ],
                "extra": []
            }
        }
        
        # Dias da semana em português para mostrar na tabela
        dias_semana = {
            "segunda": "Segunda-feira",
            "terca": "Terça-feira",
            "quarta": "Quarta-feira",
            "quinta": "Quinta-feira",
            "sexta": "Sexta-feira"
        }
        
        return render_template(
            'dashboard.html',
            student_count=student_count,
            guardian_count=guardian_count,
            upcoming_lessons=upcoming_lessons,
            total_payments=total_payments,
            agenda_semana=agenda_semana,
            dias_semana=dias_semana
        )

    # Students routes
    @app.route('/students')
    def list_students():
        students = Student.query.all()
        return render_template('students.html', students=students)

    @app.route('/students/new', methods=['GET', 'POST'])
    def new_student():
        if request.method == 'POST':
            guardian_id = request.form.get('guardian_id')
            
            # Validate guardian exists
            guardian = Guardian.query.get(guardian_id)
            if not guardian:
                flash('Guardian not found. Please select a valid guardian.', 'danger')
                guardians = Guardian.query.all()
                return render_template('forms/student_form.html', guardians=guardians)
            
            student = Student(
                name=request.form.get('name'),
                age=request.form.get('age') or None,
                grade=request.form.get('grade'),
                school=request.form.get('school'),
                whatsapp=request.form.get('whatsapp'),
                guardian_id=guardian_id,
                notes=request.form.get('notes')
            )
            
            db.session.add(student)
            db.session.commit()
            
            flash('Student created successfully!', 'success')
            return redirect(url_for('list_students'))
        
        guardians = Guardian.query.all()
        return render_template('forms/student_form.html', guardians=guardians)

    @app.route('/students/<int:id>/edit', methods=['GET', 'POST'])
    def edit_student(id):
        student = Student.query.get_or_404(id)
        
        if request.method == 'POST':
            guardian_id = request.form.get('guardian_id')
            
            # Validate guardian exists
            guardian = Guardian.query.get(guardian_id)
            if not guardian:
                flash('Guardian not found. Please select a valid guardian.', 'danger')
                guardians = Guardian.query.all()
                return render_template('forms/student_form.html', student=student, guardians=guardians)
            
            student.name = request.form.get('name')
            student.age = request.form.get('age') or None
            student.grade = request.form.get('grade')
            student.school = request.form.get('school')
            student.whatsapp = request.form.get('whatsapp')
            student.guardian_id = guardian_id
            student.notes = request.form.get('notes')
            
            db.session.commit()
            
            flash('Student updated successfully!', 'success')
            return redirect(url_for('list_students'))
        
        guardians = Guardian.query.all()
        return render_template('forms/student_form.html', student=student, guardians=guardians)

    @app.route('/students/<int:id>/delete', methods=['POST'])
    def delete_student(id):
        student = Student.query.get_or_404(id)
        
        # Check if student has lessons before deletion
        if student.lessons:
            flash('Cannot delete student with associated lessons. Delete the lessons first.', 'danger')
            return redirect(url_for('list_students'))
        
        db.session.delete(student)
        db.session.commit()
        
        flash('Student deleted successfully!', 'success')
        return redirect(url_for('list_students'))

    # Guardians routes
    @app.route('/guardians')
    def list_guardians():
        guardians = Guardian.query.all()
        return render_template('guardians.html', guardians=guardians)

    @app.route('/guardians/new', methods=['GET', 'POST'])
    def new_guardian():
        if request.method == 'POST':
            guardian = Guardian(
                name=request.form.get('name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                whatsapp=request.form.get('whatsapp'),
                address=request.form.get('address')
            )
            
            db.session.add(guardian)
            db.session.commit()
            
            flash('Guardian created successfully!', 'success')
            return redirect(url_for('list_guardians'))
        
        return render_template('forms/guardian_form.html')

    @app.route('/guardians/<int:id>/edit', methods=['GET', 'POST'])
    def edit_guardian(id):
        guardian = Guardian.query.get_or_404(id)
        
        if request.method == 'POST':
            guardian.name = request.form.get('name')
            guardian.email = request.form.get('email')
            guardian.phone = request.form.get('phone')
            guardian.whatsapp = request.form.get('whatsapp')
            guardian.address = request.form.get('address')
            
            db.session.commit()
            
            flash('Guardian updated successfully!', 'success')
            return redirect(url_for('list_guardians'))
        
        return render_template('forms/guardian_form.html', guardian=guardian)

    @app.route('/guardians/<int:id>/delete', methods=['POST'])
    def delete_guardian(id):
        guardian = Guardian.query.get_or_404(id)
        
        # Check if guardian has students before deletion
        if guardian.primary_students:
            flash('Cannot delete guardian with associated students. Delete the students first.', 'danger')
            return redirect(url_for('list_guardians'))
        
        db.session.delete(guardian)
        db.session.commit()
        
        flash('Guardian deleted successfully!', 'success')
        return redirect(url_for('list_guardians'))

    # Lessons routes
    @app.route('/lessons')
    def list_lessons():
        # Default to current week
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Allow date range filtering
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_of_week = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_of_week = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        lessons = Lesson.query.filter(
            Lesson.date >= start_of_week,
            Lesson.date <= end_of_week
        ).order_by(Lesson.date, Lesson.start_time).all()
        
        return render_template(
            'lessons.html', 
            lessons=lessons, 
            start_date=start_of_week, 
            end_date=end_of_week
        )

    @app.route('/lessons/new', methods=['GET', 'POST'])
    def new_lesson():
        if request.method == 'POST':
            try:
                student_id = request.form.get('student_id')
                lesson_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
                end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
                
                lesson = Lesson(
                    student_id=student_id,
                    date=lesson_date,
                    start_time=start_time,
                    end_time=end_time,
                    subject=request.form.get('subject'),
                    topic=request.form.get('topic'),
                    status=request.form.get('status', 'scheduled'),
                    notes=request.form.get('notes'),
                    homework=request.form.get('homework'),
                    payment_status=request.form.get('payment_status', 'unpaid'),
                    payment_amount=float(request.form.get('payment_amount') or 0)
                )
                
                db.session.add(lesson)
                db.session.commit()
                
                flash('Lesson created successfully!', 'success')
                return redirect(url_for('list_lessons'))
            except Exception as e:
                flash(f'Error creating lesson: {str(e)}', 'danger')
        
        students = Student.query.all()
        return render_template('forms/lesson_form.html', students=students)

    @app.route('/lessons/<int:id>/edit', methods=['GET', 'POST'])
    def edit_lesson(id):
        lesson = Lesson.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                student_id = request.form.get('student_id')
                lesson_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
                end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
                
                lesson.student_id = student_id
                lesson.date = lesson_date
                lesson.start_time = start_time
                lesson.end_time = end_time
                lesson.subject = request.form.get('subject')
                lesson.topic = request.form.get('topic')
                lesson.status = request.form.get('status')
                lesson.notes = request.form.get('notes')
                lesson.homework = request.form.get('homework')
                lesson.payment_status = request.form.get('payment_status')
                lesson.payment_amount = float(request.form.get('payment_amount') or 0)
                
                db.session.commit()
                
                flash('Lesson updated successfully!', 'success')
                return redirect(url_for('list_lessons'))
            except Exception as e:
                flash(f'Error updating lesson: {str(e)}', 'danger')
        
        students = Student.query.all()
        return render_template('forms/lesson_form.html', lesson=lesson, students=students)

    @app.route('/lessons/<int:id>/delete', methods=['POST'])
    def delete_lesson(id):
        lesson = Lesson.query.get_or_404(id)
        
        db.session.delete(lesson)
        db.session.commit()
        
        flash('Lesson deleted successfully!', 'success')
        return redirect(url_for('list_lessons'))

    # Reports
    @app.route('/reports')
    def reports():
        # Get date range for filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        today = date.today()
        if not start_date_str:
            # Default to first day of current month
            start_date = date(today.year, today.month, 1)
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            
        if not end_date_str:
            # Default to last day of current month
            if today.month == 12:
                end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
        else:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Get all lessons in the date range
        lessons = Lesson.query.filter(
            Lesson.date >= start_date,
            Lesson.date <= end_date
        ).order_by(Lesson.date).all()
        
        # Get all payments in the date range
        payments = Payment.query.filter(
            Payment.payment_date >= start_date,
            Payment.payment_date <= end_date
        ).order_by(Payment.payment_date).all()
        
        # Calculate statistics
        total_lessons = len(lessons)
        total_lesson_hours = sum((lesson.end_time.hour - lesson.start_time.hour) + 
                              (lesson.end_time.minute - lesson.start_time.minute) / 60 
                              for lesson in lessons)
        total_earnings = sum(lesson.payment_amount for lesson in lessons)
        total_payments = sum(payment.amount for payment in payments)
        
        return render_template(
            'reports.html',
            start_date=start_date,
            end_date=end_date,
            lessons=lessons,
            payments=payments,
            total_lessons=total_lessons,
            total_lesson_hours=total_lesson_hours,
            total_earnings=total_earnings,
            total_payments=total_payments
        )

    # API Endpoints
    @app.route('/api/students')
    def api_students():
        students = Student.query.all()
        result = [{
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'grade': student.grade,
            'school': student.school
        } for student in students]
        return jsonify(result)
