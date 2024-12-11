r'''
# `databricks_external_location`

Refer to the Terraform Registry for docs: [`databricks_external_location`](https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location).
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


class ExternalLocation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocation",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location databricks_external_location}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        credential_name: builtins.str,
        name: builtins.str,
        url: builtins.str,
        access_point: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        encryption_details: typing.Optional[typing.Union["ExternalLocationEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        isolation_mode: typing.Optional[builtins.str] = None,
        metastore_id: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location databricks_external_location} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#credential_name ExternalLocation#credential_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#name ExternalLocation#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#url ExternalLocation#url}.
        :param access_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#access_point ExternalLocation#access_point}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#comment ExternalLocation#comment}.
        :param encryption_details: encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#encryption_details ExternalLocation#encryption_details}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_destroy ExternalLocation#force_destroy}.
        :param force_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_update ExternalLocation#force_update}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#id ExternalLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#isolation_mode ExternalLocation#isolation_mode}.
        :param metastore_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#metastore_id ExternalLocation#metastore_id}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#owner ExternalLocation#owner}.
        :param read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#read_only ExternalLocation#read_only}.
        :param skip_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#skip_validation ExternalLocation#skip_validation}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7366cd3e0f3652d837eb42745a814fa1e20ee0a42261b2fa98aa1a946825cc7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExternalLocationConfig(
            credential_name=credential_name,
            name=name,
            url=url,
            access_point=access_point,
            comment=comment,
            encryption_details=encryption_details,
            force_destroy=force_destroy,
            force_update=force_update,
            id=id,
            isolation_mode=isolation_mode,
            metastore_id=metastore_id,
            owner=owner,
            read_only=read_only,
            skip_validation=skip_validation,
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
        '''Generates CDKTF code for importing a ExternalLocation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExternalLocation to import.
        :param import_from_id: The id of the existing ExternalLocation that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExternalLocation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b487c903c5e96ca29e0f565c7403f37bb181c84ee46528cec526cc2c8d115cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionDetails")
    def put_encryption_details(
        self,
        *,
        sse_encryption_details: typing.Optional[typing.Union["ExternalLocationEncryptionDetailsSseEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sse_encryption_details: sse_encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#sse_encryption_details ExternalLocation#sse_encryption_details}
        '''
        value = ExternalLocationEncryptionDetails(
            sse_encryption_details=sse_encryption_details
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionDetails", [value]))

    @jsii.member(jsii_name="resetAccessPoint")
    def reset_access_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPoint", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEncryptionDetails")
    def reset_encryption_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionDetails", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetForceUpdate")
    def reset_force_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsolationMode")
    def reset_isolation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolationMode", []))

    @jsii.member(jsii_name="resetMetastoreId")
    def reset_metastore_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreId", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSkipValidation")
    def reset_skip_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipValidation", []))

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
    @jsii.member(jsii_name="encryptionDetails")
    def encryption_details(self) -> "ExternalLocationEncryptionDetailsOutputReference":
        return typing.cast("ExternalLocationEncryptionDetailsOutputReference", jsii.get(self, "encryptionDetails"))

    @builtins.property
    @jsii.member(jsii_name="accessPointInput")
    def access_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPointInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialNameInput")
    def credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionDetailsInput")
    def encryption_details_input(
        self,
    ) -> typing.Optional["ExternalLocationEncryptionDetails"]:
        return typing.cast(typing.Optional["ExternalLocationEncryptionDetails"], jsii.get(self, "encryptionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateInput")
    def force_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="skipValidationInput")
    def skip_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipValidationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8b614a60514722fd6c2d7dc599f87a48bc5b3f0054ba755ba4e4fc1091052c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfb49855b09fbc840e526c776c84db11e7746b391e96a53c656fcfd73ceeeda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialName")
    def credential_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialName"))

    @credential_name.setter
    def credential_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9b0eb1dd8265a399c7b0def2fd7b4d078ca8970897b22217b4e2f568876098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb89ddf8eb08db03cbe6e1348ba4b2464e0ca829cb0679e67ee7f237048cbf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdate")
    def force_update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceUpdate"))

    @force_update.setter
    def force_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2241dd82e60bf6783d71279c6c37d2f9fd39ff3778511ebaa58fd97cc9fcee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53faf82a6ee345997b0604f7bed3f4505b605118c5ddd2bfc546a70dea43e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isolationMode")
    def isolation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolationMode"))

    @isolation_mode.setter
    def isolation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b114585498a3f886998231a928d05346984af0cac7f92e64061eb946e08f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metastoreId")
    def metastore_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreId"))

    @metastore_id.setter
    def metastore_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817858ff24b8d87cf7245b0b5367ffd116b2c331868ea94d6237d78d886cf796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ad4a34141ad33dad28a49d89dc204bd0b733c9b7cdcdaf6ea87fc6e3547192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19979c41d03eb85dbc5fa83ce271ff7132f30fbdba28a18f247e3aaa45ac4e89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9edadaeb8b58771f21fb736c6d5ec5990e83cec6cb8ff0f977349261aaf4957a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipValidation"))

    @skip_validation.setter
    def skip_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6e22fb16b97db63d7f3b8f3b957c69192c5c9311a2acfff06693bf07751a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31ad127868ca7e9d84b4432206c112a3e2e5a0bde9b44c608b3539d81be6e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "credential_name": "credentialName",
        "name": "name",
        "url": "url",
        "access_point": "accessPoint",
        "comment": "comment",
        "encryption_details": "encryptionDetails",
        "force_destroy": "forceDestroy",
        "force_update": "forceUpdate",
        "id": "id",
        "isolation_mode": "isolationMode",
        "metastore_id": "metastoreId",
        "owner": "owner",
        "read_only": "readOnly",
        "skip_validation": "skipValidation",
    },
)
class ExternalLocationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        credential_name: builtins.str,
        name: builtins.str,
        url: builtins.str,
        access_point: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        encryption_details: typing.Optional[typing.Union["ExternalLocationEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        isolation_mode: typing.Optional[builtins.str] = None,
        metastore_id: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#credential_name ExternalLocation#credential_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#name ExternalLocation#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#url ExternalLocation#url}.
        :param access_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#access_point ExternalLocation#access_point}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#comment ExternalLocation#comment}.
        :param encryption_details: encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#encryption_details ExternalLocation#encryption_details}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_destroy ExternalLocation#force_destroy}.
        :param force_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_update ExternalLocation#force_update}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#id ExternalLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#isolation_mode ExternalLocation#isolation_mode}.
        :param metastore_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#metastore_id ExternalLocation#metastore_id}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#owner ExternalLocation#owner}.
        :param read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#read_only ExternalLocation#read_only}.
        :param skip_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#skip_validation ExternalLocation#skip_validation}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_details, dict):
            encryption_details = ExternalLocationEncryptionDetails(**encryption_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0544337dc68b7c3c56f39e14db84cd1129a07627c0f491bb48227f8642ce62df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument credential_name", value=credential_name, expected_type=type_hints["credential_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument access_point", value=access_point, expected_type=type_hints["access_point"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument encryption_details", value=encryption_details, expected_type=type_hints["encryption_details"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
            check_type(argname="argument metastore_id", value=metastore_id, expected_type=type_hints["metastore_id"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument skip_validation", value=skip_validation, expected_type=type_hints["skip_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential_name": credential_name,
            "name": name,
            "url": url,
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
        if access_point is not None:
            self._values["access_point"] = access_point
        if comment is not None:
            self._values["comment"] = comment
        if encryption_details is not None:
            self._values["encryption_details"] = encryption_details
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if force_update is not None:
            self._values["force_update"] = force_update
        if id is not None:
            self._values["id"] = id
        if isolation_mode is not None:
            self._values["isolation_mode"] = isolation_mode
        if metastore_id is not None:
            self._values["metastore_id"] = metastore_id
        if owner is not None:
            self._values["owner"] = owner
        if read_only is not None:
            self._values["read_only"] = read_only
        if skip_validation is not None:
            self._values["skip_validation"] = skip_validation

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
    def credential_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#credential_name ExternalLocation#credential_name}.'''
        result = self._values.get("credential_name")
        assert result is not None, "Required property 'credential_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#name ExternalLocation#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#url ExternalLocation#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_point(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#access_point ExternalLocation#access_point}.'''
        result = self._values.get("access_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#comment ExternalLocation#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_details(
        self,
    ) -> typing.Optional["ExternalLocationEncryptionDetails"]:
        '''encryption_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#encryption_details ExternalLocation#encryption_details}
        '''
        result = self._values.get("encryption_details")
        return typing.cast(typing.Optional["ExternalLocationEncryptionDetails"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_destroy ExternalLocation#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#force_update ExternalLocation#force_update}.'''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#id ExternalLocation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def isolation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#isolation_mode ExternalLocation#isolation_mode}.'''
        result = self._values.get("isolation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastore_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#metastore_id ExternalLocation#metastore_id}.'''
        result = self._values.get("metastore_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#owner ExternalLocation#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#read_only ExternalLocation#read_only}.'''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#skip_validation ExternalLocation#skip_validation}.'''
        result = self._values.get("skip_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalLocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocationEncryptionDetails",
    jsii_struct_bases=[],
    name_mapping={"sse_encryption_details": "sseEncryptionDetails"},
)
class ExternalLocationEncryptionDetails:
    def __init__(
        self,
        *,
        sse_encryption_details: typing.Optional[typing.Union["ExternalLocationEncryptionDetailsSseEncryptionDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sse_encryption_details: sse_encryption_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#sse_encryption_details ExternalLocation#sse_encryption_details}
        '''
        if isinstance(sse_encryption_details, dict):
            sse_encryption_details = ExternalLocationEncryptionDetailsSseEncryptionDetails(**sse_encryption_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b494777d83b0d7be0719b63f1dfdb9818d90f1beee9c59dd750dd656c365cd3)
            check_type(argname="argument sse_encryption_details", value=sse_encryption_details, expected_type=type_hints["sse_encryption_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sse_encryption_details is not None:
            self._values["sse_encryption_details"] = sse_encryption_details

    @builtins.property
    def sse_encryption_details(
        self,
    ) -> typing.Optional["ExternalLocationEncryptionDetailsSseEncryptionDetails"]:
        '''sse_encryption_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#sse_encryption_details ExternalLocation#sse_encryption_details}
        '''
        result = self._values.get("sse_encryption_details")
        return typing.cast(typing.Optional["ExternalLocationEncryptionDetailsSseEncryptionDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalLocationEncryptionDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalLocationEncryptionDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocationEncryptionDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bea3f61673ebd42cc3d9377b9b4f9bfcf1ffbf87ffc1c25ccabda02cd57f55)
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
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#algorithm ExternalLocation#algorithm}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#aws_kms_key_arn ExternalLocation#aws_kms_key_arn}.
        '''
        value = ExternalLocationEncryptionDetailsSseEncryptionDetails(
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
    ) -> "ExternalLocationEncryptionDetailsSseEncryptionDetailsOutputReference":
        return typing.cast("ExternalLocationEncryptionDetailsSseEncryptionDetailsOutputReference", jsii.get(self, "sseEncryptionDetails"))

    @builtins.property
    @jsii.member(jsii_name="sseEncryptionDetailsInput")
    def sse_encryption_details_input(
        self,
    ) -> typing.Optional["ExternalLocationEncryptionDetailsSseEncryptionDetails"]:
        return typing.cast(typing.Optional["ExternalLocationEncryptionDetailsSseEncryptionDetails"], jsii.get(self, "sseEncryptionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExternalLocationEncryptionDetails]:
        return typing.cast(typing.Optional[ExternalLocationEncryptionDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalLocationEncryptionDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cf7bdc0df4599c7ca2408a4e784d3943b89886082368394fcc3b2b86a66710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocationEncryptionDetailsSseEncryptionDetails",
    jsii_struct_bases=[],
    name_mapping={"algorithm": "algorithm", "aws_kms_key_arn": "awsKmsKeyArn"},
)
class ExternalLocationEncryptionDetailsSseEncryptionDetails:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        aws_kms_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#algorithm ExternalLocation#algorithm}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#aws_kms_key_arn ExternalLocation#aws_kms_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ce782e23c6e7ba8a752fb3b477b4e6e945cdac6be3c9577bf4da8479d66d07)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument aws_kms_key_arn", value=aws_kms_key_arn, expected_type=type_hints["aws_kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if aws_kms_key_arn is not None:
            self._values["aws_kms_key_arn"] = aws_kms_key_arn

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#algorithm ExternalLocation#algorithm}.'''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.60.0/docs/resources/external_location#aws_kms_key_arn ExternalLocation#aws_kms_key_arn}.'''
        result = self._values.get("aws_kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalLocationEncryptionDetailsSseEncryptionDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalLocationEncryptionDetailsSseEncryptionDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.externalLocation.ExternalLocationEncryptionDetailsSseEncryptionDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb259f54559c3ec5ce4b424bf0e2ee5b304d48ad4413ceb1f35b0324646d9e88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b265df99d871418d50b6472537adabd2c3f1b9870544f58cd661f68512b40902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsKmsKeyArn")
    def aws_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsKmsKeyArn"))

    @aws_kms_key_arn.setter
    def aws_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b9b5646eebf7d663f4908ca9adb8f8e1fb876f4710aad78abcb7b4920b93d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsKmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ExternalLocationEncryptionDetailsSseEncryptionDetails]:
        return typing.cast(typing.Optional[ExternalLocationEncryptionDetailsSseEncryptionDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalLocationEncryptionDetailsSseEncryptionDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3884d05d44293c5e3f6c390d482d2f10ef82b6ea90cad37d9e1b66b6fab3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExternalLocation",
    "ExternalLocationConfig",
    "ExternalLocationEncryptionDetails",
    "ExternalLocationEncryptionDetailsOutputReference",
    "ExternalLocationEncryptionDetailsSseEncryptionDetails",
    "ExternalLocationEncryptionDetailsSseEncryptionDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__7366cd3e0f3652d837eb42745a814fa1e20ee0a42261b2fa98aa1a946825cc7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    credential_name: builtins.str,
    name: builtins.str,
    url: builtins.str,
    access_point: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    encryption_details: typing.Optional[typing.Union[ExternalLocationEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    isolation_mode: typing.Optional[builtins.str] = None,
    metastore_id: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__6b487c903c5e96ca29e0f565c7403f37bb181c84ee46528cec526cc2c8d115cd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b614a60514722fd6c2d7dc599f87a48bc5b3f0054ba755ba4e4fc1091052c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfb49855b09fbc840e526c776c84db11e7746b391e96a53c656fcfd73ceeeda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9b0eb1dd8265a399c7b0def2fd7b4d078ca8970897b22217b4e2f568876098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb89ddf8eb08db03cbe6e1348ba4b2464e0ca829cb0679e67ee7f237048cbf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2241dd82e60bf6783d71279c6c37d2f9fd39ff3778511ebaa58fd97cc9fcee7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53faf82a6ee345997b0604f7bed3f4505b605118c5ddd2bfc546a70dea43e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b114585498a3f886998231a928d05346984af0cac7f92e64061eb946e08f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817858ff24b8d87cf7245b0b5367ffd116b2c331868ea94d6237d78d886cf796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ad4a34141ad33dad28a49d89dc204bd0b733c9b7cdcdaf6ea87fc6e3547192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19979c41d03eb85dbc5fa83ce271ff7132f30fbdba28a18f247e3aaa45ac4e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edadaeb8b58771f21fb736c6d5ec5990e83cec6cb8ff0f977349261aaf4957a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6e22fb16b97db63d7f3b8f3b957c69192c5c9311a2acfff06693bf07751a9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31ad127868ca7e9d84b4432206c112a3e2e5a0bde9b44c608b3539d81be6e8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0544337dc68b7c3c56f39e14db84cd1129a07627c0f491bb48227f8642ce62df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    credential_name: builtins.str,
    name: builtins.str,
    url: builtins.str,
    access_point: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    encryption_details: typing.Optional[typing.Union[ExternalLocationEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    isolation_mode: typing.Optional[builtins.str] = None,
    metastore_id: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b494777d83b0d7be0719b63f1dfdb9818d90f1beee9c59dd750dd656c365cd3(
    *,
    sse_encryption_details: typing.Optional[typing.Union[ExternalLocationEncryptionDetailsSseEncryptionDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bea3f61673ebd42cc3d9377b9b4f9bfcf1ffbf87ffc1c25ccabda02cd57f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cf7bdc0df4599c7ca2408a4e784d3943b89886082368394fcc3b2b86a66710(
    value: typing.Optional[ExternalLocationEncryptionDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ce782e23c6e7ba8a752fb3b477b4e6e945cdac6be3c9577bf4da8479d66d07(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    aws_kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb259f54559c3ec5ce4b424bf0e2ee5b304d48ad4413ceb1f35b0324646d9e88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b265df99d871418d50b6472537adabd2c3f1b9870544f58cd661f68512b40902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b9b5646eebf7d663f4908ca9adb8f8e1fb876f4710aad78abcb7b4920b93d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3884d05d44293c5e3f6c390d482d2f10ef82b6ea90cad37d9e1b66b6fab3aa(
    value: typing.Optional[ExternalLocationEncryptionDetailsSseEncryptionDetails],
) -> None:
    """Type checking stubs"""
    pass
