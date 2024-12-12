from pydantic import Field

from vbl_aquarium.utils.vbl_base_model import VBLBaseModel


class PinpointIdResponse(VBLBaseModel):
    """Response format for a pinpoint ID request.

    :param pinpoint_id: ID of the service.
    :type pinpoint_id: str
    :param is_requester: Whether the service is a requester.
    :type is_requester: bool
    """

    pinpoint_id: str = Field(min_length=8, max_length=8)
    is_requester: bool
