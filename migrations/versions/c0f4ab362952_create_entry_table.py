"""create entry table

Revision ID: c0f4ab362952
Revises: eb524b1b15d7
Create Date: 2017-02-27 20:30:06.997341

"""

# revision identifiers, used by Alembic.
revision = 'c0f4ab362952'
down_revision = 'eb524b1b15d7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'entry',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('publisher_id', sa.Integer),
        sa.Column('channel_id', sa.Integer),
        sa.Column('title', sa.String),
        sa.Column('link', sa.String),
        sa.Column('summary', sa.String),
        sa.Column('content', sa.Text),
        sa.Column('content_type', sa.String),
        sa.Column('external_entry_id', sa.String),
        sa.Column('publication_datetime', sa.DateTime),
        sa.Column('publication_updated_datetime', sa.DateTime),

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
    op.drop_table('entry')
