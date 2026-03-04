from os import getenv

from kiota_abstractions.authentication.anonymous_authentication_provider import (
    AnonymousAuthenticationProvider,
)
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from kiota_serialization_json.json_serialization_writer import JsonSerializationWriter

from generated.ap_explanation.ap_explanation_client import ApExplanationClient
from generated.ap_explanation.models.managed_provenance_task_response import (
    ManagedProvenanceTaskResponse,
)
from generated.ap_explanation.models.pg_json import PgJson
from generated.ap_explanation.models.task_status_response import TaskStatusResponse

AP_MANAGEMENT_URL = getenv("AP_MANAGEMENT_URL", "http://ap-explanation:5000")


def _create_adapter(base_url: str) -> HttpxRequestAdapter:
    adapter = HttpxRequestAdapter(AnonymousAuthenticationProvider())
    adapter.base_url = base_url
    return adapter


def get_provenance_client() -> ApExplanationClient:
    return ApExplanationClient(_create_adapter(AP_MANAGEMENT_URL))


async def compute_provenance_async(body: PgJson) -> str:
    client = get_provenance_client()
    res = await client.api.v1.aps.explanation.post(body=body)
    return res.task_id


async def poll_for_provenance(task_id: str) -> TaskStatusResponse:
    client = get_provenance_client()
    while True:
        # NOTE : the "by_semiring_name_id" is a gneration error of the kiota codegen, it should be "by_task_id"
        res = await client.api.v1.aps.explanation.by_semiring_name_id(task_id).get()
        if res.status in ("success", "failure", "revoked"):
            return res


def serialize(model) -> dict:
    writer = JsonSerializationWriter()
    model.serialize(writer)
    return writer.get_serialized_content().decode("utf-8")
