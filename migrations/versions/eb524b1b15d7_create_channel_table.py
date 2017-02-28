"""create channel table

Revision ID: eb524b1b15d7
Revises: 43274ea2c116
Create Date: 2017-02-27 20:14:25.572541

"""

# revision identifiers, used by Alembic.
revision = 'eb524b1b15d7'
down_revision = '43274ea2c116'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'channel',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('publisher_id', sa.Integer),
        sa.Column('title', sa.String),
        sa.Column('description', sa.String),
        sa.Column('link', sa.String),
        sa.Column('publication_datetime', sa.DateTime),
        sa.Column('external_publication_id', sa.String),

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
    op.drop_table('channel')
