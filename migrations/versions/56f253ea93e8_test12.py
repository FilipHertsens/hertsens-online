"""'test12'

Revision ID: 56f253ea93e8
Revises: ca3171a699d1
Create Date: 2022-04-02 16:12:47.944778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56f253ea93e8'
down_revision = 'ca3171a699d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'asset', 'asset_type', ['type'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    # ### end Alembic commands ###