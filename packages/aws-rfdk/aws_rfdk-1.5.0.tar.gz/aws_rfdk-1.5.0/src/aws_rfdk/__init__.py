r'''
# Render Farm Deployment Kit on AWS

The Render Farm Deployment Kit on AWS (RFDK) is an open-source software development kit (SDK) that can be used to deploy, configure, and manage your render farm
infrastructure in the cloud. The RFDK is built to operate with the AWS Cloud Development Kit (CDK) and provides a library of classes, called constructs, that each
deploy and configure a component of your cloud-based render farm. The current version of the RFDK supports render farms built using AWS Thinkbox Deadline
render management software, and provides the ability for you to easily go from nothing to a production-ready render farm in the cloud.

You can model, deploy, configure, and update your AWS render farm infrastructure by writing an application, in Python or Node.js, for the CDK toolkit using the
libraries provided by the CDK and RFDK together and with other CDK-compatible libraries. Your application is written in an object-oriented style where creation of
an object from the CDK and RFDK libraries represents the creation of a resource, or collection of resources, in your AWS account when the application is deployed
via AWS CloudFormation by the CDK toolkit. The parameters of an object’s creation control the configuration of the resource.

Please see the following sources for additional information:

* The [RFDK Developer Guide](https://docs.aws.amazon.com/rfdk/latest/guide/what-is-rfdk.html)
* The [RFDK API Documentation](https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk-construct-library.html)
* The [README for the main module](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/lib/core/README.md)
* The [README for the Deadline module](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/lib/deadline/README.md)
* The [RFDK Upgrade Documentation](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/docs/upgrade/index.md)
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
import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_fsx as _aws_cdk_aws_fsx_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="aws-rfdk.ApplicationEndpointProps",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "port": "port", "protocol": "protocol"},
)
class ApplicationEndpointProps:
    def __init__(
        self,
        *,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    ) -> None:
        '''Properties for constructing an {@link ApplicationEndpoint}.

        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The application layer protocol of the endpoint. Default: HTTPS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7aae1e1e7606385280722c44443deaef00f8901625489cdbd6fd96ccd1bdfd8)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "port": port,
        }
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def address(self) -> builtins.str:
        '''The address (either an IP or hostname) of the endpoint.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number of the endpoint.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''The application layer protocol of the endpoint.

        :default: HTTPS
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.BlockVolumeFormat")
class BlockVolumeFormat(enum.Enum):
    '''Block format options for formatting a blank/new BlockVolume.'''

    EXT3 = "EXT3"
    '''See: https://en.wikipedia.org/wiki/Ext3.'''
    EXT4 = "EXT4"
    '''See: https://en.wikipedia.org/wiki/Ext4.'''
    XFS = "XFS"
    '''See: https://en.wikipedia.org/wiki/XFS.'''


class CloudWatchAgent(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.CloudWatchAgent",
):
    '''This construct is a thin wrapper that provides the ability to install and configure the CloudWatchAgent ( https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html ) on one or more EC2 instances during instance startup.

    It accomplishes this by downloading and executing the configuration script on the instance.
    The script will download the CloudWatch Agent installer,
    optionally verify the installer, and finally install the CloudWatch Agent.
    The installer is downloaded via the Amazon S3 API, thus, this construct can be used
    on instances that have no access to the internet as long as the VPC contains
    an VPC Gateway Endpoint for S3 ( https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints-s3.html ).

    {@link CloudWatchAgent.SKIP_CWAGENT_VALIDATION_CTX_VAR} - Context variable to skip validation
    of the downloaded CloudWatch Agent installer if set to 'TRUE'.
    WARNING: Only use this if your deployments are failing due to a validation failure,
    but you have verified that the failure is benign.


    Resources Deployed

    - String SSM Parameter in Systems Manager Parameter Store to store the cloudwatch agent configuration;
    - A script Asset which is uploaded to S3 bucket.



    Security Considerations

    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_watch_config: builtins.str,
        host: "IScriptHost",
        should_install_agent: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_watch_config: CloudWatch agent configuration string in json format.
        :param host: The host instance/ASG/fleet with a CloudWatch Agent to be configured.
        :param should_install_agent: Whether or not we should attempt to install the CloudWatch agent. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d1b9b863bc88f01c9cc4c26b0cc9bf80f0349ec736b442e56075dca4cff48c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudWatchAgentProps(
            cloud_watch_config=cloud_watch_config,
            host=host,
            should_install_agent=should_install_agent,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SKIP_CWAGENT_VALIDATION_CTX_VAR")
    def SKIP_CWAGENT_VALIDATION_CTX_VAR(cls) -> builtins.str:
        '''The context variable to indicate that CloudWatch agent installer validation should be skipped.'''
        return typing.cast(builtins.str, jsii.sget(cls, "SKIP_CWAGENT_VALIDATION_CTX_VAR"))


@jsii.data_type(
    jsii_type="aws-rfdk.CloudWatchAgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_config": "cloudWatchConfig",
        "host": "host",
        "should_install_agent": "shouldInstallAgent",
    },
)
class CloudWatchAgentProps:
    def __init__(
        self,
        *,
        cloud_watch_config: builtins.str,
        host: "IScriptHost",
        should_install_agent: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties for creating the resources needed for CloudWatch Agent configuration.

        :param cloud_watch_config: CloudWatch agent configuration string in json format.
        :param host: The host instance/ASG/fleet with a CloudWatch Agent to be configured.
        :param should_install_agent: Whether or not we should attempt to install the CloudWatch agent. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8221e47302da6430194635a16a777c3e4077948c6773bb08e14eb422cb26c00)
            check_type(argname="argument cloud_watch_config", value=cloud_watch_config, expected_type=type_hints["cloud_watch_config"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument should_install_agent", value=should_install_agent, expected_type=type_hints["should_install_agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_watch_config": cloud_watch_config,
            "host": host,
        }
        if should_install_agent is not None:
            self._values["should_install_agent"] = should_install_agent

    @builtins.property
    def cloud_watch_config(self) -> builtins.str:
        '''CloudWatch agent configuration string in json format.

        :see: - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html
        '''
        result = self._values.get("cloud_watch_config")
        assert result is not None, "Required property 'cloud_watch_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> "IScriptHost":
        '''The host instance/ASG/fleet with a CloudWatch Agent to be configured.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast("IScriptHost", result)

    @builtins.property
    def should_install_agent(self) -> typing.Optional[builtins.bool]:
        '''Whether or not we should attempt to install the CloudWatch agent.

        :default: true
        '''
        result = self._values.get("should_install_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchAgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWatchConfigBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.CloudWatchConfigBuilder",
):
    '''Class that can build a CloudWatch Agent configuration.'''

    def __init__(
        self,
        log_flush_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Constructs.

        :param log_flush_interval: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee3213416bf136598eadb8bb9bc028e1c4431ede6fb1dabd402caf60592534d)
            check_type(argname="argument log_flush_interval", value=log_flush_interval, expected_type=type_hints["log_flush_interval"])
        jsii.create(self.__class__, self, [log_flush_interval])

    @jsii.member(jsii_name="addLogsCollectList")
    def add_logs_collect_list(
        self,
        log_group_name: builtins.str,
        log_stream_prefix: builtins.str,
        log_file_path: builtins.str,
        time_zone: typing.Optional["TimeZone"] = None,
    ) -> None:
        '''This method adds the log file path and its associated log group and log stream properties to the list of files which needs to be streamed to cloud watch logs.

        :param log_group_name: - string for the log group name.
        :param log_stream_prefix: - string for the log stream prefix. The actual stream name will be appended by instance id
        :param log_file_path: - local file path which needs to be streamed.
        :param time_zone: - the time zone to use when putting timestamps on log events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181f242f6e8e76570db13dc1d7338ca24da148900dfeb1d1989a5405957f0b89)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_prefix", value=log_stream_prefix, expected_type=type_hints["log_stream_prefix"])
            check_type(argname="argument log_file_path", value=log_file_path, expected_type=type_hints["log_file_path"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        return typing.cast(None, jsii.invoke(self, "addLogsCollectList", [log_group_name, log_stream_prefix, log_file_path, time_zone]))

    @jsii.member(jsii_name="generateCloudWatchConfiguration")
    def generate_cloud_watch_configuration(self) -> builtins.str:
        '''The method generates the configuration for log file streaming to be added to CloudWatch Agent Configuration File.'''
        return typing.cast(builtins.str, jsii.invoke(self, "generateCloudWatchConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="logFlushInterval")
    def log_flush_interval(self) -> _aws_cdk_ceddda9d.Duration:
        '''Flush interval of the Cloud Watch Agent (in Seconds).'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "logFlushInterval"))


@jsii.data_type(
    jsii_type="aws-rfdk.ConnectableApplicationEndpointProps",
    jsii_struct_bases=[ApplicationEndpointProps],
    name_mapping={
        "address": "address",
        "port": "port",
        "protocol": "protocol",
        "connections": "connections",
    },
)
class ConnectableApplicationEndpointProps(ApplicationEndpointProps):
    def __init__(
        self,
        *,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
        connections: _aws_cdk_aws_ec2_ceddda9d.Connections,
    ) -> None:
        '''Properties for constructing an {@link ConnectableApplicationEndpoint}.

        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The application layer protocol of the endpoint. Default: HTTPS
        :param connections: The connection object of the application this endpoint is for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f25d9774cf848cafb8bf57d6cab9a23f78b963586ea9c5f3c15b333fbf34b8b)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "port": port,
            "connections": connections,
        }
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def address(self) -> builtins.str:
        '''The address (either an IP or hostname) of the endpoint.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number of the endpoint.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''The application layer protocol of the endpoint.

        :default: HTTPS
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    @builtins.property
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The connection object of the application this endpoint is for.'''
        result = self._values.get("connections")
        assert result is not None, "Required property 'connections' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectableApplicationEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.ConventionalScriptPathParams",
    jsii_struct_bases=[],
    name_mapping={"base_name": "baseName", "os_type": "osType", "root_dir": "rootDir"},
)
class ConventionalScriptPathParams:
    def __init__(
        self,
        *,
        base_name: builtins.str,
        os_type: _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType,
        root_dir: builtins.str,
    ) -> None:
        '''Specification of a script within the RFDK repo based on the script directory structure convention.

        :param base_name: The basename of the script without the file's extension.
        :param os_type: The operating system that the script is intended for.
        :param root_dir: The root directory that contains the script.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b0b193e60f50e17f048423e8cf05bb26dae07981f21aa1bcad9942e8605967)
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument root_dir", value=root_dir, expected_type=type_hints["root_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_name": base_name,
            "os_type": os_type,
            "root_dir": root_dir,
        }

    @builtins.property
    def base_name(self) -> builtins.str:
        '''The basename of the script without the file's extension.'''
        result = self._values.get("base_name")
        assert result is not None, "Required property 'base_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_type(self) -> _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType:
        '''The operating system that the script is intended for.'''
        result = self._values.get("os_type")
        assert result is not None, "Required property 'os_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.OperatingSystemType, result)

    @builtins.property
    def root_dir(self) -> builtins.str:
        '''The root directory that contains the script.'''
        result = self._values.get("root_dir")
        assert result is not None, "Required property 'root_dir' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConventionalScriptPathParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.DistinguishedName",
    jsii_struct_bases=[],
    name_mapping={"cn": "cn", "o": "o", "ou": "ou"},
)
class DistinguishedName:
    def __init__(
        self,
        *,
        cn: builtins.str,
        o: typing.Optional[builtins.str] = None,
        ou: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The identification for a self-signed CA or Certificate.

        These fields are industry standard, and can be found in rfc1779 (see: https://tools.ietf.org/html/rfc1779)
        or the X.520 specification (see: ITU-T Rec.X.520)

        :param cn: Common Name for the identity. a) For servers -- The fully qualified domain name (aka: fqdn) of the server. b) For clients, or as a self-signed CA -- Any name you would like to identify the certificate.
        :param o: Organization that is creating the identity. For example, your company name. Default: : AWS
        :param ou: Organization Unit that is creating the identity. For example, the name of your group/unit. Default: : Thinkbox
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddee105e5ab12508ec4acbfbaca4a1fb33ae318c62f07672117d3cd87b26ecc3)
            check_type(argname="argument cn", value=cn, expected_type=type_hints["cn"])
            check_type(argname="argument o", value=o, expected_type=type_hints["o"])
            check_type(argname="argument ou", value=ou, expected_type=type_hints["ou"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cn": cn,
        }
        if o is not None:
            self._values["o"] = o
        if ou is not None:
            self._values["ou"] = ou

    @builtins.property
    def cn(self) -> builtins.str:
        '''Common Name for the identity.

        a) For servers -- The fully qualified domain name (aka: fqdn) of the server.
        b) For clients, or as a self-signed CA -- Any name you would like to identify the certificate.
        '''
        result = self._values.get("cn")
        assert result is not None, "Required property 'cn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def o(self) -> typing.Optional[builtins.str]:
        '''Organization that is creating the identity.

        For example, your company name.

        :default: : AWS
        '''
        result = self._values.get("o")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou(self) -> typing.Optional[builtins.str]:
        '''Organization Unit that is creating the identity.

        For example, the name of your group/unit.

        :default: : Thinkbox
        '''
        result = self._values.get("ou")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistinguishedName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.Endpoint"):
    '''Connection endpoint.

    Consists of a combination of hostname, port, and transport protocol.
    '''

    def __init__(
        self,
        *,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Protocol] = None,
    ) -> None:
        '''Constructs an Endpoint instance.

        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The transport protocol of the endpoint. Default: TCP
        '''
        props = EndpointProps(address=address, port=port, protocol=protocol)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="portAsString")
    def port_as_string(self) -> builtins.str:
        '''Returns the port number as a string representation that can be used for embedding within other strings.

        This is intended to deal with CDK's token system. Numeric CDK tokens are not expanded when their string
        representation is embedded in a string. This function returns the port either as an unresolved string token or
        as a resolved string representation of the port value.

        :return: An (un)resolved string representation of the endpoint's port number
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "portAsString", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        '''The hostname of the endpoint.'''
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> _aws_cdk_aws_ec2_ceddda9d.Port:
        '''The port of the endpoint.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Port, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="portNumber")
    def port_number(self) -> jsii.Number:
        '''The port number of the endpoint.

        This can potentially be a CDK token. If you need to embed the port in a string (e.g. instance user data script),
        use {@link Endpoint.portAsString}.
        '''
        return typing.cast(jsii.Number, jsii.get(self, "portNumber"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> _aws_cdk_aws_ec2_ceddda9d.Protocol:
        '''The protocol of the endpoint.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Protocol, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> builtins.str:
        '''The combination of "HOSTNAME:PORT" for this endpoint.'''
        return typing.cast(builtins.str, jsii.get(self, "socketAddress"))


@jsii.data_type(
    jsii_type="aws-rfdk.EndpointProps",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "port": "port", "protocol": "protocol"},
)
class EndpointProps:
    def __init__(
        self,
        *,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Protocol] = None,
    ) -> None:
        '''Properties for constructing an {@link Endpoint}.

        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The transport protocol of the endpoint. Default: TCP
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d95bd543b1133caf30aabb41c49805136a34e32ad0f00d07379d58f49b5f73f)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "port": port,
        }
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def address(self) -> builtins.str:
        '''The address (either an IP or hostname) of the endpoint.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number of the endpoint.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Protocol]:
        '''The transport protocol of the endpoint.

        :default: TCP
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Protocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.ExecuteScriptProps",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "args": "args"},
)
class ExecuteScriptProps:
    def __init__(
        self,
        *,
        host: "IScriptHost",
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Interface of properties for adding UserData commands to download and executing a {@link ScriptAsset} on a host machine.

        :param host: The host to run the script against. For example, instances of: - {@link @aws-cdk/aws-ec2#Instance} - {@link @aws-cdk/aws-autoscaling#AutoScalingGroup} can be used.
        :param args: Command-line arguments to invoke the script with. If supplied, these arguments are simply concatenated with a space character between. No shell escaping is done. Default: No command-line arguments
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e700f29d38abec3def891c9fe8d7c313850c2d78eea8d8a7d2b845e2fd7fb3b)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
        }
        if args is not None:
            self._values["args"] = args

    @builtins.property
    def host(self) -> "IScriptHost":
        '''The host to run the script against.

        For example, instances of:

        - {@link @aws-cdk/aws-ec2#Instance}
        - {@link @aws-cdk/aws-autoscaling#AutoScalingGroup}

        can be used.
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast("IScriptHost", result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Command-line arguments to invoke the script with.

        If supplied, these arguments are simply concatenated with a space character between. No shell escaping is done.

        :default: No command-line arguments
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecuteScriptProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExportingLogGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.ExportingLogGroup",
):
    '''This construct takes the name of a CloudWatch LogGroup and will either create it if it doesn't already exist, or reuse the existing one.

    It also creates a regularly scheduled lambda that will export LogEvents to S3
    before they expire in CloudWatch.

    It's used for cost-reduction, as it is more economical to archive logs in S3 than CloudWatch when
    retaining them for more than a week.
    Note, that it isn't economical to export logs to S3 if you plan on storing them for less than
    7 days total (CloudWatch and S3 combined).


    Resources Deployed

    - The Lambda SingletonFunction that checks for the existence of the LogGroup.
    - The CloudWatch LogGroup (if it didn't exist already).
    - The CloudWatch Alarm watching log exportation failures.
    - The CloudWatch Event Rule to schedule log exportation.
    - The Lambda SingletonFunction, with role, to export log groups to S3 by schedule.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        log_group_name: builtins.str,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: The S3 bucket's name to export the logs to. Bucket must already exist and have read/write privilidges enabled for logs.amazonaws.com.
        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the hour before they expire in CloudWatch. Retention in S3 must be configured on the S3 Bucket provided. Default: - 3 days
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd293e1060041be76c1a0e849ba287648dd0ac8dd43fcf08c78cc91610ec0c84)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ExportingLogGroupProps(
            bucket_name=bucket_name, log_group_name=log_group_name, retention=retention
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="exportErrorAlarm")
    def export_error_alarm(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Alarm:
        '''CloudWatch alarm on the error metric of the export LogGroup task Lambda.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Alarm, jsii.get(self, "exportErrorAlarm"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The LogGroup created or fetched for the given name.'''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.get(self, "logGroup"))


