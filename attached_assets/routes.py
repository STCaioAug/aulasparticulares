from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date, timedelta
from app import db
from models import Student, Guardian, Lesson, Payment
from utils.sms import send_sms
from utils.whatsapp import get_whatsapp_link, format_phone_number, get_whatsapp_api_link
from utils.reports import get_daily_lessons_report
import logging

# Configure logging
logger = logging.getLogger(__name__)

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
                whatsapp=request.form.get('whatsapp'),  # Added WhatsApp field
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
            guardian.whatsapp = request.form.get('whatsapp')  # Added WhatsApp field
            guardian.address = request.form.get('address')
            
            db.session.commit()
            
            flash('Guardian updated successfully!', 'success')
            return redirect(url_for('list_guardians'))
        
        return render_template('forms/guardian_form.html', guardian=guardian)

    @app.route('/guardians/<int:id>/delete', methods=['POST'])
    def delete_guardian(id):
        guardian = Guardian.query.get_or_404(id)
        
        # Check if guardian has students before deletion
        if guardian.students:
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
                logger.error(f"Error creating lesson: {str(e)}")
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
                logger.error(f"Error updating lesson: {str(e)}")
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
        completed_lessons = sum(1 for lesson in lessons if lesson.status == 'completed')
        cancelled_lessons = sum(1 for lesson in lessons if lesson.status == 'cancelled')
        
        # Calculate total earnings
        total_earnings = sum(lesson.payment_amount for lesson in lessons)
        
        # Calculate earnings by guardian
        earnings_by_guardian = {}
        for lesson in lessons:
            guardian = lesson.student.guardian
            if guardian.id not in earnings_by_guardian:
                earnings_by_guardian[guardian.id] = {
                    'guardian_name': guardian.name,
                    'amount': 0,
                    'lessons': 0
                }
            earnings_by_guardian[guardian.id]['amount'] += lesson.payment_amount
            earnings_by_guardian[guardian.id]['lessons'] += 1
            
        return render_template(
            'reports.html',
            start_date=start_date,
            end_date=end_date,
            lessons=lessons,
            payments=payments,
            total_lessons=total_lessons,
            completed_lessons=completed_lessons,
            cancelled_lessons=cancelled_lessons,
            total_earnings=total_earnings,
            earnings_by_guardian=earnings_by_guardian.values()
        )
        
    # API endpoints for AJAX calls
    @app.route('/api/students')
    def api_students():
        students = Student.query.all()
        return jsonify([
            {
                'id': student.id,
                'name': student.name,
                'guardian_name': student.guardian.name
            }
            for student in students
        ])
        
        
    # SMS Notification routes
    @app.route('/notifications/sms/lesson/<int:lesson_id>', methods=['POST'])
    def send_lesson_notification(lesson_id):
        try:
            lesson = Lesson.query.get_or_404(lesson_id)
            student = lesson.student
            guardian = student.guardian
            
            # Check if guardian has a phone number
            if not guardian.phone:
                flash('Guardian does not have a phone number for SMS notifications.', 'danger')
                return redirect(url_for('list_lessons'))
            
            # Format date and time for message
            lesson_date = lesson.date.strftime('%A, %B %d, %Y')
            start_time = lesson.start_time.strftime('%I:%M %p')
            end_time = lesson.end_time.strftime('%I:%M %p')
            
            # Create message
            message = f"Hello {guardian.name}, this is a reminder that {student.name}'s {lesson.subject} lesson is scheduled for {lesson_date} from {start_time} to {end_time}."
            
            if lesson.topic:
                message += f" The topic will be: {lesson.topic}."
                
            # Send SMS
            result = send_sms(guardian.phone, message)
            
            if result.get('success'):
                flash(f'SMS notification sent to {guardian.name} successfully!', 'success')
                logger.info(f'SMS notification sent for lesson {lesson_id} to {guardian.name}')
            else:
                error = result.get('error', 'Unknown error')
                flash(f'Failed to send SMS: {error}', 'danger')
                logger.error(f'SMS notification failed for lesson {lesson_id}: {error}')
                
            return redirect(url_for('list_lessons'))
            
        except Exception as e:
            logger.error(f"Error sending SMS notification: {str(e)}")
            flash(f'Error sending notification: {str(e)}', 'danger')
            return redirect(url_for('list_lessons'))
    
    @app.route('/notifications/daily-report', methods=['GET', 'POST'])
    def send_daily_report():
        daily_report = None
        report_date = None
        whatsapp_link = None
        
        if request.method == 'POST':
            try:
                # Obter número de telefone do formulário
                phone_number = request.form.get('phone_number')
                date_str = request.form.get('report_date')
                
                if not phone_number:
                    flash('Por favor, informe um número de WhatsApp válido.', 'danger')
                    return redirect(url_for('send_daily_report'))
                
                # Obter relatório diário
                if date_str:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                else:
                    target_date = date.today()
                
                report = get_daily_lessons_report(target_date)
                
                if not report['success']:
                    flash(f'Erro ao gerar relatório: {report.get("error")}', 'danger')
                    return redirect(url_for('send_daily_report'))
                
                # Gerar link para WhatsApp
                whatsapp_link = get_whatsapp_link(phone_number, report['report_text'])
                
                # Recarregar o relatório para exibição
                daily_report = report['report_text']
                report_date = date_str
                
                flash('Link para WhatsApp gerado com sucesso! Clique no botão para abrir.', 'success')
                
            except Exception as e:
                logger.error(f"Erro ao gerar link para WhatsApp: {str(e)}")
                flash(f'Erro ao processar solicitação: {str(e)}', 'danger')
        else:
            # GET request - mostrar formulário ou relatório para visualização
            date_str = request.args.get('date')
            
            if date_str:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    report = get_daily_lessons_report(target_date)
                    
                    if report['success']:
                        daily_report = report['report_text']
                        report_date = date_str
                    else:
                        flash(f'Erro ao gerar relatório: {report.get("error")}', 'danger')
                except Exception as e:
                    flash(f'Erro ao processar data: {str(e)}', 'danger')
            else:
                # Sem data específica, apenas mostrar o formulário
                pass
        
        # Formatar data atual para o valor padrão do formulário
        today_date = date.today().strftime('%Y-%m-%d')
        
        return render_template(
            'notifications/daily_report.html',
            daily_report=daily_report,
            report_date=report_date,
            today_date=today_date,
            whatsapp_link=whatsapp_link
        )
        
    @app.route('/notifications/auto-daily-report/<phone_number>', methods=['GET'])
    def auto_daily_report(phone_number):
        """
        Enviar automaticamente o relatório diário para um número específico
        """
        try:
            # Validar o número de telefone
            if not phone_number:
                return jsonify({
                    'success': False,
                    'error': 'Número de telefone não fornecido'
                }), 400
                
            # Limpar o número de telefone (remover caracteres não numéricos)
            from utils.whatsapp import format_phone_number
            formatted_phone = format_phone_number(phone_number)
            
            # Obter relatório para o dia atual
            target_date = date.today()
            report = get_daily_lessons_report(target_date)
            
            if not report['success']:
                return jsonify({
                    'success': False,
                    'error': f'Erro ao gerar relatório: {report.get("error")}'
                }), 500
            
            # Gerar link para WhatsApp
            whatsapp_link = get_whatsapp_link(formatted_phone, report['report_text'])
            
            # Verificar se é uma chamada de API (aceita JSON) ou interface de usuário
            if request.headers.get('Accept') == 'application/json':
                # Retorno para API
                return jsonify({
                    'success': True,
                    'message': 'Relatório diário gerado com sucesso',
                    'report_date': target_date.strftime('%d/%m/%Y'),
                    'whatsapp_link': whatsapp_link
                })
            else:
                # Retorno para navegador - redireciona diretamente para o WhatsApp
                flash(f'Relatório diário para {target_date.strftime("%d/%m/%Y")} enviado com sucesso!', 'success')
                return redirect(whatsapp_link)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório automático: {str(e)}")
            flash(f'Erro ao processar solicitação: {str(e)}', 'danger')
            return redirect(url_for('dashboard'))
    
    @app.route('/notifications/bulk', methods=['GET', 'POST']) # Atualizado para remover 'sms' da URL
    def send_bulk_notifications():
        result = None
        today_date = date.today().strftime('%Y-%m-%d')
        
        if request.method == 'POST':
            try:
                # Get message content and lesson date filter
                message_template = request.form.get('message')
                date_str = request.form.get('lesson_date')
                use_whatsapp = request.form.get('use_whatsapp') == 'on'
                
                if not message_template:
                    flash('É necessário fornecer o conteúdo da mensagem.', 'danger')
                    return redirect(url_for('send_bulk_notifications'))
                
                notifications_sent = 0
                errors = 0
                whatsapp_links = []
                
                # Get lessons for the selected date if provided
                if date_str:
                    lesson_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    lessons = Lesson.query.filter(
                        Lesson.date == lesson_date,
                        Lesson.status != 'cancelled'
                    ).all()
                    
                    # Process each lesson
                    for lesson in lessons:
                        student = lesson.student
                        guardian = student.guardian
                        
                        # Escolhe o número adequado (WhatsApp ou telefone comum)
                        contact_number = None
                        if use_whatsapp and guardian.whatsapp:
                            contact_number = guardian.whatsapp
                        elif not use_whatsapp and guardian.phone:
                            contact_number = guardian.phone
                        else:
                            # Tenta usar o outro número como fallback
                            contact_number = guardian.phone or guardian.whatsapp
                        
                        # Pula se não houver número de contato
                        if not contact_number:
                            errors += 1
                            continue
                        
                        # Personaliza a mensagem com detalhes do aluno e da aula
                        message = message_template
                        message = message.replace('{student_name}', student.name)
                        message = message.replace('{guardian_name}', guardian.name)
                        message = message.replace('{subject}', lesson.subject or '')
                        message = message.replace('{time}', lesson.start_time.strftime('%H:%M'))
                        if '{topic}' in message and lesson.topic:
                            message = message.replace('{topic}', lesson.topic)
                        else:
                            message = message.replace('{topic}', '')
                        
                        if use_whatsapp:
                            # Gera link para WhatsApp
                            whatsapp_url = get_whatsapp_link(contact_number, message)
                            whatsapp_links.append({
                                'url': whatsapp_url,
                                'student_name': student.name,
                                'guardian_name': guardian.name,
                                'subject': lesson.subject,
                                'time': lesson.start_time.strftime('%H:%M')
                            })
                            notifications_sent += 1
                        else:
                            # Envia SMS
                            result = send_sms(contact_number, message)
                            if result.get('success'):
                                notifications_sent += 1
                            else:
                                errors += 1
                    
                    if use_whatsapp:
                        # Para WhatsApp, mostramos os links
                        result = {
                            'date_formatted': lesson_date.strftime('%d/%m/%Y'),
                            'total_lessons': len(lessons),
                            'processed': notifications_sent,
                            'links': whatsapp_links
                        }
                    else:
                        # Para SMS, mostramos mensagem de sucesso/erro
                        if notifications_sent > 0:
                            flash(f'Foram enviadas {notifications_sent} notificações por SMS com sucesso.', 'success')
                        if errors > 0:
                            flash(f'Falha ao enviar {errors} notificações por SMS.', 'warning')
                        return redirect(url_for('list_lessons'))
                else:
                    flash('Por favor, selecione uma data para as aulas.', 'danger')
                    
            except Exception as e:
                logger.error(f"Erro no envio de notificações em massa: {str(e)}")
                flash(f'Erro ao enviar notificações: {str(e)}', 'danger')
                
        # GET request - mostra o formulário
        return render_template('notifications/bulk_sms.html', result=result, today_date=today_date)
