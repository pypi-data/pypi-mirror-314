r'''
# multi-az-observability

This is a CDK construct for multi-AZ observability to help detect single-AZ impairments. This is currently an `alpha` version, but is being used in the AWS [Advanced Multi-AZ Resilience Patterns](https://catalog.workshops.aws/multi-az-gray-failures/en-US) workshop.

There is a lot of available information to think through and combine to provide signals about single-AZ impact. To simplify the setup and use reasonable defaults, this construct (available in TypeScript, Go, Python, and .NET [Java coming soon]) sets up the necessary observability. To use the CDK construct, you first define your service like this:

```csharp
var wildRydesService = new Service(new ServiceProps(){
    ServiceName = "WildRydes",
    BaseUrl = "http://www.example.com",
    FaultCountThreshold = 25,
    AvailabilityZoneNames = vpc.AvailabilityZones,
    Period = Duration.Seconds(60),
    LoadBalancer = loadBalancer,
    DefaultAvailabilityMetricDetails = new ServiceMetricDetails(new ServiceMetricDetailsProps() {
        AlarmStatistic = "Sum",
        DatapointsToAlarm = 3,
        EvaluationPeriods = 5,
        FaultAlarmThreshold = 1,
        FaultMetricNames = new string[] { "Fault", "Error" },
        GraphedFaultStatistics = new string[] { "Sum" },
        GraphedSuccessStatistics = new string[] { "Sum" },
        MetricNamespace = metricsNamespace,
        Period = Duration.Seconds(60),
        SuccessAlarmThreshold = 99,
        SuccessMetricNames = new string[] {"Success"},
        Unit = Unit.COUNT,
    }),
    DefaultLatencyMetricDetails = new ServiceMetricDetails(new ServiceMetricDetailsProps(){
        AlarmStatistic = "p99",
        DatapointsToAlarm = 3,
        EvaluationPeriods = 5,
        FaultAlarmThreshold = 1,
        FaultMetricNames = new string[] { "FaultLatency" },
        GraphedFaultStatistics = new string[] { "p50" },
        GraphedSuccessStatistics = new string[] { "p50", "p99", "tm50", "tm99" },
        MetricNamespace = metricsNamespace,
        Period = Duration.Seconds(60),
        SuccessAlarmThreshold = 100,
        SuccessMetricNames = new string[] {"SuccessLatency"},
        Unit = Unit.MILLISECONDS,
    }),
    DefaultContributorInsightRuleDetails =  new ContributorInsightRuleDetails(new ContributorInsightRuleDetailsProps() {
        AvailabilityZoneIdJsonPath = azIdJsonPath,
        FaultMetricJsonPath = faultMetricJsonPath,
        InstanceIdJsonPath = instanceIdJsonPath,
        LogGroups = serverLogGroups,
        OperationNameJsonPath = operationNameJsonPath,
        SuccessLatencyMetricJsonPath = successLatencyMetricJsonPath
    }),
    CanaryTestProps = new AddCanaryTestProps() {
        RequestCount = 10,
        LoadBalancer = loadBalancer,
        Schedule = "rate(1 minute)",
        NetworkConfiguration = new NetworkConfigurationProps() {
            Vpc = vpc,
            SubnetSelection = new SubnetSelection() { SubnetType = SubnetType.PRIVATE_ISOLATED }
        }
    }
});
wildRydesService.AddOperation(new Operation(new OperationProps() {
    OperationName = "Signin",
    Path = "/signin",
    Service = wildRydesService,
    Critical = true,
    HttpMethods = new string[] { "GET" },
    ServerSideAvailabilityMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Signin",
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Signin"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultAvailabilityMetricDetails),
    ServerSideLatencyMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Signin",
        SuccessAlarmThreshold = 150,
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Signin"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultLatencyMetricDetails),
    CanaryTestLatencyMetricsOverride = new CanaryTestMetricsOverride(new CanaryTestMetricsOverrideProps() {
        SuccessAlarmThreshold = 250
    })
}));
wildRydesService.AddOperation(new Operation(new OperationProps() {
    OperationName = "Pay",
    Path = "/pay",
    Service = wildRydesService,
    HttpMethods = new string[] { "GET" },
    Critical = true,
    ServerSideAvailabilityMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Pay",
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Pay"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultAvailabilityMetricDetails),
    ServerSideLatencyMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Pay",
        SuccessAlarmThreshold = 200,
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Pay"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultLatencyMetricDetails),
    CanaryTestLatencyMetricsOverride = new CanaryTestMetricsOverride(new CanaryTestMetricsOverrideProps() {
        SuccessAlarmThreshold = 300
    })
}));
wildRydesService.AddOperation(new Operation(new OperationProps() {
    OperationName = "Ride",
    Path = "/ride",
    Service = wildRydesService,
    HttpMethods = new string[] { "GET" },
    Critical = true,
    ServerSideAvailabilityMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Ride",
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Ride"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultAvailabilityMetricDetails),
    ServerSideLatencyMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Ride",
        SuccessAlarmThreshold = 350,
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Ride"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultLatencyMetricDetails),
    CanaryTestLatencyMetricsOverride = new CanaryTestMetricsOverride(new CanaryTestMetricsOverrideProps() {
        SuccessAlarmThreshold = 550
    })
}));
wildRydesService.AddOperation(new Operation(new OperationProps() {
    OperationName = "Home",
    Path = "/home",
    Service = wildRydesService,
    HttpMethods = new string[] { "GET" },
    Critical = true,
    ServerSideAvailabilityMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Home",
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Ride"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultAvailabilityMetricDetails),
    ServerSideLatencyMetricDetails = new OperationMetricDetails(new OperationMetricDetailsProps() {
        OperationName = "Home",
        SuccessAlarmThreshold = 100,
        MetricDimensions = new MetricDimensions(new Dictionary<string, string> {{ "Operation", "Ride"}}, "AZ-ID", "Region")
    }, wildRydesService.DefaultLatencyMetricDetails),
    CanaryTestLatencyMetricsOverride = new CanaryTestMetricsOverride(new CanaryTestMetricsOverrideProps() {
        SuccessAlarmThreshold = 200
    })
}));
```

Then you provide that service definition to the CDK construct.

```csharp
InstrumentedServiceMultiAZObservability multiAvailabilityZoneObservability = new InstrumentedServiceMultiAZObservability(this, "MultiAZObservability", new InstrumentedServiceMultiAZObservabilityProps() {
    Service = wildRydesService,
    CreateDashboards = true,
    Interval = Duration.Minutes(60), // The interval for the dashboard
    OutlierDetectionAlgorithm = OutlierDetectionAlgorithm.STATIC
});
```

You define some characteristics of the service, default values for metrics and alarms, and then add operations as well as any overrides for default values that you need. The construct can also automatically create synthetic canaries that test each operation with a very simple HTTP check, or you can configure your own synthetics and just tell the construct about the metric details and optionally log files. This creates metrics, alarms, and dashboards that can be used to detect single-AZ impact.

If you don't have service specific logs and custom metrics with per-AZ dimensions, you can still use the construct to evaluate ALB and NAT Gateway metrics to find single AZ faults.

```csharp
BasicServiceMultiAZObservability multiAvailabilityZoneObservability = new BasicServiceMultiAZObservability(this, "MultiAZObservability", new BasicServiceMultiAZObservabilityProps() {
    ApplicationLoadBalancers = new IApplicationLoadBalancer[] { loadBalancer },
    NatGateways = new Dictionary<string, CfnNatGateway>() {
        { "us-east-1a", natGateway1},
        { "us-east-1b", natGateway2},
        { "us-east-1c", natGateway3},
    },
    CreateDashboard = true,
    OutlierDetectionAlgorithm = OutlierDetectionAlgorithm.STATIC,
    FaultCountPercentageThreshold = 1.0, // The fault rate to alarm on for errors seen from the ALBs in the same AZ
    PacketLossImpactPercentageThreshold = 0.01, // The percentage of packet loss to alarm on for the NAT Gateways in the same AZ
    ServiceName = "WildRydes",
    Period = Duration.Seconds(60), // The period for metric evaluation
    Interval = Duration.Minutes(60) // The interval for the dashboards
    EvaluationPeriods = 5,
    DatapointsToAlarm = 3
});
```

If you provide a load balancer, the construct assumes it is deployed in each AZ of the VPC the load balancer is associated with and will look for HTTP metrics using those AZs as dimensions.

Both options support running workloads on EC2, ECS, Lambda, and EKS.

## TODO

* Add additional unit tests
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
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="multi-az-observability.AddCanaryTestProps",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer": "loadBalancer",
        "request_count": "requestCount",
        "schedule": "schedule",
        "headers": "headers",
        "http_methods": "httpMethods",
        "ignore_tls_errors": "ignoreTlsErrors",
        "network_configuration": "networkConfiguration",
        "post_data": "postData",
        "regional_request_count": "regionalRequestCount",
        "timeout": "timeout",
    },
)
class AddCanaryTestProps:
    def __init__(
        self,
        *,
        load_balancer: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2,
        request_count: jsii.Number,
        schedule: builtins.str,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_tls_errors: typing.Optional[builtins.bool] = None,
        network_configuration: typing.Optional[typing.Union["NetworkConfigurationProps", typing.Dict[builtins.str, typing.Any]]] = None,
        post_data: typing.Optional[builtins.str] = None,
        regional_request_count: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''The props for requesting a canary be made for an operation.

        :param load_balancer: The load balancer that will be tested against.
        :param request_count: The number of requests to send on each test.
        :param schedule: A schedule expression.
        :param headers: Any headers to include. Default: - No additional headers are added to the requests
        :param http_methods: Defining this will override the methods defined in the operation and will use these instead. Default: - The operation's defined HTTP methods will be used to conduct the canary tests
        :param ignore_tls_errors: Whether to ignore TLS validation errors. Default: - false
        :param network_configuration: The VPC network configuration. Default: - The Lambda function is not run in a VPC
        :param post_data: Data to supply in a POST, PUT, or PATCH operation. Default: - No data is sent in a POST, PUT, or PATCH request
        :param regional_request_count: Specifies a separate number of request to send to the regional endpoint. Default: - The same number of requests specified by the requestCount property is used.
        :param timeout: The timeout for each individual HTTP request. Default: - Defaults to 2 seconds
        '''
        if isinstance(network_configuration, dict):
            network_configuration = NetworkConfigurationProps(**network_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead8ba42e0ffe8c4a0a0bf4162d6495fdaa628aafcb33fec909f0b0d4326fd11)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument request_count", value=request_count, expected_type=type_hints["request_count"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument ignore_tls_errors", value=ignore_tls_errors, expected_type=type_hints["ignore_tls_errors"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument post_data", value=post_data, expected_type=type_hints["post_data"])
            check_type(argname="argument regional_request_count", value=regional_request_count, expected_type=type_hints["regional_request_count"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer": load_balancer,
            "request_count": request_count,
            "schedule": schedule,
        }
        if headers is not None:
            self._values["headers"] = headers
        if http_methods is not None:
            self._values["http_methods"] = http_methods
        if ignore_tls_errors is not None:
            self._values["ignore_tls_errors"] = ignore_tls_errors
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if post_data is not None:
            self._values["post_data"] = post_data
        if regional_request_count is not None:
            self._values["regional_request_count"] = regional_request_count
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2:
        '''The load balancer that will be tested against.'''
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2, result)

    @builtins.property
    def request_count(self) -> jsii.Number:
        '''The number of requests to send on each test.'''
        result = self._values.get("request_count")
        assert result is not None, "Required property 'request_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''A schedule expression.'''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Any headers to include.

        :default: - No additional headers are added to the requests
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def http_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defining this will override the methods defined in the operation and will use these instead.

        :default:

        - The operation's defined HTTP methods will be used to
        conduct the canary tests
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_tls_errors(self) -> typing.Optional[builtins.bool]:
        '''Whether to ignore TLS validation errors.

        :default: - false
        '''
        result = self._values.get("ignore_tls_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def network_configuration(self) -> typing.Optional["NetworkConfigurationProps"]:
        '''The VPC network configuration.

        :default: - The Lambda function is not run in a VPC
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["NetworkConfigurationProps"], result)

    @builtins.property
    def post_data(self) -> typing.Optional[builtins.str]:
        '''Data to supply in a POST, PUT, or PATCH operation.

        :default: - No data is sent in a POST, PUT, or PATCH request
        '''
        result = self._values.get("post_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regional_request_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies a separate number of request to send to the regional endpoint.

        :default: - The same number of requests specified by the requestCount property is used.
        '''
        result = self._values.get("regional_request_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The timeout for each individual HTTP request.

        :default: - Defaults to 2 seconds
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddCanaryTestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.AvailabilityZoneMapperProps",
    jsii_struct_bases=[],
    name_mapping={"availability_zone_names": "availabilityZoneNames"},
)
class AvailabilityZoneMapperProps:
    def __init__(
        self,
        *,
        availability_zone_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for the AZ mapper.

        :param availability_zone_names: The currently in use Availability Zone names which constrains the list of AZ IDs that are returned. Default: - No names are provided and the mapper returns all AZs in the region in its lists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2806dcb155fd8f09292d7b6d39dfa33ee61c19d88b123657eeca548a43253f8a)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_names is not None:
            self._values["availability_zone_names"] = availability_zone_names

    @builtins.property
    def availability_zone_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The currently in use Availability Zone names which constrains the list of AZ IDs that are returned.

        :default:

        - No names are provided and the mapper returns
        all AZs in the region in its lists
        '''
        result = self._values.get("availability_zone_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AvailabilityZoneMapperProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.BasicServiceMultiAZObservabilityProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_dashboard": "createDashboard",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "outlier_detection_algorithm": "outlierDetectionAlgorithm",
        "period": "period",
        "service_name": "serviceName",
        "application_load_balancers": "applicationLoadBalancers",
        "assets_bucket_parameter_name": "assetsBucketParameterName",
        "assets_bucket_prefix_parameter_name": "assetsBucketPrefixParameterName",
        "fault_count_percentage_threshold": "faultCountPercentageThreshold",
        "interval": "interval",
        "nat_gateways": "natGateways",
        "outlier_threshold": "outlierThreshold",
        "packet_loss_impact_percentage_threshold": "packetLossImpactPercentageThreshold",
    },
)
class BasicServiceMultiAZObservabilityProps:
    def __init__(
        self,
        *,
        create_dashboard: builtins.bool,
        datapoints_to_alarm: jsii.Number,
        evaluation_periods: jsii.Number,
        outlier_detection_algorithm: "OutlierDetectionAlgorithm",
        period: _aws_cdk_ceddda9d.Duration,
        service_name: builtins.str,
        application_load_balancers: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]] = None,
        assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
        assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
        fault_count_percentage_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        nat_gateways: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]] = None,
        outlier_threshold: typing.Optional[jsii.Number] = None,
        packet_loss_impact_percentage_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for creating a basic service.

        :param create_dashboard: Whether to create a dashboard displaying the metrics and alarms.
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms.
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms.
        :param outlier_detection_algorithm: The algorithm to use for performing outlier detection.
        :param period: The period to evaluate metrics.
        :param service_name: The service's name.
        :param application_load_balancers: The application load balancers being used by the service. Default: - No alarms for ALBs will be created
        :param assets_bucket_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket location CDK provides by default for bundled assets. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - The assets will be uploaded to the default defined asset location.
        :param assets_bucket_prefix_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket prefix CDK provides by default for bundled assets. This property only takes effect if you defined the assetsBucketParameterName. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - No object prefix will be added to your custom assets location. However, if you have overridden something like the 'BucketPrefix' property in your stack synthesizer with a variable like "${AssetsBucketPrefix", you will need to define this property so it doesn't cause a reference error even if the prefix value is blank.
        :param fault_count_percentage_threshold: The percentage of faults for a single ALB to consider an AZ to be unhealthy, this should align with your availability goal. For example 1% or 5%. Default: - 5 (as in 5%)
        :param interval: Dashboard interval. Default: - 1 hour
        :param nat_gateways: (Optional) A map of Availability Zone name to the NAT Gateways in that AZ. Default: - No alarms for NAT Gateways will be created
        :param outlier_threshold: The outlier threshold for determining if an AZ is an outlier for latency or faults. This number is interpreted differently for different outlier algorithms. When used with STATIC, the number should be between 0 and 1 to represent the percentage of errors (like .7) that an AZ must be responsible for to be considered an outlier. When used with CHI_SQUARED, it represents the p value that indicates statistical significance, like 0.05 which means the skew has less than or equal to a 5% chance of occuring. When used with Z_SCORE it indicates how many standard deviations to evaluate for an AZ being an outlier, typically 3 is standard for Z_SCORE. Standard defaults based on the outlier detection algorithm: STATIC: 0.7 CHI_SQUARED: 0.05 Z_SCORE: 2 IQR: 1.5 MAD: 3 Default: - Depends on the outlier detection algorithm selected
        :param packet_loss_impact_percentage_threshold: The amount of packet loss in a NAT GW to determine if an AZ is actually impacted, recommendation is 0.01%. Default: - 0.01 (as in 0.01%)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58ece35f77caa4f37dc329d2df9a0806a48ec2ac96819d5b3bec961e5f2b3d9)
            check_type(argname="argument create_dashboard", value=create_dashboard, expected_type=type_hints["create_dashboard"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument outlier_detection_algorithm", value=outlier_detection_algorithm, expected_type=type_hints["outlier_detection_algorithm"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument application_load_balancers", value=application_load_balancers, expected_type=type_hints["application_load_balancers"])
            check_type(argname="argument assets_bucket_parameter_name", value=assets_bucket_parameter_name, expected_type=type_hints["assets_bucket_parameter_name"])
            check_type(argname="argument assets_bucket_prefix_parameter_name", value=assets_bucket_prefix_parameter_name, expected_type=type_hints["assets_bucket_prefix_parameter_name"])
            check_type(argname="argument fault_count_percentage_threshold", value=fault_count_percentage_threshold, expected_type=type_hints["fault_count_percentage_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument outlier_threshold", value=outlier_threshold, expected_type=type_hints["outlier_threshold"])
            check_type(argname="argument packet_loss_impact_percentage_threshold", value=packet_loss_impact_percentage_threshold, expected_type=type_hints["packet_loss_impact_percentage_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_dashboard": create_dashboard,
            "datapoints_to_alarm": datapoints_to_alarm,
            "evaluation_periods": evaluation_periods,
            "outlier_detection_algorithm": outlier_detection_algorithm,
            "period": period,
            "service_name": service_name,
        }
        if application_load_balancers is not None:
            self._values["application_load_balancers"] = application_load_balancers
        if assets_bucket_parameter_name is not None:
            self._values["assets_bucket_parameter_name"] = assets_bucket_parameter_name
        if assets_bucket_prefix_parameter_name is not None:
            self._values["assets_bucket_prefix_parameter_name"] = assets_bucket_prefix_parameter_name
        if fault_count_percentage_threshold is not None:
            self._values["fault_count_percentage_threshold"] = fault_count_percentage_threshold
        if interval is not None:
            self._values["interval"] = interval
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if outlier_threshold is not None:
            self._values["outlier_threshold"] = outlier_threshold
        if packet_loss_impact_percentage_threshold is not None:
            self._values["packet_loss_impact_percentage_threshold"] = packet_loss_impact_percentage_threshold

    @builtins.property
    def create_dashboard(self) -> builtins.bool:
        '''Whether to create a dashboard displaying the metrics and alarms.'''
        result = self._values.get("create_dashboard")
        assert result is not None, "Required property 'create_dashboard' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        result = self._values.get("datapoints_to_alarm")
        assert result is not None, "Required property 'datapoints_to_alarm' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def outlier_detection_algorithm(self) -> "OutlierDetectionAlgorithm":
        '''The algorithm to use for performing outlier detection.'''
        result = self._values.get("outlier_detection_algorithm")
        assert result is not None, "Required property 'outlier_detection_algorithm' is missing"
        return typing.cast("OutlierDetectionAlgorithm", result)

    @builtins.property
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period to evaluate metrics.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''The service's name.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_load_balancers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]]:
        '''The application load balancers being used by the service.

        :default: - No alarms for ALBs will be created
        '''
        result = self._values.get("application_load_balancers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]], result)

    @builtins.property
    def assets_bucket_parameter_name(self) -> typing.Optional[builtins.str]:
        '''If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here.

        It will override the bucket location CDK provides by
        default for bundled assets. The stack containing this contruct needs
        to have a parameter defined that uses this name. The underlying
        stacks in this construct that deploy assets will copy the parent stack's
        value for this property.

        :default:

        - The assets will be uploaded to the default defined
        asset location.
        '''
        result = self._values.get("assets_bucket_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assets_bucket_prefix_parameter_name(self) -> typing.Optional[builtins.str]:
        '''If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here.

        It will override the bucket prefix CDK provides by
        default for bundled assets. This property only takes effect if you
        defined the assetsBucketParameterName. The stack containing this contruct needs
        to have a parameter defined that uses this name. The underlying
        stacks in this construct that deploy assets will copy the parent stack's
        value for this property.

        :default:

        - No object prefix will be added to your custom assets location.
        However, if you have overridden something like the 'BucketPrefix' property
        in your stack synthesizer with a variable like "${AssetsBucketPrefix",
        you will need to define this property so it doesn't cause a reference error
        even if the prefix value is blank.
        '''
        result = self._values.get("assets_bucket_prefix_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fault_count_percentage_threshold(self) -> typing.Optional[jsii.Number]:
        '''The percentage of faults for a single ALB to consider an AZ to be unhealthy, this should align with your availability goal.

        For example
        1% or 5%.

        :default: - 5 (as in 5%)
        '''
        result = self._values.get("fault_count_percentage_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Dashboard interval.

        :default: - 1 hour
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def nat_gateways(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]]:
        '''(Optional) A map of Availability Zone name to the NAT Gateways in that AZ.

        :default: - No alarms for NAT Gateways will be created
        '''
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]], result)

    @builtins.property
    def outlier_threshold(self) -> typing.Optional[jsii.Number]:
        '''The outlier threshold for determining if an AZ is an outlier for latency or faults.

        This number is interpreted
        differently for different outlier algorithms. When used with
        STATIC, the number should be between 0 and 1 to represent the
        percentage of errors (like .7) that an AZ must be responsible
        for to be considered an outlier. When used with CHI_SQUARED, it
        represents the p value that indicates statistical significance, like
        0.05 which means the skew has less than or equal to a 5% chance of
        occuring. When used with Z_SCORE it indicates how many standard
        deviations to evaluate for an AZ being an outlier, typically 3 is
        standard for Z_SCORE.

        Standard defaults based on the outlier detection algorithm:
        STATIC: 0.7
        CHI_SQUARED: 0.05
        Z_SCORE: 2
        IQR: 1.5
        MAD: 3

        :default: - Depends on the outlier detection algorithm selected
        '''
        result = self._values.get("outlier_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def packet_loss_impact_percentage_threshold(self) -> typing.Optional[jsii.Number]:
        '''The amount of packet loss in a NAT GW to determine if an AZ is actually impacted, recommendation is 0.01%.

        :default: - 0.01 (as in 0.01%)
        '''
        result = self._values.get("packet_loss_impact_percentage_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicServiceMultiAZObservabilityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.CanaryMetricProps",
    jsii_struct_bases=[],
    name_mapping={
        "canary_availability_metric_details": "canaryAvailabilityMetricDetails",
        "canary_latency_metric_details": "canaryLatencyMetricDetails",
    },
)
class CanaryMetricProps:
    def __init__(
        self,
        *,
        canary_availability_metric_details: "IOperationMetricDetails",
        canary_latency_metric_details: "IOperationMetricDetails",
    ) -> None:
        '''Properties for canary metrics in an operation.

        :param canary_availability_metric_details: The canary availability metric details.
        :param canary_latency_metric_details: The canary latency metric details.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5fbbcf0f0c157e36d061ece26f53404876732a0a0a2c1648fd38273b093052)
            check_type(argname="argument canary_availability_metric_details", value=canary_availability_metric_details, expected_type=type_hints["canary_availability_metric_details"])
            check_type(argname="argument canary_latency_metric_details", value=canary_latency_metric_details, expected_type=type_hints["canary_latency_metric_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "canary_availability_metric_details": canary_availability_metric_details,
            "canary_latency_metric_details": canary_latency_metric_details,
        }

    @builtins.property
    def canary_availability_metric_details(self) -> "IOperationMetricDetails":
        '''The canary availability metric details.'''
        result = self._values.get("canary_availability_metric_details")
        assert result is not None, "Required property 'canary_availability_metric_details' is missing"
        return typing.cast("IOperationMetricDetails", result)

    @builtins.property
    def canary_latency_metric_details(self) -> "IOperationMetricDetails":
        '''The canary latency metric details.'''
        result = self._values.get("canary_latency_metric_details")
        assert result is not None, "Required property 'canary_latency_metric_details' is missing"
        return typing.cast("IOperationMetricDetails", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanaryMetricProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.CanaryTestMetricsOverrideProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_statistic": "alarmStatistic",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "fault_alarm_threshold": "faultAlarmThreshold",
        "period": "period",
        "success_alarm_threshold": "successAlarmThreshold",
    },
)
class CanaryTestMetricsOverrideProps:
    def __init__(
        self,
        *,
        alarm_statistic: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        fault_alarm_threshold: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        success_alarm_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The properties for creating an override.

        :param alarm_statistic: The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9". Default: - This property will use the default defined for the service
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms. Default: - This property will use the default defined for the service
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms. Default: - This property will use the default defined for the service
        :param fault_alarm_threshold: The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%. Default: - This property will use the default defined for the service
        :param period: The period for the metrics. Default: - This property will use the default defined for the service
        :param success_alarm_threshold: The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%. Default: - This property will use the default defined for the service
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6b739570b1ecc0dd5ae1bb7e43518f9ab0537bdee33a1c174643779b6a45e8)
            check_type(argname="argument alarm_statistic", value=alarm_statistic, expected_type=type_hints["alarm_statistic"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument fault_alarm_threshold", value=fault_alarm_threshold, expected_type=type_hints["fault_alarm_threshold"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument success_alarm_threshold", value=success_alarm_threshold, expected_type=type_hints["success_alarm_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_statistic is not None:
            self._values["alarm_statistic"] = alarm_statistic
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if fault_alarm_threshold is not None:
            self._values["fault_alarm_threshold"] = fault_alarm_threshold
        if period is not None:
            self._values["period"] = period
        if success_alarm_threshold is not None:
            self._values["success_alarm_threshold"] = success_alarm_threshold

    @builtins.property
    def alarm_statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("alarm_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints to alarm on for latency and availability alarms.

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of evaluation periods for latency and availabiltiy alarms.

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fault_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("fault_alarm_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period for the metrics.

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def success_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.

        :default: - This property will use the default defined for the service
        '''
        result = self._values.get("success_alarm_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanaryTestMetricsOverrideProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.ContributorInsightRuleDetailsProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_id_json_path": "availabilityZoneIdJsonPath",
        "fault_metric_json_path": "faultMetricJsonPath",
        "instance_id_json_path": "instanceIdJsonPath",
        "log_groups": "logGroups",
        "operation_name_json_path": "operationNameJsonPath",
        "success_latency_metric_json_path": "successLatencyMetricJsonPath",
    },
)
class ContributorInsightRuleDetailsProps:
    def __init__(
        self,
        *,
        availability_zone_id_json_path: builtins.str,
        fault_metric_json_path: builtins.str,
        instance_id_json_path: builtins.str,
        log_groups: typing.Sequence[_aws_cdk_aws_logs_ceddda9d.ILogGroup],
        operation_name_json_path: builtins.str,
        success_latency_metric_json_path: builtins.str,
    ) -> None:
        '''The contributor insight rule details properties.

        :param availability_zone_id_json_path: The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.
        :param fault_metric_json_path: The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.
        :param instance_id_json_path: The JSON path to the instance id field in the log files, only required for server-side rules.
        :param log_groups: The log groups where CloudWatch logs for the operation are located. If this is not provided, Contributor Insight rules cannot be created.
        :param operation_name_json_path: The path in the log files to the field that identifies the operation the log file is for.
        :param success_latency_metric_json_path: The path in the log files to the field that indicates the latency for the response. This could either be success latency or fault latency depending on the alarms and rules you are creating.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928d51c92a749c4248e6b7fae43ace2d014ae6bd6898d34469f5545cdf0a040)
            check_type(argname="argument availability_zone_id_json_path", value=availability_zone_id_json_path, expected_type=type_hints["availability_zone_id_json_path"])
            check_type(argname="argument fault_metric_json_path", value=fault_metric_json_path, expected_type=type_hints["fault_metric_json_path"])
            check_type(argname="argument instance_id_json_path", value=instance_id_json_path, expected_type=type_hints["instance_id_json_path"])
            check_type(argname="argument log_groups", value=log_groups, expected_type=type_hints["log_groups"])
            check_type(argname="argument operation_name_json_path", value=operation_name_json_path, expected_type=type_hints["operation_name_json_path"])
            check_type(argname="argument success_latency_metric_json_path", value=success_latency_metric_json_path, expected_type=type_hints["success_latency_metric_json_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone_id_json_path": availability_zone_id_json_path,
            "fault_metric_json_path": fault_metric_json_path,
            "instance_id_json_path": instance_id_json_path,
            "log_groups": log_groups,
            "operation_name_json_path": operation_name_json_path,
            "success_latency_metric_json_path": success_latency_metric_json_path,
        }

    @builtins.property
    def availability_zone_id_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.'''
        result = self._values.get("availability_zone_id_json_path")
        assert result is not None, "Required property 'availability_zone_id_json_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fault_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.'''
        result = self._values.get("fault_metric_json_path")
        assert result is not None, "Required property 'fault_metric_json_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id_json_path(self) -> builtins.str:
        '''The JSON path to the instance id field in the log files, only required for server-side rules.'''
        result = self._values.get("instance_id_json_path")
        assert result is not None, "Required property 'instance_id_json_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_groups(self) -> typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log groups where CloudWatch logs for the operation are located.

        If
        this is not provided, Contributor Insight rules cannot be created.
        '''
        result = self._values.get("log_groups")
        assert result is not None, "Required property 'log_groups' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def operation_name_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the operation the log file is for.'''
        result = self._values.get("operation_name_json_path")
        assert result is not None, "Required property 'operation_name_json_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def success_latency_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that indicates the latency for the response.

        This could either be success latency or fault
        latency depending on the alarms and rules you are creating.
        '''
        result = self._values.get("success_latency_metric_json_path")
        assert result is not None, "Required property 'success_latency_metric_json_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContributorInsightRuleDetailsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="multi-az-observability.IAvailabilityZoneMapper")
class IAvailabilityZoneMapper(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''A wrapper for the Availability Zone mapper construct that allows you to translate Availability Zone names to Availability Zone Ids and vice a versa using the mapping in the AWS account where this is deployed.'''

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The function that does the mapping.'''
        ...

    @function.setter
    def function(self, value: _aws_cdk_aws_lambda_ceddda9d.IFunction) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group for the function's logs.'''
        ...

    @log_group.setter
    def log_group(self, value: _aws_cdk_aws_logs_ceddda9d.ILogGroup) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="mapper")
    def mapper(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''The custom resource that can be referenced to use Fn::GetAtt functions on to retrieve availability zone names and ids.'''
        ...

    @mapper.setter
    def mapper(self, value: _aws_cdk_ceddda9d.CustomResource) -> None:
        ...

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsArray")
    def all_availability_zone_ids_as_array(self) -> _aws_cdk_ceddda9d.Reference:
        '''Returns a reference that can be cast to a string array with all of the Availability Zone Ids.'''
        ...

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsCommaDelimitedList")
    def all_availability_zone_ids_as_comma_delimited_list(self) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id
        '''
        ...

    @jsii.member(jsii_name="allAvailabilityZoneNamesAsCommaDelimitedList")
    def all_availability_zone_names_as_comma_delimited_list(self) -> builtins.str:
        '''Gets all of the Availability Zone names in this Region as a comma delimited list.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Name
        '''
        ...

    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(
        self,
        availability_zone_name: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Id for the given Availability Zone Name in this account.

        :param availability_zone_name: -
        '''
        ...

    @jsii.member(jsii_name="availabilityZoneIdFromAvailabilityZoneLetter")
    def availability_zone_id_from_availability_zone_letter(
        self,
        letter: builtins.str,
    ) -> builtins.str:
        '''Given a letter like "f" or "a", returns the Availability Zone Id for that Availability Zone name in this account.

        :param letter: -
        '''
        ...

    @jsii.member(jsii_name="availabilityZoneIdsAsArray")
    def availability_zone_ids_as_array(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> typing.List[builtins.str]:
        '''Returns an array for Availability Zone Ids for the supplied Availability Zone names, they are returned in the same order the names were provided.

        :param availability_zone_names: -
        '''
        ...

    @jsii.member(jsii_name="availabilityZoneIdsAsCommaDelimitedList")
    def availability_zone_ids_as_comma_delimited_list(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id

        :param availability_zone_names: -
        '''
        ...

    @jsii.member(jsii_name="availabilityZoneName")
    def availability_zone_name(
        self,
        availability_zone_id: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Name for the given Availability Zone Id in this account.

        :param availability_zone_id: -
        '''
        ...

    @jsii.member(jsii_name="regionPrefixForAvailabilityZoneIds")
    def region_prefix_for_availability_zone_ids(self) -> builtins.str:
        '''Gets the prefix for the region used with Availability Zone Ids, for example in us-east-1, this returns "use1".'''
        ...


class _IAvailabilityZoneMapperProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''A wrapper for the Availability Zone mapper construct that allows you to translate Availability Zone names to Availability Zone Ids and vice a versa using the mapping in the AWS account where this is deployed.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IAvailabilityZoneMapper"

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The function that does the mapping.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))

    @function.setter
    def function(self, value: _aws_cdk_aws_lambda_ceddda9d.IFunction) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef15425f4b53258b8a7fee384baa9e4b26d617de1a46e56aa7ce30e5a4b29d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group for the function's logs.'''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: _aws_cdk_aws_logs_ceddda9d.ILogGroup) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c31c9fd1728244a4034a26db6d199f09ec0bff3d04796990d4e5baef0044fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapper")
    def mapper(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''The custom resource that can be referenced to use Fn::GetAtt functions on to retrieve availability zone names and ids.'''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "mapper"))

    @mapper.setter
    def mapper(self, value: _aws_cdk_ceddda9d.CustomResource) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdf4b5c85f9b4b6174b5ab3e84d47061a4a97fe351e51bce1ac911b3cf0061b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapper", value) # pyright: ignore[reportArgumentType]

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsArray")
    def all_availability_zone_ids_as_array(self) -> _aws_cdk_ceddda9d.Reference:
        '''Returns a reference that can be cast to a string array with all of the Availability Zone Ids.'''
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "allAvailabilityZoneIdsAsArray", []))

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsCommaDelimitedList")
    def all_availability_zone_ids_as_comma_delimited_list(self) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "allAvailabilityZoneIdsAsCommaDelimitedList", []))

    @jsii.member(jsii_name="allAvailabilityZoneNamesAsCommaDelimitedList")
    def all_availability_zone_names_as_comma_delimited_list(self) -> builtins.str:
        '''Gets all of the Availability Zone names in this Region as a comma delimited list.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Name
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "allAvailabilityZoneNamesAsCommaDelimitedList", []))

    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(
        self,
        availability_zone_name: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Id for the given Availability Zone Name in this account.

        :param availability_zone_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de18979b5bc3fcfd30bce0f73b892dbfd338671e9cd2174b608ac2ef41387108)
            check_type(argname="argument availability_zone_name", value=availability_zone_name, expected_type=type_hints["availability_zone_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneId", [availability_zone_name]))

    @jsii.member(jsii_name="availabilityZoneIdFromAvailabilityZoneLetter")
    def availability_zone_id_from_availability_zone_letter(
        self,
        letter: builtins.str,
    ) -> builtins.str:
        '''Given a letter like "f" or "a", returns the Availability Zone Id for that Availability Zone name in this account.

        :param letter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918cea02a7a8c8236a47216fd967f551b424b708cc0a0d85643145178326f10d)
            check_type(argname="argument letter", value=letter, expected_type=type_hints["letter"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneIdFromAvailabilityZoneLetter", [letter]))

    @jsii.member(jsii_name="availabilityZoneIdsAsArray")
    def availability_zone_ids_as_array(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> typing.List[builtins.str]:
        '''Returns an array for Availability Zone Ids for the supplied Availability Zone names, they are returned in the same order the names were provided.

        :param availability_zone_names: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a969f2acb8541c226aff52f673143ec2267780a385a6a4fddf08d234160bfa3c)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "availabilityZoneIdsAsArray", [availability_zone_names]))

    @jsii.member(jsii_name="availabilityZoneIdsAsCommaDelimitedList")
    def availability_zone_ids_as_comma_delimited_list(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id

        :param availability_zone_names: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030ef2a67c593ef76c9032ba6818f14ff588183846df4d3bf9eafe05f85cbc92)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneIdsAsCommaDelimitedList", [availability_zone_names]))

    @jsii.member(jsii_name="availabilityZoneName")
    def availability_zone_name(
        self,
        availability_zone_id: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Name for the given Availability Zone Id in this account.

        :param availability_zone_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc7f0c8bc56783d26fef73e3aa44e78135e00fa8e48244cfd5417513d772f93)
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneName", [availability_zone_id]))

    @jsii.member(jsii_name="regionPrefixForAvailabilityZoneIds")
    def region_prefix_for_availability_zone_ids(self) -> builtins.str:
        '''Gets the prefix for the region used with Availability Zone Ids, for example in us-east-1, this returns "use1".'''
        return typing.cast(builtins.str, jsii.invoke(self, "regionPrefixForAvailabilityZoneIds", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAvailabilityZoneMapper).__jsii_proxy_class__ = lambda : _IAvailabilityZoneMapperProxy


@jsii.interface(jsii_type="multi-az-observability.IBasicServiceMultiAZObservability")
class IBasicServiceMultiAZObservability(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''Properties of a basic service.'''

    @builtins.property
    @jsii.member(jsii_name="aggregateZonalIsolatedImpactAlarms")
    def aggregate_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The alarms indicating if an AZ has isolated impact from either ALB or NAT GW metrics.'''
        ...

    @aggregate_zonal_isolated_impact_alarms.setter
    def aggregate_zonal_isolated_impact_alarms(
        self,
        value: typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of the service.'''
        ...

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="albZonalIsolatedImpactAlarms")
    def alb_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for ALB faults and has isolated impact.'''
        ...

    @alb_zonal_isolated_impact_alarms.setter
    def alb_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationLoadBalancers")
    def application_load_balancers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]]:
        '''The application load balancers being used by the service.'''
        ...

    @application_load_balancers.setter
    def application_load_balancers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]]:
        '''The NAT Gateways being used in the service, each set of NAT Gateways are keyed by their Availability Zone Id.'''
        ...

    @nat_gateways.setter
    def nat_gateways(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="natGWZonalIsolatedImpactAlarms")
    def nat_gw_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for NAT GW packet loss and has isolated impact.'''
        ...

    @nat_gw_zonal_isolated_impact_alarms.setter
    def nat_gw_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        ...


class _IBasicServiceMultiAZObservabilityProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Properties of a basic service.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IBasicServiceMultiAZObservability"

    @builtins.property
    @jsii.member(jsii_name="aggregateZonalIsolatedImpactAlarms")
    def aggregate_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The alarms indicating if an AZ has isolated impact from either ALB or NAT GW metrics.'''
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "aggregateZonalIsolatedImpactAlarms"))

    @aggregate_zonal_isolated_impact_alarms.setter
    def aggregate_zonal_isolated_impact_alarms(
        self,
        value: typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da8d7df1ecf8a83ea92bbac9f862e0a3e70c859e8a1bf5c423f00a98bde0158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregateZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of the service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e600397d75137d2e977180f7907ce6924e8b754bfcf018df4e79d7a6396bcbdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="albZonalIsolatedImpactAlarms")
    def alb_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for ALB faults and has isolated impact.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "albZonalIsolatedImpactAlarms"))

    @alb_zonal_isolated_impact_alarms.setter
    def alb_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9699df8dc509d1cae25263f3edb070e0c0d45c937afd99759d98277e85efb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "albZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationLoadBalancers")
    def application_load_balancers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]]:
        '''The application load balancers being used by the service.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]], jsii.get(self, "applicationLoadBalancers"))

    @application_load_balancers.setter
    def application_load_balancers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0eab8db5587e70b721058fb0c3b9b12ab74016f9e83fdc74e086cfbd34f766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationLoadBalancers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]]:
        '''The NAT Gateways being used in the service, each set of NAT Gateways are keyed by their Availability Zone Id.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]], jsii.get(self, "natGateways"))

    @nat_gateways.setter
    def nat_gateways(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c77fecc2592ab95dae42a3cba29f05b42a3746148a483ee8438d00b23cc35ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGateways", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natGWZonalIsolatedImpactAlarms")
    def nat_gw_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for NAT GW packet loss and has isolated impact.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "natGWZonalIsolatedImpactAlarms"))

    @nat_gw_zonal_isolated_impact_alarms.setter
    def nat_gw_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9d785bf0c641fffc85e06501ae14ba6754f0663649bdb005dfa5eb936482af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGWZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBasicServiceMultiAZObservability).__jsii_proxy_class__ = lambda : _IBasicServiceMultiAZObservabilityProxy


