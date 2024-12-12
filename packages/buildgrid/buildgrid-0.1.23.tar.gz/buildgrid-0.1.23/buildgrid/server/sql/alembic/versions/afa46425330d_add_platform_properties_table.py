# Copyright (C) 2023 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Add platform properties table

Revision ID: afa46425330d
Revises: 9b595964dc25
Create Date: 2023-10-05 17:08:45.628326

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "afa46425330d"
down_revision = "9b595964dc25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "platform_properties",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key", sa.String(), nullable=True),
        sa.Column("value", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key", "value"),
    )
    op.create_table(
        "job_platforms",
        sa.Column("job_name", sa.String(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["job_name"],
            ["jobs.name"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform_properties.id"],
        ),
        sa.PrimaryKeyConstraint("job_name", "platform_id"),
    )


def downgrade() -> None:
    op.drop_table("job_platforms")
    op.drop_table("platform_properties")
