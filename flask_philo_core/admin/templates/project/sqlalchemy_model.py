from flask_philo_sqlalchemy.test import SQLAlchemyTestCase
from flask_philo_sqlalchemy.orm import BaseModel
from flask_philo_sqlalchemy.types import Password
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship
from flask_philo_sqlalchemy.exceptions import NotFoundError



class User(BaseModel):
    __tablename__ = '{{project_name}}'
    id = Column(Integer, primary_key=True)
