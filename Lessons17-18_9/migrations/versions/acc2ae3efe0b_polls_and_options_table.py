"""polls and options table

Revision ID: acc2ae3efe0b
Revises: 
Create Date: 2024-06-04 19:03:25.307121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acc2ae3efe0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('votes', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('option')
    op.drop_table('user')
    op.drop_table('poll')
    # ### end Alembic commands ###