"""add_image_url_to_books

Revision ID: e516da1bdc6a
Revises: 
Create Date: 2025-12-04 22:33:25.467945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e516da1bdc6a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем поле image_url в таблицу books
    op.add_column('books', sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем поле image_url из таблицы books
    op.drop_column('books', 'image_url')