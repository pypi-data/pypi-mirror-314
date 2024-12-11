r'''
# AWS Thinkbox Deadline Construct Library

The `aws-rfdk/deadline` sub-module contains Deadline-specific constructs that can be used to deploy and manage a Deadline render farm in the cloud.

```python
import * as deadline from 'aws-rfdk/deadline';
```

---


***Note:** RFDK constructs currently support Deadline 10.1.9 and later, unless otherwise stated.*

---


* [Configure Spot Event Plugin](#configure-spot-event-plugin) (supports Deadline 10.1.12 and later)

  * [Saving Spot Event Plugin Options](#saving-spot-event-plugin-options)
  * [Saving Spot Fleet Request Configurations](#saving-spot-fleet-request-configurations)
* [Deadline Secrets Management Considerations](#deadline-secrets-management-considerations)

  * [Using Dedicated Subnets for Deadline Components](#using-dedicated-subnets-for-deadline-components)
* [Render Queue](#render-queue)

  * [Docker Container Images](#render-queue-docker-container-images)
  * [Encryption](#render-queue-encryption)
  * [Health Monitoring](#render-queue-health-monitoring)
  * [Deletion Protection](#render-queue-deletion-protection)
  * [Subnet Placement](#render-queue-subnet-placement)
  * [Configuring Deadline Secrets Management](#configuring-deadline-secrets-management-on-the-render-queue)
* [Repository](#repository)

  * [Configuring Deadline Client Connections](#configuring-deadline-client-connections)
  * [Configuring Deadline Secrets Management](#configuring-deadline-secrets-management-on-the-repository)
* [Spot Event Plugin Fleet](#spot-event-plugin-fleet) (supports Deadline 10.1.12 and later)

  * [Changing Default Options](#changing-default-options)
  * [Subnet Placement](#spot-event-plugin-fleet-subnet-placement)
* [Stage](#stage)

  * [Staging Docker Recipes](#staging-docker-recipes)
* [ThinkboxDockerImages](#thinkbox-docker-images)
* [Usage Based Licensing](#usage-based-licensing-ubl)

  * [Docker Container Images](#usage-based-licensing-docker-container-images)
  * [Uploading Binary Secrets to SecretsManager](#uploading-binary-secrets-to-secretsmanager)
* [VersionQuery](#versionquery)
* [Worker Instance Fleet](#worker-instance-fleet)

  * [Health Monitoring](#worker-instance-fleet-health-monitoring)
  * [Custom Worker Instance Startup](#custom-worker-instance-startup)
  * [Subnet Placement](#worker-instance-fleet-subnet-placement)

## Configure Spot Event Plugin

![architecture diagram](../../docs/diagrams/deadline/ConfigureSpotEventPlugin.svg)

The [Spot Event Plugin](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html) can scale cloud-based EC2 Spot instances dynamically based on the queued Jobs and Tasks in the Deadline Database. It associates a Spot Fleet Request with named Deadline Worker Groups, allowing multiple Spot Fleets with different hardware and software specifications to be launched for different types of Jobs based on their Group assignment.

The `ConfigureSpotEventPlugin` construct has two main responsibilities:

* Construct a [Spot Fleet Request](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-requests.html) configuration from the list of [Spot Event Plugin Fleets](#spot-event-plugin-fleet).
* Modify and save the options of the Spot Event Plugin itself. See [Deadline Documentation](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options).

---


**Note:** This construct will configure the Spot Event Plugin, but the Spot Fleet Requests will not be created unless you:

* Submit the job with the assigned Deadline Group and Deadline Pool. See [Deadline Documentation](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-submitting.html#submitting-jobs).

---
---


***Note:** Disable 'Allow Workers to Perform House Cleaning If Pulse is not Running' in the 'Configure Repository Options' when using Spot Event Plugin. See [Deadline Documentation](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#prerequisites).*

---
---


***Note:** Any resources created by the Spot Event Plugin will not be deleted with `cdk destroy`. Make sure that all such resources (e.g. Spot Fleet Request or Fleet Instances) are cleaned up, before destroying the stacks. Disable the Spot Event Plugin by setting 'state' property to 'SpotEventPluginState.DISABLED' or via Deadline Monitor, ensure you shutdown all Pulse instances and then terminate any Spot Fleet Requests in the AWS EC2 Instance Console.*

---


### Saving Spot Event Plugin Options

To set the Spot Event Plugin options use `configuration` property of the `ConfigureSpotEventPlugin` construct:

```python
const vpc = new Vpc(/* ... */);
const renderQueue = new RenderQueue(stack, 'RenderQueue', /* ... */);

const spotEventPluginConfig = new ConfigureSpotEventPlugin(stack, 'ConfigureSpotEventPlugin', {
  vpc,
  renderQueue: renderQueue,
  configuration: {
    enableResourceTracker: true,
  },
});
```

This property is optional, so if you don't provide it, the default Spot Event Plugin Options will be used.

### Saving Spot Fleet Request Configurations

Use the `spotFleets` property to construct the Spot Fleet Request Configurations from a given [Spot Event Plugin Fleet](#spot-event-plugin-fleet):

```python
const fleet = new SpotEventPluginFleet(stack, 'SpotEventPluginFleet', /* ... */);

const spotEventPluginConfig = new ConfigureSpotEventPlugin(this, 'ConfigureSpotEventPlugin', {
  vpc,
  renderQueue: renderQueue,
  spotFleets: [
    fleet,
  ],
});
```

### Spot Event Plugin Fleet Subnet Placement

We highly recommend creating dedicated subnets for the Spot Event Plugin Fleets in your farm as it is considered best practice and is especially important if you are using
Deadline Secrets Management (see [Deadline Secrets Management Considerations](#using-dedicated-subnets-for-deadline-components)).

The following example creates a dedicated subnet group for a `SpotEventPluginFleet`:

```python
const vpc = new Vpc(this, 'Vpc', {
  // ...
  subnetConfiguration: [
    // ...

    // Provide a subnet configuration for the SpotEventPluginFleet subnet group
    {
      name: 'SpotEventPluginFleetSubnets',
      subnetType: SubnetType.PRIVATE_WITH_EGRESS,
      cidrMask: 20,
    },

    // ...
  ],
  // ...
});

// ...

const fleet = new SpotEventPluginFleet(stack, 'SpotEventPluginFleet', {
  // ...
  vpc,

  // Select the dedicated WorkerInstanceFleet subnets to put the worker nodes in
  vpcSubnets: {
    subnetGroupName: "SpotEventPluginFleetSubnets",
  },

  // ...
});

new ConfigureSpotEventPlugin(stack, 'ConfigureSpotEventPlugin', {
  vpc,
  spotFleets: [
    fleet,
  ],
  // ...
})
```

## Deadline Secrets Management Considerations

### Using Dedicated Subnets for Deadline Components

When Secrets Management is enabled on the `Repository` construct, RFDK will handle configuring [identity registration settings](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#automatically-registering-identities-and-adding-roles)
using the subnets of the RFDK constructs involved. Because a construct's resources can be assigned any IP address in the subnet range, RFDK must create rules that cover the entire subnet.
These identity registration settings work like an IP-address-based allowlist that give machines with IP addresses that match a rule access to secrets in Deadline, based on their [assigned role](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles).
The components that need identity registration settings created for them include, but are not limited to, the following:

* The Application Load Balancer of the [`RenderQueue`](#render-queue)
* Deadline workers in a [`WorkerInstanceFleet`](#worker-instance-fleet)
* Deadline workers created by the Spot Event Plugin, which are configured by the [`ConfigureSpotEventPlugin`](#configure-spot-event-plugin) construct.

RFDK creates auto-registration rules based on the Classless Inter-Domain Routing (CIDR) range of the subnet(s) that a component can be deployed into. Therefore, we highly recommend
creating a dedicated subnet for each component above for the following reasons:

1. RFDK automatically configures Deadline Secrets Management [identity registration settings](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-registration-settings-ref-label).
   These settings are configured such that the Render Queue will register identities that are created by Deadline Clients (e.g. `UsageBasedLicensing`, `WorkerInstanceFleet`, and `SpotEventPluginFleet`)
   connecting via the Render Queue's Application Load Balancer (ALB). Deadline requires that you specify trusted load balancers when configuring identity registration settings by their connecting
   IP address. Application Load Balancers can scale to use any available IP address in the subnets, so the full subnet IP range is used by RFDK. For this reason, we recommend dedicating subnets
   exclusively for the Render Queue's ALB.
2. The size of the subnet can be limited to only what is necessary for your workload, avoiding an overly permissive auto-registration rule.

Please consult the [`All-In-AWS-Infrastructure-Basic` example CDK application](https://github.com/aws/aws-rfdk/blob/release/examples/deadline/All-In-AWS-Infrastructure-Basic) for a reference implementation that demonstrates dedicated subnets.

For more details on dedicated subnet placements, see:

* [Render Queue Subnet Placement](#render-queue-subnet-placement)
* [Worker Instance Fleet Subnet Placement](#worker-instance-fleet-subnet-placement)
* [Spot Event Plugin Fleet Subnet Placement](#spot-event-plugin-fleet-subnet-placement)

## Render Queue

![architecture diagram](../../docs/diagrams/deadline/RenderQueue.svg)

The `RenderQueue` is the central service of a Deadline render farm. It consists of the following components:

* **Deadline Repository** - The repository that initializes the persistent data schema used by Deadline such as job information, connected workers, rendered output files, etc.
* **Deadline Remote Connection Server (RCS)** - The central server that all Deadline applications connect to. The RCS contains the core business logic to manage the render farm.

The `RenderQueue` construct sets up the RCS and configures it to communicate with the Repository and to listen for requests using the configured protocol (HTTP or HTTPS). Docker container images are used to deploy the `RenderQueue` as a fleet of instances within an Elastic Container Service (ECS) cluster. This fleet of instances is load balanced by an [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) which has built-in health monitoring functionality that can be configured through this construct.

The following example outlines how to construct a `RenderQueue`:

```python
const version = new VersionQuery(stack, 'Version', {
  version: '1.2.3.4',
});
const images = new ThinkboxDockerImages(stack, 'Image', {
  version,
  // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
  // of the AWS Customer Agreement and AWS Intellectual Property License.
  userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
});
const repository = new Repository(stack, 'Repository', { /* ...*/});

const renderQueue = new RenderQueue(stack, 'RenderQueue', {
  vpc: vpc,
  images: images.forRenderQueue(),
  version: version,
  repository: repository,
});
```

### Render Queue Docker Container Images

The `RenderQueue` currently requires only one Docker container image for the Deadline Remote Connection Server (RCS).

AWS Thinkbox provides Docker recipes and images that set these up for you. These can be accessed with the `ThinkboxDockerRecipes` and `ThinkboxDockerImages` constructs (see [Staging Docker Recipes](#staging-docker-recipes) and [Thinkbox Docker Images](#thinkbox-docker-images) respectively).

If you need to customize the Docker images of your Render Queue, it is recommended that you stage the recipes and modify them as desired. Once staged to a directory, consult the `README.md` file in the root for details on how to extend the recipes.

### Render Queue Encryption

The `RenderQueue` provides end-to-end encryption of communications and data at rest. However, it currently does not do any client validation or application authentication due to limitations with Application Load Balancers that made it necessary to disable Deadline Worker TLS certificate authentication.

---


***Note:** Be extra careful when setting up security group rules that govern access to the `RenderQueue` and, for the machines that do have access to it, ensure you trust the Operating System as well as any software being used.*

---


### Render Queue Health Monitoring

The `RenderQueue` construct leverages the built-in health monitoring functionality provided by Application Load Balancers. The health check grace period and interval can be configured by specifying the `healthCheckConfig` property of the construct. For more information, see [Application Load Balancer Health Checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html).

### Render Queue Deletion Protection

By default, the Load Balancer in the `RenderQueue` has [deletion protection](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#deletion-protection) enabled to ensure that it does not get accidentally deleted. This also means that it cannot be automatically destroyed by CDK when you destroy your stack and must be done manually (see [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#deletion-protection)).

You can specify deletion protection with a property in the `RenderQueue`:

```python
const renderQueue = new RenderQueue(stack, 'RenderQueue', {
  //...
  deletionProtection: false
});
```

### Render Queue Subnet Placement

We highly recommend creating dedicated subnets for the Render Queue's [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html)
that will only be used by the load balancer. Using dedicated subnets for load balancers is considered best practice and is especially important if you are using
Deadline Secrets Management (see [Deadline Secrets Management Considerations](#using-dedicated-subnets-for-deadline-components)).

The following example creates a dedicated subnet group for the `RenderQueue` to use for its Application Load balancer:

```python
const vpc = new Vpc(this, 'Vpc', {
  // ...
  subnetConfiguration: [
    // ...

    // Provide a subnet configuration for the Render Queue subnet group
    {
      name: 'RenderQueueALBSubnets',
      subnetType: SubnetType.PRIVATE_WITH_EGRESS,
      cidrMask: 27,
    },

    // ...
  ],
  // ...
});

// ...

const renderQueue = new RenderQueue(stack, 'RenderQueue', {
  // ...
  vpc,

  // Select the dedicated Render Queue subnets to put the ALB in
  vpcSubnetsAlb: vpc.selectSubnets({ subnetGroupName: 'RenderQueueALBSubnets' }),

  // ...
});
```

Application Load Balancers have requirements for the subnets they are deployed into, such as requiring that each subnet be from a different Availability Zone and that each subnet
have a CIDR block with at least a `/27` bitmask and at least 8 free IP addresses per subnet. For the full list of requirements, please see the
[Elastic Load Balancing documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#subnets-load-balancer).

### Configuring Deadline Secrets Management on the Render Queue

When [Deadline Secrets Management](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html) is enabled on the `Repository` construct,
the `RenderQueue` will automatically configure itself as a [Server role](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles) in Deadline Secrets Management.

For more information on using Deadline Secrets Management in RFDK, please see the [RFDK Developer Guide](https://docs.aws.amazon.com/rfdk/latest/guide/deadline-secrets-management-rfdk.html).

## Repository

![architecture diagram](../../docs/diagrams/deadline/Repository.svg)

The `Repository` contains the central database and file system used by Deadline. An EC2 instance is temporarily created to run the Deadline Repository installer which configures the database and file system. This construct has optional parameters for the database and file system to use, giving you the option to either provide your own resources or to have the construct create its own. Log messages emitted by the construct are forwarded to CloudWatch via a CloudWatch agent.

You can create a `Repository` like this:

```python
const repository = new Repository(stack, 'Repository', {
  vpc: props.vpc,
  version: new VersionQuery(stack, 'Version', {
    version: '1.2.3.4',
  }),
});
```

### Configuring Deadline Client Connections

Deadline Clients can be configured to connect directly to the `Repository`, which will:

* Allow ingress traffic to database & file system Security Groups
* Create IAM Permissions for database & file system
* Mount the Repository file system via [UserData](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

Deadline Clients can be configured either in ECS or EC2.

#### 1. Configure Deadline Client in ECS

An ECS Container Instance and Task Definition for deploying Deadline Client can be configured to directly connect to the `Repository`. A mapping of environment variables and ECS [`MountPoint`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ecs.MountPoint.html)s are produced which can be used to configure a [`ContainerDefinition`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ecs.ContainerDefinition.html) to connect to the `Repository`.

The example below demonstrates configuration of Deadline Client in ECS:

```python
const taskDefinition = new Ec2TaskDefinition(stack, 'TaskDefinition');
const ecsConnection = repository.configureClientECS({
      containerInstances: /* ... */,
      containers: {
        taskDefinition
      },
    });

const containerDefinition = taskDefinition.addContainer('ContainerDefinition', {
  image: /* ... */,
  environment: ecsConnection.containerEnvironment
});
containerDefinition.addMountPoints(ecsConnection.readWriteMountPoint);
```

#### 2. Configure Deadline Client on EC2

An EC2 instance running Deadline Client can be configured to directly connect to the `Repository`.

The example below demonstrates configuration of Deadline Client in an EC2 instance:

```python
const instance = new Instance(stack, 'Instance', {
  vpc,
  instanceType: new InstanceType(/* ... */),
  machineImage: MachineImage.latestAmazonLinux()
});
repository.configureClientInstance({
  host: instance,
  mountPoint: '/mnt/repository'
});
```

### Configuring Deadline Secrets Management on the Repository

When using Deadline 10.1.19 or higher, RFDK enables [Deadline Secrets Management](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html) on the `Repository` by default. To perform administrator functions for Deadline Secrets Management, credentials need to be created. You can either create your own in an AWS Secrets Manager Secret and have it imported into your RFDK app, or have RFDK generate the credentials and create the Secret for you.

When RFDK generates the administrator credentials, it sets the Secret's removal policy to `RETAIN` so that you will not lose them if you destroy the CloudFormation Stack that they are in. If you do want to delete this Secret, you will have to destroy it manually or change the `credentialsRemovalPolicy` to `DESTROY`. If you destroy the Stack that contains your Secret and its policy set to `RETAIN`, your existing Secret will be orphaned from your RFDK application and re-deploying the Stack will generate a new one. To help prevent orphaning a Secret that contains administrator credentials that are still in use, RFDK places it in the Stack that contains your database, so that their lifecycles are in sync.

If your database is imported into your RFDK app rather than being generated by it, RFDK will not generate credentials during deployment. You must create your own Secret with the credentials you'd like to use and [import it](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-secretsmanager-readme.html#importing-secrets).

If you would like to use your own credentials for Deadline Secrets Management, you can do so by storing them in AWS Secrets Manager and providing them to the `Repository` construct. The Secret must be a JSON document with the following format:

```jsonc
{
  // Replace the values of these fields with your own values
  "username": "your_username",
  "password": "your_password"
}
```

---


***Note:** The `password` should be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one symbol and one number.*

---


You can then provide the ARN of the Secret containing your credentials to the `Repository` construct:

```python
const secretsManagementCredentials = Secret.fromSecretCompleteArn(
  this,
  'DeadlineSecretsManagementCredentials',
  // Replace with your Secret ARN
  'yourSecretArn',
);

const repository = new Repository(this, 'Repository', {
  vpc,
  version,
  secretsManagementSettings: {
    enabled: true,
    credentials: secretsManagementCredentials,
  },
});
```

For further details, please consult the RFDK developer guide topic on [using Deadline Secrets Management in RFDK](https://docs.aws.amazon.com/rfdk/latest/guide/deadline-secrets-management-rfdk.html#using-deadline-secrets-management-in-rfdk). Please note that there is a specific process for [rotating your administrator credentials](https://docs.aws.amazon.com/rfdk/latest/guide/deadline-secrets-management-rfdk.html#rotating-deadline-secrets-management-administrator-credentials).

**WARNING:** Once the repository has been deployed and the administrator credentials are configured, changing the credential values in the Secret and re-deploying your RFDK app will not update the credentials in the Deadline Repository. You must first change the credentials in the Deadline Repository using the instructions linked above. Doing this incorrectly may cause the RFDK Render Queue to stop functioning. If you have done this and cannot recover the previous credentials, you will need to follow instructions for [forgotten Deadline Secrets Management administrator credentials](https://docs.aws.amazon.com/rfdk/latest/guide/deadline-secrets-management-rfdk.html#forgotten-deadline-secrets-management-administrator-credentials).

## Spot Event Plugin Fleet

![architecture diagram](../../docs/diagrams/deadline/SpotEventPluginFleet.svg)

This construct represents a Spot Fleet launched by the [Deadline's Spot Event Plugin](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html) from the [Spot Fleet Request Configuration](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#spot-fleet-request-configurations). The construct itself doesn't create a Spot Fleet Request, but creates all the required resources to be used in the Spot Fleet Request Configuration.

This construct is expected to be used as an input to the [ConfigureSpotEventPlugin](#configure-spot-event-plugin) construct. `ConfigureSpotEventPlugin` construct will generate a Spot Fleet Request Configuration from each provided `SpotEventPluginFleet` and will set these configurations to the Spot Event Plugin.

```python
const vpc = new Vpc(/* ... */);
const renderQueue = new RenderQueue(stack, 'RenderQueue', /* ... */);

const fleet = new SpotEventPluginFleet(this, 'SpotEventPluginFleet', {
  vpc,
  renderQueue,
  deadlineGroups: [
    'group_name1',
    'group_name2',
  ],
  instanceTypes: [InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)],
  workerMachineImage: new GenericLinuxImage(/* ... */),
  maxCapacity: 1,
});
```

### Changing Default Options

Here are a few examples of how you set some additional properties of the `SpotEventPluginFleet`:

#### Setting Allocation Strategy

Use `allocationStrategy` property to change the default allocation strategy of the Spot Fleet Request:

```python
const fleet = new SpotEventPluginFleet(this, 'SpotEventPluginFleet', {
  vpc,
  renderQueue,
  deadlineGroups: [
    'group_name',
  ],
  instanceTypes: [InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)],
  workerMachineImage: new GenericLinuxImage(/* ... */),
  maxCapacity: 1,
  allocationStrategy: SpotFleetAllocationStrategy.CAPACITY_OPTIMIZED,
});
```

#### Adding Deadline Pools

You can add the Workers to Deadline's Pools providing a list of pools as following:

```python
const fleet = new SpotEventPluginFleet(this, 'SpotEventPluginFleet', {
  vpc,
  renderQueue,
  deadlineGroups: [
    'group_name',
  ],
  instanceTypes: [InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)],
  workerMachineImage: new GenericLinuxImage(/* ... */),
  maxCapacity: 1,
  deadlinePools: [
    'pool1',
    'pool2',
  ],
});
```

#### Setting the End Date And Time

By default, the Spot Fleet Request will be valid until you cancel it.
You can set the end date and time until the Spot Fleet request is valid using `validUntil` property:

```python
const fleet = new SpotEventPluginFleet(this, 'SpotEventPluginFleet', {
  vpc,
  renderQueue,
  deadlineGroups: [
    'group_name',
  ],
  instanceTypes: [InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)],
  workerMachineImage: new GenericLinuxImage(/* ... */),
  maxCapacity: 1,
  validUntil: Expiration.atDate(new Date(2022, 11, 17)),
});
```

## Stage

A stage is a directory that conforms to a [conventional structure](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/docs/DockerImageRecipes.md#stage-directory-convention) that RFDK requires to deploy Deadline. This directory contains the Docker image recipes that RFDK uses to build Docker images.

### Staging Docker Recipes

Docker image recipes required by various constructs in Deadline (e.g. `RenderQueue`, `UsageBasedLicensing`, etc.) must be staged to a local directory that RFDK can consume. For information on what a Docker image recipe is and how it should be organized, see [Docker Image Recipes](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/docs/DockerImageRecipes.md). You can either stage your own recipes or use ones provided by AWS Thinkbox via `ThinkboxDockerRecipes`.

#### Using Thinkbox Docker Recipes

---


***Note:** The `ThinkboxDockerRecipes` class requires a [multi-stage Dockerfile](https://docs.docker.com/develop/develop-images/multistage-build/), so your version of Docker must meet the minimum version that supports multi-stage builds (version 17.05).*

***Note:** Regardless of what language is consuming `aws-rfdk`, the Node.js package is required since the `stage-deadline` script is used by `ThinkboxDockerRecipes` when running `cdk synth` or `cdk deploy`.*

---


AWS Thinkbox provides Docker recipes for use with Deadline constructs. To stage these recipes, use the `stage-deadline` script found in the `bin/` directory (e.g. `node_modules/aws-rfdk/bin/stage-deadline` for npm). The following example shows how to stage version 10.1.7.1 of Deadline:

```
npx stage-deadline \
  --deadlineInstallerURI s3://thinkbox-installers/Deadline/10.1.7.1/Linux/DeadlineClient-10.1.7.1-linux-x64-installer.run \
  --dockerRecipesURI s3://thinkbox-installers/DeadlineDocker/10.1.7.1/DeadlineDocker-10.1.7.1.tar.gz
```

This command will download the Deadline installers and Docker recipes for Deadline version 10.1.7.1 to a local subdirectory `stage`. The Deadline versions in the URIs **must** be equal. For more information, run `stage-deadline --help`.

In your typescript code, you can then create an instance of `ThinkboxDockerRecipes` from this stage directory like this:

```python
const recipes = new ThinkboxDockerRecipes(scope, 'DockerRecipes', {
  stage: Stage.fromDirectory(/* <path-to-stage-directory> */),
});
```

#### Conveniently Run stage-deadline Script

Having to memorize the path conventions used in the URIs of the arguments to the `stage-deadline` can be cumbersome and error-prone. The following recommendations provide a more convenient way to use `stage-deadline`.

**Typescript/Javascript**

We recommend adding a `script` field in your `package.json` that runs the `stage-deadline` script with pre-populated parameters to ease the burden of having to remember the path conventions used in the thinkbox-installers S3 bucket. You can also leverage the built-in support for accessing the values of fields in `package.json` using the `${npm_package_<field1_innerfield1_...>}` syntax.

```json
{
  ...
  "config": {
    "deadline_ver": "10.1.7.1",
    "stage_path": "stage"
  },
  ...
  "scripts": {
    ...
    "stage": "stage-deadline -d s3://thinkbox-installers/Deadline/${npm_package_config_deadline_ver}/Linux/DeadlineClient-${npm_package_config_deadline_ver}-linux-x64-installer.run -c s3://thinkbox-installers/DeadlineDocker/${npm_package_config_deadline_ver}/DeadlineDocker-${npm_package_config_deadline_ver}.tar.gz -o ${npm_package_config_stage_path}",
  },
  ...
}
```

With this in place, staging the Deadline Docker recipes can be done simply by running `npm run stage`.

## Thinkbox Docker Images

Thinkbox publishes Docker images for use with RFDK to a public ECR repository. The `ThinkboxDockerImages` construct
simplifies using these images.

---


***Note:** By downloading or using the Deadline software, you agree to the [AWS Customer Agreement](https://aws.amazon.com/agreement/)
and [AWS Intellectual Property License](https://aws.amazon.com/legal/aws-ip-license-terms/). You acknowledge that Deadline
is AWS Content as defined in those Agreements. Users of `ThinkboxDockerImages` must explicitly signify their acceptance of these terms
through the `userAwsCustomerAgreementAndIpLicenseAcceptance` property. By default, `userAwsCustomerAgreementAndIpLicenseAcceptance` is
set to reject these terms.*

---


To use it, simply create one:

```python
// This will provide Docker container images for the latest Deadline release
const images = new ThinkboxDockerImages(stack, 'Image', {
  // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
  // of the AWS Customer Agreement and AWS Intellectual Property License.
  userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
});
```

If you desire a specific version of Deadline, you can supply a version with:

```python
// Specify a version of Deadline
const version = new VersionQuery(scope, 'Version', {
  version: '10.1.12',
});

// This will provide Docker container images for the specified version of Deadline
const images = new ThinkboxDockerImages(stack, 'Image', {
  version,
  // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
  // of the AWS Customer Agreement and AWS Intellectual Property License.
  userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
});
```

To use these images, you can use the expressive methods or provide the instance directly to downstream constructs:

```python
const renderQueue = new RenderQueue(scope, 'RenderQueue', {
  images: images,
  // ...
});
const ubl = new UsageBasedLicensing(scope, 'RenderQueue', {
  images: images,
  // ...
});

// OR

const renderQueue = new RenderQueue(scope, 'RenderQueue', {
  images: images.forRenderQueue(),
  // ...
});
const ubl = new UsageBasedLicensing(scope, 'RenderQueue', {
  images: images.forUsageBasedLicensing(),
  // ...
});
```

## Usage-Based Licensing (UBL)

![architecture diagram](../../docs/diagrams/deadline/UsageBasedLicensing.svg)

Usage-Based Licensing is an on-demand licensing model (see [Deadline Documentation](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/licensing-usage-based.html)). The RFDK supports this type of licensing with the `UsageBasedLicensing` construct. This construct contains the following components:

* **Deadline License Forwarder** - Forwards licenses to Deadline Workers that are rendering jobs.

The `UsageBasedLicensing` construct sets up the License Forwarder, configures the defined license limits, and allows communication with the Render Queue. Docker container images are used to deploy the License Forwarder as a fleet of instances within an Elastic Container Service (ECS) cluster.

---


***Note:** This construct does not currently implement the Deadline License Forwarder's Web Forwarding functionality.*

***Note:** This construct is not usable in any China region.*

---


The following example outlines how to construct `UsageBasedLicensing`:

```python
const version = new VersionQuery(stack, 'Version', '1.2.3.4');
const images = new ThinkboxDockerImages(stack, 'Image', {
  version,
  // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
  // of the AWS Customer Agreement and AWS Intellectual Property License.
  userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
});


const ubl = new UsageBasedLicensing(stack, 'UsageBasedLicensing', {
  vpc: vpc,
  renderQueue: renderQueue,
  images: images,
  licenses: [ UsageBasedLicense.forKrakatoa(/* ... */), /* ... */ ],
  certificateSecret: /* ... */, // This must be a binary secret (see below)
  memoryReservationMiB: /* ... */
});
```

### Usage-Based Licensing Docker Container Images

`UsageBasedLicensing` currently requires only one Docker container image for the Deadline License Forwarder.

AWS Thinkbox provides Docker recipes that sets these up for you. These can be accessed with the `ThinkboxDockerRecipes` and `ThinkboxDockerImages` constructs (see [Staging Docker Recipes](#staging-docker-recipes) and [Thinkbox Docker Images](#thinkbox-docker-images) respectively).

### Uploading Binary Secrets to SecretsManager

The `UsageBasedLicensing` construct expects a `.zip` file containing usage-based licenses stored as a binary secret in SecretsManager. The AWS web console does not provide a way to upload binary secrets to SecretsManager, but this can be done via [AWS CLI](https://aws.amazon.com/cli/). You can use the following command to upload a binary secret:

```
aws secretsmanager create-secret --name <secret-name> --secret-binary fileb://<path-to-file>
```

## VersionQuery

The `VersionQuery` construct encapsulates a version of Deadline and the location in Amazon S3 to retrieve the installers for that version. Deadline versions follow a `<major>.<minor>.<release>.<patch>` schema (e.g. `1.2.3.4`). Various constructs in this library use `VersionQuery` to determine the version of Deadline to work with.

You can specify a Deadline version as follows:

```python
const version = new VersionQuery(stack, 'Version', {
  version: '1.2.3.4',
});
```

## Worker Instance Fleet

![architecture diagram](../../docs/diagrams/deadline/WorkerInstanceFleet.svg)

A `WorkerInstanceFleet` represents a fleet of instances that are the render nodes of your render farm. These instances are created in an [`AutoScalingGroup`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-autoscaling.AutoScalingGroup.html) with a provided AMI that should have Deadline Client installed as well as any desired render applications. Each of the instances will configure itself to connect to the specified [`RenderQueue`](#renderqueue) so that they are able to communicate with Deadline to pick up render jobs. Any logs emitted by the workers are sent to CloudWatch via a CloudWatch agent.

You can create a `WorkerInstanceFleet` like this:

```python
const fleet = new WorkerInstanceFleet(stack, 'WorkerFleet', {
  vpc,
  renderQueue,
  workerMachineImage: /* ... */,
});
```

### Worker Instance Fleet Health Monitoring

The `WorkerInstanceFleet` uses Elastic Load Balancing (ELB) health checks with its `AutoScalingGroup` to ensure the fleet is operating as expected. ELB health checks have two components:

1. **EC2 Status Checks** - Amazon EC2 identifies any hardware or software issues on instances. If a status check fails for an instance, it will be replaced. For more information, see [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html).
2. **Load Balancer Health Checks** - Load balancers send periodic pings to instances in the `AutoScalingGroup`. If a ping to an instance fails, the instance is considered unhealthy. For more information, see [here](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-add-elb-healthcheck.html).

EC2 status checks are great for detecting lower level issues with instances and automatically replacing them. If you also want to detect any issues with Deadline on your instances, you can do this by configuring health monitoring options on the `WorkerInstanceFleet` along with a `HealthMonitor` (see [aws-rfdk](https://github.com/aws/aws-rfdk/blob/release/packages/aws-rfdk/lib/core/README.md)). The `HealthMonitor` will ensure that your `WorkerInstanceFleet` remains healthy by checking that a minimum number of hosts are healthy for a given grace period. If the fleet is found to be unhealthy, its capacity will set to 0, meaning that all instances will be terminated. This is a precaution to save on costs in the case of a misconfigured render farm.

Below is an example of setting up health monitoring in a `WorkerInstanceFleet`.

```python
const healthMonitor = new HealthMonitor(stack, 'HealthMonitor', {
  vpc,
  elbAccountLimits: /* ... */
});

const workerFleet = new WorkerInstanceFleet(stack, 'WorkerFleet', {
  vpc,
  renderQueue: /* ... */,
  workerMachineImage: /* ... */,
  healthMonitor: healthMonitor,
  healthCheckConfig: {
    interval: Duration.minutes(5)
  }
});
```

### Custom Worker Instance Startup

You have possibility to run user data scripts at various points during the Worker configuration lifecycle.

To do this, subclass `InstanceUserDataProvider` and override desired methods:

```python
class UserDataProvider extends InstanceUserDataProvider {
  preCloudWatchAgent(host: IHost): void {
    host.userData.addCommands('echo preCloudWatchAgent');
  }
}
const fleet = new WorkerInstanceFleet(stack, 'WorkerFleet', {
  vpc,
  renderQueue,
  workerMachineImage: /* ... */,
  userDataProvider: new UserDataProvider(stack, 'UserDataProvider'),
});
```

### Worker Instance Fleet Subnet Placement

We highly recommend creating dedicated subnets for the Worker Instance Fleets in your farm as it is considered best practice and is especially important if you are using
Deadline Secrets Management (see [Deadline Secrets Management Considerations](#using-dedicated-subnets-for-deadline-components)).

The following example creates a dedicated subnet group for a `WorkerInstanceFleet`:

```python
const vpc = new Vpc(this, 'Vpc', {
  // ...
  subnetConfiguration: [
    // ...

    // Provide a subnet configuration for the WorkerInstanceFleet subnet group
    {
      name: 'WorkerInstanceFleetSubnets',
      subnetType: SubnetType.PRIVATE_WITH_EGRESS,
      cidrMask: 20,
    },

    // ...
  ],
  // ...
});

// ...

const workerInstanceFleet = new WorkerInstanceFleet(stack, 'WorkerInstanceFleet', {
  // ...
  vpc,

  // Select the dedicated WorkerInstanceFleet subnets to put the worker nodes in
  vpcSubnets: {
    subnetGroupName: "WorkerInstanceFleetSubnets",
  },

  // ...
});
```
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_docdb as _aws_cdk_aws_docdb_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecr_assets as _aws_cdk_aws_ecr_assets_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from .. import (
    ConnectableApplicationEndpoint as _ConnectableApplicationEndpoint_075040da,
    HealthCheckConfig as _HealthCheckConfig_ebe26fb6,
    IHealthMonitor as _IHealthMonitor_ab248fa9,
    IMongoDb as _IMongoDb_dbee748a,
    IMonitorableFleet as _IMonitorableFleet_71f4eb88,
    IMountableLinuxFilesystem as _IMountableLinuxFilesystem_5182ce0b,
    IScriptHost as _IScriptHost_ad38c9ad,
    IX509CertificatePem as _IX509CertificatePem_da3ef30f,
    IX509CertificatePkcs12 as _IX509CertificatePkcs12_63b2574c,
    LogGroupFactoryProps as _LogGroupFactoryProps_b817ed21,
)


@jsii.enum(jsii_type="aws-rfdk.deadline.AwsCustomerAgreementAndIpLicenseAcceptance")
class AwsCustomerAgreementAndIpLicenseAcceptance(enum.Enum):
    '''The ThinkboxDockerImages will install Deadline onto one or more EC2 instances.

    By downloading or using the Deadline software, you agree to the AWS Customer Agreement (https://aws.amazon.com/agreement/)
    and AWS Intellectual Property License (https://aws.amazon.com/legal/aws-ip-license-terms/). You acknowledge that Deadline
    is AWS Content as defined in those Agreements.

    This enum is used to signify acceptance or rejection of these terms.
    '''

    USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE = "USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE"
    '''The user signifies their explicit rejection of the terms.'''
    USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE = "USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE"
    '''The user signifies their explicit acceptance of the terms.'''


class ConfigureSpotEventPlugin(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.ConfigureSpotEventPlugin",
):
    '''This construct configures the Deadline Spot Event Plugin to deploy and auto-scale one or more spot fleets.

    For example, to configure the Spot Event Plugin with one spot fleet::

       import { App, Stack, Vpc } from '@aws-rfdk/core';
       import { InstanceClass, InstanceSize, InstanceType } from 'aws-cdk-lib/aws-ec2';
       import { AwsCustomerAgreementAndIpLicenseAcceptance, ConfigureSpotEventPlugin, RenderQueue, Repository, SpotEventPluginFleet, ThinkboxDockerImages, VersionQuery } from '@aws-rfdk/deadline';
       const app = new App();
       const stack = new Stack(app, 'Stack');
       const vpc = new Vpc(stack, 'Vpc');
       const version = new VersionQuery(stack, 'Version', {
         version: '10.1.12',
       });
       const images = new ThinkboxDockerImages(stack, 'Image', {
         version,
         // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
         // of the AWS Customer Agreement and AWS Intellectual Property License.
         userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
       });
       const repository = new Repository(stack, 'Repository', {
         vpc,
         version,
       });
       const renderQueue = new RenderQueue(stack, 'RenderQueue', {
         vpc,
         images: images.forRenderQueue(),
         repository: repository,
       });

       const fleet = new SpotEventPluginFleet(this, 'SpotEventPluginFleet', {
         vpc,
         renderQueue,
         deadlineGroups: ['group_name'],
         instanceTypes: [InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)],
         workerMachineImage: new GenericLinuxImage({'us-west-2': 'ami-039f0c1faba28b015'}),
         naxCapacity: 1,
       });

       const spotEventPluginConfig = new ConfigureSpotEventPlugin(this, 'ConfigureSpotEventPlugin', {
         vpc,
         renderQueue: renderQueue,
         spotFleets: [fleet],
         configuration: {
           enableResourceTracker: true,
         },
       });

    To provide this functionality, this construct will create an AWS Lambda function that is granted the ability
    to connect to the render queue. This lambda is run automatically when you deploy or update the stack containing this construct.
    Logs for all AWS Lambdas are automatically recorded in Amazon CloudWatch.

    This construct will configure the Spot Event Plugin, but the Spot Fleet Requests will not be created unless you:

    - Submit the job with the assigned Deadline Group and Deadline Pool. See `Deadline Documentation <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-submitting.html#submitting-jobs>`_.

    Important: Disable 'Allow Workers to Perform House Cleaning If Pulse is not Running' in the 'Configure Repository Options'
    when using Spot Event Plugin.
    See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#prerequisites

    Important: Any resources created by the Spot Event Plugin will not be deleted with 'cdk destroy'.
    Make sure that all such resources (e.g. Spot Fleet Request or Fleet Instances) are cleaned up, before destroying the stacks.
    Disable the Spot Event Plugin by setting 'state' property to 'SpotEventPluginState.DISABLED' or via Deadline Monitor,
    ensure you shutdown all Pulse instances and then terminate any Spot Fleet Requests in the AWS EC2 Instance Console.

    Note that this construct adds additional policies to the Render Queue's role
    required to run the Spot Event Plugin and launch a Resource Tracker:

    - AWSThinkboxDeadlineSpotEventPluginAdminPolicy
    - AWSThinkboxDeadlineResourceTrackerAdminPolicy
    - A policy to pass a fleet and instance role
    - A policy to create tags for spot fleet requests

    The Spot Fleet Requests that this construct configures Deadline to create will always use the latest version of the
    corresponding EC2 Launch Template that was created for them.

    architecture diagram


    Resources Deployed

    - An AWS Lambda that is used to connect to the render queue, and save Spot Event Plugin configurations.
    - A CloudFormation Custom Resource that triggers execution of the Lambda on stack deployment, update, and deletion.
    - An Amazon CloudWatch log group that records history of the AWS Lambda's execution.
    - An IAM Policy attached to Render Queue's Role.
    - EC2 Launch Templates for each Spot Event Plugin fleet.



    Security Considerations

    - The AWS Lambda that is deployed through this construct will be created from a deployment package
      that is uploaded to your CDK bootstrap bucket during deployment. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by this Lambda.
      We strongly recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket,
      or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The AWS Lambda function that is created by this resource has access to both the certificates used to connect to the render queue,
      and the render queue port. An attacker that can find a way to modify and execute this lambda could use it to
      execute any requets against the render queue. You should not grant any additional actors/principals the ability to modify
      or execute this Lambda.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        render_queue: "IRenderQueue",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        configuration: typing.Optional[typing.Union["SpotEventPluginSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_fleets: typing.Optional[typing.Sequence["SpotEventPluginFleet"]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param render_queue: The RenderQueue that Worker fleet should connect to.
        :param vpc: The VPC in which to create the network endpoint for the lambda function that is created by this construct.
        :param configuration: The Spot Event Plugin settings. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options Default: Default values of SpotEventPluginSettings will be set.
        :param spot_fleets: The array of Spot Event Plugin spot fleets used to generate the mapping between groups and spot fleet requests. Default: Spot Fleet Request Configurations will not be updated.
        :param vpc_subnets: Where within the VPC to place the lambda function's endpoint. Default: The instance is placed within a Private subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dcc52dcfacbe17008708565aabdc428440637c784f588ef3a7eda3f954bc56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfigureSpotEventPluginProps(
            render_queue=render_queue,
            vpc=vpc,
            configuration=configuration,
            spot_fleets=spot_fleets,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ConfigureSpotEventPluginProps",
    jsii_struct_bases=[],
    name_mapping={
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "configuration": "configuration",
        "spot_fleets": "spotFleets",
        "vpc_subnets": "vpcSubnets",
    },
)
class ConfigureSpotEventPluginProps:
    def __init__(
        self,
        *,
        render_queue: "IRenderQueue",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        configuration: typing.Optional[typing.Union["SpotEventPluginSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_fleets: typing.Optional[typing.Sequence["SpotEventPluginFleet"]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Input properties for ConfigureSpotEventPlugin.

        :param render_queue: The RenderQueue that Worker fleet should connect to.
        :param vpc: The VPC in which to create the network endpoint for the lambda function that is created by this construct.
        :param configuration: The Spot Event Plugin settings. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options Default: Default values of SpotEventPluginSettings will be set.
        :param spot_fleets: The array of Spot Event Plugin spot fleets used to generate the mapping between groups and spot fleet requests. Default: Spot Fleet Request Configurations will not be updated.
        :param vpc_subnets: Where within the VPC to place the lambda function's endpoint. Default: The instance is placed within a Private subnet.
        '''
        if isinstance(configuration, dict):
            configuration = SpotEventPluginSettings(**configuration)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e7362e9158bf38590687283b66274526c989cd9e63d789a8ab16260c5fb218)
            check_type(argname="argument render_queue", value=render_queue, expected_type=type_hints["render_queue"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument spot_fleets", value=spot_fleets, expected_type=type_hints["spot_fleets"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "render_queue": render_queue,
            "vpc": vpc,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if spot_fleets is not None:
            self._values["spot_fleets"] = spot_fleets
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def render_queue(self) -> "IRenderQueue":
        '''The RenderQueue that Worker fleet should connect to.'''
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return typing.cast("IRenderQueue", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the network endpoint for the lambda function that is created by this construct.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def configuration(self) -> typing.Optional["SpotEventPluginSettings"]:
        '''The Spot Event Plugin settings.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options

        :default: Default values of SpotEventPluginSettings will be set.
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["SpotEventPluginSettings"], result)

    @builtins.property
    def spot_fleets(self) -> typing.Optional[typing.List["SpotEventPluginFleet"]]:
        '''The array of Spot Event Plugin spot fleets used to generate the mapping between groups and spot fleet requests.

        :default: Spot Fleet Request Configurations will not be updated.
        '''
        result = self._values.get("spot_fleets")
        return typing.cast(typing.Optional[typing.List["SpotEventPluginFleet"]], result)

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
        return "ConfigureSpotEventPluginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseConnection(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-rfdk.deadline.DatabaseConnection",
):
    '''Helper class for connecting Thinkbox's Deadline to a specific Database.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="forDocDB")
    @builtins.classmethod
    def for_doc_db(
        cls,
        *,
        database: _aws_cdk_aws_docdb_ceddda9d.IDatabaseCluster,
        login: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> "DatabaseConnection":
        '''Creates a DatabaseConnection which allows Deadline to connect to Amazon DocumentDB.

        Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and higher.


        Resources Deployed

        This construct does not deploy any resources

        :param database: The Document DB Cluster this connection is for. Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and greater.
        :param login: A Secret that contains the login information for the database. This must be a secret containing a JSON document as follows: { "username": "", "password": "" }
        '''
        options = DocDBConnectionOptions(database=database, login=login)

        return typing.cast("DatabaseConnection", jsii.sinvoke(cls, "forDocDB", [options]))

    @jsii.member(jsii_name="forMongoDbInstance")
    @builtins.classmethod
    def for_mongo_db_instance(
        cls,
        *,
        client_certificate: _IX509CertificatePkcs12_63b2574c,
        database: _IMongoDb_dbee748a,
    ) -> "DatabaseConnection":
        '''Creates a DatabaseConnection which allows Deadline to connect to MongoDB.

        Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and higher.


        Resources Deployed

        This construct does not deploy any resources

        :param client_certificate: The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database. This **MUST** be signed by the same signing certificate as the MongoDB server's certificate. Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA). Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        :param database: The MongoDB database to connect to. Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and higher.
        '''
        options = MongoDbInstanceConnectionOptions(
            client_certificate=client_certificate, database=database
        )

        return typing.cast("DatabaseConnection", jsii.sinvoke(cls, "forMongoDbInstance", [options]))

    @jsii.member(jsii_name="addChildDependency")
    @abc.abstractmethod
    def add_child_dependency(self, child: _constructs_77d1e7e8.IConstruct) -> None:
        '''Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the database has been deployed.

        This can be used to ensure that the database is fully up and serving data before an instance attempts to connect to it.

        :param child: The child to make dependent upon this database.
        '''
        ...

    @jsii.member(jsii_name="addConnectionDBArgs")
    @abc.abstractmethod
    def add_connection_db_args(self, host: "IHost") -> None:
        '''Adds commands to an Instance or Autoscaling groups User Data to configure the Deadline client so it can access the DB  Implementation must add commands to the instance userData that exports a function called configure_deadline_database() that accepts no arguments, and does what ever deadline-specific setup is required to allow Deadline to connect to the database.

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        '''
        ...

    @jsii.member(jsii_name="addInstallerDBArgs")
    @abc.abstractmethod
    def add_installer_db_args(self, host: "IHost") -> None:
        '''Adds commands to a UserData to build the argument list needed to install the Deadline Repository.

        The implementation must export a shell function called configure_database_installation_args(),
        that takes no arguments. This function must define an array environment variable called
        INSTALLER_DB_ARGS where each element of the array is a key-value pair of Deadline installer
        option to option value. (ex: ["--dbuser"]=someusername).

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        '''
        ...

    @jsii.member(jsii_name="addSecurityGroup")
    @abc.abstractmethod
    def add_security_group(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds a security group to the database.

        :param security_groups: The security group to add.
        '''
        ...

    @jsii.member(jsii_name="allowConnectionsFrom")
    @abc.abstractmethod
    def allow_connections_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow connections to the Database from the given connection peer.

        :param other: -
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''Grants permissions to the principal that allow it to use the Database as a typical Deadline user.

        :param grantee: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerEnvironment")
    @abc.abstractmethod
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Returns the environment variables for configuring containers to connect to the database.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="databaseConstruct")
    @abc.abstractmethod
    def database_construct(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        '''Holds the CDK Construct that contains the database, or undefined if the database was imported into this application.'''
        ...


class _DatabaseConnectionProxy(DatabaseConnection):
    @jsii.member(jsii_name="addChildDependency")
    def add_child_dependency(self, child: _constructs_77d1e7e8.IConstruct) -> None:
        '''Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the database has been deployed.

        This can be used to ensure that the database is fully up and serving data before an instance attempts to connect to it.

        :param child: The child to make dependent upon this database.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1726210bad329893b864714001adefd6110aeca0c04a7974628fe48ba859ca)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast(None, jsii.invoke(self, "addChildDependency", [child]))

    @jsii.member(jsii_name="addConnectionDBArgs")
    def add_connection_db_args(self, host: "IHost") -> None:
        '''Adds commands to an Instance or Autoscaling groups User Data to configure the Deadline client so it can access the DB  Implementation must add commands to the instance userData that exports a function called configure_deadline_database() that accepts no arguments, and does what ever deadline-specific setup is required to allow Deadline to connect to the database.

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1afe5f939d230131d9bca553973b795d082a64b49d1bc6dc3450ee4b8684db)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "addConnectionDBArgs", [host]))

    @jsii.member(jsii_name="addInstallerDBArgs")
    def add_installer_db_args(self, host: "IHost") -> None:
        '''Adds commands to a UserData to build the argument list needed to install the Deadline Repository.

        The implementation must export a shell function called configure_database_installation_args(),
        that takes no arguments. This function must define an array environment variable called
        INSTALLER_DB_ARGS where each element of the array is a key-value pair of Deadline installer
        option to option value. (ex: ["--dbuser"]=someusername).

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ad9d3dc48c06cf0a0e95fcbadf5de623be443a730dbf798e9ddf2abd425825)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "addInstallerDBArgs", [host]))

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds a security group to the database.

        :param security_groups: The security group to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__face20232623a608481d2a6800ff5c8cd78d461091a4c9e7c36f657fa3868cc1)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [*security_groups]))

    @jsii.member(jsii_name="allowConnectionsFrom")
    def allow_connections_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow connections to the Database from the given connection peer.

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0164247e3b2c3acbfbba676ca55cb1bd14c07eb06d4c5e81a2e337af77eccea8)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowConnectionsFrom", [other]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''Grants permissions to the principal that allow it to use the Database as a typical Deadline user.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e6ad7c5effc3fb3ddfc7b1ed5a1d77b2b2b5fe004c144ea6aa8d5c9d26d412)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Returns the environment variables for configuring containers to connect to the database.'''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "containerEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="databaseConstruct")
    def database_construct(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        '''Holds the CDK Construct that contains the database, or undefined if the database was imported into this application.'''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "databaseConstruct"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DatabaseConnection).__jsii_proxy_class__ = lambda : _DatabaseConnectionProxy


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.DocDBConnectionOptions",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "login": "login"},
)
class DocDBConnectionOptions:
    def __init__(
        self,
        *,
        database: _aws_cdk_aws_docdb_ceddda9d.IDatabaseCluster,
        login: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''Options when constructing UserData for Linux.

        :param database: The Document DB Cluster this connection is for. Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and greater.
        :param login: A Secret that contains the login information for the database. This must be a secret containing a JSON document as follows: { "username": "", "password": "" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25548daa628eecb0ab05f63a6488f202046dfd41686ad9a37deeda609682e416)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "login": login,
        }

    @builtins.property
    def database(self) -> _aws_cdk_aws_docdb_ceddda9d.IDatabaseCluster:
        '''The Document DB Cluster this connection is for.

        Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and greater.
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_aws_cdk_aws_docdb_ceddda9d.IDatabaseCluster, result)

    @builtins.property
    def login(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''A Secret that contains the login information for the database.

        This must be a secret containing a JSON document as follows:
        {
        "username": "",
        "password": ""
        }
        '''
        result = self._values.get("login")
        assert result is not None, "Required property 'login' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocDBConnectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSConnectOptions",
    jsii_struct_bases=[],
    name_mapping={"grantee": "grantee", "hosts": "hosts"},
)
class ECSConnectOptions:
    def __init__(
        self,
        *,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        hosts: typing.Sequence["IHost"],
    ) -> None:
        '''Properties that need to be provided in order to connect an ECS service to a Render Queue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d95aca067039f7b60d07f229c6e943510fd04152cb24a7286afb0554058c34)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grantee": grantee,
            "hosts": hosts,
        }

    @builtins.property
    def grantee(self) -> _aws_cdk_aws_iam_ceddda9d.IGrantable:
        '''The task definitions Role that needs permissions.'''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IGrantable, result)

    @builtins.property
    def hosts(self) -> typing.List["IHost"]:
        '''The set of hosts that will be hosting the containers.

        This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        '''
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return typing.cast(typing.List["IHost"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSConnectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSContainerInstanceProps",
    jsii_struct_bases=[],
    name_mapping={"hosts": "hosts", "filesystem_mount_point": "filesystemMountPoint"},
)
class ECSContainerInstanceProps:
    def __init__(
        self,
        *,
        hosts: typing.Sequence["IHost"],
        filesystem_mount_point: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration interface for specifying ECS container instances to permit connecting hosted ECS tasks to the repository.

        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        :param filesystem_mount_point: The path where the repository file-system is mounted on the container hosts. Default: "/mnt/repo"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b374add9560530740ec1b39c66c2a3cb9d398f0ce7a3ad4e4e2dfdd2d46521)
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument filesystem_mount_point", value=filesystem_mount_point, expected_type=type_hints["filesystem_mount_point"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hosts": hosts,
        }
        if filesystem_mount_point is not None:
            self._values["filesystem_mount_point"] = filesystem_mount_point

    @builtins.property
    def hosts(self) -> typing.List["IHost"]:
        '''The set of hosts that will be hosting the containers.

        This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        '''
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return typing.cast(typing.List["IHost"], result)

    @builtins.property
    def filesystem_mount_point(self) -> typing.Optional[builtins.str]:
        '''The path where the repository file-system is mounted on the container hosts.

        :default: "/mnt/repo"
        '''
        result = self._values.get("filesystem_mount_point")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSContainerInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSDirectConnectProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_instances": "containerInstances",
        "containers": "containers",
    },
)
class ECSDirectConnectProps:
    def __init__(
        self,
        *,
        container_instances: typing.Union[ECSContainerInstanceProps, typing.Dict[builtins.str, typing.Any]],
        containers: typing.Union["ECSTaskProps", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''The properties used to configure Deadline running in an Amazon EC2 ECS task to directly connect to the repository.

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.
        '''
        if isinstance(container_instances, dict):
            container_instances = ECSContainerInstanceProps(**container_instances)
        if isinstance(containers, dict):
            containers = ECSTaskProps(**containers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29665b191fef1fb01446ddb4f90654ed00b5c294c80a498fdd1034adc7a4e038)
            check_type(argname="argument container_instances", value=container_instances, expected_type=type_hints["container_instances"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_instances": container_instances,
            "containers": containers,
        }

    @builtins.property
    def container_instances(self) -> ECSContainerInstanceProps:
        '''Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.'''
        result = self._values.get("container_instances")
        assert result is not None, "Required property 'container_instances' is missing"
        return typing.cast(ECSContainerInstanceProps, result)

    @builtins.property
    def containers(self) -> "ECSTaskProps":
        '''Configuration to directly connect an ECS task to the repository.'''
        result = self._values.get("containers")
        assert result is not None, "Required property 'containers' is missing"
        return typing.cast("ECSTaskProps", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSDirectConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task_definition": "taskDefinition",
        "filesystem_mount_point": "filesystemMountPoint",
    },
)
class ECSTaskProps:
    def __init__(
        self,
        *,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        filesystem_mount_point: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration interface to directly connect an ECS task to the repository.

        :param task_definition: The task definition to connect to the repository. [disable-awslint:ref-via-interface]
        :param filesystem_mount_point: The path where the repository file-system is mounted within the container. Default: "/opt/Thinkbox/DeadlineRepository{MAJOR_VER}"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a32c14401c769257158653c2267efa3653320b30a71cbd34d2d23a1c5ec348)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument filesystem_mount_point", value=filesystem_mount_point, expected_type=type_hints["filesystem_mount_point"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }
        if filesystem_mount_point is not None:
            self._values["filesystem_mount_point"] = filesystem_mount_point

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        '''The task definition to connect to the repository.

        [disable-awslint:ref-via-interface]
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, result)

    @builtins.property
    def filesystem_mount_point(self) -> typing.Optional[builtins.str]:
        '''The path where the repository file-system is mounted within the container.

        :default: "/opt/Thinkbox/DeadlineRepository{MAJOR_VER}"
        '''
        result = self._values.get("filesystem_mount_point")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-rfdk.deadline.IContainerDirectRepositoryConnection")
class IContainerDirectRepositoryConnection(typing_extensions.Protocol):
    '''Interface that can be used to configure a {@link @aws-cdk/aws-ecs#ContainerDefinition} definition to directly connect to the repository.'''

    @builtins.property
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Environment variables that configure a direct connection to the repository.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="readOnlyMountPoint")
    def read_only_mount_point(self) -> _aws_cdk_aws_ecs_ceddda9d.MountPoint:
        '''A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="readWriteMountPoint")
    def read_write_mount_point(self) -> _aws_cdk_aws_ecs_ceddda9d.MountPoint:
        '''A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        '''
        ...


class _IContainerDirectRepositoryConnectionProxy:
    '''Interface that can be used to configure a {@link @aws-cdk/aws-ecs#ContainerDefinition} definition to directly connect to the repository.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IContainerDirectRepositoryConnection"

    @builtins.property
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Environment variables that configure a direct connection to the repository.'''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "containerEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyMountPoint")
    def read_only_mount_point(self) -> _aws_cdk_aws_ecs_ceddda9d.MountPoint:
        '''A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.MountPoint, jsii.get(self, "readOnlyMountPoint"))

    @builtins.property
    @jsii.member(jsii_name="readWriteMountPoint")
    def read_write_mount_point(self) -> _aws_cdk_aws_ecs_ceddda9d.MountPoint:
        '''A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.MountPoint, jsii.get(self, "readWriteMountPoint"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IContainerDirectRepositoryConnection).__jsii_proxy_class__ = lambda : _IContainerDirectRepositoryConnectionProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IHost")
class IHost(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _constructs_77d1e7e8.IConstruct,
    _IScriptHost_ad38c9ad,
    typing_extensions.Protocol,
):
    '''Interface for any constructs that are Capable of connecting to Deadline.'''

    pass


class _IHostProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IScriptHost_ad38c9ad), # type: ignore[misc]
):
    '''Interface for any constructs that are Capable of connecting to Deadline.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IHost"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHost).__jsii_proxy_class__ = lambda : _IHostProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IInstanceUserDataProvider")
