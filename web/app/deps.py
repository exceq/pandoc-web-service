from core.db.session import session


def get_db():
    try:
        db = session()
        yield db
    except:
        db.close()
