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

"""Add instance name to jobs

Revision ID: d4efbcc698ca
Revises: afa46425330d
Create Date: 2023-12-11 11:57:45.292788

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4efbcc698ca"
down_revision = "bc324dfd3610"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("jobs", sa.Column("instance_name", sa.String()))
    op.create_index(op.f("ix_jobs_instance_name"), "jobs", ["instance_name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_instance_name"), table_name="jobs")
    op.drop_column("jobs", "instance_name")
