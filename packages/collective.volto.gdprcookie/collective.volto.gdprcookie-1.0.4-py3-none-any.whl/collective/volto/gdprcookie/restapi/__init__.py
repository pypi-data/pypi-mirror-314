from plone.restapi.blocks import iter_block_transform_handlers
from plone.restapi.serializer.converters import json_compatible

import json


def parse_gdpr_blocks(context, data, transformer_interface):
    """
    Each text block is a slate block and we need to apply handlers to fix some things
    like internal links for example
    """
    if isinstance(data, str):
        data = json.loads(data)

    # fix internal links
    for text in data["text"].values():
        text = fix_text(
            context=context,
            value=text,
            transformer_interface=transformer_interface,
        )
    for type_label in ["technical", "profiling"]:
        cookie_type = data.get(type_label, {})
        if not cookie_type:
            continue
        for text in cookie_type["text"].values():
            text = fix_text(
                context=context,
                value=text,
                transformer_interface=transformer_interface,
            )
        for choice in cookie_type.get("choices", []):
            for text in choice.get("text", {}).values():
                text = fix_text(
                    context=context,
                    value=text,
                    transformer_interface=transformer_interface,
                )
    return json.dumps(json_compatible(data))


def fix_text(context, value, transformer_interface):
    """
    Create a fake block to be able to apply all handlers
    """
    if value.get("description", {}):
        fake_block = {"@type": "slate", "value": value["description"]}
        for handler in iter_block_transform_handlers(
            context, fake_block, transformer_interface
        ):
            fake_block = handler(fake_block)

        value["description"] = fake_block["value"]
    return value
