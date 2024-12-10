# arpakit

from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy import inspect, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_to_json_str

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseDBM(DeclarativeBase):
    __abstract__ = True
    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data

    def simple_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def simple_json(self) -> str:
        return safely_transfer_to_json_str(self.simple_dict())


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True, nullable=False
    )
    long_id: Mapped[str] = mapped_column(
        TEXT, insert_default=uuid4, unique=True, nullable=False
    )
    creation_dt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), insert_default=now_utc_dt, index=True, nullable=False
    )

    def __repr__(self):
        return f"{self.__class__.__name__.removesuffix('DBM')} (id={self.id})"


class StoryLogDBM(SimpleDBM):
    __tablename__ = "story_log"

    class Levels(Enumeration):
        info = "info"
        warning = "warning"
        error = "error"

    level: Mapped[str] = mapped_column(
        TEXT, insert_default=Levels.info, server_default=Levels.info, index=True, nullable=False
    )
    title: Mapped[str | None] = mapped_column(TEXT, index=True, default=None, nullable=True)
    data: Mapped[dict[str, Any]] = mapped_column(
        JSONB, insert_default={}, server_default="{}", index=True, nullable=False
    )


class OperationDBM(SimpleDBM):
    __tablename__ = "operation"

    class Statuses(Enumeration):
        waiting_for_execution = "waiting_for_execution"
        executing = "executing"
        executed_without_error = "executed_without_error"
        executed_with_error = "executed_with_error"

    class Types(Enumeration):
        healthcheck_ = "healthcheck"
        raise_fake_exception_ = "raise_fake_exception"

    status: Mapped[str] = mapped_column(
        TEXT, index=True, insert_default=Statuses.waiting_for_execution,
        server_default=Statuses.waiting_for_execution, nullable=False
    )
    type: Mapped[str] = mapped_column(
        TEXT, index=True, insert_default=Types.healthcheck_, nullable=False
    )
    execution_start_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    execution_finish_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    input_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        insert_default={},
        server_default="{}",
        nullable=False
    )
    output_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)
    error_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)

    def raise_if_executed_with_error(self):
        if self.status == self.Statuses.executed_with_error:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) executed with error, error_data={self.error_data}"
            )

    def raise_if_error_data(self):
        if self.error_data:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) has error_data, error_data={self.error_data}"
            )

    @property
    def duration(self) -> timedelta | None:
        if self.execution_start_dt is None or self.execution_finish_dt is None:
            return None
        return self.execution_finish_dt - self.execution_start_dt

    @property
    def duration_total_seconds(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds()
