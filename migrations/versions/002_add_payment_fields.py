"""add payment fields

Revision ID: 002
Revises: 001
Create Date: 2024-04-13 15:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Добавляем новые поля в таблицу payments
    op.add_column('payments', sa.Column('readings_count', sa.Integer(), nullable=True))
    op.add_column('payments', sa.Column('duration_days', sa.Integer(), nullable=True))

def downgrade():
    # Удаляем добавленные поля
    op.drop_column('payments', 'readings_count')
    op.drop_column('payments', 'duration_days') 