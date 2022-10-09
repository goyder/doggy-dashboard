"""Change date-time columns

Revision ID: 40bc32a0f1c9
Revises: d350e45908cd
Create Date: 2022-10-04 20:50:04.532633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40bc32a0f1c9'
down_revision = 'd350e45908cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'pootracker', 
        sa.Column('datetime', sa.DateTime)
    )
    op.drop_column(
        'pootracker',
        'date'
    )
    op.drop_column(
        'pootracker',
        'time'
    )


def downgrade() -> None:
    op.drop_column(
        'pootracker',
        'datetime'
    )
    op.add_column(
        'pootracker', 
        sa.Column('date', sa.Date)
    )
    op.add_column(
        'pootracker', 
        sa.Column('time', sa.Time)
    )
