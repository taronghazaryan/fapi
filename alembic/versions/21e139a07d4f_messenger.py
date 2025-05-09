"""messenger

Revision ID: 21e139a07d4f
Revises: fcf12e956359
Create Date: 2025-04-23 17:34:03.609201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21e139a07d4f'
down_revision: Union[str, None] = 'fcf12e956359'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dialog',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('from_user', sa.String(), nullable=False),
    sa.Column('to_user', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['from_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('dialog_id', sa.String(), nullable=False),
    sa.Column('from_user', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('viewed', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dialog_id'], ['dialog.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('dialog')
    # ### end Alembic commands ###
