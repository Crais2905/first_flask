from app import db 
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

class Poll(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    topic: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    options: so.WriteOnlyMapped['Option'] = so.relationship(back_populates='poll')


    def __repr__(self) -> str:
        return f'Poll: {self.topic}'


class Option(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    votes: so.MappedColumn[int] = so.mapped_column(default=0)
    poll_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Poll.id))
    poll: so.Mapped[Poll] = so.relationship(back_populates='options')


    def __repr__(self) -> str:
        return f'Option: {self.title}'
    

class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)