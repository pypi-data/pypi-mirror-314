from typing import Callable


def get_many_entries(
    api_func: Callable,
    response_list_key,
    page_size=100,
    maximum=None,
    page_callback=None,
    **kwargs,
):
    """Implements the generic pagination strategy
    :param agilicus_api api: api used to get the object
    :param string response_list_key: key to get the value/list from the returned object
    :param int page_size: size of the pagination
    :param int maximum: the maximum number of objects to return. Returns all if None

    Assumes page_at_id is in the kwargs
    """
    if "limit" in kwargs:
        del kwargs["limit"]
    kwargs["limit"] = page_size
    if "page_at_id" not in kwargs:
        kwargs["page_at_id"] = ""

    list_resp = api_func(**kwargs)
    retval = list_resp.get(response_list_key) or []
    # loop quits when the list is < the page_size
    while len(list_resp.get(response_list_key, [])) >= page_size and _list_at_max_size(
        len(retval), maximum
    ):
        page_at_id = list_resp.get("page_at_id", None)
        if page_at_id is None:
            raise Exception(
                "page_at_id cannot be None for pagination to continue processing"
            )
        kwargs["page_at_id"] = list_resp.get("page_at_id", None)
        list_resp = api_func(**kwargs)
        retval.extend(list_resp.get(response_list_key, []))
        if page_callback:
            page_callback()
    return _get_max_retval(retval, maximum)


def _list_at_max_size(length, maximum):
    if maximum is None:
        return True
    return length < maximum


def _get_max_retval(retval, maximum):
    if maximum is None:
        return retval
    return retval[:maximum]
