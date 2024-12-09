r'''
# redis-cloud-subscription

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Redis::Cloud::Subscription` v1.0.0.

## Description

CloudFormation template for Pro Subscription.

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Redis::Cloud::Subscription \
  --publisher-id 991a427d4922adc55ddc491f1a3a0421a61120bc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/991a427d4922adc55ddc491f1a3a0421a61120bc/Redis-Cloud-Subscription \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Redis::Cloud::Subscription`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fredis-cloud-subscription+v1.0.0).
* Issues related to `Redis::Cloud::Subscription` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
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


class CfnSubscription(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/redis-cloud-subscription.CfnSubscription",
):
    '''A CloudFormation ``Redis::Cloud::Subscription``.

    :cloudformationResource: Redis::Cloud::Subscription
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_providers: builtins.str,
        base_url: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.str] = None,
        memory_storage: typing.Optional[builtins.str] = None,
        payment_method: typing.Optional[builtins.str] = None,
        payment_method_id: typing.Optional[builtins.str] = None,
        redis_version: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Redis::Cloud::Subscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cloud_providers: [Required as JSON]. Cloud hosting & networking details. Example: [{"regions": [{"region": "us-east-1", "networking": {}}]}]
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param deployment_type: [Optional]. Creates a single region subscription. Example: single-region
        :param dry_run: [Optional]. When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.
        :param memory_storage: [Optional]. Optional. Memory storage preference: either 'ram' or a combination of 'ram-and-flash'. Example: ram. Default: 'ram'
        :param payment_method: [Optional]. Payment method for the requested subscription. If credit card is specified, the payment method Id must be defined. Default: 'credit-card'
        :param payment_method_id: [Optional]. A valid payment method that was pre-defined in the current account. This value is Optional if 'paymentMethod' is 'marketplace', but Required for all other account types.
        :param redis_version: [Optional]. If specified, the redisVersion defines the Redis version of the databases in the subscription. If omitted, the Redis version will be the default (available in 'GET /subscriptions/redis-versions'). Example: 7.2. Default = 'default'
        :param subscription_name: [Optional]. Subscription name. Example: My new subscription
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf60b26e06c31e053411dd8fb1644ba05a7ef702fad73764f523f4710f50f86f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionProps(
            cloud_providers=cloud_providers,
            base_url=base_url,
            deployment_type=deployment_type,
            dry_run=dry_run,
            memory_storage=memory_storage,
            payment_method=payment_method,
            payment_method_id=payment_method_id,
            redis_version=redis_version,
            subscription_name=subscription_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionID")
    def attr_subscription_id(self) -> builtins.str:
        '''Attribute ``Redis::Cloud::Subscription.SubscriptionID``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSubscriptionID"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSubscriptionProps":
        '''Resource props.'''
        return typing.cast("CfnSubscriptionProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/redis-cloud-subscription.CfnSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_providers": "cloudProviders",
        "base_url": "baseUrl",
        "deployment_type": "deploymentType",
        "dry_run": "dryRun",
        "memory_storage": "memoryStorage",
        "payment_method": "paymentMethod",
        "payment_method_id": "paymentMethodId",
        "redis_version": "redisVersion",
        "subscription_name": "subscriptionName",
    },
)
class CfnSubscriptionProps:
    def __init__(
        self,
        *,
        cloud_providers: builtins.str,
        base_url: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.str] = None,
        memory_storage: typing.Optional[builtins.str] = None,
        payment_method: typing.Optional[builtins.str] = None,
        payment_method_id: typing.Optional[builtins.str] = None,
        redis_version: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CloudFormation template for Pro Subscription.

        :param cloud_providers: [Required as JSON]. Cloud hosting & networking details. Example: [{"regions": [{"region": "us-east-1", "networking": {}}]}]
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param deployment_type: [Optional]. Creates a single region subscription. Example: single-region
        :param dry_run: [Optional]. When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.
        :param memory_storage: [Optional]. Optional. Memory storage preference: either 'ram' or a combination of 'ram-and-flash'. Example: ram. Default: 'ram'
        :param payment_method: [Optional]. Payment method for the requested subscription. If credit card is specified, the payment method Id must be defined. Default: 'credit-card'
        :param payment_method_id: [Optional]. A valid payment method that was pre-defined in the current account. This value is Optional if 'paymentMethod' is 'marketplace', but Required for all other account types.
        :param redis_version: [Optional]. If specified, the redisVersion defines the Redis version of the databases in the subscription. If omitted, the Redis version will be the default (available in 'GET /subscriptions/redis-versions'). Example: 7.2. Default = 'default'
        :param subscription_name: [Optional]. Subscription name. Example: My new subscription

        :schema: CfnSubscriptionProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a8c6ece83ab6250e58db236211841e48037008da7ec2bda4c6b56d8f5fa746)
            check_type(argname="argument cloud_providers", value=cloud_providers, expected_type=type_hints["cloud_providers"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument memory_storage", value=memory_storage, expected_type=type_hints["memory_storage"])
            check_type(argname="argument payment_method", value=payment_method, expected_type=type_hints["payment_method"])
            check_type(argname="argument payment_method_id", value=payment_method_id, expected_type=type_hints["payment_method_id"])
            check_type(argname="argument redis_version", value=redis_version, expected_type=type_hints["redis_version"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_providers": cloud_providers,
        }
        if base_url is not None:
            self._values["base_url"] = base_url
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if dry_run is not None:
            self._values["dry_run"] = dry_run
        if memory_storage is not None:
            self._values["memory_storage"] = memory_storage
        if payment_method is not None:
            self._values["payment_method"] = payment_method
        if payment_method_id is not None:
            self._values["payment_method_id"] = payment_method_id
        if redis_version is not None:
            self._values["redis_version"] = redis_version
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name

    @builtins.property
    def cloud_providers(self) -> builtins.str:
        '''[Required as JSON].

        Cloud hosting & networking details. Example: [{"regions": [{"region": "us-east-1", "networking": {}}]}]

        :schema: CfnSubscriptionProps#CloudProviders
        '''
        result = self._values.get("cloud_providers")
        assert result is not None, "Required property 'cloud_providers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''[Required].

        The Base URL where the API calls are sent.

        :schema: CfnSubscriptionProps#BaseUrl
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Creates a single region subscription. Example: single-region

        :schema: CfnSubscriptionProps#DeploymentType
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dry_run(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.

        :schema: CfnSubscriptionProps#DryRun
        '''
        result = self._values.get("dry_run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_storage(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Optional. Memory storage preference: either 'ram' or a combination of 'ram-and-flash'. Example: ram. Default: 'ram'

        :schema: CfnSubscriptionProps#MemoryStorage
        '''
        result = self._values.get("memory_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payment_method(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Payment method for the requested subscription. If credit card is specified, the payment method Id must be defined. Default: 'credit-card'

        :schema: CfnSubscriptionProps#PaymentMethod
        '''
        result = self._values.get("payment_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payment_method_id(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        A valid payment method that was pre-defined in the current account. This value is Optional if 'paymentMethod' is 'marketplace', but Required for all other account types.

        :schema: CfnSubscriptionProps#PaymentMethodId
        '''
        result = self._values.get("payment_method_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_version(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        If specified, the redisVersion defines the Redis version of the databases in the subscription. If omitted, the Redis version will be the default (available in 'GET /subscriptions/redis-versions'). Example: 7.2. Default = 'default'

        :schema: CfnSubscriptionProps#RedisVersion
        '''
        result = self._values.get("redis_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Subscription name. Example: My new subscription

        :schema: CfnSubscriptionProps#SubscriptionName
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSubscription",
    "CfnSubscriptionProps",
]

publication.publish()

def _typecheckingstub__cf60b26e06c31e053411dd8fb1644ba05a7ef702fad73764f523f4710f50f86f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_providers: builtins.str,
    base_url: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.str] = None,
    memory_storage: typing.Optional[builtins.str] = None,
    payment_method: typing.Optional[builtins.str] = None,
    payment_method_id: typing.Optional[builtins.str] = None,
    redis_version: typing.Optional[builtins.str] = None,
    subscription_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a8c6ece83ab6250e58db236211841e48037008da7ec2bda4c6b56d8f5fa746(
    *,
    cloud_providers: builtins.str,
    base_url: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.str] = None,
    memory_storage: typing.Optional[builtins.str] = None,
    payment_method: typing.Optional[builtins.str] = None,
    payment_method_id: typing.Optional[builtins.str] = None,
    redis_version: typing.Optional[builtins.str] = None,
    subscription_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
