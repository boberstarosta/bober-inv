"""create buyer, rate, item, invoice

Revision ID: e0f3580054f1
Revises: 9b413911761d
Create Date: 2018-11-28 16:02:54.819013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f3580054f1'
down_revision = '9b413911761d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=600), nullable=True),
    sa.Column('vat_number', sa.String(length=20), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=True),
    sa.Column('time_expired', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_buyer_address'), 'buyer', ['address'], unique=False)
    op.create_index(op.f('ix_buyer_name'), 'buyer', ['name'], unique=False)
    op.create_index(op.f('ix_buyer_time_created'), 'buyer', ['time_created'], unique=False)
    op.create_index(op.f('ix_buyer_time_expired'), 'buyer', ['time_expired'], unique=False)
    op.create_index(op.f('ix_buyer_vat_number'), 'buyer', ['vat_number'], unique=False)
    op.create_table('rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rate_name'), 'rate', ['name'], unique=False)
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=20), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoice_date'), 'invoice', ['date'], unique=False)
    op.create_index(op.f('ix_invoice_number'), 'invoice', ['number'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('unit', sa.String(length=20), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('net_price', sa.Integer(), nullable=True),
    sa.Column('rate_id', sa.Integer(), nullable=True),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['rate_id'], ['rate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_index'), 'item', ['index'], unique=False)
    op.create_index(op.f('ix_item_name'), 'item', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_name'), table_name='item')
    op.drop_index(op.f('ix_item_index'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_invoice_number'), table_name='invoice')
    op.drop_index(op.f('ix_invoice_date'), table_name='invoice')
    op.drop_table('invoice')
    op.drop_index(op.f('ix_rate_name'), table_name='rate')
    op.drop_table('rate')
    op.drop_index(op.f('ix_buyer_vat_number'), table_name='buyer')
    op.drop_index(op.f('ix_buyer_time_expired'), table_name='buyer')
    op.drop_index(op.f('ix_buyer_time_created'), table_name='buyer')
    op.drop_index(op.f('ix_buyer_name'), table_name='buyer')
    op.drop_index(op.f('ix_buyer_address'), table_name='buyer')
    op.drop_table('buyer')
    # ### end Alembic commands ###
