from faker import Faker
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

fake = Faker('uk_UA')

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Функція для створення випадкового студента
def create_student():
    student = Student(
        name=fake.name(),
        group=session.query(Group).order_by(func.random()).first()
    )
    return student

# Функція для створення випадкового викладача
def create_teacher():
    teacher = Teacher(
        name=fake.name()
    )
    return teacher

# Реальні назви предметів
real_subjects = [
    "Математика",
    "Фізика",
    "Інформатика",
    "Історія",
    "Біологія",
    "Хімія",
    "Географія",
    "Економіка",
    "Література",
    "Музика",
    "Фізкультура",
]

# Функція для створення випадкового предмету з вказівкою викладача
def create_subject(teacher, real_subjects):
    subject_name = fake.random_element(elements=real_subjects)
    real_subjects.remove(subject_name)  # Видаляємо вже вибраний предмет
    subject = Subject(
        name=subject_name,
        teacher=teacher
    )
    return subject

# Функція для створення випадкової оцінки
def create_grade(student, subject):
    grade = Grade(
        student=student,
        subject=subject,
        grade=fake.random_int(min=10, max=100)  
    )
    return grade

# Створення 3 груп
for i in range(3):
    group = Group(name=f"Група {i + 1}")
    session.add(group)

# Створення 5 викладачів
for _ in range(5):
    teacher = create_teacher()
    session.add(teacher)

# Створення 11 предметів з випадковими викладачами
for _ in range(11):
    teacher = session.query(Teacher).order_by(func.random()).first()       
    subject = create_subject(teacher, real_subjects)
    session.add(subject)

# Створення 30 студентів
for _ in range(30):
    student = create_student()
    session.add(student)

# Створення випадкових оцінок для студентів та предметів
for student in session.query(Student).all():
    for subject in session.query(Subject).all():
        grade = create_grade(student, subject)
        session.add(grade)

# Збереження змін у базі даних
session.commit()

# Закриття сесії
session.close()

