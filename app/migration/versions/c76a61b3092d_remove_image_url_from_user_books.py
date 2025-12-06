"""remove_image_url_from_user_books

Revision ID: НОВЫЙ_ID (замените на реальный из созданного файла)
Revises: e516da1bdc6a
Create Date: 2025-12-05 14:18:48.383577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'НОВЫЙ_ID'  # замените на реальный ID
down_revision: Union[str, Sequence[str], None] = 'e516da1bdc6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем поле image_url из таблицы user_books
    op.drop_column('user_books', 'image_url')


def downgrade() -> None:
    # Восстанавливаем поле image_url в таблице user_books
    op.add_column('user_books', sa.Column('image_url', sa.String(length=500), nullable=True))