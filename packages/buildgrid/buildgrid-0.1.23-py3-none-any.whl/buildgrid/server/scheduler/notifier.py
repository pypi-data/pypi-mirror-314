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


import select
import uuid
from contextlib import contextmanager
from threading import Event, Lock
from typing import Any, Iterator, cast

from sqlalchemy import select as sql_select
from sqlalchemy.orm import Session

from buildgrid.server.logging import buildgrid_logger
from buildgrid.server.sql.models import JobEntry
from buildgrid.server.sql.provider import SqlProvider
from buildgrid.server.threading import ContextWorker

LOGGER = buildgrid_logger(__name__)


class OperationsNotifier:
    def __init__(self, sql_provider: SqlProvider, poll_interval: float = 1) -> None:
        """
        Creates a notifier for changes to jobs, used by observes of related operations.

        Note: jobs have a one-to-many relationship with operations, and for each operation
        there can be multiple clients listening for updates.
        """

        self._sql = sql_provider
        self._lock = Lock()
        self._listeners: dict[str, dict[str, Event]] = {}
        self.poll_interval = poll_interval
        self.worker = ContextWorker(name="OperationsNotifier", target=self.begin)

    def __enter__(self: "OperationsNotifier") -> "OperationsNotifier":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

    def start(self) -> None:
        self.worker.start()

    def stop(self) -> None:
        self.worker.stop()

    def listener_count(self) -> int:
        """Used for reporting job metrics about the scheduling."""
        with self._lock:
            return sum(len(events) for events in self._listeners.values())

    def begin(self, shutdown_requested: Event) -> None:
        LOGGER.info("Starting job notifier thread.")

        while not shutdown_requested.is_set():
            try:
                with self._sql.session() as session:
                    if self._sql.dialect == "postgresql":
                        self._listen_for_updates(shutdown_requested, session)
                    else:
                        self._poll_for_updates(shutdown_requested, session)
            except Exception as e:
                LOGGER.warning(
                    f"OperationsNotifier encountered exception: {e}.",
                    tags=dict(retry_delay_seconds=self.poll_interval),
                )
                # Sleep for a bit so that we give enough time for the
                # database to potentially recover
                shutdown_requested.wait(timeout=self.poll_interval)

    def _listen_for_updates(self, shutdown_requested: Event, session: Session) -> None:
        # In our `LISTEN` call, we want to *bypass the ORM* and *use the underlying Engine connection directly*.
        # This is because using a `session.execute()` will implicitly create a SQL transaction, causing
        # notifications to only be delivered when that transaction is committed.
        from psycopg2.extensions import connection

        try:
            pool_connection = session.connection().connection
            pool_connection.cursor().execute("LISTEN job_updated;")
            pool_connection.commit()
        except Exception:
            LOGGER.warning("Could not start listening to DB for job updates.", exc_info=True)
            raise

        while not shutdown_requested.is_set() and pool_connection.dbapi_connection is not None:
            # If we're in this method, we know we have a psycopg2 connection object here.
            dbapi_connection = cast(connection, pool_connection.dbapi_connection)

            # Wait until the connection is ready for reading. Timeout and try again if there was nothing to read.
            # If the connection becomes readable, collect the notifications it has received and handle them.
            #
            # See https://www.psycopg.org/docs/advanced.html#asynchronous-notifications
            if select.select([dbapi_connection], [], [], self.poll_interval) == ([], [], []):
                continue

            dbapi_connection.poll()
            while dbapi_connection.notifies:
                notify = dbapi_connection.notifies.pop()
                self.notify(notify.payload)

    def _poll_for_updates(self, shutdown_requested: Event, session: Session) -> None:
        prev_data: dict[str, tuple[bool, int]] = {}
        while not shutdown_requested.is_set():
            with self._lock:
                names = list(self._listeners)

            # Only query for the minimal amount of data required.
            # The subscribers can choose how they want to act (e.g. by querying the full job data).
            statement = sql_select(JobEntry.name, JobEntry.cancelled, JobEntry.stage).where(JobEntry.name.in_(names))
            next_data: dict[str, tuple[bool, int]] = {}
            for [name, cancelled, stage] in session.execute(statement).all():
                next_data[name] = (cancelled, stage)

            for name in next_data:
                if name not in prev_data or prev_data[name] != next_data[name]:
                    self.notify(name)

            prev_data = next_data
            shutdown_requested.wait(timeout=self.poll_interval)

    def notify(self, job_name: str) -> None:
        with self._lock:
            if job_name in self._listeners:
                for event in self._listeners[job_name].values():
                    event.set()

    @contextmanager
    def subscription(self, job_name: str) -> Iterator[Event]:
        """
        Register a threading.Event object which is triggered each time the associated job_name updates
        its cancelled or stage status. After waiting for an event, the caller should immediately call
        event.clear() if they wish to re-use the event again, otherwise the event object will remain set.
        """

        # Create a unique key for the subscription which is deleted when the job is no longer monitored.
        key = str(uuid.uuid4())
        event = Event()
        try:
            with self._lock:
                if job_name not in self._listeners:
                    self._listeners[job_name] = {}
                self._listeners[job_name][key] = event
            yield event
        finally:
            with self._lock:
                del self._listeners[job_name][key]
                if len(self._listeners[job_name]) == 0:
                    del self._listeners[job_name]
