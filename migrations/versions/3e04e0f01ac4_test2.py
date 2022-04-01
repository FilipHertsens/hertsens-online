"""'test2'

Revision ID: 3e04e0f01ac4
Revises: 496614549be0
Create Date: 2022-04-01 10:49:01.668706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e04e0f01ac4'
down_revision = '496614549be0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('telegram_id', sa.String(length=50, collation='NOCASE'), nullable=True))
    op.create_unique_constraint(None, 'person', ['telegram_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'person', type_='unique')
    op.drop_column('person', 'telegram_id')
    # ### end Alembic commands ###
