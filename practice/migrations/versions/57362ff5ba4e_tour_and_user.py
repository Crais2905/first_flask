"""Tour and User

Revision ID: 57362ff5ba4e
Revises: 
Create Date: 2024-06-12 18:49:18.699519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57362ff5ba4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tour',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('decription', sa.String(length=2000), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tour', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tour_country'), ['country'], unique=False)
        batch_op.create_index(batch_op.f('ix_tour_decription'), ['decription'], unique=False)
        batch_op.create_index(batch_op.f('ix_tour_price'), ['price'], unique=False)
        batch_op.create_index(batch_op.f('ix_tour_title'), ['title'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_password_hash'), ['password_hash'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('user_tour',
    sa.Column('tour_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True, primery_key=True),
    sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('tour_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tour')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_password_hash'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('tour', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tour_title'))
        batch_op.drop_index(batch_op.f('ix_tour_price'))
        batch_op.drop_index(batch_op.f('ix_tour_decription'))
        batch_op.drop_index(batch_op.f('ix_tour_country'))

    op.drop_table('tour')
    # ### end Alembic commands ###
