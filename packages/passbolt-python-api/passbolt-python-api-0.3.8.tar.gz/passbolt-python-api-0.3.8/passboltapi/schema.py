# Library Imports
from enum import Enum
from typing import List, Mapping, NamedTuple, Optional, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# User-Defined Structs
# > Passbolt types
PassboltFolderIdType: TypeAlias = str
PassboltResourceIdType: TypeAlias = str
PassboltResourceTypeIdType: TypeAlias = str
PassboltUserIdType: TypeAlias = str
PassboltRoleIdType: TypeAlias = str
PassboltOpenPgpKeyIdType: TypeAlias = str
PassboltGroupIdType: TypeAlias = str
PassboltSecretIdType: TypeAlias = str
PassboltPermissionIdType: TypeAlias = str

# refers to the response from passbolt which is a string representation of datetime
PassboltDateTimeType: TypeAlias = str
PassboltFavoriteDetailsType: TypeAlias = dict


class PassboltResourceType(Enum):
    PASSWORD = 1
    PASSWORD_WITH_DESCRIPTION = 2


class PassboltSecretTuple(NamedTuple):
    id: PassboltSecretIdType
    user_id: PassboltUserIdType
    resource_id: PassboltResourceIdType
    data: str
    created: PassboltDateTimeType
    modified: PassboltDateTimeType


class PassboltPermissionTuple(NamedTuple):
    id: PassboltPermissionIdType
    aco: Literal["User", "Group"]
    aco_foreign_key: Union[PassboltUserIdType, PassboltGroupIdType]
    aro: Literal["Resource", "Folder"]
    aro_foreign_key: Union[PassboltResourceIdType, PassboltFolderIdType]
    type: int
    created: PassboltDateTimeType
    modified: PassboltDateTimeType
    group: Union[None, "PassboltGroupTuple"] = None
    user: Union[None, "PassboltUserTuple"] = None


class PassboltOpenPgpKeyTuple(NamedTuple):
    id: PassboltOpenPgpKeyIdType
    armored_key: str
    created: PassboltDateTimeType
    key_created: PassboltDateTimeType
    bits: int
    deleted: bool
    modified: PassboltDateTimeType
    key_id: str
    fingerprint: str
    type: Literal["RSA", "ELG", "DSA", "ECDH", "ECDSA", "EDDSA"]
    expires: PassboltDateTimeType


class PassboltUserTuple(NamedTuple):
    id: PassboltUserIdType
    created: PassboltDateTimeType
    active: bool
    deleted: bool
    modified: PassboltDateTimeType
    username: str
    role_id: PassboltRoleIdType
    profile: dict
    last_logged_in: PassboltDateTimeType
    role: Optional[dict] = None
    gpgkey: Optional[PassboltOpenPgpKeyTuple] = None


class PassboltResourceTuple(NamedTuple):
    id: PassboltResourceIdType
    created: PassboltDateTimeType
    created_by: PassboltUserIdType
    deleted: bool
    description: str
    modified: PassboltDateTimeType
    modified_by: PassboltUserIdType
    name: str
    uri: str
    username: str
    resource_type_id: PassboltResourceIdType
    folder_parent_id: PassboltFolderIdType
    creator: Union[None, PassboltUserTuple] = None
    favorite: Union[None, PassboltFavoriteDetailsType] = None
    modifier: Union[None, PassboltUserTuple] = None
    permission: Union[PassboltPermissionTuple] = None


class PassboltResourceTypeTuple(NamedTuple):
    id: str
    slug: str
    name: str
    description: str
    definition: str
    created: str
    modified: str


class PassboltFolderTuple(NamedTuple):
    id: PassboltFolderIdType
    name: str
    created: PassboltDateTimeType
    modified: PassboltDateTimeType
    created_by: PassboltUserIdType
    modified_by: PassboltUserIdType
    folder_parent_id: PassboltFolderIdType
    personal: bool
    permissions: List[PassboltPermissionTuple] = []


class PassboltGroupTuple(NamedTuple):
    id: PassboltGroupIdType
    created: PassboltDateTimeType
    created_by: PassboltUserIdType
    deleted: bool
    modified: PassboltDateTimeType
    modified_by: PassboltUserIdType
    name: str
    groups_users: List[dict] = []


AllPassboltTupleTypes = Union[
    PassboltSecretTuple,
    PassboltPermissionTuple,
    PassboltResourceTuple,
    PassboltFolderTuple,
    PassboltGroupTuple,
    PassboltUserTuple,
    PassboltOpenPgpKeyTuple,
]


def constructor(
    _namedtuple: AllPassboltTupleTypes,
    renamed_fields: Union[None, dict] = None,
    filter_fields: bool = True,
    subconstructors: Union[None, dict] = None,
):
    def namedtuple_constructor(data: Union[Mapping, List[Mapping]]) -> Optional[List[AllPassboltTupleTypes]]:
        """Returns a namedtuple constructor function that can --
        1. Ingest dictionaries or list of dictionaries directly
        2. Renames field names from dict -> namedtuple
        3. Filters out dictionary keys that do not exist in namedtuple
        4. Can apply further constructors to subfields"""
        if data is None:
            return
        if data == []:
            return []

        # 1. ingest datatypes
        is_singleton = False
        if isinstance(data, dict):
            # if single, data is a singleton list
            data = [data]
            is_singleton = True
        elif isinstance(data, list):
            # if list, assert that all elements are dicts
            assert all(map(lambda datum: type(datum) == dict, data)), "All records must be dicts"
        else:
            raise ValueError(f"Data ingested by {_namedtuple} cannot be {type(data)}")

        # TODO: should the listcomps be made lazy?

        # 2. rename fields
        if renamed_fields:
            # make sure that all final fieldnames are present in the namedtuple
            assert not set(renamed_fields.values()).difference(_namedtuple._fields)
            data = [
                {(renamed_fields[k] if k in renamed_fields.keys() else k): v for k, v in datum.items()}
                for datum in data
            ]

        # 3. Filter extra fields not present in namedtuple definition
        if filter_fields:
            _ = data[0]
            data = [{k: v for k, v in datum.items() if k in _namedtuple._fields} for datum in data]

        # 4. [Composition] Apply constructors like this to individual fields
        if subconstructors:
            data = [
                {
                    k: (subconstructors[k](v) if k in subconstructors.keys() else v)
                    for k, v in datum.items()
                    if k in _namedtuple._fields
                }
                for datum in data
            ]
        # handle singleton lists
        if is_singleton:
            return _namedtuple(**data[0])
        return [_namedtuple(**datum) for datum in data]

    return namedtuple_constructor
