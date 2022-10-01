"""create pootracker table

Revision ID: d350e45908cd
Revises: 
Create Date: 2022-09-30 21:18:17.792618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd350e45908cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pootracker',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date),
        sa.Column('time', sa.Time),
        sa.Column('pee', sa.Boolean),
        sa.Column('poo', sa.Boolean),
        sa.Column('accident', sa.Boolean)
    )


def downgrade() -> None:
    op.drop_table(
        'pootracker'
    )
