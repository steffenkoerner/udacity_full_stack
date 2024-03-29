"""empty message

Revision ID: 9dc1790cbc42
Revises: 3fd37c520a39
Create Date: 2020-03-30 18:08:16.522586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dc1790cbc42'
down_revision = '3fd37c520a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