class IInstanceUserDataProvider(typing_extensions.Protocol):
    '''Provider for adding user data scripts Methods of this interface will be invoked in WorkerInstanceConfiguration on different stages of worker configuration.'''

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, host: IHost) -> None:
        '''Method that is invoked after all configuration is done and worker started.

        :param host: -
        '''
        ...

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, host: IHost) -> None:
        '''Method that is invoked before configuring the Cloud Watch Agent.

        :param host: -
        '''
        ...

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, host: IHost) -> None:
        '''Method that is invoked before the render queue configuration.

        :param host: -
        '''
        ...

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, host: IHost) -> None:
        '''Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param host: -
        '''
        ...


class _IInstanceUserDataProviderProxy:
    '''Provider for adding user data scripts Methods of this interface will be invoked in WorkerInstanceConfiguration on different stages of worker configuration.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IInstanceUserDataProvider"

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, host: IHost) -> None:
        '''Method that is invoked after all configuration is done and worker started.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11384c29da262d80585103f4b6c5798f37dcf9e4df9680833459a8049b959c63)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "postWorkerLaunch", [host]))

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, host: IHost) -> None:
        '''Method that is invoked before configuring the Cloud Watch Agent.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1511134e528f1873451562bd99e8a0ac3751a81b3ea5c27be6873fd3b5bea587)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "preCloudWatchAgent", [host]))

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, host: IHost) -> None:
        '''Method that is invoked before the render queue configuration.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f114ad49df14e1ac15f7458e18bb546c2c1c6e4e0fce116aa7f74aa259d78ee)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "preRenderQueueConfiguration", [host]))

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, host: IHost) -> None:
        '''Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param host: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d8953d3941ecb19d1a97d64e245608a6b353a79954d3ec0020849a3a1384da)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        return typing.cast(None, jsii.invoke(self, "preWorkerConfiguration", [host]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstanceUserDataProvider).__jsii_proxy_class__ = lambda : _IInstanceUserDataProviderProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IReleaseVersion")
class IReleaseVersion(typing_extensions.Protocol):
    '''Represents a release of Deadline up to and including the third (release) component of the version.

    E.g. 10.1.9
    '''

    @builtins.property
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        '''The major version number.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        '''The minor version number.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        '''The release version number.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="versionString")
    def version_string(self) -> builtins.str:
        '''A string representation of the version using the best available information at synthesis-time.

        This value is not guaranteed to be resolved, and is intended for output to CDK users.
        '''
        ...

    @jsii.member(jsii_name="isLessThan")
    def is_less_than(self, other: "Version") -> builtins.bool:
        '''Returns whether this version is less than another version.

        :param other: Other version to be compared.
        '''
        ...


class _IReleaseVersionProxy:
    '''Represents a release of Deadline up to and including the third (release) component of the version.

    E.g. 10.1.9
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IReleaseVersion"

    @builtins.property
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        '''The major version number.'''
        return typing.cast(jsii.Number, jsii.get(self, "majorVersion"))

    @builtins.property
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        '''The minor version number.'''
        return typing.cast(jsii.Number, jsii.get(self, "minorVersion"))

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        '''The release version number.'''
        return typing.cast(jsii.Number, jsii.get(self, "releaseVersion"))

    @builtins.property
    @jsii.member(jsii_name="versionString")
    def version_string(self) -> builtins.str:
        '''A string representation of the version using the best available information at synthesis-time.

        This value is not guaranteed to be resolved, and is intended for output to CDK users.
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionString"))

    @jsii.member(jsii_name="isLessThan")
    def is_less_than(self, other: "Version") -> builtins.bool:
        '''Returns whether this version is less than another version.

        :param other: Other version to be compared.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5b6f503f7586f77125c9a6f797f24c516cdc903160453d7a56c96561f26e02)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isLessThan", [other]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReleaseVersion).__jsii_proxy_class__ = lambda : _IReleaseVersionProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IRenderQueue")
class IRenderQueue(
    _constructs_77d1e7e8.IConstruct,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''Interface for Deadline Render Queue.'''

    @builtins.property
    @jsii.member(jsii_name="backendConnections")
    def backend_connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''A connections object for controlling access of the compute resources that host the render queue.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        '''The endpoint used to connect to the Render Queue.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> "IRepository":
        '''The Deadline Repository that the Render Queue services.'''
        ...

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        hosts: typing.Sequence[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :return: An environment mapping that is used to configure the Docker Images
        '''
        ...

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        restart_launcher: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param restart_launcher: Whether or not to start or restart the Deadline Launcher after configuring the connection. Default: true
        '''
        ...

    @jsii.member(jsii_name="configureSecretsManagementAutoRegistration")
    def configure_secrets_management_auto_registration(
        self,
        *,
        dependent: _constructs_77d1e7e8.Construct,
        registration_status: "SecretsManagementRegistrationStatus",
        role: "SecretsManagementRole",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Configure a rule to automatically register all Deadline Secrets Management identities connecting from a given subnet to a specified role and status.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-registration-settings-ref-label
        for details.

        All RFDK constructs that require Deadline Secrets Management identity registration call this method internally.
        End-users of RFDK should not need to use this method unless they have a special need and understand its inner
        workings.

        :param dependent: A construct node to make dependent on the registration setting being updated.
        :param registration_status: The Deadline Secrets Management registration status to be applied to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
        :param role: The role to be assigned to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
        :param vpc: The VPC of the Deadline Client host instances to be registered.
        :param vpc_subnets: The VPC subnets of the Deadline Client host instances to be registered.
        '''
        ...


