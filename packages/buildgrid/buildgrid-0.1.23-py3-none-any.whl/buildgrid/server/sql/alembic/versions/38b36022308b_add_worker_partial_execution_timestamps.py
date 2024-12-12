# Copyright (C) 2024 Bloomberg LP
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

"""Add worker partial execution timestamps

Revision ID: 38b36022308b
Revises: b5563d55f4e3
Create Date: 2024-10-25 17:04:49.469210

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "38b36022308b"
down_revision = "b5563d55f4e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("jobs") as batch_op:
        batch_op.add_column(sa.Column("input_fetch_start_timestamp", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("input_fetch_completed_timestamp", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("output_upload_start_timestamp", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("output_upload_completed_timestamp", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("execution_start_timestamp", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("execution_completed_timestamp", sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("jobs") as batch_op:
        batch_op.drop_column("execution_completed_timestamp")
        batch_op.drop_column("execution_start_timestamp")
        batch_op.drop_column("output_upload_completed_timestamp")
        batch_op.drop_column("output_upload_start_timestamp")
        batch_op.drop_column("input_fetch_completed_timestamp")
        batch_op.drop_column("input_fetch_start_timestamp")
