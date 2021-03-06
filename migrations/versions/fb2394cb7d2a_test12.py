"""'test12'

Revision ID: fb2394cb7d2a
Revises: 56f253ea93e8
Create Date: 2022-04-02 16:28:39.517686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb2394cb7d2a'
down_revision = '56f253ea93e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_brands',
    sa.Column('check_id', sa.Integer(), nullable=True),
    sa.Column('asset_brands_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_brands_id'], ['asset_brands.id'], ),
    sa.ForeignKeyConstraint(['check_id'], ['checks.id'], )
    )
    op.create_table('check_no_assets',
    sa.Column('check_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.ForeignKeyConstraint(['check_id'], ['checks.id'], )
    )
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_type', ['type'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_table('check_no_assets')
    op.drop_table('check_brands')
    # ### end Alembic commands ###
