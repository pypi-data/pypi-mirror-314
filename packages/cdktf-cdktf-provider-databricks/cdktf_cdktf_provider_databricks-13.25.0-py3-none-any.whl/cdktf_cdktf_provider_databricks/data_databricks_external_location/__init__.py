r'''
# `data_databricks_external_location`

Refer to the Terraform Registry for docs: [`data_databricks_external_location`](https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location).
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


class DataDatabricksExternalLocation(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocation",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location databricks_external_location}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        external_location_info: typing.Optional[typing.Union["DataDatabricksExternalLocationExternalLocationInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location databricks_external_location} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.
        :param external_location_info: external_location_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#external_location_info DataDatabricksExternalLocation#external_location_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#id DataDatabricksExternalLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59d9939c0b59a67d6c3776ccf010f86a1b8e47b61ed628cb143545179b96592)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataDatabricksExternalLocationConfig(
            name=name,
            external_location_info=external_location_info,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatabricksExternalLocation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatabricksExternalLocation to import.
        :param import_from_id: The id of the existing DataDatabricksExternalLocation that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatabricksExternalLocation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d1c4655e14037d2854f4391cf80a7a3efb9af8e0424a2b94aca42f7312b382)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExternalLocationInfo")
    def put_external_location_info(
        self,
        *,
        access_point: typing.Optional[builtins.str] = None,
        browse_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        credential_id: typing.Optional[builtins.str] = None,
        credential_name: typing.Optional[builtins.str] = None,
        encryption_details: typing.Optional[typing.Union["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation_mode: typing.Optional[builtins.str] = None,
        metastore_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        updated_at: typing.Optional[jsii.Number] = None,
        updated_by: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#access_point DataDatabricksExternalLocation#access_point}.
        :param browse_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#browse_only DataDatabricksExternalLocation#browse_only}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#comment DataDatabricksExternalLocation#comment}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_at DataDatabricksExternalLocation#created_at}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_by DataDatabricksExternalLocation#created_by}.
        :param credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_id DataDatabricksExternalLocation#credential_id}.
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_name DataDatabricksExternalLocation#credential_name}.
        :param encryption_details: encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#encryption_details DataDatabricksExternalLocation#encryption_details}
        :param fallback: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#fallback DataDatabricksExternalLocation#fallback}.
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#isolation_mode DataDatabricksExternalLocation#isolation_mode}.
        :param metastore_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#metastore_id DataDatabricksExternalLocation#metastore_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#owner DataDatabricksExternalLocation#owner}.
        :param read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#read_only DataDatabricksExternalLocation#read_only}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_at DataDatabricksExternalLocation#updated_at}.
        :param updated_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_by DataDatabricksExternalLocation#updated_by}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#url DataDatabricksExternalLocation#url}.
        '''
        value = DataDatabricksExternalLocationExternalLocationInfo(
            access_point=access_point,
            browse_only=browse_only,
            comment=comment,
            created_at=created_at,
            created_by=created_by,
            credential_id=credential_id,
            credential_name=credential_name,
            encryption_details=encryption_details,
            fallback=fallback,
            isolation_mode=isolation_mode,
            metastore_id=metastore_id,
            name=name,
            owner=owner,
            read_only=read_only,
            updated_at=updated_at,
            updated_by=updated_by,
            url=url,
        )

        return typing.cast(None, jsii.invoke(self, "putExternalLocationInfo", [value]))

    @jsii.member(jsii_name="resetExternalLocationInfo")
    def reset_external_location_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalLocationInfo", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="externalLocationInfo")
    def external_location_info(
        self,
    ) -> "DataDatabricksExternalLocationExternalLocationInfoOutputReference":
        return typing.cast("DataDatabricksExternalLocationExternalLocationInfoOutputReference", jsii.get(self, "externalLocationInfo"))

    @builtins.property
    @jsii.member(jsii_name="externalLocationInfoInput")
    def external_location_info_input(
        self,
    ) -> typing.Optional["DataDatabricksExternalLocationExternalLocationInfo"]:
        return typing.cast(typing.Optional["DataDatabricksExternalLocationExternalLocationInfo"], jsii.get(self, "externalLocationInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31435708a7ce055e2a8e20b2610ac180a0d0e098865d9a4f934945cdfd913b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1727fb2aa34163e8b66bd4989ac2a2c0aa42a37bde2b223407e900220c8f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "external_location_info": "externalLocationInfo",
        "id": "id",
    },
)
class DataDatabricksExternalLocationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        external_location_info: typing.Optional[typing.Union["DataDatabricksExternalLocationExternalLocationInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.
        :param external_location_info: external_location_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#external_location_info DataDatabricksExternalLocation#external_location_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#id DataDatabricksExternalLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(external_location_info, dict):
            external_location_info = DataDatabricksExternalLocationExternalLocationInfo(**external_location_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f31aac2ad6d10ab58e403e8f0fd2e61d63b07300aa024df37970c726694a137)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument external_location_info", value=external_location_info, expected_type=type_hints["external_location_info"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
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
        if external_location_info is not None:
            self._values["external_location_info"] = external_location_info
        if id is not None:
            self._values["id"] = id

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_location_info(
        self,
    ) -> typing.Optional["DataDatabricksExternalLocationExternalLocationInfo"]:
        '''external_location_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#external_location_info DataDatabricksExternalLocation#external_location_info}
        '''
        result = self._values.get("external_location_info")
        return typing.cast(typing.Optional["DataDatabricksExternalLocationExternalLocationInfo"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#id DataDatabricksExternalLocation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksExternalLocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfo",
    jsii_struct_bases=[],
    name_mapping={
        "access_point": "accessPoint",
        "browse_only": "browseOnly",
        "comment": "comment",
        "created_at": "createdAt",
        "created_by": "createdBy",
        "credential_id": "credentialId",
        "credential_name": "credentialName",
        "encryption_details": "encryptionDetails",
        "fallback": "fallback",
        "isolation_mode": "isolationMode",
        "metastore_id": "metastoreId",
        "name": "name",
        "owner": "owner",
        "read_only": "readOnly",
        "updated_at": "updatedAt",
        "updated_by": "updatedBy",
        "url": "url",
    },
)
class DataDatabricksExternalLocationExternalLocationInfo:
    def __init__(
        self,
        *,
        access_point: typing.Optional[builtins.str] = None,
        browse_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        credential_id: typing.Optional[builtins.str] = None,
        credential_name: typing.Optional[builtins.str] = None,
        encryption_details: typing.Optional[typing.Union["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation_mode: typing.Optional[builtins.str] = None,
        metastore_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        updated_at: typing.Optional[jsii.Number] = None,
        updated_by: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#access_point DataDatabricksExternalLocation#access_point}.
        :param browse_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#browse_only DataDatabricksExternalLocation#browse_only}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#comment DataDatabricksExternalLocation#comment}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_at DataDatabricksExternalLocation#created_at}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_by DataDatabricksExternalLocation#created_by}.
        :param credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_id DataDatabricksExternalLocation#credential_id}.
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_name DataDatabricksExternalLocation#credential_name}.
        :param encryption_details: encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#encryption_details DataDatabricksExternalLocation#encryption_details}
        :param fallback: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#fallback DataDatabricksExternalLocation#fallback}.
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#isolation_mode DataDatabricksExternalLocation#isolation_mode}.
        :param metastore_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#metastore_id DataDatabricksExternalLocation#metastore_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#owner DataDatabricksExternalLocation#owner}.
        :param read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#read_only DataDatabricksExternalLocation#read_only}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_at DataDatabricksExternalLocation#updated_at}.
        :param updated_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_by DataDatabricksExternalLocation#updated_by}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#url DataDatabricksExternalLocation#url}.
        '''
        if isinstance(encryption_details, dict):
            encryption_details = DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails(**encryption_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57eec9b93b819ed192cc53a7d8282b78d092b4171e07919232b818dfd9f18875)
            check_type(argname="argument access_point", value=access_point, expected_type=type_hints["access_point"])
            check_type(argname="argument browse_only", value=browse_only, expected_type=type_hints["browse_only"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
            check_type(argname="argument credential_id", value=credential_id, expected_type=type_hints["credential_id"])
            check_type(argname="argument credential_name", value=credential_name, expected_type=type_hints["credential_name"])
            check_type(argname="argument encryption_details", value=encryption_details, expected_type=type_hints["encryption_details"])
            check_type(argname="argument fallback", value=fallback, expected_type=type_hints["fallback"])
            check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
            check_type(argname="argument metastore_id", value=metastore_id, expected_type=type_hints["metastore_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument updated_by", value=updated_by, expected_type=type_hints["updated_by"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_point is not None:
            self._values["access_point"] = access_point
        if browse_only is not None:
            self._values["browse_only"] = browse_only
        if comment is not None:
            self._values["comment"] = comment
        if created_at is not None:
            self._values["created_at"] = created_at
        if created_by is not None:
            self._values["created_by"] = created_by
        if credential_id is not None:
            self._values["credential_id"] = credential_id
        if credential_name is not None:
            self._values["credential_name"] = credential_name
        if encryption_details is not None:
            self._values["encryption_details"] = encryption_details
        if fallback is not None:
            self._values["fallback"] = fallback
        if isolation_mode is not None:
            self._values["isolation_mode"] = isolation_mode
        if metastore_id is not None:
            self._values["metastore_id"] = metastore_id
        if name is not None:
            self._values["name"] = name
        if owner is not None:
            self._values["owner"] = owner
        if read_only is not None:
            self._values["read_only"] = read_only
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if updated_by is not None:
            self._values["updated_by"] = updated_by
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def access_point(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#access_point DataDatabricksExternalLocation#access_point}.'''
        result = self._values.get("access_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def browse_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#browse_only DataDatabricksExternalLocation#browse_only}.'''
        result = self._values.get("browse_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#comment DataDatabricksExternalLocation#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_at DataDatabricksExternalLocation#created_at}.'''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#created_by DataDatabricksExternalLocation#created_by}.'''
        result = self._values.get("created_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_id DataDatabricksExternalLocation#credential_id}.'''
        result = self._values.get("credential_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#credential_name DataDatabricksExternalLocation#credential_name}.'''
        result = self._values.get("credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_details(
        self,
    ) -> typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails"]:
        '''encryption_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#encryption_details DataDatabricksExternalLocation#encryption_details}
        '''
        result = self._values.get("encryption_details")
        return typing.cast(typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails"], result)

    @builtins.property
    def fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#fallback DataDatabricksExternalLocation#fallback}.'''
        result = self._values.get("fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def isolation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#isolation_mode DataDatabricksExternalLocation#isolation_mode}.'''
        result = self._values.get("isolation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastore_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#metastore_id DataDatabricksExternalLocation#metastore_id}.'''
        result = self._values.get("metastore_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#name DataDatabricksExternalLocation#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#owner DataDatabricksExternalLocation#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#read_only DataDatabricksExternalLocation#read_only}.'''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_at DataDatabricksExternalLocation#updated_at}.'''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def updated_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#updated_by DataDatabricksExternalLocation#updated_by}.'''
        result = self._values.get("updated_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#url DataDatabricksExternalLocation#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksExternalLocationExternalLocationInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails",
    jsii_struct_bases=[],
    name_mapping={"sse_encryption_details": "sseEncryptionDetails"},
)
class DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails:
    def __init__(
        self,
        *,
        sse_encryption_details: typing.Optional[typing.Union["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sse_encryption_details: sse_encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#sse_encryption_details DataDatabricksExternalLocation#sse_encryption_details}
        '''
        if isinstance(sse_encryption_details, dict):
            sse_encryption_details = DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails(**sse_encryption_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5401e96048e30525204680ed98d569a21b1abc48fed3b75859d5814e12b74252)
            check_type(argname="argument sse_encryption_details", value=sse_encryption_details, expected_type=type_hints["sse_encryption_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sse_encryption_details is not None:
            self._values["sse_encryption_details"] = sse_encryption_details

    @builtins.property
    def sse_encryption_details(
        self,
    ) -> typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails"]:
        '''sse_encryption_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#sse_encryption_details DataDatabricksExternalLocation#sse_encryption_details}
        '''
        result = self._values.get("sse_encryption_details")
        return typing.cast(typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f28ca0420538fbf4f0d87032bc2cb71273aff917b4afac7d05584b96f4f300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSseEncryptionDetails")
    def put_sse_encryption_details(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        aws_kms_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#algorithm DataDatabricksExternalLocation#algorithm}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#aws_kms_key_arn DataDatabricksExternalLocation#aws_kms_key_arn}.
        '''
        value = DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails(
            algorithm=algorithm, aws_kms_key_arn=aws_kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putSseEncryptionDetails", [value]))

    @jsii.member(jsii_name="resetSseEncryptionDetails")
    def reset_sse_encryption_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSseEncryptionDetails", []))

    @builtins.property
    @jsii.member(jsii_name="sseEncryptionDetails")
    def sse_encryption_details(
        self,
    ) -> "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetailsOutputReference":
        return typing.cast("DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetailsOutputReference", jsii.get(self, "sseEncryptionDetails"))

    @builtins.property
    @jsii.member(jsii_name="sseEncryptionDetailsInput")
    def sse_encryption_details_input(
        self,
    ) -> typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails"]:
        return typing.cast(typing.Optional["DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails"], jsii.get(self, "sseEncryptionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails]:
        return typing.cast(typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522a88f6a6478942ab2b156fbc29f4f1c61bab6077e421582aa65bbc7a3b9036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails",
    jsii_struct_bases=[],
    name_mapping={"algorithm": "algorithm", "aws_kms_key_arn": "awsKmsKeyArn"},
)
class DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        aws_kms_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#algorithm DataDatabricksExternalLocation#algorithm}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#aws_kms_key_arn DataDatabricksExternalLocation#aws_kms_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72ae9c8c5d788aca13c8eef9030d4ca962614603e02c6b3b58d7c0721ded003)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument aws_kms_key_arn", value=aws_kms_key_arn, expected_type=type_hints["aws_kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if aws_kms_key_arn is not None:
            self._values["aws_kms_key_arn"] = aws_kms_key_arn

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#algorithm DataDatabricksExternalLocation#algorithm}.'''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#aws_kms_key_arn DataDatabricksExternalLocation#aws_kms_key_arn}.'''
        result = self._values.get("aws_kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetailsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ee38452712ec521b340abdbe69d7c334df7ed77d576277fdf55c84b631b52b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetAwsKmsKeyArn")
    def reset_aws_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsKmsKeyArn", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="awsKmsKeyArnInput")
    def aws_kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsKmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285903728bf7be4b6cf703c5229625d91d71439db5377f840af8d91777c784c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsKmsKeyArn")
    def aws_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsKmsKeyArn"))

    @aws_kms_key_arn.setter
    def aws_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea078e49d080420a59a374c9c784068dd955f19a6b9a0cc7ffefc29c2821e2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsKmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails]:
        return typing.cast(typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e378d49e0b8d0d7ec68ec537a7743f083bdfd233cadd3ad1f46f9bd5c026dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksExternalLocationExternalLocationInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksExternalLocation.DataDatabricksExternalLocationExternalLocationInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f60de10b661f58977402d323e2a8d7c5422c2d422b450e60b16a3caf49c4581)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionDetails")
    def put_encryption_details(
        self,
        *,
        sse_encryption_details: typing.Optional[typing.Union[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sse_encryption_details: sse_encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/data-sources/external_location#sse_encryption_details DataDatabricksExternalLocation#sse_encryption_details}
        '''
        value = DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails(
            sse_encryption_details=sse_encryption_details
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionDetails", [value]))

    @jsii.member(jsii_name="resetAccessPoint")
    def reset_access_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPoint", []))

    @jsii.member(jsii_name="resetBrowseOnly")
    def reset_browse_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowseOnly", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetCreatedBy")
    def reset_created_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedBy", []))

    @jsii.member(jsii_name="resetCredentialId")
    def reset_credential_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialId", []))

    @jsii.member(jsii_name="resetCredentialName")
    def reset_credential_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialName", []))

    @jsii.member(jsii_name="resetEncryptionDetails")
    def reset_encryption_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionDetails", []))

    @jsii.member(jsii_name="resetFallback")
    def reset_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallback", []))

    @jsii.member(jsii_name="resetIsolationMode")
    def reset_isolation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolationMode", []))

    @jsii.member(jsii_name="resetMetastoreId")
    def reset_metastore_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetUpdatedBy")
    def reset_updated_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedBy", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionDetails")
    def encryption_details(
        self,
    ) -> DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsOutputReference:
        return typing.cast(DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsOutputReference, jsii.get(self, "encryptionDetails"))

    @builtins.property
    @jsii.member(jsii_name="accessPointInput")
    def access_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPointInput"))

    @builtins.property
    @jsii.member(jsii_name="browseOnlyInput")
    def browse_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "browseOnlyInput"))

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
    @jsii.member(jsii_name="credentialIdInput")
    def credential_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialNameInput")
    def credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionDetailsInput")
    def encryption_details_input(
        self,
    ) -> typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails]:
        return typing.cast(typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails], jsii.get(self, "encryptionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackInput")
    def fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationModeInput")
    def isolation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreIdInput")
    def metastore_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedByInput")
    def updated_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessPoint")
    def access_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPoint"))

    @access_point.setter
    def access_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126cadda889f814c1324d4d6c8585714fc7dc0b07b30ab67d38d9a020063366b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="browseOnly")
    def browse_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "browseOnly"))

    @browse_only.setter
    def browse_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b446d5bc6e10ff6891683358698cb1584b2d3453380896d03a322786f340e56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "browseOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efce29ffde24913ee2b62812b46a226e7958a3fba0969f5cd284581f6b5eaa22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @created_at.setter
    def created_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca76392996b99a65b710d7f20031e2cacc0975ae066cb7279a434f59dc25b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @created_by.setter
    def created_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087a81de464f1b45ee34ef702f6c42cac708cf3b48550413ba37663261a3537a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialId")
    def credential_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialId"))

    @credential_id.setter
    def credential_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6812c28951fa758be5f10e2926066ee9f43f2020c2afe9d6686f98214265bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialName")
    def credential_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialName"))

    @credential_name.setter
    def credential_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebfdccca6a43ee7751e531130db8ee1235cff7af206628a59cacfeb7344b728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fallback")
    def fallback(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fallback"))

    @fallback.setter
    def fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a7181ba6b2dc63f644e758e9eca60159a28a38f013fa0a16268053a07cd425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isolationMode")
    def isolation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolationMode"))

    @isolation_mode.setter
    def isolation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659a61a39c6ed2fd98fc2be1ea413c583464f2da231205c9f466fe4e1a1eb965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metastoreId")
    def metastore_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreId"))

    @metastore_id.setter
    def metastore_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e6a44e779585b60fa638e240bb3f31f4aac9c395eb941d8cd79a8d4dec33cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ea76f0e2c1b244e762e77f25ccd0e5917cbed0d6edd1bd0833d391c66873af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3805e7e7d028d607dd0efe6bad6640e25eba70536017ea0f6a2478059f898772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cc0df3a293bdcd6836fe4c0bafc730b799bca81b02c96679fa682af096edad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updatedAt"))

    @updated_at.setter
    def updated_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b746c84cb4337ba9ee7d0af4e23464e7130db25ec559d852f346a2f449ce8e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedBy")
    def updated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedBy"))

    @updated_by.setter
    def updated_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0a1b9f83ff055df36f2a4336086e153b4b7bd8093861dcdc0c175d0b8c5f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb67f7fa845f28964197232ac7ce6e6d36e04b51e26a21d4fc80a940ef7da49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatabricksExternalLocationExternalLocationInfo]:
        return typing.cast(typing.Optional[DataDatabricksExternalLocationExternalLocationInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83f868cf30eaefeb908ca0673b7646085cb8c47d5aa9ae4e41128d1b52e790b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataDatabricksExternalLocation",
    "DataDatabricksExternalLocationConfig",
    "DataDatabricksExternalLocationExternalLocationInfo",
    "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails",
    "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsOutputReference",
    "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails",
    "DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetailsOutputReference",
    "DataDatabricksExternalLocationExternalLocationInfoOutputReference",
]

publication.publish()

def _typecheckingstub__c59d9939c0b59a67d6c3776ccf010f86a1b8e47b61ed628cb143545179b96592(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    external_location_info: typing.Optional[typing.Union[DataDatabricksExternalLocationExternalLocationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__67d1c4655e14037d2854f4391cf80a7a3efb9af8e0424a2b94aca42f7312b382(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31435708a7ce055e2a8e20b2610ac180a0d0e098865d9a4f934945cdfd913b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1727fb2aa34163e8b66bd4989ac2a2c0aa42a37bde2b223407e900220c8f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f31aac2ad6d10ab58e403e8f0fd2e61d63b07300aa024df37970c726694a137(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    external_location_info: typing.Optional[typing.Union[DataDatabricksExternalLocationExternalLocationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57eec9b93b819ed192cc53a7d8282b78d092b4171e07919232b818dfd9f18875(
    *,
    access_point: typing.Optional[builtins.str] = None,
    browse_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[jsii.Number] = None,
    created_by: typing.Optional[builtins.str] = None,
    credential_id: typing.Optional[builtins.str] = None,
    credential_name: typing.Optional[builtins.str] = None,
    encryption_details: typing.Optional[typing.Union[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    isolation_mode: typing.Optional[builtins.str] = None,
    metastore_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    updated_at: typing.Optional[jsii.Number] = None,
    updated_by: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5401e96048e30525204680ed98d569a21b1abc48fed3b75859d5814e12b74252(
    *,
    sse_encryption_details: typing.Optional[typing.Union[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f28ca0420538fbf4f0d87032bc2cb71273aff917b4afac7d05584b96f4f300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522a88f6a6478942ab2b156fbc29f4f1c61bab6077e421582aa65bbc7a3b9036(
    value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72ae9c8c5d788aca13c8eef9030d4ca962614603e02c6b3b58d7c0721ded003(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    aws_kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ee38452712ec521b340abdbe69d7c334df7ed77d576277fdf55c84b631b52b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285903728bf7be4b6cf703c5229625d91d71439db5377f840af8d91777c784c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea078e49d080420a59a374c9c784068dd955f19a6b9a0cc7ffefc29c2821e2cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e378d49e0b8d0d7ec68ec537a7743f083bdfd233cadd3ad1f46f9bd5c026dd4(
    value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfoEncryptionDetailsSseEncryptionDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f60de10b661f58977402d323e2a8d7c5422c2d422b450e60b16a3caf49c4581(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126cadda889f814c1324d4d6c8585714fc7dc0b07b30ab67d38d9a020063366b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b446d5bc6e10ff6891683358698cb1584b2d3453380896d03a322786f340e56a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efce29ffde24913ee2b62812b46a226e7958a3fba0969f5cd284581f6b5eaa22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca76392996b99a65b710d7f20031e2cacc0975ae066cb7279a434f59dc25b91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087a81de464f1b45ee34ef702f6c42cac708cf3b48550413ba37663261a3537a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6812c28951fa758be5f10e2926066ee9f43f2020c2afe9d6686f98214265bf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebfdccca6a43ee7751e531130db8ee1235cff7af206628a59cacfeb7344b728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a7181ba6b2dc63f644e758e9eca60159a28a38f013fa0a16268053a07cd425(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659a61a39c6ed2fd98fc2be1ea413c583464f2da231205c9f466fe4e1a1eb965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e6a44e779585b60fa638e240bb3f31f4aac9c395eb941d8cd79a8d4dec33cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ea76f0e2c1b244e762e77f25ccd0e5917cbed0d6edd1bd0833d391c66873af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3805e7e7d028d607dd0efe6bad6640e25eba70536017ea0f6a2478059f898772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cc0df3a293bdcd6836fe4c0bafc730b799bca81b02c96679fa682af096edad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b746c84cb4337ba9ee7d0af4e23464e7130db25ec559d852f346a2f449ce8e78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0a1b9f83ff055df36f2a4336086e153b4b7bd8093861dcdc0c175d0b8c5f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb67f7fa845f28964197232ac7ce6e6d36e04b51e26a21d4fc80a940ef7da49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83f868cf30eaefeb908ca0673b7646085cb8c47d5aa9ae4e41128d1b52e790b(
    value: typing.Optional[DataDatabricksExternalLocationExternalLocationInfo],
) -> None:
    """Type checking stubs"""
    pass
