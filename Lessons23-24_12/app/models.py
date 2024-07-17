from app import db
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
# from werkzeug.security import generate_password_hash, check_password_hash
# from typing import Optional
from datetime import datetime



class Category(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    name: so.MappedColumn[str] = so.mapped_column(sa.String(100), index=True)
    posts: so.Mapped['Post'] = so.relationship(back_populates='category')


    def __repr__(self) -> str:
        return f'{self.name}'


class Post(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    name: so.MappedColumn[str] = so.mapped_column(sa.String(100), index=True)
    content: so.MappedColumn[str] = so.mapped_column(sa.Text, index=True)
    time: so.MappedColumn[datetime] = so.mapped_column(default=lambda: datetime.now())
    category_id: so.MappedColumn[int] = so.mapped_column(sa.ForeignKey(Category.id))
    category: so.Mapped[Category] = so.relationship(back_populates='posts')


    def __repr__(self) -> str:
        return f'{self.name}'