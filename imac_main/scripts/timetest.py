from datetime import datetime, timedelta



def isvalid(date):
    date_time_from = datetime.strptime(date, '%Y-%m-%d').date()
    after_2_days = datetime.today().date() + timedelta(days=2)
    if date_time_from >= after_2_days:
        return True
    else:
        return False
    
def is_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2

    # Convert time strings to datetime objects
    start1 = datetime.strptime(start1, "%H:%M")
    end1 = datetime.strptime(end1, "%H:%M")
    start2 = datetime.strptime(start2, "%H:%M")
    end2 = datetime.strptime(end2, "%H:%M")

    # Check for overlap
    if start1 < end2 and start2 < end1:
        return True
    else:
        return False
    

def check_date_time_range(date_from, date_till, db_date):
    # Convert input date and time ranges to datetime objects
    start_date = datetime.strptime(date_from, '%Y-%m-%d')
    end_date = datetime.strptime(date_till, '%Y-%m-%d')
    

    # Convert database date and time range to datetime objects
    db_date_obj = datetime.strptime(db_date, '%Y-%m-%d')

    # Check if the database date falls within the input date range
    if start_date <= db_date_obj <= end_date:
        # Check if the database time range overlaps with the input time range
        return True

    return False
    

def check(date, timefrom, timetill):
    date_time_from = datetime.strptime(date + ' ' + timefrom, '%Y-%m-%d %H:%M')
    date_time_till = datetime.strptime(date + ' ' + timetill, '%Y-%m-%d %H:%M')
    after_2_days = datetime.now() + timedelta(days=2)
    print(date_time_from - after_2_days)


if __name__ == '__main__':
    print(isvalid('2023-09-25'))