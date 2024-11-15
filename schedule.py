import openpyxl

def load_schedule():
    workbook = openpyxl.load_workbook("schedule_1.xlsx")
    sheet = workbook.active
    schedule = {}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        class_name = row[0]
        day = row[1]
        if class_name not in schedule:
            schedule[class_name] = {}
        schedule[class_name][day] = []

        for item in range(2, len(row), 4):
            lesson = row[item]
            time = row[item+1]
            room = row[item+2]
            teacher = row[item+3]

            if lesson and time and room and teacher:
                schedule[class_name][day].append({
                    'lesson':lesson,
                    'time':time,
                    'room':room,
                    'teacher':teacher
                })
    return schedule

schedule_data = load_schedule()