@jsii.data_type(
    jsii_type="aws-rfdk.ExportingLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "log_group_name": "logGroupName",
        "retention": "retention",
    },
)
class ExportingLogGroupProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        log_group_name: builtins.str,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''Properties for setting up an {@link ExportingLogGroup}.

        :param bucket_name: The S3 bucket's name to export the logs to. Bucket must already exist and have read/write privilidges enabled for logs.amazonaws.com.
        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the hour before they expire in CloudWatch. Retention in S3 must be configured on the S3 Bucket provided. Default: - 3 days
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc01869453fa82c8a3906575f23b32a1f7a5c67a24b7ff0b2633513e65328d8)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "log_group_name": log_group_name,
        }
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The S3 bucket's name to export the logs to.

        Bucket must already exist and have read/write privilidges enabled for
        logs.amazonaws.com.
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The log group name.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        Exportation to S3 will happen the hour before
        they expire in CloudWatch. Retention in S3 must be configured on the S3 Bucket provided.

        :default: - 3 days
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExportingLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.HealthCheckConfig",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_fleet_threshold_percent": "healthyFleetThresholdPercent",
        "instance_healthy_threshold_count": "instanceHealthyThresholdCount",
        "instance_unhealthy_threshold_count": "instanceUnhealthyThresholdCount",
        "interval": "interval",
        "port": "port",
    },
)
class HealthCheckConfig:
    def __init__(
        self,
        *,
        healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
        instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
        instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for configuring a health check.

        :param healthy_fleet_threshold_percent: The percent of healthy hosts to consider fleet healthy and functioning. Default: 65%
        :param instance_healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. Default: 2
        :param instance_unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. Default: 3
        :param interval: The approximate time between health checks for an individual target. Default: Duration.minutes(5)
        :param port: The port that the health monitor uses when performing health checks on the targets. Default: 8081
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea42155f729a06271fd2940ff6cd6cc955170cf28d6854cc516f12a28c2a08f)
            check_type(argname="argument healthy_fleet_threshold_percent", value=healthy_fleet_threshold_percent, expected_type=type_hints["healthy_fleet_threshold_percent"])
            check_type(argname="argument instance_healthy_threshold_count", value=instance_healthy_threshold_count, expected_type=type_hints["instance_healthy_threshold_count"])
            check_type(argname="argument instance_unhealthy_threshold_count", value=instance_unhealthy_threshold_count, expected_type=type_hints["instance_unhealthy_threshold_count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy_fleet_threshold_percent is not None:
            self._values["healthy_fleet_threshold_percent"] = healthy_fleet_threshold_percent
        if instance_healthy_threshold_count is not None:
            self._values["instance_healthy_threshold_count"] = instance_healthy_threshold_count
        if instance_unhealthy_threshold_count is not None:
            self._values["instance_unhealthy_threshold_count"] = instance_unhealthy_threshold_count
        if interval is not None:
            self._values["interval"] = interval
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def healthy_fleet_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''The percent of healthy hosts to consider fleet healthy and functioning.

        :default: 65%
        '''
        result = self._values.get("healthy_fleet_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks successes required before considering an unhealthy target healthy.

        :default: 2
        '''
        result = self._values.get("instance_healthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health check failures required before considering a target unhealthy.

        :default: 3
        '''
        result = self._values.get("instance_unhealthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The approximate time between health checks for an individual target.

        :default: Duration.minutes(5)
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port that the health monitor uses when performing health checks on the targets.

        :default: 8081
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.HealthMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "elb_account_limits": "elbAccountLimits",
        "encryption_key": "encryptionKey",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class HealthMonitorProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        elb_account_limits: typing.Optional[typing.Sequence[typing.Union["Limit", typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the Health Monitor.

        :param vpc: VPC to launch the Health Monitor in.
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param elb_account_limits: Describes the current Elastic Load Balancing resource limits for your AWS account. This object should be the output of 'describeAccountLimits' API. Default: default account limits for ALB is used
        :param encryption_key: A KMS Key, either managed by this CDK app, or imported. Default: A new Key will be created and used.
        :param security_group: Security group for the health monitor. This is security group is associated with the health monitor's load balancer. Default: : A security group is created
        :param vpc_subnets: Any load balancers that get created by calls to registerFleet() will be created in these subnets. Default: : The VPC default strategy
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfad80c3105e3245dca4fa4386a074b4c5f03dd705aac66898cc20c2e0c3b43)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument elb_account_limits", value=elb_account_limits, expected_type=type_hints["elb_account_limits"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if elb_account_limits is not None:
            self._values["elb_account_limits"] = elb_account_limits
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the Health Monitor in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether deletion protection is enabled for the LoadBalancer.

        :default:

        true

        Note: This value is true by default which means that the deletion protection is enabled for the
        load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#deletion-protection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def elb_account_limits(self) -> typing.Optional[typing.List["Limit"]]:
        '''Describes the current Elastic Load Balancing resource limits for your AWS account.

        This object should be the output of 'describeAccountLimits' API.

        :default: default account limits for ALB is used

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/ELBv2.html#describeAccountLimits-property
        '''
        result = self._values.get("elb_account_limits")
        return typing.cast(typing.Optional[typing.List["Limit"]], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''A KMS Key, either managed by this CDK app, or imported.

        :default: A new Key will be created and used.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security group for the health monitor.

        This is security group is associated with the health monitor's load balancer.

        :default: : A security group is created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Any load balancers that get created by calls to registerFleet() will be created in these subnets.

        :default: : The VPC default strategy
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-rfdk.IHealthMonitor")
class IHealthMonitor(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Interface for the Health Monitor.'''

    @jsii.member(jsii_name="registerFleet")
    def register_fleet(
        self,
        monitorable_fleet: "IMonitorableFleet",
        *,
        healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
        instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
        instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Attaches the load-balancing target to the ELB for instance-level monitoring.

        :param monitorable_fleet: -
        :param healthy_fleet_threshold_percent: The percent of healthy hosts to consider fleet healthy and functioning. Default: 65%
        :param instance_healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. Default: 2
        :param instance_unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. Default: 3
        :param interval: The approximate time between health checks for an individual target. Default: Duration.minutes(5)
        :param port: The port that the health monitor uses when performing health checks on the targets. Default: 8081
        '''
        ...


class _IHealthMonitorProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Interface for the Health Monitor.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IHealthMonitor"

    @jsii.member(jsii_name="registerFleet")
    def register_fleet(
        self,
        monitorable_fleet: "IMonitorableFleet",
        *,
        healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
        instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
        instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Attaches the load-balancing target to the ELB for instance-level monitoring.

        :param monitorable_fleet: -
        :param healthy_fleet_threshold_percent: The percent of healthy hosts to consider fleet healthy and functioning. Default: 65%
        :param instance_healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. Default: 2
        :param instance_unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. Default: 3
        :param interval: The approximate time between health checks for an individual target. Default: Duration.minutes(5)
        :param port: The port that the health monitor uses when performing health checks on the targets. Default: 8081
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7ee0821865234eed27a6cc965fd6816e0e85d92d76d870878c149c5739deda)
            check_type(argname="argument monitorable_fleet", value=monitorable_fleet, expected_type=type_hints["monitorable_fleet"])
        health_check_config = HealthCheckConfig(
            healthy_fleet_threshold_percent=healthy_fleet_threshold_percent,
            instance_healthy_threshold_count=instance_healthy_threshold_count,
            instance_unhealthy_threshold_count=instance_unhealthy_threshold_count,
            interval=interval,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "registerFleet", [monitorable_fleet, health_check_config]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHealthMonitor).__jsii_proxy_class__ = lambda : _IHealthMonitorProxy


@jsii.interface(jsii_type="aws-rfdk.IMongoDb")
class IMongoDb(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''Essential properties of a MongoDB database.'''

    @builtins.property
    @jsii.member(jsii_name="adminUser")
    def admin_user(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''Credentials for the admin user of the database.

        This user has database role:
        [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ]
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The certificate chain of trust for the MongoDB application's server certificate.

        The contents of this secret is a single string containing the trust chain in PEM format, and
        can be saved to a file that is then passed as the --sslCAFile option when connecting to MongoDB
        using the mongo shell.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fullHostname")
    def full_hostname(self) -> builtins.str:
        '''The full host name that can be used to connect to the MongoDB application running on this instance.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''The port to connect to for MongoDB.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "MongoDbVersion":
        '''The version of MongoDB that is running on this instance.'''
        ...

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds security groups to the database.

        :param security_groups: The security groups to add.
        '''
        ...


class _IMongoDbProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Essential properties of a MongoDB database.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IMongoDb"

    @builtins.property
    @jsii.member(jsii_name="adminUser")
    def admin_user(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''Credentials for the admin user of the database.

        This user has database role:
        [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ]
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "adminUser"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The certificate chain of trust for the MongoDB application's server certificate.

        The contents of this secret is a single string containing the trust chain in PEM format, and
        can be saved to a file that is then passed as the --sslCAFile option when connecting to MongoDB
        using the mongo shell.
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "certificateChain"))

    @builtins.property
    @jsii.member(jsii_name="fullHostname")
    def full_hostname(self) -> builtins.str:
        '''The full host name that can be used to connect to the MongoDB application running on this instance.'''
        return typing.cast(builtins.str, jsii.get(self, "fullHostname"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''The port to connect to for MongoDB.'''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "MongoDbVersion":
        '''The version of MongoDB that is running on this instance.'''
        return typing.cast("MongoDbVersion", jsii.get(self, "version"))

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds security groups to the database.

        :param security_groups: The security groups to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59049fccbead79b85bcbad3ce6d6a3d892ce907c75f9f0c4a38950b4f006cac)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [*security_groups]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMongoDb).__jsii_proxy_class__ = lambda : _IMongoDbProxy


@jsii.interface(jsii_type="aws-rfdk.IMonitorableFleet")
class IMonitorableFleet(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''Interface for the fleet which can be registered to Health Monitor.

    This declares methods to be implemented by different kind of fleets
    like ASG, Spot etc.
    '''

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> jsii.Number:
        '''This field expects the maximum instance count this fleet can have.

        eg.: maxCapacity for an ASG
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetCapacityMetric")
    def target_capacity_metric(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.IMetric:
        '''This field expects the base capacity metric of the fleet against which, the healthy percent will be calculated.

        eg.: GroupDesiredCapacity for an ASG
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetScope")
    def target_scope(self) -> _constructs_77d1e7e8.Construct:
        '''This field expects the scope in which to create the monitoring resource like TargetGroups, Listener etc.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetToMonitor")
    def target_to_monitor(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget:
        '''This field expects the component of type IApplicationLoadBalancerTarget which can be attached to Application Load Balancer for monitoring.

        eg. An AutoScalingGroup
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetUpdatePolicy")
    def target_update_policy(self) -> _aws_cdk_aws_iam_ceddda9d.IPolicy:
        '''This field expects a policy which can be attached to the lambda execution role so that it is capable of suspending the fleet.

        eg.: autoscaling:UpdateAutoScalingGroup permission for an ASG
        '''
        ...


class _IMonitorableFleetProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''Interface for the fleet which can be registered to Health Monitor.

    This declares methods to be implemented by different kind of fleets
    like ASG, Spot etc.
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IMonitorableFleet"

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> jsii.Number:
        '''This field expects the maximum instance count this fleet can have.

        eg.: maxCapacity for an ASG
        '''
        return typing.cast(jsii.Number, jsii.get(self, "targetCapacity"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacityMetric")
    def target_capacity_metric(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.IMetric:
        '''This field expects the base capacity metric of the fleet against which, the healthy percent will be calculated.

        eg.: GroupDesiredCapacity for an ASG
        '''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IMetric, jsii.get(self, "targetCapacityMetric"))

    @builtins.property
    @jsii.member(jsii_name="targetScope")
    def target_scope(self) -> _constructs_77d1e7e8.Construct:
        '''This field expects the scope in which to create the monitoring resource like TargetGroups, Listener etc.'''
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "targetScope"))

    @builtins.property
    @jsii.member(jsii_name="targetToMonitor")
    def target_to_monitor(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget:
        '''This field expects the component of type IApplicationLoadBalancerTarget which can be attached to Application Load Balancer for monitoring.

        eg. An AutoScalingGroup
        '''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget, jsii.get(self, "targetToMonitor"))

    @builtins.property
    @jsii.member(jsii_name="targetUpdatePolicy")
    def target_update_policy(self) -> _aws_cdk_aws_iam_ceddda9d.IPolicy:
        '''This field expects a policy which can be attached to the lambda execution role so that it is capable of suspending the fleet.

        eg.: autoscaling:UpdateAutoScalingGroup permission for an ASG
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPolicy, jsii.get(self, "targetUpdatePolicy"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMonitorableFleet).__jsii_proxy_class__ = lambda : _IMonitorableFleetProxy


@jsii.interface(jsii_type="aws-rfdk.IMountableLinuxFilesystem")
class IMountableLinuxFilesystem(typing_extensions.Protocol):
    '''A filesystem that can be mounted onto a Linux system.'''

    @jsii.member(jsii_name="mountToLinuxInstance")
    def mount_to_linux_instance(
        self,
        target: "IMountingInstance",
        *,
        location: builtins.str,
        permissions: typing.Optional["MountPermissions"] = None,
    ) -> None:
        '''Mount the filesystem to the given instance at instance startup.

        This is accomplished by
        adding scripting to the UserData of the instance to mount the filesystem on startup.
        If required, the instance's security group is granted ingress to the filesystem's security
        group on the required ports.

        :param target: Target instance to mount the filesystem to.
        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE
        '''
        ...

    @jsii.member(jsii_name="usesUserPosixPermissions")
    def uses_user_posix_permissions(self) -> builtins.bool:
        '''Returns whether the mounted file-system evaluates the UID/GID of the system user accessing the file-system.

        Some network file-systems provide features to fix a UID/GID for all access to the mounted file-system and ignore
        the system user accessing the file. If this is the case, an implementing class must indicate this in the return
        value.
        '''
        ...


class _IMountableLinuxFilesystemProxy:
    '''A filesystem that can be mounted onto a Linux system.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IMountableLinuxFilesystem"

    @jsii.member(jsii_name="mountToLinuxInstance")
    def mount_to_linux_instance(
        self,
        target: "IMountingInstance",
        *,
        location: builtins.str,
        permissions: typing.Optional["MountPermissions"] = None,
    ) -> None:
        '''Mount the filesystem to the given instance at instance startup.

        This is accomplished by
        adding scripting to the UserData of the instance to mount the filesystem on startup.
        If required, the instance's security group is granted ingress to the filesystem's security
        group on the required ports.

        :param target: Target instance to mount the filesystem to.
        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5271928b2275188a85699b7957d3e2ea9a76e0c869963434c43548c64d4b1661)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        mount = LinuxMountPointProps(location=location, permissions=permissions)

        return typing.cast(None, jsii.invoke(self, "mountToLinuxInstance", [target, mount]))

    @jsii.member(jsii_name="usesUserPosixPermissions")
    def uses_user_posix_permissions(self) -> builtins.bool:
        '''Returns whether the mounted file-system evaluates the UID/GID of the system user accessing the file-system.

        Some network file-systems provide features to fix a UID/GID for all access to the mounted file-system and ignore
        the system user accessing the file. If this is the case, an implementing class must indicate this in the return
        value.
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "usesUserPosixPermissions", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMountableLinuxFilesystem).__jsii_proxy_class__ = lambda : _IMountableLinuxFilesystemProxy


@jsii.interface(jsii_type="aws-rfdk.IScriptHost")
class IScriptHost(_aws_cdk_aws_iam_ceddda9d.IGrantable, typing_extensions.Protocol):
    '''An interface that unifies the common methods and properties of:.

    - {@link @aws-cdk/aws-ec2#Instance}
    - {@link @aws-cdk/aws-autoscaling#AutoScalingGroup}

    so that they can be uniformly targeted to download and execute a script asset.
    '''

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType:
        '''The operating system of the script host.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''The user data of the script host.'''
        ...


class _IScriptHostProxy(
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''An interface that unifies the common methods and properties of:.

    - {@link @aws-cdk/aws-ec2#Instance}
    - {@link @aws-cdk/aws-autoscaling#AutoScalingGroup}

    so that they can be uniformly targeted to download and execute a script asset.
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IScriptHost"

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType:
        '''The operating system of the script host.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.OperatingSystemType, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''The user data of the script host.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.get(self, "userData"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScriptHost).__jsii_proxy_class__ = lambda : _IScriptHostProxy


@jsii.interface(jsii_type="aws-rfdk.IX509CertificatePem")
class IX509CertificatePem(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Interface for fields found on an X509Certificate construct.'''

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The public certificate chain for this X.509 Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the chain is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The private key for this X509Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the key is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.

        Note that the private key is encrypted. The passphrase is stored in the the passphrase Secret.

        If you need to decrypt the private key into an unencrypted form, then you can:
        0. Caution. Decrypting a private key adds a security risk by making it easier to obtain your private key.

        1. Copy the contents of the Secret to a file called 'encrypted.key'
        2. Run: openssl rsa -in encrypted.key -out decrypted.key
        3. Enter the passphrase at the prompt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the private key is stored in the 'SecretString' of this Secret.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="certChain")
    def cert_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A Secret that contains the chain of Certificates used to sign this Certificate.

        :default: : No certificate chain is used, signifying a self-signed Certificate
        '''
        ...


class _IX509CertificatePemProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Interface for fields found on an X509Certificate construct.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IX509CertificatePem"

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The public certificate chain for this X.509 Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the chain is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The private key for this X509Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the key is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.

        Note that the private key is encrypted. The passphrase is stored in the the passphrase Secret.

        If you need to decrypt the private key into an unencrypted form, then you can:
        0. Caution. Decrypting a private key adds a security risk by making it easier to obtain your private key.

        1. Copy the contents of the Secret to a file called 'encrypted.key'
        2. Run: openssl rsa -in encrypted.key -out decrypted.key
        3. Enter the passphrase at the prompt
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the private key is stored in the 'SecretString' of this Secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "passphrase"))

    @builtins.property
    @jsii.member(jsii_name="certChain")
    def cert_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A Secret that contains the chain of Certificates used to sign this Certificate.

        :default: : No certificate chain is used, signifying a self-signed Certificate
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "certChain"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IX509CertificatePem).__jsii_proxy_class__ = lambda : _IX509CertificatePemProxy


@jsii.interface(jsii_type="aws-rfdk.IX509CertificatePkcs12")
class IX509CertificatePkcs12(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''Properties of an X.509 PKCS #12 file.'''

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The PKCS #12 data is stored in the 'SecretBinary' of this Secret.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the cert is stored in the 'SecretString' of this Secret.'''
        ...


class _IX509CertificatePkcs12Proxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Properties of an X.509 PKCS #12 file.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IX509CertificatePkcs12"

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The PKCS #12 data is stored in the 'SecretBinary' of this Secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the cert is stored in the 'SecretString' of this Secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "passphrase"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IX509CertificatePkcs12).__jsii_proxy_class__ = lambda : _IX509CertificatePkcs12Proxy


@jsii.implements(_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate)
class ImportedAcmCertificate(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.ImportedAcmCertificate",
):
    '''A Construct that creates an AWS CloudFormation Custom Resource that models a certificate that is imported into AWS Certificate Manager (ACM).

    It uses an AWS Lambda Function to extract the certificate from Secrets in AWS SecretsManager
    and then import it into ACM. The interface is intended to be used with the {@link X509CertificatePem } Construct.

    architecture diagram


    Resources Deployed

    - DynamoDB Table - Used for tracking resources created by the Custom Resource.
    - An AWS Lambda Function, with IAM Role - Used to create/update/delete the Custom Resource.
    - AWS Certificate Manager Certificate - Created by the Custom Resource.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The AWS Lambda for this construct also has broad IAM permissions to delete any Certificate that is stored
      in AWS Certificate Manager. You should not grant any additional actors/principals the ability to modify or
      execute this Lambda.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cert: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        key: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        passphrase: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        cert_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cert: A Secret that contains the Certificate data.
        :param key: A Secret that contains the encrypted Private Key data.
        :param passphrase: A Secret that contains the passphrase of the encrypted Private Key.
        :param cert_chain: A Secret that contains the chain of Certificates used to sign this Certificate. Default: : No certificate chain is used, signifying a self-signed Certificate
        :param encryption_key: The KMS Key used to encrypt the secrets. The Custom Resource to import the Certificate to ACM will be granted permission to decrypt Secrets using this Key. Default: : If the account's default CMK was used to encrypt the Secrets, no special permissions need to be given
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007bf741112c4ffd6fdde5cb15520ec322690e578859a3a9454a714a8221b83c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImportedAcmCertificateProps(
            cert=cert,
            key=key,
            passphrase=passphrase,
            cert_chain=cert_chain,
            encryption_key=encryption_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''Apply a removal policy to the custom resource that represents the certificate imported into ACM.

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad608c351636827791d224b1f58214b7f409c0f35f71b8e32b3933b326a8dba)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [policy]))

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :inheritdoc: true
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDaysToExpiry", [props]))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The ARN for the Certificate that was imported into ACM.'''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def _database(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''The DynamoDB Table that is used as a backing store for the CustomResource utilized in this construct.'''
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        '''The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.

        :inheritdoc: true
        '''
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def _resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The stack in which this resource is defined.

        :inheritdoc: true
        '''
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="uniqueTag")
    def _unique_tag(self) -> _aws_cdk_ceddda9d.Tag:
        '''A unique tag that is applied to this certificate that can be used to grant permissions to it.'''
        return typing.cast(_aws_cdk_ceddda9d.Tag, jsii.get(self, "uniqueTag"))


@jsii.data_type(
    jsii_type="aws-rfdk.ImportedAcmCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "cert": "cert",
        "key": "key",
        "passphrase": "passphrase",
        "cert_chain": "certChain",
        "encryption_key": "encryptionKey",
    },
)
class ImportedAcmCertificateProps:
    def __init__(
        self,
        *,
        cert: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        key: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        passphrase: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        cert_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''Properties for importing a Certificate from Secrets into ACM.

        :param cert: A Secret that contains the Certificate data.
        :param key: A Secret that contains the encrypted Private Key data.
        :param passphrase: A Secret that contains the passphrase of the encrypted Private Key.
        :param cert_chain: A Secret that contains the chain of Certificates used to sign this Certificate. Default: : No certificate chain is used, signifying a self-signed Certificate
        :param encryption_key: The KMS Key used to encrypt the secrets. The Custom Resource to import the Certificate to ACM will be granted permission to decrypt Secrets using this Key. Default: : If the account's default CMK was used to encrypt the Secrets, no special permissions need to be given
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd0d88a96f9c5734743f08fa09845715c16d4a270389b929385061cf9e06969)
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument passphrase", value=passphrase, expected_type=type_hints["passphrase"])
            check_type(argname="argument cert_chain", value=cert_chain, expected_type=type_hints["cert_chain"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert": cert,
            "key": key,
            "passphrase": passphrase,
        }
        if cert_chain is not None:
            self._values["cert_chain"] = cert_chain
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''A Secret that contains the Certificate data.'''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def key(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''A Secret that contains the encrypted Private Key data.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''A Secret that contains the passphrase of the encrypted Private Key.'''
        result = self._values.get("passphrase")
        assert result is not None, "Required property 'passphrase' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def cert_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A Secret that contains the chain of Certificates used to sign this Certificate.

        :default: : No certificate chain is used, signifying a self-signed Certificate
        '''
        result = self._values.get("cert_chain")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The KMS Key used to encrypt the secrets.

        The Custom Resource to import the Certificate to ACM will be granted
        permission to decrypt Secrets using this Key.

        :default: : If the account's default CMK was used to encrypt the Secrets, no special permissions need to be given
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImportedAcmCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.Limit",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "name": "name"},
)
class Limit:
    def __init__(self, *, max: jsii.Number, name: builtins.str) -> None:
        '''Information about an Elastic Load Balancing resource limit for your AWS account.

        :param max: The maximum value of the limit.
        :param name: The name of the limit. The possible values are:. application-load-balancers listeners-per-application-load-balancer listeners-per-network-load-balancer network-load-balancers rules-per-application-load-balancer target-groups target-groups-per-action-on-application-load-balancer target-groups-per-action-on-network-load-balancer target-groups-per-application-load-balancer targets-per-application-load-balancer targets-per-availability-zone-per-network-load-balancer targets-per-network-load-balancer

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_Limit.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e455b38bcb04a52144b7f18ac2f60adca374fdd61d4d782e4540f5093a6b73)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "name": name,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''The maximum value of the limit.'''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the limit. The possible values are:.

        application-load-balancers
        listeners-per-application-load-balancer
        listeners-per-network-load-balancer
        network-load-balancers
        rules-per-application-load-balancer
        target-groups
        target-groups-per-action-on-application-load-balancer
        target-groups-per-action-on-network-load-balancer
        target-groups-per-application-load-balancer
        targets-per-application-load-balancer
        targets-per-availability-zone-per-network-load-balancer
        targets-per-network-load-balancer
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Limit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.LinuxMountPointProps",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "permissions": "permissions"},
)
class LinuxMountPointProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        permissions: typing.Optional["MountPermissions"] = None,
    ) -> None:
        '''Properties for the mount point of a filesystem on a Linux system.

        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ab164dc4e5b0f1349e200824495832c9defa2ce58961d1221834bcab59123d)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def location(self) -> builtins.str:
        '''Directory for the mount point.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(self) -> typing.Optional["MountPermissions"]:
        '''File permissions for the mounted filesystem.

        :default: MountPermissions.READWRITE
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional["MountPermissions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxMountPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogGroupFactory(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.LogGroupFactory"):
    '''This factory will return an ILogGroup based on the configuration provided to it.

    The LogGroup will either be
    wrapped in a LogRetention from the aws-lambda package that has the ability to look up and reuse an existing LogGroup
    or an ExportingLogGroup that uses a LogRetention and adds additional functionality to export the logs to S3.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="createOrFetch")
    @builtins.classmethod
    def create_or_fetch(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        log_wrapper_id: builtins.str,
        log_group_name: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        log_group_prefix: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''Either create a new LogGroup given the LogGroup name, or return the existing LogGroup.

        :param scope: -
        :param log_wrapper_id: -
        :param log_group_name: -
        :param bucket_name: The S3 bucket's name to export logs to. Setting this will enable exporting logs from CloudWatch to S3. Default: - No export to S3 will be performed.
        :param log_group_prefix: Prefix assigned to the name of any LogGroups that get created. Default: - No prefix will be applied.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the day before they expire. Default: - 3 days.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8528d10537a4bbd86945bc9163a000afa02a3fbb1a26818bd9505bd909306c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument log_wrapper_id", value=log_wrapper_id, expected_type=type_hints["log_wrapper_id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
        props = LogGroupFactoryProps(
            bucket_name=bucket_name,
            log_group_prefix=log_group_prefix,
            retention=retention,
        )

        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.sinvoke(cls, "createOrFetch", [scope, log_wrapper_id, log_group_name, props]))


@jsii.data_type(
    jsii_type="aws-rfdk.LogGroupFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "log_group_prefix": "logGroupPrefix",
        "retention": "retention",
    },
)
class LogGroupFactoryProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        log_group_prefix: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''Properties for creating a LogGroup.

        :param bucket_name: The S3 bucket's name to export logs to. Setting this will enable exporting logs from CloudWatch to S3. Default: - No export to S3 will be performed.
        :param log_group_prefix: Prefix assigned to the name of any LogGroups that get created. Default: - No prefix will be applied.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the day before they expire. Default: - 3 days.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d3f4653a05483f8662df72dcd865804ecded19419422cdd06a4de9dcd75d45)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument log_group_prefix", value=log_group_prefix, expected_type=type_hints["log_group_prefix"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if log_group_prefix is not None:
            self._values["log_group_prefix"] = log_group_prefix
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The S3 bucket's name to export logs to.

        Setting this will enable exporting logs from CloudWatch to S3.

        :default: - No export to S3 will be performed.
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix assigned to the name of any LogGroups that get created.

        :default: - No prefix will be applied.
        '''
        result = self._values.get("log_group_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        Exportation to S3 will happen the day before
        they expire.

        :default: - 3 days.
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_zone": "dnsZone",
        "hostname": "hostname",
        "server_certificate": "serverCertificate",
        "version": "version",
        "admin_user": "adminUser",
        "mongo_data_volume": "mongoDataVolume",
        "user_sspl_acceptance": "userSsplAcceptance",
    },
)
class MongoDbApplicationProps:
    def __init__(
        self,
        *,
        dns_zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
        hostname: builtins.str,
        server_certificate: IX509CertificatePem,
        version: "MongoDbVersion",
        admin_user: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        mongo_data_volume: typing.Optional[typing.Union["MongoDbInstanceVolumeProps", typing.Dict[builtins.str, typing.Any]]] = None,
        user_sspl_acceptance: typing.Optional["MongoDbSsplLicenseAcceptance"] = None,
    ) -> None:
        '''Settings for the MongoDB application that will be running on a {@link MongoDbInstance}.

        :param dns_zone: Private DNS zone to register the MongoDB hostname within. An A Record will automatically be created within this DNS zone for the provided hostname to allow connection to MongoDB's static private IP.
        :param hostname: The hostname to register the MongoDB's listening interface as. The hostname must be from 1 to 63 characters long and may contain only the letters from a-z, digits from 0-9, and the hyphen character. The fully qualified domain name (FQDN) of this host will be this hostname dot the zoneName of the given dnsZone.
        :param server_certificate: A certificate that provides proof of identity for the MongoDB application. The DomainName, or CommonName, of the provided certificate must exactly match the fully qualified host name of this host. This certificate must not be self-signed; that is the given certificate must have a defined certChain property. This certificate will be used to secure encrypted network connections to the MongoDB application with the clients that connect to it.
        :param version: What version of MongoDB to install on the instance.
        :param admin_user: A secret containing credentials for the admin user of the database. The contents of this secret must be a JSON document with the keys "username" and "password". ex: { "username": , "password": , } If this user already exists in the database, then its credentials will not be modified in any way to match the credentials in this secret. Doing so automatically would be a security risk. If created, then the admin user will have the database role: [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ] Default: Credentials will be randomly generated for the admin user.
        :param mongo_data_volume: Specification of the Amazon Elastic Block Storage (EBS) Volume that will be used by the instance to store the MongoDB database's data. The Volume must not be partitioned. The volume will be mounted to /var/lib/mongo on this instance, and all files on it will be changed to be owned by the mongod user on the instance. Default: A new 20 GiB encrypted EBS volume is created to store the MongoDB database data.
        :param user_sspl_acceptance: MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstance must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstance} will be allowed to install MongoDB. Default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        if isinstance(mongo_data_volume, dict):
            mongo_data_volume = MongoDbInstanceVolumeProps(**mongo_data_volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0e67b2e068f82597a8e160692e4068c8b7f72b3c5d504539eaa2b7b8b5cab5)
            check_type(argname="argument dns_zone", value=dns_zone, expected_type=type_hints["dns_zone"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument server_certificate", value=server_certificate, expected_type=type_hints["server_certificate"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument admin_user", value=admin_user, expected_type=type_hints["admin_user"])
            check_type(argname="argument mongo_data_volume", value=mongo_data_volume, expected_type=type_hints["mongo_data_volume"])
            check_type(argname="argument user_sspl_acceptance", value=user_sspl_acceptance, expected_type=type_hints["user_sspl_acceptance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_zone": dns_zone,
            "hostname": hostname,
            "server_certificate": server_certificate,
            "version": version,
        }
        if admin_user is not None:
            self._values["admin_user"] = admin_user
        if mongo_data_volume is not None:
            self._values["mongo_data_volume"] = mongo_data_volume
        if user_sspl_acceptance is not None:
            self._values["user_sspl_acceptance"] = user_sspl_acceptance

    @builtins.property
    def dns_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone:
        '''Private DNS zone to register the MongoDB hostname within.

        An A Record will automatically be created
        within this DNS zone for the provided hostname to allow connection to MongoDB's static private IP.
        '''
        result = self._values.get("dns_zone")
        assert result is not None, "Required property 'dns_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''The hostname to register the MongoDB's listening interface as.

        The hostname must be
        from 1 to 63 characters long and may contain only the letters from a-z, digits from 0-9,
        and the hyphen character.

        The fully qualified domain name (FQDN) of this host will be this hostname dot the zoneName
        of the given dnsZone.
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_certificate(self) -> IX509CertificatePem:
        '''A certificate that provides proof of identity for the MongoDB application.

        The DomainName, or
        CommonName, of the provided certificate must exactly match the fully qualified host name
        of this host. This certificate must not be self-signed; that is the given certificate must have
        a defined certChain property.

        This certificate will be used to secure encrypted network connections to the MongoDB application
        with the clients that connect to it.
        '''
        result = self._values.get("server_certificate")
        assert result is not None, "Required property 'server_certificate' is missing"
        return typing.cast(IX509CertificatePem, result)

    @builtins.property
    def version(self) -> "MongoDbVersion":
        '''What version of MongoDB to install on the instance.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast("MongoDbVersion", result)

    @builtins.property
    def admin_user(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A secret containing credentials for the admin user of the database.

        The contents of this
        secret must be a JSON document with the keys "username" and "password". ex:
        {
        "username": ,
        "password": ,
        }
        If this user already exists in the database, then its credentials will not be modified in any way
        to match the credentials in this secret. Doing so automatically would be a security risk.

        If created, then the admin user will have the database role:
        [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ]

        :default: Credentials will be randomly generated for the admin user.
        '''
        result = self._values.get("admin_user")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def mongo_data_volume(self) -> typing.Optional["MongoDbInstanceVolumeProps"]:
        '''Specification of the Amazon Elastic Block Storage (EBS) Volume that will be used by the instance to store the MongoDB database's data.

        The Volume must not be partitioned. The volume will be mounted to /var/lib/mongo on this instance,
        and all files on it will be changed to be owned by the mongod user on the instance.

        :default: A new 20 GiB encrypted EBS volume is created to store the MongoDB database data.
        '''
        result = self._values.get("mongo_data_volume")
        return typing.cast(typing.Optional["MongoDbInstanceVolumeProps"], result)

    @builtins.property
    def user_sspl_acceptance(self) -> typing.Optional["MongoDbSsplLicenseAcceptance"]:
        '''MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstance must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstance} will be allowed to install MongoDB.

        :default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        result = self._values.get("user_sspl_acceptance")
        return typing.cast(typing.Optional["MongoDbSsplLicenseAcceptance"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MongoDbInstaller(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.MongoDbInstaller"):
    '''This class provides a mechanism to install a version of MongoDB Community Edition during the initial launch of an instance.

    MongoDB is installed from the official sources using the system
    package manger (yum). It installs the mongodb-org metapackage which will install the following packages:

    1. mongodb-org-mongos;
    2. mongodb-org-server;
    3. mongodb-org-shell; and
    4. mongodb-org-tools.

    Successful installation of MongoDB with this class requires:

    1. Explicit acceptance of the terms of the SSPL license, under which MongoDB is distributed; and
    2. The instance on which the installation is being performed is in a subnet that can access
       the official MongoDB sites: https://repo.mongodb.org/ and https://www.mongodb.org



    Resources Deployed

    - A CDK Asset package containing the installation scripts is deployed to your CDK staging bucket.



    Security Considerations

    - Since this class installs MongoDB from official sources dynamically during instance start-up, it is succeptable
      to an attacker compromising the official MongoDB Inc. distribution channel for MongoDB. Such a compromise may
      result in the installation of unauthorized MongoDB binaries. Executing this attack would require an attacker
      compromise both the official installation packages and the MongoDB Inc. gpg key with which they are signed.
    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        version: "MongoDbVersion",
        user_sspl_acceptance: typing.Optional["MongoDbSsplLicenseAcceptance"] = None,
    ) -> None:
        '''
        :param scope: -
        :param version: The version of MongoDB to install.
        :param user_sspl_acceptance: MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstaller must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstaller} will be allowed to install MongoDB. Default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b23a390fe61f77052147d302b356a6f1638c251d56f9bdfcea550dd5a32181a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = MongoDbInstallerProps(
            version=version, user_sspl_acceptance=user_sspl_acceptance
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="installerAssetSingleton")
    def _installer_asset_singleton(self) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''Fetch the Asset singleton for the installation script, or generate it if needed.'''
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, jsii.invoke(self, "installerAssetSingleton", []))

    @jsii.member(jsii_name="installOnLinuxInstance")
    def install_on_linux_instance(self, target: IScriptHost) -> None:
        '''Install MongoDB to the given instance at instance startup.

        This is accomplished by
        adding scripting to the instance's UserData to install MongoDB.

        Notes:

        1. The instance on which the installation is being performed must be in a subnet that can access
           the official MongoDB sites: https://repo.mongodb.org/ and https://www.mongodb.org; and
        2. At this time, this method only supports installation onto instances that are running an operating system
           that is compatible with x86-64 RedHat 7 -- this includes Amazon Linux 2, RedHat 7, and CentOS 7.

        :param target: The target instance onto which to install MongoDB.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8123ef5813eb0eb58a8a64aa65ad09cd8efe784bdc7578292ef430a8807a001)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "installOnLinuxInstance", [target]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "MongoDbInstallerProps":
        return typing.cast("MongoDbInstallerProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbInstallerProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version", "user_sspl_acceptance": "userSsplAcceptance"},
)
class MongoDbInstallerProps:
    def __init__(
        self,
        *,
        version: "MongoDbVersion",
        user_sspl_acceptance: typing.Optional["MongoDbSsplLicenseAcceptance"] = None,
    ) -> None:
        '''Properties that are required to create a {@link MongoDbInstaller}.

        :param version: The version of MongoDB to install.
        :param user_sspl_acceptance: MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstaller must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstaller} will be allowed to install MongoDB. Default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b496f200afaf6e5b0f3f6e857ceb8372ec3b62603f22e2d6473892f954349884)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument user_sspl_acceptance", value=user_sspl_acceptance, expected_type=type_hints["user_sspl_acceptance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if user_sspl_acceptance is not None:
            self._values["user_sspl_acceptance"] = user_sspl_acceptance

    @builtins.property
    def version(self) -> "MongoDbVersion":
        '''The version of MongoDB to install.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast("MongoDbVersion", result)

    @builtins.property
    def user_sspl_acceptance(self) -> typing.Optional["MongoDbSsplLicenseAcceptance"]:
        '''MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstaller must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstaller} will be allowed to install MongoDB.

        :default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        result = self._values.get("user_sspl_acceptance")
        return typing.cast(typing.Optional["MongoDbSsplLicenseAcceptance"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstallerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMongoDb, _aws_cdk_aws_iam_ceddda9d.IGrantable)
class MongoDbInstance(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.MongoDbInstance",
):
    '''This construct provides a {@link StaticPrivateIpServer} that is hosting MongoDB.

    The data for this MongoDB database
    is stored in an Amazon Elastic Block Storage (EBS) Volume that is automatically attached to the instance when it is
    launched, and is separate from the instance's root volume; it is recommended that you set up a backup schedule for
    this volume.

    When this instance is first launched, or relaunched after an instance replacement, it will:

    1. Attach an EBS volume to /var/lib/mongo upon which the MongoDB data is stored;
    2. Automatically install the specified version of MongoDB, from the official Mongo Inc. sources;
    3. Create an admin user in that database if one has not yet been created -- the credentials for this user
       can be provided by you, or randomly generated;
    4. Configure MongoDB to require authentication, and only allow encrypted connections over TLS.

    The instance's launch logs and MongoDB logs will be automatically stored in Amazon CloudWatch logs; the
    default log group name is: /renderfarm/


    Resources Deployed

    - {@link StaticPrivateIpServer} that hosts MongoDB.
    - An A-Record in the provided PrivateHostedZone to create a DNS entry for this server's static private IP.
    - A Secret in AWS SecretsManager that contains the administrator credentials for MongoDB.
    - An encrypted Amazon Elastic Block Store (EBS) Volume on which the MongoDB data is stored.
    - Amazon CloudWatch log group that contains instance-launch and MongoDB application logs.



    Security Considerations

    - The administrator credentials for MongoDB are stored in a Secret within AWS SecretsManager. You must strictly limit
      access to this secret to only entities that require it.
    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The EBS Volume that is created by, or provided to, this construct is used to store the contents of your MongoDB data. To
      protect the sensitive data in your database, you should not grant access to this EBS Volume to any principal or instance
      other than the instance created by this construct. Furthermore, we recommend that you ensure that the volume that is
      used for this purpose is encrypted at rest.
    - This construct uses this package's {@link StaticPrivateIpServer}, {@link MongoDbInstaller}, {@link CloudWatchAgent},
      {@link ExportingLogGroup }, and {@link MountableBlockVolume}. Security considerations that are outlined by the documentation
      for those constructs should also be taken into account.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        mongo_db: typing.Union[MongoDbApplicationProps, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[LogGroupFactoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mongo_db: Properties for the MongoDB application that will be running on the instance.
        :param vpc: The VPC in which to create the MongoDbInstance.
        :param instance_type: The type of instance to launch. Note that this must be an x86-64 instance type. Default: r5.large
        :param key_name: Name of the EC2 SSH keypair to grant access to the instance. Default: No SSH access will be possible.
        :param log_group_props: Properties for setting up the MongoDB Instance's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param role: An IAM role to associate with the instance profile that is assigned to this instance. The role must be assumable by the service principal ``ec2.amazonaws.com`` Default: A role will automatically be created, it can be accessed via the ``role`` property.
        :param security_group: The security group to assign to this instance. Default: A new security group is created for this instance.
        :param vpc_subnets: Where to place the instance within the VPC. Default: The instance is placed within a Private subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e621ae9df55786e7b260e2d74dce3b522b6efaa597507a602a78a057336f1ae4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MongoDbInstanceProps(
            mongo_db=mongo_db,
            vpc=vpc,
            instance_type=instance_type,
            key_name=key_name,
            log_group_props=log_group_props,
            role=role,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds security groups to the database.

        :param security_groups: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85a56fe3ba0d570817245e78e1b7dbef19b124d3378fdad999df16a2627001f)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [*security_groups]))

    @jsii.member(jsii_name="configureCloudWatchLogStreams")
    def _configure_cloud_watch_log_streams(
        self,
        host: IScriptHost,
        group_name: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        log_group_prefix: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''Adds UserData commands to install & configure the CloudWatch Agent onto the instance.

        The commands configure the agent to stream the following logs to a new CloudWatch log group:

        - The cloud-init log
        - The MongoDB application log.

        :param host: The instance/host to setup the CloudWatchAgent upon.
        :param group_name: Name to append to the log group prefix when forming the log group name.
        :param bucket_name: The S3 bucket's name to export logs to. Setting this will enable exporting logs from CloudWatch to S3. Default: - No export to S3 will be performed.
        :param log_group_prefix: Prefix assigned to the name of any LogGroups that get created. Default: - No prefix will be applied.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the day before they expire. Default: - 3 days.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd72ba805b523adaf73080f33bb5a18bdc09fd7c72d04304d2b7cdbce52f177)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        log_group_props = LogGroupFactoryProps(
            bucket_name=bucket_name,
            log_group_prefix=log_group_prefix,
            retention=retention,
        )

        return typing.cast(None, jsii.invoke(self, "configureCloudWatchLogStreams", [host, group_name, log_group_props]))

    @jsii.member(jsii_name="configureMongoDb")
    def _configure_mongo_db(
        self,
        instance: "StaticPrivateIpServer",
        *,
        dns_zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
        hostname: builtins.str,
        server_certificate: IX509CertificatePem,
        version: "MongoDbVersion",
        admin_user: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        mongo_data_volume: typing.Optional[typing.Union["MongoDbInstanceVolumeProps", typing.Dict[builtins.str, typing.Any]]] = None,
        user_sspl_acceptance: typing.Optional["MongoDbSsplLicenseAcceptance"] = None,
    ) -> None:
        '''Adds commands to the userData of the instance to install MongoDB, create an admin user if one does not exist, and to to start mongod running.

        :param instance: -
        :param dns_zone: Private DNS zone to register the MongoDB hostname within. An A Record will automatically be created within this DNS zone for the provided hostname to allow connection to MongoDB's static private IP.
        :param hostname: The hostname to register the MongoDB's listening interface as. The hostname must be from 1 to 63 characters long and may contain only the letters from a-z, digits from 0-9, and the hyphen character. The fully qualified domain name (FQDN) of this host will be this hostname dot the zoneName of the given dnsZone.
        :param server_certificate: A certificate that provides proof of identity for the MongoDB application. The DomainName, or CommonName, of the provided certificate must exactly match the fully qualified host name of this host. This certificate must not be self-signed; that is the given certificate must have a defined certChain property. This certificate will be used to secure encrypted network connections to the MongoDB application with the clients that connect to it.
        :param version: What version of MongoDB to install on the instance.
        :param admin_user: A secret containing credentials for the admin user of the database. The contents of this secret must be a JSON document with the keys "username" and "password". ex: { "username": , "password": , } If this user already exists in the database, then its credentials will not be modified in any way to match the credentials in this secret. Doing so automatically would be a security risk. If created, then the admin user will have the database role: [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ] Default: Credentials will be randomly generated for the admin user.
        :param mongo_data_volume: Specification of the Amazon Elastic Block Storage (EBS) Volume that will be used by the instance to store the MongoDB database's data. The Volume must not be partitioned. The volume will be mounted to /var/lib/mongo on this instance, and all files on it will be changed to be owned by the mongod user on the instance. Default: A new 20 GiB encrypted EBS volume is created to store the MongoDB database data.
        :param user_sspl_acceptance: MongoDB Community edition is licensed under the terms of the SSPL (see: https://www.mongodb.com/licensing/server-side-public-license ). Users of MongoDbInstance must explicitly signify their acceptance of the terms of the SSPL through this property before the {@link MongoDbInstance} will be allowed to install MongoDB. Default: MongoDbSsplLicenseAcceptance.USER_REJECTS_SSPL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dde051e64c0e787cd1dbe573de358b27b9e730c84cc713ab7ba1bd1cfc6f7d8)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        settings = MongoDbApplicationProps(
            dns_zone=dns_zone,
            hostname=hostname,
            server_certificate=server_certificate,
            version=version,
            admin_user=admin_user,
            mongo_data_volume=mongo_data_volume,
            user_sspl_acceptance=user_sspl_acceptance,
        )

        return typing.cast(None, jsii.invoke(self, "configureMongoDb", [instance, settings]))

    @builtins.property
    @jsii.member(jsii_name="adminUser")
    def admin_user(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''Credentials for the admin user of the database.

        This user has database role:
        [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ]
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "adminUser"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The certificate chain of trust for the MongoDB application's server certificate.

        The contents of this secret is a single string containing the trust chain in PEM format, and
        can be saved to a file that is then passed as the --sslCAFile option when connecting to MongoDB
        using the mongo shell.

        :inheritdoc: true
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "certificateChain"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Allows for providing security group connections to/from this instance.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="fullHostname")
    def full_hostname(self) -> builtins.str:
        '''The full host name that can be used to connect to the MongoDB application running on this instance.

        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fullHostname"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permission to.

        Granting permissions to this principal will grant
        those permissions to the instance role.
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="mongoDataVolume")
    def mongo_data_volume(self) -> _aws_cdk_aws_ec2_ceddda9d.IVolume:
        '''The EBS Volume on which we are storing the MongoDB database data.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVolume, jsii.get(self, "mongoDataVolume"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''The port to connect to for MongoDB.'''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The IAM role that is assumed by the instance.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> "StaticPrivateIpServer":
        '''The server that this construct creates to host MongoDB.'''
        return typing.cast("StaticPrivateIpServer", jsii.get(self, "server"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''The UserData for this instance.

        UserData is a script that is run automatically by the instance the very first time that a new instance is started.
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.get(self, "userData"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "MongoDbVersion":
        '''The version of MongoDB that is running on this instance.'''
        return typing.cast("MongoDbVersion", jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbInstanceNewVolumeProps",
    jsii_struct_bases=[],
    name_mapping={"encryption_key": "encryptionKey", "size": "size"},
)
class MongoDbInstanceNewVolumeProps:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    ) -> None:
        '''Specification for a when a new volume is being created by a MongoDbInstance.

        :param encryption_key: If creating a new EBS Volume, then this property provides a KMS key to use to encrypt the Volume's data. If you do not provide a value for this property, then your default service-owned KMS key will be used to encrypt the new Volume. Default: Your service-owned KMS key is used to encrypt a new volume.
        :param size: The size, in Gigabytes, of a new encrypted volume to be created to hold the MongoDB database data for this instance. A new volume is created only if a value for the volume property is not provided. Default: 20 GiB
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c41fb05dcf30d03a3068e6b753627e90fcc95fad10000daef3e0293f737b44)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''If creating a new EBS Volume, then this property provides a KMS key to use to encrypt the Volume's data.

        If you do not provide a value for this property, then your default
        service-owned KMS key will be used to encrypt the new Volume.

        :default: Your service-owned KMS key is used to encrypt a new volume.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''The size, in Gigabytes, of a new encrypted volume to be created to hold the MongoDB database data for this instance.

        A new volume is created only if a value for the volume property
        is not provided.

        :default: 20 GiB
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstanceNewVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "mongo_db": "mongoDb",
        "vpc": "vpc",
        "instance_type": "instanceType",
        "key_name": "keyName",
        "log_group_props": "logGroupProps",
        "role": "role",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class MongoDbInstanceProps:
    def __init__(
        self,
        *,
        mongo_db: typing.Union[MongoDbApplicationProps, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[LogGroupFactoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for a newly created {@link MongoDbInstance}.

        :param mongo_db: Properties for the MongoDB application that will be running on the instance.
        :param vpc: The VPC in which to create the MongoDbInstance.
        :param instance_type: The type of instance to launch. Note that this must be an x86-64 instance type. Default: r5.large
        :param key_name: Name of the EC2 SSH keypair to grant access to the instance. Default: No SSH access will be possible.
        :param log_group_props: Properties for setting up the MongoDB Instance's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param role: An IAM role to associate with the instance profile that is assigned to this instance. The role must be assumable by the service principal ``ec2.amazonaws.com`` Default: A role will automatically be created, it can be accessed via the ``role`` property.
        :param security_group: The security group to assign to this instance. Default: A new security group is created for this instance.
        :param vpc_subnets: Where to place the instance within the VPC. Default: The instance is placed within a Private subnet.
        '''
        if isinstance(mongo_db, dict):
            mongo_db = MongoDbApplicationProps(**mongo_db)
        if isinstance(log_group_props, dict):
            log_group_props = LogGroupFactoryProps(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90082e83281497abb52eaeae883b0134d9e66369c6c09101b997c94ebc72987)
            check_type(argname="argument mongo_db", value=mongo_db, expected_type=type_hints["mongo_db"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mongo_db": mongo_db,
            "vpc": vpc,
        }
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if key_name is not None:
            self._values["key_name"] = key_name
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def mongo_db(self) -> MongoDbApplicationProps:
        '''Properties for the MongoDB application that will be running on the instance.'''
        result = self._values.get("mongo_db")
        assert result is not None, "Required property 'mongo_db' is missing"
        return typing.cast(MongoDbApplicationProps, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the MongoDbInstance.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The type of instance to launch.

        Note that this must be an x86-64 instance type.

        :default: r5.large
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of the EC2 SSH keypair to grant access to the instance.

        :default: No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[LogGroupFactoryProps]:
        '''Properties for setting up the MongoDB Instance's LogGroup in CloudWatch.

        :default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[LogGroupFactoryProps], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile that is assigned to this instance.

        The role must be assumable by the service principal ``ec2.amazonaws.com``

        :default: A role will automatically be created, it can be accessed via the ``role`` property.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group to assign to this instance.

        :default: A new security group is created for this instance.
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the instance within the VPC.

        :default: The instance is placed within a Private subnet.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbInstanceVolumeProps",
    jsii_struct_bases=[],
    name_mapping={"volume": "volume", "volume_props": "volumeProps"},
)
class MongoDbInstanceVolumeProps:
    def __init__(
        self,
        *,
        volume: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVolume] = None,
        volume_props: typing.Optional[typing.Union[MongoDbInstanceNewVolumeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Specification of the Amazon Elastic Block Storage (EBS) Volume that will be used by a {@link MongoDbInstance} to store the MongoDB database's data.

        You must provide either an existing EBS Volume to mount to the instance, or the
        {@link MongoDbInstance} will create a new EBS Volume of the given size that is
        encrypted. The encryption will be with the given KMS key, if one is provided.

        :param volume: An existing EBS volume. This volume is mounted to the {@link MongoDbInstace } using the scripting in {@link MountableEbs }, and is subject to the restrictions outlined in that class. The Volume must not be partitioned. The volume will be mounted to /var/lib/mongo on this instance, and all files on it will be changed to be owned by the mongod user on the instance. This volume will contain all of the data that you store in MongoDB, so we recommend that you encrypt this volume. Default: A new encrypted volume is created for use by the instance.
        :param volume_props: Properties for a new volume that will be constructed for use by this instance. Default: A service-key encrypted 20Gb volume will be created.
        '''
        if isinstance(volume_props, dict):
            volume_props = MongoDbInstanceNewVolumeProps(**volume_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbefdbc270273ca4e3b0f6d9a1b3fe25fb5de4e57cd405e3c9e5540cbc0198f)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument volume_props", value=volume_props, expected_type=type_hints["volume_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if volume is not None:
            self._values["volume"] = volume
        if volume_props is not None:
            self._values["volume_props"] = volume_props

    @builtins.property
    def volume(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVolume]:
        '''An existing EBS volume.

        This volume is mounted to the {@link MongoDbInstace } using
        the scripting in {@link MountableEbs }, and is subject to the restrictions outlined
        in that class.

        The Volume must not be partitioned. The volume will be mounted to /var/lib/mongo on this instance,
        and all files on it will be changed to be owned by the mongod user on the instance.

        This volume will contain all of the data that you store in MongoDB, so we recommend that you
        encrypt this volume.

        :default: A new encrypted volume is created for use by the instance.
        '''
        result = self._values.get("volume")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVolume], result)

    @builtins.property
    def volume_props(self) -> typing.Optional[MongoDbInstanceNewVolumeProps]:
        '''Properties for a new volume that will be constructed for use by this instance.

        :default: A service-key encrypted 20Gb volume will be created.
        '''
        result = self._values.get("volume_props")
        return typing.cast(typing.Optional[MongoDbInstanceNewVolumeProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstanceVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MongoDbPostInstallSetup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.MongoDbPostInstallSetup",
):
    '''This construct performs post-installation setup on a MongoDB database by logging into the database, and executing commands against it.

    To provide this functionality, this construct will create an AWS Lambda function
    that is granted the ability to connect to the given MongoDB using its administrator credentials. This lambda
    is run automatically when you deploy or update the stack containing this construct. Logs for all AWS Lambdas are
    automatically recorded in Amazon CloudWatch.

    Presently, the only post-installation action that this construct can perform is creating users. There are two types
    of users that it can create:

    1. Password-authenticated users -- these users will be created within the 'admin' database.
    2. X.509-authenticated users -- these users will be created within the '$external' database.



    Resources Deployed

    - An AWS Lambda that is used to connect to the MongoDB application, and perform post-installation tasks.
    - A CloudFormation Custom Resource that triggers execution of the Lambda on stack deployment, update, and deletion.
    - An Amazon CloudWatch log group that records history of the AWS Lambda's execution.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The AWS Lambda function that is created by this resource has access to both the MongoDB administrator credentials,
      and the MongoDB application port. An attacker that can find a way to modify and execute this lambda could use it to
      modify or read any data in the database. You should not grant any additional actors/principals the ability to modify
      or execute this Lambda.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        mongo_db: IMongoDb,
        users: typing.Union["MongoDbUsers", typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mongo_db: The MongoDB that we will connect to to perform the post-installation steps upon.
        :param users: The Users that should be created in the MongoDB database. This construct will create these users only if they do not already exist. If a user does already exist, then it will not be modified.
        :param vpc: The VPC in which to create the network endpoint for the lambda function that is created by this construct.
        :param vpc_subnets: Where within the VPC to place the lambda function's endpoint. Default: The instance is placed within a Private subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b493fcc3de8a8c11a7912a14a89e48713c7dc223a06c821165a3f2d351a35d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MongoDbPostInstallSetupProps(
            mongo_db=mongo_db, users=users, vpc=vpc, vpc_subnets=vpc_subnets
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbPostInstallSetupProps",
    jsii_struct_bases=[],
    name_mapping={
        "mongo_db": "mongoDb",
        "users": "users",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class MongoDbPostInstallSetupProps:
    def __init__(
        self,
        *,
        mongo_db: IMongoDb,
        users: typing.Union["MongoDbUsers", typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Input properties for MongoDbPostInstallSetup.

        :param mongo_db: The MongoDB that we will connect to to perform the post-installation steps upon.
        :param users: The Users that should be created in the MongoDB database. This construct will create these users only if they do not already exist. If a user does already exist, then it will not be modified.
        :param vpc: The VPC in which to create the network endpoint for the lambda function that is created by this construct.
        :param vpc_subnets: Where within the VPC to place the lambda function's endpoint. Default: The instance is placed within a Private subnet.
        '''
        if isinstance(users, dict):
            users = MongoDbUsers(**users)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8e6b2e007846d0c58c1e5fc4e2986cb05fb6b018f6642266fd6bb2124bfe91)
            check_type(argname="argument mongo_db", value=mongo_db, expected_type=type_hints["mongo_db"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mongo_db": mongo_db,
            "users": users,
            "vpc": vpc,
        }
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def mongo_db(self) -> IMongoDb:
        '''The MongoDB that we will connect to to perform the post-installation steps upon.'''
        result = self._values.get("mongo_db")
        assert result is not None, "Required property 'mongo_db' is missing"
        return typing.cast(IMongoDb, result)

    @builtins.property
    def users(self) -> "MongoDbUsers":
        '''The Users that should be created in the MongoDB database.

        This construct will create these
        users only if they do not already exist. If a user does already exist, then it will not be modified.
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast("MongoDbUsers", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the network endpoint for the lambda function that is created by this construct.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where within the VPC to place the lambda function's endpoint.

        :default: The instance is placed within a Private subnet.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbPostInstallSetupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.MongoDbSsplLicenseAcceptance")
class MongoDbSsplLicenseAcceptance(enum.Enum):
    '''Choices for signifying the user's stance on the terms of the SSPL.

    See: https://www.mongodb.com/licensing/server-side-public-license
    '''

    USER_REJECTS_SSPL = "USER_REJECTS_SSPL"
    '''The user signifies their explicit rejection of the tems of the SSPL.'''
    USER_ACCEPTS_SSPL = "USER_ACCEPTS_SSPL"
    '''The user signifies their explicit acceptance of the terms of the SSPL.'''


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbUsers",
    jsii_struct_bases=[],
    name_mapping={
        "password_auth_users": "passwordAuthUsers",
        "x509_auth_users": "x509AuthUsers",
    },
)
class MongoDbUsers:
    def __init__(
        self,
        *,
        password_auth_users: typing.Optional[typing.Sequence[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]] = None,
        x509_auth_users: typing.Optional[typing.Sequence[typing.Union["MongoDbX509User", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''This interface is for defining a set of users to pass to MongoDbPostInstallSetup so that it can create them in the MongoDB.

        :param password_auth_users: Zero or more secrets containing credentials, and specification for users to be created in the admin database for authentication using SCRAM. See: https://docs.mongodb.com/v3.6/core/security-scram/ Each secret must be a JSON document with the following structure: { "username": , "password": , "roles": } For examples of the roles list, see the MongoDB user creation documentation. For example, https://docs.mongodb.com/manual/tutorial/create-users/ Default: No password-authenticated users are created.
        :param x509_auth_users: Information on the X.509-authenticated users that should be created. See: https://docs.mongodb.com/v3.6/core/security-x.509/. Default: No x.509 authenticated users are created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a31e98f1a2e4f2ef453c66a698577e62e73e396d0366d0ba3e18dd865eaae74)
            check_type(argname="argument password_auth_users", value=password_auth_users, expected_type=type_hints["password_auth_users"])
            check_type(argname="argument x509_auth_users", value=x509_auth_users, expected_type=type_hints["x509_auth_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password_auth_users is not None:
            self._values["password_auth_users"] = password_auth_users
        if x509_auth_users is not None:
            self._values["x509_auth_users"] = x509_auth_users

    @builtins.property
    def password_auth_users(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]]:
        '''Zero or more secrets containing credentials, and specification for users to be created in the admin database for authentication using SCRAM.

        See: https://docs.mongodb.com/v3.6/core/security-scram/

        Each secret must be a JSON document with the following structure:
        {
        "username": ,
        "password": ,
        "roles":
        }

        For examples of the roles list, see the MongoDB user creation documentation. For example,
        https://docs.mongodb.com/manual/tutorial/create-users/

        :default: No password-authenticated users are created.
        '''
        result = self._values.get("password_auth_users")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]], result)

    @builtins.property
    def x509_auth_users(self) -> typing.Optional[typing.List["MongoDbX509User"]]:
        '''Information on the X.509-authenticated users that should be created. See: https://docs.mongodb.com/v3.6/core/security-x.509/.

        :default: No x.509 authenticated users are created.
        '''
        result = self._values.get("x509_auth_users")
        return typing.cast(typing.Optional[typing.List["MongoDbX509User"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.MongoDbVersion")
class MongoDbVersion(enum.Enum):
    '''Versions of MongoDB Community Edition that the {@link MongoDbInstaller} is able to install.'''

    COMMUNITY_8_0 = "COMMUNITY_8_0"
    '''MongoDB 8.0 Community Edition. See: https://www.mongodb.com/docs/v8.0/introduction/.'''


@jsii.data_type(
    jsii_type="aws-rfdk.MongoDbX509User",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "roles": "roles"},
)
class MongoDbX509User:
    def __init__(
        self,
        *,
        certificate: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        roles: builtins.str,
    ) -> None:
        '''User added to the $external admin database.

        Referencing: https://docs.mongodb.com/v3.6/core/security-x.509/#member-certificate-requirements

        :param certificate: The certificate of the user that they will use for authentication. This must be a secret containing the plaintext string contents of the certificate in PEM format. For example, the cert property of {@link IX509CertificatePem } is compatible with this. Some important notes: 1. MongoDB **requires** that this username differ from the MongoDB server certificate in at least one of: Organization (O), Organizational Unit (OU), or Domain Component (DC). See: https://docs.mongodb.com/manual/tutorial/configure-x509-client-authentication/ 2. The client certificate must be signed by the same Certificate Authority (CA) as the server certificate that is being used by the MongoDB application.
        :param roles: JSON-encoded string with the roles this user should be given.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8a916c3b41e19d22b2c424bacbe2e2a9b8b7916d0068ab516c8ef8456e926c)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "roles": roles,
        }

    @builtins.property
    def certificate(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The certificate of the user that they will use for authentication.

        This must be a secret
        containing the plaintext string contents of the certificate in PEM format. For example,
        the cert property of {@link IX509CertificatePem } is compatible with this.

        Some important notes:

        1. MongoDB **requires** that this username differ from the MongoDB server certificate
           in at least one of: Organization (O), Organizational Unit (OU), or Domain Component (DC).
           See: https://docs.mongodb.com/manual/tutorial/configure-x509-client-authentication/
        2. The client certificate must be signed by the same Certificate Authority (CA) as the
           server certificate that is being used by the MongoDB application.
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def roles(self) -> builtins.str:
        '''JSON-encoded string with the roles this user should be given.'''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbX509User(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.MountPermissions")
class MountPermissions(enum.Enum):
    '''Permission mode under which the filesystem is mounted.'''

    READONLY = "READONLY"
    '''Mount the filesystem as read-only.'''
    READWRITE = "READWRITE"
    '''Mount the filesystem as read-write.'''


@jsii.implements(IMountableLinuxFilesystem)
class MountableBlockVolume(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.MountableBlockVolume",
):
    '''This class encapsulates scripting that can be used by an instance to mount, format, and resize an Amazon Elastic Block Store (EBS) Volume to itself when it is launched.

    The scripting is added to
    the instance's UserData to be run when the instance is first launched.

    The script that is employed by this class will:

    1. Attach the volume to this instance if it is not already attached;
    2. Format the block volume to the filesystem format that's passed as an argument to this script but,
       **ONLY IF** the filesystem has no current format;
    3. Mount the volume to the given mount point with the given mount options; and
    4. Resize the filesystem on the volume if the volume is larger than the formatted filesystem size.

    Note: This does **NOT** support multiple partitions on the EBS Volume; the script will exit with a failure code
    when it detects multiple partitions on the device. It is expected that the whole block device is a single partition.


    Security Considerations

    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.

    :remark:

    If using this script with an instance within an AWS Auto Scaling Group (ASG) and you resize
    the EBS volume, then you can terminate the instance to let the ASG replace the instance and benefit
    from the larger volume size when this script resizes the filesystem on instance launch.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        block_volume: _aws_cdk_aws_ec2_ceddda9d.IVolume,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume_format: typing.Optional[BlockVolumeFormat] = None,
    ) -> None:
        '''
        :param scope: -
        :param block_volume: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Volume.html EBS Block Volume} that will be mounted by this object.
        :param extra_mount_options: Extra mount options that will be added to /etc/fstab for the file system. See the Linux man page for mounting the Volume's file system type for information on available options. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param volume_format: The filesystem format of the block volume. Default: BlockVolumeFormat.XFS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074d44aba8b2ab8d183862018b28fb57b56393ef0bbaaaa39630b10002a9fd8b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = MountableBlockVolumeProps(
            block_volume=block_volume,
            extra_mount_options=extra_mount_options,
            volume_format=volume_format,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="grantRequiredPermissions")
    def _grant_required_permissions(self, target: "IMountingInstance") -> None:
        '''Grant required permissions to the target.

        The mounting script requires two permissions:

        1. Permission to describe the volume
        2. Permission to attach the volume

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4e1bfe44b11dcc3b16dc35a7f3084253f43f4beffbdb6bf1bfca1fe91f2583)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "grantRequiredPermissions", [target]))

    @jsii.member(jsii_name="mountAssetSingleton")
    def _mount_asset_singleton(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''Fetch the Asset singleton for the Volume mounting scripts, or generate it if needed.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4074e7c1ed2438417f56776476b39f579267f4a720433047cd008f568537ee87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, jsii.invoke(self, "mountAssetSingleton", [scope]))

    @jsii.member(jsii_name="mountToLinuxInstance")
    def mount_to_linux_instance(
        self,
        target: "IMountingInstance",
        *,
        location: builtins.str,
        permissions: typing.Optional[MountPermissions] = None,
    ) -> None:
        '''Mount the filesystem to the given instance at instance startup.

        This is accomplished by
        adding scripting to the UserData of the instance to mount the filesystem on startup.
        If required, the instance's security group is granted ingress to the filesystem's security
        group on the required ports.

        :param target: -
        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e186a94dece5cabc525b3cc468a0a6c85f7bc5586102580e21f838807afa80)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        mount = LinuxMountPointProps(location=location, permissions=permissions)

        return typing.cast(None, jsii.invoke(self, "mountToLinuxInstance", [target, mount]))

    @jsii.member(jsii_name="usesUserPosixPermissions")
    def uses_user_posix_permissions(self) -> builtins.bool:
        '''Returns whether the mounted file-system evaluates the UID/GID of the system user accessing the file-system.

        Some network file-systems provide features to fix a UID/GID for all access to the mounted file-system and ignore
        the system user accessing the file. If this is the case, an implementing class must indicate this in the return
        value.

        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "usesUserPosixPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "MountableBlockVolumeProps":
        return typing.cast("MountableBlockVolumeProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))


@jsii.data_type(
    jsii_type="aws-rfdk.MountableBlockVolumeProps",
    jsii_struct_bases=[],
    name_mapping={
        "block_volume": "blockVolume",
        "extra_mount_options": "extraMountOptions",
        "volume_format": "volumeFormat",
    },
)
class MountableBlockVolumeProps:
    def __init__(
        self,
        *,
        block_volume: _aws_cdk_aws_ec2_ceddda9d.IVolume,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume_format: typing.Optional[BlockVolumeFormat] = None,
    ) -> None:
        '''Properties that are required to create a {@link MountableBlockVolume}.

        :param block_volume: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Volume.html EBS Block Volume} that will be mounted by this object.
        :param extra_mount_options: Extra mount options that will be added to /etc/fstab for the file system. See the Linux man page for mounting the Volume's file system type for information on available options. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param volume_format: The filesystem format of the block volume. Default: BlockVolumeFormat.XFS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6dfbf49f974d5284b88260ad2587762702803a672d48f7e88ad0ff53e857a06)
            check_type(argname="argument block_volume", value=block_volume, expected_type=type_hints["block_volume"])
            check_type(argname="argument extra_mount_options", value=extra_mount_options, expected_type=type_hints["extra_mount_options"])
            check_type(argname="argument volume_format", value=volume_format, expected_type=type_hints["volume_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "block_volume": block_volume,
        }
        if extra_mount_options is not None:
            self._values["extra_mount_options"] = extra_mount_options
        if volume_format is not None:
            self._values["volume_format"] = volume_format

    @builtins.property
    def block_volume(self) -> _aws_cdk_aws_ec2_ceddda9d.IVolume:
        '''The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Volume.html EBS Block Volume} that will be mounted by this object.'''
        result = self._values.get("block_volume")
        assert result is not None, "Required property 'block_volume' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVolume, result)

    @builtins.property
    def extra_mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Extra mount options that will be added to /etc/fstab for the file system.

        See the Linux man page for mounting the Volume's file system type for information
        on available options.

        The given values will be joined together into a single string by commas.
        ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096'

        :default: No extra options.
        '''
        result = self._values.get("extra_mount_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def volume_format(self) -> typing.Optional[BlockVolumeFormat]:
        '''The filesystem format of the block volume.

        :default: BlockVolumeFormat.XFS

        :remark:

        If the volume is already formatted, but does not match this format then
        the mounting script employed by {@link MountableBlockVolume } will mount the volume as-is
        if it is able. No formatting will be performed.
        '''
        result = self._values.get("volume_format")
        return typing.cast(typing.Optional[BlockVolumeFormat], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MountableBlockVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMountableLinuxFilesystem)
class MountableEfs(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.MountableEfs"):
    '''This class encapsulates scripting that can be used to mount an Amazon Elastic File System onto an instance.

    An optional EFS access point can be specified for mounting the EFS file-system. For more information on using EFS
    Access Points, see https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html. For this to work properly, the
    EFS mount helper is required. The EFS Mount helper comes pre-installed on Amazon Linux 2. For other Linux
    distributions, the host machine must have the Amazon EFS client installed. We advise installing the Amazon EFS Client
    when building your AMI. For instructions on installing the Amazon EFS client for other distributions, see
    https://docs.aws.amazon.com/efs/latest/ug/installing-amazon-efs-utils.html#installing-other-distro.

    NOTE: Without an EFS access point, the file-system is writeable only by the root user.


    Security Considerations

    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        access_point: typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint] = None,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        resolve_mount_target_dns_with_api: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param filesystem: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-efs.FileSystem.html EFS} filesystem that will be mounted by the object.
        :param access_point: An optional access point to use for mounting the file-system. NOTE: Access points are only supported when using the EFS mount helper. The EFS Mount helper comes pre-installed on Amazon Linux 2. For other Linux distributions, you must have the Amazon EFS client installed on your AMI for this to work properly. For instructions on installing the Amazon EFS client for other distributions, see: https://docs.aws.amazon.com/efs/latest/ug/installing-amazon-efs-utils.html#installing-other-distro Default: no access point is used
        :param extra_mount_options: Extra NFSv4 mount options that will be added to /etc/fstab for the file system. See: {@link https://www.man7.org/linux/man-pages//man5/nfs.5.html}. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param resolve_mount_target_dns_with_api: If enabled, RFDK will add user-data to the instances mounting this EFS file-system that obtains the mount target IP address using AWS APIs and writes them to the system's ``/etc/hosts`` file to not require DNS lookups. If mounting EFS from instances in a VPC configured to not use the Amazon-provided DNS Route 53 Resolver server, then the EFS mount targets will not be resolvable using DNS (see https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) and enabling this will work around that issue. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee45726c62fa55071c23f9e714efc4cf7d40ba0700cf2095ff46ec393249f0fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = MountableEfsProps(
            filesystem=filesystem,
            access_point=access_point,
            extra_mount_options=extra_mount_options,
            resolve_mount_target_dns_with_api=resolve_mount_target_dns_with_api,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="mountAssetSingleton")
    def _mount_asset_singleton(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''Fetch the Asset singleton for the EFS mounting scripts, or generate it if needed.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20321acd49c203b04dff2c5d50d1c99d8ae8ee65e8bcb768707fbd5c46d81811)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, jsii.invoke(self, "mountAssetSingleton", [scope]))

    @jsii.member(jsii_name="mountToLinuxInstance")
    def mount_to_linux_instance(
        self,
        target: "IMountingInstance",
        *,
        location: builtins.str,
        permissions: typing.Optional[MountPermissions] = None,
    ) -> None:
        '''Mount the filesystem to the given instance at instance startup.

        This is accomplished by
        adding scripting to the UserData of the instance to mount the filesystem on startup.
        If required, the instance's security group is granted ingress to the filesystem's security
        group on the required ports.

        :param target: -
        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8486b0d887b43a87f64fdbe8a3950fb8879e6d715e694e1da8ef5397b7c8cd29)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        mount = LinuxMountPointProps(location=location, permissions=permissions)

        return typing.cast(None, jsii.invoke(self, "mountToLinuxInstance", [target, mount]))

    @jsii.member(jsii_name="usesUserPosixPermissions")
    def uses_user_posix_permissions(self) -> builtins.bool:
        '''Returns whether the mounted file-system evaluates the UID/GID of the system user accessing the file-system.

        Some network file-systems provide features to fix a UID/GID for all access to the mounted file-system and ignore
        the system user accessing the file. If this is the case, an implementing class must indicate this in the return
        value.

        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "usesUserPosixPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''The underlying EFS filesystem that is mounted.'''
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, jsii.get(self, "fileSystem"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "MountableEfsProps":
        return typing.cast("MountableEfsProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="accessPoint")
    def access_point(self) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint]:
        '''The optional access point used to mount the EFS file-system.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint], jsii.get(self, "accessPoint"))


@jsii.data_type(
    jsii_type="aws-rfdk.MountableEfsProps",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem": "filesystem",
        "access_point": "accessPoint",
        "extra_mount_options": "extraMountOptions",
        "resolve_mount_target_dns_with_api": "resolveMountTargetDnsWithApi",
    },
)
class MountableEfsProps:
    def __init__(
        self,
        *,
        filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        access_point: typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint] = None,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        resolve_mount_target_dns_with_api: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties that are required to create a {@link MountableEfs}.

        :param filesystem: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-efs.FileSystem.html EFS} filesystem that will be mounted by the object.
        :param access_point: An optional access point to use for mounting the file-system. NOTE: Access points are only supported when using the EFS mount helper. The EFS Mount helper comes pre-installed on Amazon Linux 2. For other Linux distributions, you must have the Amazon EFS client installed on your AMI for this to work properly. For instructions on installing the Amazon EFS client for other distributions, see: https://docs.aws.amazon.com/efs/latest/ug/installing-amazon-efs-utils.html#installing-other-distro Default: no access point is used
        :param extra_mount_options: Extra NFSv4 mount options that will be added to /etc/fstab for the file system. See: {@link https://www.man7.org/linux/man-pages//man5/nfs.5.html}. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param resolve_mount_target_dns_with_api: If enabled, RFDK will add user-data to the instances mounting this EFS file-system that obtains the mount target IP address using AWS APIs and writes them to the system's ``/etc/hosts`` file to not require DNS lookups. If mounting EFS from instances in a VPC configured to not use the Amazon-provided DNS Route 53 Resolver server, then the EFS mount targets will not be resolvable using DNS (see https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) and enabling this will work around that issue. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c94c72b7311939c7f317245510f3281104638e4ed3e69220cad9912b1482167)
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument access_point", value=access_point, expected_type=type_hints["access_point"])
            check_type(argname="argument extra_mount_options", value=extra_mount_options, expected_type=type_hints["extra_mount_options"])
            check_type(argname="argument resolve_mount_target_dns_with_api", value=resolve_mount_target_dns_with_api, expected_type=type_hints["resolve_mount_target_dns_with_api"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filesystem": filesystem,
        }
        if access_point is not None:
            self._values["access_point"] = access_point
        if extra_mount_options is not None:
            self._values["extra_mount_options"] = extra_mount_options
        if resolve_mount_target_dns_with_api is not None:
            self._values["resolve_mount_target_dns_with_api"] = resolve_mount_target_dns_with_api

    @builtins.property
    def filesystem(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-efs.FileSystem.html EFS} filesystem that will be mounted by the object.'''
        result = self._values.get("filesystem")
        assert result is not None, "Required property 'filesystem' is missing"
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, result)

    @builtins.property
    def access_point(self) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint]:
        '''An optional access point to use for mounting the file-system.

        NOTE: Access points are only supported when using the EFS mount helper. The EFS Mount helper comes pre-installed on
        Amazon Linux 2. For other Linux distributions, you must have the Amazon EFS client installed on your AMI for this
        to work properly. For instructions on installing the Amazon EFS client for other distributions, see:

        https://docs.aws.amazon.com/efs/latest/ug/installing-amazon-efs-utils.html#installing-other-distro

        :default: no access point is used
        '''
        result = self._values.get("access_point")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint], result)

    @builtins.property
    def extra_mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Extra NFSv4 mount options that will be added to /etc/fstab for the file system. See: {@link https://www.man7.org/linux/man-pages//man5/nfs.5.html}.

        The given values will be joined together into a single string by commas.
        ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096'

        :default: No extra options.
        '''
        result = self._values.get("extra_mount_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resolve_mount_target_dns_with_api(self) -> typing.Optional[builtins.bool]:
        '''If enabled, RFDK will add user-data to the instances mounting this EFS file-system that obtains the mount target IP address using AWS APIs and writes them to the system's ``/etc/hosts`` file to not require DNS lookups.

        If mounting EFS from instances in a VPC configured to not use the Amazon-provided DNS Route 53 Resolver server,
        then the EFS mount targets will not be resolvable using DNS (see
        https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) and enabling this will work around that issue.

        :default: false
        '''
        result = self._values.get("resolve_mount_target_dns_with_api")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MountableEfsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMountableLinuxFilesystem)
class MountableFsxLustre(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.MountableFsxLustre",
):
    '''This class encapsulates scripting that can be used to mount an Amazon FSx for Lustre File System onto an instance.



    Security Considerations

    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        filesystem: _aws_cdk_aws_fsx_ceddda9d.LustreFileSystem,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        fileset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param filesystem: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-fsx.LustreFileSystem.html FSx for Lustre} filesystem that will be mounted by the object.
        :param extra_mount_options: Extra Lustre mount options that will be added to /etc/fstab for the file system. See: {@link http://manpages.ubuntu.com/manpages/precise/man8/mount.lustre.8.html}. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param fileset: The fileset to mount. Default: Mounts the root of the filesystem.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb84dd6da44bca71733340804fb30b66311bca3bf753247564cb3654fa2f459d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = MountableFsxLustreProps(
            filesystem=filesystem,
            extra_mount_options=extra_mount_options,
            fileset=fileset,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="mountAssetSingleton")
    def _mount_asset_singleton(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''Fetch the Asset singleton for the FSx for Lustre mounting scripts, or generate it if needed.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2764abeebcaa56b7da9bdc4fd6402f2515f63a313683a5444b0351e823ba6bec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, jsii.invoke(self, "mountAssetSingleton", [scope]))

    @jsii.member(jsii_name="mountToLinuxInstance")
    def mount_to_linux_instance(
        self,
        target: "IMountingInstance",
        *,
        location: builtins.str,
        permissions: typing.Optional[MountPermissions] = None,
    ) -> None:
        '''Mount the filesystem to the given instance at instance startup.

        This is accomplished by
        adding scripting to the UserData of the instance to mount the filesystem on startup.
        If required, the instance's security group is granted ingress to the filesystem's security
        group on the required ports.

        :param target: -
        :param location: Directory for the mount point.
        :param permissions: File permissions for the mounted filesystem. Default: MountPermissions.READWRITE

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba07043caf53b4d521db3278198d9f606ac396ff613ed8a4c362f31a53934162)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        mount = LinuxMountPointProps(location=location, permissions=permissions)

        return typing.cast(None, jsii.invoke(self, "mountToLinuxInstance", [target, mount]))

    @jsii.member(jsii_name="usesUserPosixPermissions")
    def uses_user_posix_permissions(self) -> builtins.bool:
        '''Returns whether the mounted file-system evaluates the UID/GID of the system user accessing the file-system.

        Some network file-systems provide features to fix a UID/GID for all access to the mounted file-system and ignore
        the system user accessing the file. If this is the case, an implementing class must indicate this in the return
        value.

        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "usesUserPosixPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "MountableFsxLustreProps":
        return typing.cast("MountableFsxLustreProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))


@jsii.data_type(
    jsii_type="aws-rfdk.MountableFsxLustreProps",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem": "filesystem",
        "extra_mount_options": "extraMountOptions",
        "fileset": "fileset",
    },
)
class MountableFsxLustreProps:
    def __init__(
        self,
        *,
        filesystem: _aws_cdk_aws_fsx_ceddda9d.LustreFileSystem,
        extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        fileset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties that are required to create a {@link MountableFsxLustre}.

        :param filesystem: The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-fsx.LustreFileSystem.html FSx for Lustre} filesystem that will be mounted by the object.
        :param extra_mount_options: Extra Lustre mount options that will be added to /etc/fstab for the file system. See: {@link http://manpages.ubuntu.com/manpages/precise/man8/mount.lustre.8.html}. The given values will be joined together into a single string by commas. ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096' Default: No extra options.
        :param fileset: The fileset to mount. Default: Mounts the root of the filesystem.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2040c1feb8267635fcf3aaa1ae40c15b22baf941da809618037281e5769efef)
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument extra_mount_options", value=extra_mount_options, expected_type=type_hints["extra_mount_options"])
            check_type(argname="argument fileset", value=fileset, expected_type=type_hints["fileset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filesystem": filesystem,
        }
        if extra_mount_options is not None:
            self._values["extra_mount_options"] = extra_mount_options
        if fileset is not None:
            self._values["fileset"] = fileset

    @builtins.property
    def filesystem(self) -> _aws_cdk_aws_fsx_ceddda9d.LustreFileSystem:
        '''The {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-fsx.LustreFileSystem.html FSx for Lustre} filesystem that will be mounted by the object.'''
        result = self._values.get("filesystem")
        assert result is not None, "Required property 'filesystem' is missing"
        return typing.cast(_aws_cdk_aws_fsx_ceddda9d.LustreFileSystem, result)

    @builtins.property
    def extra_mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Extra Lustre mount options that will be added to /etc/fstab for the file system. See: {@link http://manpages.ubuntu.com/manpages/precise/man8/mount.lustre.8.html}.

        The given values will be joined together into a single string by commas.
        ex: ['soft', 'rsize=4096'] will become 'soft,rsize=4096'

        :default: No extra options.
        '''
        result = self._values.get("extra_mount_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fileset(self) -> typing.Optional[builtins.str]:
        '''The fileset to mount.

        :default: Mounts the root of the filesystem.

        :see: https://docs.aws.amazon.com/fsx/latest/LustreGuide/mounting-from-fileset.html
        '''
        result = self._values.get("fileset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MountableFsxLustreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PadEfsStorage(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.PadEfsStorage",
):
    '''This construct provides a mechanism that adds 1GB-sized files containing only zero-bytes to an Amazon EFS filesystem through a given Access Point to that filesystem.

    This is being
    provided to give you a way to increase the baseline throughput of an Amazon EFS filesystem
    that has been deployed in bursting throughput mode (see: https://docs.aws.amazon.com/efs/latest/ug/performance.html#throughput-modes).
    This is most useful for your Amazon EFS filesystems that contain a very small amount of data and
    have a baseline throughput that exceeds the throughput provided by the size of the filesystem.

    When deployed in bursting throughput mode, an Amazon EFS filesystem provides you with a baseline
    throughput that is proportional to the amount of data stored in that filesystem. However, usage
    of that filesystem is allowed to burst above that throughput; doing so consumes burst credits that
    are associated with the filesystem. When all burst credits have been expended, then your filesystem
    is no longer allowed to burst throughput and you will be limited in throughput to the greater of 1MiB/s
    or the throughput dictated by the amount of data stored in your filesystem; the filesystem will be able
    to burst again if it is able to accrue burst credits by staying below its baseline throughput for a time.

    Customers that deploy the Deadline Repository Filesystem on an Amazon EFS filesystem may find that
    the filesystem does not contain sufficient data to meet the throughput needs of Deadline; evidenced by
    a downward trend in EFS bursting credits over time. When bursting credits are expended, then the render
    farm may begin to exhibit failure mode behaviors such as the RenderQueue dropping or refusing connections,
    or becoming unresponsive.

    If you find that your Amazon EFS is depleting its burst credits and would like to increase the
    amount of padding that has been added to it then you can either:

    - Modify the value of the desired padding property of this construct and redeploy your infrastructure
      to force an update; or
    - Manually invoke the AWS Step Function that has been created by this construct by finding it
      in your AWS Console (its name will be prefixed with "StateMachine"), and
      then start an execution of the state machine with the following JSON document as input:
      { "desiredPadding":  }

    Warning: The implementation of this construct creates and starts an AWS Step Function to add the files
    to the filesystem. The execution of this Step Function occurs asynchronously from your deployment. We recommend
    verifying that the step function completed successfully via your Step Functions console.


    Resources Deployed

    - Two AWS Lambda Functions, with roles, with full access to the given EFS Access Point.
    - An Elastic Network Interface (ENI) for each Lambda Function in each of the selected VPC Subnets, so
      that the Lambda Functions can connect to the given EFS Access Point.
    - An AWS Step Function to coordinate execution of the two Lambda Functions.
    - Security Groups for each AWS Lambda Function.
    - A CloudFormation custom resource that executes StepFunctions.startExecution on the Step Function
      whenever the stack containing this construct is created or updated.



    Security Considerations

    - The AWS Lambdas that are deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by these Lambdas.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - By default, the network interfaces created by this construct's AWS Lambda Functions have Security Groups
      that restrict egress access from the Lambda Function into your VPC such that the Lambda Functions can
      access only the given EFS Access Point.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_point: _aws_cdk_aws_efs_ceddda9d.IAccessPoint,
        desired_padding: _aws_cdk_ceddda9d.Size,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_point: Amazon EFS Access Point into which the filesystem padding files will be added. Files will be added/removed from the root directory of the given access point. We strongly recommend that you provide an access point that is for a dedicated padding-files directory in your EFS filesystem, rather than the root directory or some other in-use directory of the filesystem.
        :param desired_padding: The desired total size, in GiB, of files stored in the access point directory.
        :param vpc: VPC in which the given access point is deployed.
        :param security_group: Security group for the AWS Lambdas created by this construct. Default: Security group with no egress or ingress will be automatically created for each Lambda.
        :param vpc_subnets: PadEfsStorage deploys AWS Lambda Functions that need to contact your Amazon EFS mount target(s). To do this, AWS Lambda creates network interfaces in these given subnets in your VPC. These can be any subnet(s) in your VPC that can route traffic to the EFS mount target(s). Default: All private subnets
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2806f9d6f1472412d837a5da5c0f8658de013818d7f1b2ff37580af0af60dae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PadEfsStorageProps(
            access_point=access_point,
            desired_padding=desired_padding,
            vpc=vpc,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-rfdk.PadEfsStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_point": "accessPoint",
        "desired_padding": "desiredPadding",
        "vpc": "vpc",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class PadEfsStorageProps:
    def __init__(
        self,
        *,
        access_point: _aws_cdk_aws_efs_ceddda9d.IAccessPoint,
        desired_padding: _aws_cdk_ceddda9d.Size,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Input properties for PadEfsStorage.

        :param access_point: Amazon EFS Access Point into which the filesystem padding files will be added. Files will be added/removed from the root directory of the given access point. We strongly recommend that you provide an access point that is for a dedicated padding-files directory in your EFS filesystem, rather than the root directory or some other in-use directory of the filesystem.
        :param desired_padding: The desired total size, in GiB, of files stored in the access point directory.
        :param vpc: VPC in which the given access point is deployed.
        :param security_group: Security group for the AWS Lambdas created by this construct. Default: Security group with no egress or ingress will be automatically created for each Lambda.
        :param vpc_subnets: PadEfsStorage deploys AWS Lambda Functions that need to contact your Amazon EFS mount target(s). To do this, AWS Lambda creates network interfaces in these given subnets in your VPC. These can be any subnet(s) in your VPC that can route traffic to the EFS mount target(s). Default: All private subnets
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b240cf7ea3ae2d2c08a61f2b824f60dfc1c1b976881c247fd6333f222bfb2d1)
            check_type(argname="argument access_point", value=access_point, expected_type=type_hints["access_point"])
            check_type(argname="argument desired_padding", value=desired_padding, expected_type=type_hints["desired_padding"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_point": access_point,
            "desired_padding": desired_padding,
            "vpc": vpc,
        }
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def access_point(self) -> _aws_cdk_aws_efs_ceddda9d.IAccessPoint:
        '''Amazon EFS Access Point into which the filesystem padding files will be added.

        Files will
        be added/removed from the root directory of the given access point.
        We strongly recommend that you provide an access point that is for a dedicated padding-files
        directory in your EFS filesystem, rather than the root directory or some other in-use directory
        of the filesystem.
        '''
        result = self._values.get("access_point")
        assert result is not None, "Required property 'access_point' is missing"
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IAccessPoint, result)

    @builtins.property
    def desired_padding(self) -> _aws_cdk_ceddda9d.Size:
        '''The desired total size, in GiB, of files stored in the access point directory.'''
        result = self._values.get("desired_padding")
        assert result is not None, "Required property 'desired_padding' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC in which the given access point is deployed.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security group for the AWS Lambdas created by this construct.

        :default: Security group with no egress or ingress will be automatically created for each Lambda.
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''PadEfsStorage deploys AWS Lambda Functions that need to contact your Amazon EFS mount target(s).

        To do this, AWS Lambda creates network interfaces in these given subnets in your VPC.
        These can be any subnet(s) in your VPC that can route traffic to the EFS mount target(s).

        :default: All private subnets
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PadEfsStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScriptAsset(
    _aws_cdk_aws_s3_assets_ceddda9d.Asset,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.ScriptAsset",
):
    '''An S3 asset that contains a shell script intended to be executed through instance user data.

    This is used by other constructs to generalize the concept of a script
    (bash or powershell) that executes on an instance.
    It provides a wrapper around the CDK’s S3 Asset construct
    ( https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3-assets.Asset.html )

    The script asset is placed into and fetched from the CDK bootstrap S3 bucket.


    Resources Deployed

    - An Asset which is uploaded to the bootstrap S3 bucket.



    Security Considerations

    - Using this construct on an instance will result in that instance dynamically downloading and running scripts
      from your CDK bootstrap bucket when that instance is launched. You must limit write access to your CDK bootstrap
      bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly recommend that
      you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS CloudTrail on your
      account to assist in post-incident analysis of compromised production environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        deploy_time: typing.Optional[builtins.bool] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fae01edbd9cc35ef40f65e416f67d058eecaf16813f35193baac14b4d7d682a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScriptAssetProps(
            path=path,
            deploy_time=deploy_time,
            readers=readers,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPathConvention")
    @builtins.classmethod
    def from_path_convention(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        base_name: builtins.str,
        os_type: _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType,
        root_dir: builtins.str,
    ) -> "ScriptAsset":
        '''Returns a {@link ScriptAsset} instance by computing the path to the script using RFDK's script directory structure convention.

        By convention, scripts are kept in a ``scripts`` directory in each ``aws-rfdk/*`` package. The scripts are organized
        based on target shell (and implicitly target operating system). The directory structure looks like::

           scripts/
             bash/
               script-one.sh
               script-two.sh
             powershell
               script-one.ps1
               script-one.ps1

        :param scope: The scope for the created {@link ScriptAsset}.
        :param id: The construct id for the created {@link ScriptAsset}.
        :param base_name: The basename of the script without the file's extension.
        :param os_type: The operating system that the script is intended for.
        :param root_dir: The root directory that contains the script.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5e0e51e5f067fbddb30ac61d5c6b41efd30fdb5b397817f7f205de8ed20f80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        script_params = ConventionalScriptPathParams(
            base_name=base_name, os_type=os_type, root_dir=root_dir
        )

        return typing.cast("ScriptAsset", jsii.sinvoke(cls, "fromPathConvention", [scope, id, script_params]))

    @jsii.member(jsii_name="executeOn")
    def execute_on(
        self,
        *,
        host: IScriptHost,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Adds commands to the {@link IScriptHost} to download and execute the ScriptAsset.

        :param host: The host to run the script against. For example, instances of: - {@link @aws-cdk/aws-ec2#Instance} - {@link @aws-cdk/aws-autoscaling#AutoScalingGroup} can be used.
        :param args: Command-line arguments to invoke the script with. If supplied, these arguments are simply concatenated with a space character between. No shell escaping is done. Default: No command-line arguments
        '''
        props = ExecuteScriptProps(host=host, args=args)

        return typing.cast(None, jsii.invoke(self, "executeOn", [props]))


@jsii.data_type(
    jsii_type="aws-rfdk.ScriptAssetProps",
    jsii_struct_bases=[_aws_cdk_aws_s3_assets_ceddda9d.AssetProps],
    name_mapping={
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "bundling": "bundling",
        "exclude": "exclude",
        "follow_symlinks": "followSymlinks",
        "ignore_mode": "ignoreMode",
        "deploy_time": "deployTime",
        "readers": "readers",
        "path": "path",
    },
)
class ScriptAssetProps(_aws_cdk_aws_s3_assets_ceddda9d.AssetProps):
    def __init__(
        self,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
        deploy_time: typing.Optional[builtins.bool] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        path: builtins.str,
    ) -> None:
        '''Properties for constructing a {@link ScriptAsset}.

        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        '''
        if isinstance(bundling, dict):
            bundling = _aws_cdk_ceddda9d.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbfbab47c8dce2a4d14e3076c2ec8b5ed3a0e6e47ad3d6828114449f40e7c91)
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument deploy_time", value=deploy_time, expected_type=type_hints["deploy_time"])
            check_type(argname="argument readers", value=readers, expected_type=type_hints["readers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None:
            self._values["bundling"] = bundling
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if deploy_time is not None:
            self._values["deploy_time"] = deploy_time
        if readers is not None:
            self._values["readers"] = readers

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - based on ``assetHashType``
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_aws_cdk_ceddda9d.AssetHashType]:
        '''Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
        explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AssetHashType], result)

    @builtins.property
    def bundling(self) -> typing.Optional[_aws_cdk_ceddda9d.BundlingOptions]:
        '''Bundle the asset by executing a command in a Docker container or a custom bundling provider.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
        archived into a .zip file and uploaded to S3 otherwise
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.BundlingOptions], result)

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''File paths matching the patterns will be excluded.

        See ``ignoreMode`` to set the matching behavior.
        Has no effect on Assets bundled using the ``bundling`` property.

        :default: - nothing is excluded
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_symlinks(self) -> typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_ceddda9d.IgnoreMode]:
        '''The ignore behavior to use for ``exclude`` patterns.

        :default: IgnoreMode.GLOB
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IgnoreMode], result)

    @builtins.property
    def deploy_time(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the asset needs to exist beyond deployment time;

        i.e.
        are copied over to a different location and not needed afterwards.
        Setting this property to true has an impact on the lifecycle of the asset,
        because we will assume that it is safe to delete after the CloudFormation
        deployment succeeds.

        For example, Lambda Function assets are copied over to Lambda during
        deployment. Therefore, it is not necessary to store the asset in S3, so
        we consider those deployTime assets.

        :default: false
        '''
        result = self._values.get("deploy_time")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IGrantable]]:
        '''A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        :default: - No principals that can read file asset.
        '''
        result = self._values.get("readers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IGrantable]], result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The disk location of the asset.

        The path should refer to one of the following:

        - A regular file or a .zip file, in which case the file will be uploaded as-is to S3.
        - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScriptAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SessionManagerHelper(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.SessionManagerHelper",
):
    '''This is a helper class meant to make it easier to use the AWS Systems Manager Session Manager with any EC2 Instances or AutoScalingGroups.

    Once enabled, the Session Manager can be used to
    connect to an EC2 Instance through the AWS Console and open a shell session in the browser.

    Note that in order for the Session Manager to work, you will need an AMI that has the SSM-Agent
    installed and set to run at startup. The Amazon Linux 2 and Amazon provided Windows Server AMI's
    have this configured by default.

    More details about the AWS Systems Manager Session Manager can be found here:
    https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="grantPermissionsTo")
    @builtins.classmethod
    def grant_permissions_to(
        cls,
        grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''Grants the permissions required to enable Session Manager for the provided IGrantable.

        :param grantable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d44616e89c67dda85e3442c73a9f1635be87fb41e10aefb9cc7966da9e554eb)
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast(None, jsii.sinvoke(cls, "grantPermissionsTo", [grantable]))


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable, _aws_cdk_aws_iam_ceddda9d.IGrantable)
class StaticPrivateIpServer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.StaticPrivateIpServer",
):
    '''This construct provides a single instance, provided by an Auto Scaling Group (ASG), that has an attached Elastic Network Interface (ENI) that is providing a private ip address.

    This ENI is automatically re-attached to the instance if the instance is replaced
    by the ASG.

    The ENI provides an unchanging private IP address that can always be used to connect
    to the instance regardless of how many times the instance has been replaced. Furthermore,
    the ENI has a MAC address that remains unchanged unless the ENI is destroyed.

    Essentially, this provides an instance with an unchanging private IP address that will
    automatically recover from termination. This instance is suitable for use as an application server,
    such as a license server, that must always be reachable by the same IP address.


    Resources Deployed

    - Auto Scaling Group (ASG) with min & max capacity of 1 instance.
    - Elastic Network Interface (ENI).
    - Security Group for the ASG.
    - Instance Role and corresponding IAM Policy.
    - SNS Topic & Role for instance-launch lifecycle events -- max one of each per stack.
    - Lambda function, with role, to attach the ENI in response to instance-launch lifecycle events -- max one per stack.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The AWS Lambda that is deployed through this construct has broad IAM permissions to attach any Elastic
      Network Interface (ENI) to any instance. You should not grant any additional actors/principals the ability
      to modify or execute this Lambda.
    - The SNS Topic that is deployed through this construct controls the execution of the Lambda discussed above.
      Principals that can publish messages to this SNS Topic will be able to trigger the Lambda to run. You should
      not allow any additional principals to publish messages to this SNS Topic.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        key_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_type: The type of instance to launch.
        :param machine_image: The AMI to launch the instance with.
        :param vpc: VPC in which to launch the instance.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: Uses the block device mapping of the AMI.
        :param key_name: Name of the EC2 SSH keypair to grant access to the instance. Default: No SSH access will be possible.
        :param private_ip_address: The specific private IP address to assign to the Elastic Network Interface of this instance. Default: An IP address is randomly assigned from the subnet.
        :param resource_signal_timeout: The length of time to wait for the instance to signal successful deployment during the initial deployment, or update, of your stack. The maximum value is 12 hours. Default: The deployment does not require a success signal from the instance.
        :param role: An IAM role to associate with the instance profile that is assigned to this instance. The role must be assumable by the service principal ``ec2.amazonaws.com`` Default: A role will automatically be created, it can be accessed via the ``role`` property.
        :param security_group: The security group to assign to this instance. Default: A new security group is created for this instance.
        :param user_data: Specific UserData to use. UserData is a script that is run automatically by the instance the very first time that a new instance is started. The UserData may be mutated after creation. Default: A UserData that is appropriate to the {@link machineImage }'s operating system is created.
        :param vpc_subnets: Where to place the instance within the VPC. Default: The instance is placed within a Private subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c191460db188d618ceebc2a95bc294d5896fac791b3cac4b2937730460bc3540)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticPrivateIpServerProps(
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=vpc,
            block_devices=block_devices,
            key_name=key_name,
            private_ip_address=private_ip_address,
            resource_signal_timeout=resource_signal_timeout,
            role=role,
            security_group=security_group,
            user_data=user_data,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="attachEniLifecyleTarget")
    def _attach_eni_lifecyle_target(
        self,
        eni: _aws_cdk_aws_ec2_ceddda9d.CfnNetworkInterface,
    ) -> None:
        '''Set up an instance launch lifecycle action that will attach the eni to the single instance in this construct's AutoScalingGroup when a new instance is launched.

        :param eni: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109f1d21e771bc801cd52c072416b3ae5d48df94de67d735da4ed0dd3d4c536a)
            check_type(argname="argument eni", value=eni, expected_type=type_hints["eni"])
        return typing.cast(None, jsii.invoke(self, "attachEniLifecyleTarget", [eni]))

    @jsii.member(jsii_name="setupLifecycleEventHandlerFunction")
    def _setup_lifecycle_event_handler_function(
        self,
    ) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''Create, or fetch, the lambda function that will process instance-start lifecycle events from this construct.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.invoke(self, "setupLifecycleEventHandlerFunction", []))

    @jsii.member(jsii_name="setupLifecycleNotificationTopic")
    def _setup_lifecycle_notification_topic(
        self,
        lambda_handler: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''Create, or fetch, an SNS Topic to which we'll direct the ASG's instance-start lifecycle hook events.

        Also creates, or fetches,
        the accompanying role that allows the lifecycle events to be published to the SNS Topic.

        :param lambda_handler: The lambda singleton that will be processing the lifecycle events.

        :return: : Topic, role: Role }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c35fbde32de081eaaec85a85f4ee239ae4391520b3e2b2c91676a1f6618287)
            check_type(argname="argument lambda_handler", value=lambda_handler, expected_type=type_hints["lambda_handler"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "setupLifecycleNotificationTopic", [lambda_handler]))

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        '''The Auto Scaling Group that contains the instance this construct creates.'''
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "autoscalingGroup"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Allows for providing security group connections to/from this instance.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permission to.

        Granting permissions to this principal will grant
        those permissions to the instance role.
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType:
        '''The type of operating system that the instance is running.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.OperatingSystemType, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        '''The Private IP address that has been assigned to the ENI.'''
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The IAM role that is assumed by the instance.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''The UserData for this instance.

        UserData is a script that is run automatically by the instance the very first time that a new instance is started.
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.get(self, "userData"))


@jsii.data_type(
    jsii_type="aws-rfdk.StaticPrivateIpServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "vpc": "vpc",
        "block_devices": "blockDevices",
        "key_name": "keyName",
        "private_ip_address": "privateIpAddress",
        "resource_signal_timeout": "resourceSignalTimeout",
        "role": "role",
        "security_group": "securityGroup",
        "user_data": "userData",
        "vpc_subnets": "vpcSubnets",
    },
)
class StaticPrivateIpServerProps:
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        key_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Required and optional properties that define the construction of a {@link StaticPrivateIpServer}.

        :param instance_type: The type of instance to launch.
        :param machine_image: The AMI to launch the instance with.
        :param vpc: VPC in which to launch the instance.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: Uses the block device mapping of the AMI.
        :param key_name: Name of the EC2 SSH keypair to grant access to the instance. Default: No SSH access will be possible.
        :param private_ip_address: The specific private IP address to assign to the Elastic Network Interface of this instance. Default: An IP address is randomly assigned from the subnet.
        :param resource_signal_timeout: The length of time to wait for the instance to signal successful deployment during the initial deployment, or update, of your stack. The maximum value is 12 hours. Default: The deployment does not require a success signal from the instance.
        :param role: An IAM role to associate with the instance profile that is assigned to this instance. The role must be assumable by the service principal ``ec2.amazonaws.com`` Default: A role will automatically be created, it can be accessed via the ``role`` property.
        :param security_group: The security group to assign to this instance. Default: A new security group is created for this instance.
        :param user_data: Specific UserData to use. UserData is a script that is run automatically by the instance the very first time that a new instance is started. The UserData may be mutated after creation. Default: A UserData that is appropriate to the {@link machineImage }'s operating system is created.
        :param vpc_subnets: Where to place the instance within the VPC. Default: The instance is placed within a Private subnet.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710d0b8731d3712c95c2821eda28e8c1aa851651ab86c17a4443099a11e2b48a)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument resource_signal_timeout", value=resource_signal_timeout, expected_type=type_hints["resource_signal_timeout"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "machine_image": machine_image,
            "vpc": vpc,
        }
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if key_name is not None:
            self._values["key_name"] = key_name
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if resource_signal_timeout is not None:
            self._values["resource_signal_timeout"] = resource_signal_timeout
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''The type of instance to launch.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def machine_image(self) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''The AMI to launch the instance with.'''
        result = self._values.get("machine_image")
        assert result is not None, "Required property 'machine_image' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC in which to launch the instance.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]]:
        '''Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched.

        :default: Uses the block device mapping of the AMI.
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of the EC2 SSH keypair to grant access to the instance.

        :default: No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''The specific private IP address to assign to the Elastic Network Interface of this instance.

        :default: An IP address is randomly assigned from the subnet.
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time to wait for the instance to signal successful deployment during the initial deployment, or update, of your stack.

        The maximum value is 12 hours.

        :default: The deployment does not require a success signal from the instance.
        '''
        result = self._values.get("resource_signal_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile that is assigned to this instance.

        The role must be assumable by the service principal ``ec2.amazonaws.com``

        :default: A role will automatically be created, it can be accessed via the ``role`` property.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group to assign to this instance.

        :default: A new security group is created for this instance.
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''Specific UserData to use.

        UserData is a script that is run automatically by the instance the very first time that a new instance is started.

        The UserData may be mutated after creation.

        :default: A UserData that is appropriate to the {@link machineImage }'s operating system is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the instance within the VPC.

        :default: The instance is placed within a Private subnet.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticPrivateIpServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.TimeZone")
class TimeZone(enum.Enum):
    '''Enum to describe the time zone property.'''

    LOCAL = "LOCAL"
    '''The Local time zone.'''
    UTC = "UTC"
    '''The UTC time zone.'''


@jsii.implements(IX509CertificatePem)
class X509CertificatePem(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.X509CertificatePem",
):
    '''A Construct that uses a Lambda to generate an X.509 certificate and then saves the certificate's components into Secrets. On an update, if any properties of the construct are changed, then a new certificate will be generated. When the Stack is destroyed or the Construct is removed, the Secrets will all be deleted. An X.509 certificate is comprised of the certificate, a certificate chain with the chain of signing certificates (if any), and a private key that is password protected by a randomly generated passphrase.

    Cost:
    The cost of four AWS SecretsManager Secrets in the deployed region.
    The other resources created by this construct have negligible ongoing costs.

    architecture diagram


    Resources Deployed

    - DynamoDB Table - Used for tracking resources created by the Custom Resource.
    - Secrets - 4 in total, for the certificate, it's private key, the passphrase to the key, and the cert chain.
    - Lambda Function, with role - Used to create/update/delete the Custom Resource



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - Access to the AWS SecretsManager Secrets that are created by this construct should be tightly restricted
      to only the principal(s) that require access.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subject: typing.Union[DistinguishedName, typing.Dict[builtins.str, typing.Any]],
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        signing_certificate: typing.Optional["X509CertificatePem"] = None,
        valid_for: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subject: The subject, or identity, for the generated certificate.
        :param encryption_key: If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct. [disable-awslint:ref-via-interface] Default: : Uses the account's default CMK (the one named aws/secretsmanager). If a AWS KMS CMK with that name doesn't yet exist, then Secrets Manager creates it for you automatically the first time it needs to encrypt a version's SecretString or SecretBinary fields.
        :param signing_certificate: If provided, then use this certificate to sign the generated certificate forming a chain of trust. Default: : None. The generated certificate will be self-signed
        :param valid_for: The number of days that the generated certificate will be valid for. Default: 1095 days (3 years)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ddc6d885f3912b4be7e4e33c666b507c58a702408d7f47f58cb20df0adf34a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = X509CertificatePemProps(
            subject=subject,
            encryption_key=encryption_key,
            signing_certificate=signing_certificate,
            valid_for=valid_for,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantCertRead")
    def grant_cert_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions for the certificate.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7859d86c362e46d13274f9a0903645ed079287999aee58341a6d3e0bb81ff9d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantCertRead", [grantee]))

    @jsii.member(jsii_name="grantFullRead")
    def grant_full_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions for the certificate, key, and passphrase.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb5ea571776e0d5743b2950f3b232f40d852563f7e8844e1240403223acc03f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantFullRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The public certificate chain for this X.509 Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the chain is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The private key for this X509Certificate encoded in {@link https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail PEM format}. The text of the key is stored in the 'SecretString' of the given secret. To extract the public certificate simply copy the contents of the SecretString to a file.

        Note that the private key is encrypted. The passphrase is stored in the the passphrase Secret.

        If you need to decrypt the private key into an unencrypted form, then you can:
        0. Caution. Decrypting a private key adds a security risk by making it easier to obtain your private key.

        1. Copy the contents of the Secret to a file called 'encrypted.key'
        2. Run: openssl rsa -in encrypted.key -out decrypted.key
        3. Enter the passphrase at the prompt
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the private key is in the 'SecretString' of this secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "passphrase"))

    @builtins.property
    @jsii.member(jsii_name="certChain")
    def cert_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A Secret that contains the chain of Certificates used to sign this Certificate.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "certChain"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def _database(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "database"))

    @_database.setter
    def _database(self, value: _aws_cdk_aws_dynamodb_ceddda9d.Table) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327ebc14939e1e1e9c45e87054d12059a540ed483e0235a96d578a142d46e341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFunc")
    def _lambda_func(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunc"))

    @_lambda_func.setter
    def _lambda_func(self, value: _aws_cdk_aws_lambda_ceddda9d.Function) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820d3c8e6698d22b77be9ff23fa748243ef069db8ff54c3f1b11083e8a1d3510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uniqueTag")
    def _unique_tag(self) -> _aws_cdk_ceddda9d.Tag:
        return typing.cast(_aws_cdk_ceddda9d.Tag, jsii.get(self, "uniqueTag"))

    @_unique_tag.setter
    def _unique_tag(self, value: _aws_cdk_ceddda9d.Tag) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd288d91e62695bff878cf40834e780e781bf59ff8469237913959db4dc8488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueTag", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-rfdk.X509CertificatePemProps",
    jsii_struct_bases=[],
    name_mapping={
        "subject": "subject",
        "encryption_key": "encryptionKey",
        "signing_certificate": "signingCertificate",
        "valid_for": "validFor",
    },
)
class X509CertificatePemProps:
    def __init__(
        self,
        *,
        subject: typing.Union[DistinguishedName, typing.Dict[builtins.str, typing.Any]],
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        signing_certificate: typing.Optional[X509CertificatePem] = None,
        valid_for: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for generating an X.509 certificate.

        :param subject: The subject, or identity, for the generated certificate.
        :param encryption_key: If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct. [disable-awslint:ref-via-interface] Default: : Uses the account's default CMK (the one named aws/secretsmanager). If a AWS KMS CMK with that name doesn't yet exist, then Secrets Manager creates it for you automatically the first time it needs to encrypt a version's SecretString or SecretBinary fields.
        :param signing_certificate: If provided, then use this certificate to sign the generated certificate forming a chain of trust. Default: : None. The generated certificate will be self-signed
        :param valid_for: The number of days that the generated certificate will be valid for. Default: 1095 days (3 years)
        '''
        if isinstance(subject, dict):
            subject = DistinguishedName(**subject)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2683acb2b44b2891288efdf84eac6ea342dfd7823c1e8f05a14579469ca71e5)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument signing_certificate", value=signing_certificate, expected_type=type_hints["signing_certificate"])
            check_type(argname="argument valid_for", value=valid_for, expected_type=type_hints["valid_for"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if signing_certificate is not None:
            self._values["signing_certificate"] = signing_certificate
        if valid_for is not None:
            self._values["valid_for"] = valid_for

    @builtins.property
    def subject(self) -> DistinguishedName:
        '''The subject, or identity, for the generated certificate.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(DistinguishedName, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct.

        [disable-awslint:ref-via-interface]

        :default:

        : Uses the account's default CMK (the one named aws/secretsmanager). If a AWS KMS CMK with that name
        doesn't yet exist, then Secrets Manager creates it for you automatically the first time it needs to encrypt a
        version's SecretString or SecretBinary fields.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def signing_certificate(self) -> typing.Optional[X509CertificatePem]:
        '''If provided, then use this certificate to sign the generated certificate forming a chain of trust.

        :default: : None. The generated certificate will be self-signed
        '''
        result = self._values.get("signing_certificate")
        return typing.cast(typing.Optional[X509CertificatePem], result)

    @builtins.property
    def valid_for(self) -> typing.Optional[jsii.Number]:
        '''The number of days that the generated certificate will be valid for.

        :default: 1095 days (3 years)
        '''
        result = self._values.get("valid_for")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "X509CertificatePemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IX509CertificatePkcs12)
class X509CertificatePkcs12(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.X509CertificatePkcs12",
):
    '''This Construct will generate a PKCS #12 file from an X.509 certificate in PEM format. The PEM certificate must be provided through an instance of the X509CertificatePem Construct. A Lambda Function is used to do the conversion and the result is stored in a Secret. The PKCS #12 file is password protected with a passphrase that is randomly generated and stored in a Secret.

    architecture diagram


    Resources Deployed

    - DynamoDB Table - Used for tracking resources created by the CustomResource.
    - Secrets - 2 in total, The binary of the PKCS #12 certificate and its passphrase.
    - Lambda Function, with role - Used to create/update/delete the CustomResource.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - Access to the AWS SecretsManager Secrets that are created by this construct should be tightly restricted
      to only the principal(s) that require access.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_certificate: X509CertificatePem,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_certificate: The source PEM certificiate for the PKCS #12 file.
        :param encryption_key: If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct. [disable-awslint:ref-via-interface] Default: : None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c109807fb76f18601699009346b8753aa790c458d4c7a97598fbd323392426)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = X509CertificatePkcs12Props(
            source_certificate=source_certificate, encryption_key=encryption_key
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The PKCS #12 data is stored in the 'SecretBinary' of this Secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The encryption passphrase for the private key is in the 'SecretString' of this secret.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "passphrase"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def _database(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "database"))

    @_database.setter
    def _database(self, value: _aws_cdk_aws_dynamodb_ceddda9d.Table) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4057af8359aaf7ab10e4fc229079acf5d97ba3741a64214032d7711a67575b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFunc")
    def _lambda_func(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunc"))

    @_lambda_func.setter
    def _lambda_func(self, value: _aws_cdk_aws_lambda_ceddda9d.Function) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7672fe77b797243d061153110a4106da10d5cf97b9aa7b775717a9d67127f2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uniqueTag")
    def _unique_tag(self) -> _aws_cdk_ceddda9d.Tag:
        return typing.cast(_aws_cdk_ceddda9d.Tag, jsii.get(self, "uniqueTag"))

    @_unique_tag.setter
    def _unique_tag(self, value: _aws_cdk_ceddda9d.Tag) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c70764d051ccabc636a8ed820262d61741729d1fe60cdef2f565fb42f312679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueTag", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-rfdk.X509CertificatePkcs12Props",
    jsii_struct_bases=[],
    name_mapping={
        "source_certificate": "sourceCertificate",
        "encryption_key": "encryptionKey",
    },
)
class X509CertificatePkcs12Props:
    def __init__(
        self,
        *,
        source_certificate: X509CertificatePem,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''Construct properties for generating a PKCS #12 file from an X.509 certificate.

        :param source_certificate: The source PEM certificiate for the PKCS #12 file.
        :param encryption_key: If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct. [disable-awslint:ref-via-interface] Default: : None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e0ff1d9c7da9f35e938333e84ca7d6df43be25aec5d4579a47610bfda4277f)
            check_type(argname="argument source_certificate", value=source_certificate, expected_type=type_hints["source_certificate"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_certificate": source_certificate,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def source_certificate(self) -> X509CertificatePem:
        '''The source PEM certificiate for the PKCS #12 file.'''
        result = self._values.get("source_certificate")
        assert result is not None, "Required property 'source_certificate' is missing"
        return typing.cast(X509CertificatePem, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''If provided, then this KMS is used to secure the cert, key, and passphrase Secrets created by the construct.

        [disable-awslint:ref-via-interface]

        :default: : None
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "X509CertificatePkcs12Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationEndpoint(
    Endpoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.ApplicationEndpoint",
):
    '''An endpoint serving http or https for an application.'''

    def __init__(
        self,
        *,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    ) -> None:
        '''Constructs a {@link ApplicationEndpoint} instance.

        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The application layer protocol of the endpoint. Default: HTTPS
        '''
        props = ApplicationEndpointProps(address=address, port=port, protocol=protocol)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="applicationProtocol")
    def application_protocol(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol:
        '''The http protocol that this web application listens on.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol, jsii.get(self, "applicationProtocol"))


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class ConnectableApplicationEndpoint(
    ApplicationEndpoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.ConnectableApplicationEndpoint",
):
    '''An endpoint serving http or https for an application.'''

    def __init__(
        self,
        *,
        connections: _aws_cdk_aws_ec2_ceddda9d.Connections,
        address: builtins.str,
        port: jsii.Number,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    ) -> None:
        '''Constructs a {@link ApplicationEndpoint} instance.

        :param connections: The connection object of the application this endpoint is for.
        :param address: The address (either an IP or hostname) of the endpoint.
        :param port: The port number of the endpoint.
        :param protocol: The application layer protocol of the endpoint. Default: HTTPS
        '''
        props = ConnectableApplicationEndpointProps(
            connections=connections, address=address, port=port, protocol=protocol
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Allows specifying security group connections for the application.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))


@jsii.implements(IHealthMonitor)
class HealthMonitor(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.HealthMonitor",
):
    '''This construct is responsible for the deep health checks of compute instances.

    It also replaces unhealthy instances and suspends unhealthy fleets.
    Although, using this constructs adds up additional costs for monitoring,
    it is highly recommended using this construct to help avoid / minimize runaway costs for compute instances.

    An instance is considered to be unhealthy when:

    1. Deadline client is not installed on it;
    2. Deadline client is installed but not running on it;
    3. RCS is not configured correctly for Deadline client;
    4. it is unable to connect to RCS due to any infrastructure issues;
    5. the health monitor is unable to reach it because of some infrastructure issues.

    A fleet is considered to be unhealthy when:

    1. at least 1 instance is unhealthy for the configured grace period;
    2. a percentage of unhealthy instances in the fleet is above a threshold at any given point of time.

    This internally creates an array of application load balancers and attaches
    the worker-fleet (which internally is implemented as an Auto Scaling Group) to its listeners.
    There is no load-balancing traffic on the load balancers,
    it is only used for health checks.
    Intention is to use the default properties of laod balancer health
    checks which does HTTP pings at frequent intervals to all the
    instances in the fleet and determines its health. If any of the
    instance is found unhealthy, it is replaced. The target group
    also publishes the unhealthy target count metric which is used
    to identify the unhealthy fleet.

    Other than the default instance level protection, it also creates a lambda
    which is responsible to set the fleet size to 0 in the event of a fleet
    being sufficiently unhealthy to warrant termination.
    This lambda is triggered by CloudWatch alarms via SNS (Simple Notification Service).

    architecture diagram


    Resources Deployed

    - Application Load Balancer(s) doing frequent pings to the workers.
    - An Amazon Simple Notification Service (SNS) topic for all unhealthy fleet notifications.
    - An AWS Key Management Service (KMS) Key to encrypt SNS messages - If no encryption key is provided.
    - An Amazon CloudWatch Alarm that triggers if a worker fleet is unhealthy for a long period.
    - Another CloudWatch Alarm that triggers if the healthy host percentage of a worker fleet is lower than allowed.
    - A single AWS Lambda function that sets fleet size to 0 when triggered in response to messages on the SNS Topic.
    - Execution logs of the AWS Lambda function are published to a log group in Amazon CloudWatch.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The AWS Lambda that is created by this construct to terminate unhealthy worker fleets has permission to
      UpdateAutoScalingGroup ( https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_UpdateAutoScalingGroup.html )
      on all of the fleets that this construct is monitoring. You should not grant any additional actors/principals the
      ability to modify or execute this Lambda.
    - Execution of the AWS Lambda for terminating unhealthy workers is triggered by messages to the Amazon Simple
      Notification Service (SNS) Topic that is created by this construct. Any principal that is able to publish notification
      to this SNS Topic can cause the Lambda to execute and reduce one of your worker fleets to zero instances. You should
      not grant any additional principals permissions to publish to this SNS Topic.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        elb_account_limits: typing.Optional[typing.Sequence[typing.Union[Limit, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: VPC to launch the Health Monitor in.
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param elb_account_limits: Describes the current Elastic Load Balancing resource limits for your AWS account. This object should be the output of 'describeAccountLimits' API. Default: default account limits for ALB is used
        :param encryption_key: A KMS Key, either managed by this CDK app, or imported. Default: A new Key will be created and used.
        :param security_group: Security group for the health monitor. This is security group is associated with the health monitor's load balancer. Default: : A security group is created
        :param vpc_subnets: Any load balancers that get created by calls to registerFleet() will be created in these subnets. Default: : The VPC default strategy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f90085c940de9aa8086799ac1ed613fcfb5ce5fb122ac38da0e827502c821e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HealthMonitorProps(
            vpc=vpc,
            deletion_protection=deletion_protection,
            elb_account_limits=elb_account_limits,
            encryption_key=encryption_key,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="registerFleet")
    def register_fleet(
        self,
        monitorable_fleet: IMonitorableFleet,
        *,
        healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
        instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
        instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Attaches the load-balancing target to the ELB for instance-level monitoring.

        The ELB does frequent pings to the workers and determines
        if a worker node is unhealthy. If so, it replaces the instance.

        It also creates an Alarm for healthy host percent and suspends the
        fleet if the given alarm is breaching. It sets the maxCapacity
        property of the auto-scaling group to 0. This should be
        reset manually after fixing the issue.

        :param monitorable_fleet: -
        :param healthy_fleet_threshold_percent: The percent of healthy hosts to consider fleet healthy and functioning. Default: 65%
        :param instance_healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. Default: 2
        :param instance_unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. Default: 3
        :param interval: The approximate time between health checks for an individual target. Default: Duration.minutes(5)
        :param port: The port that the health monitor uses when performing health checks on the targets. Default: 8081
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59c34d4093c94fdbe886b399c471f7955956cfa9f2d1330258a021a29f11da4)
            check_type(argname="argument monitorable_fleet", value=monitorable_fleet, expected_type=type_hints["monitorable_fleet"])
        health_check_config = HealthCheckConfig(
            healthy_fleet_threshold_percent=healthy_fleet_threshold_percent,
            instance_healthy_threshold_count=instance_healthy_threshold_count,
            instance_unhealthy_threshold_count=instance_unhealthy_threshold_count,
            interval=interval,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "registerFleet", [monitorable_fleet, health_check_config]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_HEALTH_CHECK_INTERVAL")
    def DEFAULT_HEALTH_CHECK_INTERVAL(cls) -> _aws_cdk_ceddda9d.Duration:
        '''Resource Tracker in Deadline currently publish health status every 5 min, hence keeping this same.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.sget(cls, "DEFAULT_HEALTH_CHECK_INTERVAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_HEALTH_CHECK_PORT")
    def DEFAULT_HEALTH_CHECK_PORT(cls) -> jsii.Number:
        '''Default health check listening port.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_HEALTH_CHECK_PORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_HEALTHY_HOST_THRESHOLD")
    def DEFAULT_HEALTHY_HOST_THRESHOLD(cls) -> jsii.Number:
        '''This is the minimum possible value of ALB health-check config, we want to mark worker healthy ASAP.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_HEALTHY_HOST_THRESHOLD"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_UNHEALTHY_HOST_THRESHOLD")
    def DEFAULT_UNHEALTHY_HOST_THRESHOLD(cls) -> jsii.Number:
        '''Resource Tracker in Deadline currently determines host unhealthy in 15 min, hence keeping this count.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_UNHEALTHY_HOST_THRESHOLD"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOAD_BALANCER_LISTENING_PORT")
    def LOAD_BALANCER_LISTENING_PORT(cls) -> jsii.Number:
        '''Since we are not doing any load balancing, this port is just an arbitrary port.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "LOAD_BALANCER_LISTENING_PORT"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyFleetActionTopic")
    def unhealthy_fleet_action_topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''SNS topic for all unhealthy fleet notifications.

        This is triggered by
        the grace period and hard terminations alarms for the registered fleets.

        This topic can be subscribed to get all fleet termination notifications.
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, jsii.get(self, "unhealthyFleetActionTopic"))


@jsii.interface(jsii_type="aws-rfdk.IMountingInstance")
class IMountingInstance(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _constructs_77d1e7e8.IConstruct,
    IScriptHost,
    typing_extensions.Protocol,
):
    '''An instance type that can mount an {@link IMountableFilesystem }.

    For example, this could be an
    {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Instance.html EC2 Instance}
    or an {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-autoscaling.AutoScalingGroup.html EC2 Auto Scaling Group}
    '''

    pass


class _IMountingInstanceProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(IScriptHost), # type: ignore[misc]
):
    '''An instance type that can mount an {@link IMountableFilesystem }.

    For example, this could be an
    {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Instance.html EC2 Instance}
    or an {@link https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-autoscaling.AutoScalingGroup.html EC2 Auto Scaling Group}
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.IMountingInstance"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMountingInstance).__jsii_proxy_class__ = lambda : _IMountingInstanceProxy


__all__ = [
    "ApplicationEndpoint",
    "ApplicationEndpointProps",
    "BlockVolumeFormat",
    "CloudWatchAgent",
    "CloudWatchAgentProps",
    "CloudWatchConfigBuilder",
    "ConnectableApplicationEndpoint",
    "ConnectableApplicationEndpointProps",
    "ConventionalScriptPathParams",
    "DistinguishedName",
    "Endpoint",
    "EndpointProps",
    "ExecuteScriptProps",
    "ExportingLogGroup",
    "ExportingLogGroupProps",
    "HealthCheckConfig",
    "HealthMonitor",
    "HealthMonitorProps",
    "IHealthMonitor",
    "IMongoDb",
    "IMonitorableFleet",
    "IMountableLinuxFilesystem",
    "IMountingInstance",
    "IScriptHost",
    "IX509CertificatePem",
    "IX509CertificatePkcs12",
    "ImportedAcmCertificate",
    "ImportedAcmCertificateProps",
    "Limit",
    "LinuxMountPointProps",
    "LogGroupFactory",
    "LogGroupFactoryProps",
    "MongoDbApplicationProps",
    "MongoDbInstaller",
    "MongoDbInstallerProps",
    "MongoDbInstance",
    "MongoDbInstanceNewVolumeProps",
    "MongoDbInstanceProps",
    "MongoDbInstanceVolumeProps",
    "MongoDbPostInstallSetup",
    "MongoDbPostInstallSetupProps",
    "MongoDbSsplLicenseAcceptance",
    "MongoDbUsers",
    "MongoDbVersion",
    "MongoDbX509User",
    "MountPermissions",
    "MountableBlockVolume",
    "MountableBlockVolumeProps",
    "MountableEfs",
    "MountableEfsProps",
    "MountableFsxLustre",
    "MountableFsxLustreProps",
    "PadEfsStorage",
    "PadEfsStorageProps",
    "ScriptAsset",
    "ScriptAssetProps",
    "SessionManagerHelper",
    "StaticPrivateIpServer",
    "StaticPrivateIpServerProps",
    "TimeZone",
    "X509CertificatePem",
    "X509CertificatePemProps",
    "X509CertificatePkcs12",
    "X509CertificatePkcs12Props",
    "deadline",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import deadline

def _typecheckingstub__d7aae1e1e7606385280722c44443deaef00f8901625489cdbd6fd96ccd1bdfd8(
    *,
    address: builtins.str,
    port: jsii.Number,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d1b9b863bc88f01c9cc4c26b0cc9bf80f0349ec736b442e56075dca4cff48c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_watch_config: builtins.str,
    host: IScriptHost,
    should_install_agent: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8221e47302da6430194635a16a777c3e4077948c6773bb08e14eb422cb26c00(
    *,
    cloud_watch_config: builtins.str,
    host: IScriptHost,
    should_install_agent: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee3213416bf136598eadb8bb9bc028e1c4431ede6fb1dabd402caf60592534d(
    log_flush_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181f242f6e8e76570db13dc1d7338ca24da148900dfeb1d1989a5405957f0b89(
    log_group_name: builtins.str,
    log_stream_prefix: builtins.str,
    log_file_path: builtins.str,
    time_zone: typing.Optional[TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f25d9774cf848cafb8bf57d6cab9a23f78b963586ea9c5f3c15b333fbf34b8b(
    *,
    address: builtins.str,
    port: jsii.Number,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    connections: _aws_cdk_aws_ec2_ceddda9d.Connections,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b0b193e60f50e17f048423e8cf05bb26dae07981f21aa1bcad9942e8605967(
    *,
    base_name: builtins.str,
    os_type: _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType,
    root_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddee105e5ab12508ec4acbfbaca4a1fb33ae318c62f07672117d3cd87b26ecc3(
    *,
    cn: builtins.str,
    o: typing.Optional[builtins.str] = None,
    ou: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d95bd543b1133caf30aabb41c49805136a34e32ad0f00d07379d58f49b5f73f(
    *,
    address: builtins.str,
    port: jsii.Number,
    protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Protocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e700f29d38abec3def891c9fe8d7c313850c2d78eea8d8a7d2b845e2fd7fb3b(
    *,
    host: IScriptHost,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd293e1060041be76c1a0e849ba287648dd0ac8dd43fcf08c78cc91610ec0c84(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: builtins.str,
    log_group_name: builtins.str,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc01869453fa82c8a3906575f23b32a1f7a5c67a24b7ff0b2633513e65328d8(
    *,
    bucket_name: builtins.str,
    log_group_name: builtins.str,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea42155f729a06271fd2940ff6cd6cc955170cf28d6854cc516f12a28c2a08f(
    *,
    healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
    instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
    instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfad80c3105e3245dca4fa4386a074b4c5f03dd705aac66898cc20c2e0c3b43(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    deletion_protection: typing.Optional[builtins.bool] = None,
    elb_account_limits: typing.Optional[typing.Sequence[typing.Union[Limit, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7ee0821865234eed27a6cc965fd6816e0e85d92d76d870878c149c5739deda(
    monitorable_fleet: IMonitorableFleet,
    *,
    healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
    instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
    instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59049fccbead79b85bcbad3ce6d6a3d892ce907c75f9f0c4a38950b4f006cac(
    *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5271928b2275188a85699b7957d3e2ea9a76e0c869963434c43548c64d4b1661(
    target: IMountingInstance,
    *,
    location: builtins.str,
    permissions: typing.Optional[MountPermissions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007bf741112c4ffd6fdde5cb15520ec322690e578859a3a9454a714a8221b83c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cert: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    key: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    passphrase: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    cert_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad608c351636827791d224b1f58214b7f409c0f35f71b8e32b3933b326a8dba(
    policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd0d88a96f9c5734743f08fa09845715c16d4a270389b929385061cf9e06969(
    *,
    cert: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    key: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    passphrase: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    cert_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e455b38bcb04a52144b7f18ac2f60adca374fdd61d4d782e4540f5093a6b73(
    *,
    max: jsii.Number,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ab164dc4e5b0f1349e200824495832c9defa2ce58961d1221834bcab59123d(
    *,
    location: builtins.str,
    permissions: typing.Optional[MountPermissions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8528d10537a4bbd86945bc9163a000afa02a3fbb1a26818bd9505bd909306c(
    scope: _constructs_77d1e7e8.Construct,
    log_wrapper_id: builtins.str,
    log_group_name: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    log_group_prefix: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d3f4653a05483f8662df72dcd865804ecded19419422cdd06a4de9dcd75d45(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    log_group_prefix: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0e67b2e068f82597a8e160692e4068c8b7f72b3c5d504539eaa2b7b8b5cab5(
    *,
    dns_zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
    hostname: builtins.str,
    server_certificate: IX509CertificatePem,
    version: MongoDbVersion,
    admin_user: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    mongo_data_volume: typing.Optional[typing.Union[MongoDbInstanceVolumeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_sspl_acceptance: typing.Optional[MongoDbSsplLicenseAcceptance] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b23a390fe61f77052147d302b356a6f1638c251d56f9bdfcea550dd5a32181a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    version: MongoDbVersion,
    user_sspl_acceptance: typing.Optional[MongoDbSsplLicenseAcceptance] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8123ef5813eb0eb58a8a64aa65ad09cd8efe784bdc7578292ef430a8807a001(
    target: IScriptHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b496f200afaf6e5b0f3f6e857ceb8372ec3b62603f22e2d6473892f954349884(
    *,
    version: MongoDbVersion,
    user_sspl_acceptance: typing.Optional[MongoDbSsplLicenseAcceptance] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e621ae9df55786e7b260e2d74dce3b522b6efaa597507a602a78a057336f1ae4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    mongo_db: typing.Union[MongoDbApplicationProps, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[LogGroupFactoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85a56fe3ba0d570817245e78e1b7dbef19b124d3378fdad999df16a2627001f(
    *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd72ba805b523adaf73080f33bb5a18bdc09fd7c72d04304d2b7cdbce52f177(
    host: IScriptHost,
    group_name: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    log_group_prefix: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dde051e64c0e787cd1dbe573de358b27b9e730c84cc713ab7ba1bd1cfc6f7d8(
    instance: StaticPrivateIpServer,
    *,
    dns_zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
    hostname: builtins.str,
    server_certificate: IX509CertificatePem,
    version: MongoDbVersion,
    admin_user: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    mongo_data_volume: typing.Optional[typing.Union[MongoDbInstanceVolumeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_sspl_acceptance: typing.Optional[MongoDbSsplLicenseAcceptance] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c41fb05dcf30d03a3068e6b753627e90fcc95fad10000daef3e0293f737b44(
    *,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90082e83281497abb52eaeae883b0134d9e66369c6c09101b997c94ebc72987(
    *,
    mongo_db: typing.Union[MongoDbApplicationProps, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[LogGroupFactoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbefdbc270273ca4e3b0f6d9a1b3fe25fb5de4e57cd405e3c9e5540cbc0198f(
    *,
    volume: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVolume] = None,
    volume_props: typing.Optional[typing.Union[MongoDbInstanceNewVolumeProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b493fcc3de8a8c11a7912a14a89e48713c7dc223a06c821165a3f2d351a35d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    mongo_db: IMongoDb,
    users: typing.Union[MongoDbUsers, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8e6b2e007846d0c58c1e5fc4e2986cb05fb6b018f6642266fd6bb2124bfe91(
    *,
    mongo_db: IMongoDb,
    users: typing.Union[MongoDbUsers, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a31e98f1a2e4f2ef453c66a698577e62e73e396d0366d0ba3e18dd865eaae74(
    *,
    password_auth_users: typing.Optional[typing.Sequence[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]] = None,
    x509_auth_users: typing.Optional[typing.Sequence[typing.Union[MongoDbX509User, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8a916c3b41e19d22b2c424bacbe2e2a9b8b7916d0068ab516c8ef8456e926c(
    *,
    certificate: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    roles: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074d44aba8b2ab8d183862018b28fb57b56393ef0bbaaaa39630b10002a9fd8b(
    scope: _constructs_77d1e7e8.Construct,
    *,
    block_volume: _aws_cdk_aws_ec2_ceddda9d.IVolume,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_format: typing.Optional[BlockVolumeFormat] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4e1bfe44b11dcc3b16dc35a7f3084253f43f4beffbdb6bf1bfca1fe91f2583(
    target: IMountingInstance,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4074e7c1ed2438417f56776476b39f579267f4a720433047cd008f568537ee87(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e186a94dece5cabc525b3cc468a0a6c85f7bc5586102580e21f838807afa80(
    target: IMountingInstance,
    *,
    location: builtins.str,
    permissions: typing.Optional[MountPermissions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dfbf49f974d5284b88260ad2587762702803a672d48f7e88ad0ff53e857a06(
    *,
    block_volume: _aws_cdk_aws_ec2_ceddda9d.IVolume,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_format: typing.Optional[BlockVolumeFormat] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee45726c62fa55071c23f9e714efc4cf7d40ba0700cf2095ff46ec393249f0fe(
    scope: _constructs_77d1e7e8.Construct,
    *,
    filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
    access_point: typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint] = None,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    resolve_mount_target_dns_with_api: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20321acd49c203b04dff2c5d50d1c99d8ae8ee65e8bcb768707fbd5c46d81811(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8486b0d887b43a87f64fdbe8a3950fb8879e6d715e694e1da8ef5397b7c8cd29(
    target: IMountingInstance,
    *,
    location: builtins.str,
    permissions: typing.Optional[MountPermissions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c94c72b7311939c7f317245510f3281104638e4ed3e69220cad9912b1482167(
    *,
    filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
    access_point: typing.Optional[_aws_cdk_aws_efs_ceddda9d.IAccessPoint] = None,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    resolve_mount_target_dns_with_api: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb84dd6da44bca71733340804fb30b66311bca3bf753247564cb3654fa2f459d(
    scope: _constructs_77d1e7e8.Construct,
    *,
    filesystem: _aws_cdk_aws_fsx_ceddda9d.LustreFileSystem,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    fileset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2764abeebcaa56b7da9bdc4fd6402f2515f63a313683a5444b0351e823ba6bec(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba07043caf53b4d521db3278198d9f606ac396ff613ed8a4c362f31a53934162(
    target: IMountingInstance,
    *,
    location: builtins.str,
    permissions: typing.Optional[MountPermissions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2040c1feb8267635fcf3aaa1ae40c15b22baf941da809618037281e5769efef(
    *,
    filesystem: _aws_cdk_aws_fsx_ceddda9d.LustreFileSystem,
    extra_mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    fileset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2806f9d6f1472412d837a5da5c0f8658de013818d7f1b2ff37580af0af60dae(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_point: _aws_cdk_aws_efs_ceddda9d.IAccessPoint,
    desired_padding: _aws_cdk_ceddda9d.Size,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b240cf7ea3ae2d2c08a61f2b824f60dfc1c1b976881c247fd6333f222bfb2d1(
    *,
    access_point: _aws_cdk_aws_efs_ceddda9d.IAccessPoint,
    desired_padding: _aws_cdk_ceddda9d.Size,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fae01edbd9cc35ef40f65e416f67d058eecaf16813f35193baac14b4d7d682a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    deploy_time: typing.Optional[builtins.bool] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5e0e51e5f067fbddb30ac61d5c6b41efd30fdb5b397817f7f205de8ed20f80(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    base_name: builtins.str,
    os_type: _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType,
    root_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbfbab47c8dce2a4d14e3076c2ec8b5ed3a0e6e47ad3d6828114449f40e7c91(
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    deploy_time: typing.Optional[builtins.bool] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d44616e89c67dda85e3442c73a9f1635be87fb41e10aefb9cc7966da9e554eb(
    grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c191460db188d618ceebc2a95bc294d5896fac791b3cac4b2937730460bc3540(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109f1d21e771bc801cd52c072416b3ae5d48df94de67d735da4ed0dd3d4c536a(
    eni: _aws_cdk_aws_ec2_ceddda9d.CfnNetworkInterface,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c35fbde32de081eaaec85a85f4ee239ae4391520b3e2b2c91676a1f6618287(
    lambda_handler: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710d0b8731d3712c95c2821eda28e8c1aa851651ab86c17a4443099a11e2b48a(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ddc6d885f3912b4be7e4e33c666b507c58a702408d7f47f58cb20df0adf34a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subject: typing.Union[DistinguishedName, typing.Dict[builtins.str, typing.Any]],
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    signing_certificate: typing.Optional[X509CertificatePem] = None,
    valid_for: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7859d86c362e46d13274f9a0903645ed079287999aee58341a6d3e0bb81ff9d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb5ea571776e0d5743b2950f3b232f40d852563f7e8844e1240403223acc03f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327ebc14939e1e1e9c45e87054d12059a540ed483e0235a96d578a142d46e341(
    value: _aws_cdk_aws_dynamodb_ceddda9d.Table,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820d3c8e6698d22b77be9ff23fa748243ef069db8ff54c3f1b11083e8a1d3510(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd288d91e62695bff878cf40834e780e781bf59ff8469237913959db4dc8488(
    value: _aws_cdk_ceddda9d.Tag,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2683acb2b44b2891288efdf84eac6ea342dfd7823c1e8f05a14579469ca71e5(
    *,
    subject: typing.Union[DistinguishedName, typing.Dict[builtins.str, typing.Any]],
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    signing_certificate: typing.Optional[X509CertificatePem] = None,
    valid_for: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c109807fb76f18601699009346b8753aa790c458d4c7a97598fbd323392426(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_certificate: X509CertificatePem,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4057af8359aaf7ab10e4fc229079acf5d97ba3741a64214032d7711a67575b8(
    value: _aws_cdk_aws_dynamodb_ceddda9d.Table,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7672fe77b797243d061153110a4106da10d5cf97b9aa7b775717a9d67127f2a3(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c70764d051ccabc636a8ed820262d61741729d1fe60cdef2f565fb42f312679(
    value: _aws_cdk_ceddda9d.Tag,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e0ff1d9c7da9f35e938333e84ca7d6df43be25aec5d4579a47610bfda4277f(
    *,
    source_certificate: X509CertificatePem,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f90085c940de9aa8086799ac1ed613fcfb5ce5fb122ac38da0e827502c821e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    deletion_protection: typing.Optional[builtins.bool] = None,
    elb_account_limits: typing.Optional[typing.Sequence[typing.Union[Limit, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59c34d4093c94fdbe886b399c471f7955956cfa9f2d1330258a021a29f11da4(
    monitorable_fleet: IMonitorableFleet,
    *,
    healthy_fleet_threshold_percent: typing.Optional[jsii.Number] = None,
    instance_healthy_threshold_count: typing.Optional[jsii.Number] = None,
    instance_unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
