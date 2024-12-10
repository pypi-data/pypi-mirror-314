r'''
# `google_bigquery_reservation`

Refer to the Terraform Registry for docs: [`google_bigquery_reservation`](https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation).
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


class BigqueryReservation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation google_bigquery_reservation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        slot_capacity: jsii.Number,
        autoscale: typing.Optional[typing.Union["BigqueryReservationAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        concurrency: typing.Optional[jsii.Number] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_idle_slots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation google_bigquery_reservation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the reservation. This field must only contain alphanumeric characters or dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#name BigqueryReservation#name}
        :param slot_capacity: Minimum slots available to this reservation. A slot is a unit of computational power in BigQuery, and serves as the unit of parallelism. Queries using this reservation might use more slots during runtime if ignoreIdleSlots is set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#slot_capacity BigqueryReservation#slot_capacity}
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#autoscale BigqueryReservation#autoscale}
        :param concurrency: Maximum number of queries that are allowed to run concurrently in this reservation. This is a soft limit due to asynchronous nature of the system and various optimizations for small queries. Default value is 0 which means that concurrency will be automatically set based on the reservation size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#concurrency BigqueryReservation#concurrency}
        :param edition: The edition type. Valid values are STANDARD, ENTERPRISE, ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#edition BigqueryReservation#edition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#id BigqueryReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_idle_slots: If false, any query using this reservation will use idle slots from other reservations within the same admin project. If true, a query using this reservation will execute with the slot capacity specified above at most. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#ignore_idle_slots BigqueryReservation#ignore_idle_slots}
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#location BigqueryReservation#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#project BigqueryReservation#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#timeouts BigqueryReservation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ff27bf6e86da9195f9cf509e198ef8571f57f917d79a4d0fe64829e4a8e46f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryReservationConfig(
            name=name,
            slot_capacity=slot_capacity,
            autoscale=autoscale,
            concurrency=concurrency,
            edition=edition,
            id=id,
            ignore_idle_slots=ignore_idle_slots,
            location=location,
            project=project,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a BigqueryReservation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryReservation to import.
        :param import_from_id: The id of the existing BigqueryReservation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryReservation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4263118ecb3bc30dbe7c0929a5f79f34b23e29d322cc5abca160545489b8a8b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(self, *, max_slots: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_slots: Number of slots to be scaled when needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#max_slots BigqueryReservation#max_slots}
        '''
        value = BigqueryReservationAutoscale(max_slots=max_slots)

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#create BigqueryReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#delete BigqueryReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#update BigqueryReservation#update}.
        '''
        value = BigqueryReservationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoscale")
    def reset_autoscale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscale", []))

    @jsii.member(jsii_name="resetConcurrency")
    def reset_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConcurrency", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreIdleSlots")
    def reset_ignore_idle_slots(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreIdleSlots", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="autoscale")
    def autoscale(self) -> "BigqueryReservationAutoscaleOutputReference":
        return typing.cast("BigqueryReservationAutoscaleOutputReference", jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryReservationTimeoutsOutputReference":
        return typing.cast("BigqueryReservationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(self) -> typing.Optional["BigqueryReservationAutoscale"]:
        return typing.cast(typing.Optional["BigqueryReservationAutoscale"], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrencyInput")
    def concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "concurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreIdleSlotsInput")
    def ignore_idle_slots_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreIdleSlotsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="slotCapacityInput")
    def slot_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "slotCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryReservationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryReservationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrency")
    def concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "concurrency"))

    @concurrency.setter
    def concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0ca580d18b8b4bfc40527623c0d5bbf9a6485604aa5eda855dcff73c12136a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0d62a2bd52cf8eab13585a092db2f7200c162ced260d40f9a3516fccab91b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066ff42505971946fe93006e7c5668668c632324b179413d9f31149170ea1f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreIdleSlots")
    def ignore_idle_slots(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreIdleSlots"))

    @ignore_idle_slots.setter
    def ignore_idle_slots(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c309ef949b951b4641b6bb86c8fe5c254d32f6a267ea747fc2a9b7f0c86746d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreIdleSlots", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9439ead5b5dead02b6b21e4e02b3368e8d96e51255a50e34b8357886e2891f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a69fa82ef7d78e113759f320a26567dab15ff9e8dd24783ffbc45d85c9220d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e677db66061f2d285140a525b8852a51cac3ff8d8e62df9be5130c50716623c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotCapacity")
    def slot_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "slotCapacity"))

    @slot_capacity.setter
    def slot_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d16b51123c1d48599b8293075487ebee09ea0bfb8f245252b4e1a2acf57bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotCapacity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservationAutoscale",
    jsii_struct_bases=[],
    name_mapping={"max_slots": "maxSlots"},
)
class BigqueryReservationAutoscale:
    def __init__(self, *, max_slots: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_slots: Number of slots to be scaled when needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#max_slots BigqueryReservation#max_slots}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c9cb2e660b0e8f58eeb809fce421c9ab9a7f0481f6d238251618eb0522567e)
            check_type(argname="argument max_slots", value=max_slots, expected_type=type_hints["max_slots"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_slots is not None:
            self._values["max_slots"] = max_slots

    @builtins.property
    def max_slots(self) -> typing.Optional[jsii.Number]:
        '''Number of slots to be scaled when needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#max_slots BigqueryReservation#max_slots}
        '''
        result = self._values.get("max_slots")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryReservationAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryReservationAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservationAutoscaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b8dad3aed5eef2f3c42d6a7666b11e8169cda187dfe4d2a82223df83ed11ea3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxSlots")
    def reset_max_slots(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSlots", []))

    @builtins.property
    @jsii.member(jsii_name="currentSlots")
    def current_slots(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "currentSlots"))

    @builtins.property
    @jsii.member(jsii_name="maxSlotsInput")
    def max_slots_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSlotsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSlots")
    def max_slots(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSlots"))

    @max_slots.setter
    def max_slots(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d88a97170e1a57712d57823143cf923c00663101954a7663acb768412d3a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSlots", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryReservationAutoscale]:
        return typing.cast(typing.Optional[BigqueryReservationAutoscale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryReservationAutoscale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f327275c2d32f814c5c6ab4046269994a7a57eeb211a5eb79c623461b0a3fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservationConfig",
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
        "slot_capacity": "slotCapacity",
        "autoscale": "autoscale",
        "concurrency": "concurrency",
        "edition": "edition",
        "id": "id",
        "ignore_idle_slots": "ignoreIdleSlots",
        "location": "location",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class BigqueryReservationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        slot_capacity: jsii.Number,
        autoscale: typing.Optional[typing.Union[BigqueryReservationAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
        concurrency: typing.Optional[jsii.Number] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_idle_slots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the reservation. This field must only contain alphanumeric characters or dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#name BigqueryReservation#name}
        :param slot_capacity: Minimum slots available to this reservation. A slot is a unit of computational power in BigQuery, and serves as the unit of parallelism. Queries using this reservation might use more slots during runtime if ignoreIdleSlots is set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#slot_capacity BigqueryReservation#slot_capacity}
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#autoscale BigqueryReservation#autoscale}
        :param concurrency: Maximum number of queries that are allowed to run concurrently in this reservation. This is a soft limit due to asynchronous nature of the system and various optimizations for small queries. Default value is 0 which means that concurrency will be automatically set based on the reservation size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#concurrency BigqueryReservation#concurrency}
        :param edition: The edition type. Valid values are STANDARD, ENTERPRISE, ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#edition BigqueryReservation#edition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#id BigqueryReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_idle_slots: If false, any query using this reservation will use idle slots from other reservations within the same admin project. If true, a query using this reservation will execute with the slot capacity specified above at most. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#ignore_idle_slots BigqueryReservation#ignore_idle_slots}
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#location BigqueryReservation#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#project BigqueryReservation#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#timeouts BigqueryReservation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscale, dict):
            autoscale = BigqueryReservationAutoscale(**autoscale)
        if isinstance(timeouts, dict):
            timeouts = BigqueryReservationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6824ff487a7674e468fdb9b2d3747e75209ce497a52976364fe62e0e661dca23)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument slot_capacity", value=slot_capacity, expected_type=type_hints["slot_capacity"])
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_idle_slots", value=ignore_idle_slots, expected_type=type_hints["ignore_idle_slots"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "slot_capacity": slot_capacity,
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
        if autoscale is not None:
            self._values["autoscale"] = autoscale
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if edition is not None:
            self._values["edition"] = edition
        if id is not None:
            self._values["id"] = id
        if ignore_idle_slots is not None:
            self._values["ignore_idle_slots"] = ignore_idle_slots
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''The name of the reservation. This field must only contain alphanumeric characters or dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#name BigqueryReservation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slot_capacity(self) -> jsii.Number:
        '''Minimum slots available to this reservation.

        A slot is a unit of computational power in BigQuery, and serves as the
        unit of parallelism. Queries using this reservation might use more slots during runtime if ignoreIdleSlots is set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#slot_capacity BigqueryReservation#slot_capacity}
        '''
        result = self._values.get("slot_capacity")
        assert result is not None, "Required property 'slot_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def autoscale(self) -> typing.Optional[BigqueryReservationAutoscale]:
        '''autoscale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#autoscale BigqueryReservation#autoscale}
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional[BigqueryReservationAutoscale], result)

    @builtins.property
    def concurrency(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of queries that are allowed to run concurrently in this reservation.

        This is a soft limit due to asynchronous nature of the system and various optimizations for small queries. Default value is 0 which means that concurrency will be automatically set based on the reservation size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#concurrency BigqueryReservation#concurrency}
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition type. Valid values are STANDARD, ENTERPRISE, ENTERPRISE_PLUS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#edition BigqueryReservation#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#id BigqueryReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_idle_slots(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If false, any query using this reservation will use idle slots from other reservations within the same admin project.

        If true, a query using this reservation will execute with the slot
        capacity specified above at most.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#ignore_idle_slots BigqueryReservation#ignore_idle_slots}
        '''
        result = self._values.get("ignore_idle_slots")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#location BigqueryReservation#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#project BigqueryReservation#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryReservationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#timeouts BigqueryReservation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryReservationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryReservationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#create BigqueryReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#delete BigqueryReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#update BigqueryReservation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c3c38492b4597f74c82da47723188abdba567ecb08744bdb4fea41ab0adfd8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#create BigqueryReservation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#delete BigqueryReservation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.13.0/docs/resources/bigquery_reservation#update BigqueryReservation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryReservationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryReservationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryReservation.BigqueryReservationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2431a0ff6b832cbe171e526698f845ef63c0fe448594d5dae3e833f45d0668c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c98da587da6f6348ef2d18e88b5053ce172e34d5524e367a2c2c7b1a3e5124c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6ae53fdf0ac2a42ec063fbfd04a696052d6bf391c585861ef53838418eedc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428fdbf8526d1d4e49a0fd2c521a0d4042ca09d0259376c1ea5793b0266bfbf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryReservationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryReservationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryReservationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bbd3919de894abcc6483909f02724a6cb998e1834e15ca6965d0ebf5b3db13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryReservation",
    "BigqueryReservationAutoscale",
    "BigqueryReservationAutoscaleOutputReference",
    "BigqueryReservationConfig",
    "BigqueryReservationTimeouts",
    "BigqueryReservationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a8ff27bf6e86da9195f9cf509e198ef8571f57f917d79a4d0fe64829e4a8e46f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    slot_capacity: jsii.Number,
    autoscale: typing.Optional[typing.Union[BigqueryReservationAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrency: typing.Optional[jsii.Number] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_idle_slots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4263118ecb3bc30dbe7c0929a5f79f34b23e29d322cc5abca160545489b8a8b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0ca580d18b8b4bfc40527623c0d5bbf9a6485604aa5eda855dcff73c12136a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0d62a2bd52cf8eab13585a092db2f7200c162ced260d40f9a3516fccab91b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066ff42505971946fe93006e7c5668668c632324b179413d9f31149170ea1f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c309ef949b951b4641b6bb86c8fe5c254d32f6a267ea747fc2a9b7f0c86746d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9439ead5b5dead02b6b21e4e02b3368e8d96e51255a50e34b8357886e2891f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a69fa82ef7d78e113759f320a26567dab15ff9e8dd24783ffbc45d85c9220d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e677db66061f2d285140a525b8852a51cac3ff8d8e62df9be5130c50716623c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d16b51123c1d48599b8293075487ebee09ea0bfb8f245252b4e1a2acf57bd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c9cb2e660b0e8f58eeb809fce421c9ab9a7f0481f6d238251618eb0522567e(
    *,
    max_slots: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8dad3aed5eef2f3c42d6a7666b11e8169cda187dfe4d2a82223df83ed11ea3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d88a97170e1a57712d57823143cf923c00663101954a7663acb768412d3a3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f327275c2d32f814c5c6ab4046269994a7a57eeb211a5eb79c623461b0a3fc1(
    value: typing.Optional[BigqueryReservationAutoscale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6824ff487a7674e468fdb9b2d3747e75209ce497a52976364fe62e0e661dca23(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    slot_capacity: jsii.Number,
    autoscale: typing.Optional[typing.Union[BigqueryReservationAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrency: typing.Optional[jsii.Number] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_idle_slots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c3c38492b4597f74c82da47723188abdba567ecb08744bdb4fea41ab0adfd8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2431a0ff6b832cbe171e526698f845ef63c0fe448594d5dae3e833f45d0668c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c98da587da6f6348ef2d18e88b5053ce172e34d5524e367a2c2c7b1a3e5124c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6ae53fdf0ac2a42ec063fbfd04a696052d6bf391c585861ef53838418eedc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428fdbf8526d1d4e49a0fd2c521a0d4042ca09d0259376c1ea5793b0266bfbf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bbd3919de894abcc6483909f02724a6cb998e1834e15ca6965d0ebf5b3db13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryReservationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
