"""create publisher table

Revision ID: 43274ea2c116
Revises: 4e2c22a692ad
Create Date: 2017-02-27 20:10:01.214916

"""

# revision identifiers, used by Alembic.
revision = '43274ea2c116'
down_revision = '4e2c22a692ad'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'publisher',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),

        sa.Column(
            'created_at',
            sa.DateTime,
            nullable=False,
            server_default=sa.text('now()'),
            default=sa.text('now()')
        ),
        sa.Column('deleted_at', sa.DateTime),
        sa.Column(
            'updated_at', sa.DateTime, nullable=False,
            server_onupdate=sa.text('now()'),
            onupdate=sa.text('now()'),
            default=sa.text('now()')
        ),
    )


def downgrade():
    op.drop_table('publisher')
