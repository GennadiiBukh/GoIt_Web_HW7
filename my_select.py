from sqlalchemy import create_engine, desc, func, and_, select
from sqlalchemy.orm import sessionmaker, aliased
from models import Student, Group, Teacher, Subject, Grade

#1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    top_students = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .outerjoin(Grade, Student.id == Grade.student_id)\
        .group_by(Student.id)\
        .order_by(desc('average_grade'))\
        .limit(5)\
        .all()
    return top_students

#2.Знайти студента із найвищим середнім балом з певного предмета.
def select_2():    
    subject_id = '1' #Зафіксована назва предмету  
    result = session.query(Student.name, Subject.name, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .join(Grade, Student.id == Grade.student_id, isouter=True)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .filter(Subject.id == subject_id)\
        .group_by(Student.id)\
        .order_by(desc('average_grade'))\
        .limit(1)\
        .all()
    return result

#3.Знайти середній бал у групах з певного предмета.
def select_3():    
    subject_id = '3' #Зафіксована назва предмету  
    result = session.query(Group.name, Subject.name, func.round(func.avg(Grade.grade), 2))\
        .join(Student, Group.id == Student.group_id)\
        .join(Grade, Student.id == Grade.student_id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .filter(Subject.id == subject_id)\
        .group_by(Group.name, Subject.name)\
        .all()  
    return result

#4.Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2))
    return result
    
#5.Знайти які курси читає певний викладач.
def select_5():   
    teacher_id = 3 #'Певний викладач'
    result = session.query(Subject.name.label('subject'), Teacher.name.label('teacher'))\
        .join(Teacher, Subject.teacher_id == Teacher.id)\
        .filter(Teacher.id == teacher_id)\
        .all()    
    return result
    
#6.Знайти список студентів у певній групі.
"""
SELECT students.id AS id, students.name AS students_name, groups.name AS groupe
FROM students
JOIN groups ON students.group_id = groups.id 
WHERE group_id = 2 -- Вибрана група
"""
def select_6():
    groupe_id = 2
    result = session.query(Student.id, Student.name, Group.name)\
    .join(Group, Student.group_id == Group.id)\
    .filter(Group.id == groupe_id)\
    .all()
    return result

#7.Знайти оцінки студентів у окремій групі з певного предмета.
"""
SELECT students.name AS student_name, groups.name, subjects.name AS subject, grades.grade
FROM students
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
JOIN grades ON students.id = grades.student_id
WHERE groups.id = 3 --'Певна група'
AND subjects.id = 2 --'Певний предмет'
"""
def select_7():
    group_id = 3
    subject_id = 2  
    result = session.query(Student.name, Group.name, Subject.name, Grade.grade)\
        .join(Group, Student.group_id == Group.id)\
        .join(Grade, and_(Grade.student_id == Student.id, Grade.subject_id == subject_id))\
        .join(Subject, Grade.subject_id == Subject.id)\
        .filter(Group.id == group_id)\
        .all()       
    return result

#8.Знайти середній бал, який ставить певний викладач зі своїх предметів.
"""
SELECT teachers.name AS teacher, ROUND(AVG(grades.grade)) AS average_grade
FROM grades
JOIN teachers ON subjects.teacher_id = teachers.id
JOIN subjects ON grades.subject_id = subjects.id 
WHERE teachers.id = 1 --'Певний викладач_id'
"""
def select_8():
    teacher_id = 1 #'Певний викладач'
    result = session.query(Teacher.name.label('teacher'), func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .join(Teacher, Subject.teacher_id == Teacher.id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .filter(Teacher.id == teacher_id)\
        .all()    
    return result
    
#9.Знайти список курсів, які відвідує студент.
"""
SELECT students.name AS student_name, subjects.name AS subject
FROM subjects
JOIN students
JOIN grades ON subjects.id = subject_id AND students.id = student_id
WHERE students.id = 17 --'Певний студент'
"""
def select_9():
    student_id = 17 #'Певний студент'   
    student = aliased(Student)
    subject = aliased(Subject)
    result = session.query(student.name, subject.name)\
        .select_from(student)\
        .join(Grade, and_(subject.id == Grade.subject_id, student.id == Grade.student_id))\
        .filter(student.id == student_id)\
        .all()
    return result
    
#10.Список курсів, які певному студенту читає певний викладач.
"""
SELECT students.name AS student_name, subjects.name AS subject, teachers.name AS teacher
FROM subjects
JOIN students
JOIN teachers ON subjects.teacher_id = teachers.id
JOIN grades ON students.id = student_id AND subjects.id = subject_id 
WHERE students.id = 10 AND teachers.id = 2 --'Певний студент' та 'Певний викладач'
"""
def select_10():
    student_id = 10 #'Певний студент'
    teacher_id = 2 #'Певний викладач'
    result = session.query(Student.name, Subject.name, Teacher.name)\
        .select_from(Grade)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .join(Teacher, Subject.teacher_id == Teacher.id)\
        .join(Student, Grade.student_id == Student.id)\
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
        .all()
    return result

#11.Середній бал, який певний викладач ставить певному студентові.
"""
SELECT teachers.name AS teacher, students.name AS student_name, ROUND(AVG(grades.grade)) AS average_grade
FROM students
JOIN subjects ON grades.subject_id = subjects.id
JOIN teachers ON subjects.teacher_id = teachers.id
JOIN grades ON students.id = student_id
WHERE students.id = 11 AND teachers.id = 3 --'Певний студент' та 'Певний викладач'
GROUP BY teachers.name, students.name
"""
def select_11():
    student_id = 11 #'Певний студент'
    teacher_id = 3 #'Певний викладач'
    result = session.query(Teacher.name, Student.name, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
    .select_from(Grade)\
    .join(Subject, Grade.subject_id == Subject.id)\
    .join(Teacher, Subject.teacher_id == Teacher.id)\
    .join(Student, Grade.student_id == Student.id)\
    .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
    .all()
    return result

#12.Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    group_id = 2
    subject_id = 8

    subquery = (select(func.max(Grade.date_received)).join(Student).filter(and_(
        Grade.subject_id == subject_id, Student.group_id == group_id
    ))).scalar_subquery()

    result = session.query(Student.id, Student.name, Grade.grade, Grade.date_received) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subject_id == subject_id, Student.group_id == group_id, Grade.date_received == subquery)).all()
    
    formatted_result = [(student_id, student_name, grade, date.strftime('%Y-%m-%d %H:%M'))\
                         for student_id, student_name, grade, date in result]

    return formatted_result 
    
  

def choos_query():
    while True:
        print('Запити до бази даних:\n',
        '1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.\n',
        '2.Знайти студента із найвищим середнім балом з певного предмета.\n',
        '3.Знайти середній бал у групах з певного предмета.\n',
        '4.Знайти середній бал на потоці (по всій таблиці оцінок).\n',
        '5.Знайти які курси читає певний викладач.\n',
        '6.Знайти список студентів у певній групі.\n',
        '7.Знайти оцінки студентів у окремій групі з певного предмета.\n',
        '8.Знайти середній бал, який ставить певний викладач зі своїх предметів.\n',
        '9.Знайти список курсів, які відвідує студент.\n',
        '10.Список курсів, які певному студенту читає певний викладач.\n',
        '11.Середній бал, який певний викладач ставить певному студентові.\n',
        '12.Оцінки студентів у певній групі з певного предмета на останньому занятті.\n')
        
        num = input('Введіть номер запиту або "Enter" для виходу >> ')
        if not num:
            break
        if num in queries:
            result = queries[num]()
            print(f"Результат запиту {num}:")       
            for row in result:
                print(row)
        else:
            print(f"Запит №{num} не знайдений.")               
                    
        input('\nВведіть "Enter" для продовження')


if __name__ == "__main__":

    queries = {
    '1': select_1,
    '2': select_2,
    '3': select_3,
    '4': select_4,
    '5': select_5,
    '6': select_6,
    '7': select_7,
    '8': select_8,
    '9': select_9,
    '10': select_10,
    '11': select_11,
    '12': select_12    
}
    try:
        # Підключення до бази даних
        engine = create_engine('sqlite:///university.db')

        # Створення сесії
        Session = sessionmaker(bind=engine)
        session = Session()

        choos_query()

    except Exception as e:
        # Обробка помилки (вивід, логування тощо)
        print(f"Помилка: {str(e)}")

    finally:
        # Закриття сесії навіть у випадку помилки
        if session:
            session.close()