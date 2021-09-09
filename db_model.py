from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, Float
from sqlalchemy.pool import QueuePool


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Float)
    IP = Column(String)

    def __repr__(self):
        return f"""{self.first_name} {self.first_name} is {self.age} years old.
        IP: {self.IP}."""

class DB_factory:
    def __init__(self) -> None:
        with open("db_creds.txt", "r") as file:
            user, password, host, port = file.read().split(",")
        
        self.db = f"postgresql://{user}:{password}@{host}:{port}/"
        self.creds = {'user': user,
                        'password': password,
                        'host': host,
                        'port': port}

        self.engine = create_engine(
            self.db,
            echo=False,
            pool_size=20,
            poolclass=QueuePool,
        )
        # self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/", echo=True)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()