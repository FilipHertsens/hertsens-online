"""'test6'

Revision ID: da1f8305e622
Revises: 4d0ffc505ba2
Create Date: 2022-04-01 13:19:53.699048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da1f8305e622'
down_revision = '4d0ffc505ba2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('asset', sa.Column('type', sa.Integer(), nullable=True))
    #op.add_column('asset', sa.Column('status', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_type', ['type'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_column('asset', 'status')
    op.drop_column('asset', 'type')
    # ### end Alembic commands ###
