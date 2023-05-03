from enum import Enum


class CacheTag(Enum):
    GET_EVENTS_BY_RADIUS = "get_events_by_radius"
    GET_EVENTS_BY_QUERY = "get_events_by_query"
    GET_EVENT_LIST = "GET_EVENT_LIST"
