from base import Base, engine

from base import Base, engine, User, SessionLocal
import time

def init_db():
    print('Started creating tables...')
    Base.metadata.create_all(bind=engine)

    print('Checking test users...')
    session = SessionLocal()

    # Проверяем существование пользователей
    if not session.query(User).filter(User.login.in_(['pavel', 'yura'])).count():
        print('Adding test users...')
        users = [
            User(login='pavel', email='a@gmail.com'),
            User(login='yura', email='b@gmail.com')
        ]
        session.add_all(users)
        session.commit()
        print('Test users added successfully!')
    else:
        print('Test users already exist')

    session.close()

if __name__ == "__main__":
    # Добавляем повторные попытки для надежности
    max_retries = 5
    for attempt in range(max_retries):
        try:
            init_db()
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(3)
    else:
        print("All initialization attempts failed")