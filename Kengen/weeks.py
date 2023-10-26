from datetime import datetime, timedelta
def get_week_start_end_dates(start_date, end_date):    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_week = start_date - timedelta(days=start_date.weekday())
    week_dates = []
    current_week = start_week
    week_number = 1  
    while current_week <= end_date:
        week_end = current_week + timedelta(days=4)
        week_dates.append((week_number, current_week.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")))
        current_week += timedelta(weeks=1)
        week_number += 1
    return week_dates