class _IRenderQueueProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''Interface for Deadline Render Queue.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IRenderQueue"

    @builtins.property
    @jsii.member(jsii_name="backendConnections")
    def backend_connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''A connections object for controlling access of the compute resources that host the render queue.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "backendConnections"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        '''The endpoint used to connect to the Render Queue.'''
        return typing.cast(_ConnectableApplicationEndpoint_075040da, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> "IRepository":
        '''The Deadline Repository that the Render Queue services.'''
        return typing.cast("IRepository", jsii.get(self, "repository"))

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        hosts: typing.Sequence[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :return: An environment mapping that is used to configure the Docker Images
        '''
        params = ECSConnectOptions(grantee=grantee, hosts=hosts)

        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "configureClientECS", [params]))

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        restart_launcher: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param restart_launcher: Whether or not to start or restart the Deadline Launcher after configuring the connection. Default: true
        '''
        params = InstanceConnectOptions(host=host, restart_launcher=restart_launcher)

        return typing.cast(None, jsii.invoke(self, "configureClientInstance", [params]))

    @jsii.member(jsii_name="configureSecretsManagementAutoRegistration")
    def configure_secrets_management_auto_registration(
        self,
        *,
        dependent: _constructs_77d1e7e8.Construct,
        registration_status: "SecretsManagementRegistrationStatus",
        role: "SecretsManagementRole",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Configure a rule to automatically register all Deadline Secrets Management identities connecting from a given subnet to a specified role and status.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-registration-settings-ref-label
        for details.

        All RFDK constructs that require Deadline Secrets Management identity registration call this method internally.
        End-users of RFDK should not need to use this method unless they have a special need and understand its inner
        workings.

        :param dependent: A construct node to make dependent on the registration setting being updated.
        :param registration_status: The Deadline Secrets Management registration status to be applied to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
        :param role: The role to be assigned to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
        :param vpc: The VPC of the Deadline Client host instances to be registered.
        :param vpc_subnets: The VPC subnets of the Deadline Client host instances to be registered.
        '''
        props = SubnetIdentityRegistrationSettingsProps(
            dependent=dependent,
            registration_status=registration_status,
            role=role,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast(None, jsii.invoke(self, "configureSecretsManagementAutoRegistration", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRenderQueue).__jsii_proxy_class__ = lambda : _IRenderQueueProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IRepository")
class IRepository(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Interface for Deadline Repository.'''

    @builtins.property
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        '''The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretsManagementSettings")
    def secrets_management_settings(self) -> "SecretsManagementProps":
        '''Deadline Secrets Management settings.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        '''The version of Deadline for Linux that is installed on this Repository.'''
        ...

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: typing.Union[ECSContainerInstanceProps, typing.Dict[builtins.str, typing.Any]],
        containers: typing.Union[ECSTaskProps, typing.Dict[builtins.str, typing.Any]],
    ) -> IContainerDirectRepositoryConnection:
        '''Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :return: A mapping of environment variable names and their values to set in the container
        '''
        ...

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        '''Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        '''
        ...


class _IRepositoryProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Interface for Deadline Repository.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IRepository"

    @builtins.property
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        '''The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.
        '''
        return typing.cast(builtins.str, jsii.get(self, "rootPrefix"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagementSettings")
    def secrets_management_settings(self) -> "SecretsManagementProps":
        '''Deadline Secrets Management settings.'''
        return typing.cast("SecretsManagementProps", jsii.get(self, "secretsManagementSettings"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        '''The version of Deadline for Linux that is installed on this Repository.'''
        return typing.cast("IVersion", jsii.get(self, "version"))

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: typing.Union[ECSContainerInstanceProps, typing.Dict[builtins.str, typing.Any]],
        containers: typing.Union[ECSTaskProps, typing.Dict[builtins.str, typing.Any]],
    ) -> IContainerDirectRepositoryConnection:
        '''Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :return: A mapping of environment variable names and their values to set in the container
        '''
        props = ECSDirectConnectProps(
            container_instances=container_instances, containers=containers
        )

        return typing.cast(IContainerDirectRepositoryConnection, jsii.invoke(self, "configureClientECS", [props]))

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        '''Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        '''
        props = InstanceDirectConnectProps(host=host, mount_point=mount_point)

        return typing.cast(None, jsii.invoke(self, "configureClientInstance", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRepository).__jsii_proxy_class__ = lambda : _IRepositoryProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.ISpotEventPluginFleet")
class ISpotEventPluginFleet(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _IScriptHost_ad38c9ad,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    typing_extensions.Protocol,
):
    '''Interface for Spot Event Plugin Worker Fleet.'''

    @jsii.member(jsii_name="allowRemoteControlFrom")
    def allow_remote_control_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowRemoteControlTo().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlFrom(Peer.ipv4('10.0.0.0/24'))``

        :param other: -
        '''
        ...

    @jsii.member(jsii_name="allowRemoteControlTo")
    def allow_remote_control_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowRemoteControlFrom().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlTo(Peer.ipv4('10.0.0.0/24'))``

        :param other: -
        '''
        ...


class _ISpotEventPluginFleetProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_IScriptHost_ad38c9ad), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''Interface for Spot Event Plugin Worker Fleet.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.ISpotEventPluginFleet"

    @jsii.member(jsii_name="allowRemoteControlFrom")
    def allow_remote_control_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowRemoteControlTo().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlFrom(Peer.ipv4('10.0.0.0/24'))``

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17559faf4d1d2787ca7797f6bd7df3e2427aa35848381ee154c655f3d2c38f84)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowRemoteControlFrom", [other]))

    @jsii.member(jsii_name="allowRemoteControlTo")
    def allow_remote_control_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowRemoteControlFrom().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlTo(Peer.ipv4('10.0.0.0/24'))``

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5aa016640dc0ea626c28b30a7ae08228bc03864095ddc263fc6d64ef514de4)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowRemoteControlTo", [other]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISpotEventPluginFleet).__jsii_proxy_class__ = lambda : _ISpotEventPluginFleetProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IVersion")
class IVersion(IReleaseVersion, typing_extensions.Protocol):
    '''This interface represents a deadline version.

    It contains the
    major, minor, and release numbers essential to identify
    a version. It also includes the S3 path of the installers.

    The Deadline version tag consists of four numbers:
    Major.Minor.Release.Patch
    '''

    @builtins.property
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> "PlatformInstallers":
        '''The Linux installers for this version.

        :default: No installers for Linux are provided.
        '''
        ...

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        '''Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        '''
        ...


class _IVersionProxy(
    jsii.proxy_for(IReleaseVersion), # type: ignore[misc]
):
    '''This interface represents a deadline version.

    It contains the
    major, minor, and release numbers essential to identify
    a version. It also includes the S3 path of the installers.

    The Deadline version tag consists of four numbers:
    Major.Minor.Release.Patch
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IVersion"

    @builtins.property
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> "PlatformInstallers":
        '''The Linux installers for this version.

        :default: No installers for Linux are provided.
        '''
        return typing.cast("PlatformInstallers", jsii.get(self, "linuxInstallers"))

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        '''Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "linuxFullVersionString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVersion).__jsii_proxy_class__ = lambda : _IVersionProxy


@jsii.interface(jsii_type="aws-rfdk.deadline.IWorkerFleet")
class IWorkerFleet(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _constructs_77d1e7e8.IConstruct,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    typing_extensions.Protocol,
):
    '''Interface for Deadline Worker Fleet.'''

    @jsii.member(jsii_name="allowListenerPortFrom")
    def allow_listener_port_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowListenerPortTo().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortFrom(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -
        '''
        ...

    @jsii.member(jsii_name="allowListenerPortTo")
    def allow_listener_port_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowListenerPortFrom().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortTo(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -
        '''
        ...


class _IWorkerFleetProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''Interface for Deadline Worker Fleet.'''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IWorkerFleet"

    @jsii.member(jsii_name="allowListenerPortFrom")
    def allow_listener_port_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowListenerPortTo().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortFrom(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6cad794afeaf80d6c4e8e90ed1feb89f2c7d3642a1d976858f5dbe084ec6e4)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowListenerPortFrom", [other]))

    @jsii.member(jsii_name="allowListenerPortTo")
    def allow_listener_port_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowListenerPortFrom().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortTo(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff8d74ccd3467b61d2ead2f8e5ce4203eb44de5f0021bfd655234d27b14cd02)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowListenerPortTo", [other]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWorkerFleet).__jsii_proxy_class__ = lambda : _IWorkerFleetProxy


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Installer",
    jsii_struct_bases=[],
    name_mapping={"object_key": "objectKey", "s3_bucket": "s3Bucket"},
)
class Installer:
    def __init__(
        self,
        *,
        object_key: builtins.str,
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> None:
        '''This interface represents a deadline installer object stored on an S3 bucket.

        :param object_key: The object key where the installer file is located.
        :param s3_bucket: The S3 Bucket interface where the installer is located.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8faa5873f50ce4a61a95780fc0a5962748ec973729365d0953bdf81c34abb0de)
            check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_key": object_key,
            "s3_bucket": s3_bucket,
        }

    @builtins.property
    def object_key(self) -> builtins.str:
        '''The object key where the installer file is located.'''
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 Bucket interface where the installer is located.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Installer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.InstanceConnectOptions",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "restart_launcher": "restartLauncher"},
)
class InstanceConnectOptions:
    def __init__(
        self,
        *,
        host: IHost,
        restart_launcher: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties that need to be provided in order to connect instances to a Render Queue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param restart_launcher: Whether or not to start or restart the Deadline Launcher after configuring the connection. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7562638ba04ccb0dbeb2a7533c6a672963882a064cae6a6a5ba85a801aeb54f)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument restart_launcher", value=restart_launcher, expected_type=type_hints["restart_launcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
        }
        if restart_launcher is not None:
            self._values["restart_launcher"] = restart_launcher

    @builtins.property
    def host(self) -> IHost:
        '''The Instance/UserData which will directly connect to the Repository.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(IHost, result)

    @builtins.property
    def restart_launcher(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to start or restart the Deadline Launcher after configuring the connection.

        :default: true
        '''
        result = self._values.get("restart_launcher")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceConnectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.InstanceDirectConnectProps",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "mount_point": "mountPoint"},
)
class InstanceDirectConnectProps:
    def __init__(self, *, host: IHost, mount_point: builtins.str) -> None:
        '''The Properties used to configure Deadline, that is running in an Amazon EC2 instance, a direct connection with a repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1defab2d45c3a0c48a16c697c095b94454347440e02528447ae2fc5eac4dc9)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "mount_point": mount_point,
        }

    @builtins.property
    def host(self) -> IHost:
        '''The Instance/UserData which will directly connect to the Repository.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(IHost, result)

    @builtins.property
    def mount_point(self) -> builtins.str:
        '''The location where the Repositories file system will be mounted on the instance.'''
        result = self._values.get("mount_point")
        assert result is not None, "Required property 'mount_point' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceDirectConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInstanceUserDataProvider)
class InstanceUserDataProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.InstanceUserDataProvider",
):
    '''Implementation of {@link IInstanceUserDataProvider}.

    Can be used as sub-class with override the desired methods
    to add custom user data commands for WorkerInstanceFleet or WorkerInstanceConfiguration.
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92627c86ab6795b00367244647caf558336f7d9fbc4b91ee240e1286d75e8697)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, _host: IHost) -> None:
        '''Method that is invoked after all configuration is done and worker started.

        :param _host: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1916ec53996259b0bac9e13cdd5d4d91058df3b8bc3895f5f682ab8ac737106e)
            check_type(argname="argument _host", value=_host, expected_type=type_hints["_host"])
        return typing.cast(None, jsii.invoke(self, "postWorkerLaunch", [_host]))

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, _host: IHost) -> None:
        '''Method that is invoked before configuring the Cloud Watch Agent.

        :param _host: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7f968f5501726dba5ae1e2f642349a4fe4f2f21e31bd8887bba6de5e9320e7)
            check_type(argname="argument _host", value=_host, expected_type=type_hints["_host"])
        return typing.cast(None, jsii.invoke(self, "preCloudWatchAgent", [_host]))

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, _host: IHost) -> None:
        '''Method that is invoked before the render queue configuration.

        :param _host: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4ca5a86af78b74105ca48d930c493b7ed99f1f095519181f32b055f4f1c51b)
            check_type(argname="argument _host", value=_host, expected_type=type_hints["_host"])
        return typing.cast(None, jsii.invoke(self, "preRenderQueueConfiguration", [_host]))

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, _host: IHost) -> None:
        '''Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param _host: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b81ce8706c9153254fd66d85c3e83929c4b751b5d70c4799974c89da2cc4f4)
            check_type(argname="argument _host", value=_host, expected_type=type_hints["_host"])
        return typing.cast(None, jsii.invoke(self, "preWorkerConfiguration", [_host]))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Manifest",
    jsii_struct_bases=[],
    name_mapping={"recipes": "recipes", "schema": "schema", "version": "version"},
)
class Manifest:
    def __init__(
        self,
        *,
        recipes: typing.Mapping[builtins.str, typing.Union["Recipe", typing.Dict[builtins.str, typing.Any]]],
        schema: jsii.Number,
        version: builtins.str,
    ) -> None:
        '''The manifest included with Deadline Docker image recipes.

        :param recipes: The recipes.
        :param schema: The manifest schema version number.
        :param version: The version of Deadline that the staging directory contains.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a8f7b33555bdae5362d75b04fb4994487f9e2a999ca8a81ac80b4d4d4afc9e)
            check_type(argname="argument recipes", value=recipes, expected_type=type_hints["recipes"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recipes": recipes,
            "schema": schema,
            "version": version,
        }

    @builtins.property
    def recipes(self) -> typing.Mapping[builtins.str, "Recipe"]:
        '''The recipes.'''
        result = self._values.get("recipes")
        assert result is not None, "Required property 'recipes' is missing"
        return typing.cast(typing.Mapping[builtins.str, "Recipe"], result)

    @builtins.property
    def schema(self) -> jsii.Number:
        '''The manifest schema version number.'''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The version of Deadline that the staging directory contains.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Manifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.MongoDbInstanceConnectionOptions",
    jsii_struct_bases=[],
    name_mapping={"client_certificate": "clientCertificate", "database": "database"},
)
class MongoDbInstanceConnectionOptions:
    def __init__(
        self,
        *,
        client_certificate: _IX509CertificatePkcs12_63b2574c,
        database: _IMongoDb_dbee748a,
    ) -> None:
        '''
        :param client_certificate: The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database. This **MUST** be signed by the same signing certificate as the MongoDB server's certificate. Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA). Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        :param database: The MongoDB database to connect to. Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and higher.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032f23b04b63fa287171095416177176b209474664a6234e44d45e31c30fa26c)
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_certificate": client_certificate,
            "database": database,
        }

    @builtins.property
    def client_certificate(self) -> _IX509CertificatePkcs12_63b2574c:
        '''The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database.

        This **MUST** be signed by the same signing certificate as the MongoDB server's certificate.

        Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA).
        Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        '''
        result = self._values.get("client_certificate")
        assert result is not None, "Required property 'client_certificate' is missing"
        return typing.cast(_IX509CertificatePkcs12_63b2574c, result)

    @builtins.property
    def database(self) -> _IMongoDb_dbee748a:
        '''The MongoDB database to connect to.

        Note: Deadline officially supports only databases that are compatible with MongoDB 5.0 and higher.
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_IMongoDb_dbee748a, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstanceConnectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.PlatformInstallers",
    jsii_struct_bases=[],
    name_mapping={
        "client": "client",
        "patch_version": "patchVersion",
        "repository": "repository",
    },
)
class PlatformInstallers:
    def __init__(
        self,
        *,
        client: typing.Union[Installer, typing.Dict[builtins.str, typing.Any]],
        patch_version: jsii.Number,
        repository: typing.Union[Installer, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''This interface represents a collection of Deadline installer files for a specific Deadline version stored in S3.

        :param client: The Deadline Client installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:. - DeadlineClient-10.1.8.5-linux-x64-installer.run - DeadlineClient-10.1.8.5-windows-installer.run
        :param patch_version: The patch version for these Deadline installers. ex: If the installer is for version 10.1.8.5, then this will be 5.
        :param repository: The Deadline Repository installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:. - DeadlineRepository-10.1.8.5-linux-x64-installer.run - DeadlineRepository-10.1.8.5-windows-installer.exe
        '''
        if isinstance(client, dict):
            client = Installer(**client)
        if isinstance(repository, dict):
            repository = Installer(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3b756c57602a14c72b409022a33e523f7c446c091fe1cdfb4edda5bfcac198)
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument patch_version", value=patch_version, expected_type=type_hints["patch_version"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client": client,
            "patch_version": patch_version,
            "repository": repository,
        }

    @builtins.property
    def client(self) -> Installer:
        '''The Deadline Client installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:.

        - DeadlineClient-10.1.8.5-linux-x64-installer.run
        - DeadlineClient-10.1.8.5-windows-installer.run
        '''
        result = self._values.get("client")
        assert result is not None, "Required property 'client' is missing"
        return typing.cast(Installer, result)

    @builtins.property
    def patch_version(self) -> jsii.Number:
        '''The patch version for these Deadline installers.

        ex: If the installer is for version 10.1.8.5, then this will be 5.
        '''
        result = self._values.get("patch_version")
        assert result is not None, "Required property 'patch_version' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def repository(self) -> Installer:
        '''The Deadline Repository installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:.

        - DeadlineRepository-10.1.8.5-linux-x64-installer.run
        - DeadlineRepository-10.1.8.5-windows-installer.exe
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(Installer, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlatformInstallers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Recipe",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "title": "title",
        "build_args": "buildArgs",
        "target": "target",
    },
)
class Recipe:
    def __init__(
        self,
        *,
        description: builtins.str,
        title: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Docker container image recipe.

        :param description: Description of the recipe.
        :param title: Title of the recipe.
        :param build_args: The Docker build arguments for the recipe. Default: No build arguments are supplied
        :param target: Optional target for a Docker multi-stage build. Default: The last stage in the Dockerfile is used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477aeca6274b77b0713da5feb6f3fe41324b4e4149e50aa9ea218017114c4d6e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "title": title,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def description(self) -> builtins.str:
        '''Description of the recipe.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Title of the recipe.'''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Docker build arguments for the recipe.

        :default: No build arguments are supplied
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Optional target for a Docker multi-stage build.

        :default: The last stage in the Dockerfile is used
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Recipe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable, IRenderQueue)
class RenderQueue(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.RenderQueue",
):
    '''The RenderQueue construct deploys an Elastic Container Service (ECS) service that serves Deadline's REST HTTP API to Deadline Clients.

    Most Deadline clients will connect to a Deadline render farm via the the RenderQueue. The API provides Deadline
    clients access to Deadline's database and repository file-system in a way that is secure, performant, and scalable.

    architecture diagram


    Resources Deployed

    - An Amazon Elastic Container Service (ECS) cluster.
    - An AWS EC2 auto-scaling group that provides the instances that host the ECS service.
    - An ECS service with a task definition that deploys the Deadline Remote Connetion Server (RCS) in a container.
    - A Amazon CloudWatch log group for streaming logs from the Deadline RCS.
    - An application load balancer, listener and target group that balance incoming traffic among the RCS containers.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - Care must be taken to secure what can connect to the RenderQueue. The RenderQueue does not authenticate API
      requests made against it. You must limit access to the RenderQueue endpoint to only trusted hosts. Those hosts
      should be governed carefully, as malicious software could use the API to remotely execute code across the entire render farm.
    - The RenderQueue can be deployed with network encryption through Transport Layer Security (TLS) or without it. Unencrypted
      network communications can be eavesdropped upon or modified in transit. We strongly recommend deploying the RenderQueue
      with TLS enabled in production environments and it is configured to be on by default.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        images: typing.Union["RenderQueueImages", typing.Dict[builtins.str, typing.Any]],
        repository: IRepository,
        version: IVersion,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        access_logs: typing.Optional[typing.Union["RenderQueueAccessLogProps", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        enable_local_file_caching: typing.Optional[builtins.bool] = None,
        health_check_config: typing.Optional[typing.Union["RenderQueueHealthCheckConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[typing.Union["RenderQueueHostNameProps", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        render_queue_size: typing.Optional[typing.Union["RenderQueueSizeConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Union["RenderQueueSecurityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_encryption: typing.Optional[typing.Union["RenderQueueTrafficEncryptionProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets_alb: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param images: A collection of Docker container images used to run the RenderQueue.
        :param repository: The Deadline Repository which the RCS instances will create a direct connection to.
        :param version: The Deadline Client version that will be running within this RenderQueue.
        :param vpc: VPC to launch the Render Queue in.
        :param access_logs: Properties for configuring access logging for the load balancer used by the Render Queue. This is disabled by default, but it is highly recommended to enable it to allow engineers to identify and root cause incidents such as unauthorized access. Default: - Access logging is disabled
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param enable_local_file_caching: If enabled, then Linux's cachefilesd will be installed and set to running on the ECS container host for the Deadline Remote Connection Server. This can reduce the amount of read throughput required for the Repository Filesystem. For more information, please see: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-fscache Note: If enabling this, then your Repository filesystem may require additional mount options to take advantage. Not every filesystem's driver supports integration with cachefilesd. e.g. NFS and Amazon EFS do support it, and require the 'fsc' mount option be provided. Note2: Your ECS container host will require access to port 80 on the regional S3 service when enabling this option so that it can install cachefilesd. This host is based on Amazon Linux 2, and the package repository for these systems is hosted on S3 and reached via port 80. Default: false
        :param health_check_config: Configuration for the health checks performed by the RenderQueue upon the Deadline RCS. Default: The values outlined in {@link RenderQueueHealthCheckConfiguration }
        :param hostname: Hostname to use to connect to the RenderQueue. Default: - The hostname ``renderqueue`` will be used and a PrivateHostedZone will be created with the domain name ``aws-rfdk.com``
        :param instance_type: The type of instance on which each Deadline RCS will run. Default: c5.Large instances will be launched.
        :param log_group_props: Properties for setting up the Render Queue's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param render_queue_size: Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue. Default: Allow no less than one Deadline RCS to be running.
        :param security_groups: Security groups to use for the Render Queue. Default: - new security groups are created
        :param traffic_encryption: Whether or not network traffic to the RenderQueue should be encrypted. Enabling this requires that all Deadline clients connect with TLS. Default: traffic is encrypted between Clients and the Render Queue and between its components
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param vpc_subnets_alb: The subnets into which to place the Application Load Balancer that is deployed. Default: - One Private subnet from each AZ.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ed8d99946cb7a2d5fabed2c862df495b001cb15bf80036a8bc9038e77998a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RenderQueueProps(
            images=images,
            repository=repository,
            version=version,
            vpc=vpc,
            access_logs=access_logs,
            deletion_protection=deletion_protection,
            enable_local_file_caching=enable_local_file_caching,
            health_check_config=health_check_config,
            hostname=hostname,
            instance_type=instance_type,
            log_group_props=log_group_props,
            render_queue_size=render_queue_size,
            security_groups=security_groups,
            traffic_encryption=traffic_encryption,
            vpc_subnets=vpc_subnets,
            vpc_subnets_alb=vpc_subnets_alb,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addBackendSecurityGroups")
    def add_backend_security_groups(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds security groups to the backend components of the Render Queue, which consists of the AutoScalingGroup for the Deadline RCS.

        :param security_groups: The security groups to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fece8ed0030db2902fbed388e48050502bf569294c86bbbe838a389ea55f985c)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addBackendSecurityGroups", [*security_groups]))

    @jsii.member(jsii_name="addChildDependency")
    def add_child_dependency(self, child: _constructs_77d1e7e8.IConstruct) -> None:
        '''Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the RenderQueue has been deployed and is ready to recieve traffic.

        This can be used to ensure that the RenderQueue is fully up and serving queries before a client attempts to connect to it.

        :param child: The child to make dependent upon this RenderQueue.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f92f98973954e818a3781bd1c7d19dbf1058650e19c7dfece4c1511a5a75ad)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast(None, jsii.invoke(self, "addChildDependency", [child]))

    @jsii.member(jsii_name="addFrontendSecurityGroups")
    def add_frontend_security_groups(
        self,
        *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Adds security groups to the frontend of the Render Queue, which is its load balancer.

        :param security_groups: The security groups to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec036f8dff121679b9d1261693a9cdd587eeebabb8b802d7007e11cae081d2a)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addFrontendSecurityGroups", [*security_groups]))

    @jsii.member(jsii_name="addSEPPolicies")
    def add_sep_policies(
        self,
        include_resource_tracker: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Adds AWS Managed Policies to the Render Queue so it is able to control Deadline's Spot Event Plugin.

        See: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html for additonal information.

        :param include_resource_tracker: Whether or not the Resource tracker admin policy should also be added (Default: True).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5737ac23037c32c853ea3c839170a3cb9ff5038a485e166495538c88cbfa51)
            check_type(argname="argument include_resource_tracker", value=include_resource_tracker, expected_type=type_hints["include_resource_tracker"])
        return typing.cast(None, jsii.invoke(self, "addSEPPolicies", [include_resource_tracker]))

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        hosts: typing.Sequence[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :inheritdoc: true
        '''
        param = ECSConnectOptions(grantee=grantee, hosts=hosts)

        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "configureClientECS", [param]))

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        restart_launcher: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param restart_launcher: Whether or not to start or restart the Deadline Launcher after configuring the connection. Default: true

        :inheritdoc: true
        '''
        param = InstanceConnectOptions(host=host, restart_launcher=restart_launcher)

        return typing.cast(None, jsii.invoke(self, "configureClientInstance", [param]))

    @jsii.member(jsii_name="configureSecretsManagementAutoRegistration")
    def configure_secrets_management_auto_registration(
        self,
        *,
        dependent: _constructs_77d1e7e8.Construct,
        registration_status: "SecretsManagementRegistrationStatus",
        role: "SecretsManagementRole",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Configure a rule to automatically register all Deadline Secrets Management identities connecting from a given subnet to a specified role and status.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-registration-settings-ref-label
        for details.

        All RFDK constructs that require Deadline Secrets Management identity registration call this method internally.
        End-users of RFDK should not need to use this method unless they have a special need and understand its inner
        workings.

        :param dependent: A construct node to make dependent on the registration setting being updated.
        :param registration_status: The Deadline Secrets Management registration status to be applied to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
        :param role: The role to be assigned to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
        :param vpc: The VPC of the Deadline Client host instances to be registered.
        :param vpc_subnets: The VPC subnets of the Deadline Client host instances to be registered.

        :inheritdoc: true
        '''
        props = SubnetIdentityRegistrationSettingsProps(
            dependent=dependent,
            registration_status=registration_status,
            role=role,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast(None, jsii.invoke(self, "configureSecretsManagementAutoRegistration", [props]))

    @builtins.property
    @jsii.member(jsii_name="asg")
    def asg(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        '''The Amazon EC2 Auto Scaling Group within the {@link RenderQueue.cluster} that contains the Deadline RCS's instances.'''
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "asg"))

    @builtins.property
    @jsii.member(jsii_name="backendConnections")
    def backend_connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''A connections object for controlling access of the compute resources that host the render queue.

        :inheritdoc: true
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "backendConnections"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.Cluster:
        '''The Amazon ECS cluster that is hosting the fleet of Deadline RCS applications.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Allows specifying security group connections for the Render Queue.

        :inheritdoc: true
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        '''The endpoint that Deadline clients can use to connect to the Render Queue.

        :inheritdoc: true
        '''
        return typing.cast(_ConnectableApplicationEndpoint_075040da, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer:
        '''The application load balancer that serves the traffic.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> IRepository:
        '''The Deadline Repository that the Render Queue services.

        :inheritdoc: true
        '''
        return typing.cast(IRepository, jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> IVersion:
        '''The version of Deadline that the RenderQueue uses.'''
        return typing.cast(IVersion, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="certChain")
    def cert_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''The secret containing the cert chain for external connections.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "certChain"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueAccessLogProps",
    jsii_struct_bases=[],
    name_mapping={"destination_bucket": "destinationBucket", "prefix": "prefix"},
)
class RenderQueueAccessLogProps:
    def __init__(
        self,
        *,
        destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for enabling access logs for the Render Queue's load balancer.

        See
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
        for more information on what gets logged and how to access them.

        :param destination_bucket: The S3 Bucket that the access logs should be stored in. It is recommended to set a lifecycle rule on this Bucket to avoid having it grow indefinitely. Costs will be incurred for requests made to put logs in the Bucket as well as storage.
        :param prefix: The prefix to be used for the access logs when they are stored in S3. Default: None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73101760f0868b5335905dde3ce348066e082ee85e4a24469f64ac33de3e645)
            check_type(argname="argument destination_bucket", value=destination_bucket, expected_type=type_hints["destination_bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_bucket": destination_bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def destination_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 Bucket that the access logs should be stored in.

        It is recommended to set a lifecycle rule on
        this Bucket to avoid having it grow indefinitely. Costs will be incurred for
        requests made to put logs in the Bucket as well as storage.
        '''
        result = self._values.get("destination_bucket")
        assert result is not None, "Required property 'destination_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix to be used for the access logs when they are stored in S3.

        :default: None
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueAccessLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueExternalTLSProps",
    jsii_struct_bases=[],
    name_mapping={
        "acm_certificate": "acmCertificate",
        "acm_certificate_chain": "acmCertificateChain",
        "enabled": "enabled",
        "rfdk_certificate": "rfdkCertificate",
    },
)
class RenderQueueExternalTLSProps:
    def __init__(
        self,
        *,
        acm_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        acm_certificate_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rfdk_certificate: typing.Optional[_IX509CertificatePem_da3ef30f] = None,
    ) -> None:
        '''Properties for configuring external TLS connections between the Render Queue and Deadline clients.

        You must provide one of the following combinations of properties:

        - acmCertificate ({@link @aws-cdk/aws-certificatemanager#ICertificate}) representing a certificate in ACM and
          acmCertificateChain ({@link @aws-cdk/aws-secretsmanager#ISecret}) containing the Certificate chain of the acmCertificate.
        - rfdkCertificate ({@link IX509CertificatePem}) Representing all of the properties of the certificate.

        In both cases the certificate chain **must** include only the CA certificates PEM file due to a known limitation in Deadline.

        :param acm_certificate: The ACM certificate that will be used for establishing incoming external TLS connections to the RenderQueue. Default: If rfdkCertificate and acmCertificate are both not provided when TLS is enabled, an rfdkCertificate will be generated and used.
        :param acm_certificate_chain: The secret containing the cert chain of the provided acmCert. This certifiate chain **must** include only the CA Certificates PEM file. Default: If an acmCertificate was provided then this must be provided, otherwise this is ignored.
        :param enabled: Whether to enable TLS between the Render Queue and Deadline clients. Default: true
        :param rfdk_certificate: The parameters for an X509 Certificate that will be imported into ACM then used by the RenderQueue. Default: If rfdkCertificate and acmCertificate are both not provided when TLS is enabled, an rfdkCertificate will be generated and used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3bec6cbece960d31a81a8445b158789cd2de49289e502f3cc82754fe4adb42d)
            check_type(argname="argument acm_certificate", value=acm_certificate, expected_type=type_hints["acm_certificate"])
            check_type(argname="argument acm_certificate_chain", value=acm_certificate_chain, expected_type=type_hints["acm_certificate_chain"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rfdk_certificate", value=rfdk_certificate, expected_type=type_hints["rfdk_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm_certificate is not None:
            self._values["acm_certificate"] = acm_certificate
        if acm_certificate_chain is not None:
            self._values["acm_certificate_chain"] = acm_certificate_chain
        if enabled is not None:
            self._values["enabled"] = enabled
        if rfdk_certificate is not None:
            self._values["rfdk_certificate"] = rfdk_certificate

    @builtins.property
    def acm_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''The ACM certificate that will be used for establishing incoming external TLS connections to the RenderQueue.

        :default: If rfdkCertificate and acmCertificate are both not provided when TLS is enabled, an rfdkCertificate will be generated and used.
        '''
        result = self._values.get("acm_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def acm_certificate_chain(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''The secret containing the cert chain of the provided acmCert.

        This certifiate chain **must** include only the CA Certificates PEM file.

        :default: If an acmCertificate was provided then this must be provided, otherwise this is ignored.
        '''
        result = self._values.get("acm_certificate_chain")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable TLS between the Render Queue and Deadline clients.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rfdk_certificate(self) -> typing.Optional[_IX509CertificatePem_da3ef30f]:
        '''The parameters for an X509 Certificate that will be imported into ACM then used by the RenderQueue.

        :default: If rfdkCertificate and acmCertificate are both not provided when TLS is enabled, an rfdkCertificate will be generated and used.
        '''
        result = self._values.get("rfdk_certificate")
        return typing.cast(typing.Optional[_IX509CertificatePem_da3ef30f], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueExternalTLSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueHealthCheckConfiguration",
    jsii_struct_bases=[],
    name_mapping={"check_interval": "checkInterval", "grace_period": "gracePeriod"},
)
class RenderQueueHealthCheckConfiguration:
    def __init__(
        self,
        *,
        check_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        grace_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Configuration for the health checks performed by the RenderQueue upon the Deadline RCS.

        These health checks periodically query the Deadline RCS to ensure that it is still operating
        nominally. If a Deadline RCS is found to not be operating nominally, then it will be terminated
        and automatically replaced.

        Please see {@link https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html}
        for additional information on this style of health check.

        :param check_interval: The approximate amount of time between health checks for an individual RCS instance. The value provided must be between 5 and 300 seconds. Default: 1 Minute
        :param grace_period: The startup duration where we will not perform health checks on newly created RCS instances. This should be at least a little longer than the time it takes for the Deadline RCS to start up. Default: 5 Minutes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050ab1ec2e1eae87e0d7233e4ce476edbd81e21e3bcf4d3fbda656ef822d91b9)
            check_type(argname="argument check_interval", value=check_interval, expected_type=type_hints["check_interval"])
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_interval is not None:
            self._values["check_interval"] = check_interval
        if grace_period is not None:
            self._values["grace_period"] = grace_period

    @builtins.property
    def check_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The approximate amount of time between health checks for an individual RCS instance.

        The value provided must be between 5 and 300 seconds.

        :default: 1 Minute
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def grace_period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The startup duration where we will not perform health checks on newly created RCS instances.

        This should be at least a little longer than the time it takes for the Deadline RCS to start up.

        :default: 5 Minutes
        '''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueHealthCheckConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueHostNameProps",
    jsii_struct_bases=[],
    name_mapping={"zone": "zone", "hostname": "hostname"},
)
class RenderQueueHostNameProps:
    def __init__(
        self,
        *,
        zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Parameters for the generation of a VPC-internal hostname for the RenderQueue.

        :param zone: The private zone to which the DNS A record for the render queue will be added. We do not recommend using an unregistered domain for your PrivateHostedZone and we have registered aws-rfdk.com that can be used if you do not own your own. Refer to RFC 6762 Appendix G for more details about private DNS namespaces: https://datatracker.ietf.org/doc/html/rfc6762#appendix-G
        :param hostname: The hostname to assign to the RenderQueue. A valid hostname is 1 to 63 characters long and may only contain: - letters from A-Z - digits from 0 to 9 - the hyphen (-) It must start with a letter and end with a letter or digit. Default: "renderqueue"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40591a8e194c9c058901f5636910f4e6a5112c43268f47299e27fb20d2c8d511)
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "zone": zone,
        }
        if hostname is not None:
            self._values["hostname"] = hostname

    @builtins.property
    def zone(self) -> _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone:
        '''The private zone to which the DNS A record for the render queue will be added.

        We do not recommend
        using an unregistered domain for your PrivateHostedZone and we have registered aws-rfdk.com that
        can be used if you do not own your own. Refer to RFC 6762 Appendix G for more details about private
        DNS namespaces: https://datatracker.ietf.org/doc/html/rfc6762#appendix-G
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to assign to the RenderQueue.

        A valid hostname is 1 to 63 characters long and may only contain:

        - letters from A-Z
        - digits from 0 to 9
        - the hyphen (-)
          It must start with a letter and end with a letter or digit.

        :default: "renderqueue"
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueHostNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueImages",
    jsii_struct_bases=[],
    name_mapping={"remote_connection_server": "remoteConnectionServer"},
)
class RenderQueueImages:
    def __init__(
        self,
        *,
        remote_connection_server: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    ) -> None:
        '''Collection of {@link ContainerImage}s required to deploy the RenderQueue.

        :param remote_connection_server: The AWS ECS container image from which the Deadline RCS will be run. This container **must** implement the same environment variable interface as defined in the official container images provided by AWS-Thinkbox. Note: A future change to the RenderQueue will make this property optional.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2077347bdbce4b13e4ec04196d18d06beb92412b531886f7e9e90f1fac39dece)
            check_type(argname="argument remote_connection_server", value=remote_connection_server, expected_type=type_hints["remote_connection_server"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_connection_server": remote_connection_server,
        }

    @builtins.property
    def remote_connection_server(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''The AWS ECS container image from which the Deadline RCS will be run.

        This container
        **must** implement the same environment variable interface as defined in the official
        container images provided by AWS-Thinkbox.

        Note: A future change to the RenderQueue will make this property optional.
        '''
        result = self._values.get("remote_connection_server")
        assert result is not None, "Required property 'remote_connection_server' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "images": "images",
        "repository": "repository",
        "version": "version",
        "vpc": "vpc",
        "access_logs": "accessLogs",
        "deletion_protection": "deletionProtection",
        "enable_local_file_caching": "enableLocalFileCaching",
        "health_check_config": "healthCheckConfig",
        "hostname": "hostname",
        "instance_type": "instanceType",
        "log_group_props": "logGroupProps",
        "render_queue_size": "renderQueueSize",
        "security_groups": "securityGroups",
        "traffic_encryption": "trafficEncryption",
        "vpc_subnets": "vpcSubnets",
        "vpc_subnets_alb": "vpcSubnetsAlb",
    },
)
class RenderQueueProps:
    def __init__(
        self,
        *,
        images: typing.Union[RenderQueueImages, typing.Dict[builtins.str, typing.Any]],
        repository: IRepository,
        version: IVersion,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        access_logs: typing.Optional[typing.Union[RenderQueueAccessLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        enable_local_file_caching: typing.Optional[builtins.bool] = None,
        health_check_config: typing.Optional[typing.Union[RenderQueueHealthCheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[typing.Union[RenderQueueHostNameProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        render_queue_size: typing.Optional[typing.Union["RenderQueueSizeConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Union["RenderQueueSecurityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_encryption: typing.Optional[typing.Union["RenderQueueTrafficEncryptionProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets_alb: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the Render Queue.

        :param images: A collection of Docker container images used to run the RenderQueue.
        :param repository: The Deadline Repository which the RCS instances will create a direct connection to.
        :param version: The Deadline Client version that will be running within this RenderQueue.
        :param vpc: VPC to launch the Render Queue in.
        :param access_logs: Properties for configuring access logging for the load balancer used by the Render Queue. This is disabled by default, but it is highly recommended to enable it to allow engineers to identify and root cause incidents such as unauthorized access. Default: - Access logging is disabled
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param enable_local_file_caching: If enabled, then Linux's cachefilesd will be installed and set to running on the ECS container host for the Deadline Remote Connection Server. This can reduce the amount of read throughput required for the Repository Filesystem. For more information, please see: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-fscache Note: If enabling this, then your Repository filesystem may require additional mount options to take advantage. Not every filesystem's driver supports integration with cachefilesd. e.g. NFS and Amazon EFS do support it, and require the 'fsc' mount option be provided. Note2: Your ECS container host will require access to port 80 on the regional S3 service when enabling this option so that it can install cachefilesd. This host is based on Amazon Linux 2, and the package repository for these systems is hosted on S3 and reached via port 80. Default: false
        :param health_check_config: Configuration for the health checks performed by the RenderQueue upon the Deadline RCS. Default: The values outlined in {@link RenderQueueHealthCheckConfiguration }
        :param hostname: Hostname to use to connect to the RenderQueue. Default: - The hostname ``renderqueue`` will be used and a PrivateHostedZone will be created with the domain name ``aws-rfdk.com``
        :param instance_type: The type of instance on which each Deadline RCS will run. Default: c5.Large instances will be launched.
        :param log_group_props: Properties for setting up the Render Queue's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param render_queue_size: Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue. Default: Allow no less than one Deadline RCS to be running.
        :param security_groups: Security groups to use for the Render Queue. Default: - new security groups are created
        :param traffic_encryption: Whether or not network traffic to the RenderQueue should be encrypted. Enabling this requires that all Deadline clients connect with TLS. Default: traffic is encrypted between Clients and the Render Queue and between its components
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param vpc_subnets_alb: The subnets into which to place the Application Load Balancer that is deployed. Default: - One Private subnet from each AZ.
        '''
        if isinstance(images, dict):
            images = RenderQueueImages(**images)
        if isinstance(access_logs, dict):
            access_logs = RenderQueueAccessLogProps(**access_logs)
        if isinstance(health_check_config, dict):
            health_check_config = RenderQueueHealthCheckConfiguration(**health_check_config)
        if isinstance(hostname, dict):
            hostname = RenderQueueHostNameProps(**hostname)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(render_queue_size, dict):
            render_queue_size = RenderQueueSizeConstraints(**render_queue_size)
        if isinstance(security_groups, dict):
            security_groups = RenderQueueSecurityGroups(**security_groups)
        if isinstance(traffic_encryption, dict):
            traffic_encryption = RenderQueueTrafficEncryptionProps(**traffic_encryption)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if isinstance(vpc_subnets_alb, dict):
            vpc_subnets_alb = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets_alb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea009a7f12a97b7efb261edfc69a17430aaf694438fe76bc1fb9158c16f1874)
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument access_logs", value=access_logs, expected_type=type_hints["access_logs"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument enable_local_file_caching", value=enable_local_file_caching, expected_type=type_hints["enable_local_file_caching"])
            check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument render_queue_size", value=render_queue_size, expected_type=type_hints["render_queue_size"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument traffic_encryption", value=traffic_encryption, expected_type=type_hints["traffic_encryption"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument vpc_subnets_alb", value=vpc_subnets_alb, expected_type=type_hints["vpc_subnets_alb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "images": images,
            "repository": repository,
            "version": version,
            "vpc": vpc,
        }
        if access_logs is not None:
            self._values["access_logs"] = access_logs
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_local_file_caching is not None:
            self._values["enable_local_file_caching"] = enable_local_file_caching
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if hostname is not None:
            self._values["hostname"] = hostname
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if render_queue_size is not None:
            self._values["render_queue_size"] = render_queue_size
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if traffic_encryption is not None:
            self._values["traffic_encryption"] = traffic_encryption
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if vpc_subnets_alb is not None:
            self._values["vpc_subnets_alb"] = vpc_subnets_alb

    @builtins.property
    def images(self) -> RenderQueueImages:
        '''A collection of Docker container images used to run the RenderQueue.'''
        result = self._values.get("images")
        assert result is not None, "Required property 'images' is missing"
        return typing.cast(RenderQueueImages, result)

    @builtins.property
    def repository(self) -> IRepository:
        '''The Deadline Repository which the RCS instances will create a direct connection to.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(IRepository, result)

    @builtins.property
    def version(self) -> IVersion:
        '''The Deadline Client version that will be running within this RenderQueue.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(IVersion, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the Render Queue in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def access_logs(self) -> typing.Optional[RenderQueueAccessLogProps]:
        '''Properties for configuring access logging for the load balancer used by the Render Queue.

        This is disabled by default, but it is highly recommended to enable it to
        allow engineers to identify and root cause incidents such as unauthorized access.

        :default: - Access logging is disabled
        '''
        result = self._values.get("access_logs")
        return typing.cast(typing.Optional[RenderQueueAccessLogProps], result)

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
    def enable_local_file_caching(self) -> typing.Optional[builtins.bool]:
        '''If enabled, then Linux's cachefilesd will be installed and set to running on the ECS container host for the Deadline Remote Connection Server.

        This can reduce
        the amount of read throughput required for the Repository Filesystem.

        For more information, please see: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-fscache

        Note: If enabling this, then your Repository filesystem may require additional
        mount options to take advantage. Not every filesystem's driver supports integration
        with cachefilesd. e.g. NFS and Amazon EFS do support it, and require the 'fsc' mount
        option be provided.

        Note2: Your ECS container host will require access to port 80 on the regional S3 service
        when enabling this option so that it can install cachefilesd. This host is based on
        Amazon Linux 2, and the package repository for these systems is hosted on S3 and reached
        via port 80.

        :default: false
        '''
        result = self._values.get("enable_local_file_caching")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_config(
        self,
    ) -> typing.Optional[RenderQueueHealthCheckConfiguration]:
        '''Configuration for the health checks performed by the RenderQueue upon the Deadline RCS.

        :default: The values outlined in {@link RenderQueueHealthCheckConfiguration }
        '''
        result = self._values.get("health_check_config")
        return typing.cast(typing.Optional[RenderQueueHealthCheckConfiguration], result)

    @builtins.property
    def hostname(self) -> typing.Optional[RenderQueueHostNameProps]:
        '''Hostname to use to connect to the RenderQueue.

        :default: - The hostname ``renderqueue`` will be used and a PrivateHostedZone will be created with the domain name ``aws-rfdk.com``
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[RenderQueueHostNameProps], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The type of instance on which each Deadline RCS will run.

        :default: c5.Large instances will be launched.
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''Properties for setting up the Render Queue's LogGroup.

        :default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def render_queue_size(self) -> typing.Optional["RenderQueueSizeConstraints"]:
        '''Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue.

        :default: Allow no less than one Deadline RCS to be running.
        '''
        result = self._values.get("render_queue_size")
        return typing.cast(typing.Optional["RenderQueueSizeConstraints"], result)

    @builtins.property
    def security_groups(self) -> typing.Optional["RenderQueueSecurityGroups"]:
        '''Security groups to use for the Render Queue.

        :default: - new security groups are created
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional["RenderQueueSecurityGroups"], result)

    @builtins.property
    def traffic_encryption(
        self,
    ) -> typing.Optional["RenderQueueTrafficEncryptionProps"]:
        '''Whether or not network traffic to the RenderQueue should be encrypted.

        Enabling this requires that all Deadline clients connect with TLS.

        :default: traffic is encrypted between Clients and the Render Queue and between its components
        '''
        result = self._values.get("traffic_encryption")
        return typing.cast(typing.Optional["RenderQueueTrafficEncryptionProps"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place instances within the VPC.

        :default: - All Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc_subnets_alb(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The subnets into which to place the Application Load Balancer that is deployed.

        :default: - One Private subnet from each AZ.
        '''
        result = self._values.get("vpc_subnets_alb")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueSecurityGroups",
    jsii_struct_bases=[],
    name_mapping={"backend": "backend", "frontend": "frontend"},
)
class RenderQueueSecurityGroups:
    def __init__(
        self,
        *,
        backend: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        frontend: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Security groups of the Render Queue.

        :param backend: The security group for the backend components of the Render Queue, which consists of the AutoScalingGroup for the Deadline RCS.
        :param frontend: The security group for the frontend of the Render Queue, which is its load balancer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5ab2581ffd8861c3d7b50043c7a9a129b8166eaca446d057891a31c1da5578)
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument frontend", value=frontend, expected_type=type_hints["frontend"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend is not None:
            self._values["backend"] = backend
        if frontend is not None:
            self._values["frontend"] = frontend

    @builtins.property
    def backend(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group for the backend components of the Render Queue, which consists of the AutoScalingGroup for the Deadline RCS.'''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def frontend(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group for the frontend of the Render Queue, which is its load balancer.'''
        result = self._values.get("frontend")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueSecurityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueSizeConstraints",
    jsii_struct_bases=[],
    name_mapping={"desired": "desired", "max": "max", "min": "min"},
)
class RenderQueueSizeConstraints:
    def __init__(
        self,
        *,
        desired: typing.Optional[jsii.Number] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Constraints on the number of Deadline RCS processes that will be created as part of this RenderQueue.

        The number of processes created will be equal to the desired capacity. Setting the minimum and
        maximum capacity provides constraints for modifying the number of processes dynamically via,
        say, the AWS Console.

        :param desired: The number of Deadline RCS processes that you want to create as part of this RenderQueue. If this is set to a number, every deployment will reset the number of RCS processes to this number. It is recommended to leave this value undefined. Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer. For these versions of Deadline, the desired number of processes can only be set to 1. Default: The min size.
        :param max: Maximum number of Deadline RCS processes that will serve RenderQueue requests. Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer. For these versions of Deadline, the maximum number of processes can only be set to 1, otherwise an error is thrown. The minimum that this value can be set to is 1. This value cannot be less than ``min`` or ``desired``. Default: 1
        :param min: Minimum number of Deadline RCS processes that will serve RenderQueue requests. Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer. For these versions of Deadline, the minimum number of processes can only be set to 1, otherwise an error is thrown. The minimum that this value can be set to is 1. Default: 1
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b43f6e9cf3327c7024d397d97df56d9722b6234099357d8712b4c8358a105b7)
            check_type(argname="argument desired", value=desired, expected_type=type_hints["desired"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if desired is not None:
            self._values["desired"] = desired
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def desired(self) -> typing.Optional[jsii.Number]:
        '''The number of Deadline RCS processes that you want to create as part of this RenderQueue.

        If this is set to a number, every deployment will reset the number of RCS processes
        to this number. It is recommended to leave this value undefined.

        Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer.
        For these versions of Deadline, the desired number of processes can only be set to 1.

        :default: The min size.
        '''
        result = self._values.get("desired")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of Deadline RCS processes that will serve RenderQueue requests.

        Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer.
        For these versions of Deadline, the maximum number of processes can only be set to 1, otherwise an error is thrown.

        The minimum that this value can be set to is 1.
        This value cannot be less than ``min`` or ``desired``.

        :default: 1
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of Deadline RCS processes that will serve RenderQueue requests.

        Deadline versions earlier than 10.1.10 do not support being horizontally scaled behind a load-balancer.
        For these versions of Deadline, the minimum number of processes can only be set to 1, otherwise an error is thrown.

        The minimum that this value can be set to is 1.

        :default: 1
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueSizeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueTrafficEncryptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "external_tls": "externalTLS",
        "internal_protocol": "internalProtocol",
    },
)
class RenderQueueTrafficEncryptionProps:
    def __init__(
        self,
        *,
        external_tls: typing.Optional[typing.Union[RenderQueueExternalTLSProps, typing.Dict[builtins.str, typing.Any]]] = None,
        internal_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    ) -> None:
        '''Interface to specify the protocols used (HTTP vs HTTPS) for communication between the Render Queue and clients and internally between the components of the RenderQueue.

        :param external_tls: Properties for configuring external TLS connections between the Render Queue and Deadline clients. Default: A default certificate is generated and HTTPS communication is used
        :param internal_protocol: Whether to encrypt traffic between the Application Load Balancer and its backing services. Default: HTTPS
        '''
        if isinstance(external_tls, dict):
            external_tls = RenderQueueExternalTLSProps(**external_tls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cac9e6e72e0c93ac86800c107707f0b5ace86418ee3d9b7d5654d9d6e19df57)
            check_type(argname="argument external_tls", value=external_tls, expected_type=type_hints["external_tls"])
            check_type(argname="argument internal_protocol", value=internal_protocol, expected_type=type_hints["internal_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_tls is not None:
            self._values["external_tls"] = external_tls
        if internal_protocol is not None:
            self._values["internal_protocol"] = internal_protocol

    @builtins.property
    def external_tls(self) -> typing.Optional[RenderQueueExternalTLSProps]:
        '''Properties for configuring external TLS connections between the Render Queue and Deadline clients.

        :default: A default certificate is generated and HTTPS communication is used
        '''
        result = self._values.get("external_tls")
        return typing.cast(typing.Optional[RenderQueueExternalTLSProps], result)

    @builtins.property
    def internal_protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''Whether to encrypt traffic between the Application Load Balancer and its backing services.

        :default: HTTPS
        '''
        result = self._values.get("internal_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueTrafficEncryptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRepository)
class Repository(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.Repository",
):
    '''This construct represents the main Deadline Repository which contains the central database and file system that Deadline requires.

    When deployed this construct will start up a single instance which will run the Deadline Repository installer to
    initialize the file system and database, the logs of which will be forwarded to Cloudwatch via a CloudWatchAgent.
    After the installation is complete the instance will be shutdown.

    Whenever the stack is updated if a change is detected in the installer a new instance will be started, which will perform
    a check on the existing Deadline Repository. If they are compatible with the new installer an update will be performed
    and the deployment will continue, otherwise the the deployment will be cancelled.
    In either case the instance will be cleaned up.

    architecture diagram


    Resources Deployed

    - Encrypted Amazon Elastic File System (EFS) - If no file system is provided.
    - An Amazon EFS Point - If no filesystem is provided.
    - An Amazon DocumentDB - If no database connection is provided.
    - Auto Scaling Group (ASG) with min & max capacity of 1 instance.
    - Instance Role and corresponding IAM Policy.
    - An Amazon CloudWatch log group that contains the Deadline Repository installation logs.
    - An RFDK PadEfsStorage - If no filesystem is provided.
    - An AWS Secrets Manager Secret - If no Secret with admin credentials for Deadline Secrets Management is provided.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The file system that is created by, or provided to, this construct contains the data for Deadline's Repository file
      system. This file system contains information about your submitted jobs, and the plugin scripts that are run by the
      Deadline applications in your render farm. An actor that can modify the contents of this file system can cause your
      Deadline applications to run code of their choosing. You should restrict access to this file system to only those who
      require it.
    - The database that is created by, or provided to, this construct is used by Deadline to store data about its configuration,
      submitted jobs, machine information and status, and so on. An actor with access to this database can read any information
      that is entered into Deadline, and modify the bevavior of your render farm. You should restrict access to this database
      to only those who require it.
    - If no file-system is provided to the Repository, then the Repository creates an EFS access point with unrestricted
      access to the entire EFS file-system. If you would like a single EFS file-system that is used by the Deadline
      Repository and other agents, you should supply the file-system and a access-restricted EFS access point to the
      Repository construct instead.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        version: IVersion,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        backup_options: typing.Optional[typing.Union["RepositoryBackupOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        database: typing.Optional[DatabaseConnection] = None,
        database_audit_logging: typing.Optional[builtins.bool] = None,
        document_db_instance_count: typing.Optional[jsii.Number] = None,
        file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[typing.Union["RepositoryRemovalPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_installation_prefix: typing.Optional[builtins.str] = None,
        repository_installation_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        repository_settings: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        secrets_management_settings: typing.Optional[typing.Union["SecretsManagementProps", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups_options: typing.Optional[typing.Union["RepositorySecurityGroupsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: Version property to specify the version of deadline repository to be installed. This, in future, would be an optional property. If not passed, it should fetch the latest version of deadline. The current implementation of Version construct only supports importing it with static values, hence keeping it mandatory for now.
        :param vpc: VPC to launch the Repository In.
        :param backup_options: Define the backup options for the resources that this Repository creates. Default: Duration.days(15) for the database
        :param database: Specify the database where the deadline schema needs to be initialized. Note that Deadline supports only databases that are compatible with MongoDB 5.0 and greater. Default: A Document DB Cluster will be created with a single db.r5.large instance.
        :param database_audit_logging: If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled. Audit logs are a security best-practice. They record connection, data definition language (DDL), user management, and authorization events within the database, and are useful for post-incident auditing. That is, they can help you figure out what an unauthorized user, who gained access to your database, has done with that access. Default: true
        :param document_db_instance_count: If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created. Default: 1
        :param file_system: Specify the file system where the deadline repository needs to be initialized. If not providing a filesystem, then we will provision an Amazon EFS filesystem for you. This filesystem will contain files for the Deadline Repository filesystem. It will also contain 40GB of additional padding files (see RFDK's PadEfsStorage for details) to increase the baseline throughput of the filesystem; these files will be added to the /RFDK_PaddingFiles directory in the filesystem. Default: An Encrypted EFS File System and Access Point will be created.
        :param log_group_props: Properties for setting up the Deadline Repository's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param removal_policy: Define the removal policies for the resources that this Repository creates. These define what happens to the resoureces when the stack that defines them is destroyed. Default: RemovalPolicy.RETAIN for all resources
        :param repository_installation_prefix: The prefix for the Deadline Repository installation path on the mounted file system. Default: : "/DeadlineRepository/"
        :param repository_installation_timeout: The length of time to wait for the repository installation before considering it as failure. The maximum value is 43200 (12 hours). Default: Duration.minutes(30)
        :param repository_settings: The Deadline Repository settings file to import. Default: Repository settings are not imported.
        :param secrets_management_settings: Define the settings used by Deadline Secrets Management, a feature introduced in Deadline 10.1.10 for securely managing storage and access of Secrets for your render farm. More details at: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html. Default: : Secrets Management will be enabled and a username and password will be automatically generated if none are supplied.
        :param security_groups_options: Options to add additional security groups to the Repository.
        :param vpc_subnets: All resources that are created by this Repository will be deployed to these Subnets. This includes the Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets to which they are deployed. Default: : Private subnets in the VPC
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f99a81718b7293f5270ff48249692460af35b328a2a8aa6cca5be92ad132b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RepositoryProps(
            version=version,
            vpc=vpc,
            backup_options=backup_options,
            database=database,
            database_audit_logging=database_audit_logging,
            document_db_instance_count=document_db_instance_count,
            file_system=file_system,
            log_group_props=log_group_props,
            removal_policy=removal_policy,
            repository_installation_prefix=repository_installation_prefix,
            repository_installation_timeout=repository_installation_timeout,
            repository_settings=repository_settings,
            secrets_management_settings=secrets_management_settings,
            security_groups_options=security_groups_options,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: typing.Union[ECSContainerInstanceProps, typing.Dict[builtins.str, typing.Any]],
        containers: typing.Union[ECSTaskProps, typing.Dict[builtins.str, typing.Any]],
    ) -> IContainerDirectRepositoryConnection:
        '''Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :inheritdoc: true
        '''
        props = ECSDirectConnectProps(
            container_instances=container_instances, containers=containers
        )

        return typing.cast(IContainerDirectRepositoryConnection, jsii.invoke(self, "configureClientECS", [props]))

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        '''Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.

        :inheritdoc: true
        '''
        props = InstanceDirectConnectProps(host=host, mount_point=mount_point)

        return typing.cast(None, jsii.invoke(self, "configureClientInstance", [props]))

    @builtins.property
    @jsii.member(jsii_name="databaseConnection")
    def database_connection(self) -> DatabaseConnection:
        '''Connection object for the database for this repository.'''
        return typing.cast(DatabaseConnection, jsii.get(self, "databaseConnection"))

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _IMountableLinuxFilesystem_5182ce0b:
        '''The Linux-mountable filesystem that will store the Deadline repository filesystem contents.'''
        return typing.cast(_IMountableLinuxFilesystem_5182ce0b, jsii.get(self, "fileSystem"))

    @builtins.property
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        '''The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.

        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "rootPrefix"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagementSettings")
    def secrets_management_settings(self) -> "SecretsManagementProps":
        '''Deadline Secrets Management settings.

        :inheritdoc: true
        '''
        return typing.cast("SecretsManagementProps", jsii.get(self, "secretsManagementSettings"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> IVersion:
        '''The version of Deadline for Linux that is installed on this Repository.

        :inheritdoc: true
        '''
        return typing.cast(IVersion, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="efs")
    def efs(self) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.FileSystem]:
        '''The underlying Amazon Elastic File System (EFS) used by the Repository.

        This is only defined if this Repository created its own filesystem, otherwise it will be ``undefined``.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.FileSystem], jsii.get(self, "efs"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryBackupOptions",
    jsii_struct_bases=[],
    name_mapping={"database_retention": "databaseRetention"},
)
class RepositoryBackupOptions:
    def __init__(
        self,
        *,
        database_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties for backups of resources that are created by the Repository.

        :param database_retention: If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention period to use on the database. If the Repository is not creating a DocumentDB database, because one was given, then this property is ignored. Please visit https://aws.amazon.com/documentdb/pricing/ to learn more about DocumentDB backup storage pricing. Default: Duration.days(15)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d97ba60da610c56fc5818d385e906bf0628c8b7c85d49eb18dd683bf251f97)
            check_type(argname="argument database_retention", value=database_retention, expected_type=type_hints["database_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_retention is not None:
            self._values["database_retention"] = database_retention

    @builtins.property
    def database_retention(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention period to use on the database.

        If the Repository is not creating a DocumentDB database, because one was given,
        then this property is ignored.
        Please visit https://aws.amazon.com/documentdb/pricing/ to learn more about DocumentDB backup storage pricing.

        :default: Duration.days(15)
        '''
        result = self._values.get("database_retention")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryBackupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "vpc": "vpc",
        "backup_options": "backupOptions",
        "database": "database",
        "database_audit_logging": "databaseAuditLogging",
        "document_db_instance_count": "documentDbInstanceCount",
        "file_system": "fileSystem",
        "log_group_props": "logGroupProps",
        "removal_policy": "removalPolicy",
        "repository_installation_prefix": "repositoryInstallationPrefix",
        "repository_installation_timeout": "repositoryInstallationTimeout",
        "repository_settings": "repositorySettings",
        "secrets_management_settings": "secretsManagementSettings",
        "security_groups_options": "securityGroupsOptions",
        "vpc_subnets": "vpcSubnets",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        version: IVersion,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        backup_options: typing.Optional[typing.Union[RepositoryBackupOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        database: typing.Optional[DatabaseConnection] = None,
        database_audit_logging: typing.Optional[builtins.bool] = None,
        document_db_instance_count: typing.Optional[jsii.Number] = None,
        file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[typing.Union["RepositoryRemovalPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_installation_prefix: typing.Optional[builtins.str] = None,
        repository_installation_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        repository_settings: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        secrets_management_settings: typing.Optional[typing.Union["SecretsManagementProps", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups_options: typing.Optional[typing.Union["RepositorySecurityGroupsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the Deadline repository.

        :param version: Version property to specify the version of deadline repository to be installed. This, in future, would be an optional property. If not passed, it should fetch the latest version of deadline. The current implementation of Version construct only supports importing it with static values, hence keeping it mandatory for now.
        :param vpc: VPC to launch the Repository In.
        :param backup_options: Define the backup options for the resources that this Repository creates. Default: Duration.days(15) for the database
        :param database: Specify the database where the deadline schema needs to be initialized. Note that Deadline supports only databases that are compatible with MongoDB 5.0 and greater. Default: A Document DB Cluster will be created with a single db.r5.large instance.
        :param database_audit_logging: If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled. Audit logs are a security best-practice. They record connection, data definition language (DDL), user management, and authorization events within the database, and are useful for post-incident auditing. That is, they can help you figure out what an unauthorized user, who gained access to your database, has done with that access. Default: true
        :param document_db_instance_count: If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created. Default: 1
        :param file_system: Specify the file system where the deadline repository needs to be initialized. If not providing a filesystem, then we will provision an Amazon EFS filesystem for you. This filesystem will contain files for the Deadline Repository filesystem. It will also contain 40GB of additional padding files (see RFDK's PadEfsStorage for details) to increase the baseline throughput of the filesystem; these files will be added to the /RFDK_PaddingFiles directory in the filesystem. Default: An Encrypted EFS File System and Access Point will be created.
        :param log_group_props: Properties for setting up the Deadline Repository's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param removal_policy: Define the removal policies for the resources that this Repository creates. These define what happens to the resoureces when the stack that defines them is destroyed. Default: RemovalPolicy.RETAIN for all resources
        :param repository_installation_prefix: The prefix for the Deadline Repository installation path on the mounted file system. Default: : "/DeadlineRepository/"
        :param repository_installation_timeout: The length of time to wait for the repository installation before considering it as failure. The maximum value is 43200 (12 hours). Default: Duration.minutes(30)
        :param repository_settings: The Deadline Repository settings file to import. Default: Repository settings are not imported.
        :param secrets_management_settings: Define the settings used by Deadline Secrets Management, a feature introduced in Deadline 10.1.10 for securely managing storage and access of Secrets for your render farm. More details at: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html. Default: : Secrets Management will be enabled and a username and password will be automatically generated if none are supplied.
        :param security_groups_options: Options to add additional security groups to the Repository.
        :param vpc_subnets: All resources that are created by this Repository will be deployed to these Subnets. This includes the Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets to which they are deployed. Default: : Private subnets in the VPC
        '''
        if isinstance(backup_options, dict):
            backup_options = RepositoryBackupOptions(**backup_options)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(removal_policy, dict):
            removal_policy = RepositoryRemovalPolicies(**removal_policy)
        if isinstance(secrets_management_settings, dict):
            secrets_management_settings = SecretsManagementProps(**secrets_management_settings)
        if isinstance(security_groups_options, dict):
            security_groups_options = RepositorySecurityGroupsOptions(**security_groups_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42179c3dc6ac9346e35102fd03089d4440b6bdf471dda6d8d9654e194358bc6)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument backup_options", value=backup_options, expected_type=type_hints["backup_options"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument database_audit_logging", value=database_audit_logging, expected_type=type_hints["database_audit_logging"])
            check_type(argname="argument document_db_instance_count", value=document_db_instance_count, expected_type=type_hints["document_db_instance_count"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument repository_installation_prefix", value=repository_installation_prefix, expected_type=type_hints["repository_installation_prefix"])
            check_type(argname="argument repository_installation_timeout", value=repository_installation_timeout, expected_type=type_hints["repository_installation_timeout"])
            check_type(argname="argument repository_settings", value=repository_settings, expected_type=type_hints["repository_settings"])
            check_type(argname="argument secrets_management_settings", value=secrets_management_settings, expected_type=type_hints["secrets_management_settings"])
            check_type(argname="argument security_groups_options", value=security_groups_options, expected_type=type_hints["security_groups_options"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
            "vpc": vpc,
        }
        if backup_options is not None:
            self._values["backup_options"] = backup_options
        if database is not None:
            self._values["database"] = database
        if database_audit_logging is not None:
            self._values["database_audit_logging"] = database_audit_logging
        if document_db_instance_count is not None:
            self._values["document_db_instance_count"] = document_db_instance_count
        if file_system is not None:
            self._values["file_system"] = file_system
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if repository_installation_prefix is not None:
            self._values["repository_installation_prefix"] = repository_installation_prefix
        if repository_installation_timeout is not None:
            self._values["repository_installation_timeout"] = repository_installation_timeout
        if repository_settings is not None:
            self._values["repository_settings"] = repository_settings
        if secrets_management_settings is not None:
            self._values["secrets_management_settings"] = secrets_management_settings
        if security_groups_options is not None:
            self._values["security_groups_options"] = security_groups_options
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def version(self) -> IVersion:
        '''Version property to specify the version of deadline repository to be installed.

        This, in future, would be an optional property. If not passed, it should fetch
        the latest version of deadline. The current implementation of Version construct
        only supports importing it with static values, hence keeping it mandatory for now.
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(IVersion, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the Repository In.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def backup_options(self) -> typing.Optional[RepositoryBackupOptions]:
        '''Define the backup options for the resources that this Repository creates.

        :default: Duration.days(15) for the database
        '''
        result = self._values.get("backup_options")
        return typing.cast(typing.Optional[RepositoryBackupOptions], result)

    @builtins.property
    def database(self) -> typing.Optional[DatabaseConnection]:
        '''Specify the database where the deadline schema needs to be initialized.

        Note that Deadline supports only databases that are compatible with MongoDB 5.0 and greater.

        :default: A Document DB Cluster will be created with a single db.r5.large instance.
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[DatabaseConnection], result)

    @builtins.property
    def database_audit_logging(self) -> typing.Optional[builtins.bool]:
        '''If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled.

        Audit logs are a security best-practice. They record connection, data definition language (DDL), user management,
        and authorization events within the database, and are useful for post-incident auditing. That is, they can help you
        figure out what an unauthorized user, who gained access to your database, has done with that access.

        :default: true
        '''
        result = self._values.get("database_audit_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def document_db_instance_count(self) -> typing.Optional[jsii.Number]:
        '''If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created.

        :default: 1
        '''
        result = self._values.get("document_db_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_system(self) -> typing.Optional[_IMountableLinuxFilesystem_5182ce0b]:
        '''Specify the file system where the deadline repository needs to be initialized.

        If not providing a filesystem, then we will provision an Amazon EFS filesystem for you.
        This filesystem will contain files for the Deadline Repository filesystem. It will also
        contain 40GB of additional padding files (see RFDK's PadEfsStorage for details) to increase
        the baseline throughput of the filesystem; these files will be added to the /RFDK_PaddingFiles directory
        in the filesystem.

        :default: An Encrypted EFS File System and Access Point will be created.
        '''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional[_IMountableLinuxFilesystem_5182ce0b], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''Properties for setting up the Deadline Repository's LogGroup in CloudWatch.

        :default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["RepositoryRemovalPolicies"]:
        '''Define the removal policies for the resources that this Repository creates.

        These define what happens
        to the resoureces when the stack that defines them is destroyed.

        :default: RemovalPolicy.RETAIN for all resources
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["RepositoryRemovalPolicies"], result)

    @builtins.property
    def repository_installation_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix for the Deadline Repository installation path on the mounted file system.

        :default: : "/DeadlineRepository/"
        '''
        result = self._values.get("repository_installation_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_installation_timeout(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time to wait for the repository installation before considering it as failure.

        The maximum value is 43200 (12 hours).

        :default: Duration.minutes(30)
        '''
        result = self._values.get("repository_installation_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def repository_settings(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset]:
        '''The Deadline Repository settings file to import.

        :default: Repository settings are not imported.

        :see: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/repository-settings-importer-exporter.html
        '''
        result = self._values.get("repository_settings")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset], result)

    @builtins.property
    def secrets_management_settings(self) -> typing.Optional["SecretsManagementProps"]:
        '''Define the settings used by Deadline Secrets Management, a feature introduced in Deadline 10.1.10 for securely managing storage and access of Secrets for your render farm. More details at: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html.

        :default: : Secrets Management will be enabled and a username and password will be automatically generated if none are supplied.
        '''
        result = self._values.get("secrets_management_settings")
        return typing.cast(typing.Optional["SecretsManagementProps"], result)

    @builtins.property
    def security_groups_options(
        self,
    ) -> typing.Optional["RepositorySecurityGroupsOptions"]:
        '''Options to add additional security groups to the Repository.'''
        result = self._values.get("security_groups_options")
        return typing.cast(typing.Optional["RepositorySecurityGroupsOptions"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''All resources that are created by this Repository will be deployed to these Subnets.

        This includes the
        Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating
        an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets
        to which they are deployed.

        :default: : Private subnets in the VPC
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryRemovalPolicies",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "filesystem": "filesystem"},
)
class RepositoryRemovalPolicies:
    def __init__(
        self,
        *,
        database: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        filesystem: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param database: If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention policy to use on the database. If the Repository is not creating a DocumentDB database, because one was given, then this property is ignored. Default: RemovalPolicy.RETAIN
        :param filesystem: If this Repository is creating its own Amazon Elastic File System (EFS), then this specifies the retention policy to use on the filesystem. If the Repository is not creating an EFS, because one was given, then this property is ignored. Default: RemovalPolicy.RETAIN
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8b7efa858fe0522801e80042aa2d58c92d4229626c35bdd23be296f860be9c)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if filesystem is not None:
            self._values["filesystem"] = filesystem

    @builtins.property
    def database(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention policy to use on the database.

        If the Repository is not creating a DocumentDB database, because one was given,
        then this property is ignored.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''If this Repository is creating its own Amazon Elastic File System (EFS), then this specifies the retention policy to use on the filesystem.

        If the Repository is not creating an EFS, because one was given, then this property is ignored.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRemovalPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositorySecurityGroupsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "file_system": "fileSystem",
        "installer": "installer",
    },
)
class RepositorySecurityGroupsOptions:
    def __init__(
        self,
        *,
        database: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        file_system: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        installer: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Options for the security groups of the Repository.

        :param database: The security group for the database of the Repository. This is ignored if the Repository is not creating its own DocumentDB database because one was given.
        :param file_system: The security group for the filesystem of the Repository. This is ignored if the Repository is not creating its own Amazon Elastic File System (EFS) because one was given.
        :param installer: The security group for the AutoScalingGroup of the instance that runs the Deadline Repository installer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdbca0093e88164369525a7e1f6612cd09bc1b81400e0e32b0ef9a4fcf71acd)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
            check_type(argname="argument installer", value=installer, expected_type=type_hints["installer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if file_system is not None:
            self._values["file_system"] = file_system
        if installer is not None:
            self._values["installer"] = installer

    @builtins.property
    def database(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group for the database of the Repository.

        This is ignored if the Repository is not creating
        its own DocumentDB database because one was given.
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def file_system(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group for the filesystem of the Repository.

        This is ignored if the Repository is not creating
        its own Amazon Elastic File System (EFS) because one was given.
        '''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def installer(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group for the AutoScalingGroup of the instance that runs the Deadline Repository installer.'''
        result = self._values.get("installer")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositorySecurityGroupsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.SecretsManagementProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "credentials": "credentials",
        "credentials_removal_policy": "credentialsRemovalPolicy",
    },
)
class SecretsManagementProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        credentials: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        credentials_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''Settings used by Deadline Secrets Management, a feature introduced in Deadline 10.1.10 for securely managing storage and access of Secrets for your render farm. More details at: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html Using Secrets Management requires TLS to be enabled between the RenderQueue and its clients. If this feature is enabled, the ``externalTLS`` on the ``RenderQueueTrafficEncryptionProps`` interface on the RenderQueue cannot be disabled.

        :param enabled: Whether or not to enable the Secrets Management feature.
        :param credentials: A Secret containing the username and password to use for the admin role. The contents of this secret must be a JSON document with the keys "username" and "password". ex: { "username": , "password": , } Password should be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one symbol and one number. In the case when the password does not meet the requirements, the repository construct will fail to deploy. It is highly recommended that you leave this parameter undefined to enable the automatic generation of a strong password. Default: : A random username and password will be generated in a Secret with ID ``SMAdminUser`` and will need to be retrieved from AWS Secrets Manager if it is needed
        :param credentials_removal_policy: If Secret with admin credentials is not defined in property ``credentials``, then this specifies the retention policy to use on the Secret with generated credentials. If Secret with credentials is provided, then this property is ignored. Default: RemovalPolicy.RETAIN
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a692e77f4defe52e9939b229241edfba1b691d01647ec09ebf21d64d6b63759)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument credentials_removal_policy", value=credentials_removal_policy, expected_type=type_hints["credentials_removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if credentials_removal_policy is not None:
            self._values["credentials_removal_policy"] = credentials_removal_policy

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Whether or not to enable the Secrets Management feature.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''A Secret containing the username and password to use for the admin role.

        The contents of this secret must be a JSON document with the keys "username" and "password". ex:
        {
        "username": ,
        "password": ,
        }
        Password should be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one symbol and one number.
        In the case when the password does not meet the requirements, the repository construct will fail to deploy.
        It is highly recommended that you leave this parameter undefined to enable the automatic generation of a strong password.

        :default: : A random username and password will be generated in a Secret with ID ``SMAdminUser`` and will need to be retrieved from AWS Secrets Manager if it is needed
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def credentials_removal_policy(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''If Secret with admin credentials is not defined in property ``credentials``, then this specifies the retention policy to use on the Secret with generated credentials.

        If Secret with credentials is provided, then this property is ignored.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("credentials_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsManagementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.deadline.SecretsManagementRegistrationStatus")
class SecretsManagementRegistrationStatus(enum.Enum):
    '''The different possible Deadline Secrets Management registration statuses that a Deadline Client's identity can be set to.

    See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
    '''

    PENDING = "PENDING"
    '''This is the default status for an Identity that has just registered itself.

    It cannot access any secrets with this status.
    '''
    REGISTERED = "REGISTERED"
    '''This status allows Identities to make use of the Secrets API, so long as they have the appropriate `Identity Role <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-roles-ref-label>`_.'''
    REVOKED = "REVOKED"
    '''Identities with this status will not be allowed to make use of the Secrets API.'''


@jsii.enum(jsii_type="aws-rfdk.deadline.SecretsManagementRole")
class SecretsManagementRole(enum.Enum):
    '''Deadline Secrets Management roles.

    See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
    '''

    ADMINISTRATOR = "ADMINISTRATOR"
    '''The administrator role is given to users that are created either by the Repository Installer when enabling the Deadline Secrets Management feature for the first time, or by running the CreateNewAdmin command.

    Note: there can
    be more than one Administrator user. All Administrators are equal and have full read and write access to all
    secrets.
    '''
    SERVER = "SERVER"
    '''The Server role is intended to be granted to your machine(s) running the `Remote Connection Server <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-connection-server.html#remote-connection-server-ref-label>`_ application. The Server role is granted to a registered machine by an administrator in the `Monitor UI <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-assigning-ref-label>`_. In order to encrypt and decrypt secrets, the master key must be assigned to the Server by an Administrator user running the `GrantKeyAccessToServer command <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#deadline-secrets-management-command-grantkeyaccesstoserver>`_. Servers can encrypt and decrypt all secrets, and are responsible for providing secrets to approved clients.'''
    CLIENT = "CLIENT"
    '''The Client role is typically intended to be granted to any of your machines running the `Worker <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/worker.html#worker-ref-label>`_ application. The Client role is granted to a registered machine by an administrator in the `Monitor UI <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#identity-management-assigning-ref-label>`_. Clients can request storage of secrets not in the `Administrator Secret Access Level <https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#deadline-secrets-management-secret-namespace-ref-label>`_, and can retrieve secrets from all namespaces when authenticating through the server.'''


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotEventPluginDisplayInstanceStatus")
class SpotEventPluginDisplayInstanceStatus(enum.Enum):
    '''The Worker Extra Info column to be used to display AWS Instance Status if the instance has been marked to be stopped or terminated by EC2 or Spot Event Plugin.

    See "AWS Instance Status" option at https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options
    and https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/worker-config.html#extra-info
    '''

    DISABLED = "DISABLED"
    EXTRA_INFO_0 = "EXTRA_INFO_0"
    EXTRA_INFO_1 = "EXTRA_INFO_1"
    EXTRA_INFO_2 = "EXTRA_INFO_2"
    EXTRA_INFO_3 = "EXTRA_INFO_3"
    EXTRA_INFO_4 = "EXTRA_INFO_4"
    EXTRA_INFO_5 = "EXTRA_INFO_5"
    EXTRA_INFO_6 = "EXTRA_INFO_6"
    EXTRA_INFO_7 = "EXTRA_INFO_7"
    EXTRA_INFO_8 = "EXTRA_INFO_8"
    EXTRA_INFO_9 = "EXTRA_INFO_9"


@jsii.implements(ISpotEventPluginFleet)
class SpotEventPluginFleet(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.SpotEventPluginFleet",
):
    '''This construct reperesents a fleet from the Spot Fleet Request created by the Spot Event Plugin.

    This fleet is intended to be used as input for the {@link @aws-rfdk/deadline#ConfigureSpotEventPlugin} construct.

    The construct itself doesn't create the Spot Fleet Request, but deploys all the resources
    required for the Spot Fleet Request and generates the Spot Fleet Configuration setting:
    a one to one mapping between a Deadline Group and Spot Fleet Request Configurations.

    architecture diagram


    Resources Deployed

    - An Instance Role, corresponding IAM Policy and an Instance Profile.
    - A Fleet Role and corresponding IAM Policy.
    - An Amazon CloudWatch log group that contains the Deadline Worker, Deadline Launcher, and instance-startup logs for the instances
      in the fleet.
    - A security Group if security groups are not provided.
    - An EC2 Launch Template for the Spot Fleet.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The data that is stored on your Worker's local EBS volume can include temporary working files from the applications
      that are rendering your jobs and tasks. That data can be sensitive or privileged, so we recommend that you encrypt
      the data volumes of these instances using either the provided option or by using an encrypted AMI as your source.
    - The software on the AMI that is being used by this construct may pose a security risk. We recommend that you adopt a
      patching strategy to keep this software current with the latest security patches. Please see
      https://docs.aws.amazon.com/rfdk/latest/guide/patching-software.html for more information.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        deadline_groups: typing.Sequence[builtins.str],
        instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
        max_capacity: jsii.Number,
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        allocation_strategy: typing.Optional["SpotFleetAllocationStrategy"] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        context: typing.Optional[builtins.str] = None,
        deadline_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        deadline_region: typing.Optional[builtins.str] = None,
        fleet_instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        track_instances_with_resource_tracker: typing.Optional[builtins.bool] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        valid_until: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param deadline_groups: Deadline groups these workers need to be assigned to. Also, note that the Spot Fleet configuration does not allow using wildcards as part of the Group name as described here https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#wildcards
        :param instance_types: Types of instances to launch.
        :param max_capacity: The the maximum capacity that the Spot Fleet can grow to. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#spot-fleet-requests
        :param render_queue: The RenderQueue that Worker fleet should connect to.
        :param vpc: VPC to launch the Worker fleet in.
        :param worker_machine_image: The AMI of the Deadline Worker to launch.
        :param allocation_strategy: Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request. Default: - SpotFleetAllocationStrategy.LOWEST_PRICE.
        :param block_devices: The Block devices that will be attached to your workers. Default: - The default devices of the provided ami will be used.
        :param context: Reserved. Default: - No context string
        :param deadline_pools: Deadline pools these workers need to be assigned to. Default: - Workers are not assigned to any pool.
        :param deadline_region: Deadline region these workers needs to be assigned to. Note that this is not an AWS region but a Deadline region used for path mapping. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/cross-platform.html#regions Default: - Worker is not assigned to any Deadline region.
        :param fleet_instance_role: An IAM role to associate with the instance profile assigned to its resources. Create this role on the same stack with the SpotEventPluginFleet to avoid circular dependencies. The role must be assumable by the service principal ``ec2.amazonaws.com`` and have AWSThinkboxDeadlineSpotEventPluginWorkerPolicy policy attached:: const role = new iam.Role(this, 'MyRole', { assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'), managedPolicies: [ ManagedPolicy.fromAwsManagedPolicyName('AWSThinkboxDeadlineSpotEventPluginWorkerPolicy'), ], }); Default: - A role will automatically be created.
        :param fleet_role: An IAM role for the spot fleet. The role must be assumable by the service principal ``spotfleet.amazonaws.com`` and have AmazonEC2SpotFleetTaggingRole policy attached Example:: const role = new iam.Role(this, 'FleetRole', { assumedBy: new iam.ServicePrincipal('spotfleet.amazonaws.com'), managedPolicies: [ ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2SpotFleetTaggingRole'), ], }); Default: - A role will automatically be created.
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param security_groups: Security Groups to assign to this fleet. Default: - A new security group will be created automatically.
        :param track_instances_with_resource_tracker: Whether the instances in the Spot Fleet should be tracked by Deadline Resource Tracker. In addition to this property, the Spot Event Plugin must also be configured to use the Resource tracker by using the ```enableResourceTracker`` <https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk.deadline.SpotEventPluginSettings.html#enableresourcetracker>`_ property of the ``ConfigureSpotEventPlugin`` construct, which is ``true`` by default. Default: true
        :param user_data: User data that instances use when starting up. Default: - User data will be created automatically.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired. Default: : Not used.
        :param valid_until: The end date and time of the request. After the end date and time, no new Spot Instance requests are placed or able to fulfill the request. Default: - the Spot Fleet request remains until you cancel it.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366f31a28b730ce5a7a5b3de617afb7209cd13b567df3aed6c91c9fd7c754919)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SpotEventPluginFleetProps(
            deadline_groups=deadline_groups,
            instance_types=instance_types,
            max_capacity=max_capacity,
            render_queue=render_queue,
            vpc=vpc,
            worker_machine_image=worker_machine_image,
            allocation_strategy=allocation_strategy,
            block_devices=block_devices,
            context=context,
            deadline_pools=deadline_pools,
            deadline_region=deadline_region,
            fleet_instance_role=fleet_instance_role,
            fleet_role=fleet_role,
            key_name=key_name,
            log_group_props=log_group_props,
            security_groups=security_groups,
            track_instances_with_resource_tracker=track_instances_with_resource_tracker,
            user_data=user_data,
            user_data_provider=user_data_provider,
            valid_until=valid_until,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allowRemoteControlFrom")
    def allow_remote_control_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowRemoteControlTo().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlFrom(Peer.ipv4('10.0.0.0/24'))``

        :param other: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab275f821b69a802c37ee2cb63c834aac1982012c8f3d304c85e07314c3a6f1)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowRemoteControlFrom", [other]))

    @jsii.member(jsii_name="allowRemoteControlTo")
    def allow_remote_control_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the Worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowRemoteControlFrom().
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/remote-control.html

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowRemoteControlTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowRemoteControlTo(Peer.ipv4('10.0.0.0/24'))``

        :param other: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8018d7f2b9fdd4242798b8492d9a28756f8fc7f62b7714225725e91d67b2e7c7)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowRemoteControlTo", [other]))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> "SpotFleetAllocationStrategy":
        '''Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request.'''
        return typing.cast("SpotFleetAllocationStrategy", jsii.get(self, "allocationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The security groups/rules used to allow network connections.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="deadlineGroups")
    def deadline_groups(self) -> typing.List[builtins.str]:
        '''Deadline groups the workers need to be assigned to.

        :default: - Workers are not assigned to any group
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deadlineGroups"))

    @builtins.property
    @jsii.member(jsii_name="defaultSubnets")
    def default_subnets(self) -> builtins.bool:
        '''Indicates whether the subnets are the defaults.

        If ``props.vpcSubnets`` was passed in, this
        will be false.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "defaultSubnets"))

    @builtins.property
    @jsii.member(jsii_name="fleetInstanceRole")
    def fleet_instance_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''An IAM role associated with the instance profile assigned to its resources.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "fleetInstanceRole"))

    @builtins.property
    @jsii.member(jsii_name="fleetRole")
    def fleet_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''An IAM role that grants the Spot Fleet the permission to request, launch, terminate, and tag instances on your behalf.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "fleetRole"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.

        Granting permissions to this principal will grant
        those permissions to the spot instance role.
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfile")
    def instance_profile(self) -> _aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile:
        '''The IAM instance profile that fleet instance role is associated to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile, jsii.get(self, "instanceProfile"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Types of instances to launch.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], jsii.get(self, "instanceTypes"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> _aws_cdk_aws_ec2_ceddda9d.LaunchTemplate:
        '''The Launch Template for this Spot Fleet.

        This launch template does not specify an instance type or subnet.
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.LaunchTemplate, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="machineImage")
    def machine_image(self) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''The Worker AMI.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.get(self, "machineImage"))

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        '''The  the maximum capacity that the Spot Fleet can grow to.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#spot-fleet-requests
        '''
        return typing.cast(jsii.Number, jsii.get(self, "maxCapacity"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> _aws_cdk_aws_ec2_ceddda9d.OperatingSystemType:
        '''The operating system of the script host.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.OperatingSystemType, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="remoteControlPorts")
    def remote_control_ports(self) -> _aws_cdk_aws_ec2_ceddda9d.Port:
        '''The port workers listen on to share their logs.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Port, jsii.get(self, "remoteControlPorts"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Groups assigned to this fleet.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''Subnets where the instance will be placed within the VPC.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, jsii.get(self, "subnets"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''The tags to apply during creation of instances and of the Spot Fleet Request.'''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''The user data that instances use when starting up.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.get(self, "userData"))

    @builtins.property
    @jsii.member(jsii_name="blockDevices")
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]]:
        '''The Block devices that will be attached to your workers.

        :default: - The default devices of the provided ami will be used.
        '''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]], jsii.get(self, "blockDevices"))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[builtins.str]:
        '''Reserved.

        :default: - No context string
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "context"))

    @builtins.property
    @jsii.member(jsii_name="deadlinePools")
    def deadline_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline pools the workers need to be assigned to.

        :default: - Workers are not assigned to any pool
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deadlinePools"))

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of SSH keypair to grant access to instances.

        :default: - No SSH access will be possible.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyName"))

    @builtins.property
    @jsii.member(jsii_name="validUntil")
    def valid_until(self) -> typing.Optional[_aws_cdk_ceddda9d.Expiration]:
        '''The end date and time of the request.

        After the end date and time, no new Spot Instance requests are placed or able to fulfill the request.

        :default: - the Spot Fleet request remains until you cancel it.
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Expiration], jsii.get(self, "validUntil"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.SpotEventPluginFleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "deadline_groups": "deadlineGroups",
        "instance_types": "instanceTypes",
        "max_capacity": "maxCapacity",
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "worker_machine_image": "workerMachineImage",
        "allocation_strategy": "allocationStrategy",
        "block_devices": "blockDevices",
        "context": "context",
        "deadline_pools": "deadlinePools",
        "deadline_region": "deadlineRegion",
        "fleet_instance_role": "fleetInstanceRole",
        "fleet_role": "fleetRole",
        "key_name": "keyName",
        "log_group_props": "logGroupProps",
        "security_groups": "securityGroups",
        "track_instances_with_resource_tracker": "trackInstancesWithResourceTracker",
        "user_data": "userData",
        "user_data_provider": "userDataProvider",
        "valid_until": "validUntil",
        "vpc_subnets": "vpcSubnets",
    },
)
class SpotEventPluginFleetProps:
    def __init__(
        self,
        *,
        deadline_groups: typing.Sequence[builtins.str],
        instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
        max_capacity: jsii.Number,
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        allocation_strategy: typing.Optional["SpotFleetAllocationStrategy"] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        context: typing.Optional[builtins.str] = None,
        deadline_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        deadline_region: typing.Optional[builtins.str] = None,
        fleet_instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        track_instances_with_resource_tracker: typing.Optional[builtins.bool] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        valid_until: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the Spot Event Plugin Worker Fleet.

        :param deadline_groups: Deadline groups these workers need to be assigned to. Also, note that the Spot Fleet configuration does not allow using wildcards as part of the Group name as described here https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#wildcards
        :param instance_types: Types of instances to launch.
        :param max_capacity: The the maximum capacity that the Spot Fleet can grow to. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#spot-fleet-requests
        :param render_queue: The RenderQueue that Worker fleet should connect to.
        :param vpc: VPC to launch the Worker fleet in.
        :param worker_machine_image: The AMI of the Deadline Worker to launch.
        :param allocation_strategy: Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request. Default: - SpotFleetAllocationStrategy.LOWEST_PRICE.
        :param block_devices: The Block devices that will be attached to your workers. Default: - The default devices of the provided ami will be used.
        :param context: Reserved. Default: - No context string
        :param deadline_pools: Deadline pools these workers need to be assigned to. Default: - Workers are not assigned to any pool.
        :param deadline_region: Deadline region these workers needs to be assigned to. Note that this is not an AWS region but a Deadline region used for path mapping. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/cross-platform.html#regions Default: - Worker is not assigned to any Deadline region.
        :param fleet_instance_role: An IAM role to associate with the instance profile assigned to its resources. Create this role on the same stack with the SpotEventPluginFleet to avoid circular dependencies. The role must be assumable by the service principal ``ec2.amazonaws.com`` and have AWSThinkboxDeadlineSpotEventPluginWorkerPolicy policy attached:: const role = new iam.Role(this, 'MyRole', { assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'), managedPolicies: [ ManagedPolicy.fromAwsManagedPolicyName('AWSThinkboxDeadlineSpotEventPluginWorkerPolicy'), ], }); Default: - A role will automatically be created.
        :param fleet_role: An IAM role for the spot fleet. The role must be assumable by the service principal ``spotfleet.amazonaws.com`` and have AmazonEC2SpotFleetTaggingRole policy attached Example:: const role = new iam.Role(this, 'FleetRole', { assumedBy: new iam.ServicePrincipal('spotfleet.amazonaws.com'), managedPolicies: [ ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2SpotFleetTaggingRole'), ], }); Default: - A role will automatically be created.
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param security_groups: Security Groups to assign to this fleet. Default: - A new security group will be created automatically.
        :param track_instances_with_resource_tracker: Whether the instances in the Spot Fleet should be tracked by Deadline Resource Tracker. In addition to this property, the Spot Event Plugin must also be configured to use the Resource tracker by using the ```enableResourceTracker`` <https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk.deadline.SpotEventPluginSettings.html#enableresourcetracker>`_ property of the ``ConfigureSpotEventPlugin`` construct, which is ``true`` by default. Default: true
        :param user_data: User data that instances use when starting up. Default: - User data will be created automatically.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired. Default: : Not used.
        :param valid_until: The end date and time of the request. After the end date and time, no new Spot Instance requests are placed or able to fulfill the request. Default: - the Spot Fleet request remains until you cancel it.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        '''
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24b850e03104788afddc109df2e6fb0604829a3a0c78abded4f8d0ddf7a8a36)
            check_type(argname="argument deadline_groups", value=deadline_groups, expected_type=type_hints["deadline_groups"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument render_queue", value=render_queue, expected_type=type_hints["render_queue"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument worker_machine_image", value=worker_machine_image, expected_type=type_hints["worker_machine_image"])
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deadline_pools", value=deadline_pools, expected_type=type_hints["deadline_pools"])
            check_type(argname="argument deadline_region", value=deadline_region, expected_type=type_hints["deadline_region"])
            check_type(argname="argument fleet_instance_role", value=fleet_instance_role, expected_type=type_hints["fleet_instance_role"])
            check_type(argname="argument fleet_role", value=fleet_role, expected_type=type_hints["fleet_role"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument track_instances_with_resource_tracker", value=track_instances_with_resource_tracker, expected_type=type_hints["track_instances_with_resource_tracker"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument user_data_provider", value=user_data_provider, expected_type=type_hints["user_data_provider"])
            check_type(argname="argument valid_until", value=valid_until, expected_type=type_hints["valid_until"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deadline_groups": deadline_groups,
            "instance_types": instance_types,
            "max_capacity": max_capacity,
            "render_queue": render_queue,
            "vpc": vpc,
            "worker_machine_image": worker_machine_image,
        }
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if context is not None:
            self._values["context"] = context
        if deadline_pools is not None:
            self._values["deadline_pools"] = deadline_pools
        if deadline_region is not None:
            self._values["deadline_region"] = deadline_region
        if fleet_instance_role is not None:
            self._values["fleet_instance_role"] = fleet_instance_role
        if fleet_role is not None:
            self._values["fleet_role"] = fleet_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if track_instances_with_resource_tracker is not None:
            self._values["track_instances_with_resource_tracker"] = track_instances_with_resource_tracker
        if user_data is not None:
            self._values["user_data"] = user_data
        if user_data_provider is not None:
            self._values["user_data_provider"] = user_data_provider
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def deadline_groups(self) -> typing.List[builtins.str]:
        '''Deadline groups these workers need to be assigned to.

        Also, note that the Spot Fleet configuration does not allow using wildcards as part of the Group name
        as described here https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#wildcards
        '''
        result = self._values.get("deadline_groups")
        assert result is not None, "Required property 'deadline_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Types of instances to launch.'''
        result = self._values.get("instance_types")
        assert result is not None, "Required property 'instance_types' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        '''The  the maximum capacity that the Spot Fleet can grow to.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#spot-fleet-requests
        '''
        result = self._values.get("max_capacity")
        assert result is not None, "Required property 'max_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def render_queue(self) -> IRenderQueue:
        '''The RenderQueue that Worker fleet should connect to.'''
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return typing.cast(IRenderQueue, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the Worker fleet in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def worker_machine_image(self) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''The AMI of the Deadline Worker to launch.'''
        result = self._values.get("worker_machine_image")
        assert result is not None, "Required property 'worker_machine_image' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, result)

    @builtins.property
    def allocation_strategy(self) -> typing.Optional["SpotFleetAllocationStrategy"]:
        '''Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request.

        :default: - SpotFleetAllocationStrategy.LOWEST_PRICE.
        '''
        result = self._values.get("allocation_strategy")
        return typing.cast(typing.Optional["SpotFleetAllocationStrategy"], result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]]:
        '''The Block devices that will be attached to your workers.

        :default: - The default devices of the provided ami will be used.
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]], result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Reserved.

        :default: - No context string
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deadline_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline pools these workers need to be assigned to.

        :default: - Workers are not assigned to any pool.
        '''
        result = self._values.get("deadline_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deadline_region(self) -> typing.Optional[builtins.str]:
        '''Deadline region these workers needs to be assigned to.

        Note that this is not an AWS region but a Deadline region used for path mapping.
        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/cross-platform.html#regions

        :default: - Worker is not assigned to any Deadline region.
        '''
        result = self._values.get("deadline_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to its resources.

        Create this role on the same stack with the SpotEventPluginFleet to avoid circular dependencies.

        The role must be assumable by the service principal ``ec2.amazonaws.com`` and
        have AWSThinkboxDeadlineSpotEventPluginWorkerPolicy policy attached::

           const role = new iam.Role(this, 'MyRole', {
             assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
             managedPolicies: [
               ManagedPolicy.fromAwsManagedPolicyName('AWSThinkboxDeadlineSpotEventPluginWorkerPolicy'),
             ],
           });

        :default: - A role will automatically be created.
        '''
        result = self._values.get("fleet_instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role for the spot fleet.

        The role must be assumable by the service principal ``spotfleet.amazonaws.com``
        and have AmazonEC2SpotFleetTaggingRole policy attached Example::

           const role = new iam.Role(this, 'FleetRole', {
             assumedBy: new iam.ServicePrincipal('spotfleet.amazonaws.com'),
             managedPolicies: [
               ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2SpotFleetTaggingRole'),
             ],
           });

        :default: - A role will automatically be created.
        '''
        result = self._values.get("fleet_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of SSH keypair to grant access to instances.

        :default: - No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''Properties for setting up the Deadline Worker's LogGroup.

        :default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''Security Groups to assign to this fleet.

        :default: - A new security group will be created automatically.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def track_instances_with_resource_tracker(self) -> typing.Optional[builtins.bool]:
        '''Whether the instances in the Spot Fleet should be tracked by Deadline Resource Tracker.

        In addition to this property, the Spot Event Plugin must also be configured to use the Resource tracker by using the
        ```enableResourceTracker`` <https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk.deadline.SpotEventPluginSettings.html#enableresourcetracker>`_
        property of the ``ConfigureSpotEventPlugin`` construct, which is ``true`` by default.

        :default: true
        '''
        result = self._values.get("track_instances_with_resource_tracker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''User data that instances use when starting up.

        :default: - User data will be created automatically.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def user_data_provider(self) -> typing.Optional[IInstanceUserDataProvider]:
        '''An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle.

        You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.

        :default: : Not used.
        '''
        result = self._values.get("user_data_provider")
        return typing.cast(typing.Optional[IInstanceUserDataProvider], result)

    @builtins.property
    def valid_until(self) -> typing.Optional[_aws_cdk_ceddda9d.Expiration]:
        '''The end date and time of the request.

        After the end date and time, no new Spot Instance requests are placed or able to fulfill the request.

        :default: - the Spot Fleet request remains until you cancel it.
        '''
        result = self._values.get("valid_until")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Expiration], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotEventPluginFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotEventPluginLoggingLevel")
class SpotEventPluginLoggingLevel(enum.Enum):
    '''Logging verbosity levels for the Spot Event Plugin.'''

    STANDARD = "STANDARD"
    '''Standard logging level.'''
    VERBOSE = "VERBOSE"
    '''Detailed logging about the inner workings of the Spot Event Plugin.'''
    DEBUG = "DEBUG"
    '''All Verbose logs plus additional information on AWS API calls that are used.'''
    OFF = "OFF"
    '''No logging enabled.'''


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotEventPluginPreJobTaskMode")
class SpotEventPluginPreJobTaskMode(enum.Enum):
    '''How the Spot Event Plugin should handle Pre Job Tasks.

    See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-scripts.html
    '''

    CONSERVATIVE = "CONSERVATIVE"
    '''Only start 1 Spot instance for the pre job task and ignore any other tasks for that job until the pre job task is completed.'''
    IGNORE = "IGNORE"
    '''Do not take the pre job task into account when calculating target capacity.'''
    NORMAL = "NORMAL"
    '''Treat the pre job task like a regular job queued task.'''


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.SpotEventPluginSettings",
    jsii_struct_bases=[],
    name_mapping={
        "aws_instance_status": "awsInstanceStatus",
        "delete_ec2_spot_interrupted_workers": "deleteEC2SpotInterruptedWorkers",
        "delete_sep_terminated_workers": "deleteSEPTerminatedWorkers",
        "enable_resource_tracker": "enableResourceTracker",
        "idle_shutdown": "idleShutdown",
        "logging_level": "loggingLevel",
        "maximum_instances_started_per_cycle": "maximumInstancesStartedPerCycle",
        "pre_job_task_mode": "preJobTaskMode",
        "region": "region",
        "state": "state",
        "strict_hard_cap": "strictHardCap",
    },
)
class SpotEventPluginSettings:
    def __init__(
        self,
        *,
        aws_instance_status: typing.Optional[SpotEventPluginDisplayInstanceStatus] = None,
        delete_ec2_spot_interrupted_workers: typing.Optional[builtins.bool] = None,
        delete_sep_terminated_workers: typing.Optional[builtins.bool] = None,
        enable_resource_tracker: typing.Optional[builtins.bool] = None,
        idle_shutdown: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging_level: typing.Optional[SpotEventPluginLoggingLevel] = None,
        maximum_instances_started_per_cycle: typing.Optional[jsii.Number] = None,
        pre_job_task_mode: typing.Optional[SpotEventPluginPreJobTaskMode] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional["SpotEventPluginState"] = None,
        strict_hard_cap: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''The settings of the Spot Event Plugin.

        For more details see https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/event-spot.html#event-plugin-configuration-options

        :param aws_instance_status: The Worker Extra Info column to be used to display AWS Instance Status if the instance has been marked to be stopped or terminated by EC2 or Spot Event Plugin. All timestamps are displayed in UTC format. Default: SpotEventPluginDisplayInstanceStatus.DISABLED
        :param delete_ec2_spot_interrupted_workers: Determines if EC2 Spot interrupted AWS Workers will be deleted from the Workers Panel on the next House Cleaning cycle. Default: false
        :param delete_sep_terminated_workers: Determines if Deadline Spot Event Plugin terminated AWS Workers will be deleted from the Workers Panel on the next House Cleaning cycle. Default: false
        :param enable_resource_tracker: Determines whether the Deadline Resource Tracker should be used. In addition to this property, the Spot Instances deployed by the Spot Event Plugin must also be configured to be tracked by the Resource Tracker using the ```trackInstancesWithResourceTracker`` <https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk.deadline.SpotEventPluginFleet.html#trackinstanceswithresourcetracker>`_ property of the ``SpotEventPluginFleet`` construct, which is ``true`` by default. You can set that property to ``false`` for fleets that you would like to opt out of the Resource Tracker. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/resource-tracker-overview.html Default: true
        :param idle_shutdown: The length of time that an AWS Worker will wait in a non-rendering state before it is shutdown. Should evenly divide into minutes. Default: Duration.minutes(10)
        :param logging_level: Spot Event Plugin logging level. Note that Spot Event Plugin adds output to the logs of the render queue and the Workers. Default: SpotEventPluginLoggingLevel.STANDARD
        :param maximum_instances_started_per_cycle: The Spot Event Plugin will request this maximum number of instances per House Cleaning cycle. Default: 50
        :param pre_job_task_mode: Determines how the Spot Event Plugin should handle Pre Job Tasks. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-scripts.html Default: SpotEventPluginPreJobTaskMode.CONSERVATIVE
        :param region: The AWS region in which to start the spot fleet request. Default: The region of the Render Queue if it is available; otherwise the region of the current stack.
        :param state: How the event plug-in should respond to events. Default: SpotEventPluginState.GLOBAL_ENABLED
        :param strict_hard_cap: Determines if any active instances greater than the target capacity for each group will be terminated. Workers may be terminated even while rendering. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc3317f9d5b90675b9845a5ed84cfedde7f7fd5900a04b0b7bc66a2b8460cf6)
            check_type(argname="argument aws_instance_status", value=aws_instance_status, expected_type=type_hints["aws_instance_status"])
            check_type(argname="argument delete_ec2_spot_interrupted_workers", value=delete_ec2_spot_interrupted_workers, expected_type=type_hints["delete_ec2_spot_interrupted_workers"])
            check_type(argname="argument delete_sep_terminated_workers", value=delete_sep_terminated_workers, expected_type=type_hints["delete_sep_terminated_workers"])
            check_type(argname="argument enable_resource_tracker", value=enable_resource_tracker, expected_type=type_hints["enable_resource_tracker"])
            check_type(argname="argument idle_shutdown", value=idle_shutdown, expected_type=type_hints["idle_shutdown"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument maximum_instances_started_per_cycle", value=maximum_instances_started_per_cycle, expected_type=type_hints["maximum_instances_started_per_cycle"])
            check_type(argname="argument pre_job_task_mode", value=pre_job_task_mode, expected_type=type_hints["pre_job_task_mode"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument strict_hard_cap", value=strict_hard_cap, expected_type=type_hints["strict_hard_cap"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_instance_status is not None:
            self._values["aws_instance_status"] = aws_instance_status
        if delete_ec2_spot_interrupted_workers is not None:
            self._values["delete_ec2_spot_interrupted_workers"] = delete_ec2_spot_interrupted_workers
        if delete_sep_terminated_workers is not None:
            self._values["delete_sep_terminated_workers"] = delete_sep_terminated_workers
        if enable_resource_tracker is not None:
            self._values["enable_resource_tracker"] = enable_resource_tracker
        if idle_shutdown is not None:
            self._values["idle_shutdown"] = idle_shutdown
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if maximum_instances_started_per_cycle is not None:
            self._values["maximum_instances_started_per_cycle"] = maximum_instances_started_per_cycle
        if pre_job_task_mode is not None:
            self._values["pre_job_task_mode"] = pre_job_task_mode
        if region is not None:
            self._values["region"] = region
        if state is not None:
            self._values["state"] = state
        if strict_hard_cap is not None:
            self._values["strict_hard_cap"] = strict_hard_cap

    @builtins.property
    def aws_instance_status(
        self,
    ) -> typing.Optional[SpotEventPluginDisplayInstanceStatus]:
        '''The Worker Extra Info column to be used to display AWS Instance Status if the instance has been marked to be stopped or terminated by EC2 or Spot Event Plugin.

        All timestamps are displayed in UTC format.

        :default: SpotEventPluginDisplayInstanceStatus.DISABLED
        '''
        result = self._values.get("aws_instance_status")
        return typing.cast(typing.Optional[SpotEventPluginDisplayInstanceStatus], result)

    @builtins.property
    def delete_ec2_spot_interrupted_workers(self) -> typing.Optional[builtins.bool]:
        '''Determines if EC2 Spot interrupted AWS Workers will be deleted from the Workers Panel on the next House Cleaning cycle.

        :default: false
        '''
        result = self._values.get("delete_ec2_spot_interrupted_workers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delete_sep_terminated_workers(self) -> typing.Optional[builtins.bool]:
        '''Determines if Deadline Spot Event Plugin terminated AWS Workers will be deleted from the Workers Panel on the next House Cleaning cycle.

        :default: false
        '''
        result = self._values.get("delete_sep_terminated_workers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_resource_tracker(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Deadline Resource Tracker should be used.

        In addition to this property, the Spot Instances deployed by the Spot Event Plugin must also be configured to be tracked by the Resource Tracker using the
        ```trackInstancesWithResourceTracker`` <https://docs.aws.amazon.com/rfdk/api/latest/docs/aws-rfdk.deadline.SpotEventPluginFleet.html#trackinstanceswithresourcetracker>`_
        property of the ``SpotEventPluginFleet`` construct, which is ``true`` by default. You can set that property to ``false`` for fleets that you would like to opt out of the
        Resource Tracker.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/resource-tracker-overview.html

        :default: true
        '''
        result = self._values.get("enable_resource_tracker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def idle_shutdown(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time that an AWS Worker will wait in a non-rendering state before it is shutdown.

        Should evenly divide into minutes.

        :default: Duration.minutes(10)
        '''
        result = self._values.get("idle_shutdown")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[SpotEventPluginLoggingLevel]:
        '''Spot Event Plugin logging level.

        Note that Spot Event Plugin adds output to the logs of the render queue and the Workers.

        :default: SpotEventPluginLoggingLevel.STANDARD
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[SpotEventPluginLoggingLevel], result)

    @builtins.property
    def maximum_instances_started_per_cycle(self) -> typing.Optional[jsii.Number]:
        '''The Spot Event Plugin will request this maximum number of instances per House Cleaning cycle.

        :default: 50
        '''
        result = self._values.get("maximum_instances_started_per_cycle")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pre_job_task_mode(self) -> typing.Optional[SpotEventPluginPreJobTaskMode]:
        '''Determines how the Spot Event Plugin should handle Pre Job Tasks.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-scripts.html

        :default: SpotEventPluginPreJobTaskMode.CONSERVATIVE
        '''
        result = self._values.get("pre_job_task_mode")
        return typing.cast(typing.Optional[SpotEventPluginPreJobTaskMode], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region in which to start the spot fleet request.

        :default: The region of the Render Queue if it is available; otherwise the region of the current stack.
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional["SpotEventPluginState"]:
        '''How the event plug-in should respond to events.

        :default: SpotEventPluginState.GLOBAL_ENABLED
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional["SpotEventPluginState"], result)

    @builtins.property
    def strict_hard_cap(self) -> typing.Optional[builtins.bool]:
        '''Determines if any active instances greater than the target capacity for each group will be terminated.

        Workers may be terminated even while rendering.

        :default: false
        '''
        result = self._values.get("strict_hard_cap")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotEventPluginSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotEventPluginState")
class SpotEventPluginState(enum.Enum):
    '''How the event plug-in should respond to events.'''

    GLOBAL_ENABLED = "GLOBAL_ENABLED"
    '''The Render Queue, all jobs and Workers will trigger the events for this plugin.'''
    DISABLED = "DISABLED"
    '''No events are triggered for the plugin.'''


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotFleetAllocationStrategy")
class SpotFleetAllocationStrategy(enum.Enum):
    '''The allocation strategy for the Spot Instances in your Spot Fleet determines how it fulfills your Spot Fleet request from the possible Spot Instance pools represented by its launch specifications.

    See https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-configuration-strategies.html#ec2-fleet-allocation-strategy
    '''

    LOWEST_PRICE = "LOWEST_PRICE"
    '''Spot Fleet launches instances from the Spot Instance pools with the lowest price.'''
    DIVERSIFIED = "DIVERSIFIED"
    '''Spot Fleet launches instances from all the Spot Instance pools that you specify.'''
    CAPACITY_OPTIMIZED = "CAPACITY_OPTIMIZED"
    '''Spot Fleet launches instances from Spot Instance pools with optimal capacity for the number of instances that are launching.'''


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotFleetRequestType")
class SpotFleetRequestType(enum.Enum):
    '''The type of request.

    Indicates whether the Spot Fleet only requests the target capacity or also attempts to maintain it.
    Only 'maintain' is currently supported.
    '''

    MAINTAIN = "MAINTAIN"
    '''The Spot Fleet maintains the target capacity.

    The Spot Fleet places the required requests to meet capacity and automatically replenishes any interrupted instances.
    '''


@jsii.enum(jsii_type="aws-rfdk.deadline.SpotFleetResourceType")
class SpotFleetResourceType(enum.Enum):
    '''Resource types that presently support tag on create.'''

    INSTANCE = "INSTANCE"
    '''EC2 Instances.'''
    SPOT_FLEET_REQUEST = "SPOT_FLEET_REQUEST"
    '''Spot fleet requests.'''


class Stage(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.deadline.Stage"):
    '''Class for interacting with the Deadline stage directory.

    The stage is a directory that conforms to a conventional structure that RFDK
    requires to deploy Deadline. It should contain a manifest file, the Deadline
    installers, and any supporting files required for building the Deadline
    container.

    Note: Current version of RFDK supports Deadline v10.1.9.2 and later.
    '''

    def __init__(
        self,
        *,
        manifest: typing.Union[Manifest, typing.Dict[builtins.str, typing.Any]],
        path: builtins.str,
    ) -> None:
        '''Constructs a Stage instance.

        :param manifest: The parsed manifest that describes the contents of the stage directory.
        :param path: The path to the directory where Deadline is staged.
        '''
        props = StageProps(manifest=manifest, path=path)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromDirectory")
    @builtins.classmethod
    def from_directory(cls, stage_path: builtins.str) -> "Stage":
        '''Returns a {@link Stage} loaded using the specified directory as the Docker build context and loads and uses the manifest named ``manifest.json`` in the directory.

        :param stage_path: The path to the Deadline stage directory.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a61c8cdf837b3b2964992fc2d1c8dae86a2496a6bf3c633f5aa3d87838519a7)
            check_type(argname="argument stage_path", value=stage_path, expected_type=type_hints["stage_path"])
        return typing.cast("Stage", jsii.sinvoke(cls, "fromDirectory", [stage_path]))

    @jsii.member(jsii_name="loadManifest")
    @builtins.classmethod
    def load_manifest(cls, manifest_path: builtins.str) -> Manifest:
        '''Loads and parses the manifest file from a given path.

        :param manifest_path: The path to the manifest JSON file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9548d598c3482f4994b40ccbfd44253eb8e537c4063f34509b25502f2a63c1)
            check_type(argname="argument manifest_path", value=manifest_path, expected_type=type_hints["manifest_path"])
        return typing.cast(Manifest, jsii.sinvoke(cls, "loadManifest", [manifest_path]))

    @jsii.member(jsii_name="getVersion")
    def get_version(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> IVersion:
        '''Creates a {@link Version} based on the manifest version.

        :param scope: The parent scope.
        :param id: The construct ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3da84ed7aec5ea6a88184e8d81776a34b7ae17b963f2fe8ea5c901df6fd2e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(IVersion, jsii.invoke(self, "getVersion", [scope, id]))

    @jsii.member(jsii_name="imageFromRecipe")
    def image_from_recipe(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        recipe_name: builtins.str,
    ) -> _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset:
        '''Construct a {@link DockerImageAsset} instance from a recipe in the Stage.

        :param scope: The scope for the {@link DockerImageAsset}.
        :param id: The construct ID of the {@link DockerImageAsset}.
        :param recipe_name: The name of the recipe.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cf6f738174c7ba86904f9fceee22a78d543f24630b1d49294855dc393b8609)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast(_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset, jsii.invoke(self, "imageFromRecipe", [scope, id, recipe_name]))

    @builtins.property
    @jsii.member(jsii_name="clientInstallerPath")
    def client_installer_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientInstallerPath"))

    @builtins.property
    @jsii.member(jsii_name="dirPath")
    def dir_path(self) -> builtins.str:
        '''The path to the stage directory.'''
        return typing.cast(builtins.str, jsii.get(self, "dirPath"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> Manifest:
        '''The parsed manifest within the stage directory.'''
        return typing.cast(Manifest, jsii.get(self, "manifest"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.StageProps",
    jsii_struct_bases=[],
    name_mapping={"manifest": "manifest", "path": "path"},
)
class StageProps:
    def __init__(
        self,
        *,
        manifest: typing.Union[Manifest, typing.Dict[builtins.str, typing.Any]],
        path: builtins.str,
    ) -> None:
        '''Constructor properties of the {@link Stage} class.

        :param manifest: The parsed manifest that describes the contents of the stage directory.
        :param path: The path to the directory where Deadline is staged.
        '''
        if isinstance(manifest, dict):
            manifest = Manifest(**manifest)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac94b28fc77e31ee86750d20e26d8f44b4b1adfc18588b335f3100640c5fee60)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manifest": manifest,
            "path": path,
        }

    @builtins.property
    def manifest(self) -> Manifest:
        '''The parsed manifest that describes the contents of the stage directory.'''
        result = self._values.get("manifest")
        assert result is not None, "Required property 'manifest' is missing"
        return typing.cast(Manifest, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to the directory where Deadline is staged.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.SubnetIdentityRegistrationSettingsProps",
    jsii_struct_bases=[],
    name_mapping={
        "dependent": "dependent",
        "registration_status": "registrationStatus",
        "role": "role",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SubnetIdentityRegistrationSettingsProps:
    def __init__(
        self,
        *,
        dependent: _constructs_77d1e7e8.Construct,
        registration_status: SecretsManagementRegistrationStatus,
        role: SecretsManagementRole,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Properties that specify how to deploy and configure an identity registration setting for a specified VPC subnet.

        :param dependent: A construct node to make dependent on the registration setting being updated.
        :param registration_status: The Deadline Secrets Management registration status to be applied to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
        :param role: The role to be assigned to the Deadline Client identities that connect from the specified VPC subnets. See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
        :param vpc: The VPC of the Deadline Client host instances to be registered.
        :param vpc_subnets: The VPC subnets of the Deadline Client host instances to be registered.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0053659919d4730a89b9fbcf980fc7ef02b65174f2fec86a91184e7a34ccf9)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument registration_status", value=registration_status, expected_type=type_hints["registration_status"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dependent": dependent,
            "registration_status": registration_status,
            "role": role,
            "vpc": vpc,
            "vpc_subnets": vpc_subnets,
        }

    @builtins.property
    def dependent(self) -> _constructs_77d1e7e8.Construct:
        '''A construct node to make dependent on the registration setting being updated.'''
        result = self._values.get("dependent")
        assert result is not None, "Required property 'dependent' is missing"
        return typing.cast(_constructs_77d1e7e8.Construct, result)

    @builtins.property
    def registration_status(self) -> SecretsManagementRegistrationStatus:
        '''The Deadline Secrets Management registration status to be applied to the Deadline Client identities that connect from the specified VPC subnets.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#registration-status
        '''
        result = self._values.get("registration_status")
        assert result is not None, "Required property 'registration_status' is missing"
        return typing.cast(SecretsManagementRegistrationStatus, result)

    @builtins.property
    def role(self) -> SecretsManagementRole:
        '''The role to be assigned to the Deadline Client identities that connect from the specified VPC subnets.

        See https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/secrets-management/deadline-secrets-management.html#assigned-roles
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(SecretsManagementRole, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC of the Deadline Client host instances to be registered.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''The VPC subnets of the Deadline Client host instances to be registered.'''
        result = self._values.get("vpc_subnets")
        assert result is not None, "Required property 'vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetIdentityRegistrationSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ThinkboxDockerImages(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.ThinkboxDockerImages",
):
    '''An API for interacting with publicly available Deadline container images published by AWS Thinkbox.

    This provides container images as required by RFDK's Deadline constructs such as

    - {@link @aws-rfdk/deadline#RenderQueue}
    - {@link @aws-rfdk/deadline#UsageBasedLicensing}

    Successful usage of the published Deadline container images with this class requires:

    1. Explicit acceptance of the terms of the AWS Thinkbox End User License Agreement, under which Deadline is
       distributed; and
    2. The lambda on which the custom resource looks up the Thinkbox container images is able to make HTTPS
       requests to the official AWS Thinbox download site: https://downloads.thinkboxsoftware.com



    Resources Deployed

    - A Lambda function containing a script to look up the AWS Thinkbox container image registry



    Security Considerations

    - CDK deploys the code for this lambda as an S3 object in the CDK bootstrap bucket. You must limit write access to
      your CDK bootstrap bucket to prevent an attacker from modifying the actions performed by these scripts. We strongly
      recommend that you either enable Amazon S3 server access logging on your CDK bootstrap bucket, or enable AWS
      CloudTrail on your account to assist in post-incident analysis of compromised production environments.

    For example, to construct a RenderQueue using the images::

       import { App, Stack, Vpc } from '@aws-rfdk/core';
       import { AwsCustomerAgreementAndIpLicenseAcceptance, RenderQueue, Repository, ThinkboxDockerImages, VersionQuery } from '@aws-rfdk/deadline';
       const app = new App();
       const stack = new Stack(app, 'Stack');
       const vpc = new Vpc(stack, 'Vpc');
       const version = new VersionQuery(stack, 'Version', {
         version: '10.1.12',
       });
       const images = new ThinkboxDockerImages(stack, 'Image', {
         version,
         // Change this to AwsCustomerAgreementAndIpLicenseAcceptance.USER_ACCEPTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE to accept the terms
         // of the AWS Customer Agreement and AWS Intellectual Property License.
         userAwsCustomerAgreementAndIpLicenseAcceptance: AwsCustomerAgreementAndIpLicenseAcceptance.USER_REJECTS_AWS_CUSTOMER_AGREEMENT_AND_IP_LICENSE,
       });
       const repository = new Repository(stack, 'Repository', {
         vpc,
         version,
       });

       const renderQueue = new RenderQueue(stack, 'RenderQueue', {
         images: images.forRenderQueue(),
         // ...
       });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user_aws_customer_agreement_and_ip_license_acceptance: AwsCustomerAgreementAndIpLicenseAcceptance,
        version: typing.Optional[IVersion] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user_aws_customer_agreement_and_ip_license_acceptance: The ThinkboxDockerImages will install Deadline onto one or more EC2 instances. By downloading or using the Deadline software, you agree to the AWS Customer Agreement (https://aws.amazon.com/agreement/) and AWS Intellectual Property License (https://aws.amazon.com/legal/aws-ip-license-terms/). You acknowledge that Deadline is AWS Content as defined in those Agreements. Use this property to indicate whether you accept or reject these terms.
        :param version: The Deadline version to obtain images for. Default: latest
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d83f51eb06568090b405784d1244c35832077ff71a3ed9931011568357cf155)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ThinkboxDockerImagesProps(
            user_aws_customer_agreement_and_ip_license_acceptance=user_aws_customer_agreement_and_ip_license_acceptance,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="forRenderQueue")
    def for_render_queue(self) -> RenderQueueImages:
        '''Returns container images for use with the {@link RenderQueue } construct.'''
        return typing.cast(RenderQueueImages, jsii.invoke(self, "forRenderQueue", []))

    @jsii.member(jsii_name="forUsageBasedLicensing")
    def for_usage_based_licensing(self) -> "UsageBasedLicensingImages":
        '''Returns container images for use with the {@link UsageBasedLicensing } construct.'''
        return typing.cast("UsageBasedLicensingImages", jsii.invoke(self, "forUsageBasedLicensing", []))

    @builtins.property
    @jsii.member(jsii_name="licenseForwarder")
    def license_forwarder(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''A {@link DockerImageAsset } that can be used to build Thinkbox's Deadline License Forwarder Docker Recipe into a container image that can be deployed in CDK.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "licenseForwarder"))

    @builtins.property
    @jsii.member(jsii_name="remoteConnectionServer")
    def remote_connection_server(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''A {@link DockerImageAsset } that can be used to build Thinkbox's Deadline RCS Docker Recipe into a container image that can be deployed in CDK.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "remoteConnectionServer"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ThinkboxDockerImagesProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_aws_customer_agreement_and_ip_license_acceptance": "userAwsCustomerAgreementAndIpLicenseAcceptance",
        "version": "version",
    },
)
class ThinkboxDockerImagesProps:
    def __init__(
        self,
        *,
        user_aws_customer_agreement_and_ip_license_acceptance: AwsCustomerAgreementAndIpLicenseAcceptance,
        version: typing.Optional[IVersion] = None,
    ) -> None:
        '''Interface to specify the properties when instantiating a {@link ThinkboxDockerImages} instnace.

        :param user_aws_customer_agreement_and_ip_license_acceptance: The ThinkboxDockerImages will install Deadline onto one or more EC2 instances. By downloading or using the Deadline software, you agree to the AWS Customer Agreement (https://aws.amazon.com/agreement/) and AWS Intellectual Property License (https://aws.amazon.com/legal/aws-ip-license-terms/). You acknowledge that Deadline is AWS Content as defined in those Agreements. Use this property to indicate whether you accept or reject these terms.
        :param version: The Deadline version to obtain images for. Default: latest
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd873c36a3fa2b0ad39de5449ad3c3a6d30b99c3d098b25cc83e8e41b67e377f)
            check_type(argname="argument user_aws_customer_agreement_and_ip_license_acceptance", value=user_aws_customer_agreement_and_ip_license_acceptance, expected_type=type_hints["user_aws_customer_agreement_and_ip_license_acceptance"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_aws_customer_agreement_and_ip_license_acceptance": user_aws_customer_agreement_and_ip_license_acceptance,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def user_aws_customer_agreement_and_ip_license_acceptance(
        self,
    ) -> AwsCustomerAgreementAndIpLicenseAcceptance:
        '''The ThinkboxDockerImages will install Deadline onto one or more EC2 instances.

        By downloading or using the Deadline software, you agree to the AWS Customer Agreement (https://aws.amazon.com/agreement/)
        and AWS Intellectual Property License (https://aws.amazon.com/legal/aws-ip-license-terms/). You acknowledge that Deadline
        is AWS Content as defined in those Agreements.

        Use this property to indicate whether you accept or reject these terms.
        '''
        result = self._values.get("user_aws_customer_agreement_and_ip_license_acceptance")
        assert result is not None, "Required property 'user_aws_customer_agreement_and_ip_license_acceptance' is missing"
        return typing.cast(AwsCustomerAgreementAndIpLicenseAcceptance, result)

    @builtins.property
    def version(self) -> typing.Optional[IVersion]:
        '''The Deadline version to obtain images for.

        :default: latest
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[IVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThinkboxDockerImagesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ThinkboxDockerRecipes(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.ThinkboxDockerRecipes",
):
    '''An API for interacting with staged Deadline Docker recipes provided by AWS Thinkbox.

    This provides container images as required by RFDK's Deadline constructs such as

    - {@link @aws-rfdk/deadline#RenderQueue}
    - {@link @aws-rfdk/deadline#UsageBasedLicensing}

    Example::

        Construct a RenderQueue
        
        import { App, Stack, Vpc } from '@aws-rfdk/core';
        import { RenderQueue, Repository, ThinkboxDockerRecipes } from '@aws-rfdk/deadline';
        const app = new App();
        const stack = new Stack(app, 'Stack');
        const vpc = new Vpc(app, stack);
        const recipes = new ThinkboxDockerRecipes(stack, 'Recipes', {
        path: '/path/to/staged/recipes'
        });
        const repository = new Repository(stack, 'Repository', {
        vpc,
        version: recipes.version
        });
        
        const renderQueue = new RenderQueue(stack, 'RenderQueue', {
        images: recipes.renderQueueImages,
        // ...
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stage: Stage,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stage: The place where Deadline is staged.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14c72197439cb1d6842806386c7ec6247a2d2b7611389ecdb0d6771a02e4292)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ThinkboxDockerRecipesProps(stage=stage)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="licenseForwarder")
    def license_forwarder(self) -> _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset:
        '''A {@link DockerImageAsset} that can be used to build Thinkbox's Deadline License Forwarder Docker Recipe into a container image that can be deployed in CDK.'''
        return typing.cast(_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset, jsii.get(self, "licenseForwarder"))

    @builtins.property
    @jsii.member(jsii_name="remoteConnectionServer")
    def remote_connection_server(
        self,
    ) -> _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset:
        '''A {@link DockerImageAsset} that can be used to build Thinkbox's Deadline RCS Docker Recipe into a container image that can be deployed in CDK.'''
        return typing.cast(_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset, jsii.get(self, "remoteConnectionServer"))

    @builtins.property
    @jsii.member(jsii_name="renderQueueImages")
    def render_queue_images(self) -> RenderQueueImages:
        '''Docker images staged locally for use with the {@link RenderQueue } construct.'''
        return typing.cast(RenderQueueImages, jsii.get(self, "renderQueueImages"))

    @builtins.property
    @jsii.member(jsii_name="ublImages")
    def ubl_images(self) -> "UsageBasedLicensingImages":
        '''Docker images staged locally for use with the {@link UsageBasedLicensing } construct.'''
        return typing.cast("UsageBasedLicensingImages", jsii.get(self, "ublImages"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> IVersion:
        return typing.cast(IVersion, jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ThinkboxDockerRecipesProps",
    jsii_struct_bases=[],
    name_mapping={"stage": "stage"},
)
class ThinkboxDockerRecipesProps:
    def __init__(self, *, stage: Stage) -> None:
        '''Interface to specify the properties when instantiating a {@link ThinkboxDockerRecipes} instnace.

        :param stage: The place where Deadline is staged.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13eabe941ad0e16c49b0ff3a25fdc08912e4df439ce912fdf87f8a9e5196abc0)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
        }

    @builtins.property
    def stage(self) -> Stage:
        '''The place where Deadline is staged.'''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(Stage, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThinkboxDockerRecipesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.deadline.ThinkboxManagedDeadlineDockerRecipes")
class ThinkboxManagedDeadlineDockerRecipes(enum.Enum):
    '''An enum that is associated with AWS Thinkbox managed recipes that are available in the stage manifest.'''

    REMOTE_CONNECTION_SERVER = "REMOTE_CONNECTION_SERVER"
    '''The Docker Image Asset for the Remote Connection Server.'''
    LICENSE_FORWARDER = "LICENSE_FORWARDER"
    '''The Docker Image Asset for the License Forwarder.'''


class UsageBasedLicense(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.UsageBasedLicense",
):
    '''Instances of this class represent a usage-based license for a particular product.

    It encapsulates all of the information specific to a product that the UsageBasedLicensing
    construct requires to interoperate with that product.
    '''

    def __init__(
        self,
        *,
        license_name: builtins.str,
        ports: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Port],
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param license_name: The name of the product that the usage-based license applies to.
        :param ports: The set of ports that are used for licensing traffic.
        :param limit: The maximum number of usage-based licenses that can be used concurrently.
        '''
        props = UsageBasedLicenseProps(
            license_name=license_name, ports=ports, limit=limit
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="for3dsMax")
    @builtins.classmethod
    def for3ds_max(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for 3dsMax license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58183295cc6f79925d3dc41f7b26411cabe1f14c87d7fe7c592baa76109d80e6)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "for3dsMax", [limit]))

    @jsii.member(jsii_name="forArnold")
    @builtins.classmethod
    def for_arnold(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Arnold license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89467b35ad130fe47737c62ffa68da05ba60ba56157627e4a479ed36ec8de3f9)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forArnold", [limit]))

    @jsii.member(jsii_name="forCinema4D")
    @builtins.classmethod
    def for_cinema4_d(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Cinema 4D license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b503dfee4e4200e93a4f552a31d11daaa9637aef07b1350108003daea6d6be7)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forCinema4D", [limit]))

    @jsii.member(jsii_name="forClarisse")
    @builtins.classmethod
    def for_clarisse(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Clarisse license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32b62b0ddc0e8daa25daabe4d0581dad64d6770516439a1b1324fcd56d48891)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forClarisse", [limit]))

    @jsii.member(jsii_name="forHoudini")
    @builtins.classmethod
    def for_houdini(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Houdini license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9dda7af2655f33d01f8ac5c9b2e1f4506ed0c917122744396393b949c8f65e)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forHoudini", [limit]))

    @jsii.member(jsii_name="forKatana")
    @builtins.classmethod
    def for_katana(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Katana license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ebc0981ea5e424337802b51b392e49c264441446258f829b0b4846c8f41ff2)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forKatana", [limit]))

    @jsii.member(jsii_name="forKeyShot")
    @builtins.classmethod
    def for_key_shot(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for KeyShot license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7873f7f682d37cb56f271c2ac958b4f1832dfd2745e5acc893a68a55c54889a)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forKeyShot", [limit]))

    @jsii.member(jsii_name="forKrakatoa")
    @builtins.classmethod
    def for_krakatoa(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for krakatoa license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dac2ac3d07447a7a21d7e77c8623f2a3c240697e6c7419c98027b449f60f87a)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forKrakatoa", [limit]))

    @jsii.member(jsii_name="forMantra")
    @builtins.classmethod
    def for_mantra(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Mantra license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815157dee6fef8a445edcc5493fabf2642a6a8a9e9b5b92bd01ab96855a5c71d)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forMantra", [limit]))

    @jsii.member(jsii_name="forMaxwell")
    @builtins.classmethod
    def for_maxwell(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for maxwell license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c7fde5eb0d2de564b89e5d97756958028bcc314780d76bd6f1c5682a3691f5)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forMaxwell", [limit]))

    @jsii.member(jsii_name="forMaya")
    @builtins.classmethod
    def for_maya(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Maya license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cc804944d36c92ece672e1c7c4f5c2efe0580df75158bc15878d368b1dbbac)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forMaya", [limit]))

    @jsii.member(jsii_name="forNuke")
    @builtins.classmethod
    def for_nuke(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Nuke license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed10df99b2bd05e529b930f93cdc405a7b57f6dfad021de7197a11fb82bc08db)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forNuke", [limit]))

    @jsii.member(jsii_name="forRealFlow")
    @builtins.classmethod
    def for_real_flow(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for RealFlow license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec5f059cbac14dc2950f89d9ed4da7f70a4cf77283c3a276a0f8f9e424fb68c)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forRealFlow", [limit]))

    @jsii.member(jsii_name="forRedShift")
    @builtins.classmethod
    def for_red_shift(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for RedShift license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c9c374b1e9323c755eefecb74d10f33ebfefb3fd091a035cda8c982d5b0ca0)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forRedShift", [limit]))

    @jsii.member(jsii_name="forVray")
    @builtins.classmethod
    def for_vray(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for V-Ray license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0312086803246326dc699e2065d716ed450b4eb35b4b213ca75cf82612701056)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forVray", [limit]))

    @jsii.member(jsii_name="forYeti")
    @builtins.classmethod
    def for_yeti(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        '''Method for Yeti license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc31a7108e3ffa9d50bb593c199be8651ca16b40f433a5a56815706ee2eb7974)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        return typing.cast("UsageBasedLicense", jsii.sinvoke(cls, "forYeti", [limit]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UNLIMITED")
    def UNLIMITED(cls) -> jsii.Number:
        '''Constant used to signify unlimited overage.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "UNLIMITED"))

    @builtins.property
    @jsii.member(jsii_name="licenseName")
    def license_name(self) -> builtins.str:
        '''The name of license limit.'''
        return typing.cast(builtins.str, jsii.get(self, "licenseName"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.Port]:
        '''Ports that will be used for this license.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.Port], jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Maximum count of licenses that will be used.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limit"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicenseProps",
    jsii_struct_bases=[],
    name_mapping={"license_name": "licenseName", "ports": "ports", "limit": "limit"},
)
class UsageBasedLicenseProps:
    def __init__(
        self,
        *,
        license_name: builtins.str,
        ports: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Port],
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for constructing a {@link UsageBasedLicense} instance.

        :param license_name: The name of the product that the usage-based license applies to.
        :param ports: The set of ports that are used for licensing traffic.
        :param limit: The maximum number of usage-based licenses that can be used concurrently.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34bfb0006ce6481fa4b2176b93c014843baf43e93af34b50c16d77c229f0231)
            check_type(argname="argument license_name", value=license_name, expected_type=type_hints["license_name"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "license_name": license_name,
            "ports": ports,
        }
        if limit is not None:
            self._values["limit"] = limit

    @builtins.property
    def license_name(self) -> builtins.str:
        '''The name of the product that the usage-based license applies to.'''
        result = self._values.get("license_name")
        assert result is not None, "Required property 'license_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.Port]:
        '''The set of ports that are used for licensing traffic.'''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.Port], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of usage-based licenses that can be used concurrently.'''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicenseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable)
class UsageBasedLicensing(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.UsageBasedLicensing",
):
    '''This construct is an implementation of the Deadline component that is required for Usage-based Licensing (UBL) (see: https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/licensing-usage-based.html ) in a render farm.

    Internally this is implemented as one or more instances of the Deadline License Forwarder application set up
    to communicate to the render queue and Thinkbox’s licensing system, and to allow ingress connections
    from the worker nodes so that they can acquire licenses as needed.

    The Deadline License Forwarder is set up to run within an AWS ECS task.

    Access to the running License Forwarder is gated by a security group that, by default, only allows ingress from the
    Render Queue (in order to register Workers for license forwarding).

    When a Deadline Worker requires access to licensing via ``UsageBasedLicensing.grantPortAccess(...)``, then the RFDK
    constructs will grant that worker’s security group ingress on TCP port 17004 as well as other ports as required by
    the specific licenses being used.

    Note: This construct does not currently implement the Deadline License Forwarder's Web Forwarding functionality.
    This construct is not usable in any China region.

    architecture diagram


    Resources Deployed

    - The Auto Scaling Group (ASG) added to the Amazon Elastic Container Service cluster that is hosting the Deadline
      License Forwarder for UBL. This creates one C5 Large instance by default.
    - Amazon Elastic Block Store (EBS) device(s) associated with the EC2 instance(s) in the ASG. The default volume size is 30 GiB.
    - An Amazon CloudWatch log group that contains the logs from the Deadline License Forwarder application.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The Deadline License Forwarder is designed to be secured by restricting network access to it. For security, only the Deadline
      Workers that require access to Usage-based Licenses should be granted network access to the instances deployed by this construct.
      Futhermore, you should restrict that access to only the product(s) that those workers require when deploying this construct.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        images: typing.Union["UsageBasedLicensingImages", typing.Dict[builtins.str, typing.Any]],
        licenses: typing.Sequence[UsageBasedLicense],
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        desired_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate_secret: A secret with with 3rd Party Licensing Certificates. If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace and download file with certificates. File with certificates should be put in in a secret.
        :param images: Docker Image for License Forwarder.
        :param licenses: License limits that will be set in repository configuration.
        :param render_queue: The Deadline Render Queue, to which the License Forwarder needs to be connected.
        :param vpc: VPC to launch the License Forwarder In.
        :param desired_count: The desired number of Deadline License Forwarders that this construct keeps running. Default: 1
        :param instance_type: Type of instance that will be added to an AutoScalingGroup. Default: - Will be used C5 Large instance
        :param log_group_props: Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param security_group: The security group to use for the License Forwarder. Default: - A new security group will be created
        :param vpc_subnets: Subnets within the VPC in which to host the UBLLicesing servers. Default: All private subnets in the VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9a5c3031f59ef678ed72fb1d893f955c8a3d1ad665dfce5ea9f4e6cfc0aec1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UsageBasedLicensingProps(
            certificate_secret=certificate_secret,
            images=images,
            licenses=licenses,
            render_queue=render_queue,
            vpc=vpc,
            desired_count=desired_count,
            instance_type=instance_type,
            log_group_props=log_group_props,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantPortAccess")
    def grant_port_access(
        self,
        worker_fleet: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
        licenses: typing.Sequence[UsageBasedLicense],
    ) -> None:
        '''This method grant access of worker fleet to ports that required.

        :param worker_fleet: - worker fleet.
        :param licenses: - UBL licenses.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e12212787e2563f77d9f9691a17260dc477544948daa7fcc6f9c016416286c)
            check_type(argname="argument worker_fleet", value=worker_fleet, expected_type=type_hints["worker_fleet"])
            check_type(argname="argument licenses", value=licenses, expected_type=type_hints["licenses"])
        return typing.cast(None, jsii.invoke(self, "grantPortAccess", [worker_fleet, licenses]))

    @builtins.property
    @jsii.member(jsii_name="asg")
    def asg(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        '''Autoscaling group for license forwarder instances.'''
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "asg"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.Cluster:
        '''The Amazon ECS cluster that is hosting the Deadline License Forwarder for UBL.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The connections object that allows you to control network egress/ingress to the License Forwarder.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_ceddda9d.Ec2Service:
        '''The ECS service that serves usage based licensing.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.Ec2Service, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicensingImages",
    jsii_struct_bases=[],
    name_mapping={"license_forwarder": "licenseForwarder"},
)
class UsageBasedLicensingImages:
    def __init__(
        self,
        *,
        license_forwarder: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    ) -> None:
        '''Set of container images used to serve the {@link UsageBasedLicensing} construct.

        :param license_forwarder: The container image for the Deadline License Forwarder.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868952e5dbbed51ce3349c95eb4a4e04cb73df666a8568b2d73b3a88d447d7b1)
            check_type(argname="argument license_forwarder", value=license_forwarder, expected_type=type_hints["license_forwarder"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "license_forwarder": license_forwarder,
        }

    @builtins.property
    def license_forwarder(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''The container image for the Deadline License Forwarder.'''
        result = self._values.get("license_forwarder")
        assert result is not None, "Required property 'license_forwarder' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicensingImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicensingProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_secret": "certificateSecret",
        "images": "images",
        "licenses": "licenses",
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "desired_count": "desiredCount",
        "instance_type": "instanceType",
        "log_group_props": "logGroupProps",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class UsageBasedLicensingProps:
    def __init__(
        self,
        *,
        certificate_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        images: typing.Union[UsageBasedLicensingImages, typing.Dict[builtins.str, typing.Any]],
        licenses: typing.Sequence[UsageBasedLicense],
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        desired_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the UsageBasedLicensing construct.

        :param certificate_secret: A secret with with 3rd Party Licensing Certificates. If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace and download file with certificates. File with certificates should be put in in a secret.
        :param images: Docker Image for License Forwarder.
        :param licenses: License limits that will be set in repository configuration.
        :param render_queue: The Deadline Render Queue, to which the License Forwarder needs to be connected.
        :param vpc: VPC to launch the License Forwarder In.
        :param desired_count: The desired number of Deadline License Forwarders that this construct keeps running. Default: 1
        :param instance_type: Type of instance that will be added to an AutoScalingGroup. Default: - Will be used C5 Large instance
        :param log_group_props: Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param security_group: The security group to use for the License Forwarder. Default: - A new security group will be created
        :param vpc_subnets: Subnets within the VPC in which to host the UBLLicesing servers. Default: All private subnets in the VPC.
        '''
        if isinstance(images, dict):
            images = UsageBasedLicensingImages(**images)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c34019ac5eac7dac1440f6c0f3e5462784549281ed3a41ae8df530e412a19b0)
            check_type(argname="argument certificate_secret", value=certificate_secret, expected_type=type_hints["certificate_secret"])
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument licenses", value=licenses, expected_type=type_hints["licenses"])
            check_type(argname="argument render_queue", value=render_queue, expected_type=type_hints["render_queue"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_secret": certificate_secret,
            "images": images,
            "licenses": licenses,
            "render_queue": render_queue,
            "vpc": vpc,
        }
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def certificate_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''A secret with with 3rd Party Licensing Certificates.

        If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace
        and download file with certificates.
        File with certificates should be put in in a secret.
        '''
        result = self._values.get("certificate_secret")
        assert result is not None, "Required property 'certificate_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def images(self) -> UsageBasedLicensingImages:
        '''Docker Image for License Forwarder.'''
        result = self._values.get("images")
        assert result is not None, "Required property 'images' is missing"
        return typing.cast(UsageBasedLicensingImages, result)

    @builtins.property
    def licenses(self) -> typing.List[UsageBasedLicense]:
        '''License limits that will be set in repository configuration.'''
        result = self._values.get("licenses")
        assert result is not None, "Required property 'licenses' is missing"
        return typing.cast(typing.List[UsageBasedLicense], result)

    @builtins.property
    def render_queue(self) -> IRenderQueue:
        '''The Deadline Render Queue, to which the License Forwarder needs to be connected.'''
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return typing.cast(IRenderQueue, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the License Forwarder In.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of Deadline License Forwarders that this construct keeps running.

        :default: 1
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Type of instance that will be added to an AutoScalingGroup.

        :default: - Will be used C5 Large instance
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch.

        :default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security group to use for the License Forwarder.

        :default: - A new security group will be created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Subnets within the VPC in which to host the UBLLicesing servers.

        :default: All private subnets in the VPC.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicensingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVersion)
class VersionQuery(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.VersionQuery",
):
    '''This class encapsulates information about a particular version of Thinkbox's Deadline software.

    Information such as the version number, and where to get installers for that version from Amazon S3.

    The version of an official release of Deadline is always four numeric version components separated by dots.
    ex: 10.1.8.5. We refer to the components in this version, in order from left-to-right, as the
    major, minor, release, and patch versions. For example, Deadline version 10.1.8.5 is majorVersion 10, minorVersion 1,
    releaseVersion 8, and patchVersion 5.

    All of the installers provided by an instance of this class must be for the same Deadline release (ex: 10.1.8),
    but the patch versions may differ between operating systems depending on the particulars of that release of Deadline.
    This class provides a simple way to query a version of Deadline prior to or during deployment of a
    CDK app.

    You pass an instance of this class to various Deadline constructs in this library to tell those
    constructs which version of Deadline you want them to use, and be configured for.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: String containing the complete or partial deadline version. Default: - the latest available version of deadline installer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c4080322c875167088ee1aa79460b7ba6a0e4a0e0cf7f6e23a6b29f601a28b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VersionQueryProps(version=version)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isLessThan")
    def is_less_than(self, other: "Version") -> builtins.bool:
        '''Returns whether this version is less than another version.

        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fa58f11ab292ca5222e5962e63b1b5b1794efa4d2208e1b842b85bb7ca996c)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isLessThan", [other]))

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        '''Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "linuxFullVersionString", []))

    @builtins.property
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> PlatformInstallers:
        '''The Linux installers for this version.

        :inheritdoc: true
        '''
        return typing.cast(PlatformInstallers, jsii.get(self, "linuxInstallers"))

    @builtins.property
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        '''The major version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "majorVersion"))

    @builtins.property
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        '''The minor version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "minorVersion"))

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        '''The release version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "releaseVersion"))

    @builtins.property
    @jsii.member(jsii_name="versionString")
    def version_string(self) -> builtins.str:
        '''A string representation of the version using the best available information at synthesis-time.

        This value is not guaranteed to be resolved, and is intended for output to CDK users.
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionString"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Optional[builtins.str]:
        '''The expression used as input to the ``VersionQuery``.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expression"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.VersionQueryProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class VersionQueryProps:
    def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
        '''Properties for the Deadline Version.

        :param version: String containing the complete or partial deadline version. Default: - the latest available version of deadline installer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fa144528ec71005da23187396ec6abbc1bb7b1826348d29daed814e87da8d1)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''String containing the complete or partial deadline version.

        :default: - the latest available version of deadline installer.
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VersionQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkerInstanceConfiguration(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.WorkerInstanceConfiguration",
):
    '''This construct can be used to configure Deadline Workers on an instance to connect to a RenderQueue, stream their log files to CloudWatch, and configure various settings of the Deadline Worker.

    The configuration happens on instance start-up using user data scripting.

    This configuration performs the following steps in order:

    1. Configure Cloud Watch Agent
    2. Configure Deadline Worker RenderQueue connection
    3. Configure Deadline Worker settings

    A ``userDataProvider`` can be specified that defines callback functions.
    These callbacks can be used to inject user data commands at different points during the Worker instance configuration.


    Security Considerations

    - The instances configured by this construct will download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        worker: IHost,
        cloud_watch_log_settings: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        render_queue: typing.Optional[IRenderQueue] = None,
        should_install_cloud_watch_agent: typing.Optional[builtins.bool] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        worker_settings: typing.Optional[typing.Union["WorkerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param worker: The Deadline Worker that should be configured.
        :param cloud_watch_log_settings: The configuration for streaming the Deadline Worker logs to AWS CloudWatch. Default: The Worker logs will not be streamed to CloudWatch.
        :param render_queue: The RenderQueue that the worker should be configured to connect to. Default: The Worker is not configured to connect to a RenderQueue
        :param should_install_cloud_watch_agent: Whether or not the CloudWatch agent should be automatically installed onto all worker instances. This installation will be a best effort, but will not fail the deployment if it isn't completed successfully. Ideally the CloudWatch agent should be installed on the AMI to avoid issues. If the installation fails, logs will not be streamed off of the workers into CloudWatch. Default: true
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param worker_settings: The settings to apply to the Deadline Worker. Default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c737ab6625475ccd2bd3354f52ac7616135c85411c2d2591c067712b243dca9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkerInstanceConfigurationProps(
            worker=worker,
            cloud_watch_log_settings=cloud_watch_log_settings,
            render_queue=render_queue,
            should_install_cloud_watch_agent=should_install_cloud_watch_agent,
            user_data_provider=user_data_provider,
            worker_settings=worker_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="configureCloudWatchLogStream")
    def _configure_cloud_watch_log_stream(
        self,
        worker: IHost,
        id: builtins.str,
        log_group_props: typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]],
        should_install_agent: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''This method can be used to configure a Deadline Worker instance to stream its logs to the AWS CloudWatch service.

        The logs that this configures to stream are:

        - EC2 Instance UserData execution; this is the startup scripting that is run when the instance launches
          for the first time.
        - Deadline Worker logs.
        - Deadline Launcher logs.

        :param worker: The worker to configure. This can be an instance, auto scaling group, launch template, etc.
        :param id: Identifier to disambiguate the resources that are created.
        :param log_group_props: Configuration for the log group in CloudWatch.
        :param should_install_agent: Boolean for if the worker's User Data should attempt to install the CloudWatch agent.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e55982980bceacf37b29f080441101853976cab8aed15125d6422a765c9f793)
            check_type(argname="argument worker", value=worker, expected_type=type_hints["worker"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument should_install_agent", value=should_install_agent, expected_type=type_hints["should_install_agent"])
        return typing.cast(None, jsii.invoke(self, "configureCloudWatchLogStream", [worker, id, log_group_props, should_install_agent]))

    @jsii.member(jsii_name="configureWorkerSettings")
    def _configure_worker_settings(
        self,
        worker: IHost,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''This method can be used to set up the Deadline Worker application on an EC2 instance.

        From a practical
        perspective, this is executing the script found in aws-rfdk/lib/deadline/scripts/[bash,powershell]/configureWorker.[sh,ps1]
        to configure the Deadline Worker application.

        :param worker: The worker to configure. This can be an instance, auto scaling group, launch template, etc.
        :param id: Identifier to disambiguate the resources that are created.
        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param listener_port: The port to configure the worker to listen on for remote commands such as requests for its log stream. If more than one worker is present on a single host, connsecutive ports will be opened, starting with the supplied port, up to the maximum number of workers defined by the WorkerInstanceFleet. Default: 56032
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8af4774cb01dd769b9d9b4c15632e229d703b889ca562a0c6dd0ad3a6e39a2)
            check_type(argname="argument worker", value=worker, expected_type=type_hints["worker"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        settings = WorkerSettings(
            groups=groups, listener_port=listener_port, pools=pools, region=region
        )

        return typing.cast(None, jsii.invoke(self, "configureWorkerSettings", [worker, id, settings]))

    @builtins.property
    @jsii.member(jsii_name="listenerPort")
    def listener_port(self) -> jsii.Number:
        '''
        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "listenerPort"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerInstanceConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "worker": "worker",
        "cloud_watch_log_settings": "cloudWatchLogSettings",
        "render_queue": "renderQueue",
        "should_install_cloud_watch_agent": "shouldInstallCloudWatchAgent",
        "user_data_provider": "userDataProvider",
        "worker_settings": "workerSettings",
    },
)
class WorkerInstanceConfigurationProps:
    def __init__(
        self,
        *,
        worker: IHost,
        cloud_watch_log_settings: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        render_queue: typing.Optional[IRenderQueue] = None,
        should_install_cloud_watch_agent: typing.Optional[builtins.bool] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        worker_settings: typing.Optional[typing.Union["WorkerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for a WorkerInstanceConfiguration.

        :param worker: The Deadline Worker that should be configured.
        :param cloud_watch_log_settings: The configuration for streaming the Deadline Worker logs to AWS CloudWatch. Default: The Worker logs will not be streamed to CloudWatch.
        :param render_queue: The RenderQueue that the worker should be configured to connect to. Default: The Worker is not configured to connect to a RenderQueue
        :param should_install_cloud_watch_agent: Whether or not the CloudWatch agent should be automatically installed onto all worker instances. This installation will be a best effort, but will not fail the deployment if it isn't completed successfully. Ideally the CloudWatch agent should be installed on the AMI to avoid issues. If the installation fails, logs will not be streamed off of the workers into CloudWatch. Default: true
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param worker_settings: The settings to apply to the Deadline Worker. Default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        '''
        if isinstance(cloud_watch_log_settings, dict):
            cloud_watch_log_settings = _LogGroupFactoryProps_b817ed21(**cloud_watch_log_settings)
        if isinstance(worker_settings, dict):
            worker_settings = WorkerSettings(**worker_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d9bce71a7fd19c065dfded85a010d34d94cdf22af8016e52f9034175b858f6)
            check_type(argname="argument worker", value=worker, expected_type=type_hints["worker"])
            check_type(argname="argument cloud_watch_log_settings", value=cloud_watch_log_settings, expected_type=type_hints["cloud_watch_log_settings"])
            check_type(argname="argument render_queue", value=render_queue, expected_type=type_hints["render_queue"])
            check_type(argname="argument should_install_cloud_watch_agent", value=should_install_cloud_watch_agent, expected_type=type_hints["should_install_cloud_watch_agent"])
            check_type(argname="argument user_data_provider", value=user_data_provider, expected_type=type_hints["user_data_provider"])
            check_type(argname="argument worker_settings", value=worker_settings, expected_type=type_hints["worker_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "worker": worker,
        }
        if cloud_watch_log_settings is not None:
            self._values["cloud_watch_log_settings"] = cloud_watch_log_settings
        if render_queue is not None:
            self._values["render_queue"] = render_queue
        if should_install_cloud_watch_agent is not None:
            self._values["should_install_cloud_watch_agent"] = should_install_cloud_watch_agent
        if user_data_provider is not None:
            self._values["user_data_provider"] = user_data_provider
        if worker_settings is not None:
            self._values["worker_settings"] = worker_settings

    @builtins.property
    def worker(self) -> IHost:
        '''The Deadline Worker that should be configured.'''
        result = self._values.get("worker")
        assert result is not None, "Required property 'worker' is missing"
        return typing.cast(IHost, result)

    @builtins.property
    def cloud_watch_log_settings(
        self,
    ) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''The configuration for streaming the Deadline Worker logs to AWS CloudWatch.

        :default: The Worker logs will not be streamed to CloudWatch.
        '''
        result = self._values.get("cloud_watch_log_settings")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def render_queue(self) -> typing.Optional[IRenderQueue]:
        '''The RenderQueue that the worker should be configured to connect to.

        :default: The Worker is not configured to connect to a RenderQueue
        '''
        result = self._values.get("render_queue")
        return typing.cast(typing.Optional[IRenderQueue], result)

    @builtins.property
    def should_install_cloud_watch_agent(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the CloudWatch agent should be automatically installed onto all worker instances.

        This installation will be a best effort, but will not fail the deployment if it isn't completed
        successfully. Ideally the CloudWatch agent should be installed on the AMI to avoid issues. If
        the installation fails, logs will not be streamed off of the workers into CloudWatch.

        :default: true
        '''
        result = self._values.get("should_install_cloud_watch_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_data_provider(self) -> typing.Optional[IInstanceUserDataProvider]:
        '''An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle.

        You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        '''
        result = self._values.get("user_data_provider")
        return typing.cast(typing.Optional[IInstanceUserDataProvider], result)

    @builtins.property
    def worker_settings(self) -> typing.Optional["WorkerSettings"]:
        '''The settings to apply to the Deadline Worker.

        :default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        '''
        result = self._values.get("worker_settings")
        return typing.cast(typing.Optional["WorkerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerInstanceConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWorkerFleet, _IMonitorableFleet_71f4eb88)
class WorkerInstanceFleet(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.WorkerInstanceFleet",
):
    '''This construct reperesents a fleet of Deadline Workers.

    The construct consists of an Auto Scaling Group (ASG) of instances using a provided AMI which has Deadline and any number
    of render applications installed.  Whenever an instance in the ASG start it will connect Deadline to the desired render queue.

    When the worker fleet is deployed if it has been provided a HealthMonitor the Worker fleet will register itself against the Monitor
    to ensure that the fleet remains healthy.

    architecture diagram


    Resources Deployed

    - An EC2 Auto Scaling Group to maintain the number of instances.
    - An Instance Role and corresponding IAM Policy.
    - An Amazon CloudWatch log group that contains the Deadline Worker, Deadline Launcher, and instance-startup logs for the instances
      in the fleet.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The data that is stored on your Worker's local EBS volume can include temporary working files from the applications
      that are rendering your jobs and tasks. That data can be sensitive or privileged, so we recommend that you encrypt
      the data volumes of these instances using either the provided option or by using an encrypted AMI as your source.
    - The software on the AMI that is being used by this construct may pose a security risk. We recommend that you adopt a
      patching strategy to keep this software current with the latest security patches. Please see
      https://docs.aws.amazon.com/rfdk/latest/guide/patching-software.html for more information.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        health_check_config: typing.Optional[typing.Union[_HealthCheckConfig_ebe26fb6, typing.Dict[builtins.str, typing.Any]]] = None,
        health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        spot_price: typing.Optional[jsii.Number] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param render_queue: Endpoint for the RenderQueue, to which the worker fleet needs to be connected.
        :param vpc: VPC to launch the worker fleet in.
        :param worker_machine_image: AMI of the deadline worker to launch.
        :param block_devices: 
        :param desired_capacity: Initial amount of workers in the fleet. If this is set to a number, every deployment will reset the amount of workers to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check_config: Properties for configuring a health check. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: properties of HealthCheckConfig applies
        :param health_monitor: Health Monitor component to monitor the health of instances. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: - Health Monitoring is turned-off
        :param instance_type: Type of instance to launch for the Workers. Default: - a T3-Large type will be used.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity, or minCapacity if desiredCapacity is not set
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param role: An IAM role to associate with the instance profile assigned to its resources. The role must be assumable by the service principal ``ec2.amazonaws.com``: const role = new iam.Role(this, 'MyRole', { assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com') }); Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this fleet. Default: - create new security group
        :param spot_price: The maximum hourly price($) to be paid for each Spot instance. min - 0.001; max - 255 Default: - launches on-demand EC2 instances.
        :param user_data: The specific UserData to use. The UserData will be mutated by this construct and may be mutated afterwards as well. Default: A UserData object appropriate for the MachineImage's Operating System is created.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param listener_port: The port to configure the worker to listen on for remote commands such as requests for its log stream. If more than one worker is present on a single host, connsecutive ports will be opened, starting with the supplied port, up to the maximum number of workers defined by the WorkerInstanceFleet. Default: 56032
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e672c5ae8a9c0f5ede477720680e29af86abd75d99d3b694314d9569c26c67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkerInstanceFleetProps(
            render_queue=render_queue,
            vpc=vpc,
            worker_machine_image=worker_machine_image,
            block_devices=block_devices,
            desired_capacity=desired_capacity,
            health_check_config=health_check_config,
            health_monitor=health_monitor,
            instance_type=instance_type,
            key_name=key_name,
            log_group_props=log_group_props,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            role=role,
            security_group=security_group,
            spot_price=spot_price,
            user_data=user_data,
            user_data_provider=user_data_provider,
            vpc_subnets=vpc_subnets,
            groups=groups,
            listener_port=listener_port,
            pools=pools,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    ) -> None:
        '''Add the security group to all workers.

        :param security_group: : The security group to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9679a03a73c2811a52ceed6f73d3ebe137803e90b3160ab90bea20b0c173a8d)
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [security_group]))

    @jsii.member(jsii_name="allowListenerPortFrom")
    def allow_listener_port_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that depends on this stack.

        If this stack depends on the other stack, use allowListenerPortTo().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortFrom(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortFrom(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbde8bb042ab2246e58f6c1611f74e2596034bfb27a9773b12b049ed31f2111b)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowListenerPortFrom", [other]))

    @jsii.member(jsii_name="allowListenerPortTo")
    def allow_listener_port_to(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    ) -> None:
        '''Allow access to the worker's remote command listener port (configured as a part of the WorkerConfiguration) for an IConnectable that is either in this stack, or in a stack that this stack depends on.

        If the other stack depends on this stack, use allowListenerPortFrom().

        Common uses are:

        Adding a SecurityGroup:
        ``workerFleet.allowListenerPortTo(securityGroup)``

        Adding a CIDR:
        ``workerFleet.allowListenerPortTo(Peer.ipv4('10.0.0.0/24').connections)``

        :param other: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371917bb1feabe107f46ea61078c671e18b96751ef272c92a00cb5b830d34859)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(None, jsii.invoke(self, "allowListenerPortTo", [other]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SPOT_PRICE_MAX_LIMIT")
    def SPOT_PRICE_MAX_LIMIT(cls) -> jsii.Number:
        '''The max limit for spot price.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "SPOT_PRICE_MAX_LIMIT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SPOT_PRICE_MIN_LIMIT")
    def SPOT_PRICE_MIN_LIMIT(cls) -> jsii.Number:
        '''The min limit for spot price.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "SPOT_PRICE_MIN_LIMIT"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The security groups/rules used to allow network connections to the file system.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        '''The ASG object created by the construct.'''
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="listeningPorts")
    def listening_ports(self) -> _aws_cdk_aws_ec2_ceddda9d.Port:
        '''The port workers listen on to share their logs.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Port, jsii.get(self, "listeningPorts"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> jsii.Number:
        '''This field implements the maximum instance count this fleet can have.'''
        return typing.cast(jsii.Number, jsii.get(self, "targetCapacity"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacityMetric")
    def target_capacity_metric(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.IMetric:
        '''This field implements the base capacity metric of the fleet against which, the healthy percent will be calculated.

        eg.: GroupDesiredCapacity for an ASG
        '''
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IMetric, jsii.get(self, "targetCapacityMetric"))

    @builtins.property
    @jsii.member(jsii_name="targetScope")
    def target_scope(self) -> _constructs_77d1e7e8.Construct:
        '''This field implements the scope in which to create the monitoring resource like TargetGroups, Listener etc.'''
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "targetScope"))

    @builtins.property
    @jsii.member(jsii_name="targetToMonitor")
    def target_to_monitor(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget:
        '''This field implements the component of type INetworkLoadBalancerTarget which can be attached to Network Load Balancer for monitoring.

        eg. An AutoScalingGroup
        '''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget, jsii.get(self, "targetToMonitor"))

    @builtins.property
    @jsii.member(jsii_name="targetUpdatePolicy")
    def target_update_policy(self) -> _aws_cdk_aws_iam_ceddda9d.IPolicy:
        '''This field implements a policy which can be attached to the lambda execution role so that it is capable of suspending the fleet.

        eg.: autoscaling:UpdateAutoScalingGroup permission for an ASG
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPolicy, jsii.get(self, "targetUpdatePolicy"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerSettings",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "listener_port": "listenerPort",
        "pools": "pools",
        "region": "region",
    },
)
class WorkerSettings:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration settings for Deadline Workers.

        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param listener_port: The port to configure the worker to listen on for remote commands such as requests for its log stream. If more than one worker is present on a single host, connsecutive ports will be opened, starting with the supplied port, up to the maximum number of workers defined by the WorkerInstanceFleet. Default: 56032
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75dcefb96ba46cf970ec474d4ee6223514fdd9fa26193ddac2f9159183eccf42)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument pools", value=pools, expected_type=type_hints["pools"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if pools is not None:
            self._values["pools"] = pools
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline groups these workers needs to be assigned to.

        The group is
        created if it does not already exist.

        :default: - Worker is not assigned to any group
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''The port to configure the worker to listen on for remote commands such as requests for its log stream.

        If more than one worker is present on a single
        host, connsecutive ports will be opened, starting with the supplied port,
        up to the maximum number of workers defined by the WorkerInstanceFleet.

        :default: 56032
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline pools these workers needs to be assigned to.

        The pool is created
        if it does not already exist.

        :default: - Worker is not assigned to any pool.
        '''
        result = self._values.get("pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Deadline region these workers needs to be assigned to.

        :default: - Worker is not assigned to any region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-rfdk.deadline.IPatchVersion")
class IPatchVersion(IReleaseVersion, typing_extensions.Protocol):
    '''Represents a fully-qualified release version number.

    E.g. 10.1.9.2
    '''

    @builtins.property
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        '''The patch version number.'''
        ...


class _IPatchVersionProxy(
    jsii.proxy_for(IReleaseVersion), # type: ignore[misc]
):
    '''Represents a fully-qualified release version number.

    E.g. 10.1.9.2
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IPatchVersion"

    @builtins.property
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        '''The patch version number.'''
        return typing.cast(jsii.Number, jsii.get(self, "patchVersion"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPatchVersion).__jsii_proxy_class__ = lambda : _IPatchVersionProxy


@jsii.implements(IPatchVersion)
class Version(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.deadline.Version"):
    '''This class is reposonsible to do basic operations on version format.'''

    def __init__(self, components: typing.Sequence[jsii.Number]) -> None:
        '''
        :param components: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4ff9d30fda5d1f404bf9183bea19d4d6e9621f270b43fa3759a0a260d76b6f)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
        jsii.create(self.__class__, self, [components])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, version: builtins.str) -> "Version":
        '''This method parses the input string and returns the version object.

        :param version: version string to parse.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0720999d7961642ff7016483094188bdb6e24ad94e1c705a960dba3aad135ff)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("Version", jsii.sinvoke(cls, "parse", [version]))

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, version: "Version") -> builtins.bool:
        '''This method compares two version strings.

        :param version: -

        :return:

        true if this version is equal to the provided version;
        false otherwise.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52a09c2b7c311158028b2c228d0fc5f54fdd1d3ca68a6878d4492a9538ace20)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [version]))

    @jsii.member(jsii_name="isGreaterThan")
    def is_greater_than(self, version: "Version") -> builtins.bool:
        '''This method compares two version strings.

        :param version: -

        :return:

        true if this version is greater than the provided version;
        false if this version is less than or equal to the provided verison.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fe1e9bebc794f478a42f875d0b5fcd420e549d95cf06262b7c0f0cd4c291a6)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isGreaterThan", [version]))

    @jsii.member(jsii_name="isLessThan")
    def is_less_than(self, version: "Version") -> builtins.bool:
        '''This method compares two version strings.

        :param version: -

        :return:

        true if this version is less than the provided version;
        false if this version is greater than or equal to the provided verison.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7754a3469b09ae78f83f1a7119547aca2a2b46149827ea08e536c37d8828e8b5)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isLessThan", [version]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''The method returns the version components in dot separated string format.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MINIMUM_SECRETS_MANAGEMENT_VERSION")
    def MINIMUM_SECRETS_MANAGEMENT_VERSION(cls) -> "Version":
        '''The minimum Deadline version required to enable Deadline Secrets Management.'''
        return typing.cast("Version", jsii.sget(cls, "MINIMUM_SECRETS_MANAGEMENT_VERSION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MINIMUM_SUPPORTED_DEADLINE_VERSION")
    def MINIMUM_SUPPORTED_DEADLINE_VERSION(cls) -> "Version":
        '''This variable holds the value for minimum supported deadline version.'''
        return typing.cast("Version", jsii.sget(cls, "MINIMUM_SUPPORTED_DEADLINE_VERSION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MINIMUM_VERSION_USING_NEW_INSTALLBUILDER_LOG")
    def MINIMUM_VERSION_USING_NEW_INSTALLBUILDER_LOG(cls) -> "Version":
        '''The minimum Deadline version which uses Install Builder instead of Bitrock Installer.'''
        return typing.cast("Version", jsii.sget(cls, "MINIMUM_VERSION_USING_NEW_INSTALLBUILDER_LOG"))

    @builtins.property
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        '''The major version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "majorVersion"))

    @builtins.property
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        '''The minor version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "minorVersion"))

    @builtins.property
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        '''The patch version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "patchVersion"))

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        '''The release version number.

        :inheritdoc: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "releaseVersion"))

    @builtins.property
    @jsii.member(jsii_name="versionString")
    def version_string(self) -> builtins.str:
        '''A string representation of the version using the best available information at synthesis-time.

        This value is not guaranteed to be resolved, and is intended for output to CDK users.

        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionString"))


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerInstanceFleetProps",
    jsii_struct_bases=[WorkerSettings],
    name_mapping={
        "groups": "groups",
        "listener_port": "listenerPort",
        "pools": "pools",
        "region": "region",
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "worker_machine_image": "workerMachineImage",
        "block_devices": "blockDevices",
        "desired_capacity": "desiredCapacity",
        "health_check_config": "healthCheckConfig",
        "health_monitor": "healthMonitor",
        "instance_type": "instanceType",
        "key_name": "keyName",
        "log_group_props": "logGroupProps",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "role": "role",
        "security_group": "securityGroup",
        "spot_price": "spotPrice",
        "user_data": "userData",
        "user_data_provider": "userDataProvider",
        "vpc_subnets": "vpcSubnets",
    },
)
class WorkerInstanceFleetProps(WorkerSettings):
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        render_queue: IRenderQueue,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        health_check_config: typing.Optional[typing.Union[_HealthCheckConfig_ebe26fb6, typing.Dict[builtins.str, typing.Any]]] = None,
        health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        spot_price: typing.Optional[jsii.Number] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the Deadline Worker Fleet.

        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param listener_port: The port to configure the worker to listen on for remote commands such as requests for its log stream. If more than one worker is present on a single host, connsecutive ports will be opened, starting with the supplied port, up to the maximum number of workers defined by the WorkerInstanceFleet. Default: 56032
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        :param render_queue: Endpoint for the RenderQueue, to which the worker fleet needs to be connected.
        :param vpc: VPC to launch the worker fleet in.
        :param worker_machine_image: AMI of the deadline worker to launch.
        :param block_devices: 
        :param desired_capacity: Initial amount of workers in the fleet. If this is set to a number, every deployment will reset the amount of workers to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check_config: Properties for configuring a health check. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: properties of HealthCheckConfig applies
        :param health_monitor: Health Monitor component to monitor the health of instances. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: - Health Monitoring is turned-off
        :param instance_type: Type of instance to launch for the Workers. Default: - a T3-Large type will be used.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity, or minCapacity if desiredCapacity is not set
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param role: An IAM role to associate with the instance profile assigned to its resources. The role must be assumable by the service principal ``ec2.amazonaws.com``: const role = new iam.Role(this, 'MyRole', { assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com') }); Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this fleet. Default: - create new security group
        :param spot_price: The maximum hourly price($) to be paid for each Spot instance. min - 0.001; max - 255 Default: - launches on-demand EC2 instances.
        :param user_data: The specific UserData to use. The UserData will be mutated by this construct and may be mutated afterwards as well. Default: A UserData object appropriate for the MachineImage's Operating System is created.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        '''
        if isinstance(health_check_config, dict):
            health_check_config = _HealthCheckConfig_ebe26fb6(**health_check_config)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5185fbd88e4b40cfb9f11f6a580addea8a00b9ae6033cf03226bc7ab0619356)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument pools", value=pools, expected_type=type_hints["pools"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument render_queue", value=render_queue, expected_type=type_hints["render_queue"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument worker_machine_image", value=worker_machine_image, expected_type=type_hints["worker_machine_image"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            check_type(argname="argument health_monitor", value=health_monitor, expected_type=type_hints["health_monitor"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument spot_price", value=spot_price, expected_type=type_hints["spot_price"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument user_data_provider", value=user_data_provider, expected_type=type_hints["user_data_provider"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "render_queue": render_queue,
            "vpc": vpc,
            "worker_machine_image": worker_machine_image,
        }
        if groups is not None:
            self._values["groups"] = groups
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if pools is not None:
            self._values["pools"] = pools
        if region is not None:
            self._values["region"] = region
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if health_monitor is not None:
            self._values["health_monitor"] = health_monitor
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if key_name is not None:
            self._values["key_name"] = key_name
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if user_data is not None:
            self._values["user_data"] = user_data
        if user_data_provider is not None:
            self._values["user_data_provider"] = user_data_provider
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline groups these workers needs to be assigned to.

        The group is
        created if it does not already exist.

        :default: - Worker is not assigned to any group
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''The port to configure the worker to listen on for remote commands such as requests for its log stream.

        If more than one worker is present on a single
        host, connsecutive ports will be opened, starting with the supplied port,
        up to the maximum number of workers defined by the WorkerInstanceFleet.

        :default: 56032
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Deadline pools these workers needs to be assigned to.

        The pool is created
        if it does not already exist.

        :default: - Worker is not assigned to any pool.
        '''
        result = self._values.get("pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Deadline region these workers needs to be assigned to.

        :default: - Worker is not assigned to any region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def render_queue(self) -> IRenderQueue:
        '''Endpoint for the RenderQueue, to which the worker fleet needs to be connected.'''
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return typing.cast(IRenderQueue, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the worker fleet in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def worker_machine_image(self) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''AMI of the deadline worker to launch.'''
        result = self._values.get("worker_machine_image")
        assert result is not None, "Required property 'worker_machine_image' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]]:
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice]], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''Initial amount of workers in the fleet.

        If this is set to a number, every deployment will reset the amount of
        workers to this number. It is recommended to leave this value blank.

        :default: minCapacity, and leave unchanged during deployment
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_config(self) -> typing.Optional[_HealthCheckConfig_ebe26fb6]:
        '''Properties for configuring a health check.

        Note: The health-check feature is supported with Deadline Client v10.1.9 and later.

        :default: properties of HealthCheckConfig applies
        '''
        result = self._values.get("health_check_config")
        return typing.cast(typing.Optional[_HealthCheckConfig_ebe26fb6], result)

    @builtins.property
    def health_monitor(self) -> typing.Optional[_IHealthMonitor_ab248fa9]:
        '''Health Monitor component to monitor the health of instances.

        Note: The health-check feature is supported with Deadline Client v10.1.9 and later.

        :default: - Health Monitoring is turned-off
        '''
        result = self._values.get("health_monitor")
        return typing.cast(typing.Optional[_IHealthMonitor_ab248fa9], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Type of instance to launch for the Workers.

        :default: - a T3-Large type will be used.
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of SSH keypair to grant access to instance.

        :default: - No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        '''Properties for setting up the Deadline Worker's LogGroup.

        :default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_LogGroupFactoryProps_b817ed21], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of instances in the fleet.

        :default: desiredCapacity, or minCapacity if desiredCapacity is not set
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances in the fleet.

        :default: 1
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to its resources.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        const role = new iam.Role(this, 'MyRole', {
        assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
        });

        :default: - A role will automatically be created, it can be accessed via the ``role`` property
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this fleet.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def spot_price(self) -> typing.Optional[jsii.Number]:
        '''The maximum hourly price($) to be paid for each Spot instance.

        min - 0.001; max - 255

        :default: - launches on-demand EC2 instances.
        '''
        result = self._values.get("spot_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''The specific UserData to use.

        The UserData will be mutated by this construct and may be mutated afterwards as well.

        :default: A UserData object appropriate for the MachineImage's Operating System is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def user_data_provider(self) -> typing.Optional[IInstanceUserDataProvider]:
        '''An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle.

        You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        '''
        result = self._values.get("user_data_provider")
        return typing.cast(typing.Optional[IInstanceUserDataProvider], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerInstanceFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCustomerAgreementAndIpLicenseAcceptance",
    "ConfigureSpotEventPlugin",
    "ConfigureSpotEventPluginProps",
    "DatabaseConnection",
    "DocDBConnectionOptions",
    "ECSConnectOptions",
    "ECSContainerInstanceProps",
    "ECSDirectConnectProps",
    "ECSTaskProps",
    "IContainerDirectRepositoryConnection",
    "IHost",
    "IInstanceUserDataProvider",
    "IPatchVersion",
    "IReleaseVersion",
    "IRenderQueue",
    "IRepository",
    "ISpotEventPluginFleet",
    "IVersion",
    "IWorkerFleet",
    "Installer",
    "InstanceConnectOptions",
    "InstanceDirectConnectProps",
    "InstanceUserDataProvider",
    "Manifest",
    "MongoDbInstanceConnectionOptions",
    "PlatformInstallers",
    "Recipe",
    "RenderQueue",
    "RenderQueueAccessLogProps",
    "RenderQueueExternalTLSProps",
    "RenderQueueHealthCheckConfiguration",
    "RenderQueueHostNameProps",
    "RenderQueueImages",
    "RenderQueueProps",
    "RenderQueueSecurityGroups",
    "RenderQueueSizeConstraints",
    "RenderQueueTrafficEncryptionProps",
    "Repository",
    "RepositoryBackupOptions",
    "RepositoryProps",
    "RepositoryRemovalPolicies",
    "RepositorySecurityGroupsOptions",
    "SecretsManagementProps",
    "SecretsManagementRegistrationStatus",
    "SecretsManagementRole",
    "SpotEventPluginDisplayInstanceStatus",
    "SpotEventPluginFleet",
    "SpotEventPluginFleetProps",
    "SpotEventPluginLoggingLevel",
    "SpotEventPluginPreJobTaskMode",
    "SpotEventPluginSettings",
    "SpotEventPluginState",
    "SpotFleetAllocationStrategy",
    "SpotFleetRequestType",
    "SpotFleetResourceType",
    "Stage",
    "StageProps",
    "SubnetIdentityRegistrationSettingsProps",
    "ThinkboxDockerImages",
    "ThinkboxDockerImagesProps",
    "ThinkboxDockerRecipes",
    "ThinkboxDockerRecipesProps",
    "ThinkboxManagedDeadlineDockerRecipes",
    "UsageBasedLicense",
    "UsageBasedLicenseProps",
    "UsageBasedLicensing",
    "UsageBasedLicensingImages",
    "UsageBasedLicensingProps",
    "Version",
    "VersionQuery",
    "VersionQueryProps",
    "WorkerInstanceConfiguration",
    "WorkerInstanceConfigurationProps",
    "WorkerInstanceFleet",
    "WorkerInstanceFleetProps",
    "WorkerSettings",
]

publication.publish()

def _typecheckingstub__d5dcc52dcfacbe17008708565aabdc428440637c784f588ef3a7eda3f954bc56(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    configuration: typing.Optional[typing.Union[SpotEventPluginSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_fleets: typing.Optional[typing.Sequence[SpotEventPluginFleet]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e7362e9158bf38590687283b66274526c989cd9e63d789a8ab16260c5fb218(
    *,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    configuration: typing.Optional[typing.Union[SpotEventPluginSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_fleets: typing.Optional[typing.Sequence[SpotEventPluginFleet]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1726210bad329893b864714001adefd6110aeca0c04a7974628fe48ba859ca(
    child: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1afe5f939d230131d9bca553973b795d082a64b49d1bc6dc3450ee4b8684db(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ad9d3dc48c06cf0a0e95fcbadf5de623be443a730dbf798e9ddf2abd425825(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__face20232623a608481d2a6800ff5c8cd78d461091a4c9e7c36f657fa3868cc1(
    *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0164247e3b2c3acbfbba676ca55cb1bd14c07eb06d4c5e81a2e337af77eccea8(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e6ad7c5effc3fb3ddfc7b1ed5a1d77b2b2b5fe004c144ea6aa8d5c9d26d412(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25548daa628eecb0ab05f63a6488f202046dfd41686ad9a37deeda609682e416(
    *,
    database: _aws_cdk_aws_docdb_ceddda9d.IDatabaseCluster,
    login: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d95aca067039f7b60d07f229c6e943510fd04152cb24a7286afb0554058c34(
    *,
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    hosts: typing.Sequence[IHost],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b374add9560530740ec1b39c66c2a3cb9d398f0ce7a3ad4e4e2dfdd2d46521(
    *,
    hosts: typing.Sequence[IHost],
    filesystem_mount_point: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29665b191fef1fb01446ddb4f90654ed00b5c294c80a498fdd1034adc7a4e038(
    *,
    container_instances: typing.Union[ECSContainerInstanceProps, typing.Dict[builtins.str, typing.Any]],
    containers: typing.Union[ECSTaskProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a32c14401c769257158653c2267efa3653320b30a71cbd34d2d23a1c5ec348(
    *,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    filesystem_mount_point: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11384c29da262d80585103f4b6c5798f37dcf9e4df9680833459a8049b959c63(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1511134e528f1873451562bd99e8a0ac3751a81b3ea5c27be6873fd3b5bea587(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f114ad49df14e1ac15f7458e18bb546c2c1c6e4e0fce116aa7f74aa259d78ee(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d8953d3941ecb19d1a97d64e245608a6b353a79954d3ec0020849a3a1384da(
    host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5b6f503f7586f77125c9a6f797f24c516cdc903160453d7a56c96561f26e02(
    other: Version,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17559faf4d1d2787ca7797f6bd7df3e2427aa35848381ee154c655f3d2c38f84(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5aa016640dc0ea626c28b30a7ae08228bc03864095ddc263fc6d64ef514de4(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6cad794afeaf80d6c4e8e90ed1feb89f2c7d3642a1d976858f5dbe084ec6e4(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff8d74ccd3467b61d2ead2f8e5ce4203eb44de5f0021bfd655234d27b14cd02(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8faa5873f50ce4a61a95780fc0a5962748ec973729365d0953bdf81c34abb0de(
    *,
    object_key: builtins.str,
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7562638ba04ccb0dbeb2a7533c6a672963882a064cae6a6a5ba85a801aeb54f(
    *,
    host: IHost,
    restart_launcher: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1defab2d45c3a0c48a16c697c095b94454347440e02528447ae2fc5eac4dc9(
    *,
    host: IHost,
    mount_point: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92627c86ab6795b00367244647caf558336f7d9fbc4b91ee240e1286d75e8697(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1916ec53996259b0bac9e13cdd5d4d91058df3b8bc3895f5f682ab8ac737106e(
    _host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7f968f5501726dba5ae1e2f642349a4fe4f2f21e31bd8887bba6de5e9320e7(
    _host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4ca5a86af78b74105ca48d930c493b7ed99f1f095519181f32b055f4f1c51b(
    _host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b81ce8706c9153254fd66d85c3e83929c4b751b5d70c4799974c89da2cc4f4(
    _host: IHost,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a8f7b33555bdae5362d75b04fb4994487f9e2a999ca8a81ac80b4d4d4afc9e(
    *,
    recipes: typing.Mapping[builtins.str, typing.Union[Recipe, typing.Dict[builtins.str, typing.Any]]],
    schema: jsii.Number,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032f23b04b63fa287171095416177176b209474664a6234e44d45e31c30fa26c(
    *,
    client_certificate: _IX509CertificatePkcs12_63b2574c,
    database: _IMongoDb_dbee748a,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3b756c57602a14c72b409022a33e523f7c446c091fe1cdfb4edda5bfcac198(
    *,
    client: typing.Union[Installer, typing.Dict[builtins.str, typing.Any]],
    patch_version: jsii.Number,
    repository: typing.Union[Installer, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477aeca6274b77b0713da5feb6f3fe41324b4e4149e50aa9ea218017114c4d6e(
    *,
    description: builtins.str,
    title: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ed8d99946cb7a2d5fabed2c862df495b001cb15bf80036a8bc9038e77998a7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    images: typing.Union[RenderQueueImages, typing.Dict[builtins.str, typing.Any]],
    repository: IRepository,
    version: IVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    access_logs: typing.Optional[typing.Union[RenderQueueAccessLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    enable_local_file_caching: typing.Optional[builtins.bool] = None,
    health_check_config: typing.Optional[typing.Union[RenderQueueHealthCheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname: typing.Optional[typing.Union[RenderQueueHostNameProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    render_queue_size: typing.Optional[typing.Union[RenderQueueSizeConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Union[RenderQueueSecurityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_encryption: typing.Optional[typing.Union[RenderQueueTrafficEncryptionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets_alb: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fece8ed0030db2902fbed388e48050502bf569294c86bbbe838a389ea55f985c(
    *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f92f98973954e818a3781bd1c7d19dbf1058650e19c7dfece4c1511a5a75ad(
    child: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec036f8dff121679b9d1261693a9cdd587eeebabb8b802d7007e11cae081d2a(
    *security_groups: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5737ac23037c32c853ea3c839170a3cb9ff5038a485e166495538c88cbfa51(
    include_resource_tracker: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73101760f0868b5335905dde3ce348066e082ee85e4a24469f64ac33de3e645(
    *,
    destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bec6cbece960d31a81a8445b158789cd2de49289e502f3cc82754fe4adb42d(
    *,
    acm_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    acm_certificate_chain: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rfdk_certificate: typing.Optional[_IX509CertificatePem_da3ef30f] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050ab1ec2e1eae87e0d7233e4ce476edbd81e21e3bcf4d3fbda656ef822d91b9(
    *,
    check_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    grace_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40591a8e194c9c058901f5636910f4e6a5112c43268f47299e27fb20d2c8d511(
    *,
    zone: _aws_cdk_aws_route53_ceddda9d.IPrivateHostedZone,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2077347bdbce4b13e4ec04196d18d06beb92412b531886f7e9e90f1fac39dece(
    *,
    remote_connection_server: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea009a7f12a97b7efb261edfc69a17430aaf694438fe76bc1fb9158c16f1874(
    *,
    images: typing.Union[RenderQueueImages, typing.Dict[builtins.str, typing.Any]],
    repository: IRepository,
    version: IVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    access_logs: typing.Optional[typing.Union[RenderQueueAccessLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    enable_local_file_caching: typing.Optional[builtins.bool] = None,
    health_check_config: typing.Optional[typing.Union[RenderQueueHealthCheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname: typing.Optional[typing.Union[RenderQueueHostNameProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    render_queue_size: typing.Optional[typing.Union[RenderQueueSizeConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Union[RenderQueueSecurityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_encryption: typing.Optional[typing.Union[RenderQueueTrafficEncryptionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets_alb: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5ab2581ffd8861c3d7b50043c7a9a129b8166eaca446d057891a31c1da5578(
    *,
    backend: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    frontend: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b43f6e9cf3327c7024d397d97df56d9722b6234099357d8712b4c8358a105b7(
    *,
    desired: typing.Optional[jsii.Number] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cac9e6e72e0c93ac86800c107707f0b5ace86418ee3d9b7d5654d9d6e19df57(
    *,
    external_tls: typing.Optional[typing.Union[RenderQueueExternalTLSProps, typing.Dict[builtins.str, typing.Any]]] = None,
    internal_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f99a81718b7293f5270ff48249692460af35b328a2a8aa6cca5be92ad132b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    version: IVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    backup_options: typing.Optional[typing.Union[RepositoryBackupOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    database: typing.Optional[DatabaseConnection] = None,
    database_audit_logging: typing.Optional[builtins.bool] = None,
    document_db_instance_count: typing.Optional[jsii.Number] = None,
    file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[typing.Union[RepositoryRemovalPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_installation_prefix: typing.Optional[builtins.str] = None,
    repository_installation_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    repository_settings: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    secrets_management_settings: typing.Optional[typing.Union[SecretsManagementProps, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups_options: typing.Optional[typing.Union[RepositorySecurityGroupsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d97ba60da610c56fc5818d385e906bf0628c8b7c85d49eb18dd683bf251f97(
    *,
    database_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42179c3dc6ac9346e35102fd03089d4440b6bdf471dda6d8d9654e194358bc6(
    *,
    version: IVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    backup_options: typing.Optional[typing.Union[RepositoryBackupOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    database: typing.Optional[DatabaseConnection] = None,
    database_audit_logging: typing.Optional[builtins.bool] = None,
    document_db_instance_count: typing.Optional[jsii.Number] = None,
    file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[typing.Union[RepositoryRemovalPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_installation_prefix: typing.Optional[builtins.str] = None,
    repository_installation_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    repository_settings: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    secrets_management_settings: typing.Optional[typing.Union[SecretsManagementProps, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups_options: typing.Optional[typing.Union[RepositorySecurityGroupsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8b7efa858fe0522801e80042aa2d58c92d4229626c35bdd23be296f860be9c(
    *,
    database: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    filesystem: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdbca0093e88164369525a7e1f6612cd09bc1b81400e0e32b0ef9a4fcf71acd(
    *,
    database: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    file_system: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    installer: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a692e77f4defe52e9939b229241edfba1b691d01647ec09ebf21d64d6b63759(
    *,
    enabled: builtins.bool,
    credentials: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    credentials_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366f31a28b730ce5a7a5b3de617afb7209cd13b567df3aed6c91c9fd7c754919(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    deadline_groups: typing.Sequence[builtins.str],
    instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
    max_capacity: jsii.Number,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    allocation_strategy: typing.Optional[SpotFleetAllocationStrategy] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    context: typing.Optional[builtins.str] = None,
    deadline_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    deadline_region: typing.Optional[builtins.str] = None,
    fleet_instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    track_instances_with_resource_tracker: typing.Optional[builtins.bool] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    valid_until: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab275f821b69a802c37ee2cb63c834aac1982012c8f3d304c85e07314c3a6f1(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8018d7f2b9fdd4242798b8492d9a28756f8fc7f62b7714225725e91d67b2e7c7(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24b850e03104788afddc109df2e6fb0604829a3a0c78abded4f8d0ddf7a8a36(
    *,
    deadline_groups: typing.Sequence[builtins.str],
    instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
    max_capacity: jsii.Number,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    allocation_strategy: typing.Optional[SpotFleetAllocationStrategy] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    context: typing.Optional[builtins.str] = None,
    deadline_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    deadline_region: typing.Optional[builtins.str] = None,
    fleet_instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    track_instances_with_resource_tracker: typing.Optional[builtins.bool] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    valid_until: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc3317f9d5b90675b9845a5ed84cfedde7f7fd5900a04b0b7bc66a2b8460cf6(
    *,
    aws_instance_status: typing.Optional[SpotEventPluginDisplayInstanceStatus] = None,
    delete_ec2_spot_interrupted_workers: typing.Optional[builtins.bool] = None,
    delete_sep_terminated_workers: typing.Optional[builtins.bool] = None,
    enable_resource_tracker: typing.Optional[builtins.bool] = None,
    idle_shutdown: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging_level: typing.Optional[SpotEventPluginLoggingLevel] = None,
    maximum_instances_started_per_cycle: typing.Optional[jsii.Number] = None,
    pre_job_task_mode: typing.Optional[SpotEventPluginPreJobTaskMode] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[SpotEventPluginState] = None,
    strict_hard_cap: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a61c8cdf837b3b2964992fc2d1c8dae86a2496a6bf3c633f5aa3d87838519a7(
    stage_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9548d598c3482f4994b40ccbfd44253eb8e537c4063f34509b25502f2a63c1(
    manifest_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3da84ed7aec5ea6a88184e8d81776a34b7ae17b963f2fe8ea5c901df6fd2e6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cf6f738174c7ba86904f9fceee22a78d543f24630b1d49294855dc393b8609(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac94b28fc77e31ee86750d20e26d8f44b4b1adfc18588b335f3100640c5fee60(
    *,
    manifest: typing.Union[Manifest, typing.Dict[builtins.str, typing.Any]],
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0053659919d4730a89b9fbcf980fc7ef02b65174f2fec86a91184e7a34ccf9(
    *,
    dependent: _constructs_77d1e7e8.Construct,
    registration_status: SecretsManagementRegistrationStatus,
    role: SecretsManagementRole,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d83f51eb06568090b405784d1244c35832077ff71a3ed9931011568357cf155(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user_aws_customer_agreement_and_ip_license_acceptance: AwsCustomerAgreementAndIpLicenseAcceptance,
    version: typing.Optional[IVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd873c36a3fa2b0ad39de5449ad3c3a6d30b99c3d098b25cc83e8e41b67e377f(
    *,
    user_aws_customer_agreement_and_ip_license_acceptance: AwsCustomerAgreementAndIpLicenseAcceptance,
    version: typing.Optional[IVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14c72197439cb1d6842806386c7ec6247a2d2b7611389ecdb0d6771a02e4292(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stage: Stage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13eabe941ad0e16c49b0ff3a25fdc08912e4df439ce912fdf87f8a9e5196abc0(
    *,
    stage: Stage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58183295cc6f79925d3dc41f7b26411cabe1f14c87d7fe7c592baa76109d80e6(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89467b35ad130fe47737c62ffa68da05ba60ba56157627e4a479ed36ec8de3f9(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b503dfee4e4200e93a4f552a31d11daaa9637aef07b1350108003daea6d6be7(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32b62b0ddc0e8daa25daabe4d0581dad64d6770516439a1b1324fcd56d48891(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9dda7af2655f33d01f8ac5c9b2e1f4506ed0c917122744396393b949c8f65e(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ebc0981ea5e424337802b51b392e49c264441446258f829b0b4846c8f41ff2(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7873f7f682d37cb56f271c2ac958b4f1832dfd2745e5acc893a68a55c54889a(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dac2ac3d07447a7a21d7e77c8623f2a3c240697e6c7419c98027b449f60f87a(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815157dee6fef8a445edcc5493fabf2642a6a8a9e9b5b92bd01ab96855a5c71d(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c7fde5eb0d2de564b89e5d97756958028bcc314780d76bd6f1c5682a3691f5(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cc804944d36c92ece672e1c7c4f5c2efe0580df75158bc15878d368b1dbbac(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed10df99b2bd05e529b930f93cdc405a7b57f6dfad021de7197a11fb82bc08db(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec5f059cbac14dc2950f89d9ed4da7f70a4cf77283c3a276a0f8f9e424fb68c(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c9c374b1e9323c755eefecb74d10f33ebfefb3fd091a035cda8c982d5b0ca0(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0312086803246326dc699e2065d716ed450b4eb35b4b213ca75cf82612701056(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc31a7108e3ffa9d50bb593c199be8651ca16b40f433a5a56815706ee2eb7974(
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34bfb0006ce6481fa4b2176b93c014843baf43e93af34b50c16d77c229f0231(
    *,
    license_name: builtins.str,
    ports: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Port],
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9a5c3031f59ef678ed72fb1d893f955c8a3d1ad665dfce5ea9f4e6cfc0aec1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    images: typing.Union[UsageBasedLicensingImages, typing.Dict[builtins.str, typing.Any]],
    licenses: typing.Sequence[UsageBasedLicense],
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    desired_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e12212787e2563f77d9f9691a17260dc477544948daa7fcc6f9c016416286c(
    worker_fleet: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    licenses: typing.Sequence[UsageBasedLicense],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868952e5dbbed51ce3349c95eb4a4e04cb73df666a8568b2d73b3a88d447d7b1(
    *,
    license_forwarder: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c34019ac5eac7dac1440f6c0f3e5462784549281ed3a41ae8df530e412a19b0(
    *,
    certificate_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    images: typing.Union[UsageBasedLicensingImages, typing.Dict[builtins.str, typing.Any]],
    licenses: typing.Sequence[UsageBasedLicense],
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    desired_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c4080322c875167088ee1aa79460b7ba6a0e4a0e0cf7f6e23a6b29f601a28b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fa58f11ab292ca5222e5962e63b1b5b1794efa4d2208e1b842b85bb7ca996c(
    other: Version,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fa144528ec71005da23187396ec6abbc1bb7b1826348d29daed814e87da8d1(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c737ab6625475ccd2bd3354f52ac7616135c85411c2d2591c067712b243dca9e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    worker: IHost,
    cloud_watch_log_settings: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    render_queue: typing.Optional[IRenderQueue] = None,
    should_install_cloud_watch_agent: typing.Optional[builtins.bool] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    worker_settings: typing.Optional[typing.Union[WorkerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e55982980bceacf37b29f080441101853976cab8aed15125d6422a765c9f793(
    worker: IHost,
    id: builtins.str,
    log_group_props: typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]],
    should_install_agent: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8af4774cb01dd769b9d9b4c15632e229d703b889ca562a0c6dd0ad3a6e39a2(
    worker: IHost,
    id: builtins.str,
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d9bce71a7fd19c065dfded85a010d34d94cdf22af8016e52f9034175b858f6(
    *,
    worker: IHost,
    cloud_watch_log_settings: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    render_queue: typing.Optional[IRenderQueue] = None,
    should_install_cloud_watch_agent: typing.Optional[builtins.bool] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    worker_settings: typing.Optional[typing.Union[WorkerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e672c5ae8a9c0f5ede477720680e29af86abd75d99d3b694314d9569c26c67(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    health_check_config: typing.Optional[typing.Union[_HealthCheckConfig_ebe26fb6, typing.Dict[builtins.str, typing.Any]]] = None,
    health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    spot_price: typing.Optional[jsii.Number] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9679a03a73c2811a52ceed6f73d3ebe137803e90b3160ab90bea20b0c173a8d(
    security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbde8bb042ab2246e58f6c1611f74e2596034bfb27a9773b12b049ed31f2111b(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371917bb1feabe107f46ea61078c671e18b96751ef272c92a00cb5b830d34859(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dcefb96ba46cf970ec474d4ee6223514fdd9fa26193ddac2f9159183eccf42(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4ff9d30fda5d1f404bf9183bea19d4d6e9621f270b43fa3759a0a260d76b6f(
    components: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0720999d7961642ff7016483094188bdb6e24ad94e1c705a960dba3aad135ff(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52a09c2b7c311158028b2c228d0fc5f54fdd1d3ca68a6878d4492a9538ace20(
    version: Version,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fe1e9bebc794f478a42f875d0b5fcd420e549d95cf06262b7c0f0cd4c291a6(
    version: Version,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7754a3469b09ae78f83f1a7119547aca2a2b46149827ea08e536c37d8828e8b5(
    version: Version,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5185fbd88e4b40cfb9f11f6a580addea8a00b9ae6033cf03226bc7ab0619356(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    render_queue: IRenderQueue,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    worker_machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_autoscaling_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    health_check_config: typing.Optional[typing.Union[_HealthCheckConfig_ebe26fb6, typing.Dict[builtins.str, typing.Any]]] = None,
    health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    key_name: typing.Optional[builtins.str] = None,
    log_group_props: typing.Optional[typing.Union[_LogGroupFactoryProps_b817ed21, typing.Dict[builtins.str, typing.Any]]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    spot_price: typing.Optional[jsii.Number] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
