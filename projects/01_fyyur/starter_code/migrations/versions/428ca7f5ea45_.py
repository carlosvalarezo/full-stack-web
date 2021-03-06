"""empty message

Revision ID: 428ca7f5ea45
Revises: 9ef4ab87bad5
Create Date: 2021-06-23 08:24:45.157383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '428ca7f5ea45'
down_revision = '9ef4ab87bad5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###
