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

"""Add command column to the jobs table

Revision ID: 9b595964dc25
Revises: fcb6e8f09a1d
Create Date: 2023-10-05 14:54:18.791620

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9b595964dc25"
down_revision = "e1448dca2c7a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("jobs", sa.Column("command", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("jobs", "command")
