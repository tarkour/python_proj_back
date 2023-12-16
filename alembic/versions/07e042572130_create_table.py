"""create table

Revision ID: 07e042572130
Revises: 
Create Date: 2023-12-16 23:10:25.961442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from database_runner import Messages, Users


# revision identifiers, used by Alembic.
revision: str = '07e042572130'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        Messages,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('messages', sa.String(120), nullable=False),
        sa.Column('date', sa.DateTime, default=datetime.datetime.now(tz=pytz.timezone('UTC')))
    )
    op.create_foreign_key('fk_user_id', Messages, Users,
                          ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table(Messages)
