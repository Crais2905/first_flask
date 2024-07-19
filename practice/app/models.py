from app import db, login
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from datetime import datetime

user_tour = sa.Table(
    'user_tour',
    db.metadata,
    sa.Column('tour_id', sa.Integer, sa.ForeignKey('tour.id'), primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)  
)

class Tour(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(50), index=True)
    decription: so.MappedColumn[str] = so.mapped_column(sa.String(2000), index=True)
    price: so.MappedColumn[float] = so.mapped_column(index=True)
    country: so.MappedColumn[str] = so.mapped_column(index=True)
    time: so.MappedColumn[datetime] = so.mapped_column(default=lambda: datetime.now())
    users: so.WriteOnlyMapped['User'] = so.relationship('User', secondary='user_tour', back_populates='bought_tours')


    def __repr__(self) -> str:
        return f"{self.title}"


class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True)
    bought_tours: so.WriteOnlyMapped[Tour] = so.relationship('Tour', secondary='user_tour', back_populates='users')

    def __repr__(self) -> str:
        return f'{self.username}'
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)
    

@login.user_loader
def user_loader(id):
    return db.session.get(User, id)