@jsii.interface(jsii_type="multi-az-observability.ICanaryMetrics")
class ICanaryMetrics(typing_extensions.Protocol):
    '''The metric definitions for metric produced by the canary.'''

    @builtins.property
    @jsii.member(jsii_name="canaryAvailabilityMetricDetails")
    def canary_availability_metric_details(self) -> "IOperationMetricDetails":
        '''The canary availability metric details.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryLatencyMetricDetails")
    def canary_latency_metric_details(self) -> "IOperationMetricDetails":
        '''The canary latency metric details.'''
        ...


class _ICanaryMetricsProxy:
    '''The metric definitions for metric produced by the canary.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.ICanaryMetrics"

    @builtins.property
    @jsii.member(jsii_name="canaryAvailabilityMetricDetails")
    def canary_availability_metric_details(self) -> "IOperationMetricDetails":
        '''The canary availability metric details.'''
        return typing.cast("IOperationMetricDetails", jsii.get(self, "canaryAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="canaryLatencyMetricDetails")
    def canary_latency_metric_details(self) -> "IOperationMetricDetails":
        '''The canary latency metric details.'''
        return typing.cast("IOperationMetricDetails", jsii.get(self, "canaryLatencyMetricDetails"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICanaryMetrics).__jsii_proxy_class__ = lambda : _ICanaryMetricsProxy


@jsii.interface(jsii_type="multi-az-observability.ICanaryTestMetricsOverride")
class ICanaryTestMetricsOverride(typing_extensions.Protocol):
    '''Provides overrides for the default metric settings used for the automatically created canary tests.'''

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        ...

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period for the metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        ...


class _ICanaryTestMetricsOverrideProxy:
    '''Provides overrides for the default metric settings used for the automatically created canary tests.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.ICanaryTestMetricsOverride"

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period for the metrics.'''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successAlarmThreshold"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICanaryTestMetricsOverride).__jsii_proxy_class__ = lambda : _ICanaryTestMetricsOverrideProxy


@jsii.interface(jsii_type="multi-az-observability.IContributorInsightRuleDetails")
class IContributorInsightRuleDetails(typing_extensions.Protocol):
    '''Details for setting up Contributor Insight rules.'''

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdJsonPath")
    def availability_zone_id_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultMetricJsonPath")
    def fault_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdJsonPath")
    def instance_id_json_path(self) -> builtins.str:
        '''The JSON path to the instance id field in the log files, only required for server-side rules.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroups")
    def log_groups(self) -> typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log groups where CloudWatch logs for the operation are located.

        If
        this is not provided, Contributor Insight rules cannot be created.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="operationNameJsonPath")
    def operation_name_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the operation the log file is for.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successLatencyMetricJsonPath")
    def success_latency_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that indicates the latency for the response.

        This could either be success latency or fault
        latency depending on the alarms and rules you are creating.
        '''
        ...


class _IContributorInsightRuleDetailsProxy:
    '''Details for setting up Contributor Insight rules.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IContributorInsightRuleDetails"

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdJsonPath")
    def availability_zone_id_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneIdJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricJsonPath")
    def fault_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.'''
        return typing.cast(builtins.str, jsii.get(self, "faultMetricJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdJsonPath")
    def instance_id_json_path(self) -> builtins.str:
        '''The JSON path to the instance id field in the log files, only required for server-side rules.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="logGroups")
    def log_groups(self) -> typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log groups where CloudWatch logs for the operation are located.

        If
        this is not provided, Contributor Insight rules cannot be created.
        '''
        return typing.cast(typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup], jsii.get(self, "logGroups"))

    @builtins.property
    @jsii.member(jsii_name="operationNameJsonPath")
    def operation_name_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the operation the log file is for.'''
        return typing.cast(builtins.str, jsii.get(self, "operationNameJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="successLatencyMetricJsonPath")
    def success_latency_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that indicates the latency for the response.

        This could either be success latency or fault
        latency depending on the alarms and rules you are creating.
        '''
        return typing.cast(builtins.str, jsii.get(self, "successLatencyMetricJsonPath"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IContributorInsightRuleDetails).__jsii_proxy_class__ = lambda : _IContributorInsightRuleDetailsProxy


@jsii.interface(
    jsii_type="multi-az-observability.IInstrumentedServiceMultiAZObservability"
)
class IInstrumentedServiceMultiAZObservability(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''Observability for an instrumented service.'''

    @builtins.property
    @jsii.member(jsii_name="perOperationZonalImpactAlarms")
    def per_operation_zonal_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''Index into the dictionary by operation name, then by Availability Zone Id to get the alarms that indicate an AZ shows isolated impact from availability or latency as seen by either the server-side or canary.

        These are the alarms
        you would want to use to trigger automation to evacuate an AZ.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceAlarms")
    def service_alarms(self) -> "IServiceAlarmsAndRules":
        '''The alarms and rules for the overall service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryLogGroup")
    def canary_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''If the service is configured to have canary tests created, this will be the log group where the canary's logs are stored.

        :default: - No log group is created if the canary is not requested.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="operationDashboards")
    def operation_dashboards(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]]:
        '''The dashboards for each operation.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceDashboard")
    def service_dashboard(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]:
        '''The service level dashboard.'''
        ...


class _IInstrumentedServiceMultiAZObservabilityProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Observability for an instrumented service.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IInstrumentedServiceMultiAZObservability"

    @builtins.property
    @jsii.member(jsii_name="perOperationZonalImpactAlarms")
    def per_operation_zonal_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''Index into the dictionary by operation name, then by Availability Zone Id to get the alarms that indicate an AZ shows isolated impact from availability or latency as seen by either the server-side or canary.

        These are the alarms
        you would want to use to trigger automation to evacuate an AZ.
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "perOperationZonalImpactAlarms"))

    @builtins.property
    @jsii.member(jsii_name="serviceAlarms")
    def service_alarms(self) -> "IServiceAlarmsAndRules":
        '''The alarms and rules for the overall service.'''
        return typing.cast("IServiceAlarmsAndRules", jsii.get(self, "serviceAlarms"))

    @builtins.property
    @jsii.member(jsii_name="canaryLogGroup")
    def canary_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''If the service is configured to have canary tests created, this will be the log group where the canary's logs are stored.

        :default: - No log group is created if the canary is not requested.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], jsii.get(self, "canaryLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="operationDashboards")
    def operation_dashboards(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]]:
        '''The dashboards for each operation.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]], jsii.get(self, "operationDashboards"))

    @builtins.property
    @jsii.member(jsii_name="serviceDashboard")
    def service_dashboard(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]:
        '''The service level dashboard.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard], jsii.get(self, "serviceDashboard"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstrumentedServiceMultiAZObservability).__jsii_proxy_class__ = lambda : _IInstrumentedServiceMultiAZObservabilityProxy


@jsii.interface(jsii_type="multi-az-observability.IOperation")
class IOperation(typing_extensions.Protocol):
    '''Represents an operation in a service.'''

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> builtins.bool:
        '''Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(self) -> typing.List[builtins.str]:
        '''The http methods supported by the operation.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The name of the operation.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''The HTTP path for the operation for canaries to run against, something like "/products/list".'''
        ...

    @builtins.property
    @jsii.member(jsii_name="serverSideAvailabilityMetricDetails")
    def server_side_availability_metric_details(self) -> "IOperationMetricDetails":
        '''The server side availability metric details.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="serverSideLatencyMetricDetails")
    def server_side_latency_metric_details(self) -> "IOperationMetricDetails":
        '''The server side latency metric details.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        '''The service the operation is associated with.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryMetricDetails")
    def canary_metric_details(self) -> typing.Optional[ICanaryMetrics]:
        '''Optional metric details if the service has an existing canary.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryTestAvailabilityMetricsOverride")
    def canary_test_availability_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryTestLatencyMetricsOverride")
    def canary_test_latency_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''If they have been added, the properties for creating new canary tests on this operation.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="optOutOfServiceCreatedCanary")
    def opt_out_of_service_created_canary(self) -> typing.Optional[builtins.bool]:
        '''Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation.

        :default: - The operation is not opted out
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serverSideContributorInsightRuleDetails")
    def server_side_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The server side details for contributor insights rules.'''
        ...


