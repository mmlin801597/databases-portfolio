
"""Code-first data contract for the repaired maintenance schema."""

from datetime import date

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    MetaData,
    UniqueConstraint,
)

# 1. Application-level validation using Pydantic

class Machine(BaseModel):
    machine_id: int = Field(ge=1)
    machine_name: str = Field(min_length=1)
    serial_no: str = Field(min_length=3)
    site: str
    installed: date

    @field_validator("serial_no")
    @classmethod
    def serial_has_prefix(cls, v: str) -> str:
        if not v.startswith("SN-"):
            raise ValueError("serial numbers must start with 'SN-'")
        return v


class MaintenanceJob(BaseModel):
    job_id: int = Field(ge=1)
    machine_id: int = Field(ge=1)
    technician_id: int = Field(ge=1)
    done_on: date
    part_nos: list[str] = Field(default_factory=list)


class Technician(BaseModel):
    technician_id: int = Field(ge=1)
    technician_name: str = Field(min_length=1)


# 2. Database-level constraints using SQLAlchemy

metadata = MetaData()

machine_t = Table(
    "machine",
    metadata,
    Column("machine_id", Integer, primary_key=True),
    Column("machine_name", String, nullable=False, unique=True),
    Column("serial_no", String, nullable=False),
    Column("site", String, nullable=False),
    Column("installed", Date, nullable=False),
    UniqueConstraint("serial_no", name="uq_machine_serial"),
    CheckConstraint("machine_id > 0", name="ck_machine_id_positive"),
    CheckConstraint("substr(serial_no, 1, 3) = 'SN-'", name="ck_machine_serial_prefix"),
)

technician_t = Table(
    "technician",
    metadata,
    Column("technician_id", Integer, primary_key=True),
    Column("technician_name", String, nullable=False),
    CheckConstraint("technician_id > 0", name="ck_technician_id_positive"),
    CheckConstraint("length(trim(technician_name)) > 0", name="ck_technician_name_nonempty"),
)

part_t = Table(
    "part",
    metadata,
    Column("part_no", String, primary_key=True),
    Column("description", String, nullable=False),
    Column("unit_price", Numeric(9, 2), nullable=False),
    CheckConstraint("unit_price >= 0", name="ck_part_price_nonnegative"),
)

maint_job_t = Table(
    "maint_job",
    metadata,
    Column("job_id", Integer, primary_key=True),
    CheckConstraint("job_id > 0", name="ck_maint_job_id_positive"),
    Column(
        "machine_id",
        Integer,
        ForeignKey("machine.machine_id"),
        nullable=False,
    ),
    Column(
        "technician_id",
        Integer,
        ForeignKey("technician.technician_id"),
        nullable=False,
    ),
    Column("done_on", Date, nullable=False),
)

job_part_t = Table(
    "job_part",
    metadata,
    Column(
        "job_id",
        Integer,
        ForeignKey("maint_job.job_id"),
        primary_key=True,
    ),
    Column(
        "part_no",
        String,
        ForeignKey("part.part_no"),
        primary_key=True,
    ),
)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite://")
    metadata.create_all(engine)

    for table in (machine_t, technician_t, part_t, maint_job_t, job_part_t):
        print(str(CreateTable(table).compile(engine)).strip(), ";\n")
