from app import app
from utils.time_analysis import get_weekly_free_slots, get_worked_hours_analysis
from datetime import datetime, date

print('Debugging time_analysis.py')

with app.app_context():
    start_date = date.today()
    try:
        free_slots = get_weekly_free_slots(start_date)
        print("Free slots data OK")
    except Exception as e:
        print(f"Error in get_weekly_free_slots: {str(e)}")
    
    try:
        worked_hours = get_worked_hours_analysis(start_date)
        print("Worked hours data OK")
    except Exception as e:
        print(f"Error in get_worked_hours_analysis: {str(e)}")
