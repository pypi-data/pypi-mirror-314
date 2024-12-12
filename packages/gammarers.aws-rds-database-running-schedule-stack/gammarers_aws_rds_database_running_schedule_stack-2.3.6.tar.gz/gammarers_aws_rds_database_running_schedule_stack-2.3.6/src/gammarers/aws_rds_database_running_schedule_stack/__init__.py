r'''
# AWS RDS Database Running Schedule Stack

[![GitHub](https://img.shields.io/github/license/gammarers/aws-rds-database-running-schedule-stack?style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-rds-database-running-schedule-stack?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-rds-database-running-schedule-stack)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-rds-database-running-schedule-stack?style=flat-square)](https://pypi.org/project/gammarers.aws-rds-database-running-schedule-stack/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.RdsDatabaseRunningScheduleStack?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.RdsDatabaseRunningScheduleStack/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-rds-database-running-schedule-stack/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-rds-database-running-schedule-stack?sort=semver&style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-rds-database-running-schedule-stack)](https://constructs.dev/packages/@gammarers/aws-rds-database-running-schedule-stack)

This AWS CDK Construct Stack controls the starting and stopping of RDS DB instances and clusters based on specified tags, ensuring they only run during working hours. It uses EventBridge Scheduler to trigger a StepFunctions State Machine at the start and end of the working hours(default 07:50(UTC) - 21:10(UTC)), which then starts or stops the databases depending on the mode.

> [!WARNING]
> v2.3.0:
> Stack props add option resourceNamingOption
> default ResourceNamingType.DEFAULT is cdk generated name
> f you want to maintain compatibility with versions below `v2.3.0`, please include the following settings (ResourceNamingType.AUTO).
>
> ```python
> new RDSDatabaseRunningScheduleStack(app, 'RDSDatabaseRunningScheduleStack', {
>   targetResource: {
>     tagKey: 'WorkHoursRunning',
>     tagValues: ['YES'],
>   },
>   resourceNamingOption: {
>     type: ResourceNamingType.AUTO, // HERE
>   },
> });
> ```

## Fixed

* RDS Aurora Cluster
* RDS Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler
* StepFunctions StateMahcine (star or stop controle)
* StepFunctions StateMahcine execution role

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-rds-database-running-schedule-stack
```

#### install by yarn

```shell
yarn add @gammarers/aws-rds-database-running-schedule-stack
```

#### install by pnpm

```shell
pnpm add @gammarers/aws-rds-database-running-schedule-stack
```

#### install by bun

```shell
bun add @gammarers/aws-rds-database-running-schedule-stack
```

### Python

```shell
pip install gammarers.aws-rds-database-running-schedule-stack
```

### C# / .NET

```shell
dotnet add package Gammarers.CDK.AWS.RdsDatabaseRunningScheduleStack
```

## Example

```python
import { RdsDatabaseRunningScheduler, DatabaseType } from '@gammarer/aws-rds-database-running-schedule-stack';

new RDSDatabaseRunningScheduleStack(app, 'RDSDatabaseRunningScheduleStack', {
  targetResource: {
    tagKey: 'WorkHoursRunning', // already tagging to rds instance or cluster
    tagValues: ['YES'], // already tagging to rds instance or cluster
  },
  enableScheduling: true,
  startSchedule: {
    timezone: 'Asia/Tokyo',
    minute: '55',
    hour: '8',
    week: 'MON-FRI',
  },
  stopSchedule: {
    timezone: 'Asia/Tokyo',
    minute: '5',
    hour: '19',
    week: 'MON-FRI',
  },
  resourceNamingOption: {
    type: ResourceNamingType.AUTO, // DEFAULT or AUTO or CUSTOM
  },
});
```

## License

This project is licensed under the Apache-2.0 License.
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8
import gammarers.aws_resource_naming as _gammarers_aws_resource_naming_22f917da


@jsii.data_type(
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.CustomNaming",
    jsii_struct_bases=[],
    name_mapping={
        "notification_topic_display_name": "notificationTopicDisplayName",
        "notification_topic_name": "notificationTopicName",
        "scheduler_role_name": "schedulerRoleName",
        "start_schedule_name": "startScheduleName",
        "state_machine_name": "stateMachineName",
        "state_machine_role_name": "stateMachineRoleName",
        "stop_schedule_name": "stopScheduleName",
        "type": "type",
    },
)
class CustomNaming:
    def __init__(
        self,
        *,
        notification_topic_display_name: builtins.str,
        notification_topic_name: builtins.str,
        scheduler_role_name: builtins.str,
        start_schedule_name: builtins.str,
        state_machine_name: builtins.str,
        state_machine_role_name: builtins.str,
        stop_schedule_name: builtins.str,
        type: _gammarers_aws_resource_naming_22f917da.ResourceNamingType,
    ) -> None:
        '''
        :param notification_topic_display_name: 
        :param notification_topic_name: 
        :param scheduler_role_name: 
        :param start_schedule_name: 
        :param state_machine_name: 
        :param state_machine_role_name: 
        :param stop_schedule_name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6db5a15616ecf5d03a994e1e18a8dc960a3e7c1b808221a2f79d29d1f2c27c)
            check_type(argname="argument notification_topic_display_name", value=notification_topic_display_name, expected_type=type_hints["notification_topic_display_name"])
            check_type(argname="argument notification_topic_name", value=notification_topic_name, expected_type=type_hints["notification_topic_name"])
            check_type(argname="argument scheduler_role_name", value=scheduler_role_name, expected_type=type_hints["scheduler_role_name"])
            check_type(argname="argument start_schedule_name", value=start_schedule_name, expected_type=type_hints["start_schedule_name"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument state_machine_role_name", value=state_machine_role_name, expected_type=type_hints["state_machine_role_name"])
            check_type(argname="argument stop_schedule_name", value=stop_schedule_name, expected_type=type_hints["stop_schedule_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_topic_display_name": notification_topic_display_name,
            "notification_topic_name": notification_topic_name,
            "scheduler_role_name": scheduler_role_name,
            "start_schedule_name": start_schedule_name,
            "state_machine_name": state_machine_name,
            "state_machine_role_name": state_machine_role_name,
            "stop_schedule_name": stop_schedule_name,
            "type": type,
        }

    @builtins.property
    def notification_topic_display_name(self) -> builtins.str:
        result = self._values.get("notification_topic_display_name")
        assert result is not None, "Required property 'notification_topic_display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_topic_name(self) -> builtins.str:
        result = self._values.get("notification_topic_name")
        assert result is not None, "Required property 'notification_topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scheduler_role_name(self) -> builtins.str:
        result = self._values.get("scheduler_role_name")
        assert result is not None, "Required property 'scheduler_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_schedule_name(self) -> builtins.str:
        result = self._values.get("start_schedule_name")
        assert result is not None, "Required property 'start_schedule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_role_name(self) -> builtins.str:
        result = self._values.get("state_machine_role_name")
        assert result is not None, "Required property 'state_machine_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stop_schedule_name(self) -> builtins.str:
        result = self._values.get("stop_schedule_name")
        assert result is not None, "Required property 'stop_schedule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> _gammarers_aws_resource_naming_22f917da.ResourceNamingType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(_gammarers_aws_resource_naming_22f917da.ResourceNamingType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomNaming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.NotificationsProperty",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails"},
)
class NotificationsProperty:
    def __init__(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param emails: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251a05c825e7beb6ddfd9ceb6b6c38129822252bd8cdfdc0c3fe1e576d3a4326)
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emails is not None:
            self._values["emails"] = emails

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationsProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RDSDatabaseRunningScheduleStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.RDSDatabaseRunningScheduleStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        target_resource: typing.Union["TargetResourceProperty", typing.Dict[builtins.str, typing.Any]],
        enable_scheduling: typing.Optional[builtins.bool] = None,
        notifications: typing.Optional[typing.Union[NotificationsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_naming_option: typing.Optional[typing.Union[typing.Union[CustomNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceAutoNaming, typing.Dict[builtins.str, typing.Any]]]] = None,
        start_schedule: typing.Optional[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        stop_schedule: typing.Optional[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param target_resource: 
        :param enable_scheduling: 
        :param notifications: 
        :param resource_naming_option: 
        :param start_schedule: 
        :param stop_schedule: 
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1280dc248fa00837f0fd9aade32e57cf0658d41b8f0e88b4b04685819fded2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RDSDatabaseRunningScheduleStackProps(
            target_resource=target_resource,
            enable_scheduling=enable_scheduling,
            notifications=notifications,
            resource_naming_option=resource_naming_option,
            start_schedule=start_schedule,
            stop_schedule=stop_schedule,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            suppress_template_indentation=suppress_template_indentation,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.RDSDatabaseRunningScheduleStackProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "permissions_boundary": "permissionsBoundary",
        "stack_name": "stackName",
        "suppress_template_indentation": "suppressTemplateIndentation",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "target_resource": "targetResource",
        "enable_scheduling": "enableScheduling",
        "notifications": "notifications",
        "resource_naming_option": "resourceNamingOption",
        "start_schedule": "startSchedule",
        "stop_schedule": "stopSchedule",
    },
)
class RDSDatabaseRunningScheduleStackProps(_aws_cdk_ceddda9d.StackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        target_resource: typing.Union["TargetResourceProperty", typing.Dict[builtins.str, typing.Any]],
        enable_scheduling: typing.Optional[builtins.bool] = None,
        notifications: typing.Optional[typing.Union[NotificationsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_naming_option: typing.Optional[typing.Union[typing.Union[CustomNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceAutoNaming, typing.Dict[builtins.str, typing.Any]]]] = None,
        start_schedule: typing.Optional[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        stop_schedule: typing.Optional[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param target_resource: 
        :param enable_scheduling: 
        :param notifications: 
        :param resource_naming_option: 
        :param start_schedule: 
        :param stop_schedule: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if isinstance(target_resource, dict):
            target_resource = TargetResourceProperty(**target_resource)
        if isinstance(notifications, dict):
            notifications = NotificationsProperty(**notifications)
        if isinstance(start_schedule, dict):
            start_schedule = ScheduleProperty(**start_schedule)
        if isinstance(stop_schedule, dict):
            stop_schedule = ScheduleProperty(**stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a02c77b05b4403ac204e4b21fbecf9f310b2adf40ef9f6754f8cde04bbb117)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument suppress_template_indentation", value=suppress_template_indentation, expected_type=type_hints["suppress_template_indentation"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument target_resource", value=target_resource, expected_type=type_hints["target_resource"])
            check_type(argname="argument enable_scheduling", value=enable_scheduling, expected_type=type_hints["enable_scheduling"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument resource_naming_option", value=resource_naming_option, expected_type=type_hints["resource_naming_option"])
            check_type(argname="argument start_schedule", value=start_schedule, expected_type=type_hints["start_schedule"])
            check_type(argname="argument stop_schedule", value=stop_schedule, expected_type=type_hints["stop_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_resource": target_resource,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if suppress_template_indentation is not None:
            self._values["suppress_template_indentation"] = suppress_template_indentation
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if enable_scheduling is not None:
            self._values["enable_scheduling"] = enable_scheduling
        if notifications is not None:
            self._values["notifications"] = notifications
        if resource_naming_option is not None:
            self._values["resource_naming_option"] = resource_naming_option
        if start_schedule is not None:
            self._values["start_schedule"] = start_schedule
        if stop_schedule is not None:
            self._values["stop_schedule"] = stop_schedule

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress_template_indentation(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to suppress indentation in generated CloudFormation templates.

        If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation``
        context key will be used. If that is not specified, then the
        default value ``false`` will be used.

        :default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        '''
        result = self._values.get("suppress_template_indentation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        The Stack Synthesizer controls aspects of synthesis and deployment,
        like how assets are referenced and what IAM roles to use. For more
        information, see the README of the main CDK package.

        If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used.
        If that is not specified, ``DefaultStackSynthesizer`` is used if
        ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major
        version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no
        other synthesizer is specified.

        :default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target_resource(self) -> "TargetResourceProperty":
        result = self._values.get("target_resource")
        assert result is not None, "Required property 'target_resource' is missing"
        return typing.cast("TargetResourceProperty", result)

    @builtins.property
    def enable_scheduling(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_scheduling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notifications(self) -> typing.Optional[NotificationsProperty]:
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[NotificationsProperty], result)

    @builtins.property
    def resource_naming_option(
        self,
    ) -> typing.Optional[typing.Union[CustomNaming, _gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, _gammarers_aws_resource_naming_22f917da.ResourceAutoNaming]]:
        result = self._values.get("resource_naming_option")
        return typing.cast(typing.Optional[typing.Union[CustomNaming, _gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, _gammarers_aws_resource_naming_22f917da.ResourceAutoNaming]], result)

    @builtins.property
    def start_schedule(self) -> typing.Optional["ScheduleProperty"]:
        result = self._values.get("start_schedule")
        return typing.cast(typing.Optional["ScheduleProperty"], result)

    @builtins.property
    def stop_schedule(self) -> typing.Optional["ScheduleProperty"]:
        result = self._values.get("stop_schedule")
        return typing.cast(typing.Optional["ScheduleProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RDSDatabaseRunningScheduleStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.ScheduleProperty",
    jsii_struct_bases=[],
    name_mapping={
        "timezone": "timezone",
        "hour": "hour",
        "minute": "minute",
        "week": "week",
    },
)
class ScheduleProperty:
    def __init__(
        self,
        *,
        timezone: builtins.str,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        week: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param timezone: 
        :param hour: 
        :param minute: 
        :param week: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698ada8cebb0f29cf7aa1b64e0b10a701ff87508b556665b4c2bae69b2799be8)
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument week", value=week, expected_type=type_hints["week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "timezone": timezone,
        }
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if week is not None:
            self._values["week"] = week

    @builtins.property
    def timezone(self) -> builtins.str:
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week(self) -> typing.Optional[builtins.str]:
        result = self._values.get("week")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarers/aws-rds-database-running-schedule-stack.TargetResourceProperty",
    jsii_struct_bases=[],
    name_mapping={"tag_key": "tagKey", "tag_values": "tagValues"},
)
class TargetResourceProperty:
    def __init__(
        self,
        *,
        tag_key: builtins.str,
        tag_values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param tag_key: 
        :param tag_values: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8591c95e42de5a4e537e0f91a2110f72b09d18b72008139e5e23a0d230607030)
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_key": tag_key,
            "tag_values": tag_values,
        }

    @builtins.property
    def tag_key(self) -> builtins.str:
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_values(self) -> typing.List[builtins.str]:
        result = self._values.get("tag_values")
        assert result is not None, "Required property 'tag_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetResourceProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CustomNaming",
    "NotificationsProperty",
    "RDSDatabaseRunningScheduleStack",
    "RDSDatabaseRunningScheduleStackProps",
    "ScheduleProperty",
    "TargetResourceProperty",
]

publication.publish()

def _typecheckingstub__bc6db5a15616ecf5d03a994e1e18a8dc960a3e7c1b808221a2f79d29d1f2c27c(
    *,
    notification_topic_display_name: builtins.str,
    notification_topic_name: builtins.str,
    scheduler_role_name: builtins.str,
    start_schedule_name: builtins.str,
    state_machine_name: builtins.str,
    state_machine_role_name: builtins.str,
    stop_schedule_name: builtins.str,
    type: _gammarers_aws_resource_naming_22f917da.ResourceNamingType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251a05c825e7beb6ddfd9ceb6b6c38129822252bd8cdfdc0c3fe1e576d3a4326(
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1280dc248fa00837f0fd9aade32e57cf0658d41b8f0e88b4b04685819fded2e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    target_resource: typing.Union[TargetResourceProperty, typing.Dict[builtins.str, typing.Any]],
    enable_scheduling: typing.Optional[builtins.bool] = None,
    notifications: typing.Optional[typing.Union[NotificationsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_naming_option: typing.Optional[typing.Union[typing.Union[CustomNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceAutoNaming, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_schedule: typing.Optional[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    stop_schedule: typing.Optional[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a02c77b05b4403ac204e4b21fbecf9f310b2adf40ef9f6754f8cde04bbb117(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    target_resource: typing.Union[TargetResourceProperty, typing.Dict[builtins.str, typing.Any]],
    enable_scheduling: typing.Optional[builtins.bool] = None,
    notifications: typing.Optional[typing.Union[NotificationsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_naming_option: typing.Optional[typing.Union[typing.Union[CustomNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceDefaultNaming, typing.Dict[builtins.str, typing.Any]], typing.Union[_gammarers_aws_resource_naming_22f917da.ResourceAutoNaming, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_schedule: typing.Optional[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    stop_schedule: typing.Optional[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698ada8cebb0f29cf7aa1b64e0b10a701ff87508b556665b4c2bae69b2799be8(
    *,
    timezone: builtins.str,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    week: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8591c95e42de5a4e537e0f91a2110f72b09d18b72008139e5e23a0d230607030(
    *,
    tag_key: builtins.str,
    tag_values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