class _IOperationProxy:
    '''Represents an operation in a service.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IOperation"

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> builtins.bool:
        '''Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.'''
        return typing.cast(builtins.bool, jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(self) -> typing.List[builtins.str]:
        '''The http methods supported by the operation.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The name of the operation.'''
        return typing.cast(builtins.str, jsii.get(self, "operationName"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''The HTTP path for the operation for canaries to run against, something like "/products/list".'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="serverSideAvailabilityMetricDetails")
    def server_side_availability_metric_details(self) -> "IOperationMetricDetails":
        '''The server side availability metric details.'''
        return typing.cast("IOperationMetricDetails", jsii.get(self, "serverSideAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="serverSideLatencyMetricDetails")
    def server_side_latency_metric_details(self) -> "IOperationMetricDetails":
        '''The server side latency metric details.'''
        return typing.cast("IOperationMetricDetails", jsii.get(self, "serverSideLatencyMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        '''The service the operation is associated with.'''
        return typing.cast("IService", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="canaryMetricDetails")
    def canary_metric_details(self) -> typing.Optional[ICanaryMetrics]:
        '''Optional metric details if the service has an existing canary.'''
        return typing.cast(typing.Optional[ICanaryMetrics], jsii.get(self, "canaryMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestAvailabilityMetricsOverride")
    def canary_test_availability_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability.'''
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], jsii.get(self, "canaryTestAvailabilityMetricsOverride"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestLatencyMetricsOverride")
    def canary_test_latency_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency.'''
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], jsii.get(self, "canaryTestLatencyMetricsOverride"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''If they have been added, the properties for creating new canary tests on this operation.'''
        return typing.cast(typing.Optional[AddCanaryTestProps], jsii.get(self, "canaryTestProps"))

    @builtins.property
    @jsii.member(jsii_name="optOutOfServiceCreatedCanary")
    def opt_out_of_service_created_canary(self) -> typing.Optional[builtins.bool]:
        '''Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation.

        :default: - The operation is not opted out
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "optOutOfServiceCreatedCanary"))

    @builtins.property
    @jsii.member(jsii_name="serverSideContributorInsightRuleDetails")
    def server_side_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The server side details for contributor insights rules.'''
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], jsii.get(self, "serverSideContributorInsightRuleDetails"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOperation).__jsii_proxy_class__ = lambda : _IOperationProxy


