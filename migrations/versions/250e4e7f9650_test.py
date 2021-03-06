"""test

Revision ID: 250e4e7f9650
Revises: 9e788395cd78
Create Date: 2022-04-14 11:15:43.247790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '250e4e7f9650'
down_revision = '9e788395cd78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'asset', ['wacs_id'])
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_model', ['model'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    op.drop_column('asset', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset', sa.Column('type', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='unique')
    # ### end Alembic commands ###
