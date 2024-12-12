from agilicus.agilicus_api import (
    ResourceConfig,
)


def map_resource_published(mapping, published):
    if published is not None:
        config = mapping.spec.resource_config
        if config is None:
            config = ResourceConfig()
            mapping.spec.resource_config = config
        mapping.spec.resource_config["published"] = published
    return mapping
