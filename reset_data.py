from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Видалення всіх записів з таблиць
session.query(Grade).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()

# Збереження змін у базі даних
session.commit()

# Закриття сесії
session.close()
