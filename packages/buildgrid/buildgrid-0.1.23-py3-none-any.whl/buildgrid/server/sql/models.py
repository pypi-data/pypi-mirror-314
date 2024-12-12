# Copyright (C) 2019 Bloomberg LP
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
import datetime
from typing import Annotated

from sqlalchemy import BigInteger, Column, ForeignKey, Index, Table, UniqueConstraint, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry, relationship

from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import Action, Digest
from buildgrid._protos.google.devtools.remoteworkers.v1test2 import bots_pb2
from buildgrid.server.enums import LeaseState

bigint = Annotated[int, "bigint"]


class Base(DeclarativeBase):
    registry = registry(type_annotation_map={bigint: BigInteger()})


job_platform_association = Table(
    "job_platforms",
    Base.metadata,
    Column("job_name", ForeignKey("jobs.name", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("platform_id", ForeignKey("platform_properties.id"), primary_key=True),
)


class PlatformEntry(Base):
    __tablename__ = "platform_properties"
    __table_args__ = (UniqueConstraint("key", "value"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    key: Mapped[str]
    value: Mapped[str]

    jobs: Mapped[list["JobEntry"]] = relationship(
        "JobEntry", secondary=job_platform_association, back_populates="platform"
    )


class JobEntry(Base):
    __tablename__ = "jobs"

    # Immutable data
    name: Mapped[str] = mapped_column(primary_key=True)
    instance_name: Mapped[str] = mapped_column(index=True)
    action_digest: Mapped[str] = mapped_column(index=True)
    action: Mapped[bytes]
    do_not_cache: Mapped[bool] = mapped_column(default=False)
    # This is a hash of the platform properties, used for matching jobs to workers
    platform_requirements: Mapped[str]
    property_label: Mapped[str] = mapped_column(server_default="unknown")
    command: Mapped[str]

    # Scheduling state
    stage: Mapped[int] = mapped_column(default=0)
    priority: Mapped[int] = mapped_column(default=1, index=True)
    cancelled: Mapped[bool] = mapped_column(default=False)
    assigned: Mapped[bool] = mapped_column(default=False)
    n_tries: Mapped[int] = mapped_column(default=0)

    # Return data on completion
    result: Mapped[str | None]
    status_code: Mapped[int | None]

    # Auditing data
    create_timestamp: Mapped[datetime.datetime | None]
    queued_timestamp: Mapped[datetime.datetime] = mapped_column(index=True)
    queued_time_duration: Mapped[int | None]
    worker_start_timestamp: Mapped[datetime.datetime | None]
    worker_completed_timestamp: Mapped[datetime.datetime | None]
    input_fetch_start_timestamp: Mapped[datetime.datetime | None]
    input_fetch_completed_timestamp: Mapped[datetime.datetime | None]
    output_upload_start_timestamp: Mapped[datetime.datetime | None]
    output_upload_completed_timestamp: Mapped[datetime.datetime | None]
    execution_start_timestamp: Mapped[datetime.datetime | None]
    execution_completed_timestamp: Mapped[datetime.datetime | None]

    # Logstream identifiers
    stdout_stream_name: Mapped[str | None]
    stdout_stream_write_name: Mapped[str | None]
    stderr_stream_name: Mapped[str | None]
    stderr_stream_write_name: Mapped[str | None]

    leases: Mapped[list["LeaseEntry"]] = relationship("LeaseEntry", back_populates="job")
    active_states: list[int] = [
        LeaseState.UNSPECIFIED.value,
        LeaseState.PENDING.value,
        LeaseState.ACTIVE.value,
        LeaseState.CANCELLED.value,
    ]
    active_leases: Mapped[list["LeaseEntry"]] = relationship(
        "LeaseEntry",
        primaryjoin=f"and_(LeaseEntry.job_name==JobEntry.name, LeaseEntry.state.in_({active_states}))",
        order_by="LeaseEntry.id.desc()",
        overlaps="job,leases",
    )

    operations: Mapped[list["OperationEntry"]] = relationship("OperationEntry", back_populates="job")

    platform: Mapped[list["PlatformEntry"]] = relationship(
        "PlatformEntry", secondary=job_platform_association, back_populates="jobs"
    )

    __table_args__ = (
        Index(
            "ix_worker_start_timestamp",
            "worker_start_timestamp",
            unique=False,
            postgresql_where="worker_start_timestamp IS NOT null",
            sqlite_where="worker_start_timestamp IS NOT null",
        ),
        Index(
            "ix_worker_completed_timestamp",
            "worker_completed_timestamp",
            unique=False,
            postgresql_where="worker_completed_timestamp IS NOT null",
            sqlite_where="worker_completed_timestamp IS NOT null",
        ),
        Index(
            "ix_jobs_stage_property_label",
            "stage",
            "property_label",
            unique=False,
        ),
    )


class LeaseEntry(Base):
    __tablename__ = "leases"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(ForeignKey("jobs.name", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    status: Mapped[int | None]
    state: Mapped[int]
    worker_name: Mapped[str | None] = mapped_column(index=True, default=None)

    job: Mapped[JobEntry] = relationship(JobEntry, back_populates="leases")

    def to_protobuf(self) -> bots_pb2.Lease:
        lease = bots_pb2.Lease()
        lease.id = self.job_name

        if self.job.action is not None:
            action = Action()
            action.ParseFromString(self.job.action)
            lease.payload.Pack(action)
        else:
            lease.payload.Pack(string_to_digest(self.job.action_digest))

        lease.state = self.state  # type: ignore[assignment]
        if self.status is not None:
            lease.status.code = self.status
        return lease


class ClientIdentityEntry(Base):
    __tablename__ = "client_identities"
    __table_args__ = (UniqueConstraint("instance", "workflow", "actor", "subject"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instance: Mapped[str]
    workflow: Mapped[str]
    actor: Mapped[str]
    subject: Mapped[str]

    def __str__(self) -> str:
        return (
            f"ClientIdentity: [instance={self.instance} workflow={self.workflow}"
            f" actor={self.actor} subject={self.subject}]"
        )


class RequestMetadataEntry(Base):
    __tablename__ = "request_metadata"
    __table_args__ = (
        UniqueConstraint(
            "tool_name",
            "tool_version",
            "invocation_id",
            "correlated_invocations_id",
            "action_mnemonic",
            "target_id",
            "configuration_id",
            name="unique_metadata_constraint",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tool_name: Mapped[str | None]
    tool_version: Mapped[str | None]
    invocation_id: Mapped[str | None]
    correlated_invocations_id: Mapped[str | None]
    action_mnemonic: Mapped[str | None]
    target_id: Mapped[str | None]
    configuration_id: Mapped[str | None]


class OperationEntry(Base):
    __tablename__ = "operations"

    name: Mapped[str] = mapped_column(primary_key=True)
    cancelled: Mapped[bool] = mapped_column(default=False, nullable=False)
    tool_name: Mapped[str | None]
    tool_version: Mapped[str | None]
    invocation_id: Mapped[str | None]
    correlated_invocations_id: Mapped[str | None]

    job_name: Mapped[str] = mapped_column(ForeignKey("jobs.name", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    job: Mapped[JobEntry] = relationship(JobEntry, back_populates="operations")

    client_identity_id: Mapped[int | None] = mapped_column(ForeignKey("client_identities.id"))
    client_identity: Mapped[ClientIdentityEntry | None] = relationship("ClientIdentityEntry")

    request_metadata_id: Mapped[int | None] = mapped_column(ForeignKey(RequestMetadataEntry.id))
    request_metadata: Mapped[RequestMetadataEntry | None] = relationship(RequestMetadataEntry)


class IndexEntry(Base):
    __tablename__ = "index"

    digest_hash: Mapped[str] = mapped_column(index=True, primary_key=True)
    digest_size_bytes: Mapped[bigint]
    accessed_timestamp: Mapped[datetime.datetime] = mapped_column(index=True)
    deleted: Mapped[bool] = mapped_column(server_default=false())
    inline_blob: Mapped[bytes | None]


# This table is used to store the bot session state. It also stores the
# assigned leases, instead of making use of the 'leases' table through an
# SQLAlchemy relationship, as the 'leases' table is dependent on the type of
# data store selected, and might never be populated.
# TODO: We can now guarantee that `leases` exists, and should add a proper
# relationship in the data model instead of this.
class BotEntry(Base):
    __tablename__ = "bots"

    # Immutable data
    name: Mapped[str] = mapped_column(index=True, primary_key=True)
    bot_id: Mapped[str] = mapped_column(index=True)
    instance_name: Mapped[str]

    # Scheduling state
    bot_status: Mapped[int]
    lease_id: Mapped[str | None]

    # Auditing data
    expiry_time: Mapped[datetime.datetime] = mapped_column(index=True)
    last_update_timestamp: Mapped[datetime.datetime] = mapped_column(index=True)

    job: Mapped[JobEntry | None] = relationship(JobEntry, primaryjoin="foreign(BotEntry.lease_id) == JobEntry.name")


# This table is used by the SQLStorage CAS backend to store blobs
# in a database.
class BlobEntry(Base):
    __tablename__ = "blobs"

    digest_hash: Mapped[str] = mapped_column(primary_key=True)
    digest_size_bytes: Mapped[bigint]
    data: Mapped[bytes]


def digest_to_string(digest: Digest) -> str:
    return f"{digest.hash}/{digest.size_bytes}"


def string_to_digest(string: str) -> Digest:
    digest_hash, size_bytes = string.split("/", 1)
    return Digest(hash=digest_hash, size_bytes=int(size_bytes))
