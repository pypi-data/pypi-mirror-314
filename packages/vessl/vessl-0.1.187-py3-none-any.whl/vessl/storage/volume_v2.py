from typing import Optional

from openapi_client import ProtoTag, ResponseVolumeV2Info, VolumeV2CreateAPIInput
from vessl import vessl_api
from vessl.organization import _get_organization_name


def list_volumes(
    storage_name: str, keyword: Optional[str] = None, **kwargs
) -> list[ResponseVolumeV2Info]:
    """List volumes in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        storage_name: name of the storage
        keyword: optional search keyword

    Example:
        ```python
        vessl.storage.list_volumes(storage_name="my-storage")
        ```
    """
    query_keys = {"limit", "offset"}
    query_kwargs = {k: v for k, v in kwargs.items() if k in query_keys}

    return vessl_api.volume_v2_list_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        keyword=keyword,
        **query_kwargs,
    ).results


def create_volume(name: str, storage_name: str, tags: tuple[str, ...] = (), **kwargs):
    """Create volume in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        name: The name of the volume.
        storage_name: The name of the storage.
        tags: The tags of the volume.

    Example:
        ```python
        vessl.storage.create_volume(
            name="my-volume",
            storage_name="my-storage",
            tags=("my-tag1", "my-tag2"),
        )
        ```
    """
    vessl_api.volume_v2_create_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        volume_v2_create_api_input=VolumeV2CreateAPIInput(
            volume_name=name,
            tags=[ProtoTag(name=tag) for tag in tags],
        ),
    )


def delete_volume(name: str, storage_name: str, **kwargs):
    """Delete volume in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        name: The name of the volume.
        storage_name: The name of the storage.

    Example:
        ```python
        vessl.storage.delete_volume(name="my-volume", storage_name="my-storage")
        ```
    """
    vessl_api.volume_v2_delete_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        volume_name=name,
    )
