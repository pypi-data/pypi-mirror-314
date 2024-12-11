r'''
# `data_databricks_share_pluginframework`

Refer to the Terraform Registry for docs: [`data_databricks_share_pluginframework`](https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataDatabricksSharePluginframework(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframework",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework databricks_share_pluginframework}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        object: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObject", typing.Dict[builtins.str, typing.Any]]]]] = None,
        owner: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[builtins.str] = None,
        storage_root: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[jsii.Number] = None,
        updated_by: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework databricks_share_pluginframework} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#comment DataDatabricksSharePluginframework#comment}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_at DataDatabricksSharePluginframework#created_at}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_by DataDatabricksSharePluginframework#created_by}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.
        :param object: object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#object DataDatabricksSharePluginframework#object}
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#owner DataDatabricksSharePluginframework#owner}.
        :param storage_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_location DataDatabricksSharePluginframework#storage_location}.
        :param storage_root: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_root DataDatabricksSharePluginframework#storage_root}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_at DataDatabricksSharePluginframework#updated_at}.
        :param updated_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_by DataDatabricksSharePluginframework#updated_by}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9957c10f0c58d9f2234383a786572860e109bbdfbf6df9108796a7f160e5695a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatabricksSharePluginframeworkConfig(
            comment=comment,
            created_at=created_at,
            created_by=created_by,
            name=name,
            object=object,
            owner=owner,
            storage_location=storage_location,
            storage_root=storage_root,
            updated_at=updated_at,
            updated_by=updated_by,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatabricksSharePluginframework resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatabricksSharePluginframework to import.
        :param import_from_id: The id of the existing DataDatabricksSharePluginframework that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatabricksSharePluginframework to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b02abe38806d258e6d3a3dffb53f755f9d817eb75f807ff16ea52837822b2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putObject")
    def put_object(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObject", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb50014116691f72a623d8db67d798df7b6d74650fe724b3084ce9a0b65ccff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putObject", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetCreatedBy")
    def reset_created_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedBy", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetObject")
    def reset_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObject", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetStorageLocation")
    def reset_storage_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageLocation", []))

    @jsii.member(jsii_name="resetStorageRoot")
    def reset_storage_root(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageRoot", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetUpdatedBy")
    def reset_updated_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedBy", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> "DataDatabricksSharePluginframeworkObjectList":
        return typing.cast("DataDatabricksSharePluginframeworkObjectList", jsii.get(self, "object"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAtInput")
    def created_at_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "createdAtInput"))

    @builtins.property
    @jsii.member(jsii_name="createdByInput")
    def created_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdByInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObject"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObject"]]], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationInput")
    def storage_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageRootInput")
    def storage_root_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageRootInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedByInput")
    def updated_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038100539e15ff062f8316e7a3d382bfd551aaabecad5d8168c466ca6afc5c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @created_at.setter
    def created_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d06d17c179e8fca4f4711e45fdd01d28481422f4df0156cccc727011728f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @created_by.setter
    def created_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da369dd6def6d17db97d6fee640db7c35d4a48513dfe5117220dd2acb8ebfb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a301efe9eae5ba297fff0708546d90e69352ff2c2ffa0aee962a32d373666070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b187c4a3928a7223b7871353b91105ecb36fe91bab38333bf8e21c4050c9445c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageLocation")
    def storage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageLocation"))

    @storage_location.setter
    def storage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adee1c2f2d2f5ba052f5f26d4635fbf18820d145276271d1adf5d648c00a0949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageRoot")
    def storage_root(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageRoot"))

    @storage_root.setter
    def storage_root(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ff99cd5846b6021f04803a63f709a36c69ce4b6f3e9895d4674fbcc235654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageRoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updatedAt"))

    @updated_at.setter
    def updated_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cc2122c30dab1a39fafb3e9144fb0c88fd474d7b21d7a75bc0392cb6e70fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedBy")
    def updated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedBy"))

    @updated_by.setter
    def updated_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5f2a2ad58bc273e539f9e620507c3bf06636c978fd209c7d584dcf9d436b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedBy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "comment": "comment",
        "created_at": "createdAt",
        "created_by": "createdBy",
        "name": "name",
        "object": "object",
        "owner": "owner",
        "storage_location": "storageLocation",
        "storage_root": "storageRoot",
        "updated_at": "updatedAt",
        "updated_by": "updatedBy",
    },
)
class DataDatabricksSharePluginframeworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        object: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObject", typing.Dict[builtins.str, typing.Any]]]]] = None,
        owner: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[builtins.str] = None,
        storage_root: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[jsii.Number] = None,
        updated_by: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#comment DataDatabricksSharePluginframework#comment}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_at DataDatabricksSharePluginframework#created_at}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_by DataDatabricksSharePluginframework#created_by}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.
        :param object: object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#object DataDatabricksSharePluginframework#object}
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#owner DataDatabricksSharePluginframework#owner}.
        :param storage_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_location DataDatabricksSharePluginframework#storage_location}.
        :param storage_root: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_root DataDatabricksSharePluginframework#storage_root}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_at DataDatabricksSharePluginframework#updated_at}.
        :param updated_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_by DataDatabricksSharePluginframework#updated_by}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327ebd313600f2fd482292bf6e59521307b0d273955b6525c5f4a6a8d67c2669)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument storage_root", value=storage_root, expected_type=type_hints["storage_root"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument updated_by", value=updated_by, expected_type=type_hints["updated_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if comment is not None:
            self._values["comment"] = comment
        if created_at is not None:
            self._values["created_at"] = created_at
        if created_by is not None:
            self._values["created_by"] = created_by
        if name is not None:
            self._values["name"] = name
        if object is not None:
            self._values["object"] = object
        if owner is not None:
            self._values["owner"] = owner
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if storage_root is not None:
            self._values["storage_root"] = storage_root
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if updated_by is not None:
            self._values["updated_by"] = updated_by

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#comment DataDatabricksSharePluginframework#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_at DataDatabricksSharePluginframework#created_at}.'''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#created_by DataDatabricksSharePluginframework#created_by}.'''
        result = self._values.get("created_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObject"]]]:
        '''object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#object DataDatabricksSharePluginframework#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObject"]]], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#owner DataDatabricksSharePluginframework#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_location DataDatabricksSharePluginframework#storage_location}.'''
        result = self._values.get("storage_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_root(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#storage_root DataDatabricksSharePluginframework#storage_root}.'''
        result = self._values.get("storage_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_at DataDatabricksSharePluginframework#updated_at}.'''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def updated_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#updated_by DataDatabricksSharePluginframework#updated_by}.'''
        result = self._values.get("updated_by")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksSharePluginframeworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObject",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "added_at": "addedAt",
        "added_by": "addedBy",
        "cdf_enabled": "cdfEnabled",
        "comment": "comment",
        "content": "content",
        "data_object_type": "dataObjectType",
        "effective_cdf_enabled": "effectiveCdfEnabled",
        "effective_history_data_sharing_status": "effectiveHistoryDataSharingStatus",
        "effective_shared_as": "effectiveSharedAs",
        "effective_start_version": "effectiveStartVersion",
        "history_data_sharing_status": "historyDataSharingStatus",
        "partition": "partition",
        "shared_as": "sharedAs",
        "start_version": "startVersion",
        "status": "status",
        "string_shared_as": "stringSharedAs",
    },
)
class DataDatabricksSharePluginframeworkObject:
    def __init__(
        self,
        *,
        name: builtins.str,
        added_at: typing.Optional[jsii.Number] = None,
        added_by: typing.Optional[builtins.str] = None,
        cdf_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comment: typing.Optional[builtins.str] = None,
        content: typing.Optional[builtins.str] = None,
        data_object_type: typing.Optional[builtins.str] = None,
        effective_cdf_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        effective_history_data_sharing_status: typing.Optional[builtins.str] = None,
        effective_shared_as: typing.Optional[builtins.str] = None,
        effective_start_version: typing.Optional[jsii.Number] = None,
        history_data_sharing_status: typing.Optional[builtins.str] = None,
        partition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObjectPartition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shared_as: typing.Optional[builtins.str] = None,
        start_version: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        string_shared_as: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.
        :param added_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#added_at DataDatabricksSharePluginframework#added_at}.
        :param added_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#added_by DataDatabricksSharePluginframework#added_by}.
        :param cdf_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#cdf_enabled DataDatabricksSharePluginframework#cdf_enabled}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#comment DataDatabricksSharePluginframework#comment}.
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#content DataDatabricksSharePluginframework#content}.
        :param data_object_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#data_object_type DataDatabricksSharePluginframework#data_object_type}.
        :param effective_cdf_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_cdf_enabled DataDatabricksSharePluginframework#effective_cdf_enabled}.
        :param effective_history_data_sharing_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_history_data_sharing_status DataDatabricksSharePluginframework#effective_history_data_sharing_status}.
        :param effective_shared_as: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_shared_as DataDatabricksSharePluginframework#effective_shared_as}.
        :param effective_start_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_start_version DataDatabricksSharePluginframework#effective_start_version}.
        :param history_data_sharing_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#history_data_sharing_status DataDatabricksSharePluginframework#history_data_sharing_status}.
        :param partition: partition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#partition DataDatabricksSharePluginframework#partition}
        :param shared_as: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#shared_as DataDatabricksSharePluginframework#shared_as}.
        :param start_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#start_version DataDatabricksSharePluginframework#start_version}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#status DataDatabricksSharePluginframework#status}.
        :param string_shared_as: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#string_shared_as DataDatabricksSharePluginframework#string_shared_as}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c45169444cfc8aba52f349d4bd54c95ed004e21bf30e1ffbd2449d9f046ed21)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument added_at", value=added_at, expected_type=type_hints["added_at"])
            check_type(argname="argument added_by", value=added_by, expected_type=type_hints["added_by"])
            check_type(argname="argument cdf_enabled", value=cdf_enabled, expected_type=type_hints["cdf_enabled"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument data_object_type", value=data_object_type, expected_type=type_hints["data_object_type"])
            check_type(argname="argument effective_cdf_enabled", value=effective_cdf_enabled, expected_type=type_hints["effective_cdf_enabled"])
            check_type(argname="argument effective_history_data_sharing_status", value=effective_history_data_sharing_status, expected_type=type_hints["effective_history_data_sharing_status"])
            check_type(argname="argument effective_shared_as", value=effective_shared_as, expected_type=type_hints["effective_shared_as"])
            check_type(argname="argument effective_start_version", value=effective_start_version, expected_type=type_hints["effective_start_version"])
            check_type(argname="argument history_data_sharing_status", value=history_data_sharing_status, expected_type=type_hints["history_data_sharing_status"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument shared_as", value=shared_as, expected_type=type_hints["shared_as"])
            check_type(argname="argument start_version", value=start_version, expected_type=type_hints["start_version"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument string_shared_as", value=string_shared_as, expected_type=type_hints["string_shared_as"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if added_at is not None:
            self._values["added_at"] = added_at
        if added_by is not None:
            self._values["added_by"] = added_by
        if cdf_enabled is not None:
            self._values["cdf_enabled"] = cdf_enabled
        if comment is not None:
            self._values["comment"] = comment
        if content is not None:
            self._values["content"] = content
        if data_object_type is not None:
            self._values["data_object_type"] = data_object_type
        if effective_cdf_enabled is not None:
            self._values["effective_cdf_enabled"] = effective_cdf_enabled
        if effective_history_data_sharing_status is not None:
            self._values["effective_history_data_sharing_status"] = effective_history_data_sharing_status
        if effective_shared_as is not None:
            self._values["effective_shared_as"] = effective_shared_as
        if effective_start_version is not None:
            self._values["effective_start_version"] = effective_start_version
        if history_data_sharing_status is not None:
            self._values["history_data_sharing_status"] = history_data_sharing_status
        if partition is not None:
            self._values["partition"] = partition
        if shared_as is not None:
            self._values["shared_as"] = shared_as
        if start_version is not None:
            self._values["start_version"] = start_version
        if status is not None:
            self._values["status"] = status
        if string_shared_as is not None:
            self._values["string_shared_as"] = string_shared_as

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def added_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#added_at DataDatabricksSharePluginframework#added_at}.'''
        result = self._values.get("added_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def added_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#added_by DataDatabricksSharePluginframework#added_by}.'''
        result = self._values.get("added_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdf_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#cdf_enabled DataDatabricksSharePluginframework#cdf_enabled}.'''
        result = self._values.get("cdf_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#comment DataDatabricksSharePluginframework#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#content DataDatabricksSharePluginframework#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_object_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#data_object_type DataDatabricksSharePluginframework#data_object_type}.'''
        result = self._values.get("data_object_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_cdf_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_cdf_enabled DataDatabricksSharePluginframework#effective_cdf_enabled}.'''
        result = self._values.get("effective_cdf_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def effective_history_data_sharing_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_history_data_sharing_status DataDatabricksSharePluginframework#effective_history_data_sharing_status}.'''
        result = self._values.get("effective_history_data_sharing_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_shared_as(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_shared_as DataDatabricksSharePluginframework#effective_shared_as}.'''
        result = self._values.get("effective_shared_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_start_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#effective_start_version DataDatabricksSharePluginframework#effective_start_version}.'''
        result = self._values.get("effective_start_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def history_data_sharing_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#history_data_sharing_status DataDatabricksSharePluginframework#history_data_sharing_status}.'''
        result = self._values.get("history_data_sharing_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartition"]]]:
        '''partition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#partition DataDatabricksSharePluginframework#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartition"]]], result)

    @builtins.property
    def shared_as(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#shared_as DataDatabricksSharePluginframework#shared_as}.'''
        result = self._values.get("shared_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#start_version DataDatabricksSharePluginframework#start_version}.'''
        result = self._values.get("start_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#status DataDatabricksSharePluginframework#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def string_shared_as(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#string_shared_as DataDatabricksSharePluginframework#string_shared_as}.'''
        result = self._values.get("string_shared_as")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksSharePluginframeworkObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksSharePluginframeworkObjectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298807ad629b11b40b4486efa7f8f7bdfc31450bffa743afe38155447263cfe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksSharePluginframeworkObjectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b197884d868082e1a3fbb84ee8b820c23af5dce6bf868e4591ae8dd172e039)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksSharePluginframeworkObjectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c758deed3c709dd6742d3fe8f1ac987b7abca5892abbcb15bf68a154d342de21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90aad071efabdac7494e83ea4fd24e54649edd75c478a2e20b1e14eb04129059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48320525a6fc090978ef96a15fcac92f09dc6e5db1dff2ddb608f9970717bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObject]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObject]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee121a094cdab2821bf012a29123d98ee9da85ecc35b8bc2ef0a6a337a7b65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksSharePluginframeworkObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc7211e885605a1dc897727e49dde210aedd41551eaf973d66650b063f9f661)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPartition")
    def put_partition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObjectPartition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa73e91e77a01f941c9b75a13ef2c7c31f709f06fa582a66b602cb65553528d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPartition", [value]))

    @jsii.member(jsii_name="resetAddedAt")
    def reset_added_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddedAt", []))

    @jsii.member(jsii_name="resetAddedBy")
    def reset_added_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddedBy", []))

    @jsii.member(jsii_name="resetCdfEnabled")
    def reset_cdf_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdfEnabled", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetDataObjectType")
    def reset_data_object_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataObjectType", []))

    @jsii.member(jsii_name="resetEffectiveCdfEnabled")
    def reset_effective_cdf_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveCdfEnabled", []))

    @jsii.member(jsii_name="resetEffectiveHistoryDataSharingStatus")
    def reset_effective_history_data_sharing_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveHistoryDataSharingStatus", []))

    @jsii.member(jsii_name="resetEffectiveSharedAs")
    def reset_effective_shared_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveSharedAs", []))

    @jsii.member(jsii_name="resetEffectiveStartVersion")
    def reset_effective_start_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveStartVersion", []))

    @jsii.member(jsii_name="resetHistoryDataSharingStatus")
    def reset_history_data_sharing_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHistoryDataSharingStatus", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetSharedAs")
    def reset_shared_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedAs", []))

    @jsii.member(jsii_name="resetStartVersion")
    def reset_start_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartVersion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetStringSharedAs")
    def reset_string_shared_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringSharedAs", []))

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> "DataDatabricksSharePluginframeworkObjectPartitionList":
        return typing.cast("DataDatabricksSharePluginframeworkObjectPartitionList", jsii.get(self, "partition"))

    @builtins.property
    @jsii.member(jsii_name="addedAtInput")
    def added_at_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="addedByInput")
    def added_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addedByInput"))

    @builtins.property
    @jsii.member(jsii_name="cdfEnabledInput")
    def cdf_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cdfEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="dataObjectTypeInput")
    def data_object_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataObjectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveCdfEnabledInput")
    def effective_cdf_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "effectiveCdfEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveHistoryDataSharingStatusInput")
    def effective_history_data_sharing_status_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveHistoryDataSharingStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveSharedAsInput")
    def effective_shared_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveSharedAsInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveStartVersionInput")
    def effective_start_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "effectiveStartVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="historyDataSharingStatusInput")
    def history_data_sharing_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "historyDataSharingStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartition"]]], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedAsInput")
    def shared_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedAsInput"))

    @builtins.property
    @jsii.member(jsii_name="startVersionInput")
    def start_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="stringSharedAsInput")
    def string_shared_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringSharedAsInput"))

    @builtins.property
    @jsii.member(jsii_name="addedAt")
    def added_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addedAt"))

    @added_at.setter
    def added_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ab40291eca409cda5a83b92c85f88b312701d185f45745087b331b4d10ff2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addedBy")
    def added_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addedBy"))

    @added_by.setter
    def added_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa736c86cfe0470f90500d24fb4f0d2265c15caacf972d57cbdc6973dc388ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addedBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdfEnabled")
    def cdf_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cdfEnabled"))

    @cdf_enabled.setter
    def cdf_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acf1e387e96de00cc8f41589d425cdd49ec2e5399b40ea508f63173e595c73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdfEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a44812d1cdc2cb76bd164a61cc4caa373cfa40c63e9de53affc9734bb5b272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f45b3e608149638cc53d7ec6c37e28a0783e8e8690b83dd3cdd6e9618d4ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataObjectType")
    def data_object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataObjectType"))

    @data_object_type.setter
    def data_object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844db3c0a5a96e0d8a6c79c17f3f875c0a7b97bbb910e6290c18d31ee39a21b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataObjectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveCdfEnabled")
    def effective_cdf_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "effectiveCdfEnabled"))

    @effective_cdf_enabled.setter
    def effective_cdf_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851b0722688aa10c92600e7d03896fe0860df987a13931b66f4562cef14af269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveCdfEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveHistoryDataSharingStatus")
    def effective_history_data_sharing_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveHistoryDataSharingStatus"))

    @effective_history_data_sharing_status.setter
    def effective_history_data_sharing_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac3bb74d75c4240e6bfc73d890b76de322073a7617b5e935e6151e8b57ca609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveHistoryDataSharingStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveSharedAs")
    def effective_shared_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveSharedAs"))

    @effective_shared_as.setter
    def effective_shared_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be09996a1c75b9e1a448fcabf2dba1bb3a1b08f30ca0f5a84a2f94785d10c2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveSharedAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveStartVersion")
    def effective_start_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "effectiveStartVersion"))

    @effective_start_version.setter
    def effective_start_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55635f64dcce69a4d7317e3b572254e9046d282af90b28206241cb3daa0ce96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveStartVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="historyDataSharingStatus")
    def history_data_sharing_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "historyDataSharingStatus"))

    @history_data_sharing_status.setter
    def history_data_sharing_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862b9adefccc062b5a1cb934cc501ff3858b827c065c5a9dd46e3c8ea2cbe79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "historyDataSharingStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c94d56f5eaa9510b3a06c90c197703d7de25deb04e336c1fd90257c4a0b4a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedAs")
    def shared_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedAs"))

    @shared_as.setter
    def shared_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d86334ba2c3d203e33620235edcd8edb1186f6d20194c25b80bb2fc2a9b1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startVersion")
    def start_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startVersion"))

    @start_version.setter
    def start_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf26547e46d37776f3408dd146ed9df2beccf39cfbdef1c6ab6989cb4b2394e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72671c7f7fc4be369450eb51fbef4440a766a8f75f2d11de6c680e99debf0b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringSharedAs")
    def string_shared_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringSharedAs"))

    @string_shared_as.setter
    def string_shared_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3c59a0f7d3e2a485c4bfa6c21188d79169a2724c8d547380ef5b82f47a1807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringSharedAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObject]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObject]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObject]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad3a6c2c8d308429f06ded6a71909279b3568b641d129aa2e8b239c92e02d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartition",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class DataDatabricksSharePluginframeworkObjectPartition:
    def __init__(
        self,
        *,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObjectPartitionValue", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#value DataDatabricksSharePluginframework#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f065bf5f66d207d2fcdd39c5fdc17e255c8e8125bfbaa087b2d850cb9aec8b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartitionValue"]]]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#value DataDatabricksSharePluginframework#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartitionValue"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksSharePluginframeworkObjectPartition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksSharePluginframeworkObjectPartitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartitionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedf64285916f7e1b9b86257b053c430c82dfa7e041627feb77e3e0f5bf1e466)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksSharePluginframeworkObjectPartitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404858107184d297eaf03058999712a29d9676a0ccbea468a5b838ccd4b39000)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksSharePluginframeworkObjectPartitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42fc54c24998cf2d665ac16b8d08e5c7f3e61e4e839871fa9ff09f06efa955e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f65db254dc734075027e356d7926254734b553edc4ade63e940b0a13a62f40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e68f373d0edc0be4f952f10369507289bbf9f7bee7966a38c4a2185724cbc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbb275e0825c9f36629c3bf35ce88dafb2dc22e0c44dae399e48f240b6c14ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksSharePluginframeworkObjectPartitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartitionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01aff1ec66e1c1c3da85c2b4f4e76d75b42224d75543e9862f6306e29a7ec9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksSharePluginframeworkObjectPartitionValue", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6cd0de7a0a09b19d11f5738ea97cf0de624e641c65a52a41580f8a4922b66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "DataDatabricksSharePluginframeworkObjectPartitionValueList":
        return typing.cast("DataDatabricksSharePluginframeworkObjectPartitionValueList", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartitionValue"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksSharePluginframeworkObjectPartitionValue"]]], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f826e87162b16cd9bd55256883d41d700fdae2f67f24d7f641a7afd0e141fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartitionValue",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "op": "op",
        "recipient_property_key": "recipientPropertyKey",
        "value": "value",
    },
)
class DataDatabricksSharePluginframeworkObjectPartitionValue:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        op: typing.Optional[builtins.str] = None,
        recipient_property_key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.
        :param op: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#op DataDatabricksSharePluginframework#op}.
        :param recipient_property_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#recipient_property_key DataDatabricksSharePluginframework#recipient_property_key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#value DataDatabricksSharePluginframework#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b8b287da3d4e2f731b81aeb6a1e8959f9336ade17668cca4a92af77062e46c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument op", value=op, expected_type=type_hints["op"])
            check_type(argname="argument recipient_property_key", value=recipient_property_key, expected_type=type_hints["recipient_property_key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if op is not None:
            self._values["op"] = op
        if recipient_property_key is not None:
            self._values["recipient_property_key"] = recipient_property_key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#name DataDatabricksSharePluginframework#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def op(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#op DataDatabricksSharePluginframework#op}.'''
        result = self._values.get("op")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipient_property_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#recipient_property_key DataDatabricksSharePluginframework#recipient_property_key}.'''
        result = self._values.get("recipient_property_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/share_pluginframework#value DataDatabricksSharePluginframework#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksSharePluginframeworkObjectPartitionValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksSharePluginframeworkObjectPartitionValueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartitionValueList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6268e7bc1be00d79c03996a8c40cb9375e0620f1b14e292d665e09f7d5924e9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksSharePluginframeworkObjectPartitionValueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ec3ce0f81dced5db0d7ada867f5556d1c6e3ed1df5a59b199e1745204e170a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksSharePluginframeworkObjectPartitionValueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0f867315995f6081e5a7f322d02dde0ca0a05c602bbf4174ee88f77e64430d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc396a8f2a58a66e16b2143a0482d5d2cdf7ebfd2e59d2da2f236975453d579a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d61b90aa9966c0f41d890350062036a81c5fd68d7d4f332175cdb994f0f2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartitionValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartitionValue]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartitionValue]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a02492ba4f8905912e97a3136e1333898267b601c60c6948383a2a806afa71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksSharePluginframeworkObjectPartitionValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSharePluginframework.DataDatabricksSharePluginframeworkObjectPartitionValueOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d85891e2e22ccbbb430d5aa2cb11380a8b73f98041ddf29bc0d5a224fe080ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOp")
    def reset_op(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOp", []))

    @jsii.member(jsii_name="resetRecipientPropertyKey")
    def reset_recipient_property_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipientPropertyKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="opInput")
    def op_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientPropertyKeyInput")
    def recipient_property_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recipientPropertyKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514cd86577d1f83057e5fee2790b011e679f00948d84d8f390a071571b4fe50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ed3d11635de13caced8adba1306776a267a99506b7f930b4fcca7e664ebde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipientPropertyKey")
    def recipient_property_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recipientPropertyKey"))

    @recipient_property_key.setter
    def recipient_property_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed7e6881f96bc5232574ba1728a1a523be8e495e09f7210eb958dc2591bc55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipientPropertyKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5b41c08632dae764fe3f36e632e8c53b2a3eb9ab53f5982fffac4ff2a6267f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartitionValue]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartitionValue]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartitionValue]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910e177a109829d5ca101234d7497ce63f0a0a4b879d856614a13e4996c6655b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataDatabricksSharePluginframework",
    "DataDatabricksSharePluginframeworkConfig",
    "DataDatabricksSharePluginframeworkObject",
    "DataDatabricksSharePluginframeworkObjectList",
    "DataDatabricksSharePluginframeworkObjectOutputReference",
    "DataDatabricksSharePluginframeworkObjectPartition",
    "DataDatabricksSharePluginframeworkObjectPartitionList",
    "DataDatabricksSharePluginframeworkObjectPartitionOutputReference",
    "DataDatabricksSharePluginframeworkObjectPartitionValue",
    "DataDatabricksSharePluginframeworkObjectPartitionValueList",
    "DataDatabricksSharePluginframeworkObjectPartitionValueOutputReference",
]

