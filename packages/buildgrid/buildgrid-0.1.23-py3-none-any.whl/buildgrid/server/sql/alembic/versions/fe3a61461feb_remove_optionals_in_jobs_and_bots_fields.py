# Copyright (C) 2020 Bloomberg LP
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

"""remove optionals in jobs and bots fields

Revision ID: fe3a61461feb
Revises: e83194af8292
Create Date: 2024-08-30 12:39:10.653746

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fe3a61461feb"
down_revision = "e83194af8292"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("jobs") as batch_op:
        batch_op.alter_column("instance_name", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("action", existing_type=postgresql.BYTEA(), nullable=False)
        batch_op.alter_column("queued_timestamp", existing_type=postgresql.TIMESTAMP(), nullable=False)
        batch_op.alter_column("assigned", existing_type=sa.BOOLEAN(), nullable=False)
        batch_op.alter_column("n_tries", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column("platform_requirements", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("command", existing_type=sa.VARCHAR(), nullable=False)

    with op.batch_alter_table("bots") as batch_op:
        batch_op.alter_column("instance_name", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("expiry_time", existing_type=postgresql.TIMESTAMP(), nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("jobs") as batch_op:
        batch_op.alter_column("instance_name", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("action", existing_type=postgresql.BYTEA(), nullable=True)
        batch_op.alter_column("queued_timestamp", existing_type=postgresql.TIMESTAMP(), nullable=True)
        batch_op.alter_column("assigned", existing_type=sa.BOOLEAN(), nullable=True)
        batch_op.alter_column("n_tries", existing_type=sa.INTEGER(), nullable=True)
        batch_op.alter_column("platform_requirements", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("command", existing_type=sa.VARCHAR(), nullable=True)

    with op.batch_alter_table("bots") as batch_op:
        batch_op.alter_column("instance_name", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("expiry_time", existing_type=postgresql.TIMESTAMP(), nullable=True)
