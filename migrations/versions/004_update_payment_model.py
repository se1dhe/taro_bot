"""update payment model

Revision ID: 004
Revises: 003
Create Date: 2024-03-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем enum для валюты
    op.execute("CREATE TYPE currency_enum AS ENUM ('RUB', 'STARS')")
    
    # Создаем enum для статуса платежа
    op.execute("CREATE TYPE payment_status_enum AS ENUM ('PENDING', 'COMPLETED', 'CANCELLED')")
    
    # Обновляем таблицу payments
    op.alter_column('payments', 'amount',
                    existing_type=sa.Float(),
                    type_=sa.Integer(),
                    nullable=False)
    
    op.add_column('payments', sa.Column('stars_amount', sa.Integer(), nullable=True))
    
    op.alter_column('payments', 'currency',
                    existing_type=sa.String(length=3),
                    type_=sa.Enum('RUB', 'STARS', name='currency_enum'),
                    nullable=False)
    
    op.alter_column('payments', 'status',
                    existing_type=sa.String(length=20),
                    type_=sa.Enum('PENDING', 'COMPLETED', 'CANCELLED', name='payment_status_enum'),
                    nullable=False)
    
    op.alter_column('payments', 'payment_id',
                    existing_type=sa.String(length=100),
                    type_=sa.String(length=255),
                    nullable=True)


def downgrade() -> None:
    # Откатываем изменения
    op.alter_column('payments', 'payment_id',
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=100),
                    nullable=True)
    
    op.alter_column('payments', 'status',
                    existing_type=sa.Enum('PENDING', 'COMPLETED', 'CANCELLED', name='payment_status_enum'),
                    type_=sa.String(length=20),
                    nullable=True)
    
    op.alter_column('payments', 'currency',
                    existing_type=sa.Enum('RUB', 'STARS', name='currency_enum'),
                    type_=sa.String(length=3),
                    nullable=True)
    
    op.drop_column('payments', 'stars_amount')
    
    op.alter_column('payments', 'amount',
                    existing_type=sa.Integer(),
                    type_=sa.Float(),
                    nullable=False)
    
    # Удаляем enum типы
    op.execute("DROP TYPE payment_status_enum")
    op.execute("DROP TYPE currency_enum") 