publication.publish()

def _typecheckingstub__9957c10f0c58d9f2234383a786572860e109bbdfbf6df9108796a7f160e5695a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[jsii.Number] = None,
    created_by: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    object: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObject, typing.Dict[builtins.str, typing.Any]]]]] = None,
    owner: typing.Optional[builtins.str] = None,
    storage_location: typing.Optional[builtins.str] = None,
    storage_root: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[jsii.Number] = None,
    updated_by: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b02abe38806d258e6d3a3dffb53f755f9d817eb75f807ff16ea52837822b2e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb50014116691f72a623d8db67d798df7b6d74650fe724b3084ce9a0b65ccff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObject, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038100539e15ff062f8316e7a3d382bfd551aaabecad5d8168c466ca6afc5c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d06d17c179e8fca4f4711e45fdd01d28481422f4df0156cccc727011728f29(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da369dd6def6d17db97d6fee640db7c35d4a48513dfe5117220dd2acb8ebfb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a301efe9eae5ba297fff0708546d90e69352ff2c2ffa0aee962a32d373666070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b187c4a3928a7223b7871353b91105ecb36fe91bab38333bf8e21c4050c9445c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adee1c2f2d2f5ba052f5f26d4635fbf18820d145276271d1adf5d648c00a0949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ff99cd5846b6021f04803a63f709a36c69ce4b6f3e9895d4674fbcc235654(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cc2122c30dab1a39fafb3e9144fb0c88fd474d7b21d7a75bc0392cb6e70fa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5f2a2ad58bc273e539f9e620507c3bf06636c978fd209c7d584dcf9d436b5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327ebd313600f2fd482292bf6e59521307b0d273955b6525c5f4a6a8d67c2669(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[jsii.Number] = None,
    created_by: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    object: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObject, typing.Dict[builtins.str, typing.Any]]]]] = None,
    owner: typing.Optional[builtins.str] = None,
    storage_location: typing.Optional[builtins.str] = None,
    storage_root: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[jsii.Number] = None,
    updated_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c45169444cfc8aba52f349d4bd54c95ed004e21bf30e1ffbd2449d9f046ed21(
    *,
    name: builtins.str,
    added_at: typing.Optional[jsii.Number] = None,
    added_by: typing.Optional[builtins.str] = None,
    cdf_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comment: typing.Optional[builtins.str] = None,
    content: typing.Optional[builtins.str] = None,
    data_object_type: typing.Optional[builtins.str] = None,
    effective_cdf_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    effective_history_data_sharing_status: typing.Optional[builtins.str] = None,
    effective_shared_as: typing.Optional[builtins.str] = None,
    effective_start_version: typing.Optional[jsii.Number] = None,
    history_data_sharing_status: typing.Optional[builtins.str] = None,
    partition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObjectPartition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shared_as: typing.Optional[builtins.str] = None,
    start_version: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    string_shared_as: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298807ad629b11b40b4486efa7f8f7bdfc31450bffa743afe38155447263cfe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b197884d868082e1a3fbb84ee8b820c23af5dce6bf868e4591ae8dd172e039(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c758deed3c709dd6742d3fe8f1ac987b7abca5892abbcb15bf68a154d342de21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90aad071efabdac7494e83ea4fd24e54649edd75c478a2e20b1e14eb04129059(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48320525a6fc090978ef96a15fcac92f09dc6e5db1dff2ddb608f9970717bb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee121a094cdab2821bf012a29123d98ee9da85ecc35b8bc2ef0a6a337a7b65b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc7211e885605a1dc897727e49dde210aedd41551eaf973d66650b063f9f661(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa73e91e77a01f941c9b75a13ef2c7c31f709f06fa582a66b602cb65553528d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObjectPartition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ab40291eca409cda5a83b92c85f88b312701d185f45745087b331b4d10ff2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa736c86cfe0470f90500d24fb4f0d2265c15caacf972d57cbdc6973dc388ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acf1e387e96de00cc8f41589d425cdd49ec2e5399b40ea508f63173e595c73e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a44812d1cdc2cb76bd164a61cc4caa373cfa40c63e9de53affc9734bb5b272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f45b3e608149638cc53d7ec6c37e28a0783e8e8690b83dd3cdd6e9618d4ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844db3c0a5a96e0d8a6c79c17f3f875c0a7b97bbb910e6290c18d31ee39a21b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851b0722688aa10c92600e7d03896fe0860df987a13931b66f4562cef14af269(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac3bb74d75c4240e6bfc73d890b76de322073a7617b5e935e6151e8b57ca609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be09996a1c75b9e1a448fcabf2dba1bb3a1b08f30ca0f5a84a2f94785d10c2d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55635f64dcce69a4d7317e3b572254e9046d282af90b28206241cb3daa0ce96b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862b9adefccc062b5a1cb934cc501ff3858b827c065c5a9dd46e3c8ea2cbe79d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c94d56f5eaa9510b3a06c90c197703d7de25deb04e336c1fd90257c4a0b4a8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d86334ba2c3d203e33620235edcd8edb1186f6d20194c25b80bb2fc2a9b1e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf26547e46d37776f3408dd146ed9df2beccf39cfbdef1c6ab6989cb4b2394e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72671c7f7fc4be369450eb51fbef4440a766a8f75f2d11de6c680e99debf0b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3c59a0f7d3e2a485c4bfa6c21188d79169a2724c8d547380ef5b82f47a1807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad3a6c2c8d308429f06ded6a71909279b3568b641d129aa2e8b239c92e02d33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObject]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f065bf5f66d207d2fcdd39c5fdc17e255c8e8125bfbaa087b2d850cb9aec8b10(
    *,
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObjectPartitionValue, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedf64285916f7e1b9b86257b053c430c82dfa7e041627feb77e3e0f5bf1e466(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404858107184d297eaf03058999712a29d9676a0ccbea468a5b838ccd4b39000(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42fc54c24998cf2d665ac16b8d08e5c7f3e61e4e839871fa9ff09f06efa955e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f65db254dc734075027e356d7926254734b553edc4ade63e940b0a13a62f40f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e68f373d0edc0be4f952f10369507289bbf9f7bee7966a38c4a2185724cbc7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbb275e0825c9f36629c3bf35ce88dafb2dc22e0c44dae399e48f240b6c14ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01aff1ec66e1c1c3da85c2b4f4e76d75b42224d75543e9862f6306e29a7ec9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6cd0de7a0a09b19d11f5738ea97cf0de624e641c65a52a41580f8a4922b66d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksSharePluginframeworkObjectPartitionValue, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f826e87162b16cd9bd55256883d41d700fdae2f67f24d7f641a7afd0e141fb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b8b287da3d4e2f731b81aeb6a1e8959f9336ade17668cca4a92af77062e46c(
    *,
    name: typing.Optional[builtins.str] = None,
    op: typing.Optional[builtins.str] = None,
    recipient_property_key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6268e7bc1be00d79c03996a8c40cb9375e0620f1b14e292d665e09f7d5924e9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ec3ce0f81dced5db0d7ada867f5556d1c6e3ed1df5a59b199e1745204e170a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0f867315995f6081e5a7f322d02dde0ca0a05c602bbf4174ee88f77e64430d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc396a8f2a58a66e16b2143a0482d5d2cdf7ebfd2e59d2da2f236975453d579a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d61b90aa9966c0f41d890350062036a81c5fd68d7d4f332175cdb994f0f2c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a02492ba4f8905912e97a3136e1333898267b601c60c6948383a2a806afa71c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksSharePluginframeworkObjectPartitionValue]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d85891e2e22ccbbb430d5aa2cb11380a8b73f98041ddf29bc0d5a224fe080ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514cd86577d1f83057e5fee2790b011e679f00948d84d8f390a071571b4fe50e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ed3d11635de13caced8adba1306776a267a99506b7f930b4fcca7e664ebde0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7e6881f96bc5232574ba1728a1a523be8e495e09f7210eb958dc2591bc55c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5b41c08632dae764fe3f36e632e8c53b2a3eb9ab53f5982fffac4ff2a6267f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910e177a109829d5ca101234d7497ce63f0a0a4b879d856614a13e4996c6655b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksSharePluginframeworkObjectPartitionValue]],
) -> None:
    """Type checking stubs"""
    pass
