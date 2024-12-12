from agilicus_api import (
    Message,
    MessageAction,
    MessageAddress,
    MessageClass,
    MessageType,
    MessageSendRequest,
    MessageSendItem,
    MessageTagName,
    MessageTag,
    MessagesBulkDeleteRequest,
)

from . import context
from . import input_helpers
from .output.json import convert_to_json
from .output.table import (
    format_table,
    metadata_column,
    spec_column,
    status_column,
)


def list_message_endpoints(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    if user_id:
        kwargs["user_id"] = user_id
    results = apiclient.messages_api.list_message_endpoints(**kwargs)
    return results.messages


def format_message_endpoints(ctx, details):
    columns = [
        metadata_column("message_endpoint_id"),
        metadata_column("user_id", "User ID"),
        spec_column("endpoint_type", "Type"),
        spec_column("nickname", "Nickname"),
        spec_column("address", "Address"),
    ]

    return format_table(ctx, details, columns)


def delete_message_endpoint(ctx, message_endpoint_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    resp = apiclient.messages_api.delete_message_endpoint(message_endpoint_id)
    return resp


def get_message_endpoint(ctx, message_endpoint_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    result = apiclient.messages_api.get_message_endpoint(message_endpoint_id, **kwargs)
    return result


def update_message_endpoint(ctx, user_id, message_endpoint_id, enabled=None, **kwargs):
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    endpoint = apiclient.messages_api.get_message_endpoint(
        user_id=user_id, message_endpoint_id=message_endpoint_id
    )

    if enabled is not None:
        endpoint.spec.enabled = enabled

    return apiclient.messages_api.replace_message_endpoint(message_endpoint_id, endpoint)


def send_message(
    ctx,
    user_id,
    text,
    org_id=None,
    message_class=None,
    message_type=None,
    sub_header=None,
    approve_uri=None,
    reject_uri=None,
    tag=None,
    **kwargs,
):
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id, **kwargs)
    kwargs = input_helpers.strip_none(kwargs)
    message = Message(text=text, **kwargs)
    if message_class is not None:
        message.message_class = MessageClass(message_class)
    if message_type is not None:
        message.message_type = MessageType(message_type)

    message.actions = []
    if approve_uri is not None:
        message.actions.append(MessageAction(title="approve", uri=approve_uri))

    if reject_uri is not None:
        message.actions.append(MessageAction(title="reject", uri=reject_uri))

    if tag is not None:
        message.tag = make_message_tag(tag, org_id)

    address = MessageAddress(user_id=user_id)
    if org_id is not None:
        address.org_id = org_id
    else:
        address.org_id = input_helpers.get_org_from_input_or_ctx(ctx, **kwargs)
    item = MessageSendItem(message=message, addresses=[address], ephemeral=False)
    req = MessageSendRequest(messages=[item])

    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.messages_api.create_routed_message(req)


def make_message_tag(tag, org_id):
    if tag is None:
        return None
    result = MessageTag(MessageTagName(tag))
    if org_id is not None:
        result.org_id = org_id
    return result


def list_inbox_items(ctx, user_id, **kwargs):
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = input_helpers.strip_none(kwargs)
    return apiclient.messages_api.list_inbox_items(user_id=user_id, **kwargs)


def update_inbox_item(ctx, user_id, inbox_item_id, has_been_read=None, **kwargs):
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    item = apiclient.messages_api.get_inbox_item(
        user_id=user_id, inbox_item_id=inbox_item_id
    )
    if has_been_read is not None:
        item.spec.has_been_read = has_been_read
    return apiclient.messages_api.replace_inbox_item(
        inbox_item=item, user_id=user_id, inbox_item_id=inbox_item_id
    )


def bulk_delete_messages(ctx, tag, org_id, **kwargs):
    req = MessagesBulkDeleteRequest(make_message_tag(tag, org_id))
    apiclient = context.get_apiclient_from_ctx(ctx)
    resp = apiclient.messages_api.bulk_delete_messages(req)
    return resp


def format_inbox_items_response(ctx, response):
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        metadata_column("org_id"),
        spec_column("has_been_read", "read"),
        status_column("message.message_class", "class"),
        status_column("message.message_type", "type"),
        status_column("message.title", "title"),
        status_column("message.expiry_date", "expiry"),
    ]
    if context.output_json(ctx):
        return convert_to_json(ctx, response.to_dict())

    return format_table(ctx, response.inbox_items, columns)
