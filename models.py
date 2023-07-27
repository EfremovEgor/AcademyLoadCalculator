from __future__ import annotations
import datetime
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, validator, Field


class Person(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    full_name: str
    birth_date: datetime.date = Field(default_factory=str)
    phone_number: str
    degree: str | None
    academic_title: str | None
    position: str
    rate: float
    subjects: list[Subject] | list = Field(default_factory=list)


class Position(BaseModel):
    position_name: str
    load: int
    salary: float


class Subject(BaseModel):
    name: str
    holding_type: Literal["Семинар", "Лабораторная работа", "Лекция"]
    course: int
    semester: int
    group_name: str
    total_time_for_group: int
    used: bool = False
    semester_duration: int
    study_level: Literal[
        "Бакалавриат", "Специалитет", "Магистратура", "Аспирантура"
    ] = "Магистратура"
    _subject_type: Literal[
        "Курсовые работы / проекты",
        "Базовая компонента",
        "Вариативная компонента",
        "Часть, формируемая участниками образовательных отношений",
        "Практики и НИР",
        "Государственная итоговая аттестация",
        "Факультатив",
    ]
    _department: str
    _credit: int


class PersonResponse(Person):
    load_from_rate: int
    salary_from_rate: float
    actual_load: tuple[float, float]