@jsii.interface(jsii_type="multi-az-observability.IOperationMetricDetails")
class IOperationMetricDetails(typing_extensions.Protocol):
    '''Details for operation metrics in one perspective, such as server side latency.'''

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        ...

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="metricDimensions")
    def metric_dimensions(self) -> "MetricDimensions":
        '''The metric dimensions for this operation, must be implemented as a concrete class by the user.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The operation these metric details are for.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        ...


class _IOperationMetricDetailsProxy:
    '''Details for operation metrics in one perspective, such as server side latency.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IOperationMetricDetails"

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(builtins.str, jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(jsii.Number, jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "faultMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="metricDimensions")
    def metric_dimensions(self) -> "MetricDimensions":
        '''The metric dimensions for this operation, must be implemented as a concrete class by the user.'''
        return typing.cast("MetricDimensions", jsii.get(self, "metricDimensions"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The operation these metric details are for.'''
        return typing.cast(builtins.str, jsii.get(self, "operationName"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(jsii.Number, jsii.get(self, "successAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "successMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Unit, jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedFaultStatistics"))

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedSuccessStatistics"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOperationMetricDetails).__jsii_proxy_class__ = lambda : _IOperationMetricDetailsProxy


@jsii.interface(jsii_type="multi-az-observability.IService")
class IService(typing_extensions.Protocol):
    '''Represents a complete service composed of one or more operations.'''

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneNames")
    def availability_zone_names(self) -> typing.List[builtins.str]:
        '''A list of the Availability Zone names used by this application.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        '''The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultAvailabilityMetricDetails")
    def default_availability_metric_details(self) -> "IServiceMetricDetails":
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultLatencyMetricDetails")
    def default_latency_metric_details(self) -> "IServiceMetricDetails":
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultCountThreshold")
    def fault_count_threshold(self) -> jsii.Number:
        '''The fault count threshold that indicates the service is unhealthy.

        This is an absolute value of faults
        being produced by all critical operations in aggregate.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[IOperation]:
        '''The operations that are part of this service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for which metrics for the service should be aggregated.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of your service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''Define these settings if you want to automatically add canary tests to your operations.

        Operations can individually opt out
        of canary test creation if you define this setting.

        :default:

        - Automatic canary tests will not be created for
        operations in this service.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultContributorInsightRuleDetails")
    def default_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The default settings that are used for contributor insight rules.

        :default: - No defaults are provided and must be specified per operation
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2]:
        '''The load balancer this service sits behind.

        :default:

        - No load balancer metrics are included in
        dashboards and its ARN is not added to top level AZ
        alarm descriptions.
        '''
        ...

    @jsii.member(jsii_name="addOperation")
    def add_operation(self, operation: IOperation) -> None:
        '''Adds an operation to this service.

        :param operation: -
        '''
        ...


class _IServiceProxy:
    '''Represents a complete service composed of one or more operations.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IService"

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneNames")
    def availability_zone_names(self) -> typing.List[builtins.str]:
        '''A list of the Availability Zone names used by this application.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZoneNames"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        '''The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.'''
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @builtins.property
    @jsii.member(jsii_name="defaultAvailabilityMetricDetails")
    def default_availability_metric_details(self) -> "IServiceMetricDetails":
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        return typing.cast("IServiceMetricDetails", jsii.get(self, "defaultAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="defaultLatencyMetricDetails")
    def default_latency_metric_details(self) -> "IServiceMetricDetails":
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        return typing.cast("IServiceMetricDetails", jsii.get(self, "defaultLatencyMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="faultCountThreshold")
    def fault_count_threshold(self) -> jsii.Number:
        '''The fault count threshold that indicates the service is unhealthy.

        This is an absolute value of faults
        being produced by all critical operations in aggregate.
        '''
        return typing.cast(jsii.Number, jsii.get(self, "faultCountThreshold"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[IOperation]:
        '''The operations that are part of this service.'''
        return typing.cast(typing.List[IOperation], jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for which metrics for the service should be aggregated.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of your service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''Define these settings if you want to automatically add canary tests to your operations.

        Operations can individually opt out
        of canary test creation if you define this setting.

        :default:

        - Automatic canary tests will not be created for
        operations in this service.
        '''
        return typing.cast(typing.Optional[AddCanaryTestProps], jsii.get(self, "canaryTestProps"))

    @builtins.property
    @jsii.member(jsii_name="defaultContributorInsightRuleDetails")
    def default_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The default settings that are used for contributor insight rules.

        :default: - No defaults are provided and must be specified per operation
        '''
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], jsii.get(self, "defaultContributorInsightRuleDetails"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2]:
        '''The load balancer this service sits behind.

        :default:

        - No load balancer metrics are included in
        dashboards and its ARN is not added to top level AZ
        alarm descriptions.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2], jsii.get(self, "loadBalancer"))

    @jsii.member(jsii_name="addOperation")
    def add_operation(self, operation: IOperation) -> None:
        '''Adds an operation to this service.

        :param operation: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bde07ece32c22e2ed407a2bd209e7524e6cff22e9de936befaa0909e4557fb)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        return typing.cast(None, jsii.invoke(self, "addOperation", [operation]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.interface(jsii_type="multi-az-observability.IServiceAlarmsAndRules")
class IServiceAlarmsAndRules(typing_extensions.Protocol):
    '''Service level alarms and rules using critical operations.'''

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityOrLatencyServerSideAlarm")
    def regional_availability_or_latency_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for regional availability or latency impact of any critical operation as measured by the server-side.'''
        ...

    @regional_availability_or_latency_server_side_alarm.setter
    def regional_availability_or_latency_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityServerSideAlarm")
    def regional_availability_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for regional availability impact of any critical operation as measured by the server-side.'''
        ...

    @regional_availability_server_side_alarm.setter
    def regional_availability_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalFaultCountServerSideAlarm")
    def regional_fault_count_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for fault count exceeding a regional threshold for all critical operations.'''
        ...

    @regional_fault_count_server_side_alarm.setter
    def regional_fault_count_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The service these alarms and rules are for.'''
        ...

    @service.setter
    def service(self, value: IService) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="zonalAggregateIsolatedImpactAlarms")
    def zonal_aggregate_isolated_impact_alarms(
        self,
    ) -> typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The zonal aggregate isolated impact alarms.

        There is 1 alarm per AZ that
        triggers for availability or latency impact to any critical operation in that AZ
        that indicates it has isolated impact as measured by canaries or server-side.
        '''
        ...

    @zonal_aggregate_isolated_impact_alarms.setter
    def zonal_aggregate_isolated_impact_alarms(
        self,
        value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="zonalServerSideIsolatedImpactAlarms")
    def zonal_server_side_isolated_impact_alarms(
        self,
    ) -> typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The zonal server-side isolated impact alarms.

        There is 1 alarm per AZ that triggers
        on availability or atency impact to any critical operation in that AZ. These are useful
        for deployment monitoring to not inadvertently fail when a canary can't contact an AZ
        during a deployment.
        '''
        ...

    @zonal_server_side_isolated_impact_alarms.setter
    def zonal_server_side_isolated_impact_alarms(
        self,
        value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityCanaryAlarm")
    def regional_availability_canary_alarm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''An alarm for regional availability impact of any critical operation as measured by the canary.'''
        ...

    @regional_availability_canary_alarm.setter
    def regional_availability_canary_alarm(
        self,
        value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityOrLatencyCanaryAlarm")
    def regional_availability_or_latency_canary_alarm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''An alarm for regional availability or latency impact of any critical operation as measured by the canary.'''
        ...

    @regional_availability_or_latency_canary_alarm.setter
    def regional_availability_or_latency_canary_alarm(
        self,
        value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        ...


class _IServiceAlarmsAndRulesProxy:
    '''Service level alarms and rules using critical operations.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IServiceAlarmsAndRules"

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityOrLatencyServerSideAlarm")
    def regional_availability_or_latency_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for regional availability or latency impact of any critical operation as measured by the server-side.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm, jsii.get(self, "regionalAvailabilityOrLatencyServerSideAlarm"))

    @regional_availability_or_latency_server_side_alarm.setter
    def regional_availability_or_latency_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8626bf78b2e0e32e118334d17c1e620cf433211d5939817daa86d322b2191b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalAvailabilityOrLatencyServerSideAlarm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityServerSideAlarm")
    def regional_availability_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for regional availability impact of any critical operation as measured by the server-side.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm, jsii.get(self, "regionalAvailabilityServerSideAlarm"))

    @regional_availability_server_side_alarm.setter
    def regional_availability_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f953b292bd0ef9e32eb4dceb7a72cabb187dd71dcaf0a427359258f774229d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalAvailabilityServerSideAlarm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionalFaultCountServerSideAlarm")
    def regional_fault_count_server_side_alarm(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''An alarm for fault count exceeding a regional threshold for all critical operations.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm, jsii.get(self, "regionalFaultCountServerSideAlarm"))

    @regional_fault_count_server_side_alarm.setter
    def regional_fault_count_server_side_alarm(
        self,
        value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f807c1960ac162df87afc2feba30c47a91d0af00d78bda7a2fa0459180c1ed93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalFaultCountServerSideAlarm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The service these alarms and rules are for.'''
        return typing.cast(IService, jsii.get(self, "service"))

    @service.setter
    def service(self, value: IService) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc293180ad805fbcb81ccd21086bb19e1bb36c6fa11a9bc231ac5dd4edb0e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zonalAggregateIsolatedImpactAlarms")
    def zonal_aggregate_isolated_impact_alarms(
        self,
    ) -> typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The zonal aggregate isolated impact alarms.

        There is 1 alarm per AZ that
        triggers for availability or latency impact to any critical operation in that AZ
        that indicates it has isolated impact as measured by canaries or server-side.
        '''
        return typing.cast(typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "zonalAggregateIsolatedImpactAlarms"))

    @zonal_aggregate_isolated_impact_alarms.setter
    def zonal_aggregate_isolated_impact_alarms(
        self,
        value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baf67c32f5dbd43108c4cab5d950436bc928c5c7f155fe0d74070c41cdb3dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zonalAggregateIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zonalServerSideIsolatedImpactAlarms")
    def zonal_server_side_isolated_impact_alarms(
        self,
    ) -> typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The zonal server-side isolated impact alarms.

        There is 1 alarm per AZ that triggers
        on availability or atency impact to any critical operation in that AZ. These are useful
        for deployment monitoring to not inadvertently fail when a canary can't contact an AZ
        during a deployment.
        '''
        return typing.cast(typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "zonalServerSideIsolatedImpactAlarms"))

    @zonal_server_side_isolated_impact_alarms.setter
    def zonal_server_side_isolated_impact_alarms(
        self,
        value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00de5a388f5dc72443906156fb11ab31d9a2aa725f6682a0da502b7ae776045e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zonalServerSideIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityCanaryAlarm")
    def regional_availability_canary_alarm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''An alarm for regional availability impact of any critical operation as measured by the canary.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "regionalAvailabilityCanaryAlarm"))

    @regional_availability_canary_alarm.setter
    def regional_availability_canary_alarm(
        self,
        value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2274d795072407a74901eb5921d753f3d8a0702daab149426e8d5487a1379f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalAvailabilityCanaryAlarm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionalAvailabilityOrLatencyCanaryAlarm")
    def regional_availability_or_latency_canary_alarm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''An alarm for regional availability or latency impact of any critical operation as measured by the canary.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "regionalAvailabilityOrLatencyCanaryAlarm"))

    @regional_availability_or_latency_canary_alarm.setter
    def regional_availability_or_latency_canary_alarm(
        self,
        value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fb5ac43ab62a6bd0808b3b73124460d735c87caeb435f8a55050e78d9bf5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalAvailabilityOrLatencyCanaryAlarm", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceAlarmsAndRules).__jsii_proxy_class__ = lambda : _IServiceAlarmsAndRulesProxy


@jsii.interface(jsii_type="multi-az-observability.IServiceMetricDetails")
class IServiceMetricDetails(typing_extensions.Protocol):
    '''Details for the defaults used in a service for metrics in one perspective, such as server side latency.'''

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        ...

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        ...


class _IServiceMetricDetailsProxy:
    '''Details for the defaults used in a service for metrics in one perspective, such as server side latency.'''

    __jsii_type__: typing.ClassVar[str] = "multi-az-observability.IServiceMetricDetails"

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(builtins.str, jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(jsii.Number, jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "faultMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(jsii.Number, jsii.get(self, "successAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "successMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Unit, jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedFaultStatistics"))

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedSuccessStatistics"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceMetricDetails).__jsii_proxy_class__ = lambda : _IServiceMetricDetailsProxy


@jsii.implements(IInstrumentedServiceMultiAZObservability)
class InstrumentedServiceMultiAZObservability(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.InstrumentedServiceMultiAZObservability",
):
    '''An service that implements its own instrumentation to record availability and latency metrics that can be used to create alarms, rules, and dashboards from.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        outlier_detection_algorithm: "OutlierDetectionAlgorithm",
        service: IService,
        assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
        assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
        create_dashboards: typing.Optional[builtins.bool] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        outlier_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param outlier_detection_algorithm: The algorithm to use for performing outlier detection.
        :param service: The service that the alarms and dashboards are being crated for.
        :param assets_bucket_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket location CDK provides by default for bundled assets. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - The assets will be uploaded to the default defined asset location.
        :param assets_bucket_prefix_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket prefix CDK provides by default for bundled assets. This property only takes effect if you defined the assetsBucketParameterName. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - No object prefix will be added to your custom assets location. However, if you have overridden something like the 'BucketPrefix' property in your stack synthesizer with a variable like "${AssetsBucketPrefix", you will need to define this property so it doesn't cause a reference error even if the prefix value is blank.
        :param create_dashboards: Indicates whether to create per operation and overall service dashboards. Default: - No dashboards are created
        :param interval: The interval used in the dashboard, defaults to 60 minutes. Default: - 60 minutes
        :param outlier_threshold: The outlier threshold for determining if an AZ is an outlier for latency or faults. This number is interpreted differently for different outlier algorithms. When used with STATIC, the number should be between 0 and 1 to represent the percentage of errors (like .7) that an AZ must be responsible for to be considered an outlier. When used with CHI_SQUARED, it represents the p value that indicates statistical significance, like 0.05 which means the skew has less than or equal to a 5% chance of occuring. When used with Z_SCORE it indicates how many standard deviations to evaluate for an AZ being an outlier, typically 3 is standard for Z_SCORE. Standard defaults based on the outlier detection algorithm: STATIC: 0.7 CHI_SQUARED: 0.05 Z_SCORE: 2 IQR: 1.5 MAD: 3 Default: - Depends on the outlier detection algorithm selected
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e3399e5b1fb72c387324d7303207d55300674a9aceeda9884cbd2c515a112d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InstrumentedServiceMultiAZObservabilityProps(
            outlier_detection_algorithm=outlier_detection_algorithm,
            service=service,
            assets_bucket_parameter_name=assets_bucket_parameter_name,
            assets_bucket_prefix_parameter_name=assets_bucket_prefix_parameter_name,
            create_dashboards=create_dashboards,
            interval=interval,
            outlier_threshold=outlier_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="perOperationZonalImpactAlarms")
    def per_operation_zonal_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''Index into the dictionary by operation name, then by Availability Zone Id to get the alarms that indicate an AZ shows isolated impact from availability or latency as seen by either the server-side or canary.

        These are the alarms
        you would want to use to trigger automation to evacuate an AZ.
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "perOperationZonalImpactAlarms"))

    @builtins.property
    @jsii.member(jsii_name="serviceAlarms")
    def service_alarms(self) -> IServiceAlarmsAndRules:
        '''The alarms and rules for the overall service.'''
        return typing.cast(IServiceAlarmsAndRules, jsii.get(self, "serviceAlarms"))

    @builtins.property
    @jsii.member(jsii_name="canaryLogGroup")
    def canary_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''If the service is configured to have canary tests created, this will be the log group where the canary's logs are stored.

        :default: - No log group is created if the canary is not requested.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], jsii.get(self, "canaryLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="operationDashboards")
    def operation_dashboards(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]]:
        '''The dashboards for each operation.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]], jsii.get(self, "operationDashboards"))

    @builtins.property
    @jsii.member(jsii_name="serviceDashboard")
    def service_dashboard(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]:
        '''The service level dashboard.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard], jsii.get(self, "serviceDashboard"))


