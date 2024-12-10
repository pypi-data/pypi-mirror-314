r'''
# `google_storage_transfer_job`

Refer to the Terraform Registry for docs: [`google_storage_transfer_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job).
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


class GoogleStorageTransferJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job google_storage_transfer_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        transfer_spec: typing.Union["GoogleStorageTransferJobTransferSpec", typing.Dict[builtins.str, typing.Any]],
        event_stream: typing.Optional[typing.Union["GoogleStorageTransferJobEventStream", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["GoogleStorageTransferJobNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["GoogleStorageTransferJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job google_storage_transfer_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Unique description to identify the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#description GoogleStorageTransferJob#description}
        :param transfer_spec: transfer_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_spec GoogleStorageTransferJob#transfer_spec}
        :param event_stream: event_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream GoogleStorageTransferJob#event_stream}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#id GoogleStorageTransferJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The name of the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#notification_config GoogleStorageTransferJob#notification_config}
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#project GoogleStorageTransferJob#project}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule GoogleStorageTransferJob#schedule}
        :param status: Status of the job. Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#status GoogleStorageTransferJob#status}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa0e6d9f40b0f4824748507a8f9bba74e07cf4b9f348b6149b4ffb41a4e7200)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageTransferJobConfig(
            description=description,
            transfer_spec=transfer_spec,
            event_stream=event_stream,
            id=id,
            name=name,
            notification_config=notification_config,
            project=project,
            schedule=schedule,
            status=status,
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
        '''Generates CDKTF code for importing a GoogleStorageTransferJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageTransferJob to import.
        :param import_from_id: The id of the existing GoogleStorageTransferJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageTransferJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abe485176e54191e1dddef5bb791535ed919838828f1ce783c01cb82241b337)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventStream")
    def put_event_stream(
        self,
        *,
        name: builtins.str,
        event_stream_expiration_time: typing.Optional[builtins.str] = None,
        event_stream_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        :param event_stream_expiration_time: Specifies the data and time at which Storage Transfer Service stops listening for events from this stream. After this time, any transfers in progress will complete, but no new transfers are initiated Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_expiration_time GoogleStorageTransferJob#event_stream_expiration_time}
        :param event_stream_start_time: Specifies the date and time that Storage Transfer Service starts listening for events from this stream. If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_start_time GoogleStorageTransferJob#event_stream_start_time}
        '''
        value = GoogleStorageTransferJobEventStream(
            name=name,
            event_stream_expiration_time=event_stream_expiration_time,
            event_stream_start_time=event_stream_start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putEventStream", [value]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        payload_format: builtins.str,
        pubsub_topic: builtins.str,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param payload_format: The desired format of the notification message payloads. One of "NONE" or "JSON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#payload_format GoogleStorageTransferJob#payload_format}
        :param pubsub_topic: The Topic.name of the Pub/Sub topic to which to publish notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#pubsub_topic GoogleStorageTransferJob#pubsub_topic}
        :param event_types: Event types for which a notification is desired. If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_types GoogleStorageTransferJob#event_types}
        '''
        value = GoogleStorageTransferJobNotificationConfig(
            payload_format=payload_format,
            pubsub_topic=pubsub_topic,
            event_types=event_types,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        schedule_start_date: typing.Union["GoogleStorageTransferJobScheduleScheduleStartDate", typing.Dict[builtins.str, typing.Any]],
        repeat_interval: typing.Optional[builtins.str] = None,
        schedule_end_date: typing.Optional[typing.Union["GoogleStorageTransferJobScheduleScheduleEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time_of_day: typing.Optional[typing.Union["GoogleStorageTransferJobScheduleStartTimeOfDay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule_start_date: schedule_start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_start_date GoogleStorageTransferJob#schedule_start_date}
        :param repeat_interval: Interval between the start of each scheduled transfer. If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#repeat_interval GoogleStorageTransferJob#repeat_interval}
        :param schedule_end_date: schedule_end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_end_date GoogleStorageTransferJob#schedule_end_date}
        :param start_time_of_day: start_time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#start_time_of_day GoogleStorageTransferJob#start_time_of_day}
        '''
        value = GoogleStorageTransferJobSchedule(
            schedule_start_date=schedule_start_date,
            repeat_interval=repeat_interval,
            schedule_end_date=schedule_end_date,
            start_time_of_day=start_time_of_day,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putTransferSpec")
    def put_transfer_spec(
        self,
        *,
        aws_s3_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAwsS3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_sink: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        http_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecHttpDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_sink: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecPosixDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecPosixDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        sink_agent_pool_name: typing.Optional[builtins.str] = None,
        source_agent_pool_name: typing.Optional[builtins.str] = None,
        transfer_options: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_s3_data_source: aws_s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_s3_data_source GoogleStorageTransferJob#aws_s3_data_source}
        :param azure_blob_storage_data_source: azure_blob_storage_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_blob_storage_data_source GoogleStorageTransferJob#azure_blob_storage_data_source}
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_sink GoogleStorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_source GoogleStorageTransferJob#gcs_data_source}
        :param http_data_source: http_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#http_data_source GoogleStorageTransferJob#http_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#object_conditions GoogleStorageTransferJob#object_conditions}
        :param posix_data_sink: posix_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_sink GoogleStorageTransferJob#posix_data_sink}
        :param posix_data_source: posix_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_source GoogleStorageTransferJob#posix_data_source}
        :param sink_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sink_agent_pool_name GoogleStorageTransferJob#sink_agent_pool_name}
        :param source_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#source_agent_pool_name GoogleStorageTransferJob#source_agent_pool_name}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_options GoogleStorageTransferJob#transfer_options}
        '''
        value = GoogleStorageTransferJobTransferSpec(
            aws_s3_data_source=aws_s3_data_source,
            azure_blob_storage_data_source=azure_blob_storage_data_source,
            gcs_data_sink=gcs_data_sink,
            gcs_data_source=gcs_data_source,
            http_data_source=http_data_source,
            object_conditions=object_conditions,
            posix_data_sink=posix_data_sink,
            posix_data_source=posix_data_source,
            sink_agent_pool_name=sink_agent_pool_name,
            source_agent_pool_name=source_agent_pool_name,
            transfer_options=transfer_options,
        )

        return typing.cast(None, jsii.invoke(self, "putTransferSpec", [value]))

    @jsii.member(jsii_name="resetEventStream")
    def reset_event_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStream", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

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
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="deletionTime")
    def deletion_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionTime"))

    @builtins.property
    @jsii.member(jsii_name="eventStream")
    def event_stream(self) -> "GoogleStorageTransferJobEventStreamOutputReference":
        return typing.cast("GoogleStorageTransferJobEventStreamOutputReference", jsii.get(self, "eventStream"))

    @builtins.property
    @jsii.member(jsii_name="lastModificationTime")
    def last_modification_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "GoogleStorageTransferJobNotificationConfigOutputReference":
        return typing.cast("GoogleStorageTransferJobNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "GoogleStorageTransferJobScheduleOutputReference":
        return typing.cast("GoogleStorageTransferJobScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="transferSpec")
    def transfer_spec(self) -> "GoogleStorageTransferJobTransferSpecOutputReference":
        return typing.cast("GoogleStorageTransferJobTransferSpecOutputReference", jsii.get(self, "transferSpec"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamInput")
    def event_stream_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobEventStream"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobEventStream"], jsii.get(self, "eventStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobNotificationConfig"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["GoogleStorageTransferJobSchedule"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="transferSpecInput")
    def transfer_spec_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpec"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpec"], jsii.get(self, "transferSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db30cb36b031ca871bd7d46f8831cdcf8734f566413c9844b53a73b51c4df569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480e69080926fc7d0d9b21c3bfa3a4ec6248fd91c18b6fb7ed12233e6c2d8be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f63f58155b19562027f76abe83123a6a2aa7c8a7c7bec44c32d3b6773f0f302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7d4ad62350b3c194a289d29297af76990462f307e96499134ba2c4668ac5b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2e4e24b87eededac2893a4ac2e9dba06006d65831cff41eea86703a597a98a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "transfer_spec": "transferSpec",
        "event_stream": "eventStream",
        "id": "id",
        "name": "name",
        "notification_config": "notificationConfig",
        "project": "project",
        "schedule": "schedule",
        "status": "status",
    },
)
class GoogleStorageTransferJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        transfer_spec: typing.Union["GoogleStorageTransferJobTransferSpec", typing.Dict[builtins.str, typing.Any]],
        event_stream: typing.Optional[typing.Union["GoogleStorageTransferJobEventStream", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["GoogleStorageTransferJobNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["GoogleStorageTransferJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: Unique description to identify the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#description GoogleStorageTransferJob#description}
        :param transfer_spec: transfer_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_spec GoogleStorageTransferJob#transfer_spec}
        :param event_stream: event_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream GoogleStorageTransferJob#event_stream}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#id GoogleStorageTransferJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The name of the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#notification_config GoogleStorageTransferJob#notification_config}
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#project GoogleStorageTransferJob#project}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule GoogleStorageTransferJob#schedule}
        :param status: Status of the job. Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#status GoogleStorageTransferJob#status}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(transfer_spec, dict):
            transfer_spec = GoogleStorageTransferJobTransferSpec(**transfer_spec)
        if isinstance(event_stream, dict):
            event_stream = GoogleStorageTransferJobEventStream(**event_stream)
        if isinstance(notification_config, dict):
            notification_config = GoogleStorageTransferJobNotificationConfig(**notification_config)
        if isinstance(schedule, dict):
            schedule = GoogleStorageTransferJobSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c1d961b14a89391da0f77f62bcbf5af44420597571e86b0fb6e74fe20ac51a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument transfer_spec", value=transfer_spec, expected_type=type_hints["transfer_spec"])
            check_type(argname="argument event_stream", value=event_stream, expected_type=type_hints["event_stream"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "transfer_spec": transfer_spec,
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
        if event_stream is not None:
            self._values["event_stream"] = event_stream
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if project is not None:
            self._values["project"] = project
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status

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
    def description(self) -> builtins.str:
        '''Unique description to identify the Transfer Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#description GoogleStorageTransferJob#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def transfer_spec(self) -> "GoogleStorageTransferJobTransferSpec":
        '''transfer_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_spec GoogleStorageTransferJob#transfer_spec}
        '''
        result = self._values.get("transfer_spec")
        assert result is not None, "Required property 'transfer_spec' is missing"
        return typing.cast("GoogleStorageTransferJobTransferSpec", result)

    @builtins.property
    def event_stream(self) -> typing.Optional["GoogleStorageTransferJobEventStream"]:
        '''event_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream GoogleStorageTransferJob#event_stream}
        '''
        result = self._values.get("event_stream")
        return typing.cast(typing.Optional["GoogleStorageTransferJobEventStream"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#id GoogleStorageTransferJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Transfer Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#notification_config GoogleStorageTransferJob#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["GoogleStorageTransferJobNotificationConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which the resource belongs. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#project GoogleStorageTransferJob#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["GoogleStorageTransferJobSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule GoogleStorageTransferJob#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["GoogleStorageTransferJobSchedule"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of the job.

        Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#status GoogleStorageTransferJob#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobEventStream",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "event_stream_expiration_time": "eventStreamExpirationTime",
        "event_stream_start_time": "eventStreamStartTime",
    },
)
class GoogleStorageTransferJobEventStream:
    def __init__(
        self,
        *,
        name: builtins.str,
        event_stream_expiration_time: typing.Optional[builtins.str] = None,
        event_stream_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        :param event_stream_expiration_time: Specifies the data and time at which Storage Transfer Service stops listening for events from this stream. After this time, any transfers in progress will complete, but no new transfers are initiated Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_expiration_time GoogleStorageTransferJob#event_stream_expiration_time}
        :param event_stream_start_time: Specifies the date and time that Storage Transfer Service starts listening for events from this stream. If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_start_time GoogleStorageTransferJob#event_stream_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1637153c101c25686eeb4844f49b8302850868d3fe4fdd8abb297b18af39f828)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument event_stream_expiration_time", value=event_stream_expiration_time, expected_type=type_hints["event_stream_expiration_time"])
            check_type(argname="argument event_stream_start_time", value=event_stream_start_time, expected_type=type_hints["event_stream_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if event_stream_expiration_time is not None:
            self._values["event_stream_expiration_time"] = event_stream_expiration_time
        if event_stream_start_time is not None:
            self._values["event_stream_start_time"] = event_stream_start_time

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#name GoogleStorageTransferJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_stream_expiration_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the data and time at which Storage Transfer Service stops listening for events from this stream.

        After this time, any transfers in progress will complete, but no new transfers are initiated

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_expiration_time GoogleStorageTransferJob#event_stream_expiration_time}
        '''
        result = self._values.get("event_stream_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_stream_start_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the date and time that Storage Transfer Service starts listening for events from this stream.

        If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_stream_start_time GoogleStorageTransferJob#event_stream_start_time}
        '''
        result = self._values.get("event_stream_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobEventStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobEventStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobEventStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaea62fb9ca859d0e6fa2da45da2a4e3d32668bee179a3ace63a389c15cc0564)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventStreamExpirationTime")
    def reset_event_stream_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStreamExpirationTime", []))

    @jsii.member(jsii_name="resetEventStreamStartTime")
    def reset_event_stream_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStreamStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="eventStreamExpirationTimeInput")
    def event_stream_expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventStreamExpirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamStartTimeInput")
    def event_stream_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventStreamStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamExpirationTime")
    def event_stream_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventStreamExpirationTime"))

    @event_stream_expiration_time.setter
    def event_stream_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddab4e173ed667d75268e866f267398704de9bc2315931e2c4caf34215aebc80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventStreamExpirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventStreamStartTime")
    def event_stream_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventStreamStartTime"))

    @event_stream_start_time.setter
    def event_stream_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d3a48fcc8db54983539f7154c77fbe2f40d9d137f5a445d29ba56c9cebeda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventStreamStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee7bd1ceed264a45fdfc1bbd7cb2c0aad822d246438ea38bf860f1836c5a3f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageTransferJobEventStream]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobEventStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobEventStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111da4b0023b46055621932ca349e5cfce3eed8682320082442138034336818e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "payload_format": "payloadFormat",
        "pubsub_topic": "pubsubTopic",
        "event_types": "eventTypes",
    },
)
class GoogleStorageTransferJobNotificationConfig:
    def __init__(
        self,
        *,
        payload_format: builtins.str,
        pubsub_topic: builtins.str,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param payload_format: The desired format of the notification message payloads. One of "NONE" or "JSON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#payload_format GoogleStorageTransferJob#payload_format}
        :param pubsub_topic: The Topic.name of the Pub/Sub topic to which to publish notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#pubsub_topic GoogleStorageTransferJob#pubsub_topic}
        :param event_types: Event types for which a notification is desired. If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_types GoogleStorageTransferJob#event_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9867f8190484a9321b33a153b3119bfa913f102da67c563e0fd054d20edd23)
            check_type(argname="argument payload_format", value=payload_format, expected_type=type_hints["payload_format"])
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument event_types", value=event_types, expected_type=type_hints["event_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "payload_format": payload_format,
            "pubsub_topic": pubsub_topic,
        }
        if event_types is not None:
            self._values["event_types"] = event_types

    @builtins.property
    def payload_format(self) -> builtins.str:
        '''The desired format of the notification message payloads. One of "NONE" or "JSON".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#payload_format GoogleStorageTransferJob#payload_format}
        '''
        result = self._values.get("payload_format")
        assert result is not None, "Required property 'payload_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Topic.name of the Pub/Sub topic to which to publish notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#pubsub_topic GoogleStorageTransferJob#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Event types for which a notification is desired.

        If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#event_types GoogleStorageTransferJob#event_types}
        '''
        result = self._values.get("event_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abb8dcf6c5e11610014734b0cd4a53ef3fff65082f0f817ff47d7b9ce8d5ea8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventTypes")
    def reset_event_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTypes", []))

    @builtins.property
    @jsii.member(jsii_name="eventTypesInput")
    def event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFormatInput")
    def payload_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypes")
    def event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventTypes"))

    @event_types.setter
    def event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec01815146cf2e07b3d5a857a781c9d16c68ab2779b09a1999dc36da168cb462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadFormat")
    def payload_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadFormat"))

    @payload_format.setter
    def payload_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ffafd908425725fd2c447ecab03082d18888deb01d56e9b1c12dc27e23a43fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d155d5cba211a1e4ac36a40ab9aef97f786f36434d8b7faafc1b86fed5ba4a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobNotificationConfig]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0626cc80d7484c5505b2eb7fbb223c9b2d95c485441c4432ec354d47ff587a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "schedule_start_date": "scheduleStartDate",
        "repeat_interval": "repeatInterval",
        "schedule_end_date": "scheduleEndDate",
        "start_time_of_day": "startTimeOfDay",
    },
)
class GoogleStorageTransferJobSchedule:
    def __init__(
        self,
        *,
        schedule_start_date: typing.Union["GoogleStorageTransferJobScheduleScheduleStartDate", typing.Dict[builtins.str, typing.Any]],
        repeat_interval: typing.Optional[builtins.str] = None,
        schedule_end_date: typing.Optional[typing.Union["GoogleStorageTransferJobScheduleScheduleEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time_of_day: typing.Optional[typing.Union["GoogleStorageTransferJobScheduleStartTimeOfDay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule_start_date: schedule_start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_start_date GoogleStorageTransferJob#schedule_start_date}
        :param repeat_interval: Interval between the start of each scheduled transfer. If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#repeat_interval GoogleStorageTransferJob#repeat_interval}
        :param schedule_end_date: schedule_end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_end_date GoogleStorageTransferJob#schedule_end_date}
        :param start_time_of_day: start_time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#start_time_of_day GoogleStorageTransferJob#start_time_of_day}
        '''
        if isinstance(schedule_start_date, dict):
            schedule_start_date = GoogleStorageTransferJobScheduleScheduleStartDate(**schedule_start_date)
        if isinstance(schedule_end_date, dict):
            schedule_end_date = GoogleStorageTransferJobScheduleScheduleEndDate(**schedule_end_date)
        if isinstance(start_time_of_day, dict):
            start_time_of_day = GoogleStorageTransferJobScheduleStartTimeOfDay(**start_time_of_day)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0cfcd70190b0e8a99fca4e8453e5298f0df03efa255bda0df9d7e8cd22782a)
            check_type(argname="argument schedule_start_date", value=schedule_start_date, expected_type=type_hints["schedule_start_date"])
            check_type(argname="argument repeat_interval", value=repeat_interval, expected_type=type_hints["repeat_interval"])
            check_type(argname="argument schedule_end_date", value=schedule_end_date, expected_type=type_hints["schedule_end_date"])
            check_type(argname="argument start_time_of_day", value=start_time_of_day, expected_type=type_hints["start_time_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule_start_date": schedule_start_date,
        }
        if repeat_interval is not None:
            self._values["repeat_interval"] = repeat_interval
        if schedule_end_date is not None:
            self._values["schedule_end_date"] = schedule_end_date
        if start_time_of_day is not None:
            self._values["start_time_of_day"] = start_time_of_day

    @builtins.property
    def schedule_start_date(
        self,
    ) -> "GoogleStorageTransferJobScheduleScheduleStartDate":
        '''schedule_start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_start_date GoogleStorageTransferJob#schedule_start_date}
        '''
        result = self._values.get("schedule_start_date")
        assert result is not None, "Required property 'schedule_start_date' is missing"
        return typing.cast("GoogleStorageTransferJobScheduleScheduleStartDate", result)

    @builtins.property
    def repeat_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between the start of each scheduled transfer.

        If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#repeat_interval GoogleStorageTransferJob#repeat_interval}
        '''
        result = self._values.get("repeat_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_end_date(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobScheduleScheduleEndDate"]:
        '''schedule_end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#schedule_end_date GoogleStorageTransferJob#schedule_end_date}
        '''
        result = self._values.get("schedule_end_date")
        return typing.cast(typing.Optional["GoogleStorageTransferJobScheduleScheduleEndDate"], result)

    @builtins.property
    def start_time_of_day(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobScheduleStartTimeOfDay"]:
        '''start_time_of_day block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#start_time_of_day GoogleStorageTransferJob#start_time_of_day}
        '''
        result = self._values.get("start_time_of_day")
        return typing.cast(typing.Optional["GoogleStorageTransferJobScheduleStartTimeOfDay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07bc2c2fa39b8d358d108a5bfeb7ae7b779df16b8920c0328f210ddfa16b378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScheduleEndDate")
    def put_schedule_end_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        value = GoogleStorageTransferJobScheduleScheduleEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleEndDate", [value]))

    @jsii.member(jsii_name="putScheduleStartDate")
    def put_schedule_start_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        value = GoogleStorageTransferJobScheduleScheduleStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleStartDate", [value]))

    @jsii.member(jsii_name="putStartTimeOfDay")
    def put_start_time_of_day(
        self,
        *,
        hours: jsii.Number,
        minutes: jsii.Number,
        nanos: jsii.Number,
        seconds: jsii.Number,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#hours GoogleStorageTransferJob#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#minutes GoogleStorageTransferJob#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#nanos GoogleStorageTransferJob#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#seconds GoogleStorageTransferJob#seconds}
        '''
        value = GoogleStorageTransferJobScheduleStartTimeOfDay(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTimeOfDay", [value]))

    @jsii.member(jsii_name="resetRepeatInterval")
    def reset_repeat_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepeatInterval", []))

    @jsii.member(jsii_name="resetScheduleEndDate")
    def reset_schedule_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleEndDate", []))

    @jsii.member(jsii_name="resetStartTimeOfDay")
    def reset_start_time_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOfDay", []))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndDate")
    def schedule_end_date(
        self,
    ) -> "GoogleStorageTransferJobScheduleScheduleEndDateOutputReference":
        return typing.cast("GoogleStorageTransferJobScheduleScheduleEndDateOutputReference", jsii.get(self, "scheduleEndDate"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartDate")
    def schedule_start_date(
        self,
    ) -> "GoogleStorageTransferJobScheduleScheduleStartDateOutputReference":
        return typing.cast("GoogleStorageTransferJobScheduleScheduleStartDateOutputReference", jsii.get(self, "scheduleStartDate"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDay")
    def start_time_of_day(
        self,
    ) -> "GoogleStorageTransferJobScheduleStartTimeOfDayOutputReference":
        return typing.cast("GoogleStorageTransferJobScheduleStartTimeOfDayOutputReference", jsii.get(self, "startTimeOfDay"))

    @builtins.property
    @jsii.member(jsii_name="repeatIntervalInput")
    def repeat_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repeatIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndDateInput")
    def schedule_end_date_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobScheduleScheduleEndDate"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobScheduleScheduleEndDate"], jsii.get(self, "scheduleEndDateInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartDateInput")
    def schedule_start_date_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobScheduleScheduleStartDate"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobScheduleScheduleStartDate"], jsii.get(self, "scheduleStartDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDayInput")
    def start_time_of_day_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobScheduleStartTimeOfDay"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobScheduleStartTimeOfDay"], jsii.get(self, "startTimeOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="repeatInterval")
    def repeat_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repeatInterval"))

    @repeat_interval.setter
    def repeat_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c509258eadd33ead14fc5d7fefa04962753f11c7403a7d880db6331713ccc7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repeatInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageTransferJobSchedule]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62807e5ece83216e92a848cfec4bc5a3b1c53c40366e55536bef0f2ee75edd03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleScheduleEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleStorageTransferJobScheduleScheduleEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01a550ee8e1c80b8ba882079e7d6ac074149ff46981ba6c32e8a210ee3f0b82)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobScheduleScheduleEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobScheduleScheduleEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleScheduleEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08dea72d4f2339cf682cf6c90f4c848590417c8aa21a84571dba36cb33ffd7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e907225462bfb75752b8b45636c9523fd6f9c08fec4f2d7f2df0a868ceed01e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f721120a65e78c6aecf30b685fc36d887c972d0bf81aeb8efee8310f51f47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bae4a9ad8413916aaf074e8a1f651a9a772c435246f2ee04604cd4ac3e6ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobScheduleScheduleEndDate]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobScheduleScheduleEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobScheduleScheduleEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fe2669881a7c9f67912fb85e743db40109c3e29433ff846b7af4126af09ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleScheduleStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleStorageTransferJobScheduleScheduleStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a552b715d0d676bcd53e353c7b7680587c3c58bcb1e3f485f8784db7f8fa703)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#day GoogleStorageTransferJob#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#month GoogleStorageTransferJob#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#year GoogleStorageTransferJob#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobScheduleScheduleStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobScheduleScheduleStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleScheduleStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22d54c05efdbdebac8becb1368a543e4b52990a4355669d37e8ec8fd29de09c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd701485719fca5c5eb3e8a2b917e7f1684cbe0d37ac483393a4234ff2acc051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9436b63f0113ed2bb767623bec1183103476d8b237d799aace375a906ab1aa23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652e8b6c784545a3135a381919ddddc6c687d7f038351e4a8fbd8dc2e479bf33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobScheduleScheduleStartDate]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobScheduleScheduleStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobScheduleScheduleStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47893ac92d3364b3609267d1a6085944527f3a7a7f393215a98ab471b7296dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleStartTimeOfDay",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleStorageTransferJobScheduleStartTimeOfDay:
    def __init__(
        self,
        *,
        hours: jsii.Number,
        minutes: jsii.Number,
        nanos: jsii.Number,
        seconds: jsii.Number,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#hours GoogleStorageTransferJob#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#minutes GoogleStorageTransferJob#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#nanos GoogleStorageTransferJob#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#seconds GoogleStorageTransferJob#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80463f09043d691af86c1773a0e02c1b9b345a3a2a5484463861bfbfe2c2008)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
            "minutes": minutes,
            "nanos": nanos,
            "seconds": seconds,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#hours GoogleStorageTransferJob#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minutes(self) -> jsii.Number:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#minutes GoogleStorageTransferJob#minutes}
        '''
        result = self._values.get("minutes")
        assert result is not None, "Required property 'minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> jsii.Number:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#nanos GoogleStorageTransferJob#nanos}
        '''
        result = self._values.get("nanos")
        assert result is not None, "Required property 'nanos' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#seconds GoogleStorageTransferJob#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobScheduleStartTimeOfDay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobScheduleStartTimeOfDayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobScheduleStartTimeOfDayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__217b342b10f0a405a000e2d33dbc7b948f211d7b9929d3172d51b8c48efcd6da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e6129c5918d9df0237ca41c8bc6709ca83c02e3ca3d3350745e27ccb56fe98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548974be57345c56527d47879d22ff6955e7140c3f5b327ce2c44d876364a78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f88ad526355e879d0f66739b56a0e56d4ff79ba772cac9f2f9c6d52e2c24a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b234f0d4723a20a97b5e554ecebbb561bfb634fa801fb6fadc093b4bf6ee36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobScheduleStartTimeOfDay]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobScheduleStartTimeOfDay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobScheduleStartTimeOfDay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a140dc575737a7b44b96eee92b537340e60f662e4cc8020f98383e4a018eb6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpec",
    jsii_struct_bases=[],
    name_mapping={
        "aws_s3_data_source": "awsS3DataSource",
        "azure_blob_storage_data_source": "azureBlobStorageDataSource",
        "gcs_data_sink": "gcsDataSink",
        "gcs_data_source": "gcsDataSource",
        "http_data_source": "httpDataSource",
        "object_conditions": "objectConditions",
        "posix_data_sink": "posixDataSink",
        "posix_data_source": "posixDataSource",
        "sink_agent_pool_name": "sinkAgentPoolName",
        "source_agent_pool_name": "sourceAgentPoolName",
        "transfer_options": "transferOptions",
    },
)
class GoogleStorageTransferJobTransferSpec:
    def __init__(
        self,
        *,
        aws_s3_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAwsS3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_sink: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        http_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecHttpDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_sink: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecPosixDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_source: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecPosixDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        sink_agent_pool_name: typing.Optional[builtins.str] = None,
        source_agent_pool_name: typing.Optional[builtins.str] = None,
        transfer_options: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_s3_data_source: aws_s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_s3_data_source GoogleStorageTransferJob#aws_s3_data_source}
        :param azure_blob_storage_data_source: azure_blob_storage_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_blob_storage_data_source GoogleStorageTransferJob#azure_blob_storage_data_source}
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_sink GoogleStorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_source GoogleStorageTransferJob#gcs_data_source}
        :param http_data_source: http_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#http_data_source GoogleStorageTransferJob#http_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#object_conditions GoogleStorageTransferJob#object_conditions}
        :param posix_data_sink: posix_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_sink GoogleStorageTransferJob#posix_data_sink}
        :param posix_data_source: posix_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_source GoogleStorageTransferJob#posix_data_source}
        :param sink_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sink_agent_pool_name GoogleStorageTransferJob#sink_agent_pool_name}
        :param source_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#source_agent_pool_name GoogleStorageTransferJob#source_agent_pool_name}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_options GoogleStorageTransferJob#transfer_options}
        '''
        if isinstance(aws_s3_data_source, dict):
            aws_s3_data_source = GoogleStorageTransferJobTransferSpecAwsS3DataSource(**aws_s3_data_source)
        if isinstance(azure_blob_storage_data_source, dict):
            azure_blob_storage_data_source = GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource(**azure_blob_storage_data_source)
        if isinstance(gcs_data_sink, dict):
            gcs_data_sink = GoogleStorageTransferJobTransferSpecGcsDataSink(**gcs_data_sink)
        if isinstance(gcs_data_source, dict):
            gcs_data_source = GoogleStorageTransferJobTransferSpecGcsDataSource(**gcs_data_source)
        if isinstance(http_data_source, dict):
            http_data_source = GoogleStorageTransferJobTransferSpecHttpDataSource(**http_data_source)
        if isinstance(object_conditions, dict):
            object_conditions = GoogleStorageTransferJobTransferSpecObjectConditions(**object_conditions)
        if isinstance(posix_data_sink, dict):
            posix_data_sink = GoogleStorageTransferJobTransferSpecPosixDataSink(**posix_data_sink)
        if isinstance(posix_data_source, dict):
            posix_data_source = GoogleStorageTransferJobTransferSpecPosixDataSource(**posix_data_source)
        if isinstance(transfer_options, dict):
            transfer_options = GoogleStorageTransferJobTransferSpecTransferOptions(**transfer_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616e0879a2a9378c34a7d8f5ad35ca6a4fb3467b52db8451be19bef266ba2701)
            check_type(argname="argument aws_s3_data_source", value=aws_s3_data_source, expected_type=type_hints["aws_s3_data_source"])
            check_type(argname="argument azure_blob_storage_data_source", value=azure_blob_storage_data_source, expected_type=type_hints["azure_blob_storage_data_source"])
            check_type(argname="argument gcs_data_sink", value=gcs_data_sink, expected_type=type_hints["gcs_data_sink"])
            check_type(argname="argument gcs_data_source", value=gcs_data_source, expected_type=type_hints["gcs_data_source"])
            check_type(argname="argument http_data_source", value=http_data_source, expected_type=type_hints["http_data_source"])
            check_type(argname="argument object_conditions", value=object_conditions, expected_type=type_hints["object_conditions"])
            check_type(argname="argument posix_data_sink", value=posix_data_sink, expected_type=type_hints["posix_data_sink"])
            check_type(argname="argument posix_data_source", value=posix_data_source, expected_type=type_hints["posix_data_source"])
            check_type(argname="argument sink_agent_pool_name", value=sink_agent_pool_name, expected_type=type_hints["sink_agent_pool_name"])
            check_type(argname="argument source_agent_pool_name", value=source_agent_pool_name, expected_type=type_hints["source_agent_pool_name"])
            check_type(argname="argument transfer_options", value=transfer_options, expected_type=type_hints["transfer_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_s3_data_source is not None:
            self._values["aws_s3_data_source"] = aws_s3_data_source
        if azure_blob_storage_data_source is not None:
            self._values["azure_blob_storage_data_source"] = azure_blob_storage_data_source
        if gcs_data_sink is not None:
            self._values["gcs_data_sink"] = gcs_data_sink
        if gcs_data_source is not None:
            self._values["gcs_data_source"] = gcs_data_source
        if http_data_source is not None:
            self._values["http_data_source"] = http_data_source
        if object_conditions is not None:
            self._values["object_conditions"] = object_conditions
        if posix_data_sink is not None:
            self._values["posix_data_sink"] = posix_data_sink
        if posix_data_source is not None:
            self._values["posix_data_source"] = posix_data_source
        if sink_agent_pool_name is not None:
            self._values["sink_agent_pool_name"] = sink_agent_pool_name
        if source_agent_pool_name is not None:
            self._values["source_agent_pool_name"] = source_agent_pool_name
        if transfer_options is not None:
            self._values["transfer_options"] = transfer_options

    @builtins.property
    def aws_s3_data_source(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecAwsS3DataSource"]:
        '''aws_s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_s3_data_source GoogleStorageTransferJob#aws_s3_data_source}
        '''
        result = self._values.get("aws_s3_data_source")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecAwsS3DataSource"], result)

    @builtins.property
    def azure_blob_storage_data_source(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource"]:
        '''azure_blob_storage_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_blob_storage_data_source GoogleStorageTransferJob#azure_blob_storage_data_source}
        '''
        result = self._values.get("azure_blob_storage_data_source")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource"], result)

    @builtins.property
    def gcs_data_sink(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecGcsDataSink"]:
        '''gcs_data_sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_sink GoogleStorageTransferJob#gcs_data_sink}
        '''
        result = self._values.get("gcs_data_sink")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecGcsDataSink"], result)

    @builtins.property
    def gcs_data_source(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecGcsDataSource"]:
        '''gcs_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#gcs_data_source GoogleStorageTransferJob#gcs_data_source}
        '''
        result = self._values.get("gcs_data_source")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecGcsDataSource"], result)

    @builtins.property
    def http_data_source(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecHttpDataSource"]:
        '''http_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#http_data_source GoogleStorageTransferJob#http_data_source}
        '''
        result = self._values.get("http_data_source")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecHttpDataSource"], result)

    @builtins.property
    def object_conditions(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecObjectConditions"]:
        '''object_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#object_conditions GoogleStorageTransferJob#object_conditions}
        '''
        result = self._values.get("object_conditions")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecObjectConditions"], result)

    @builtins.property
    def posix_data_sink(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSink"]:
        '''posix_data_sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_sink GoogleStorageTransferJob#posix_data_sink}
        '''
        result = self._values.get("posix_data_sink")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSink"], result)

    @builtins.property
    def posix_data_source(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSource"]:
        '''posix_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#posix_data_source GoogleStorageTransferJob#posix_data_source}
        '''
        result = self._values.get("posix_data_source")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSource"], result)

    @builtins.property
    def sink_agent_pool_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sink_agent_pool_name GoogleStorageTransferJob#sink_agent_pool_name}
        '''
        result = self._values.get("sink_agent_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_agent_pool_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#source_agent_pool_name GoogleStorageTransferJob#source_agent_pool_name}
        '''
        result = self._values.get("source_agent_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_options(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecTransferOptions"]:
        '''transfer_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#transfer_options GoogleStorageTransferJob#transfer_options}
        '''
        result = self._values.get("transfer_options")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecTransferOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAwsS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "aws_access_key": "awsAccessKey",
        "path": "path",
        "role_arn": "roleArn",
    },
)
class GoogleStorageTransferJobTransferSpecAwsS3DataSource:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        aws_access_key: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: S3 Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param aws_access_key: aws_access_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_access_key GoogleStorageTransferJob#aws_access_key}
        :param path: S3 Bucket path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        :param role_arn: The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'. For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#role_arn GoogleStorageTransferJob#role_arn}
        '''
        if isinstance(aws_access_key, dict):
            aws_access_key = GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(**aws_access_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aef2d6377b055ff6790b534ba4568f9597c275b67aed9780e928b17d73a633f)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument aws_access_key", value=aws_access_key, expected_type=type_hints["aws_access_key"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if aws_access_key is not None:
            self._values["aws_access_key"] = aws_access_key
        if path is not None:
            self._values["path"] = path
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''S3 Bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_key(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey"]:
        '''aws_access_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_access_key GoogleStorageTransferJob#aws_access_key}
        '''
        result = self._values.get("aws_access_key")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''S3 Bucket path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'.

        For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#role_arn GoogleStorageTransferJob#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecAwsS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
    },
)
class GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: AWS Key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#access_key_id GoogleStorageTransferJob#access_key_id}
        :param secret_access_key: AWS Secret Access Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#secret_access_key GoogleStorageTransferJob#secret_access_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ccb74f9b8a89b13c42895c2a0556cabe96e5993a842cd280d109f34330449f)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''AWS Key ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#access_key_id GoogleStorageTransferJob#access_key_id}
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''AWS Secret Access Key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#secret_access_key GoogleStorageTransferJob#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2c6953dfddc4d647904d38b7e127801d0320516bf98b5abf739b64d52907bf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab25f7dd20e2eebb94d1932701fce6a6c9911474f7e21dea831030148ba5b24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ab122bec315bc35d438f8a7bdcd2669dadec8bd567525761d10d732f7ca139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26abbbfe14fa0a8922f4fe0d7b5ba9559d94d7f0175a3c3bcc956e7f80689686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageTransferJobTransferSpecAwsS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAwsS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ad893462683b0eb28ec8eabbf7d1dfe2e2c2334d774b005dfd8169f025ffce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsAccessKey")
    def put_aws_access_key(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: AWS Key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#access_key_id GoogleStorageTransferJob#access_key_id}
        :param secret_access_key: AWS Secret Access Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#secret_access_key GoogleStorageTransferJob#secret_access_key}
        '''
        value = GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(
            access_key_id=access_key_id, secret_access_key=secret_access_key
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAccessKey", [value]))

    @jsii.member(jsii_name="resetAwsAccessKey")
    def reset_aws_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccessKey", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKey")
    def aws_access_key(
        self,
    ) -> GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference, jsii.get(self, "awsAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeyInput")
    def aws_access_key_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey], jsii.get(self, "awsAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f845352251bd66143645e77d98b50cbbf460e3a7a4ed612f189a645632d27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8262e32d55402c8096488bdfcaf2cfd4046693ef9daf99e205d3de8ad0ccb724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f82a4e1acb618b5b4098585124147e70305a7cc968a186d4420c0de2eafd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bd9787ffd218357229debd9a8c51e99999d981ac8238f099febb3b435911a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "storage_account": "storageAccount",
        "azure_credentials": "azureCredentials",
        "credentials_secret": "credentialsSecret",
        "path": "path",
    },
)
class GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource:
    def __init__(
        self,
        *,
        container: builtins.str,
        storage_account: builtins.str,
        azure_credentials: typing.Optional[typing.Union["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        credentials_secret: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container: The container to transfer from the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#container GoogleStorageTransferJob#container}
        :param storage_account: The name of the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#storage_account GoogleStorageTransferJob#storage_account}
        :param azure_credentials: azure_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_credentials GoogleStorageTransferJob#azure_credentials}
        :param credentials_secret: The Resource name of a secret in Secret Manager containing SAS Credentials in JSON form. Service Agent must have permissions to access secret. If credentials_secret is specified, do not specify azure_credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#credentials_secret GoogleStorageTransferJob#credentials_secret}
        :param path: Root path to transfer objects. Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        if isinstance(azure_credentials, dict):
            azure_credentials = GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(**azure_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed9b65c8c86aff57d5afbfb84bce37fa1f43b7bf5a2108471460c28399bb2e3)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument azure_credentials", value=azure_credentials, expected_type=type_hints["azure_credentials"])
            check_type(argname="argument credentials_secret", value=credentials_secret, expected_type=type_hints["credentials_secret"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
            "storage_account": storage_account,
        }
        if azure_credentials is not None:
            self._values["azure_credentials"] = azure_credentials
        if credentials_secret is not None:
            self._values["credentials_secret"] = credentials_secret
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def container(self) -> builtins.str:
        '''The container to transfer from the Azure Storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#container GoogleStorageTransferJob#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> builtins.str:
        '''The name of the Azure Storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#storage_account GoogleStorageTransferJob#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_credentials(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials"]:
        '''azure_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_credentials GoogleStorageTransferJob#azure_credentials}
        '''
        result = self._values.get("azure_credentials")
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials"], result)

    @builtins.property
    def credentials_secret(self) -> typing.Optional[builtins.str]:
        '''The Resource name of a secret in Secret Manager containing SAS Credentials in JSON form.

        Service Agent must have permissions to access secret. If credentials_secret is specified, do not specify azure_credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#credentials_secret GoogleStorageTransferJob#credentials_secret}
        '''
        result = self._values.get("credentials_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Root path to transfer objects.

        Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials",
    jsii_struct_bases=[],
    name_mapping={"sas_token": "sasToken"},
)
class GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials:
    def __init__(self, *, sas_token: builtins.str) -> None:
        '''
        :param sas_token: Azure shared access signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sas_token GoogleStorageTransferJob#sas_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c5c3b7cc29e1c081f87271aadb74392784a5124686177d7ec71498734f3cb9)
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sas_token": sas_token,
        }

    @builtins.property
    def sas_token(self) -> builtins.str:
        '''Azure shared access signature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sas_token GoogleStorageTransferJob#sas_token}
        '''
        result = self._values.get("sas_token")
        assert result is not None, "Required property 'sas_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__949e518ef7bae1ff13324fb3cd8f2975300a582bfc8771a1b2ccba565666f403)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebb0eaabf107dd89d2e6e29a55941b428c834915fe8573a8783394202fcde2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb59e2aeca6bf8d57fec91596065e7cd3a736383910346805ba974243190dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51a320623d57b734112f626e6dc5272e78792595588d5f37e3572992527f6396)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureCredentials")
    def put_azure_credentials(self, *, sas_token: builtins.str) -> None:
        '''
        :param sas_token: Azure shared access signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#sas_token GoogleStorageTransferJob#sas_token}
        '''
        value = GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(
            sas_token=sas_token
        )

        return typing.cast(None, jsii.invoke(self, "putAzureCredentials", [value]))

    @jsii.member(jsii_name="resetAzureCredentials")
    def reset_azure_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureCredentials", []))

    @jsii.member(jsii_name="resetCredentialsSecret")
    def reset_credentials_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialsSecret", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="azureCredentials")
    def azure_credentials(
        self,
    ) -> GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference, jsii.get(self, "azureCredentials"))

    @builtins.property
    @jsii.member(jsii_name="azureCredentialsInput")
    def azure_credentials_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials], jsii.get(self, "azureCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsSecretInput")
    def credentials_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a861ace8b1ebde3f5ec19e50ad964b12deea0f3701b9f105ee83f842bda89fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialsSecret")
    def credentials_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialsSecret"))

    @credentials_secret.setter
    def credentials_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dbcd63868946ab7f8b7a7ad6798307d3dd3eb795be51bb9ed6a03d0177e83b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf54e38e934621decd67ea57f1ac3310fb4ed4118a8708e40e3ab1809aefdaf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccount"))

    @storage_account.setter
    def storage_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae352d4029345f0efe7aa3d0f60b15bee48bd093f956f683c5940a5a71324fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f396c6b1ad68a99cfcd831e0394f3858e18d9bc5334e02bd2e23f6cb9e12ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecGcsDataSink",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class GoogleStorageTransferJobTransferSpecGcsDataSink:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b1e4645fd1b23fdcffb06411b264965342108ed8494b697479a863b360019c)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecGcsDataSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecGcsDataSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecGcsDataSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e17c0a0aae97d43fab55bd845b75ee7e88dc41bfc9a772a13b9fbb6af23194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee94ffc058d9fc40225f073bb0d606d65a3e13c39ece357f29c363f12abbfc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec529a4e1bdfc48911764b1a1dc04eaf0169df451157dfb5de8b45a740cf3bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3c0a2bfac6f30f96fe952eddb1dfd532cb22e477ba6f8d48e1a22f9eeb39a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecGcsDataSource",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class GoogleStorageTransferJobTransferSpecGcsDataSource:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e81d9f521306ea6bf326c8210b90856d550d6dd555a4ae4228b8a461095169)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecGcsDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecGcsDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecGcsDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48e03fa781f7d856f53d2d63aaf4b1573dadf4a04c9041282092f3aeee40041f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe65f5c105e9b9a06ae8b85f5446b8b64737db1026cb7a97cfa2a3031336f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd0db4b4fa17bee7deda5bf911e74213ee4aeb4757257e391d4c0a8632160fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb2a6faa4b36cd633c6a3e142c9e1bc805319ac84eaa3e4b702493d3235f1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecHttpDataSource",
    jsii_struct_bases=[],
    name_mapping={"list_url": "listUrl"},
)
class GoogleStorageTransferJobTransferSpecHttpDataSource:
    def __init__(self, *, list_url: builtins.str) -> None:
        '''
        :param list_url: The URL that points to the file that stores the object list entries. This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#list_url GoogleStorageTransferJob#list_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5a5633ddc033bb451ef0be9ddf4ff149bb98006fcd3493c3727ae06145b822)
            check_type(argname="argument list_url", value=list_url, expected_type=type_hints["list_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "list_url": list_url,
        }

    @builtins.property
    def list_url(self) -> builtins.str:
        '''The URL that points to the file that stores the object list entries.

        This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#list_url GoogleStorageTransferJob#list_url}
        '''
        result = self._values.get("list_url")
        assert result is not None, "Required property 'list_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecHttpDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecHttpDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecHttpDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfdce3890b8364e0d9ca488d9c1f91e787a985ff88125ad121f44ef44385b0f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listUrlInput")
    def list_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="listUrl")
    def list_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listUrl"))

    @list_url.setter
    def list_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612df7815db80bc1b11137041632f6b4c61f4c2256b0259bd33758f138fb9352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0af0757ec57f612aaccba203193f3d46fdc2c94c82c852cf46a97a258aeecb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecObjectConditions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_prefixes": "excludePrefixes",
        "include_prefixes": "includePrefixes",
        "last_modified_before": "lastModifiedBefore",
        "last_modified_since": "lastModifiedSince",
        "max_time_elapsed_since_last_modification": "maxTimeElapsedSinceLastModification",
        "min_time_elapsed_since_last_modification": "minTimeElapsedSinceLastModification",
    },
)
class GoogleStorageTransferJobTransferSpecObjectConditions:
    def __init__(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#exclude_prefixes GoogleStorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#include_prefixes GoogleStorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_before GoogleStorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_since GoogleStorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#max_time_elapsed_since_last_modification GoogleStorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#min_time_elapsed_since_last_modification GoogleStorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2575f1467704aec9e2c1173755a35cd61fa0f2af17dc930cc852340e35ff58f8)
            check_type(argname="argument exclude_prefixes", value=exclude_prefixes, expected_type=type_hints["exclude_prefixes"])
            check_type(argname="argument include_prefixes", value=include_prefixes, expected_type=type_hints["include_prefixes"])
            check_type(argname="argument last_modified_before", value=last_modified_before, expected_type=type_hints["last_modified_before"])
            check_type(argname="argument last_modified_since", value=last_modified_since, expected_type=type_hints["last_modified_since"])
            check_type(argname="argument max_time_elapsed_since_last_modification", value=max_time_elapsed_since_last_modification, expected_type=type_hints["max_time_elapsed_since_last_modification"])
            check_type(argname="argument min_time_elapsed_since_last_modification", value=min_time_elapsed_since_last_modification, expected_type=type_hints["min_time_elapsed_since_last_modification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_prefixes is not None:
            self._values["exclude_prefixes"] = exclude_prefixes
        if include_prefixes is not None:
            self._values["include_prefixes"] = include_prefixes
        if last_modified_before is not None:
            self._values["last_modified_before"] = last_modified_before
        if last_modified_since is not None:
            self._values["last_modified_since"] = last_modified_since
        if max_time_elapsed_since_last_modification is not None:
            self._values["max_time_elapsed_since_last_modification"] = max_time_elapsed_since_last_modification
        if min_time_elapsed_since_last_modification is not None:
            self._values["min_time_elapsed_since_last_modification"] = min_time_elapsed_since_last_modification

    @builtins.property
    def exclude_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''exclude_prefixes must follow the requirements described for include_prefixes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#exclude_prefixes GoogleStorageTransferJob#exclude_prefixes}
        '''
        result = self._values.get("exclude_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes.

        If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#include_prefixes GoogleStorageTransferJob#include_prefixes}
        '''
        result = self._values.get("include_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def last_modified_before(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_before GoogleStorageTransferJob#last_modified_before}
        '''
        result = self._values.get("last_modified_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_modified_since(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_since GoogleStorageTransferJob#last_modified_since}
        '''
        result = self._values.get("last_modified_since")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#max_time_elapsed_since_last_modification GoogleStorageTransferJob#max_time_elapsed_since_last_modification}
        '''
        result = self._values.get("max_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#min_time_elapsed_since_last_modification GoogleStorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        result = self._values.get("min_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecObjectConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecObjectConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecObjectConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c500f97908b8a5f4ca60e806cc92813fdfa2fe4866544a4a880e46827ef477a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludePrefixes")
    def reset_exclude_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludePrefixes", []))

    @jsii.member(jsii_name="resetIncludePrefixes")
    def reset_include_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePrefixes", []))

    @jsii.member(jsii_name="resetLastModifiedBefore")
    def reset_last_modified_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedBefore", []))

    @jsii.member(jsii_name="resetLastModifiedSince")
    def reset_last_modified_since(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedSince", []))

    @jsii.member(jsii_name="resetMaxTimeElapsedSinceLastModification")
    def reset_max_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTimeElapsedSinceLastModification", []))

    @jsii.member(jsii_name="resetMinTimeElapsedSinceLastModification")
    def reset_min_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTimeElapsedSinceLastModification", []))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixesInput")
    def exclude_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="includePrefixesInput")
    def include_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBeforeInput")
    def last_modified_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSinceInput")
    def last_modified_since_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedSinceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModificationInput")
    def max_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModificationInput")
    def min_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixes")
    def exclude_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePrefixes"))

    @exclude_prefixes.setter
    def exclude_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9d5cd2bcad23d15f346aef09f43a40ddb94a2b92adc7572a5f731537913da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePrefixes")
    def include_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePrefixes"))

    @include_prefixes.setter
    def include_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f50dc3a914a5f25ba48c690550f02b637558fcc558878676a6a734079a5e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBefore")
    def last_modified_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedBefore"))

    @last_modified_before.setter
    def last_modified_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7c1546891334558d52cb849f63896c284d933e7a477df1444726381ab46c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSince")
    def last_modified_since(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedSince"))

    @last_modified_since.setter
    def last_modified_since(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f84d245bae289dc0d1209968cc68f52bef632b20f3a113b0a86366b1ef8bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedSince", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModification")
    def max_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTimeElapsedSinceLastModification"))

    @max_time_elapsed_since_last_modification.setter
    def max_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4fcd0a9dd9820ff60623d520f7e350ecfb923cf2b27327e20906c96bb93720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModification")
    def min_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTimeElapsedSinceLastModification"))

    @min_time_elapsed_since_last_modification.setter
    def min_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604e0ad0f4b8f4a81b2921b49c6f282bb4ae05329cef6a57076847c6990c594b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2e0cff6c9e004028dade56006e76fd73e3203b12237b79c3802a349a4c6b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageTransferJobTransferSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c69e7ffa7a53bc54f5069ebcb36b13ca25a5ab3f43d57f263bb4c2467ef3fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsS3DataSource")
    def put_aws_s3_data_source(
        self,
        *,
        bucket_name: builtins.str,
        aws_access_key: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: S3 Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param aws_access_key: aws_access_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#aws_access_key GoogleStorageTransferJob#aws_access_key}
        :param path: S3 Bucket path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        :param role_arn: The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'. For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#role_arn GoogleStorageTransferJob#role_arn}
        '''
        value = GoogleStorageTransferJobTransferSpecAwsS3DataSource(
            bucket_name=bucket_name,
            aws_access_key=aws_access_key,
            path=path,
            role_arn=role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsS3DataSource", [value]))

    @jsii.member(jsii_name="putAzureBlobStorageDataSource")
    def put_azure_blob_storage_data_source(
        self,
        *,
        container: builtins.str,
        storage_account: builtins.str,
        azure_credentials: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        credentials_secret: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container: The container to transfer from the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#container GoogleStorageTransferJob#container}
        :param storage_account: The name of the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#storage_account GoogleStorageTransferJob#storage_account}
        :param azure_credentials: azure_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#azure_credentials GoogleStorageTransferJob#azure_credentials}
        :param credentials_secret: The Resource name of a secret in Secret Manager containing SAS Credentials in JSON form. Service Agent must have permissions to access secret. If credentials_secret is specified, do not specify azure_credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#credentials_secret GoogleStorageTransferJob#credentials_secret}
        :param path: Root path to transfer objects. Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        value = GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource(
            container=container,
            storage_account=storage_account,
            azure_credentials=azure_credentials,
            credentials_secret=credentials_secret,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureBlobStorageDataSource", [value]))

    @jsii.member(jsii_name="putGcsDataSink")
    def put_gcs_data_sink(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        value = GoogleStorageTransferJobTransferSpecGcsDataSink(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSink", [value]))

    @jsii.member(jsii_name="putGcsDataSource")
    def put_gcs_data_source(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#bucket_name GoogleStorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#path GoogleStorageTransferJob#path}
        '''
        value = GoogleStorageTransferJobTransferSpecGcsDataSource(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSource", [value]))

    @jsii.member(jsii_name="putHttpDataSource")
    def put_http_data_source(self, *, list_url: builtins.str) -> None:
        '''
        :param list_url: The URL that points to the file that stores the object list entries. This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#list_url GoogleStorageTransferJob#list_url}
        '''
        value = GoogleStorageTransferJobTransferSpecHttpDataSource(list_url=list_url)

        return typing.cast(None, jsii.invoke(self, "putHttpDataSource", [value]))

    @jsii.member(jsii_name="putObjectConditions")
    def put_object_conditions(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#exclude_prefixes GoogleStorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#include_prefixes GoogleStorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_before GoogleStorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#last_modified_since GoogleStorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#max_time_elapsed_since_last_modification GoogleStorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#min_time_elapsed_since_last_modification GoogleStorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        value = GoogleStorageTransferJobTransferSpecObjectConditions(
            exclude_prefixes=exclude_prefixes,
            include_prefixes=include_prefixes,
            last_modified_before=last_modified_before,
            last_modified_since=last_modified_since,
            max_time_elapsed_since_last_modification=max_time_elapsed_since_last_modification,
            min_time_elapsed_since_last_modification=min_time_elapsed_since_last_modification,
        )

        return typing.cast(None, jsii.invoke(self, "putObjectConditions", [value]))

    @jsii.member(jsii_name="putPosixDataSink")
    def put_posix_data_sink(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        value = GoogleStorageTransferJobTransferSpecPosixDataSink(
            root_directory=root_directory
        )

        return typing.cast(None, jsii.invoke(self, "putPosixDataSink", [value]))

    @jsii.member(jsii_name="putPosixDataSource")
    def put_posix_data_source(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        value = GoogleStorageTransferJobTransferSpecPosixDataSource(
            root_directory=root_directory
        )

        return typing.cast(None, jsii.invoke(self, "putPosixDataSource", [value]))

    @jsii.member(jsii_name="putTransferOptions")
    def put_transfer_options(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_from_source_after_transfer GoogleStorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_unique_in_sink GoogleStorageTransferJob#delete_objects_unique_in_sink}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_objects_already_existing_in_sink GoogleStorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_when GoogleStorageTransferJob#overwrite_when}
        '''
        value = GoogleStorageTransferJobTransferSpecTransferOptions(
            delete_objects_from_source_after_transfer=delete_objects_from_source_after_transfer,
            delete_objects_unique_in_sink=delete_objects_unique_in_sink,
            overwrite_objects_already_existing_in_sink=overwrite_objects_already_existing_in_sink,
            overwrite_when=overwrite_when,
        )

        return typing.cast(None, jsii.invoke(self, "putTransferOptions", [value]))

    @jsii.member(jsii_name="resetAwsS3DataSource")
    def reset_aws_s3_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsS3DataSource", []))

    @jsii.member(jsii_name="resetAzureBlobStorageDataSource")
    def reset_azure_blob_storage_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureBlobStorageDataSource", []))

    @jsii.member(jsii_name="resetGcsDataSink")
    def reset_gcs_data_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSink", []))

    @jsii.member(jsii_name="resetGcsDataSource")
    def reset_gcs_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSource", []))

    @jsii.member(jsii_name="resetHttpDataSource")
    def reset_http_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpDataSource", []))

    @jsii.member(jsii_name="resetObjectConditions")
    def reset_object_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectConditions", []))

    @jsii.member(jsii_name="resetPosixDataSink")
    def reset_posix_data_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosixDataSink", []))

    @jsii.member(jsii_name="resetPosixDataSource")
    def reset_posix_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosixDataSource", []))

    @jsii.member(jsii_name="resetSinkAgentPoolName")
    def reset_sink_agent_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSinkAgentPoolName", []))

    @jsii.member(jsii_name="resetSourceAgentPoolName")
    def reset_source_agent_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAgentPoolName", []))

    @jsii.member(jsii_name="resetTransferOptions")
    def reset_transfer_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferOptions", []))

    @builtins.property
    @jsii.member(jsii_name="awsS3DataSource")
    def aws_s3_data_source(
        self,
    ) -> GoogleStorageTransferJobTransferSpecAwsS3DataSourceOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecAwsS3DataSourceOutputReference, jsii.get(self, "awsS3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageDataSource")
    def azure_blob_storage_data_source(
        self,
    ) -> GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference, jsii.get(self, "azureBlobStorageDataSource"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSink")
    def gcs_data_sink(
        self,
    ) -> GoogleStorageTransferJobTransferSpecGcsDataSinkOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecGcsDataSinkOutputReference, jsii.get(self, "gcsDataSink"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSource")
    def gcs_data_source(
        self,
    ) -> GoogleStorageTransferJobTransferSpecGcsDataSourceOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecGcsDataSourceOutputReference, jsii.get(self, "gcsDataSource"))

    @builtins.property
    @jsii.member(jsii_name="httpDataSource")
    def http_data_source(
        self,
    ) -> GoogleStorageTransferJobTransferSpecHttpDataSourceOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecHttpDataSourceOutputReference, jsii.get(self, "httpDataSource"))

    @builtins.property
    @jsii.member(jsii_name="objectConditions")
    def object_conditions(
        self,
    ) -> GoogleStorageTransferJobTransferSpecObjectConditionsOutputReference:
        return typing.cast(GoogleStorageTransferJobTransferSpecObjectConditionsOutputReference, jsii.get(self, "objectConditions"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSink")
    def posix_data_sink(
        self,
    ) -> "GoogleStorageTransferJobTransferSpecPosixDataSinkOutputReference":
        return typing.cast("GoogleStorageTransferJobTransferSpecPosixDataSinkOutputReference", jsii.get(self, "posixDataSink"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSource")
    def posix_data_source(
        self,
    ) -> "GoogleStorageTransferJobTransferSpecPosixDataSourceOutputReference":
        return typing.cast("GoogleStorageTransferJobTransferSpecPosixDataSourceOutputReference", jsii.get(self, "posixDataSource"))

    @builtins.property
    @jsii.member(jsii_name="transferOptions")
    def transfer_options(
        self,
    ) -> "GoogleStorageTransferJobTransferSpecTransferOptionsOutputReference":
        return typing.cast("GoogleStorageTransferJobTransferSpecTransferOptionsOutputReference", jsii.get(self, "transferOptions"))

    @builtins.property
    @jsii.member(jsii_name="awsS3DataSourceInput")
    def aws_s3_data_source_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource], jsii.get(self, "awsS3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageDataSourceInput")
    def azure_blob_storage_data_source_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource], jsii.get(self, "azureBlobStorageDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSinkInput")
    def gcs_data_sink_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink], jsii.get(self, "gcsDataSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSourceInput")
    def gcs_data_source_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource], jsii.get(self, "gcsDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="httpDataSourceInput")
    def http_data_source_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource], jsii.get(self, "httpDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="objectConditionsInput")
    def object_conditions_input(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions], jsii.get(self, "objectConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSinkInput")
    def posix_data_sink_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSink"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSink"], jsii.get(self, "posixDataSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSourceInput")
    def posix_data_source_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSource"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecPosixDataSource"], jsii.get(self, "posixDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sinkAgentPoolNameInput")
    def sink_agent_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sinkAgentPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAgentPoolNameInput")
    def source_agent_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceAgentPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="transferOptionsInput")
    def transfer_options_input(
        self,
    ) -> typing.Optional["GoogleStorageTransferJobTransferSpecTransferOptions"]:
        return typing.cast(typing.Optional["GoogleStorageTransferJobTransferSpecTransferOptions"], jsii.get(self, "transferOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sinkAgentPoolName")
    def sink_agent_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sinkAgentPoolName"))

    @sink_agent_pool_name.setter
    def sink_agent_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90e2a90dc28b117a3be92163bb86732a55bf8c7b747ef070a46d8eb4c24b3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sinkAgentPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceAgentPoolName")
    def source_agent_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceAgentPoolName"))

    @source_agent_pool_name.setter
    def source_agent_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa386a2c6177178fad31a304b477f90e3ac3d7d13c0f6e4ea60273aaf4672777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAgentPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageTransferJobTransferSpec]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f79dbb0337a0b682e91cdd6b0c2bacf82873de4c2ddcf332f60d6e772d05603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecPosixDataSink",
    jsii_struct_bases=[],
    name_mapping={"root_directory": "rootDirectory"},
)
class GoogleStorageTransferJobTransferSpecPosixDataSink:
    def __init__(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb3644bf93cead28304317aa48fa27ae7850b55e9e7e211045cd7a9c0c35ba2)
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "root_directory": root_directory,
        }

    @builtins.property
    def root_directory(self) -> builtins.str:
        '''Root directory path to the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        result = self._values.get("root_directory")
        assert result is not None, "Required property 'root_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecPosixDataSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecPosixDataSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecPosixDataSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090575c5e2f42b76d69bb33cfd346a6464de75e27ccec8756cc928d3ded63749)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="rootDirectoryInput")
    def root_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4396dfb5cc392d91c6f941983aa09a8aed73b64f84c0f828d4a2c297e09e41f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSink]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a411e5b9d60ada973e545a417a4e646cf2e910b4e6c4b02a765b89abef71c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecPosixDataSource",
    jsii_struct_bases=[],
    name_mapping={"root_directory": "rootDirectory"},
)
class GoogleStorageTransferJobTransferSpecPosixDataSource:
    def __init__(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7996fb301122e1242254057f1544a9f5e1ae540115d72d27ba2ff71b430607)
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "root_directory": root_directory,
        }

    @builtins.property
    def root_directory(self) -> builtins.str:
        '''Root directory path to the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#root_directory GoogleStorageTransferJob#root_directory}
        '''
        result = self._values.get("root_directory")
        assert result is not None, "Required property 'root_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecPosixDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecPosixDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecPosixDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda91551ccb182ae20413e4f785dac2e950ea5d3be8ff445bf9ca0d31d1f499b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="rootDirectoryInput")
    def root_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103eacf956ff3034985c179b61b40cc7ee6c6a0f3338eb1dd4f38edef04c2260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSource]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48084704fbf2911e9bcf5c5b7710e2652eb3db7302655532276cee6f460ec563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecTransferOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delete_objects_from_source_after_transfer": "deleteObjectsFromSourceAfterTransfer",
        "delete_objects_unique_in_sink": "deleteObjectsUniqueInSink",
        "overwrite_objects_already_existing_in_sink": "overwriteObjectsAlreadyExistingInSink",
        "overwrite_when": "overwriteWhen",
    },
)
class GoogleStorageTransferJobTransferSpecTransferOptions:
    def __init__(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_from_source_after_transfer GoogleStorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_unique_in_sink GoogleStorageTransferJob#delete_objects_unique_in_sink}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_objects_already_existing_in_sink GoogleStorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_when GoogleStorageTransferJob#overwrite_when}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ff029553bfa7d2e54698fe7a7e3504d37c99244ba2f25d3e85c269deacf187)
            check_type(argname="argument delete_objects_from_source_after_transfer", value=delete_objects_from_source_after_transfer, expected_type=type_hints["delete_objects_from_source_after_transfer"])
            check_type(argname="argument delete_objects_unique_in_sink", value=delete_objects_unique_in_sink, expected_type=type_hints["delete_objects_unique_in_sink"])
            check_type(argname="argument overwrite_objects_already_existing_in_sink", value=overwrite_objects_already_existing_in_sink, expected_type=type_hints["overwrite_objects_already_existing_in_sink"])
            check_type(argname="argument overwrite_when", value=overwrite_when, expected_type=type_hints["overwrite_when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_objects_from_source_after_transfer is not None:
            self._values["delete_objects_from_source_after_transfer"] = delete_objects_from_source_after_transfer
        if delete_objects_unique_in_sink is not None:
            self._values["delete_objects_unique_in_sink"] = delete_objects_unique_in_sink
        if overwrite_objects_already_existing_in_sink is not None:
            self._values["overwrite_objects_already_existing_in_sink"] = overwrite_objects_already_existing_in_sink
        if overwrite_when is not None:
            self._values["overwrite_when"] = overwrite_when

    @builtins.property
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects should be deleted from the source after they are transferred to the sink.

        Note that this option and delete_objects_unique_in_sink are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_from_source_after_transfer GoogleStorageTransferJob#delete_objects_from_source_after_transfer}
        '''
        result = self._values.get("delete_objects_from_source_after_transfer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects that exist only in the sink should be deleted.

        Note that this option and delete_objects_from_source_after_transfer are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#delete_objects_unique_in_sink GoogleStorageTransferJob#delete_objects_unique_in_sink}
        '''
        result = self._values.get("delete_objects_unique_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether overwriting objects that already exist in the sink is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_objects_already_existing_in_sink GoogleStorageTransferJob#overwrite_objects_already_existing_in_sink}
        '''
        result = self._values.get("overwrite_objects_already_existing_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overwrite_when(self) -> typing.Optional[builtins.str]:
        '''When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.13.0/docs/resources/google_storage_transfer_job#overwrite_when GoogleStorageTransferJob#overwrite_when}
        '''
        result = self._values.get("overwrite_when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageTransferJobTransferSpecTransferOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageTransferJobTransferSpecTransferOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageTransferJob.GoogleStorageTransferJobTransferSpecTransferOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad360481c71d6c897ef73ab768b4e628498e29be2c4a105b838360848a0a1b29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeleteObjectsFromSourceAfterTransfer")
    def reset_delete_objects_from_source_after_transfer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsFromSourceAfterTransfer", []))

    @jsii.member(jsii_name="resetDeleteObjectsUniqueInSink")
    def reset_delete_objects_unique_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsUniqueInSink", []))

    @jsii.member(jsii_name="resetOverwriteObjectsAlreadyExistingInSink")
    def reset_overwrite_objects_already_existing_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteObjectsAlreadyExistingInSink", []))

    @jsii.member(jsii_name="resetOverwriteWhen")
    def reset_overwrite_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteWhen", []))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransferInput")
    def delete_objects_from_source_after_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsFromSourceAfterTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSinkInput")
    def delete_objects_unique_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsUniqueInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSinkInput")
    def overwrite_objects_already_existing_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteObjectsAlreadyExistingInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteWhenInput")
    def overwrite_when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteWhenInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransfer")
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsFromSourceAfterTransfer"))

    @delete_objects_from_source_after_transfer.setter
    def delete_objects_from_source_after_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417baa8561029f0b93035da97899ac224896596ff2924b9d8536fe241d32bc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsFromSourceAfterTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSink")
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsUniqueInSink"))

    @delete_objects_unique_in_sink.setter
    def delete_objects_unique_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009f973070f6bb56c0284396d157f9d661e5f3b8de9c2681698e06e47ebdb096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsUniqueInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSink")
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteObjectsAlreadyExistingInSink"))

    @overwrite_objects_already_existing_in_sink.setter
    def overwrite_objects_already_existing_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a159faebecc0434f9c008238895f55b848144930e5561bd224f8392e4c71e888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteObjectsAlreadyExistingInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteWhen")
    def overwrite_when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteWhen"))

    @overwrite_when.setter
    def overwrite_when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aff5832a5c4c8898235b9bc9bacd54afa036daa48e467ce42a4683106a66b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteWhen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageTransferJobTransferSpecTransferOptions]:
        return typing.cast(typing.Optional[GoogleStorageTransferJobTransferSpecTransferOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageTransferJobTransferSpecTransferOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cab6d612a96a2230201f81e563682cf32ae82773e1206a3b7f06cc03f7c9986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageTransferJob",
    "GoogleStorageTransferJobConfig",
    "GoogleStorageTransferJobEventStream",
    "GoogleStorageTransferJobEventStreamOutputReference",
    "GoogleStorageTransferJobNotificationConfig",
    "GoogleStorageTransferJobNotificationConfigOutputReference",
    "GoogleStorageTransferJobSchedule",
    "GoogleStorageTransferJobScheduleOutputReference",
    "GoogleStorageTransferJobScheduleScheduleEndDate",
    "GoogleStorageTransferJobScheduleScheduleEndDateOutputReference",
    "GoogleStorageTransferJobScheduleScheduleStartDate",
    "GoogleStorageTransferJobScheduleScheduleStartDateOutputReference",
    "GoogleStorageTransferJobScheduleStartTimeOfDay",
    "GoogleStorageTransferJobScheduleStartTimeOfDayOutputReference",
    "GoogleStorageTransferJobTransferSpec",
    "GoogleStorageTransferJobTransferSpecAwsS3DataSource",
    "GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey",
    "GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference",
    "GoogleStorageTransferJobTransferSpecAwsS3DataSourceOutputReference",
    "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource",
    "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials",
    "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference",
    "GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference",
    "GoogleStorageTransferJobTransferSpecGcsDataSink",
    "GoogleStorageTransferJobTransferSpecGcsDataSinkOutputReference",
    "GoogleStorageTransferJobTransferSpecGcsDataSource",
    "GoogleStorageTransferJobTransferSpecGcsDataSourceOutputReference",
    "GoogleStorageTransferJobTransferSpecHttpDataSource",
    "GoogleStorageTransferJobTransferSpecHttpDataSourceOutputReference",
    "GoogleStorageTransferJobTransferSpecObjectConditions",
    "GoogleStorageTransferJobTransferSpecObjectConditionsOutputReference",
    "GoogleStorageTransferJobTransferSpecOutputReference",
    "GoogleStorageTransferJobTransferSpecPosixDataSink",
    "GoogleStorageTransferJobTransferSpecPosixDataSinkOutputReference",
    "GoogleStorageTransferJobTransferSpecPosixDataSource",
    "GoogleStorageTransferJobTransferSpecPosixDataSourceOutputReference",
    "GoogleStorageTransferJobTransferSpecTransferOptions",
    "GoogleStorageTransferJobTransferSpecTransferOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__6aa0e6d9f40b0f4824748507a8f9bba74e07cf4b9f348b6149b4ffb41a4e7200(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    transfer_spec: typing.Union[GoogleStorageTransferJobTransferSpec, typing.Dict[builtins.str, typing.Any]],
    event_stream: typing.Optional[typing.Union[GoogleStorageTransferJobEventStream, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[GoogleStorageTransferJobNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[GoogleStorageTransferJobSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8abe485176e54191e1dddef5bb791535ed919838828f1ce783c01cb82241b337(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db30cb36b031ca871bd7d46f8831cdcf8734f566413c9844b53a73b51c4df569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480e69080926fc7d0d9b21c3bfa3a4ec6248fd91c18b6fb7ed12233e6c2d8be9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f63f58155b19562027f76abe83123a6a2aa7c8a7c7bec44c32d3b6773f0f302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7d4ad62350b3c194a289d29297af76990462f307e96499134ba2c4668ac5b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2e4e24b87eededac2893a4ac2e9dba06006d65831cff41eea86703a597a98a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c1d961b14a89391da0f77f62bcbf5af44420597571e86b0fb6e74fe20ac51a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    transfer_spec: typing.Union[GoogleStorageTransferJobTransferSpec, typing.Dict[builtins.str, typing.Any]],
    event_stream: typing.Optional[typing.Union[GoogleStorageTransferJobEventStream, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[GoogleStorageTransferJobNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[GoogleStorageTransferJobSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1637153c101c25686eeb4844f49b8302850868d3fe4fdd8abb297b18af39f828(
    *,
    name: builtins.str,
    event_stream_expiration_time: typing.Optional[builtins.str] = None,
    event_stream_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaea62fb9ca859d0e6fa2da45da2a4e3d32668bee179a3ace63a389c15cc0564(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddab4e173ed667d75268e866f267398704de9bc2315931e2c4caf34215aebc80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d3a48fcc8db54983539f7154c77fbe2f40d9d137f5a445d29ba56c9cebeda6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee7bd1ceed264a45fdfc1bbd7cb2c0aad822d246438ea38bf860f1836c5a3f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111da4b0023b46055621932ca349e5cfce3eed8682320082442138034336818e(
    value: typing.Optional[GoogleStorageTransferJobEventStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9867f8190484a9321b33a153b3119bfa913f102da67c563e0fd054d20edd23(
    *,
    payload_format: builtins.str,
    pubsub_topic: builtins.str,
    event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abb8dcf6c5e11610014734b0cd4a53ef3fff65082f0f817ff47d7b9ce8d5ea8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec01815146cf2e07b3d5a857a781c9d16c68ab2779b09a1999dc36da168cb462(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffafd908425725fd2c447ecab03082d18888deb01d56e9b1c12dc27e23a43fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d155d5cba211a1e4ac36a40ab9aef97f786f36434d8b7faafc1b86fed5ba4a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0626cc80d7484c5505b2eb7fbb223c9b2d95c485441c4432ec354d47ff587a(
    value: typing.Optional[GoogleStorageTransferJobNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0cfcd70190b0e8a99fca4e8453e5298f0df03efa255bda0df9d7e8cd22782a(
    *,
    schedule_start_date: typing.Union[GoogleStorageTransferJobScheduleScheduleStartDate, typing.Dict[builtins.str, typing.Any]],
    repeat_interval: typing.Optional[builtins.str] = None,
    schedule_end_date: typing.Optional[typing.Union[GoogleStorageTransferJobScheduleScheduleEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time_of_day: typing.Optional[typing.Union[GoogleStorageTransferJobScheduleStartTimeOfDay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07bc2c2fa39b8d358d108a5bfeb7ae7b779df16b8920c0328f210ddfa16b378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c509258eadd33ead14fc5d7fefa04962753f11c7403a7d880db6331713ccc7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62807e5ece83216e92a848cfec4bc5a3b1c53c40366e55536bef0f2ee75edd03(
    value: typing.Optional[GoogleStorageTransferJobSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01a550ee8e1c80b8ba882079e7d6ac074149ff46981ba6c32e8a210ee3f0b82(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08dea72d4f2339cf682cf6c90f4c848590417c8aa21a84571dba36cb33ffd7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e907225462bfb75752b8b45636c9523fd6f9c08fec4f2d7f2df0a868ceed01e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f721120a65e78c6aecf30b685fc36d887c972d0bf81aeb8efee8310f51f47c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bae4a9ad8413916aaf074e8a1f651a9a772c435246f2ee04604cd4ac3e6ab3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fe2669881a7c9f67912fb85e743db40109c3e29433ff846b7af4126af09ea5(
    value: typing.Optional[GoogleStorageTransferJobScheduleScheduleEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a552b715d0d676bcd53e353c7b7680587c3c58bcb1e3f485f8784db7f8fa703(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d54c05efdbdebac8becb1368a543e4b52990a4355669d37e8ec8fd29de09c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd701485719fca5c5eb3e8a2b917e7f1684cbe0d37ac483393a4234ff2acc051(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9436b63f0113ed2bb767623bec1183103476d8b237d799aace375a906ab1aa23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652e8b6c784545a3135a381919ddddc6c687d7f038351e4a8fbd8dc2e479bf33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47893ac92d3364b3609267d1a6085944527f3a7a7f393215a98ab471b7296dfb(
    value: typing.Optional[GoogleStorageTransferJobScheduleScheduleStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80463f09043d691af86c1773a0e02c1b9b345a3a2a5484463861bfbfe2c2008(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
    nanos: jsii.Number,
    seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217b342b10f0a405a000e2d33dbc7b948f211d7b9929d3172d51b8c48efcd6da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e6129c5918d9df0237ca41c8bc6709ca83c02e3ca3d3350745e27ccb56fe98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548974be57345c56527d47879d22ff6955e7140c3f5b327ce2c44d876364a78a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f88ad526355e879d0f66739b56a0e56d4ff79ba772cac9f2f9c6d52e2c24a02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b234f0d4723a20a97b5e554ecebbb561bfb634fa801fb6fadc093b4bf6ee36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a140dc575737a7b44b96eee92b537340e60f662e4cc8020f98383e4a018eb6c2(
    value: typing.Optional[GoogleStorageTransferJobScheduleStartTimeOfDay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616e0879a2a9378c34a7d8f5ad35ca6a4fb3467b52db8451be19bef266ba2701(
    *,
    aws_s3_data_source: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAwsS3DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_blob_storage_data_source: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_data_sink: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecGcsDataSink, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_data_source: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecGcsDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    http_data_source: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecHttpDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    object_conditions: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecObjectConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    posix_data_sink: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecPosixDataSink, typing.Dict[builtins.str, typing.Any]]] = None,
    posix_data_source: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecPosixDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    sink_agent_pool_name: typing.Optional[builtins.str] = None,
    source_agent_pool_name: typing.Optional[builtins.str] = None,
    transfer_options: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecTransferOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aef2d6377b055ff6790b534ba4568f9597c275b67aed9780e928b17d73a633f(
    *,
    bucket_name: builtins.str,
    aws_access_key: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ccb74f9b8a89b13c42895c2a0556cabe96e5993a842cd280d109f34330449f(
    *,
    access_key_id: builtins.str,
    secret_access_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c6953dfddc4d647904d38b7e127801d0320516bf98b5abf739b64d52907bf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab25f7dd20e2eebb94d1932701fce6a6c9911474f7e21dea831030148ba5b24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ab122bec315bc35d438f8a7bdcd2669dadec8bd567525761d10d732f7ca139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26abbbfe14fa0a8922f4fe0d7b5ba9559d94d7f0175a3c3bcc956e7f80689686(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ad893462683b0eb28ec8eabbf7d1dfe2e2c2334d774b005dfd8169f025ffce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f845352251bd66143645e77d98b50cbbf460e3a7a4ed612f189a645632d27f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8262e32d55402c8096488bdfcaf2cfd4046693ef9daf99e205d3de8ad0ccb724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f82a4e1acb618b5b4098585124147e70305a7cc968a186d4420c0de2eafd80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bd9787ffd218357229debd9a8c51e99999d981ac8238f099febb3b435911a0(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecAwsS3DataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed9b65c8c86aff57d5afbfb84bce37fa1f43b7bf5a2108471460c28399bb2e3(
    *,
    container: builtins.str,
    storage_account: builtins.str,
    azure_credentials: typing.Optional[typing.Union[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    credentials_secret: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c5c3b7cc29e1c081f87271aadb74392784a5124686177d7ec71498734f3cb9(
    *,
    sas_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949e518ef7bae1ff13324fb3cd8f2975300a582bfc8771a1b2ccba565666f403(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebb0eaabf107dd89d2e6e29a55941b428c834915fe8573a8783394202fcde2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb59e2aeca6bf8d57fec91596065e7cd3a736383910346805ba974243190dbe(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a320623d57b734112f626e6dc5272e78792595588d5f37e3572992527f6396(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a861ace8b1ebde3f5ec19e50ad964b12deea0f3701b9f105ee83f842bda89fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dbcd63868946ab7f8b7a7ad6798307d3dd3eb795be51bb9ed6a03d0177e83b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf54e38e934621decd67ea57f1ac3310fb4ed4118a8708e40e3ab1809aefdaf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae352d4029345f0efe7aa3d0f60b15bee48bd093f956f683c5940a5a71324fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f396c6b1ad68a99cfcd831e0394f3858e18d9bc5334e02bd2e23f6cb9e12ae(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecAzureBlobStorageDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b1e4645fd1b23fdcffb06411b264965342108ed8494b697479a863b360019c(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e17c0a0aae97d43fab55bd845b75ee7e88dc41bfc9a772a13b9fbb6af23194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee94ffc058d9fc40225f073bb0d606d65a3e13c39ece357f29c363f12abbfc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec529a4e1bdfc48911764b1a1dc04eaf0169df451157dfb5de8b45a740cf3bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3c0a2bfac6f30f96fe952eddb1dfd532cb22e477ba6f8d48e1a22f9eeb39a3(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e81d9f521306ea6bf326c8210b90856d550d6dd555a4ae4228b8a461095169(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e03fa781f7d856f53d2d63aaf4b1573dadf4a04c9041282092f3aeee40041f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe65f5c105e9b9a06ae8b85f5446b8b64737db1026cb7a97cfa2a3031336f2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd0db4b4fa17bee7deda5bf911e74213ee4aeb4757257e391d4c0a8632160fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb2a6faa4b36cd633c6a3e142c9e1bc805319ac84eaa3e4b702493d3235f1d0(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecGcsDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5a5633ddc033bb451ef0be9ddf4ff149bb98006fcd3493c3727ae06145b822(
    *,
    list_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdce3890b8364e0d9ca488d9c1f91e787a985ff88125ad121f44ef44385b0f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612df7815db80bc1b11137041632f6b4c61f4c2256b0259bd33758f138fb9352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0af0757ec57f612aaccba203193f3d46fdc2c94c82c852cf46a97a258aeecb2(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecHttpDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2575f1467704aec9e2c1173755a35cd61fa0f2af17dc930cc852340e35ff58f8(
    *,
    exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_modified_before: typing.Optional[builtins.str] = None,
    last_modified_since: typing.Optional[builtins.str] = None,
    max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c500f97908b8a5f4ca60e806cc92813fdfa2fe4866544a4a880e46827ef477a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9d5cd2bcad23d15f346aef09f43a40ddb94a2b92adc7572a5f731537913da3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f50dc3a914a5f25ba48c690550f02b637558fcc558878676a6a734079a5e82(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7c1546891334558d52cb849f63896c284d933e7a477df1444726381ab46c70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f84d245bae289dc0d1209968cc68f52bef632b20f3a113b0a86366b1ef8bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4fcd0a9dd9820ff60623d520f7e350ecfb923cf2b27327e20906c96bb93720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604e0ad0f4b8f4a81b2921b49c6f282bb4ae05329cef6a57076847c6990c594b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2e0cff6c9e004028dade56006e76fd73e3203b12237b79c3802a349a4c6b0a(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecObjectConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c69e7ffa7a53bc54f5069ebcb36b13ca25a5ab3f43d57f263bb4c2467ef3fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90e2a90dc28b117a3be92163bb86732a55bf8c7b747ef070a46d8eb4c24b3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa386a2c6177178fad31a304b477f90e3ac3d7d13c0f6e4ea60273aaf4672777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f79dbb0337a0b682e91cdd6b0c2bacf82873de4c2ddcf332f60d6e772d05603(
    value: typing.Optional[GoogleStorageTransferJobTransferSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb3644bf93cead28304317aa48fa27ae7850b55e9e7e211045cd7a9c0c35ba2(
    *,
    root_directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090575c5e2f42b76d69bb33cfd346a6464de75e27ccec8756cc928d3ded63749(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4396dfb5cc392d91c6f941983aa09a8aed73b64f84c0f828d4a2c297e09e41f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a411e5b9d60ada973e545a417a4e646cf2e910b4e6c4b02a765b89abef71c9c(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7996fb301122e1242254057f1544a9f5e1ae540115d72d27ba2ff71b430607(
    *,
    root_directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda91551ccb182ae20413e4f785dac2e950ea5d3be8ff445bf9ca0d31d1f499b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103eacf956ff3034985c179b61b40cc7ee6c6a0f3338eb1dd4f38edef04c2260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48084704fbf2911e9bcf5c5b7710e2652eb3db7302655532276cee6f460ec563(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecPosixDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ff029553bfa7d2e54698fe7a7e3504d37c99244ba2f25d3e85c269deacf187(
    *,
    delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overwrite_when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad360481c71d6c897ef73ab768b4e628498e29be2c4a105b838360848a0a1b29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417baa8561029f0b93035da97899ac224896596ff2924b9d8536fe241d32bc89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009f973070f6bb56c0284396d157f9d661e5f3b8de9c2681698e06e47ebdb096(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a159faebecc0434f9c008238895f55b848144930e5561bd224f8392e4c71e888(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aff5832a5c4c8898235b9bc9bacd54afa036daa48e467ce42a4683106a66b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cab6d612a96a2230201f81e563682cf32ae82773e1206a3b7f06cc03f7c9986(
    value: typing.Optional[GoogleStorageTransferJobTransferSpecTransferOptions],
) -> None:
    """Type checking stubs"""
    pass
