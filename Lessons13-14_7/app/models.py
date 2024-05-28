from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from datetime import datetime


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True)
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')


    def __repr__(self) -> str:
        return f'User: {self.username}'
    

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(500), unique=True, index=True)
    time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')


    def __repr__(self) -> str:
        return f'Post: {self.body}'