@jsii.data_type(
    jsii_type="multi-az-observability.InstrumentedServiceMultiAZObservabilityProps",
    jsii_struct_bases=[],
    name_mapping={
        "outlier_detection_algorithm": "outlierDetectionAlgorithm",
        "service": "service",
        "assets_bucket_parameter_name": "assetsBucketParameterName",
        "assets_bucket_prefix_parameter_name": "assetsBucketPrefixParameterName",
        "create_dashboards": "createDashboards",
        "interval": "interval",
        "outlier_threshold": "outlierThreshold",
    },
)
class InstrumentedServiceMultiAZObservabilityProps:
    def __init__(
        self,
        *,
        outlier_detection_algorithm: "OutlierDetectionAlgorithm",
        service: IService,
        assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
        assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
        create_dashboards: typing.Optional[builtins.bool] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        outlier_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The properties for adding alarms and dashboards for an instrumented service.

        :param outlier_detection_algorithm: The algorithm to use for performing outlier detection.
        :param service: The service that the alarms and dashboards are being crated for.
        :param assets_bucket_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket location CDK provides by default for bundled assets. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - The assets will be uploaded to the default defined asset location.
        :param assets_bucket_prefix_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket prefix CDK provides by default for bundled assets. This property only takes effect if you defined the assetsBucketParameterName. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - No object prefix will be added to your custom assets location. However, if you have overridden something like the 'BucketPrefix' property in your stack synthesizer with a variable like "${AssetsBucketPrefix", you will need to define this property so it doesn't cause a reference error even if the prefix value is blank.
        :param create_dashboards: Indicates whether to create per operation and overall service dashboards. Default: - No dashboards are created
        :param interval: The interval used in the dashboard, defaults to 60 minutes. Default: - 60 minutes
        :param outlier_threshold: The outlier threshold for determining if an AZ is an outlier for latency or faults. This number is interpreted differently for different outlier algorithms. When used with STATIC, the number should be between 0 and 1 to represent the percentage of errors (like .7) that an AZ must be responsible for to be considered an outlier. When used with CHI_SQUARED, it represents the p value that indicates statistical significance, like 0.05 which means the skew has less than or equal to a 5% chance of occuring. When used with Z_SCORE it indicates how many standard deviations to evaluate for an AZ being an outlier, typically 3 is standard for Z_SCORE. Standard defaults based on the outlier detection algorithm: STATIC: 0.7 CHI_SQUARED: 0.05 Z_SCORE: 2 IQR: 1.5 MAD: 3 Default: - Depends on the outlier detection algorithm selected
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30d92d75ef7cead0db6fa29895cdd2786739a400f56564f0fdff625741fee87)
            check_type(argname="argument outlier_detection_algorithm", value=outlier_detection_algorithm, expected_type=type_hints["outlier_detection_algorithm"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument assets_bucket_parameter_name", value=assets_bucket_parameter_name, expected_type=type_hints["assets_bucket_parameter_name"])
            check_type(argname="argument assets_bucket_prefix_parameter_name", value=assets_bucket_prefix_parameter_name, expected_type=type_hints["assets_bucket_prefix_parameter_name"])
            check_type(argname="argument create_dashboards", value=create_dashboards, expected_type=type_hints["create_dashboards"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument outlier_threshold", value=outlier_threshold, expected_type=type_hints["outlier_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "outlier_detection_algorithm": outlier_detection_algorithm,
            "service": service,
        }
        if assets_bucket_parameter_name is not None:
            self._values["assets_bucket_parameter_name"] = assets_bucket_parameter_name
        if assets_bucket_prefix_parameter_name is not None:
            self._values["assets_bucket_prefix_parameter_name"] = assets_bucket_prefix_parameter_name
        if create_dashboards is not None:
            self._values["create_dashboards"] = create_dashboards
        if interval is not None:
            self._values["interval"] = interval
        if outlier_threshold is not None:
            self._values["outlier_threshold"] = outlier_threshold

    @builtins.property
    def outlier_detection_algorithm(self) -> "OutlierDetectionAlgorithm":
        '''The algorithm to use for performing outlier detection.'''
        result = self._values.get("outlier_detection_algorithm")
        assert result is not None, "Required property 'outlier_detection_algorithm' is missing"
        return typing.cast("OutlierDetectionAlgorithm", result)

    @builtins.property
    def service(self) -> IService:
        '''The service that the alarms and dashboards are being crated for.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    @builtins.property
    def assets_bucket_parameter_name(self) -> typing.Optional[builtins.str]:
        '''If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here.

        It will override the bucket location CDK provides by
        default for bundled assets. The stack containing this contruct needs
        to have a parameter defined that uses this name. The underlying
        stacks in this construct that deploy assets will copy the parent stack's
        value for this property.

        :default:

        - The assets will be uploaded to the default defined
        asset location.
        '''
        result = self._values.get("assets_bucket_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assets_bucket_prefix_parameter_name(self) -> typing.Optional[builtins.str]:
        '''If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here.

        It will override the bucket prefix CDK provides by
        default for bundled assets. This property only takes effect if you
        defined the assetsBucketParameterName. The stack containing this contruct needs
        to have a parameter defined that uses this name. The underlying
        stacks in this construct that deploy assets will copy the parent stack's
        value for this property.

        :default:

        - No object prefix will be added to your custom assets location.
        However, if you have overridden something like the 'BucketPrefix' property
        in your stack synthesizer with a variable like "${AssetsBucketPrefix",
        you will need to define this property so it doesn't cause a reference error
        even if the prefix value is blank.
        '''
        result = self._values.get("assets_bucket_prefix_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_dashboards(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to create per operation and overall service dashboards.

        :default: - No dashboards are created
        '''
        result = self._values.get("create_dashboards")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The interval used in the dashboard, defaults to 60 minutes.

        :default: - 60 minutes
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def outlier_threshold(self) -> typing.Optional[jsii.Number]:
        '''The outlier threshold for determining if an AZ is an outlier for latency or faults.

        This number is interpreted
        differently for different outlier algorithms. When used with
        STATIC, the number should be between 0 and 1 to represent the
        percentage of errors (like .7) that an AZ must be responsible
        for to be considered an outlier. When used with CHI_SQUARED, it
        represents the p value that indicates statistical significance, like
        0.05 which means the skew has less than or equal to a 5% chance of
        occuring. When used with Z_SCORE it indicates how many standard
        deviations to evaluate for an AZ being an outlier, typically 3 is
        standard for Z_SCORE.

        Standard defaults based on the outlier detection algorithm:
        STATIC: 0.7
        CHI_SQUARED: 0.05
        Z_SCORE: 2
        IQR: 1.5
        MAD: 3

        :default: - Depends on the outlier detection algorithm selected
        '''
        result = self._values.get("outlier_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstrumentedServiceMultiAZObservabilityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricDimensions(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.MetricDimensions",
):
    '''Provides the ability to get operation specific metric dimensions for metrics at the regional level as well as Availability Zone level.'''

    def __init__(
        self,
        static_dimensions: typing.Mapping[builtins.str, builtins.str],
        availability_zone_id_key: builtins.str,
        region_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param static_dimensions: -
        :param availability_zone_id_key: -
        :param region_key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0231732b77fe1623a009bf60b8908d730dde31c8d87942d8422f2559384453)
            check_type(argname="argument static_dimensions", value=static_dimensions, expected_type=type_hints["static_dimensions"])
            check_type(argname="argument availability_zone_id_key", value=availability_zone_id_key, expected_type=type_hints["availability_zone_id_key"])
            check_type(argname="argument region_key", value=region_key, expected_type=type_hints["region_key"])
        jsii.create(self.__class__, self, [static_dimensions, availability_zone_id_key, region_key])

    @jsii.member(jsii_name="regionalDimensions")
    def regional_dimensions(
        self,
        region: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Gets the regional dimensions for these metrics by combining the static metric dimensions with the keys provided the optional Region key, expected to return something like {   "Region": "us-east-1",   "Operation": "ride",   "Service": "WildRydes" }.

        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdced2a5b7053ef36dcb9443b3f7e91e32352c16565af3c8421b9c6397f7d63)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "regionalDimensions", [region]))

    @jsii.member(jsii_name="zonalDimensions")
    def zonal_dimensions(
        self,
        availability_zone_id: builtins.str,
        region: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Gets the zonal dimensions for these metrics by combining the static metric dimensions with the keys provided for Availability Zone and optional Region, expected to return something like {   "Region": "us-east-1",   "AZ-ID": "use1-az1",   "Operation": "ride",   "Service": "WildRydes" }.

        :param availability_zone_id: -
        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddc4ff234cfbd9f867ff3ee124a1f90bd70f935be37852933515593c920f3d8)
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "zonalDimensions", [availability_zone_id, region]))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdKey")
    def availability_zone_id_key(self) -> builtins.str:
        '''The key used to specify an Availability Zone specific metric dimension, for example: "AZ-ID".'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneIdKey"))

    @availability_zone_id_key.setter
    def availability_zone_id_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316caab4a239cc5e349828bf51796599dd691b46028d84c569f7de2dbc4b3499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneIdKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticDimensions")
    def static_dimensions(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The dimensions that are the same for all Availability Zones for example: {   "Operation": "ride",   "Service": "WildRydes" }.'''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "staticDimensions"))

    @static_dimensions.setter
    def static_dimensions(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f4b0a06877f54397ed9dc9b6e220aee3f221b18b480882fc715fe0974010f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticDimensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionKey")
    def region_key(self) -> typing.Optional[builtins.str]:
        '''The key used for the Region in your dimensions, if you provide one.

        :default:

        - A region specific key and value is not added to your
        zonal and regional metric dimensions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionKey"))

    @region_key.setter
    def region_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a832567c9a2a7011d2c4689c1f3e7d90d5fd6538d40f7833c9d813035ca6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionKey", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="multi-az-observability.NetworkConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"subnet_selection": "subnetSelection", "vpc": "vpc"},
)
class NetworkConfigurationProps:
    def __init__(
        self,
        *,
        subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    ) -> None:
        '''The network configuration for the canary function.

        :param subnet_selection: The subnets the Lambda function will be deployed in the VPC.
        :param vpc: The VPC to run the canary in. A security group will be created that allows the function to communicate with the VPC as well as the required IAM permissions.
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfe87bdb6a05e67c7bb0ac6cb230997c6ff554b711f2126ce0a751647097eff)
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_selection": subnet_selection,
            "vpc": vpc,
        }

    @builtins.property
    def subnet_selection(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''The subnets the Lambda function will be deployed in the VPC.'''
        result = self._values.get("subnet_selection")
        assert result is not None, "Required property 'subnet_selection' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to run the canary in.

        A security group will be created
        that allows the function to communicate with the VPC as well
        as the required IAM permissions.
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOperation)
class Operation(metaclass=jsii.JSIIMeta, jsii_type="multi-az-observability.Operation"):
    '''A single operation that is part of a service.'''

    def __init__(
        self,
        *,
        critical: builtins.bool,
        http_methods: typing.Sequence[builtins.str],
        operation_name: builtins.str,
        path: builtins.str,
        server_side_availability_metric_details: IOperationMetricDetails,
        server_side_latency_metric_details: IOperationMetricDetails,
        service: IService,
        canary_metric_details: typing.Optional[ICanaryMetrics] = None,
        canary_test_availability_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
        canary_test_latency_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
        canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
        opt_out_of_service_created_canary: typing.Optional[builtins.bool] = None,
        server_side_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
    ) -> None:
        '''
        :param critical: Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.
        :param http_methods: The http methods supported by the operation.
        :param operation_name: The name of the operation.
        :param path: The HTTP path for the operation for canaries to run against, something like "/products/list".
        :param server_side_availability_metric_details: The server side availability metric details.
        :param server_side_latency_metric_details: The server side latency metric details.
        :param service: The service the operation is associated with.
        :param canary_metric_details: Optional metric details if the service has a canary. Default: - No alarms, rules, or dashboards will be created from canary metrics
        :param canary_test_availability_metrics_override: The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability. Default: - No availability metric details will be overridden and the service defaults will be used for the automatically created canaries
        :param canary_test_latency_metrics_override: The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency. Default: - No latency metric details will be overridden and the service defaults will be used for the automatically created canaries
        :param canary_test_props: If you define this property, a synthetic canary will be provisioned to test the operation. Default: - The default for the service will be used, if that is undefined, then no canary will be provisioned for this operation.
        :param opt_out_of_service_created_canary: Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation. Default: - The operation is not opted out
        :param server_side_contributor_insight_rule_details: The server side details for contributor insights rules. Default: - The default service contributor insight rule details will be used. If those are not defined no Contributor Insight rules will be created and the number of instances contributing to AZ faults or high latency will not be considered, so a single bad instance could make the AZ appear to look impaired.
        '''
        props = OperationProps(
            critical=critical,
            http_methods=http_methods,
            operation_name=operation_name,
            path=path,
            server_side_availability_metric_details=server_side_availability_metric_details,
            server_side_latency_metric_details=server_side_latency_metric_details,
            service=service,
            canary_metric_details=canary_metric_details,
            canary_test_availability_metrics_override=canary_test_availability_metrics_override,
            canary_test_latency_metrics_override=canary_test_latency_metrics_override,
            canary_test_props=canary_test_props,
            opt_out_of_service_created_canary=opt_out_of_service_created_canary,
            server_side_contributor_insight_rule_details=server_side_contributor_insight_rule_details,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> builtins.bool:
        '''Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.'''
        return typing.cast(builtins.bool, jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(self) -> typing.List[builtins.str]:
        '''The http methods supported by the operation.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The name of the operation.'''
        return typing.cast(builtins.str, jsii.get(self, "operationName"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''The HTTP path for the operation for canaries to run against, something like "/products/list".'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="serverSideAvailabilityMetricDetails")
    def server_side_availability_metric_details(self) -> IOperationMetricDetails:
        '''The server side availability metric details.'''
        return typing.cast(IOperationMetricDetails, jsii.get(self, "serverSideAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="serverSideLatencyMetricDetails")
    def server_side_latency_metric_details(self) -> IOperationMetricDetails:
        '''The server side latency metric details.'''
        return typing.cast(IOperationMetricDetails, jsii.get(self, "serverSideLatencyMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The service the operation is associated with.'''
        return typing.cast(IService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="canaryMetricDetails")
    def canary_metric_details(self) -> typing.Optional[ICanaryMetrics]:
        '''Optional metric details if the service has a canary.'''
        return typing.cast(typing.Optional[ICanaryMetrics], jsii.get(self, "canaryMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestAvailabilityMetricsOverride")
    def canary_test_availability_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability.'''
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], jsii.get(self, "canaryTestAvailabilityMetricsOverride"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestLatencyMetricsOverride")
    def canary_test_latency_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency.'''
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], jsii.get(self, "canaryTestLatencyMetricsOverride"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''If they have been added, the properties for creating new canary tests on this operation.'''
        return typing.cast(typing.Optional[AddCanaryTestProps], jsii.get(self, "canaryTestProps"))

    @builtins.property
    @jsii.member(jsii_name="optOutOfServiceCreatedCanary")
    def opt_out_of_service_created_canary(self) -> typing.Optional[builtins.bool]:
        '''Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation.

        :default: - The operation is not opted out
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "optOutOfServiceCreatedCanary"))

    @builtins.property
    @jsii.member(jsii_name="serverSideContributorInsightRuleDetails")
    def server_side_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The server side details for contributor insights rules.'''
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], jsii.get(self, "serverSideContributorInsightRuleDetails"))


@jsii.implements(IOperationMetricDetails)
class OperationMetricDetails(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.OperationMetricDetails",
):
    '''Generic metric details for an operation.'''

    def __init__(
        self,
        props: typing.Union["OperationMetricDetailsProps", typing.Dict[builtins.str, typing.Any]],
        default_props: IServiceMetricDetails,
    ) -> None:
        '''
        :param props: -
        :param default_props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992972ebf895c0ea7d9905239a632ff039b0c8d79aac7b7b31905fecc6c595ea)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument default_props", value=default_props, expected_type=type_hints["default_props"])
        jsii.create(self.__class__, self, [props, default_props])

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(builtins.str, jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(jsii.Number, jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "faultMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="metricDimensions")
    def metric_dimensions(self) -> MetricDimensions:
        '''The metric dimensions for this operation, must be implemented as a concrete class by the user.'''
        return typing.cast(MetricDimensions, jsii.get(self, "metricDimensions"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        '''The operation these metric details are for.'''
        return typing.cast(builtins.str, jsii.get(self, "operationName"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(jsii.Number, jsii.get(self, "successAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "successMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Unit, jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedFaultStatistics"))

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedSuccessStatistics"))


@jsii.data_type(
    jsii_type="multi-az-observability.OperationMetricDetailsProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric_dimensions": "metricDimensions",
        "operation_name": "operationName",
        "alarm_statistic": "alarmStatistic",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "fault_alarm_threshold": "faultAlarmThreshold",
        "fault_metric_names": "faultMetricNames",
        "graphed_fault_statistics": "graphedFaultStatistics",
        "graphed_success_statistics": "graphedSuccessStatistics",
        "metric_namespace": "metricNamespace",
        "period": "period",
        "success_alarm_threshold": "successAlarmThreshold",
        "success_metric_names": "successMetricNames",
        "unit": "unit",
    },
)
class OperationMetricDetailsProps:
    def __init__(
        self,
        *,
        metric_dimensions: MetricDimensions,
        operation_name: builtins.str,
        alarm_statistic: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        fault_alarm_threshold: typing.Optional[jsii.Number] = None,
        fault_metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphed_fault_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphed_success_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_namespace: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        success_alarm_threshold: typing.Optional[jsii.Number] = None,
        success_metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> None:
        '''The properties for operation metric details.

        :param metric_dimensions: The user implemented functions for providing the metric's dimensions.
        :param operation_name: The operation these metric details are for.
        :param alarm_statistic: The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9". Default: - The service default is used
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms. Default: - The service default is used
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms. Default: - The service default is used
        :param fault_alarm_threshold: The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%. Default: - The service default is used
        :param fault_metric_names: The names of fault indicating metrics. Default: - The service default is used
        :param graphed_fault_statistics: The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - The service default is used
        :param graphed_success_statistics: The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - The service default is used
        :param metric_namespace: The CloudWatch metric namespace for these metrics. Default: - The service default is used
        :param period: The period for the metrics. Default: - The service default is used
        :param success_alarm_threshold: The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%. Default: - The service default is used
        :param success_metric_names: The names of success indicating metrics. Default: - The service default is used
        :param unit: The unit used for these metrics. Default: - The service default is used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf637b714cdbee8ae242e21c6b369adfefc190ccf00d0385165c32c2fc2f214)
            check_type(argname="argument metric_dimensions", value=metric_dimensions, expected_type=type_hints["metric_dimensions"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument alarm_statistic", value=alarm_statistic, expected_type=type_hints["alarm_statistic"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument fault_alarm_threshold", value=fault_alarm_threshold, expected_type=type_hints["fault_alarm_threshold"])
            check_type(argname="argument fault_metric_names", value=fault_metric_names, expected_type=type_hints["fault_metric_names"])
            check_type(argname="argument graphed_fault_statistics", value=graphed_fault_statistics, expected_type=type_hints["graphed_fault_statistics"])
            check_type(argname="argument graphed_success_statistics", value=graphed_success_statistics, expected_type=type_hints["graphed_success_statistics"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument success_alarm_threshold", value=success_alarm_threshold, expected_type=type_hints["success_alarm_threshold"])
            check_type(argname="argument success_metric_names", value=success_metric_names, expected_type=type_hints["success_metric_names"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_dimensions": metric_dimensions,
            "operation_name": operation_name,
        }
        if alarm_statistic is not None:
            self._values["alarm_statistic"] = alarm_statistic
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if fault_alarm_threshold is not None:
            self._values["fault_alarm_threshold"] = fault_alarm_threshold
        if fault_metric_names is not None:
            self._values["fault_metric_names"] = fault_metric_names
        if graphed_fault_statistics is not None:
            self._values["graphed_fault_statistics"] = graphed_fault_statistics
        if graphed_success_statistics is not None:
            self._values["graphed_success_statistics"] = graphed_success_statistics
        if metric_namespace is not None:
            self._values["metric_namespace"] = metric_namespace
        if period is not None:
            self._values["period"] = period
        if success_alarm_threshold is not None:
            self._values["success_alarm_threshold"] = success_alarm_threshold
        if success_metric_names is not None:
            self._values["success_metric_names"] = success_metric_names
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_dimensions(self) -> MetricDimensions:
        '''The user implemented functions for providing the metric's dimensions.'''
        result = self._values.get("metric_dimensions")
        assert result is not None, "Required property 'metric_dimensions' is missing"
        return typing.cast(MetricDimensions, result)

    @builtins.property
    def operation_name(self) -> builtins.str:
        '''The operation these metric details are for.'''
        result = self._values.get("operation_name")
        assert result is not None, "Required property 'operation_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".

        :default: - The service default is used
        '''
        result = self._values.get("alarm_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints to alarm on for latency and availability alarms.

        :default: - The service default is used
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of evaluation periods for latency and availabiltiy alarms.

        :default: - The service default is used
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fault_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.

        :default: - The service default is used
        '''
        result = self._values.get("fault_alarm_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fault_metric_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of fault indicating metrics.

        :default: - The service default is used
        '''
        result = self._values.get("fault_metric_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - The service default is used
        '''
        result = self._values.get("graphed_fault_statistics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - The service default is used
        '''
        result = self._values.get("graphed_success_statistics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_namespace(self) -> typing.Optional[builtins.str]:
        '''The CloudWatch metric namespace for these metrics.

        :default: - The service default is used
        '''
        result = self._values.get("metric_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period for the metrics.

        :default: - The service default is used
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def success_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.

        :default: - The service default is used
        '''
        result = self._values.get("success_alarm_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_metric_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of success indicating metrics.

        :default: - The service default is used
        '''
        result = self._values.get("success_metric_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def unit(self) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit]:
        '''The unit used for these metrics.

        :default: - The service default is used
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OperationMetricDetailsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.OperationProps",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "http_methods": "httpMethods",
        "operation_name": "operationName",
        "path": "path",
        "server_side_availability_metric_details": "serverSideAvailabilityMetricDetails",
        "server_side_latency_metric_details": "serverSideLatencyMetricDetails",
        "service": "service",
        "canary_metric_details": "canaryMetricDetails",
        "canary_test_availability_metrics_override": "canaryTestAvailabilityMetricsOverride",
        "canary_test_latency_metrics_override": "canaryTestLatencyMetricsOverride",
        "canary_test_props": "canaryTestProps",
        "opt_out_of_service_created_canary": "optOutOfServiceCreatedCanary",
        "server_side_contributor_insight_rule_details": "serverSideContributorInsightRuleDetails",
    },
)
class OperationProps:
    def __init__(
        self,
        *,
        critical: builtins.bool,
        http_methods: typing.Sequence[builtins.str],
        operation_name: builtins.str,
        path: builtins.str,
        server_side_availability_metric_details: IOperationMetricDetails,
        server_side_latency_metric_details: IOperationMetricDetails,
        service: IService,
        canary_metric_details: typing.Optional[ICanaryMetrics] = None,
        canary_test_availability_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
        canary_test_latency_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
        canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
        opt_out_of_service_created_canary: typing.Optional[builtins.bool] = None,
        server_side_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
    ) -> None:
        '''Properties for an operation.

        :param critical: Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.
        :param http_methods: The http methods supported by the operation.
        :param operation_name: The name of the operation.
        :param path: The HTTP path for the operation for canaries to run against, something like "/products/list".
        :param server_side_availability_metric_details: The server side availability metric details.
        :param server_side_latency_metric_details: The server side latency metric details.
        :param service: The service the operation is associated with.
        :param canary_metric_details: Optional metric details if the service has a canary. Default: - No alarms, rules, or dashboards will be created from canary metrics
        :param canary_test_availability_metrics_override: The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability. Default: - No availability metric details will be overridden and the service defaults will be used for the automatically created canaries
        :param canary_test_latency_metrics_override: The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency. Default: - No latency metric details will be overridden and the service defaults will be used for the automatically created canaries
        :param canary_test_props: If you define this property, a synthetic canary will be provisioned to test the operation. Default: - The default for the service will be used, if that is undefined, then no canary will be provisioned for this operation.
        :param opt_out_of_service_created_canary: Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation. Default: - The operation is not opted out
        :param server_side_contributor_insight_rule_details: The server side details for contributor insights rules. Default: - The default service contributor insight rule details will be used. If those are not defined no Contributor Insight rules will be created and the number of instances contributing to AZ faults or high latency will not be considered, so a single bad instance could make the AZ appear to look impaired.
        '''
        if isinstance(canary_test_props, dict):
            canary_test_props = AddCanaryTestProps(**canary_test_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d484fa77c0f6fbd2c974e219a3a6ddd645dec7dda3146ffc0cc68275ee2f24)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument server_side_availability_metric_details", value=server_side_availability_metric_details, expected_type=type_hints["server_side_availability_metric_details"])
            check_type(argname="argument server_side_latency_metric_details", value=server_side_latency_metric_details, expected_type=type_hints["server_side_latency_metric_details"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument canary_metric_details", value=canary_metric_details, expected_type=type_hints["canary_metric_details"])
            check_type(argname="argument canary_test_availability_metrics_override", value=canary_test_availability_metrics_override, expected_type=type_hints["canary_test_availability_metrics_override"])
            check_type(argname="argument canary_test_latency_metrics_override", value=canary_test_latency_metrics_override, expected_type=type_hints["canary_test_latency_metrics_override"])
            check_type(argname="argument canary_test_props", value=canary_test_props, expected_type=type_hints["canary_test_props"])
            check_type(argname="argument opt_out_of_service_created_canary", value=opt_out_of_service_created_canary, expected_type=type_hints["opt_out_of_service_created_canary"])
            check_type(argname="argument server_side_contributor_insight_rule_details", value=server_side_contributor_insight_rule_details, expected_type=type_hints["server_side_contributor_insight_rule_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
            "http_methods": http_methods,
            "operation_name": operation_name,
            "path": path,
            "server_side_availability_metric_details": server_side_availability_metric_details,
            "server_side_latency_metric_details": server_side_latency_metric_details,
            "service": service,
        }
        if canary_metric_details is not None:
            self._values["canary_metric_details"] = canary_metric_details
        if canary_test_availability_metrics_override is not None:
            self._values["canary_test_availability_metrics_override"] = canary_test_availability_metrics_override
        if canary_test_latency_metrics_override is not None:
            self._values["canary_test_latency_metrics_override"] = canary_test_latency_metrics_override
        if canary_test_props is not None:
            self._values["canary_test_props"] = canary_test_props
        if opt_out_of_service_created_canary is not None:
            self._values["opt_out_of_service_created_canary"] = opt_out_of_service_created_canary
        if server_side_contributor_insight_rule_details is not None:
            self._values["server_side_contributor_insight_rule_details"] = server_side_contributor_insight_rule_details

    @builtins.property
    def critical(self) -> builtins.bool:
        '''Indicates this is a critical operation for the service and will be included in service level metrics and dashboards.'''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def http_methods(self) -> typing.List[builtins.str]:
        '''The http methods supported by the operation.'''
        result = self._values.get("http_methods")
        assert result is not None, "Required property 'http_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operation_name(self) -> builtins.str:
        '''The name of the operation.'''
        result = self._values.get("operation_name")
        assert result is not None, "Required property 'operation_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The HTTP path for the operation for canaries to run against, something like "/products/list".'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_side_availability_metric_details(self) -> IOperationMetricDetails:
        '''The server side availability metric details.'''
        result = self._values.get("server_side_availability_metric_details")
        assert result is not None, "Required property 'server_side_availability_metric_details' is missing"
        return typing.cast(IOperationMetricDetails, result)

    @builtins.property
    def server_side_latency_metric_details(self) -> IOperationMetricDetails:
        '''The server side latency metric details.'''
        result = self._values.get("server_side_latency_metric_details")
        assert result is not None, "Required property 'server_side_latency_metric_details' is missing"
        return typing.cast(IOperationMetricDetails, result)

    @builtins.property
    def service(self) -> IService:
        '''The service the operation is associated with.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    @builtins.property
    def canary_metric_details(self) -> typing.Optional[ICanaryMetrics]:
        '''Optional metric details if the service has a canary.

        :default:

        - No alarms, rules, or dashboards will be created
        from canary metrics
        '''
        result = self._values.get("canary_metric_details")
        return typing.cast(typing.Optional[ICanaryMetrics], result)

    @builtins.property
    def canary_test_availability_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for availability.

        :default:

        - No availability metric details will be overridden and the
        service defaults will be used for the automatically created canaries
        '''
        result = self._values.get("canary_test_availability_metrics_override")
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], result)

    @builtins.property
    def canary_test_latency_metrics_override(
        self,
    ) -> typing.Optional[ICanaryTestMetricsOverride]:
        '''The override values for automatically created canary tests so you can use values other than the service defaults to define the thresholds for latency.

        :default:

        - No latency metric details will be overridden and the
        service defaults will be used for the automatically created canaries
        '''
        result = self._values.get("canary_test_latency_metrics_override")
        return typing.cast(typing.Optional[ICanaryTestMetricsOverride], result)

    @builtins.property
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''If you define this property, a synthetic canary will be provisioned to test the operation.

        :default:

        - The default for the service will be used, if that
        is undefined, then no canary will be provisioned for this operation.
        '''
        result = self._values.get("canary_test_props")
        return typing.cast(typing.Optional[AddCanaryTestProps], result)

    @builtins.property
    def opt_out_of_service_created_canary(self) -> typing.Optional[builtins.bool]:
        '''Set to true if you have defined CanaryTestProps for your service, which applies to all operations, but you want to opt out of creating the canary test for this operation.

        :default: - The operation is not opted out
        '''
        result = self._values.get("opt_out_of_service_created_canary")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def server_side_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The server side details for contributor insights rules.

        :default:

        - The default service contributor insight rule
        details will be used. If those are not defined no Contributor Insight
        rules will be created and the number of instances contributing to AZ
        faults or high latency will not be considered, so a single bad instance
        could make the AZ appear to look impaired.
        '''
        result = self._values.get("server_side_contributor_insight_rule_details")
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OperationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="multi-az-observability.OutlierDetectionAlgorithm")
class OutlierDetectionAlgorithm(enum.Enum):
    '''Available algorithms for performing outlier detection.'''

    STATIC = "STATIC"
    '''Defines using a static value to compare skew in faults or high latency responses.

    A good default threshold for this is .7 meaning one AZ
    is responsible for 70% of the total errors or high latency responses
    '''
    CHI_SQUARED = "CHI_SQUARED"
    '''Uses the chi squared statistic to determine if there is a statistically significant skew in fault rate or high latency distribution.

    A normal default threshold for this is 0.05, which means there is a 5% or
    less chance of the skew in errors or high latency responses occuring
    '''
    Z_SCORE = "Z_SCORE"
    '''Uses z-score to determine if the skew in faults or high latency respones exceeds a defined number of standard devations.

    A good default threshold value for this is 2, meaning the outlier value is outside
    95% of the normal distribution. Using 3 means the outlier is outside 99.7% of
    the normal distribution.
    '''
    IQR = "IQR"
    '''Uses Interquartile Range Method to determine an outlier for faults or latency.

    No threshold is required for this method and will be ignored
    '''
    MAD = "MAD"
    '''Median Absolute Deviation (MAD) to determine an outlier for faults or latency.

    A common default value threshold 3
    '''


@jsii.implements(IService)
class Service(metaclass=jsii.JSIIMeta, jsii_type="multi-az-observability.Service"):
    '''The representation of a service composed of multiple operations.'''

    def __init__(
        self,
        *,
        availability_zone_names: typing.Sequence[builtins.str],
        base_url: builtins.str,
        default_availability_metric_details: IServiceMetricDetails,
        default_latency_metric_details: IServiceMetricDetails,
        fault_count_threshold: jsii.Number,
        period: _aws_cdk_ceddda9d.Duration,
        service_name: builtins.str,
        canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2] = None,
    ) -> None:
        '''
        :param availability_zone_names: A list of the Availability Zone names used by this application.
        :param base_url: The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.
        :param default_availability_metric_details: The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.
        :param default_latency_metric_details: The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.
        :param fault_count_threshold: The fault count threshold that indicates the service is unhealthy. This is an absolute value of faults being produced by all critical operations in aggregate.
        :param period: The period for which metrics for the service should be aggregated.
        :param service_name: The name of your service.
        :param canary_test_props: Define these settings if you want to automatically add canary tests to your operations. Operations can individually opt out of canary test creation if you define this setting. Default: - Automatic canary tests will not be created for operations in this service.
        :param default_contributor_insight_rule_details: The default settings that are used for contributor insight rules. Default: - No defaults are provided and must be specified per operation if the operation has logs that can be queried by contributor insights
        :param load_balancer: The load balancer this service sits behind. Default: - Load balancer metrics won't be shown on dashboards and its ARN won't be included in top level alarm descriptions that automation can use to implement a zonal shift.
        '''
        props = ServiceProps(
            availability_zone_names=availability_zone_names,
            base_url=base_url,
            default_availability_metric_details=default_availability_metric_details,
            default_latency_metric_details=default_latency_metric_details,
            fault_count_threshold=fault_count_threshold,
            period=period,
            service_name=service_name,
            canary_test_props=canary_test_props,
            default_contributor_insight_rule_details=default_contributor_insight_rule_details,
            load_balancer=load_balancer,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addOperation")
    def add_operation(self, operation: IOperation) -> None:
        '''Adds an operation to this service and sets the operation's service property.

        :param operation: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ac8fba10f62a93023efbb6d4c5f64df730e4d49fff16f85614294cb5a334ea)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        return typing.cast(None, jsii.invoke(self, "addOperation", [operation]))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneNames")
    def availability_zone_names(self) -> typing.List[builtins.str]:
        '''A list of the Availability Zone names used by this application.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZoneNames"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        '''The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.'''
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @builtins.property
    @jsii.member(jsii_name="defaultAvailabilityMetricDetails")
    def default_availability_metric_details(self) -> IServiceMetricDetails:
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        return typing.cast(IServiceMetricDetails, jsii.get(self, "defaultAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="defaultLatencyMetricDetails")
    def default_latency_metric_details(self) -> IServiceMetricDetails:
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        return typing.cast(IServiceMetricDetails, jsii.get(self, "defaultLatencyMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="faultCountThreshold")
    def fault_count_threshold(self) -> jsii.Number:
        '''The fault count threshold that indicates the service is unhealthy.

        This is an absolute value of faults
        being produced by all critical operations in aggregate.
        '''
        return typing.cast(jsii.Number, jsii.get(self, "faultCountThreshold"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[IOperation]:
        '''The operations that are part of this service.'''
        return typing.cast(typing.List[IOperation], jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for which metrics for the service should be aggregated.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of your service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="canaryTestProps")
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''Define these settings if you want to automatically add canary tests to your operations.

        Operations can individually opt out
        of canary test creation if you define this setting.

        :default:

        - Automatic canary tests will not be created for
        operations in this service.
        '''
        return typing.cast(typing.Optional[AddCanaryTestProps], jsii.get(self, "canaryTestProps"))

    @builtins.property
    @jsii.member(jsii_name="defaultContributorInsightRuleDetails")
    def default_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The default settings that are used for contributor insight rules.

        :default: - No defaults are provided and must be specified per operation
        '''
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], jsii.get(self, "defaultContributorInsightRuleDetails"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2]:
        '''The load balancer this service sits behind.

        :default:

        - No load balancer metrics will be included in
        dashboards and its ARN will not be added to top level AZ
        alarm descriptions.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2], jsii.get(self, "loadBalancer"))


@jsii.implements(IServiceMetricDetails)
class ServiceMetricDetails(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.ServiceMetricDetails",
):
    '''Default metric details for a service.'''

    def __init__(
        self,
        *,
        alarm_statistic: builtins.str,
        datapoints_to_alarm: jsii.Number,
        evaluation_periods: jsii.Number,
        fault_alarm_threshold: jsii.Number,
        fault_metric_names: typing.Sequence[builtins.str],
        metric_namespace: builtins.str,
        period: _aws_cdk_ceddda9d.Duration,
        success_alarm_threshold: jsii.Number,
        success_metric_names: typing.Sequence[builtins.str],
        unit: _aws_cdk_aws_cloudwatch_ceddda9d.Unit,
        graphed_fault_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphed_success_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param alarm_statistic: The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms.
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms.
        :param fault_alarm_threshold: The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.
        :param fault_metric_names: The names of fault indicating metrics.
        :param metric_namespace: The CloudWatch metric namespace for these metrics.
        :param period: The period for the metrics.
        :param success_alarm_threshold: The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.
        :param success_metric_names: The names of success indicating metrics.
        :param unit: The unit used for these metrics.
        :param graphed_fault_statistics: The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        :param graphed_success_statistics: The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        props = ServiceMetricDetailsProps(
            alarm_statistic=alarm_statistic,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            fault_alarm_threshold=fault_alarm_threshold,
            fault_metric_names=fault_metric_names,
            metric_namespace=metric_namespace,
            period=period,
            success_alarm_threshold=success_alarm_threshold,
            success_metric_names=success_metric_names,
            unit=unit,
            graphed_fault_statistics=graphed_fault_statistics,
            graphed_success_statistics=graphed_success_statistics,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(builtins.str, jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(jsii.Number, jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricNames")
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "faultMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(jsii.Number, jsii.get(self, "successAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="successMetricNames")
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "successMetricNames"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Unit, jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="graphedFaultStatistics")
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedFaultStatistics"))

    @builtins.property
    @jsii.member(jsii_name="graphedSuccessStatistics")
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphedSuccessStatistics"))


@jsii.data_type(
    jsii_type="multi-az-observability.ServiceMetricDetailsProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_statistic": "alarmStatistic",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "fault_alarm_threshold": "faultAlarmThreshold",
        "fault_metric_names": "faultMetricNames",
        "metric_namespace": "metricNamespace",
        "period": "period",
        "success_alarm_threshold": "successAlarmThreshold",
        "success_metric_names": "successMetricNames",
        "unit": "unit",
        "graphed_fault_statistics": "graphedFaultStatistics",
        "graphed_success_statistics": "graphedSuccessStatistics",
    },
)
class ServiceMetricDetailsProps:
    def __init__(
        self,
        *,
        alarm_statistic: builtins.str,
        datapoints_to_alarm: jsii.Number,
        evaluation_periods: jsii.Number,
        fault_alarm_threshold: jsii.Number,
        fault_metric_names: typing.Sequence[builtins.str],
        metric_namespace: builtins.str,
        period: _aws_cdk_ceddda9d.Duration,
        success_alarm_threshold: jsii.Number,
        success_metric_names: typing.Sequence[builtins.str],
        unit: _aws_cdk_aws_cloudwatch_ceddda9d.Unit,
        graphed_fault_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphed_success_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''The properties for default service metric details.

        :param alarm_statistic: The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms.
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms.
        :param fault_alarm_threshold: The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.
        :param fault_metric_names: The names of fault indicating metrics.
        :param metric_namespace: The CloudWatch metric namespace for these metrics.
        :param period: The period for the metrics.
        :param success_alarm_threshold: The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.
        :param success_metric_names: The names of success indicating metrics.
        :param unit: The unit used for these metrics.
        :param graphed_fault_statistics: The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        :param graphed_success_statistics: The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99. For availability metrics this will typically just be "Sum". Default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7149a4b69b51765276c5603c7584f1951ed8c9f5eedf87441b153b5a83380d)
            check_type(argname="argument alarm_statistic", value=alarm_statistic, expected_type=type_hints["alarm_statistic"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument fault_alarm_threshold", value=fault_alarm_threshold, expected_type=type_hints["fault_alarm_threshold"])
            check_type(argname="argument fault_metric_names", value=fault_metric_names, expected_type=type_hints["fault_metric_names"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument success_alarm_threshold", value=success_alarm_threshold, expected_type=type_hints["success_alarm_threshold"])
            check_type(argname="argument success_metric_names", value=success_metric_names, expected_type=type_hints["success_metric_names"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument graphed_fault_statistics", value=graphed_fault_statistics, expected_type=type_hints["graphed_fault_statistics"])
            check_type(argname="argument graphed_success_statistics", value=graphed_success_statistics, expected_type=type_hints["graphed_success_statistics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_statistic": alarm_statistic,
            "datapoints_to_alarm": datapoints_to_alarm,
            "evaluation_periods": evaluation_periods,
            "fault_alarm_threshold": fault_alarm_threshold,
            "fault_metric_names": fault_metric_names,
            "metric_namespace": metric_namespace,
            "period": period,
            "success_alarm_threshold": success_alarm_threshold,
            "success_metric_names": success_metric_names,
            "unit": unit,
        }
        if graphed_fault_statistics is not None:
            self._values["graphed_fault_statistics"] = graphed_fault_statistics
        if graphed_success_statistics is not None:
            self._values["graphed_success_statistics"] = graphed_success_statistics

    @builtins.property
    def alarm_statistic(self) -> builtins.str:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        result = self._values.get("alarm_statistic")
        assert result is not None, "Required property 'alarm_statistic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datapoints_to_alarm(self) -> jsii.Number:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        result = self._values.get("datapoints_to_alarm")
        assert result is not None, "Required property 'datapoints_to_alarm' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def fault_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        result = self._values.get("fault_alarm_threshold")
        assert result is not None, "Required property 'fault_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def fault_metric_names(self) -> typing.List[builtins.str]:
        '''The names of fault indicating metrics.'''
        result = self._values.get("fault_metric_names")
        assert result is not None, "Required property 'fault_metric_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The CloudWatch metric namespace for these metrics.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for the metrics.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def success_alarm_threshold(self) -> jsii.Number:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        result = self._values.get("success_alarm_threshold")
        assert result is not None, "Required property 'success_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def success_metric_names(self) -> typing.List[builtins.str]:
        '''The names of success indicating metrics.'''
        result = self._values.get("success_metric_names")
        assert result is not None, "Required property 'success_metric_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unit(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.Unit:
        '''The unit used for these metrics.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Unit, result)

    @builtins.property
    def graphed_fault_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for faults you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        result = self._values.get("graphed_fault_statistics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def graphed_success_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The statistics for successes you want to appear on dashboards, for example, with latency metrics, you might want p50, p99, and tm99.

        For availability
        metrics this will typically just be "Sum".

        :default: - For availability metrics, this will be "Sum", for latency metrics it will be just "p99"
        '''
        result = self._values.get("graphed_success_statistics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceMetricDetailsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="multi-az-observability.ServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_names": "availabilityZoneNames",
        "base_url": "baseUrl",
        "default_availability_metric_details": "defaultAvailabilityMetricDetails",
        "default_latency_metric_details": "defaultLatencyMetricDetails",
        "fault_count_threshold": "faultCountThreshold",
        "period": "period",
        "service_name": "serviceName",
        "canary_test_props": "canaryTestProps",
        "default_contributor_insight_rule_details": "defaultContributorInsightRuleDetails",
        "load_balancer": "loadBalancer",
    },
)
class ServiceProps:
    def __init__(
        self,
        *,
        availability_zone_names: typing.Sequence[builtins.str],
        base_url: builtins.str,
        default_availability_metric_details: IServiceMetricDetails,
        default_latency_metric_details: IServiceMetricDetails,
        fault_count_threshold: jsii.Number,
        period: _aws_cdk_ceddda9d.Duration,
        service_name: builtins.str,
        canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2] = None,
    ) -> None:
        '''Properties to initialize a service.

        :param availability_zone_names: A list of the Availability Zone names used by this application.
        :param base_url: The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.
        :param default_availability_metric_details: The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.
        :param default_latency_metric_details: The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.
        :param fault_count_threshold: The fault count threshold that indicates the service is unhealthy. This is an absolute value of faults being produced by all critical operations in aggregate.
        :param period: The period for which metrics for the service should be aggregated.
        :param service_name: The name of your service.
        :param canary_test_props: Define these settings if you want to automatically add canary tests to your operations. Operations can individually opt out of canary test creation if you define this setting. Default: - Automatic canary tests will not be created for operations in this service.
        :param default_contributor_insight_rule_details: The default settings that are used for contributor insight rules. Default: - No defaults are provided and must be specified per operation if the operation has logs that can be queried by contributor insights
        :param load_balancer: The load balancer this service sits behind. Default: - Load balancer metrics won't be shown on dashboards and its ARN won't be included in top level alarm descriptions that automation can use to implement a zonal shift.
        '''
        if isinstance(canary_test_props, dict):
            canary_test_props = AddCanaryTestProps(**canary_test_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8292313fdf86d8fe32f33cf45a68ef9b39914f11b67335d49298260fca9f00de)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument default_availability_metric_details", value=default_availability_metric_details, expected_type=type_hints["default_availability_metric_details"])
            check_type(argname="argument default_latency_metric_details", value=default_latency_metric_details, expected_type=type_hints["default_latency_metric_details"])
            check_type(argname="argument fault_count_threshold", value=fault_count_threshold, expected_type=type_hints["fault_count_threshold"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument canary_test_props", value=canary_test_props, expected_type=type_hints["canary_test_props"])
            check_type(argname="argument default_contributor_insight_rule_details", value=default_contributor_insight_rule_details, expected_type=type_hints["default_contributor_insight_rule_details"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone_names": availability_zone_names,
            "base_url": base_url,
            "default_availability_metric_details": default_availability_metric_details,
            "default_latency_metric_details": default_latency_metric_details,
            "fault_count_threshold": fault_count_threshold,
            "period": period,
            "service_name": service_name,
        }
        if canary_test_props is not None:
            self._values["canary_test_props"] = canary_test_props
        if default_contributor_insight_rule_details is not None:
            self._values["default_contributor_insight_rule_details"] = default_contributor_insight_rule_details
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer

    @builtins.property
    def availability_zone_names(self) -> typing.List[builtins.str]:
        '''A list of the Availability Zone names used by this application.'''
        result = self._values.get("availability_zone_names")
        assert result is not None, "Required property 'availability_zone_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def base_url(self) -> builtins.str:
        '''The base endpoint for this service, like "https://www.example.com". Operation paths will be appended to this endpoint for canary testing the service.'''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_availability_metric_details(self) -> IServiceMetricDetails:
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        result = self._values.get("default_availability_metric_details")
        assert result is not None, "Required property 'default_availability_metric_details' is missing"
        return typing.cast(IServiceMetricDetails, result)

    @builtins.property
    def default_latency_metric_details(self) -> IServiceMetricDetails:
        '''The default settings that are used for availability metrics for all operations unless specifically overridden in an operation definition.'''
        result = self._values.get("default_latency_metric_details")
        assert result is not None, "Required property 'default_latency_metric_details' is missing"
        return typing.cast(IServiceMetricDetails, result)

    @builtins.property
    def fault_count_threshold(self) -> jsii.Number:
        '''The fault count threshold that indicates the service is unhealthy.

        This is an absolute value of faults
        being produced by all critical operations in aggregate.
        '''
        result = self._values.get("fault_count_threshold")
        assert result is not None, "Required property 'fault_count_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''The period for which metrics for the service should be aggregated.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''The name of your service.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canary_test_props(self) -> typing.Optional[AddCanaryTestProps]:
        '''Define these settings if you want to automatically add canary tests to your operations.

        Operations can individually opt out
        of canary test creation if you define this setting.

        :default:

        - Automatic canary tests will not be created for
        operations in this service.
        '''
        result = self._values.get("canary_test_props")
        return typing.cast(typing.Optional[AddCanaryTestProps], result)

    @builtins.property
    def default_contributor_insight_rule_details(
        self,
    ) -> typing.Optional[IContributorInsightRuleDetails]:
        '''The default settings that are used for contributor insight rules.

        :default:

        - No defaults are provided and must be specified per operation
        if the operation has logs that can be queried by contributor insights
        '''
        result = self._values.get("default_contributor_insight_rule_details")
        return typing.cast(typing.Optional[IContributorInsightRuleDetails], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2]:
        '''The load balancer this service sits behind.

        :default:

        - Load balancer metrics won't be shown on dashboards
        and its ARN won't be included in top level alarm descriptions
        that automation can use to implement a zonal shift.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAvailabilityZoneMapper)
class AvailabilityZoneMapper(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.AvailabilityZoneMapper",
):
    '''A construct that allows you to map AZ names to ids and back.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zone_names: The currently in use Availability Zone names which constrains the list of AZ IDs that are returned. Default: - No names are provided and the mapper returns all AZs in the region in its lists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585c51e84a8f3bb791f23a2e17e84165faf2c7da42fe1473e7d7f07dee294aec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AvailabilityZoneMapperProps(
            availability_zone_names=availability_zone_names
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsArray")
    def all_availability_zone_ids_as_array(self) -> _aws_cdk_ceddda9d.Reference:
        '''Returns a reference that can be cast to a string array with all of the Availability Zone Ids.'''
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "allAvailabilityZoneIdsAsArray", []))

    @jsii.member(jsii_name="allAvailabilityZoneIdsAsCommaDelimitedList")
    def all_availability_zone_ids_as_comma_delimited_list(self) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "allAvailabilityZoneIdsAsCommaDelimitedList", []))

    @jsii.member(jsii_name="allAvailabilityZoneNamesAsCommaDelimitedList")
    def all_availability_zone_names_as_comma_delimited_list(self) -> builtins.str:
        '''Gets all of the Availability Zone names in this Region as a comma delimited list.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Name
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "allAvailabilityZoneNamesAsCommaDelimitedList", []))

    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(
        self,
        availability_zone_name: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Id for the given Availability Zone Name in this account.

        :param availability_zone_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cde3a0b835c7ec259cfd42c2b95b6eead298927cf17be162ffa4ef19fc0e1d0)
            check_type(argname="argument availability_zone_name", value=availability_zone_name, expected_type=type_hints["availability_zone_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneId", [availability_zone_name]))

    @jsii.member(jsii_name="availabilityZoneIdFromAvailabilityZoneLetter")
    def availability_zone_id_from_availability_zone_letter(
        self,
        letter: builtins.str,
    ) -> builtins.str:
        '''Given a letter like "f" or "a", returns the Availability Zone Id for that Availability Zone name in this account.

        :param letter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24f7608ecd89d63b70f11709bcb35d148188c2d62d0a242b6be7aadb5e3a585)
            check_type(argname="argument letter", value=letter, expected_type=type_hints["letter"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneIdFromAvailabilityZoneLetter", [letter]))

    @jsii.member(jsii_name="availabilityZoneIdsAsArray")
    def availability_zone_ids_as_array(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> typing.List[builtins.str]:
        '''Returns an array for Availability Zone Ids for the supplied Availability Zone names, they are returned in the same order the names were provided.

        :param availability_zone_names: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7f6db7dd2a1e9ccffcfa6c84fb6ebdcb7f41c6f1aab7df8066380703be4fa5)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "availabilityZoneIdsAsArray", [availability_zone_names]))

    @jsii.member(jsii_name="availabilityZoneIdsAsCommaDelimitedList")
    def availability_zone_ids_as_comma_delimited_list(
        self,
        availability_zone_names: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''Returns a comma delimited list of Availability Zone Ids for the supplied Availability Zone names.

        You can use this string with Fn.Select(x, Fn.Split(",", azs)) to
        get a specific Availability Zone Id

        :param availability_zone_names: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bab0ae038b9ffefe5b182837771bfd45222d6159b5d837c778fda0cb0010081)
            check_type(argname="argument availability_zone_names", value=availability_zone_names, expected_type=type_hints["availability_zone_names"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneIdsAsCommaDelimitedList", [availability_zone_names]))

    @jsii.member(jsii_name="availabilityZoneName")
    def availability_zone_name(
        self,
        availability_zone_id: builtins.str,
    ) -> builtins.str:
        '''Gets the Availability Zone Name for the given Availability Zone Id in this account.

        :param availability_zone_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa84169ecad60d48c1cdcda563723475c0216ac384a78ceb4382bdd1a919273)
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "availabilityZoneName", [availability_zone_id]))

    @jsii.member(jsii_name="regionPrefixForAvailabilityZoneIds")
    def region_prefix_for_availability_zone_ids(self) -> builtins.str:
        '''Gets the prefix for the region used with Availability Zone Ids, for example in us-east-1, this returns "use1".'''
        return typing.cast(builtins.str, jsii.invoke(self, "regionPrefixForAvailabilityZoneIds", []))

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The function that does the mapping.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))

    @function.setter
    def function(self, value: _aws_cdk_aws_lambda_ceddda9d.IFunction) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af51bda9380215b07fe0b0958367d23c488575d1774e7f0bb97f444574aaab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group for the function's logs.'''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: _aws_cdk_aws_logs_ceddda9d.ILogGroup) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29194ef39eaaecc9f9f91e9a083f2137bdcb4ac882afc1583175e2200b01c691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapper")
    def mapper(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''The custom resource that can be referenced to use Fn::GetAtt functions on to retrieve availability zone names and ids.'''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "mapper"))

    @mapper.setter
    def mapper(self, value: _aws_cdk_ceddda9d.CustomResource) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e28c12ab3649a0e6b8be31dda54ffcb3ab7079fd90428cc535ec617df0e8687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapper", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IBasicServiceMultiAZObservability)
class BasicServiceMultiAZObservability(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.BasicServiceMultiAZObservability",
):
    '''Basic observability for a service using metrics from ALBs and NAT Gateways.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        create_dashboard: builtins.bool,
        datapoints_to_alarm: jsii.Number,
        evaluation_periods: jsii.Number,
        outlier_detection_algorithm: OutlierDetectionAlgorithm,
        period: _aws_cdk_ceddda9d.Duration,
        service_name: builtins.str,
        application_load_balancers: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]] = None,
        assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
        assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
        fault_count_percentage_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        nat_gateways: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]] = None,
        outlier_threshold: typing.Optional[jsii.Number] = None,
        packet_loss_impact_percentage_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_dashboard: Whether to create a dashboard displaying the metrics and alarms.
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms.
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms.
        :param outlier_detection_algorithm: The algorithm to use for performing outlier detection.
        :param period: The period to evaluate metrics.
        :param service_name: The service's name.
        :param application_load_balancers: The application load balancers being used by the service. Default: - No alarms for ALBs will be created
        :param assets_bucket_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket whose name is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket location CDK provides by default for bundled assets. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - The assets will be uploaded to the default defined asset location.
        :param assets_bucket_prefix_parameter_name: If you are not using a static bucket to deploy assets, for example you are synthing this and it gets uploaded to a bucket that uses a prefix that is unknown to you (maybe used as part of a central CI/CD system) and is provided as a parameter to your stack, specify that parameter name here. It will override the bucket prefix CDK provides by default for bundled assets. This property only takes effect if you defined the assetsBucketParameterName. The stack containing this contruct needs to have a parameter defined that uses this name. The underlying stacks in this construct that deploy assets will copy the parent stack's value for this property. Default: - No object prefix will be added to your custom assets location. However, if you have overridden something like the 'BucketPrefix' property in your stack synthesizer with a variable like "${AssetsBucketPrefix", you will need to define this property so it doesn't cause a reference error even if the prefix value is blank.
        :param fault_count_percentage_threshold: The percentage of faults for a single ALB to consider an AZ to be unhealthy, this should align with your availability goal. For example 1% or 5%. Default: - 5 (as in 5%)
        :param interval: Dashboard interval. Default: - 1 hour
        :param nat_gateways: (Optional) A map of Availability Zone name to the NAT Gateways in that AZ. Default: - No alarms for NAT Gateways will be created
        :param outlier_threshold: The outlier threshold for determining if an AZ is an outlier for latency or faults. This number is interpreted differently for different outlier algorithms. When used with STATIC, the number should be between 0 and 1 to represent the percentage of errors (like .7) that an AZ must be responsible for to be considered an outlier. When used with CHI_SQUARED, it represents the p value that indicates statistical significance, like 0.05 which means the skew has less than or equal to a 5% chance of occuring. When used with Z_SCORE it indicates how many standard deviations to evaluate for an AZ being an outlier, typically 3 is standard for Z_SCORE. Standard defaults based on the outlier detection algorithm: STATIC: 0.7 CHI_SQUARED: 0.05 Z_SCORE: 2 IQR: 1.5 MAD: 3 Default: - Depends on the outlier detection algorithm selected
        :param packet_loss_impact_percentage_threshold: The amount of packet loss in a NAT GW to determine if an AZ is actually impacted, recommendation is 0.01%. Default: - 0.01 (as in 0.01%)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2e493c3d8cd36f651e9f9f9711d438d697a976a4230c2e5e52c4417edacdac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BasicServiceMultiAZObservabilityProps(
            create_dashboard=create_dashboard,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            outlier_detection_algorithm=outlier_detection_algorithm,
            period=period,
            service_name=service_name,
            application_load_balancers=application_load_balancers,
            assets_bucket_parameter_name=assets_bucket_parameter_name,
            assets_bucket_prefix_parameter_name=assets_bucket_prefix_parameter_name,
            fault_count_percentage_threshold=fault_count_percentage_threshold,
            interval=interval,
            nat_gateways=nat_gateways,
            outlier_threshold=outlier_threshold,
            packet_loss_impact_percentage_threshold=packet_loss_impact_percentage_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="aggregateZonalIsolatedImpactAlarms")
    def aggregate_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]:
        '''The alarms indicating if an AZ has isolated impact from either ALB or NAT GW metrics.'''
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm], jsii.get(self, "aggregateZonalIsolatedImpactAlarms"))

    @aggregate_zonal_isolated_impact_alarms.setter
    def aggregate_zonal_isolated_impact_alarms(
        self,
        value: typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb653ee9a50a44f0c8f3bb74b95b207123391b02252012e94bd58f862084a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregateZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''The name of the service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d12b88d7383f8f7b969be06d5ad4045aa5e9a64ec11b373e1f6dae943557c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="albZonalIsolatedImpactAlarms")
    def alb_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for ALB faults and has isolated impact.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "albZonalIsolatedImpactAlarms"))

    @alb_zonal_isolated_impact_alarms.setter
    def alb_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7adcebc9b688e24f6b9e10073b07a3c32fefd78ef8477f5d5217fdf2f9b0bbb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "albZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationLoadBalancers")
    def application_load_balancers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]]:
        '''The application load balancers being used by the service.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]], jsii.get(self, "applicationLoadBalancers"))

    @application_load_balancers.setter
    def application_load_balancers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88789e6caba89da484557e63f5c3330a408b147ba87d6bded19358a62453813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationLoadBalancers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dashboard")
    def dashboard(self) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard]:
        '''The dashboard that is optionally created.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard], jsii.get(self, "dashboard"))

    @dashboard.setter
    def dashboard(
        self,
        value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed35796b81d97a45b8ace57698158b35bd5c22cc2c035a267efb902f6d4e7f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]]:
        '''The NAT Gateways being used in the service, each set of NAT Gateways are keyed by their Availability Zone Id.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]], jsii.get(self, "natGateways"))

    @nat_gateways.setter
    def nat_gateways(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3831ff8ab7f5a8158659cf2b7298e31b02f7981b1d736a9678980915423f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGateways", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natGWZonalIsolatedImpactAlarms")
    def nat_gw_zonal_isolated_impact_alarms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]]:
        '''The alarms indicating if an AZ is an outlier for NAT GW packet loss and has isolated impact.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]], jsii.get(self, "natGWZonalIsolatedImpactAlarms"))

    @nat_gw_zonal_isolated_impact_alarms.setter
    def nat_gw_zonal_isolated_impact_alarms(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee06f89094957713daf0bd17e2a3a7e2fb27f23ab8621981bec9241a438e2382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGWZonalIsolatedImpactAlarms", value) # pyright: ignore[reportArgumentType]


@jsii.implements(ICanaryMetrics)
class CanaryMetrics(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.CanaryMetrics",
):
    '''Represents metrics for a canary testing a service.'''

    def __init__(
        self,
        *,
        canary_availability_metric_details: IOperationMetricDetails,
        canary_latency_metric_details: IOperationMetricDetails,
    ) -> None:
        '''
        :param canary_availability_metric_details: The canary availability metric details.
        :param canary_latency_metric_details: The canary latency metric details.
        '''
        props = CanaryMetricProps(
            canary_availability_metric_details=canary_availability_metric_details,
            canary_latency_metric_details=canary_latency_metric_details,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="canaryAvailabilityMetricDetails")
    def canary_availability_metric_details(self) -> IOperationMetricDetails:
        '''The canary availability metric details.'''
        return typing.cast(IOperationMetricDetails, jsii.get(self, "canaryAvailabilityMetricDetails"))

    @builtins.property
    @jsii.member(jsii_name="canaryLatencyMetricDetails")
    def canary_latency_metric_details(self) -> IOperationMetricDetails:
        '''The canary latency metric details.'''
        return typing.cast(IOperationMetricDetails, jsii.get(self, "canaryLatencyMetricDetails"))


@jsii.implements(ICanaryTestMetricsOverride)
class CanaryTestMetricsOverride(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.CanaryTestMetricsOverride",
):
    '''Provides overrides for the default metric settings used for the automatically created canary tests.'''

    def __init__(
        self,
        *,
        alarm_statistic: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        fault_alarm_threshold: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        success_alarm_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param alarm_statistic: The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9". Default: - This property will use the default defined for the service
        :param datapoints_to_alarm: The number of datapoints to alarm on for latency and availability alarms. Default: - This property will use the default defined for the service
        :param evaluation_periods: The number of evaluation periods for latency and availabiltiy alarms. Default: - This property will use the default defined for the service
        :param fault_alarm_threshold: The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%. Default: - This property will use the default defined for the service
        :param period: The period for the metrics. Default: - This property will use the default defined for the service
        :param success_alarm_threshold: The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%. Default: - This property will use the default defined for the service
        '''
        props = CanaryTestMetricsOverrideProps(
            alarm_statistic=alarm_statistic,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            fault_alarm_threshold=fault_alarm_threshold,
            period=period,
            success_alarm_threshold=success_alarm_threshold,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="alarmStatistic")
    def alarm_statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic used for alarms, for availability metrics this should be "Sum", for latency metrics it could something like "p99" or "p99.9".'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmStatistic"))

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints to alarm on for latency and availability alarms.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "datapointsToAlarm"))

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of evaluation periods for latency and availabiltiy alarms.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationPeriods"))

    @builtins.property
    @jsii.member(jsii_name="faultAlarmThreshold")
    def fault_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with fault metrics, for example if measuring fault rate, the threshold may be 1, meaning you would want an alarm that triggers if the fault rate goes above 1%.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "faultAlarmThreshold"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period for the metrics.'''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="successAlarmThreshold")
    def success_alarm_threshold(self) -> typing.Optional[jsii.Number]:
        '''The threshold for alarms associated with success metrics, for example if measuring success rate, the threshold may be 99, meaning you would want an alarm that triggers if success drops below 99%.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successAlarmThreshold"))


@jsii.implements(IContributorInsightRuleDetails)
class ContributorInsightRuleDetails(
    metaclass=jsii.JSIIMeta,
    jsii_type="multi-az-observability.ContributorInsightRuleDetails",
):
    '''The contributor insight rule details for creating an insight rule.'''

    def __init__(
        self,
        *,
        availability_zone_id_json_path: builtins.str,
        fault_metric_json_path: builtins.str,
        instance_id_json_path: builtins.str,
        log_groups: typing.Sequence[_aws_cdk_aws_logs_ceddda9d.ILogGroup],
        operation_name_json_path: builtins.str,
        success_latency_metric_json_path: builtins.str,
    ) -> None:
        '''
        :param availability_zone_id_json_path: The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.
        :param fault_metric_json_path: The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.
        :param instance_id_json_path: The JSON path to the instance id field in the log files, only required for server-side rules.
        :param log_groups: The log groups where CloudWatch logs for the operation are located. If this is not provided, Contributor Insight rules cannot be created.
        :param operation_name_json_path: The path in the log files to the field that identifies the operation the log file is for.
        :param success_latency_metric_json_path: The path in the log files to the field that indicates the latency for the response. This could either be success latency or fault latency depending on the alarms and rules you are creating.
        '''
        props = ContributorInsightRuleDetailsProps(
            availability_zone_id_json_path=availability_zone_id_json_path,
            fault_metric_json_path=fault_metric_json_path,
            instance_id_json_path=instance_id_json_path,
            log_groups=log_groups,
            operation_name_json_path=operation_name_json_path,
            success_latency_metric_json_path=success_latency_metric_json_path,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdJsonPath")
    def availability_zone_id_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the Availability Zone Id that the request was handled in, for example { "AZ-ID": "use1-az1" } would have a path of $.AZ-ID.'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneIdJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="faultMetricJsonPath")
    def fault_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies if the response resulted in a fault, for example { "Fault" : 1 } would have a path of $.Fault.'''
        return typing.cast(builtins.str, jsii.get(self, "faultMetricJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdJsonPath")
    def instance_id_json_path(self) -> builtins.str:
        '''The JSON path to the instance id field in the log files, only required for server-side rules.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="logGroups")
    def log_groups(self) -> typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log groups where CloudWatch logs for the operation are located.

        If
        this is not provided, Contributor Insight rules cannot be created.
        '''
        return typing.cast(typing.List[_aws_cdk_aws_logs_ceddda9d.ILogGroup], jsii.get(self, "logGroups"))

    @builtins.property
    @jsii.member(jsii_name="operationNameJsonPath")
    def operation_name_json_path(self) -> builtins.str:
        '''The path in the log files to the field that identifies the operation the log file is for.'''
        return typing.cast(builtins.str, jsii.get(self, "operationNameJsonPath"))

    @builtins.property
    @jsii.member(jsii_name="successLatencyMetricJsonPath")
    def success_latency_metric_json_path(self) -> builtins.str:
        '''The path in the log files to the field that indicates the latency for the response.

        This could either be success latency or fault
        latency depending on the alarms and rules you are creating.
        '''
        return typing.cast(builtins.str, jsii.get(self, "successLatencyMetricJsonPath"))


__all__ = [
    "AddCanaryTestProps",
    "AvailabilityZoneMapper",
    "AvailabilityZoneMapperProps",
    "BasicServiceMultiAZObservability",
    "BasicServiceMultiAZObservabilityProps",
    "CanaryMetricProps",
    "CanaryMetrics",
    "CanaryTestMetricsOverride",
    "CanaryTestMetricsOverrideProps",
    "ContributorInsightRuleDetails",
    "ContributorInsightRuleDetailsProps",
    "IAvailabilityZoneMapper",
    "IBasicServiceMultiAZObservability",
    "ICanaryMetrics",
    "ICanaryTestMetricsOverride",
    "IContributorInsightRuleDetails",
    "IInstrumentedServiceMultiAZObservability",
    "IOperation",
    "IOperationMetricDetails",
    "IService",
    "IServiceAlarmsAndRules",
    "IServiceMetricDetails",
    "InstrumentedServiceMultiAZObservability",
    "InstrumentedServiceMultiAZObservabilityProps",
    "MetricDimensions",
    "NetworkConfigurationProps",
    "Operation",
    "OperationMetricDetails",
    "OperationMetricDetailsProps",
    "OperationProps",
    "OutlierDetectionAlgorithm",
    "Service",
    "ServiceMetricDetails",
    "ServiceMetricDetailsProps",
    "ServiceProps",
]

publication.publish()

def _typecheckingstub__ead8ba42e0ffe8c4a0a0bf4162d6495fdaa628aafcb33fec909f0b0d4326fd11(
    *,
    load_balancer: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2,
    request_count: jsii.Number,
    schedule: builtins.str,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    http_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_tls_errors: typing.Optional[builtins.bool] = None,
    network_configuration: typing.Optional[typing.Union[NetworkConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
    post_data: typing.Optional[builtins.str] = None,
    regional_request_count: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2806dcb155fd8f09292d7b6d39dfa33ee61c19d88b123657eeca548a43253f8a(
    *,
    availability_zone_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58ece35f77caa4f37dc329d2df9a0806a48ec2ac96819d5b3bec961e5f2b3d9(
    *,
    create_dashboard: builtins.bool,
    datapoints_to_alarm: jsii.Number,
    evaluation_periods: jsii.Number,
    outlier_detection_algorithm: OutlierDetectionAlgorithm,
    period: _aws_cdk_ceddda9d.Duration,
    service_name: builtins.str,
    application_load_balancers: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]] = None,
    assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
    assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
    fault_count_percentage_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    nat_gateways: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]] = None,
    outlier_threshold: typing.Optional[jsii.Number] = None,
    packet_loss_impact_percentage_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5fbbcf0f0c157e36d061ece26f53404876732a0a0a2c1648fd38273b093052(
    *,
    canary_availability_metric_details: IOperationMetricDetails,
    canary_latency_metric_details: IOperationMetricDetails,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6b739570b1ecc0dd5ae1bb7e43518f9ab0537bdee33a1c174643779b6a45e8(
    *,
    alarm_statistic: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    fault_alarm_threshold: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    success_alarm_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928d51c92a749c4248e6b7fae43ace2d014ae6bd6898d34469f5545cdf0a040(
    *,
    availability_zone_id_json_path: builtins.str,
    fault_metric_json_path: builtins.str,
    instance_id_json_path: builtins.str,
    log_groups: typing.Sequence[_aws_cdk_aws_logs_ceddda9d.ILogGroup],
    operation_name_json_path: builtins.str,
    success_latency_metric_json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef15425f4b53258b8a7fee384baa9e4b26d617de1a46e56aa7ce30e5a4b29d8(
    value: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c31c9fd1728244a4034a26db6d199f09ec0bff3d04796990d4e5baef0044fa(
    value: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdf4b5c85f9b4b6174b5ab3e84d47061a4a97fe351e51bce1ac911b3cf0061b(
    value: _aws_cdk_ceddda9d.CustomResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de18979b5bc3fcfd30bce0f73b892dbfd338671e9cd2174b608ac2ef41387108(
    availability_zone_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918cea02a7a8c8236a47216fd967f551b424b708cc0a0d85643145178326f10d(
    letter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a969f2acb8541c226aff52f673143ec2267780a385a6a4fddf08d234160bfa3c(
    availability_zone_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030ef2a67c593ef76c9032ba6818f14ff588183846df4d3bf9eafe05f85cbc92(
    availability_zone_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc7f0c8bc56783d26fef73e3aa44e78135e00fa8e48244cfd5417513d772f93(
    availability_zone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da8d7df1ecf8a83ea92bbac9f862e0a3e70c859e8a1bf5c423f00a98bde0158(
    value: typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e600397d75137d2e977180f7907ce6924e8b754bfcf018df4e79d7a6396bcbdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9699df8dc509d1cae25263f3edb070e0c0d45c937afd99759d98277e85efb3(
    value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0eab8db5587e70b721058fb0c3b9b12ab74016f9e83fdc74e086cfbd34f766(
    value: typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c77fecc2592ab95dae42a3cba29f05b42a3746148a483ee8438d00b23cc35ae(
    value: typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9d785bf0c641fffc85e06501ae14ba6754f0663649bdb005dfa5eb936482af(
    value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bde07ece32c22e2ed407a2bd209e7524e6cff22e9de936befaa0909e4557fb(
    operation: IOperation,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8626bf78b2e0e32e118334d17c1e620cf433211d5939817daa86d322b2191b5(
    value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f953b292bd0ef9e32eb4dceb7a72cabb187dd71dcaf0a427359258f774229d64(
    value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f807c1960ac162df87afc2feba30c47a91d0af00d78bda7a2fa0459180c1ed93(
    value: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc293180ad805fbcb81ccd21086bb19e1bb36c6fa11a9bc231ac5dd4edb0e9f(
    value: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baf67c32f5dbd43108c4cab5d950436bc928c5c7f155fe0d74070c41cdb3dc6(
    value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00de5a388f5dc72443906156fb11ab31d9a2aa725f6682a0da502b7ae776045e(
    value: typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2274d795072407a74901eb5921d753f3d8a0702daab149426e8d5487a1379f96(
    value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fb5ac43ab62a6bd0808b3b73124460d735c87caeb435f8a55050e78d9bf5a5(
    value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e3399e5b1fb72c387324d7303207d55300674a9aceeda9884cbd2c515a112d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    outlier_detection_algorithm: OutlierDetectionAlgorithm,
    service: IService,
    assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
    assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
    create_dashboards: typing.Optional[builtins.bool] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    outlier_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30d92d75ef7cead0db6fa29895cdd2786739a400f56564f0fdff625741fee87(
    *,
    outlier_detection_algorithm: OutlierDetectionAlgorithm,
    service: IService,
    assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
    assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
    create_dashboards: typing.Optional[builtins.bool] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    outlier_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0231732b77fe1623a009bf60b8908d730dde31c8d87942d8422f2559384453(
    static_dimensions: typing.Mapping[builtins.str, builtins.str],
    availability_zone_id_key: builtins.str,
    region_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdced2a5b7053ef36dcb9443b3f7e91e32352c16565af3c8421b9c6397f7d63(
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddc4ff234cfbd9f867ff3ee124a1f90bd70f935be37852933515593c920f3d8(
    availability_zone_id: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316caab4a239cc5e349828bf51796599dd691b46028d84c569f7de2dbc4b3499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f4b0a06877f54397ed9dc9b6e220aee3f221b18b480882fc715fe0974010f7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a832567c9a2a7011d2c4689c1f3e7d90d5fd6538d40f7833c9d813035ca6b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfe87bdb6a05e67c7bb0ac6cb230997c6ff554b711f2126ce0a751647097eff(
    *,
    subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992972ebf895c0ea7d9905239a632ff039b0c8d79aac7b7b31905fecc6c595ea(
    props: typing.Union[OperationMetricDetailsProps, typing.Dict[builtins.str, typing.Any]],
    default_props: IServiceMetricDetails,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf637b714cdbee8ae242e21c6b369adfefc190ccf00d0385165c32c2fc2f214(
    *,
    metric_dimensions: MetricDimensions,
    operation_name: builtins.str,
    alarm_statistic: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    fault_alarm_threshold: typing.Optional[jsii.Number] = None,
    fault_metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphed_fault_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphed_success_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_namespace: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    success_alarm_threshold: typing.Optional[jsii.Number] = None,
    success_metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d484fa77c0f6fbd2c974e219a3a6ddd645dec7dda3146ffc0cc68275ee2f24(
    *,
    critical: builtins.bool,
    http_methods: typing.Sequence[builtins.str],
    operation_name: builtins.str,
    path: builtins.str,
    server_side_availability_metric_details: IOperationMetricDetails,
    server_side_latency_metric_details: IOperationMetricDetails,
    service: IService,
    canary_metric_details: typing.Optional[ICanaryMetrics] = None,
    canary_test_availability_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
    canary_test_latency_metrics_override: typing.Optional[ICanaryTestMetricsOverride] = None,
    canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
    opt_out_of_service_created_canary: typing.Optional[builtins.bool] = None,
    server_side_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ac8fba10f62a93023efbb6d4c5f64df730e4d49fff16f85614294cb5a334ea(
    operation: IOperation,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7149a4b69b51765276c5603c7584f1951ed8c9f5eedf87441b153b5a83380d(
    *,
    alarm_statistic: builtins.str,
    datapoints_to_alarm: jsii.Number,
    evaluation_periods: jsii.Number,
    fault_alarm_threshold: jsii.Number,
    fault_metric_names: typing.Sequence[builtins.str],
    metric_namespace: builtins.str,
    period: _aws_cdk_ceddda9d.Duration,
    success_alarm_threshold: jsii.Number,
    success_metric_names: typing.Sequence[builtins.str],
    unit: _aws_cdk_aws_cloudwatch_ceddda9d.Unit,
    graphed_fault_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphed_success_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8292313fdf86d8fe32f33cf45a68ef9b39914f11b67335d49298260fca9f00de(
    *,
    availability_zone_names: typing.Sequence[builtins.str],
    base_url: builtins.str,
    default_availability_metric_details: IServiceMetricDetails,
    default_latency_metric_details: IServiceMetricDetails,
    fault_count_threshold: jsii.Number,
    period: _aws_cdk_ceddda9d.Duration,
    service_name: builtins.str,
    canary_test_props: typing.Optional[typing.Union[AddCanaryTestProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_contributor_insight_rule_details: typing.Optional[IContributorInsightRuleDetails] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ILoadBalancerV2] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585c51e84a8f3bb791f23a2e17e84165faf2c7da42fe1473e7d7f07dee294aec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cde3a0b835c7ec259cfd42c2b95b6eead298927cf17be162ffa4ef19fc0e1d0(
    availability_zone_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24f7608ecd89d63b70f11709bcb35d148188c2d62d0a242b6be7aadb5e3a585(
    letter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7f6db7dd2a1e9ccffcfa6c84fb6ebdcb7f41c6f1aab7df8066380703be4fa5(
    availability_zone_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bab0ae038b9ffefe5b182837771bfd45222d6159b5d837c778fda0cb0010081(
    availability_zone_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa84169ecad60d48c1cdcda563723475c0216ac384a78ceb4382bdd1a919273(
    availability_zone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af51bda9380215b07fe0b0958367d23c488575d1774e7f0bb97f444574aaab4(
    value: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29194ef39eaaecc9f9f91e9a083f2137bdcb4ac882afc1583175e2200b01c691(
    value: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e28c12ab3649a0e6b8be31dda54ffcb3ab7079fd90428cc535ec617df0e8687(
    value: _aws_cdk_ceddda9d.CustomResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2e493c3d8cd36f651e9f9f9711d438d697a976a4230c2e5e52c4417edacdac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    create_dashboard: builtins.bool,
    datapoints_to_alarm: jsii.Number,
    evaluation_periods: jsii.Number,
    outlier_detection_algorithm: OutlierDetectionAlgorithm,
    period: _aws_cdk_ceddda9d.Duration,
    service_name: builtins.str,
    application_load_balancers: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]] = None,
    assets_bucket_parameter_name: typing.Optional[builtins.str] = None,
    assets_bucket_prefix_parameter_name: typing.Optional[builtins.str] = None,
    fault_count_percentage_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    nat_gateways: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]] = None,
    outlier_threshold: typing.Optional[jsii.Number] = None,
    packet_loss_impact_percentage_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb653ee9a50a44f0c8f3bb74b95b207123391b02252012e94bd58f862084a61(
    value: typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d12b88d7383f8f7b969be06d5ad4045aa5e9a64ec11b373e1f6dae943557c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adcebc9b688e24f6b9e10073b07a3c32fefd78ef8477f5d5217fdf2f9b0bbb4(
    value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88789e6caba89da484557e63f5c3330a408b147ba87d6bded19358a62453813(
    value: typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed35796b81d97a45b8ace57698158b35bd5c22cc2c035a267efb902f6d4e7f04(
    value: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3831ff8ab7f5a8158659cf2b7298e31b02f7981b1d736a9678980915423f89(
    value: typing.Optional[typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee06f89094957713daf0bd17e2a3a7e2fb27f23ab8621981bec9241a438e2382(
    value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm]],
) -> None:
    """Type checking stubs"""
    pass
