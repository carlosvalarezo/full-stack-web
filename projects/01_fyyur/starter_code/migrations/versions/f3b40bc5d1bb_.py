"""empty message

Revision ID: f3b40bc5d1bb
Revises: 428ca7f5ea45
Create Date: 2021-06-23 09:31:25.699332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b40bc5d1bb'
down_revision = '428ca7f5ea45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_venue')
    # ### end Alembic commands ###
