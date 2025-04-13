from datetime import datetime, date, timedelta
from models import Lesson
import logging

logger = logging.getLogger(__name__)

def get_daily_lessons_report(target_date=None):
    """
    Gera um relatório de texto com todas as aulas de um dia específico
    
    Args:
        target_date (date, optional): A data para gerar o relatório. Padrão é hoje.
        
    Returns:
        dict: Dicionário com texto do relatório e estatísticas
    """
    try:
        # Use a data especificada ou a data atual
        if target_date is None:
            target_date = date.today()
        elif isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        # Busca todas as aulas do dia
        lessons = Lesson.query.filter(
            Lesson.date == target_date
        ).order_by(Lesson.start_time).all()
        
        # Estatísticas básicas
        total_lessons = len(lessons)
        completed_lessons = sum(1 for lesson in lessons if lesson.status == 'completed')
        scheduled_lessons = sum(1 for lesson in lessons if lesson.status == 'scheduled')
        cancelled_lessons = sum(1 for lesson in lessons if lesson.status == 'cancelled')
        
        # Cabeçalho do relatório
        weekday_names = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        weekday_name = weekday_names[target_date.weekday()]
        
        formatted_date = target_date.strftime('%d/%m/%Y')
        report_text = f"📅 AULAS DO DIA: {weekday_name}, {formatted_date}\n\n"
        
        # Se não houver aulas
        if total_lessons == 0:
            report_text += "Não há aulas agendadas para hoje.\n"
        else:
            # Lista todas as aulas
            for i, lesson in enumerate(lessons, 1):
                status_emoji = "✅" if lesson.status == 'completed' else "⏳" if lesson.status == 'scheduled' else "❌"
                
                start_time = lesson.start_time.strftime('%H:%M')
                end_time = lesson.end_time.strftime('%H:%M')
                
                report_text += f"{i}. {status_emoji} {start_time}-{end_time}: {lesson.student.name}\n"
                report_text += f"   📚 {lesson.subject}"
                
                if lesson.topic:
                    report_text += f" - {lesson.topic}"
                    
                report_text += "\n"
                
                # Adiciona notas se houver
                if lesson.notes:
                    report_text += f"   📝 {lesson.notes}\n"
                    
                # Adiciona linha em branco entre aulas
                if i < total_lessons:
                    report_text += "\n"
            
            # Resumo
            report_text += f"\n📊 RESUMO: {total_lessons} aulas total"
            if scheduled_lessons > 0:
                report_text += f", {scheduled_lessons} agendada(s)"
            if completed_lessons > 0:
                report_text += f", {completed_lessons} concluída(s)"
            if cancelled_lessons > 0:
                report_text += f", {cancelled_lessons} cancelada(s)"
        
        return {
            "report_text": report_text,
            "statistics": {
                "total": total_lessons,
                "completed": completed_lessons,
                "scheduled": scheduled_lessons,
                "cancelled": cancelled_lessons
            },
            "date": target_date,
            "success": True
        }
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório diário: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }