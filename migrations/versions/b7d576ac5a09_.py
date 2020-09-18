"""empty message

Revision ID: b7d576ac5a09
Revises: ddaa36f81f86
Create Date: 2020-09-17 18:02:56.057708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d576ac5a09'
down_revision = 'ddaa36f81f86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'creation_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('creation_date', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
