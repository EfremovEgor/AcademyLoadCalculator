import sys
from io import StringIO

if sys.stdout is None:
    sys.stdout = StringIO()
if sys.stderr is None:
    sys.stderr = StringIO()
import eel
import json
import models
import pydantic_core
from utils import (
    CWD,
    DATA_FOLDER,
    append_persons_to_file,
    get_person_responses,
    get_data_by_class,
    response_from_model,
    override_models_file,
)
import utils
from uuid import UUID

eel.init("static_web_folder", allowed_extensions=[".js", ".html"])


@eel.expose
def get_positions() -> list[dict]:
    return response_from_model(get_data_by_class(models.Position))


@eel.expose
def get_subjects() -> list[dict]:
    return response_from_model(
        sorted(get_data_by_class(models.Subject), key=lambda a: a.name)
    )


@eel.expose
def get_subjects_by_field(fields: list[str], values: list[str]) -> list[dict]:
    return response_from_model(
        sorted(
            [
                item
                for item in get_data_by_class(models.Subject)
                if all(
                    [
                        str(getattr(item, field)) == str(values[i])
                        for i, field in enumerate(fields)
                    ]
                )
            ],
            key=lambda a: a.name,
        )
    )


@eel.expose
def get_person_by_uuid(uuid: models.UUID) -> models.PersonResponse:
    for person in get_person_responses():
        if str(person.uuid) == uuid:
            return response_from_model(person)


@eel.expose
def delete_person_by_uuid(uuid: models.UUID) -> models.PersonResponse:
    data = get_person_responses()
    override_models_file(
        [person for person in data if str(person.uuid) != uuid], models.Person
    )


@eel.expose
def override_person_with_uuid(person: models.Person) -> None:
    person = models.Person(**person)

    data = get_person_responses()
    for i in range(len(data)):
        if str(data[i].uuid) == str(person.uuid):
            data[i] = person

    override_models_file(data, models.Person)


@eel.expose
def save_person(data: models.Person) -> str | None:
    try:
        temp_data = dict(data)
        data = models.Person(**temp_data)
    except pydantic_core._pydantic_core.ValidationError as ex:
        return json.loads(ex.json())
    append_persons_to_file([data])


@eel.expose
def get_persons() -> list[models.PersonResponse] | list:
    return response_from_model(get_person_responses())


@eel.expose
def get_unique_subjects_by_type(study_level: str) -> list[dict]:
    data = utils.get_unique_subjects_by_type(study_level)
    # for key, value in data.items():
    #     data[key] = [response_from_model(item) for item in value]
    return data


@eel.expose
def get_subjects_response_by_groups(study_level: str, name: str) -> dict:
    data = utils.get_subjects_response_by_groups(study_level, name)
    for key, value in data.items():
        data[key] = sorted(
            [response_from_model(item) for item in value],
            key=lambda a: a["holding_type"],
        )
    return data


eel.start(
    "index.html",
    shutdown_delay=1,
    mode="chrome",
)
