import enum


class RequestType(enum.Enum):
    Request = 1
    Original_Response = 2
    Replayed_Response = 3
