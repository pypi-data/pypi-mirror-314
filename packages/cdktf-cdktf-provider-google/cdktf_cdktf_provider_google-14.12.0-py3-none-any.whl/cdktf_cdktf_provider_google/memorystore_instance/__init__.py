r'''
# `google_memorystore_instance`

Refer to the Terraform Registry for docs: [`google_memorystore_instance`](https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance).
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


class MemorystoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance google_memorystore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        desired_psc_auto_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
        instance_id: builtins.str,
        location: builtins.str,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["MemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance google_memorystore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        :param engine_version: Optional. Immutable. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        :param mode: Optional. Standalone or cluster. Possible values: CLUSTER STANDALONE Possible values: ["CLUSTER", "STANDALONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param node_type: Optional. Immutable. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2fb45bb8e1c847a4a17ca4c94c17a84d676c09dbde16423c0c0a689a1401a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MemorystoreInstanceConfig(
            desired_psc_auto_connections=desired_psc_auto_connections,
            instance_id=instance_id,
            location=location,
            shard_count=shard_count,
            authorization_mode=authorization_mode,
            deletion_protection_enabled=deletion_protection_enabled,
            engine_configs=engine_configs,
            engine_version=engine_version,
            id=id,
            labels=labels,
            mode=mode,
            node_type=node_type,
            persistence_config=persistence_config,
            project=project,
            replica_count=replica_count,
            timeouts=timeouts,
            transit_encryption_mode=transit_encryption_mode,
            zone_distribution_config=zone_distribution_config,
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
        '''Generates CDKTF code for importing a MemorystoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MemorystoreInstance to import.
        :param import_from_id: The id of the existing MemorystoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MemorystoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5999bf261933318d3928796bbc87858f3284b2b0856a80ba3908e3c78dcb6149)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDesiredPscAutoConnections")
    def put_desired_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f8b3ca7a5c726269af10f8f3baa00f32352171a258c1c441fb545233681cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredPscAutoConnections", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        aof_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        value = MemorystoreInstancePersistenceConfig(
            aof_config=aof_config, mode=mode, rdb_config=rdb_config
        )

        return typing.cast(None, jsii.invoke(self, "putPersistenceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.
        '''
        value = MemorystoreInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putZoneDistributionConfig")
    def put_zone_distribution_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        value = MemorystoreInstanceZoneDistributionConfig(mode=mode, zone=zone)

        return typing.cast(None, jsii.invoke(self, "putZoneDistributionConfig", [value]))

    @jsii.member(jsii_name="resetAuthorizationMode")
    def reset_authorization_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationMode", []))

    @jsii.member(jsii_name="resetDeletionProtectionEnabled")
    def reset_deletion_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionEnabled", []))

    @jsii.member(jsii_name="resetEngineConfigs")
    def reset_engine_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineConfigs", []))

    @jsii.member(jsii_name="resetEngineVersion")
    def reset_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetPersistenceConfig")
    def reset_persistence_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReplicaCount")
    def reset_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCount", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransitEncryptionMode")
    def reset_transit_encryption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitEncryptionMode", []))

    @jsii.member(jsii_name="resetZoneDistributionConfig")
    def reset_zone_distribution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneDistributionConfig", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnections")
    def desired_psc_auto_connections(
        self,
    ) -> "MemorystoreInstanceDesiredPscAutoConnectionsList":
        return typing.cast("MemorystoreInstanceDesiredPscAutoConnectionsList", jsii.get(self, "desiredPscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoints")
    def discovery_endpoints(self) -> "MemorystoreInstanceDiscoveryEndpointsList":
        return typing.cast("MemorystoreInstanceDiscoveryEndpointsList", jsii.get(self, "discoveryEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> _cdktf_9a9027ec.StringListList:
        return typing.cast(_cdktf_9a9027ec.StringListList, jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "MemorystoreInstanceNodeConfigList":
        return typing.cast("MemorystoreInstanceNodeConfigList", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(
        self,
    ) -> "MemorystoreInstancePersistenceConfigOutputReference":
        return typing.cast("MemorystoreInstancePersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnections")
    def psc_auto_connections(self) -> "MemorystoreInstancePscAutoConnectionsList":
        return typing.cast("MemorystoreInstancePscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateInfo")
    def state_info(self) -> "MemorystoreInstanceStateInfoList":
        return typing.cast("MemorystoreInstanceStateInfoList", jsii.get(self, "stateInfo"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MemorystoreInstanceTimeoutsOutputReference":
        return typing.cast("MemorystoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfig")
    def zone_distribution_config(
        self,
    ) -> "MemorystoreInstanceZoneDistributionConfigOutputReference":
        return typing.cast("MemorystoreInstanceZoneDistributionConfigOutputReference", jsii.get(self, "zoneDistributionConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationModeInput")
    def authorization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnectionsInput")
    def desired_psc_auto_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]], jsii.get(self, "desiredPscAutoConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="engineConfigsInput")
    def engine_configs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "engineConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfigInput")
    def persistence_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCountInput")
    def replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="shardCountInput")
    def shard_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shardCountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfigInput")
    def zone_distribution_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceZoneDistributionConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstanceZoneDistributionConfig"], jsii.get(self, "zoneDistributionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationMode")
    def authorization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationMode"))

    @authorization_mode.setter
    def authorization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314163717def6def7427963860283520f9dae21947b9b85d7d11fb3da38fca6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabled")
    def deletion_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtectionEnabled"))

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba6264442e0d3675fa984b8b6b73e92d785805cef96cf0a3e097b7e68ff6677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineConfigs")
    def engine_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "engineConfigs"))

    @engine_configs.setter
    def engine_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3709f2e023f297982b4d562e66862abda06d692dfbecb17dd4614b2db11dbee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f7066f3cf0b7fed9af12493ee42a710453ed4048d245c452cb4d04027cc6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbea60c334c216a49ce5e969a6de927630d8c5271ca623c55ba8b40afe7a92c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4253d7579842b6b9565cc68381fdcb973f54b9a506a8141692920f85289e8262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6030b8fd7c5d1d6d400509880ccfe5bc117c8168aa5bae4064d98e3adee2b668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19b2d8726834b58afc9f9651887c5dd44f463ffcbca9bfe3b616dcded38ec05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac46b8400839740879734134c86ef3aa4eaad4955c332b0e83e2c34d6fd7b614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9676613b4ff73e9197c5fba4306e8db26fc31a56a1241e4f06e8c88f10a198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4b97fab2d84a7e93d96ed1be06b4edf72ce55bc8c0a051c4fb31135dfac647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608afdbc5e8b92a5d21cba1c94b90e60110b9f8bab447520a2c4260dc1f20d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930a9d6aa4b5980cff31b999170c74a4ebcd4a96c4200cec381071f91a734648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da65f8b6ec7ad35a3e5044080b42d086ef89128afead8dde501886ac59719e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "desired_psc_auto_connections": "desiredPscAutoConnections",
        "instance_id": "instanceId",
        "location": "location",
        "shard_count": "shardCount",
        "authorization_mode": "authorizationMode",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "engine_configs": "engineConfigs",
        "engine_version": "engineVersion",
        "id": "id",
        "labels": "labels",
        "mode": "mode",
        "node_type": "nodeType",
        "persistence_config": "persistenceConfig",
        "project": "project",
        "replica_count": "replicaCount",
        "timeouts": "timeouts",
        "transit_encryption_mode": "transitEncryptionMode",
        "zone_distribution_config": "zoneDistributionConfig",
    },
)
class MemorystoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        desired_psc_auto_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
        instance_id: builtins.str,
        location: builtins.str,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["MemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        :param engine_version: Optional. Immutable. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        :param mode: Optional. Standalone or cluster. Possible values: CLUSTER STANDALONE Possible values: ["CLUSTER", "STANDALONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param node_type: Optional. Immutable. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(persistence_config, dict):
            persistence_config = MemorystoreInstancePersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = MemorystoreInstanceTimeouts(**timeouts)
        if isinstance(zone_distribution_config, dict):
            zone_distribution_config = MemorystoreInstanceZoneDistributionConfig(**zone_distribution_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de3252cb028a71fd621942b25263bfe393f97041bc2a312c902ff977d4131b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument desired_psc_auto_connections", value=desired_psc_auto_connections, expected_type=type_hints["desired_psc_auto_connections"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument authorization_mode", value=authorization_mode, expected_type=type_hints["authorization_mode"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument engine_configs", value=engine_configs, expected_type=type_hints["engine_configs"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument persistence_config", value=persistence_config, expected_type=type_hints["persistence_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transit_encryption_mode", value=transit_encryption_mode, expected_type=type_hints["transit_encryption_mode"])
            check_type(argname="argument zone_distribution_config", value=zone_distribution_config, expected_type=type_hints["zone_distribution_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "desired_psc_auto_connections": desired_psc_auto_connections,
            "instance_id": instance_id,
            "location": location,
            "shard_count": shard_count,
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
        if authorization_mode is not None:
            self._values["authorization_mode"] = authorization_mode
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if engine_configs is not None:
            self._values["engine_configs"] = engine_configs
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mode is not None:
            self._values["mode"] = mode
        if node_type is not None:
            self._values["node_type"] = node_type
        if persistence_config is not None:
            self._values["persistence_config"] = persistence_config
        if project is not None:
            self._values["project"] = project
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transit_encryption_mode is not None:
            self._values["transit_encryption_mode"] = transit_encryption_mode
        if zone_distribution_config is not None:
            self._values["zone_distribution_config"] = zone_distribution_config

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
    def desired_psc_auto_connections(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]:
        '''desired_psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        '''
        result = self._values.get("desired_psc_auto_connections")
        assert result is not None, "Required property 'desired_psc_auto_connections' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]], result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Required. The ID to use for the instance, which will become the final component of the instance's resource name.

        This value is subject to the following restrictions:

        - Must be 4-63 characters in length
        - Must begin with a letter or digit
        - Must contain only lowercase letters, digits, and hyphens
        - Must not end with a hyphen
        - Must be unique within a location

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'.

        It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shard_count(self) -> jsii.Number:
        '''Required. Number of shards for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorization_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. Authorization mode of the instance. Possible values:  AUTH_DISABLED IAM_AUTH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        '''
        result = self._values.get("authorization_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If set to true deletion of the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def engine_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User-provided engine configurations for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        '''
        result = self._values.get("engine_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. Engine version of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Standalone or cluster.   Possible values:  CLUSTER STANDALONE Possible values: ["CLUSTER", "STANDALONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. Machine type for individual nodes of the instance.   Possible values:  SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional. Number of replica nodes per shard. If omitted the default is 0 replicas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MemorystoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MemorystoreInstanceTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. In-transit encryption mode of the instance.   Possible values:  TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_distribution_config(
        self,
    ) -> typing.Optional["MemorystoreInstanceZoneDistributionConfig"]:
        '''zone_distribution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        '''
        result = self._values.get("zone_distribution_config")
        return typing.cast(typing.Optional["MemorystoreInstanceZoneDistributionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "project_id": "projectId"},
)
class MemorystoreInstanceDesiredPscAutoConnections:
    def __init__(self, *, network: builtins.str, project_id: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        :param project_id: Required. The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76db34ada6b358af4632b8cec3b794296d03488bdf8a6fb3ac955d2f5c08246e)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "project_id": project_id,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a5a75ff50325fba2758481f90765d870da191bd3af52eee6f94a98035dca62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDesiredPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50482b1aa741c93f4c6ec9ff8a290de853258a5ac40e479a554b3b79b1cd7e24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDesiredPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa568015bcb6ccad30db9a1a550040fe52200208912fbd505efbd0d1f20b05d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b214daa5a189121307b9d45d1aeb027c7e1f4cd8dd1ac214c7428569fb9d69b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d83ee45ef1aca3818fc3ad0c4536451c3e9a01ac50fc6e88f9bc534f2f19f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d54229755f3398b74c9e12cd8c73d8b2d1bdb05dd7e9a1e739fd717058b1336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7cd4cbebb36e6eca7e5816b1a852356264f90b6b49e20e43e8b748346482ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64a0ede266977ce99fa5acbe1777c0ee6082d7a95a5a3f8e087d6ed6b1e850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ab0617e10e8cd10e3333cbc00d1f066c1689807413fbb348f32190fe724f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4476f1b5395acc9434ce8168c8dfad05119eca700f0d99ec7a06e9806caece42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceDiscoveryEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDiscoveryEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDiscoveryEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07eec391684704b3b66f0aab3c60e54184f419c967e99afed83d9c386b97d04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDiscoveryEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b3956559536c29e4ae6deb2fa6edfae137a486fc5f7aa7fd4f0f0ef6a34a1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDiscoveryEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee06425654db2d0ba270286ed5fd96229e17d5d47c7427d5aa694ddfa2750fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ee1b2745accf7ae8a05bc86617348257045e0d8c381598d4ae41cc261e07eb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd596310fbf52060c13c4c21d9512b7c84fa0a7d308414eb9df264b75196ea02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDiscoveryEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d5e410e24c343a5594a58338eda10e1d78c71fac87688106cd96352f0de65b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceDiscoveryEndpoints]:
        return typing.cast(typing.Optional[MemorystoreInstanceDiscoveryEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceDiscoveryEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d145318fb59423f668a373fac1969d57653ef62847b28419a65aa101c14167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceNodeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceNodeConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b235a65d0ecfb283379eb19478d9ef9973f101b5e48e22608f66837fbf88e44d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemorystoreInstanceNodeConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62fa3b688059a73d27cac7f8e488153ce08048e920c26898f4a1436fa406290)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceNodeConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55f8334e7f6f94db59a7a9178782aa045b89a0679aecf63e63265f80351734d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a945acd2b62c9d2ab7809aa8f7bee21049a5dd42d7e3365151b87991cc271a7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0b1a1a58df9b749b3b879bedef3c32e92cbe7845d9001583f5862431a271b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6d37e39e2583c013ea71c4d94f8630ec51f93ee1d01dd4154ab2319e85b38d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceNodeConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752f3f0e9ad4955b683394cc173a47f938a89f7142fee4d4fa3d91c35d783aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aof_config": "aofConfig",
        "mode": "mode",
        "rdb_config": "rdbConfig",
    },
)
class MemorystoreInstancePersistenceConfig:
    def __init__(
        self,
        *,
        aof_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        if isinstance(aof_config, dict):
            aof_config = MemorystoreInstancePersistenceConfigAofConfig(**aof_config)
        if isinstance(rdb_config, dict):
            rdb_config = MemorystoreInstancePersistenceConfigRdbConfig(**rdb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9414844fbf7265eb139df17a1a5d3d7ffb5ea373cae0c371773ba8f2a189e147)
            check_type(argname="argument aof_config", value=aof_config, expected_type=type_hints["aof_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument rdb_config", value=rdb_config, expected_type=type_hints["rdb_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aof_config is not None:
            self._values["aof_config"] = aof_config
        if mode is not None:
            self._values["mode"] = mode
        if rdb_config is not None:
            self._values["rdb_config"] = rdb_config

    @builtins.property
    def aof_config(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigAofConfig"]:
        '''aof_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        '''
        result = self._values.get("aof_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigAofConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Current persistence mode.   Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_config(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"]:
        '''rdb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        result = self._values.get("rdb_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigAofConfig",
    jsii_struct_bases=[],
    name_mapping={"append_fsync": "appendFsync"},
)
class MemorystoreInstancePersistenceConfigAofConfig:
    def __init__(self, *, append_fsync: typing.Optional[builtins.str] = None) -> None:
        '''
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b54e3ca144d7d6c06914605ba866043ec9bcd168b3ba038f7788a3f7b84ef38)
            check_type(argname="argument append_fsync", value=append_fsync, expected_type=type_hints["append_fsync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if append_fsync is not None:
            self._values["append_fsync"] = append_fsync

    @builtins.property
    def append_fsync(self) -> typing.Optional[builtins.str]:
        '''Optional. The fsync mode.   Possible values:  NEVER EVERY_SEC ALWAYS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        result = self._values.get("append_fsync")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfigAofConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePersistenceConfigAofConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigAofConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__068bcc0536a632e29160ddf193998f8e244e48fb374dd2695a06f75e6a3da6d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppendFsync")
    def reset_append_fsync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppendFsync", []))

    @builtins.property
    @jsii.member(jsii_name="appendFsyncInput")
    def append_fsync_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appendFsyncInput"))

    @builtins.property
    @jsii.member(jsii_name="appendFsync")
    def append_fsync(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appendFsync"))

    @append_fsync.setter
    def append_fsync(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13b73b72c6d179fdf76e26fefbe2c0a45ab792e67503cac5061502ef3ebb613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendFsync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfigAofConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d62526aa04f462a8bf8dca0cad341a17c28c0275158d3985797a3361c3c79bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstancePersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ec9221129d2c0e7ba383cd2ae710eedcb54b2aad4aa70a2bec769a45d579c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAofConfig")
    def put_aof_config(
        self,
        *,
        append_fsync: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        value = MemorystoreInstancePersistenceConfigAofConfig(
            append_fsync=append_fsync
        )

        return typing.cast(None, jsii.invoke(self, "putAofConfig", [value]))

    @jsii.member(jsii_name="putRdbConfig")
    def put_rdb_config(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        value = MemorystoreInstancePersistenceConfigRdbConfig(
            rdb_snapshot_period=rdb_snapshot_period,
            rdb_snapshot_start_time=rdb_snapshot_start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putRdbConfig", [value]))

    @jsii.member(jsii_name="resetAofConfig")
    def reset_aof_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAofConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRdbConfig")
    def reset_rdb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbConfig", []))

    @builtins.property
    @jsii.member(jsii_name="aofConfig")
    def aof_config(
        self,
    ) -> MemorystoreInstancePersistenceConfigAofConfigOutputReference:
        return typing.cast(MemorystoreInstancePersistenceConfigAofConfigOutputReference, jsii.get(self, "aofConfig"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfig")
    def rdb_config(
        self,
    ) -> "MemorystoreInstancePersistenceConfigRdbConfigOutputReference":
        return typing.cast("MemorystoreInstancePersistenceConfigRdbConfigOutputReference", jsii.get(self, "rdbConfig"))

    @builtins.property
    @jsii.member(jsii_name="aofConfigInput")
    def aof_config_input(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "aofConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfigInput")
    def rdb_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"], jsii.get(self, "rdbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f6c3070e821d5b4e6415ff5b5f1ef1da16a827567e7b1db51088088d8ed32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstancePersistenceConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81c6253caed7197ff8b4d7f5de291b29f642a5d8831b19f2acc190bf0e52171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigRdbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class MemorystoreInstancePersistenceConfigRdbConfig:
    def __init__(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7db1332c63344ecd106396a78ef3aca1c1d1aa37a8f2a6679c26a5287e60c1b)
            check_type(argname="argument rdb_snapshot_period", value=rdb_snapshot_period, expected_type=type_hints["rdb_snapshot_period"])
            check_type(argname="argument rdb_snapshot_start_time", value=rdb_snapshot_start_time, expected_type=type_hints["rdb_snapshot_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rdb_snapshot_period is not None:
            self._values["rdb_snapshot_period"] = rdb_snapshot_period
        if rdb_snapshot_start_time is not None:
            self._values["rdb_snapshot_start_time"] = rdb_snapshot_start_time

    @builtins.property
    def rdb_snapshot_period(self) -> typing.Optional[builtins.str]:
        '''Optional. Period between RDB snapshots.   Possible values:  ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Time that the first snapshot was/will be attempted, and to which future
        snapshots will be aligned. If not provided, the current time will be
        used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfigRdbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePersistenceConfigRdbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigRdbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9bb3725df1ccc4e463860ffdf14983714ebeb0604837eb6c38ec7243a0e2887)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRdbSnapshotPeriod")
    def reset_rdb_snapshot_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotPeriod", []))

    @jsii.member(jsii_name="resetRdbSnapshotStartTime")
    def reset_rdb_snapshot_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriodInput")
    def rdb_snapshot_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTimeInput")
    def rdb_snapshot_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriod")
    def rdb_snapshot_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotPeriod"))

    @rdb_snapshot_period.setter
    def rdb_snapshot_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88283cf8512976da15737eb287396b0a0b16aca2c62c04b3ce03fa22f8fc93b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f8bb3176258d4d065ebc6cba1cf00280508244b266a94bff2591ae1edc9fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be216345b93f500c49669530fd7df3e06fb462779ce4748e1ed58273112abfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstancePscAutoConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b6b230a2494df4f2c3dfb4a94c4036acf58d4593978cf67999c82d05563996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstancePscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e726538e2ca4ec0285ca02774cf4d4cf09602cd9530dc34e917fefc3bc7bb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstancePscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2a1beefb527f323ce88fa135d54bf6100d0096f8dffa0d59df6afcfd03d970)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34347ebd5ea54b15bcd1da860c0915eb3415ccf4ee16d94d1785d28d9c5c32ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fccef096778a353341a88796f2b143979f10d8e608342b2d7f0af478033b9a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstancePscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7544ccf3b7409b50fb57ef537ca9506bf1c1cf4577fefc4f32b78ff94c074cf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionStatus")
    def psc_connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstancePscAutoConnections]:
        return typing.cast(typing.Optional[MemorystoreInstancePscAutoConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePscAutoConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f995bbb332727706b9f077f3f2f4ef24769e21744182f7abbe4601951841cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceStateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceStateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceStateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf660e4341e02329e199f83f60f3155acb64e2333f4dc45d98dafdd2bd05c1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemorystoreInstanceStateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bd93d3c424fdf868151c1bb65f03ae31f3737851cf6a4059dc5e8e9922fc6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceStateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99a564e1a8e87c84ae384e0a03e4847e007f98d33a5a2e9efb1d90c758784e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c41a8d4a08552be15f9fc8acb6e54d2c288b0ffb23dcd844c41612d4b269de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f84f2340d4339a960e65282a66c9d68e974c12dffb5bbe960a23e002357d3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceStateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f822742e887f4501b90646bff3dc2aca400aa1ffd3cc161069973a2be09f1ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateInfo")
    def update_info(self) -> "MemorystoreInstanceStateInfoUpdateInfoList":
        return typing.cast("MemorystoreInstanceStateInfoUpdateInfoList", jsii.get(self, "updateInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceStateInfo]:
        return typing.cast(typing.Optional[MemorystoreInstanceStateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceStateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abd473b792faf2bfe074cf766ea539e701b0aff462a84f3b4c1c30b758e9cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceStateInfoUpdateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceStateInfoUpdateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceStateInfoUpdateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca39fd862fa28c6771459e17324d473da43531c2b9436d404a4555524b48b5a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceStateInfoUpdateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e49b627d0cf8f14c187e5ba9ff6a7a7f76b0fa9193d09d80cd78b9e57aa9e9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceStateInfoUpdateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f0853a7dafcffa99a6014e18ce7be7aca09305a5b48abfd7254af38d0915b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aac8d57ab93b9d3ab1d81ac9ad9fdd1632d49c804ab31c88809ed06beca3119d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb5e69ba11c33245e7f77d2218f93bbcda38423b71ab2345ebb2adc0b518963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceStateInfoUpdateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a3f94882bcc5f02bde866a481184eba294c2603c21dde2dabf0e137e61deec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="targetReplicaCount")
    def target_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="targetShardCount")
    def target_shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetShardCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceStateInfoUpdateInfo]:
        return typing.cast(typing.Optional[MemorystoreInstanceStateInfoUpdateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceStateInfoUpdateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a00f36a1febe806df0db7387da82f08da8a6c076925a25fda22af9b6eec6b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MemorystoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34020f411c6a81ce19b1c60b8ddb0a35402efaae888d8996711dca20e6ed4fb4)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe659aaad8eca5a2bb17a8884e69bcfb527a96fb3b4426d0f0bd96d88b59302f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd9dcde0564f5e6551552c74551cb673b193e3808880599708a09e972d98888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e0356560862ed62e131874219761f2b55f43a3f39629e59e878962171dbc83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bd1c782bdc0caaf80fdd05553eb206f6ca983603a7b7a5cab9bcab143f79b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ad08ac4ae77cb7e45d30ba85a49c2dd55fdedc9327d470c418abd273312d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceZoneDistributionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "zone": "zone"},
)
class MemorystoreInstanceZoneDistributionConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ab258450e70cb8e297e157f1b64a4eeeddb1817eec3fa23d4215fd7fa2c505)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Current zone distribution mode. Defaults to MULTI_ZONE.   Possible values:  MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceZoneDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceZoneDistributionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceZoneDistributionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9fde4a94263b67d257c19190b323d87c62969126edf85326fb471e6a07dafe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b253b164f077a6c2352baf0cd9a0bc406e04486bf47bb0f7f0e6a419928a12f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf82efdd19426a53c5840978e92503b1b69d96fa121ce87b8ab5315e7f3beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceZoneDistributionConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceZoneDistributionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceZoneDistributionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03cdfc8f5febaee3dfe45f5da8e337c2aec578bd53f7a938d410d0111327e40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MemorystoreInstance",
    "MemorystoreInstanceConfig",
    "MemorystoreInstanceDesiredPscAutoConnections",
    "MemorystoreInstanceDesiredPscAutoConnectionsList",
    "MemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
    "MemorystoreInstanceDiscoveryEndpoints",
    "MemorystoreInstanceDiscoveryEndpointsList",
    "MemorystoreInstanceDiscoveryEndpointsOutputReference",
    "MemorystoreInstanceNodeConfig",
    "MemorystoreInstanceNodeConfigList",
    "MemorystoreInstanceNodeConfigOutputReference",
    "MemorystoreInstancePersistenceConfig",
    "MemorystoreInstancePersistenceConfigAofConfig",
    "MemorystoreInstancePersistenceConfigAofConfigOutputReference",
    "MemorystoreInstancePersistenceConfigOutputReference",
    "MemorystoreInstancePersistenceConfigRdbConfig",
    "MemorystoreInstancePersistenceConfigRdbConfigOutputReference",
    "MemorystoreInstancePscAutoConnections",
    "MemorystoreInstancePscAutoConnectionsList",
    "MemorystoreInstancePscAutoConnectionsOutputReference",
    "MemorystoreInstanceStateInfo",
    "MemorystoreInstanceStateInfoList",
    "MemorystoreInstanceStateInfoOutputReference",
    "MemorystoreInstanceStateInfoUpdateInfo",
    "MemorystoreInstanceStateInfoUpdateInfoList",
    "MemorystoreInstanceStateInfoUpdateInfoOutputReference",
    "MemorystoreInstanceTimeouts",
    "MemorystoreInstanceTimeoutsOutputReference",
    "MemorystoreInstanceZoneDistributionConfig",
    "MemorystoreInstanceZoneDistributionConfigOutputReference",
]

publication.publish()

def _typecheckingstub__cc2fb45bb8e1c847a4a17ca4c94c17a84d676c09dbde16423c0c0a689a1401a6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    desired_psc_auto_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
    instance_id: builtins.str,
    location: builtins.str,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[MemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5999bf261933318d3928796bbc87858f3284b2b0856a80ba3908e3c78dcb6149(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f8b3ca7a5c726269af10f8f3baa00f32352171a258c1c441fb545233681cf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314163717def6def7427963860283520f9dae21947b9b85d7d11fb3da38fca6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba6264442e0d3675fa984b8b6b73e92d785805cef96cf0a3e097b7e68ff6677(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3709f2e023f297982b4d562e66862abda06d692dfbecb17dd4614b2db11dbee2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f7066f3cf0b7fed9af12493ee42a710453ed4048d245c452cb4d04027cc6bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbea60c334c216a49ce5e969a6de927630d8c5271ca623c55ba8b40afe7a92c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4253d7579842b6b9565cc68381fdcb973f54b9a506a8141692920f85289e8262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6030b8fd7c5d1d6d400509880ccfe5bc117c8168aa5bae4064d98e3adee2b668(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19b2d8726834b58afc9f9651887c5dd44f463ffcbca9bfe3b616dcded38ec05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac46b8400839740879734134c86ef3aa4eaad4955c332b0e83e2c34d6fd7b614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9676613b4ff73e9197c5fba4306e8db26fc31a56a1241e4f06e8c88f10a198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4b97fab2d84a7e93d96ed1be06b4edf72ce55bc8c0a051c4fb31135dfac647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608afdbc5e8b92a5d21cba1c94b90e60110b9f8bab447520a2c4260dc1f20d41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930a9d6aa4b5980cff31b999170c74a4ebcd4a96c4200cec381071f91a734648(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da65f8b6ec7ad35a3e5044080b42d086ef89128afead8dde501886ac59719e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de3252cb028a71fd621942b25263bfe393f97041bc2a312c902ff977d4131b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_psc_auto_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
    instance_id: builtins.str,
    location: builtins.str,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[MemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76db34ada6b358af4632b8cec3b794296d03488bdf8a6fb3ac955d2f5c08246e(
    *,
    network: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a5a75ff50325fba2758481f90765d870da191bd3af52eee6f94a98035dca62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50482b1aa741c93f4c6ec9ff8a290de853258a5ac40e479a554b3b79b1cd7e24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa568015bcb6ccad30db9a1a550040fe52200208912fbd505efbd0d1f20b05d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b214daa5a189121307b9d45d1aeb027c7e1f4cd8dd1ac214c7428569fb9d69b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d83ee45ef1aca3818fc3ad0c4536451c3e9a01ac50fc6e88f9bc534f2f19f97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d54229755f3398b74c9e12cd8c73d8b2d1bdb05dd7e9a1e739fd717058b1336(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cd4cbebb36e6eca7e5816b1a852356264f90b6b49e20e43e8b748346482ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64a0ede266977ce99fa5acbe1777c0ee6082d7a95a5a3f8e087d6ed6b1e850d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ab0617e10e8cd10e3333cbc00d1f066c1689807413fbb348f32190fe724f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4476f1b5395acc9434ce8168c8dfad05119eca700f0d99ec7a06e9806caece42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07eec391684704b3b66f0aab3c60e54184f419c967e99afed83d9c386b97d04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b3956559536c29e4ae6deb2fa6edfae137a486fc5f7aa7fd4f0f0ef6a34a1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee06425654db2d0ba270286ed5fd96229e17d5d47c7427d5aa694ddfa2750fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee1b2745accf7ae8a05bc86617348257045e0d8c381598d4ae41cc261e07eb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd596310fbf52060c13c4c21d9512b7c84fa0a7d308414eb9df264b75196ea02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5e410e24c343a5594a58338eda10e1d78c71fac87688106cd96352f0de65b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d145318fb59423f668a373fac1969d57653ef62847b28419a65aa101c14167(
    value: typing.Optional[MemorystoreInstanceDiscoveryEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235a65d0ecfb283379eb19478d9ef9973f101b5e48e22608f66837fbf88e44d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62fa3b688059a73d27cac7f8e488153ce08048e920c26898f4a1436fa406290(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55f8334e7f6f94db59a7a9178782aa045b89a0679aecf63e63265f80351734d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a945acd2b62c9d2ab7809aa8f7bee21049a5dd42d7e3365151b87991cc271a7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0b1a1a58df9b749b3b879bedef3c32e92cbe7845d9001583f5862431a271b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6d37e39e2583c013ea71c4d94f8630ec51f93ee1d01dd4154ab2319e85b38d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752f3f0e9ad4955b683394cc173a47f938a89f7142fee4d4fa3d91c35d783aad(
    value: typing.Optional[MemorystoreInstanceNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9414844fbf7265eb139df17a1a5d3d7ffb5ea373cae0c371773ba8f2a189e147(
    *,
    aof_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfigAofConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    rdb_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfigRdbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b54e3ca144d7d6c06914605ba866043ec9bcd168b3ba038f7788a3f7b84ef38(
    *,
    append_fsync: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068bcc0536a632e29160ddf193998f8e244e48fb374dd2695a06f75e6a3da6d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13b73b72c6d179fdf76e26fefbe2c0a45ab792e67503cac5061502ef3ebb613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d62526aa04f462a8bf8dca0cad341a17c28c0275158d3985797a3361c3c79bc(
    value: typing.Optional[MemorystoreInstancePersistenceConfigAofConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ec9221129d2c0e7ba383cd2ae710eedcb54b2aad4aa70a2bec769a45d579c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f6c3070e821d5b4e6415ff5b5f1ef1da16a827567e7b1db51088088d8ed32e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81c6253caed7197ff8b4d7f5de291b29f642a5d8831b19f2acc190bf0e52171(
    value: typing.Optional[MemorystoreInstancePersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7db1332c63344ecd106396a78ef3aca1c1d1aa37a8f2a6679c26a5287e60c1b(
    *,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bb3725df1ccc4e463860ffdf14983714ebeb0604837eb6c38ec7243a0e2887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88283cf8512976da15737eb287396b0a0b16aca2c62c04b3ce03fa22f8fc93b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f8bb3176258d4d065ebc6cba1cf00280508244b266a94bff2591ae1edc9fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be216345b93f500c49669530fd7df3e06fb462779ce4748e1ed58273112abfe0(
    value: typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b6b230a2494df4f2c3dfb4a94c4036acf58d4593978cf67999c82d05563996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e726538e2ca4ec0285ca02774cf4d4cf09602cd9530dc34e917fefc3bc7bb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2a1beefb527f323ce88fa135d54bf6100d0096f8dffa0d59df6afcfd03d970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34347ebd5ea54b15bcd1da860c0915eb3415ccf4ee16d94d1785d28d9c5c32ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccef096778a353341a88796f2b143979f10d8e608342b2d7f0af478033b9a2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7544ccf3b7409b50fb57ef537ca9506bf1c1cf4577fefc4f32b78ff94c074cf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f995bbb332727706b9f077f3f2f4ef24769e21744182f7abbe4601951841cf(
    value: typing.Optional[MemorystoreInstancePscAutoConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf660e4341e02329e199f83f60f3155acb64e2333f4dc45d98dafdd2bd05c1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bd93d3c424fdf868151c1bb65f03ae31f3737851cf6a4059dc5e8e9922fc6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99a564e1a8e87c84ae384e0a03e4847e007f98d33a5a2e9efb1d90c758784e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c41a8d4a08552be15f9fc8acb6e54d2c288b0ffb23dcd844c41612d4b269de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f84f2340d4339a960e65282a66c9d68e974c12dffb5bbe960a23e002357d3bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f822742e887f4501b90646bff3dc2aca400aa1ffd3cc161069973a2be09f1ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd473b792faf2bfe074cf766ea539e701b0aff462a84f3b4c1c30b758e9cc5(
    value: typing.Optional[MemorystoreInstanceStateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca39fd862fa28c6771459e17324d473da43531c2b9436d404a4555524b48b5a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e49b627d0cf8f14c187e5ba9ff6a7a7f76b0fa9193d09d80cd78b9e57aa9e9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f0853a7dafcffa99a6014e18ce7be7aca09305a5b48abfd7254af38d0915b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac8d57ab93b9d3ab1d81ac9ad9fdd1632d49c804ab31c88809ed06beca3119d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb5e69ba11c33245e7f77d2218f93bbcda38423b71ab2345ebb2adc0b518963(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a3f94882bcc5f02bde866a481184eba294c2603c21dde2dabf0e137e61deec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a00f36a1febe806df0db7387da82f08da8a6c076925a25fda22af9b6eec6b1b(
    value: typing.Optional[MemorystoreInstanceStateInfoUpdateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34020f411c6a81ce19b1c60b8ddb0a35402efaae888d8996711dca20e6ed4fb4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe659aaad8eca5a2bb17a8884e69bcfb527a96fb3b4426d0f0bd96d88b59302f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd9dcde0564f5e6551552c74551cb673b193e3808880599708a09e972d98888(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e0356560862ed62e131874219761f2b55f43a3f39629e59e878962171dbc83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bd1c782bdc0caaf80fdd05553eb206f6ca983603a7b7a5cab9bcab143f79b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ad08ac4ae77cb7e45d30ba85a49c2dd55fdedc9327d470c418abd273312d90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab258450e70cb8e297e157f1b64a4eeeddb1817eec3fa23d4215fd7fa2c505(
    *,
    mode: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9fde4a94263b67d257c19190b323d87c62969126edf85326fb471e6a07dafe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b253b164f077a6c2352baf0cd9a0bc406e04486bf47bb0f7f0e6a419928a12f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebf82efdd19426a53c5840978e92503b1b69d96fa121ce87b8ab5315e7f3beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cdfc8f5febaee3dfe45f5da8e337c2aec578bd53f7a938d410d0111327e40e(
    value: typing.Optional[MemorystoreInstanceZoneDistributionConfig],
) -> None:
    """Type checking stubs"""
    pass
