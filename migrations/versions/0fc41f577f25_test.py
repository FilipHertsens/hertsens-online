"""test

Revision ID: 0fc41f577f25
Revises: 250e4e7f9650
Create Date: 2022-04-14 11:17:19.737819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fc41f577f25'
down_revision = '250e4e7f9650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'asset', ['wacs_id'])
    op.create_foreign_key(None, 'asset', 'asset_model', ['model'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    op.drop_column('asset', 'type')
    op.add_column('users', sa.Column('current_asset_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'asset', ['current_asset_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'current_asset_id')
    op.add_column('asset', sa.Column('type', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='unique')
    # ### end Alembic commands ###
