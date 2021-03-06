"""empty message

Revision ID: 5c53db006c72
Revises: 2e9edf2bb3ba
Create Date: 2021-07-10 02:37:05.906820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c53db006c72'
down_revision = '2e9edf2bb3ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venues', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venues', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
