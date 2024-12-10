#
# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
#
import re
import zipfile

from typing import List

from etptypes.energistics.etp.v12.datatypes.supported_protocol import (
    SupportedProtocol,
)
from etptypes.energistics.etp.v12.datatypes.supported_data_object import (
    SupportedDataObject,
)
from etptypes.energistics.etp.v12.datatypes.version import Version

import uuid
from datetime import datetime

from etpproto.messages import Message

from etptypes.energistics.etp.v12.datatypes.object.context_info import (
    ContextInfo,
)
from etptypes.energistics.etp.v12.datatypes.object.context_scope_kind import (
    ContextScopeKind,
)
from etptypes.energistics.etp.v12.datatypes.object.active_status_kind import (
    ActiveStatusKind,
)
from etptypes.energistics.etp.v12.datatypes.object.relationship_kind import (
    RelationshipKind,
)


from etptypes.energistics.etp.v12.protocol.dataspace.get_dataspaces import (
    GetDataspaces,
)
from etptypes.energistics.etp.v12.protocol.dataspace.delete_dataspaces import (
    DeleteDataspaces,
)
from etptypes.energistics.etp.v12.protocol.dataspace.put_dataspaces import (
    PutDataspaces,
)

from etptypes.energistics.etp.v12.protocol.core.request_session import (
    RequestSession,
)
from etptypes.energistics.etp.v12.protocol.core.close_session import (
    CloseSession,
)
from etptypes.energistics.etp.v12.protocol.discovery.get_resources import (
    GetResources,
)
from etptypes.energistics.etp.v12.protocol.store.put_data_objects import (
    PutDataObjects,
)
from etptypes.energistics.etp.v12.protocol.store.get_data_objects import (
    GetDataObjects,
)
from etptypes.energistics.etp.v12.datatypes.object.data_object import (
    DataObject,
)
from etptypes.energistics.etp.v12.datatypes.object.resource import Resource
from etptypes.energistics.etp.v12.datatypes.object.dataspace import Dataspace

# from etptypes.energistics.etp.v12.datatypes.uuid import to_Uuid, to_UUID

from etpproto.uri import *

from etpproto.connection import ETPConnection


etp_version = Version(major=1, minor=2, revision=0, patch=0)
local_protocols = [
    SupportedProtocol(
        protocol=0,
        protocolVersion=etp_version,
        role="server",
        protocolCapabilities={},
    ),
    SupportedProtocol(
        protocol=3,
        protocolVersion=etp_version,
        role="store",
        protocolCapabilities={},
    ),
]

supported_objects = [
    SupportedDataObject(
        qualifiedType="resqml20", dataObjectCapabilities={}  # ["resqml20"]
    )
]


requestSession_msg = Message.get_object_message(
    RequestSession(
        applicationName="Geosiris etp client",
        applicationVersion="0.0.1",
        clientInstanceId=uuid.uuid4(),
        requestedProtocols=local_protocols,
        supportedDataObjects=supported_objects,
        supportedCompression=["string"],
        supportedFormats=["xml"],
        currentDateTime=int(datetime.utcnow().timestamp()),
        # endpointCapabilities=ETPConnection.server_capabilities,
        endpointCapabilities={},
        earliest_retained_change_time=0,
    ),
    msg_id=1,
)


def request_session():
    return RequestSession(
        applicationName="Geosiris etp client",
        applicationVersion="0.0.1",
        clientInstanceId=uuid.uuid4(),
        requestedProtocols=local_protocols,
        supportedDataObjects=supported_objects,
        supportedCompression=["string"],
        supportedFormats=["xml"],
        currentDateTime=int(datetime.utcnow().timestamp()),
        endpointCapabilities={},
        earliest_retained_change_time=0,
    )


def get_scope(scope: str):
    if scope is not None:
        scope_lw = scope.lower()
        if "target" in scope_lw:
            if "self" in scope_lw:
                return ContextScopeKind.TARGETS_OR_SELF
            else:
                return ContextScopeKind.TARGETS
        elif "source" in scope_lw:
            if "self" in scope_lw:
                return ContextScopeKind.SOURCES_OR_SELF
            else:
                return ContextScopeKind.SOURCES
    return ContextScopeKind.SELF


def get_resouces(uri: str = "eml:///", depth: int = 1, scope=None):
    if not uri.startswith("eml:///"):
        uri = f"eml:///dataspace('{uri}')"
    return GetResources(
        context=ContextInfo(
            uri=uri,
            depth=depth,
            dataObjectTypes=[],
            navigableEdges=RelationshipKind.PRIMARY,
        ),
        scope=get_scope(scope),
        countObjects=False,
        storeLastWriteFilter=None,
        activeStatusFilter=ActiveStatusKind.INACTIVE,
        includeEdges=False,
    )


def get_dataspaces():
    return GetDataspaces()


