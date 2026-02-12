"""add scan cursor boundary fields

Revision ID: c9d6f18a2a10
Revises: 57a053abb139
Create Date: 2026-02-12 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "c9d6f18a2a10"
down_revision = "57a053abb139"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "scan_runs",
        sa.Column("cursor_before_sent_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "scan_runs",
        sa.Column("cursor_last_message_id", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("scan_runs", "cursor_last_message_id")
    op.drop_column("scan_runs", "cursor_before_sent_at")
