"""create tables

Revision ID: 000
Revises: 
Create Date: 2024-04-15 10:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создаем enum для статуса платежа, если он не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE payment_status_enum AS ENUM ('PENDING', 'COMPLETED', 'CANCELLED');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    # Создаем enum для валюты, если он не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE currency_enum AS ENUM ('RUB', 'STARS');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    # Создаем таблицу тарифов, если она не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TABLE tariffs (
                id SERIAL NOT NULL,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(500),
                price FLOAT NOT NULL,
                duration_days INTEGER NOT NULL,
                readings_count INTEGER NOT NULL,
                is_active BOOLEAN,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
                PRIMARY KEY (id)
            );
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)
    
    # Создаем таблицу пользователей, если она не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TABLE users (
                id SERIAL NOT NULL,
                telegram_id BIGINT NOT NULL,
                username VARCHAR(32),
                first_name VARCHAR(64),
                last_name VARCHAR(64),
                language VARCHAR(2),
                readings_remaining INTEGER,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
                last_activity TIMESTAMP WITHOUT TIME ZONE,
                referral_id INTEGER,
                referrals_count INTEGER DEFAULT 0,
                subscription_end TIMESTAMP WITHOUT TIME ZONE,
                tariff_id INTEGER,
                PRIMARY KEY (id),
                UNIQUE (telegram_id),
                FOREIGN KEY(referral_id) REFERENCES users (id),
                FOREIGN KEY(tariff_id) REFERENCES tariffs (id)
            );
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)
    
    # Создаем таблицу раскладов, если она не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TABLE readings (
                id SERIAL NOT NULL,
                user_id INTEGER NOT NULL,
                question VARCHAR(500) NOT NULL,
                cards JSONB,
                interpretation VARCHAR(2000) NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY(user_id) REFERENCES users (id)
            );
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)
    
    # Создаем таблицу платежей, если она не существует
    op.execute("""
        DO $$ BEGIN
            CREATE TABLE payments (
                id SERIAL NOT NULL,
                user_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                stars_amount INTEGER,
                currency currency_enum NOT NULL,
                status payment_status_enum NOT NULL,
                payment_id VARCHAR(255),
                readings_count INTEGER,
                duration_days INTEGER,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
                completed_at TIMESTAMP WITHOUT TIME ZONE,
                PRIMARY KEY (id),
                FOREIGN KEY(user_id) REFERENCES users (id)
            );
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)


def downgrade():
    # Удаляем таблицы в обратном порядке
    op.drop_table('payments')
    op.drop_table('readings')
    op.drop_table('users')
    op.drop_table('tariffs')
    
    # Удаляем enum типы
    op.execute('DROP TYPE payment_status_enum')
    op.execute('DROP TYPE currency_enum') 