def extractResqmlUuid(content: str):
    return findUuid(content)


XML_TYPE_REGXP = r"<([\w]+:)?([\w]+)"


def extractResqmlURI(content: str, dataspace_name: str = None):
    pattern = re.compile(XML_TYPE_REGXP)
    # print("PATT ", pattern)
    result = pattern.search(content)
    # print("result ", result)
    return (
        "eml:///"
        + (
            "dataspace('" + dataspace_name + "')/"
            if dataspace_name is not None
            else ""
        )
        + "resqml20."
        + result.group(2)
        + "("
        + extractResqmlUuid(content)
        + ")"
    )


def put_dataspace(dataspace_names: list):
    ds_map = {}
    for ds_name in dataspace_names:
        ds_map[str(len(ds_map))] = Dataspace(
            uri="eml:///dataspace('" + ds_name + "')"
            if "eml:///" not in ds_name
            else ds_name,
            store_last_write=0,
            store_created=0,
        )

    return PutDataspaces(dataspaces=ds_map)


def delete_dataspace(dataspace_names: str):
    ds_map = {}
    for ds_name in dataspace_names:
        ds_map[str(len(ds_map))] = (
            "eml:///dataspace('" + ds_name + "')"
            if "eml:///" not in ds_name
            else ds_name
        )
    return DeleteDataspaces(uris=ds_map)


def put_data_object_by_path(path: str, dataspace_name: str = None):
    result = []
    try:
        if path.endswith(".xml"):

            f = open(path)
            f_content = f.read()

            result.append(put_data_object(f_content, dataspace_name))
            f.close()
        elif path.endswith(".epc"):
            do_lst = {}
            zfile = zipfile.ZipFile(path, "r")
            for zinfo in zfile.infolist():
                if (
                    zinfo.filename.endswith(".xml")
                    and findUuid(zinfo.filename) != None
                ):
                    # print('%s (%s --> %s)' % (zinfo.filename, zinfo.file_size, zinfo.compress_size))
                    with zfile.open(zinfo.filename) as myfile:
                        do_lst[len(do_lst)] = _create_data_object(
                            myfile.read().decode("utf-8"), dataspace_name
                        )
            zfile.close()
            result.append(PutDataObjects(data_objects=do_lst))
        else:
            print("Unkown file type")
    except Exception as e:
        print("Except : ", e)

    return result


def _create_data_object(f_content: str, dataspace_name: str = None):
    uri = extractResqmlURI(f_content, dataspace_name)
    print("Sending data object at uri ", uri)
    real_uuid = uuid.UUID(extractResqmlUuid(f_content)).hex
    ressource = Resource(
        uri=uri,
        name=uri,  # + ".xml",
        source_count=0,
        target_count=0,
        last_changed=0,
        store_last_write=0,
        store_created=0,
        active_status=ActiveStatusKind.INACTIVE,
        alternate_uris=[],
        custom_data=[],
    )
    return DataObject(blob_id=real_uuid, resource=ressource, data=f_content)


def put_data_object(f_content: str, dataspace_name: str = None):
    uri = extractResqmlURI(f_content, dataspace_name)
    print("Sending data object at uri ", uri)
    real_uuid = uuid.UUID(extractResqmlUuid(f_content)).hex
    ressource = Resource(
        uri=uri,
        name=uri,  # + ".xml",
        source_count=0,
        target_count=0,
        last_changed=0,
        store_last_write=0,
        store_created=0,
        active_status=ActiveStatusKind.INACTIVE,
        alternate_uris=[],
        custom_data=[],
    )
    do = DataObject(blob_id=real_uuid, resource=ressource, data=f_content)
    return PutDataObjects(data_objects={"0": do})


def get_data_object(uris: List[str], format: str = "xml"):
    uris_dict = {}
    for num, u in enumerate(uris, start=1):
        uris_dict[num] = u
    return GetDataObjects(uris=uris_dict, format_=format)


def get_close_session(reason="We have finished"):
    return CloseSession(reason=reason)


#     ____        __        ___
#    / __ \____ _/ /_____ _/   |  ______________ ___  __
#   / / / / __ `/ __/ __ `/ /| | / ___/ ___/ __ `/ / / /
#  / /_/ / /_/ / /_/ /_/ / ___ |/ /  / /  / /_/ / /_/ /
# /_____/\__,_/\__/\__,_/_/  |_/_/  /_/   \__,_/\__, /
#                                              /____/

from etptypes.energistics.etp.v12.datatypes.data_array_types.data_array_identifier import (
    DataArrayIdentifier,
)
from etptypes.energistics.etp.v12.protocol.data_array.get_data_arrays import (
    GetDataArrays,
)


def get_data_array(uri: str, path_in_res: str):
    return GetDataArrays(
        data_arrays={
            "0": DataArrayIdentifier(uri=uri, path_in_resource=path_in_res)
        }
    )
