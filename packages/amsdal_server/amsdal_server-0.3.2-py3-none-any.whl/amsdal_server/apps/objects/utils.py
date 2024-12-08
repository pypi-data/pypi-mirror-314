from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import Versions


def apply_version_to_address(
    address: Address,
    version_id: str | None,
    *,
    all_versions: bool = False,
) -> Address:
    object_version: str | Versions
    class_version: str | Versions

    if all_versions:
        object_version = Versions.ALL
        class_version = Versions.ALL
    elif version_id:
        object_version = version_id or address.object_version
        class_version = address.class_version
    else:
        object_version = Versions.LATEST
        class_version = Versions.LATEST

    address.object_version = object_version
    address.class_version = class_version

    return address
