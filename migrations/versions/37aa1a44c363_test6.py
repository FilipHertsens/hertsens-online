"""'test6'

Revision ID: 37aa1a44c363
Revises: da1f8305e622
Create Date: 2022-04-01 18:18:03.707663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37aa1a44c363'
down_revision = 'da1f8305e622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aggregaat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('asset_aggregaat',
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('aggregaat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['aggregaat_id'], ['aggregaat.id'], ),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], )
    )
    op.create_foreign_key(None, 'asset', 'asset_brands', ['brand'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_type', ['type'], ['id'])
    op.create_foreign_key(None, 'asset', 'asset_status', ['status'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.drop_table('asset_aggregaat')
    op.drop_table('aggregaat')
    # ### end Alembic commands ###
