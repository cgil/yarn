"""create books table

Revision ID: 4e2c22a692ad
Revises:
Create Date: 2017-02-25 14:44:01.203557

"""

# revision identifiers, used by Alembic.
revision = '4e2c22a692ad'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'book',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String),
        sa.Column('description', sa.String),
        sa.Column('content', sa.Text),
        sa.Column('cover_image_url', sa.String),

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
    op.drop_table('snippet')
