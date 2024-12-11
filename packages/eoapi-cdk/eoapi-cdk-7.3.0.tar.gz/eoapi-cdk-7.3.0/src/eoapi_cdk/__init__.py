'''
# eoAPI CDK Constructs

eoapi-cdk is a package of [AWS CDK constructs](https://docs.aws.amazon.com/prescriptive-guidance/latest/best-practices-cdk-typescript-iac/constructs-best-practices.html) designed to encapsulate eoAPI services and best practices as simple reusable components.

For more background on the included services see [The Earth Observation API](https://eoapi.dev/)

## Included constructs

Detailed API docs for the constructs can be found [here](https://developmentseed.org/eoapi-cdk/).

### [pgSTAC Database](https://developmentseed.org/eoapi-cdk/#pgstacdatabase-)

An [RDS](https://aws.amazon.com/rds/) instance with [pgSTAC](https://github.com/stac-utils/pgstac) installed and the Postgres parameters optimized for the selected instance type.

### [STAC API](https://developmentseed.org/eoapi-cdk/#pgstacapilambda-)

A STAC API implementation using [stac-fastapi](https://github.com/stac-utils/stac-fastapi) with a [pgSTAC backend](https://github.com/stac-utils/stac-fastapi-pgstac). Packaged as a complete runtime for deployment with API Gateway and Lambda.

### [pgSTAC Titiler API](https://developmentseed.org/eoapi-cdk/#titilerpgstacapilambda-)

A complete dynamic tiling API using [titiler-pgstac](https://github.com/stac-utils/titiler-pgstac) to create dynamic mosaics of assets based on [STAC Search queries](https://github.com/radiantearth/stac-api-spec/tree/master/item-search).  Packaged as a complete runtime for deployment with API Gateway and Lambda and fully integrated with the pgSTAC Database construct.

### [STAC browser](https://developmentseed.org/eoapi-cdk/#stacbrowser-)

A CDK construct to host a static [Radiant Earth STAC browser](https://github.com/radiantearth/stac-browser) on S3.

### [OGC Features/Tiles API](https://developmentseed.org/eoapi-cdk/#titilerpgstacapilambda-)

A complete OGC Features/Tiles API using [tipg](https://github.com/developmentseed/tipg). Packaged as a complete runtime for deployment with API Gateway and Lambda. By default the API will be connected to the Database's `public` schema.

### [STAC Ingestor](https://developmentseed.org/eoapi-cdk/#stacingestor-)

An API for large scale STAC data ingestion and validation into a pgSTAC instance.

![ingestor](/diagrams/ingestor_diagram.png)

Authentication for the STAC Ingestor API can be configured with JWTs authenticated by JWKS.  To learn more about securing FastAPI applications with this approach see [Securing FastAPI with JWKS (AWS Cognito, Auth0)](https://alukach.com/posts/fastapi-rs256-jwt/).

A sample Cognito-based authentication system is available at [aws-asdi-auth](https://github.com/developmentseed/aws-asdi-auth).

### [Bastion Host](https://developmentseed.org/eoapi-cdk/#bastionhost-)

A bastion host is a secure gateway that provides access to resources in a private subnet.  In this case it provides the ability to make administrative connections to eoAPI's pgSTAC instance.

![Alt text](/diagrams/bastion_diagram.png)

For more background on bastion hosts in AWS see [this article](https://dev.to/aws-builders/bastion-host-in-aws-vpc-2i63).

And for configuration instructions for this construct see [the docs](https://developmentseed.org/eoapi-cdk/#bastionhost-).

## Published Packages

* https://pypi.org/project/eoapi-cdk/
* https://www.npmjs.com/package/eoapi-cdk/

## Release

Versioning is automatically handled via [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and [Semantic Release](https://semantic-release.gitbook.io/semantic-release/).

*Warning*: If you rebase `main`, you must ensure that the commits referenced by tags point to commits that are within the `main` branch. If a commit references a commit that is no longer on the `main` branch, Semantic Release will fail to detect the correct version of the project. [More information](https://github.com/semantic-release/semantic-release/issues/1121#issuecomment-517945233).

## Tests

Each pull request to `main` is added to a [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue#triggering-merge-group-checks-with-github-actions) so that a "deployment test" workflow can run before the merge actually happens. If the deployment fails, the merge is cancelled. Here is [the definition of this workflow](https://github.com/developmentseed/eoapi-cdk/blob/main/.github/workflows/deploy.yaml) and the [tests definition](https://github.com/developmentseed/eoapi-cdk/blob/main/tests).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_apigatewayv2_alpha as _aws_cdk_aws_apigatewayv2_alpha_050969fe
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_deployment as _aws_cdk_aws_s3_deployment_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


class BastionHost(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.BastionHost",
):
    '''(experimental) The database is located in an isolated subnet, meaning that it is not accessible from the public internet.

    As such, to interact with the database directly, a user must tunnel through a bastion host.


    Configuring

    This codebase controls *who* is allowed to connect to the bastion host. This requires two steps:

    1. Adding the IP address from which you are connecting to the ``ipv4Allowlist`` array
    2. Creating a bastion host system user by adding the user's configuration inform to ``userdata.yaml``



    Adding an IP address to the ``ipv4Allowlist`` array

    The ``BastionHost`` construct takes in an ``ipv4Allowlist`` array as an argument. Find your IP address (eg ``curl api.ipify.org``) and add that to the array along with the trailing CIDR block (likely ``/32`` to indicate that you are adding a single IP address).


    Creating a user via ``userdata.yaml``

    Add an entry to the ``users`` array with a username (likely matching your local systems username, which you can get by running the ``whoami`` command in your terminal) and a public key (likely your default public key, which you can get by running ``cat ~/.ssh/id_*.pub`` in your terminal).


    Tips & Tricks when using the Bastion Host

    **Connecting to RDS Instance via SSM*::

       aws ssm start-session --target $INSTANCE_ID \\
       --document-name AWS-StartPortForwardingSessionToRemoteHost \\
       --parameters '{
       "host": [
       "example-db.c5abcdefghij.us-west-2.rds.amazonaws.com"
       ],
       "portNumber": [
       "5432"
       ],
       "localPortNumber": [
       "9999"
       ]
       }' \\
       --profile $AWS_PROFILE

    Example::

       psql -h localhost -p 9999 # continue adding username (-U) and db (-d) here...

    Connect directly to Bastion Host::

       aws ssm start-session --target $INSTANCE_ID --profile $AWS_PROFILE

    **Setting up an SSH tunnel**

    In your ``~/.ssh/config`` file, add an entry like::

       Host db-tunnel
       Hostname {the-bastion-host-address}
       LocalForward 9999 {the-db-hostname}:5432

    Then a tunnel can be opened via::

       ssh -N db-tunnel

    And a connection to the DB can be made via::

       psql -h 127.0.0.1 -p 9999 -U {username} -d {database}

    **Handling ``REMOTE HOST IDENTIFICATION HAS CHANGED!`` error**

    If you've redeployed a bastion host that you've previously connected to, you may see an error like::

    :stability: experimental
    ::

    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    SHA256:mPnxAOXTpb06PFgI1Qc8TMQ2e9b7goU8y2NdS5hzIr8.
    Please contact your system administrator.
    Add correct host key in /Users/username/.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /Users/username/.ssh/known_hosts:28
    ECDSA host key for ec2-12-34-56-789.us-west-2.compute.amazonaws.com has changed and you have requested strict checking.
    Host key verification failed::


    This is due to the server's fingerprint changing. We can scrub the fingerprint from our system with a command like:

    ssh-keygen -R 12.34.56.789 Example::
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        ipv4_allowlist: typing.Sequence[builtins.str],
        user_data: _aws_cdk_aws_ec2_ceddda9d.UserData,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        create_elastic_ip: typing.Optional[builtins.bool] = None,
        ssh_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: 
        :param ipv4_allowlist: 
        :param user_data: 
        :param vpc: 
        :param create_elastic_ip: (experimental) Whether or not an elastic IP should be created for the bastion host. Default: false
        :param ssh_port: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18e4a05ea5338da6442f75b48edb06202da020c3d8bf632551496a430733dea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastionHostProps(
            db=db,
            ipv4_allowlist=ipv4_allowlist,
            user_data=user_data,
            vpc=vpc,
            create_elastic_ip=create_elastic_ip,
            ssh_port=ssh_port,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> _aws_cdk_aws_ec2_ceddda9d.Instance:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Instance, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: _aws_cdk_aws_ec2_ceddda9d.Instance) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fb0feedb858fb24741f897aca05b271358cdc74e541cfb7aab020793c77769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.BastionHostProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "ipv4_allowlist": "ipv4Allowlist",
        "user_data": "userData",
        "vpc": "vpc",
        "create_elastic_ip": "createElasticIp",
        "ssh_port": "sshPort",
    },
)
class BastionHostProps:
    def __init__(
        self,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        ipv4_allowlist: typing.Sequence[builtins.str],
        user_data: _aws_cdk_aws_ec2_ceddda9d.UserData,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        create_elastic_ip: typing.Optional[builtins.bool] = None,
        ssh_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param db: 
        :param ipv4_allowlist: 
        :param user_data: 
        :param vpc: 
        :param create_elastic_ip: (experimental) Whether or not an elastic IP should be created for the bastion host. Default: false
        :param ssh_port: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b386a6dcf129df4056c8a5276b48fe035d0e88dfdab638585b346608595de11a)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument ipv4_allowlist", value=ipv4_allowlist, expected_type=type_hints["ipv4_allowlist"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument create_elastic_ip", value=create_elastic_ip, expected_type=type_hints["create_elastic_ip"])
            check_type(argname="argument ssh_port", value=ssh_port, expected_type=type_hints["ssh_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db": db,
            "ipv4_allowlist": ipv4_allowlist,
            "user_data": user_data,
            "vpc": vpc,
        }
        if create_elastic_ip is not None:
            self._values["create_elastic_ip"] = create_elastic_ip
        if ssh_port is not None:
            self._values["ssh_port"] = ssh_port

    @builtins.property
    def db(self) -> _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance:
        '''
        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IDatabaseInstance, result)

    @builtins.property
    def ipv4_allowlist(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ipv4_allowlist")
        assert result is not None, "Required property 'ipv4_allowlist' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_data")
        assert result is not None, "Required property 'user_data' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def create_elastic_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not an elastic IP should be created for the bastion host.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("create_elastic_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_port(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ssh_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="eoapi-cdk.DatabaseParameters",
    jsii_struct_bases=[],
    name_mapping={
        "effective_cache_size": "effectiveCacheSize",
        "maintenance_work_mem": "maintenanceWorkMem",
        "max_connections": "maxConnections",
        "max_locks_per_transaction": "maxLocksPerTransaction",
        "random_page_cost": "randomPageCost",
        "seq_page_cost": "seqPageCost",
        "shared_buffers": "sharedBuffers",
        "temp_buffers": "tempBuffers",
        "work_mem": "workMem",
    },
)
class DatabaseParameters:
    def __init__(
        self,
        *,
        effective_cache_size: builtins.str,
        maintenance_work_mem: builtins.str,
        max_connections: builtins.str,
        max_locks_per_transaction: builtins.str,
        random_page_cost: builtins.str,
        seq_page_cost: builtins.str,
        shared_buffers: builtins.str,
        temp_buffers: builtins.str,
        work_mem: builtins.str,
    ) -> None:
        '''
        :param effective_cache_size: Default: - 75% of instance memory
        :param maintenance_work_mem: Default: - 25% of shared buffers
        :param max_connections: Default: - LEAST({DBInstanceClassMemory/9531392}, 5000)
        :param max_locks_per_transaction: Default: 1024
        :param random_page_cost: Default: 1.1
        :param seq_page_cost: Default: 1
        :param shared_buffers: (experimental) Note: This value is measured in 8KB blocks. Default: '{DBInstanceClassMemory/32768}' 25% of instance memory, ie ``{(DBInstanceClassMemory/(1024*8)) * 0.25}``
        :param temp_buffers: Default: 131172 (128 * 1024)
        :param work_mem: Default: - shared buffers divided by max connections

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea09864cfb7ef653ba6117478229014e8f7a29d8b3c241aa363b884a0c943ee)
            check_type(argname="argument effective_cache_size", value=effective_cache_size, expected_type=type_hints["effective_cache_size"])
            check_type(argname="argument maintenance_work_mem", value=maintenance_work_mem, expected_type=type_hints["maintenance_work_mem"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_locks_per_transaction", value=max_locks_per_transaction, expected_type=type_hints["max_locks_per_transaction"])
            check_type(argname="argument random_page_cost", value=random_page_cost, expected_type=type_hints["random_page_cost"])
            check_type(argname="argument seq_page_cost", value=seq_page_cost, expected_type=type_hints["seq_page_cost"])
            check_type(argname="argument shared_buffers", value=shared_buffers, expected_type=type_hints["shared_buffers"])
            check_type(argname="argument temp_buffers", value=temp_buffers, expected_type=type_hints["temp_buffers"])
            check_type(argname="argument work_mem", value=work_mem, expected_type=type_hints["work_mem"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effective_cache_size": effective_cache_size,
            "maintenance_work_mem": maintenance_work_mem,
            "max_connections": max_connections,
            "max_locks_per_transaction": max_locks_per_transaction,
            "random_page_cost": random_page_cost,
            "seq_page_cost": seq_page_cost,
            "shared_buffers": shared_buffers,
            "temp_buffers": temp_buffers,
            "work_mem": work_mem,
        }

    @builtins.property
    def effective_cache_size(self) -> builtins.str:
        '''
        :default: - 75% of instance memory

        :stability: experimental
        '''
        result = self._values.get("effective_cache_size")
        assert result is not None, "Required property 'effective_cache_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_work_mem(self) -> builtins.str:
        '''
        :default: - 25% of shared buffers

        :stability: experimental
        '''
        result = self._values.get("maintenance_work_mem")
        assert result is not None, "Required property 'maintenance_work_mem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_connections(self) -> builtins.str:
        '''
        :default: - LEAST({DBInstanceClassMemory/9531392}, 5000)

        :stability: experimental
        '''
        result = self._values.get("max_connections")
        assert result is not None, "Required property 'max_connections' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_locks_per_transaction(self) -> builtins.str:
        '''
        :default: 1024

        :stability: experimental
        '''
        result = self._values.get("max_locks_per_transaction")
        assert result is not None, "Required property 'max_locks_per_transaction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def random_page_cost(self) -> builtins.str:
        '''
        :default: 1.1

        :stability: experimental
        '''
        result = self._values.get("random_page_cost")
        assert result is not None, "Required property 'random_page_cost' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def seq_page_cost(self) -> builtins.str:
        '''
        :default: 1

        :stability: experimental
        '''
        result = self._values.get("seq_page_cost")
        assert result is not None, "Required property 'seq_page_cost' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shared_buffers(self) -> builtins.str:
        '''(experimental) Note: This value is measured in 8KB blocks.

        :default: '{DBInstanceClassMemory/32768}' 25% of instance memory, ie ``{(DBInstanceClassMemory/(1024*8)) * 0.25}``

        :stability: experimental
        '''
        result = self._values.get("shared_buffers")
        assert result is not None, "Required property 'shared_buffers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def temp_buffers(self) -> builtins.str:
        '''
        :default: 131172 (128 * 1024)

        :stability: experimental
        '''
        result = self._values.get("temp_buffers")
        assert result is not None, "Required property 'temp_buffers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def work_mem(self) -> builtins.str:
        '''
        :default: - shared buffers divided by max connections

        :stability: experimental
        '''
        result = self._values.get("work_mem")
        assert result is not None, "Required property 'work_mem' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PgStacApiLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.PgStacApiLambda",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        stac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to fastapi-pgstac runtime.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param stac_api_domain_name: (experimental) Custom Domain Name Options for STAC API,.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001e0940684741a8dcd75ad791003ac3ff1c57fce9c2ee18d768c590ee1c200b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PgStacApiLambdaProps(
            db=db,
            db_secret=db_secret,
            api_env=api_env,
            lambda_function_options=lambda_function_options,
            stac_api_domain_name=stac_api_domain_name,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="stacApiLambdaFunction")
    def stac_api_lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "stacApiLambdaFunction"))

    @stac_api_lambda_function.setter
    def stac_api_lambda_function(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c3356e9c4fcad6133b4d30c2f7d84fd7701ed6e27781d7055d4f617ea74570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacApiLambdaFunction", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.PgStacApiLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "db_secret": "dbSecret",
        "api_env": "apiEnv",
        "lambda_function_options": "lambdaFunctionOptions",
        "stac_api_domain_name": "stacApiDomainName",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class PgStacApiLambdaProps:
    def __init__(
        self,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        stac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to fastapi-pgstac runtime.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param stac_api_domain_name: (experimental) Custom Domain Name Options for STAC API,.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac048adccce72d79219bafd7e28ffb071969e8f3fa9b9b9048c3ff3355fa171)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument db_secret", value=db_secret, expected_type=type_hints["db_secret"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
            check_type(argname="argument lambda_function_options", value=lambda_function_options, expected_type=type_hints["lambda_function_options"])
            check_type(argname="argument stac_api_domain_name", value=stac_api_domain_name, expected_type=type_hints["stac_api_domain_name"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db": db,
            "db_secret": db_secret,
        }
        if api_env is not None:
            self._values["api_env"] = api_env
        if lambda_function_options is not None:
            self._values["lambda_function_options"] = lambda_function_options
        if stac_api_domain_name is not None:
            self._values["stac_api_domain_name"] = stac_api_domain_name
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def db(self) -> _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance:
        '''(experimental) RDS Instance with installed pgSTAC.

        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IDatabaseInstance, result)

    @builtins.property
    def db_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) Secret containing connection information for pgSTAC database.

        :stability: experimental
        '''
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Customized environment variables to send to fastapi-pgstac runtime.

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stac_api_domain_name(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName]:
        '''(experimental) Custom Domain Name Options for STAC API,.

        :stability: experimental
        '''
        result = self._values.get("stac_api_domain_name")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnet into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgStacApiLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PgStacDatabase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.PgStacDatabase",
):
    '''(experimental) An RDS instance with pgSTAC installed.

    This is a wrapper around the
    ``rds.DatabaseInstance`` higher-level construct making use
    of the BootstrapPgStac construct.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bootstrapper_lambda_function_options: typing.Any = None,
        custom_resource_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
        character_set_name: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        engine: _aws_cdk_aws_rds_ceddda9d.IInstanceEngine,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        license_model: typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timezone: typing.Optional[builtins.str] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        ca_certificate: typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate] = None,
        cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloudwatch_logs_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        cloudwatch_logs_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
        delete_automated_backups: typing.Optional[builtins.bool] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        enable_performance_insights: typing.Optional[builtins.bool] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        monitoring_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        multi_az: typing.Optional[builtins.bool] = None,
        network_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType] = None,
        option_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
        performance_insight_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        performance_insight_retention: typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        s3_export_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        s3_export_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        s3_import_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        s3_import_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_throughput: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType] = None,
        subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bootstrapper_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param custom_resource_properties: (experimental) Lambda function Custom Resource properties. A custom resource property is going to be created to trigger the boostrapping lambda function. This parameter allows the user to specify additional properties on top of the defaults ones.
        :param pgstac_db_name: (experimental) Name of database that is to be created and onto which pgSTAC will be installed. Default: pgstac
        :param pgstac_username: (experimental) Name of user that will be generated for connecting to the pgSTAC database. Default: pgstac_user
        :param secrets_prefix: (experimental) Prefix to assign to the generated ``secrets_manager.Secret``. Default: pgstac
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param credentials: Credentials for the administrative user. Default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gibibytes (GiB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param parameters: The parameters in the DBParameterGroup to create automatically. You can only specify parameterGroup or parameters but not both. You need to use a versioned engine to auto-generate a DBParameterGroup. Default: - None
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. When creating a read replica, you must enable automatic backups on the source database instance by setting the backup retention to a value other than zero. Default: - Duration.days(1) for source instances, disabled for read replicas
        :param ca_certificate: The identifier of the CA certificate for this DB instance. Specifying or updating this property triggers a reboot. For RDS DB engines: Default: - RDS will choose a certificate authority
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: true
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if ``DatabaseInstanceNewProps#domain`` is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRetention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops if storage type is not specified. For GP3: 3,000 IOPS if allocated storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL, less than 200 GiB for Oracle and less than 20 GiB for SQL Server. 12,000 IOPS otherwise (except for SQL Server where the default is always 3,000 IOPS).
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param network_type: The network type of the DB instance. Default: - IPV4
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7 this is the free tier
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. If not specified, the instance's vpcSubnets will be used to determine if the instance is internet-facing or not. Default: - ``true`` if the instance's ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This property must not be used if ``s3ExportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_export_role: Role that will be associated with this DB instance to enable S3 export. This property must not be used if ``s3ExportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_import_role: Role that will be associated with this DB instance to enable S3 import. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_throughput: The storage throughput, specified in mebibytes per second (MiBps). Only applicable for GP3. Default: - 125 MiBps if allocated storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL, less than 200 GiB for Oracle and less than 20 GiB for SQL Server. 500 MiBps otherwise (except for SQL Server where the default is always 125 MiBps).
        :param storage_type: The storage type. Storage types supported are gp2, io1, standard. Default: GP2
        :param subnet_group: Existing subnet group for the instance. Default: - a new subnet group will be created.
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee96e62bc19e035f9c50d6fa57ffa87eec4eddea97361cc3013acc3001e78e01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PgStacDatabaseProps(
            bootstrapper_lambda_function_options=bootstrapper_lambda_function_options,
            custom_resource_properties=custom_resource_properties,
            pgstac_db_name=pgstac_db_name,
            pgstac_username=pgstac_username,
            secrets_prefix=secrets_prefix,
            character_set_name=character_set_name,
            credentials=credentials,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
            engine=engine,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            database_name=database_name,
            instance_type=instance_type,
            license_model=license_model,
            parameters=parameters,
            timezone=timezone,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            ca_certificate=ca_certificate,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            network_type=network_type,
            option_group=option_group,
            parameter_group=parameter_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            publicly_accessible=publicly_accessible,
            removal_policy=removal_policy,
            s3_export_buckets=s3_export_buckets,
            s3_export_role=s3_export_role,
            s3_import_buckets=s3_import_buckets,
            s3_import_role=s3_import_role,
            security_groups=security_groups,
            storage_throughput=storage_throughput,
            storage_type=storage_type,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getParameters")
    def get_parameters(
        self,
        instance_type: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> DatabaseParameters:
        '''
        :param instance_type: -
        :param parameters: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff6bc5a4652111b5590ced879fe657007b0fb02fe8dc4e13d41a922474a3ef8)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(DatabaseParameters, jsii.invoke(self, "getParameters", [instance_type, parameters]))

    @builtins.property
    @jsii.member(jsii_name="db")
    def db(self) -> _aws_cdk_aws_rds_ceddda9d.DatabaseInstance:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.DatabaseInstance, jsii.get(self, "db"))

    @db.setter
    def db(self, value: _aws_cdk_aws_rds_ceddda9d.DatabaseInstance) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e80f4c7855b52d0a5a598524d2fcdafa861926a45a2af11846d99c3bc6d7d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "db", value)

    @builtins.property
    @jsii.member(jsii_name="pgstacSecret")
    def pgstac_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "pgstacSecret"))

    @pgstac_secret.setter
    def pgstac_secret(
        self,
        value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9f4370761bcda923ab4970fe50e71c6c3ac2b30f7238afa86c49b09a8a3414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgstacSecret", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.PgStacDatabaseProps",
    jsii_struct_bases=[_aws_cdk_aws_rds_ceddda9d.DatabaseInstanceProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "ca_certificate": "caCertificate",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "network_type": "networkType",
        "option_group": "optionGroup",
        "parameter_group": "parameterGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "publicly_accessible": "publiclyAccessible",
        "removal_policy": "removalPolicy",
        "s3_export_buckets": "s3ExportBuckets",
        "s3_export_role": "s3ExportRole",
        "s3_import_buckets": "s3ImportBuckets",
        "s3_import_role": "s3ImportRole",
        "security_groups": "securityGroups",
        "storage_throughput": "storageThroughput",
        "storage_type": "storageType",
        "subnet_group": "subnetGroup",
        "vpc_subnets": "vpcSubnets",
        "engine": "engine",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "database_name": "databaseName",
        "instance_type": "instanceType",
        "license_model": "licenseModel",
        "parameters": "parameters",
        "timezone": "timezone",
        "character_set_name": "characterSetName",
        "credentials": "credentials",
        "storage_encrypted": "storageEncrypted",
        "storage_encryption_key": "storageEncryptionKey",
        "bootstrapper_lambda_function_options": "bootstrapperLambdaFunctionOptions",
        "custom_resource_properties": "customResourceProperties",
        "pgstac_db_name": "pgstacDbName",
        "pgstac_username": "pgstacUsername",
        "secrets_prefix": "secretsPrefix",
    },
)
class PgStacDatabaseProps(_aws_cdk_aws_rds_ceddda9d.DatabaseInstanceProps):
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        ca_certificate: typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate] = None,
        cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloudwatch_logs_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        cloudwatch_logs_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
        delete_automated_backups: typing.Optional[builtins.bool] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        enable_performance_insights: typing.Optional[builtins.bool] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        monitoring_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        multi_az: typing.Optional[builtins.bool] = None,
        network_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType] = None,
        option_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
        performance_insight_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        performance_insight_retention: typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        s3_export_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        s3_export_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        s3_import_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        s3_import_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_throughput: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType] = None,
        subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        engine: _aws_cdk_aws_rds_ceddda9d.IInstanceEngine,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        license_model: typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timezone: typing.Optional[builtins.str] = None,
        character_set_name: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        bootstrapper_lambda_function_options: typing.Any = None,
        custom_resource_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. When creating a read replica, you must enable automatic backups on the source database instance by setting the backup retention to a value other than zero. Default: - Duration.days(1) for source instances, disabled for read replicas
        :param ca_certificate: The identifier of the CA certificate for this DB instance. Specifying or updating this property triggers a reboot. For RDS DB engines: Default: - RDS will choose a certificate authority
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: true
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if ``DatabaseInstanceNewProps#domain`` is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRetention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops if storage type is not specified. For GP3: 3,000 IOPS if allocated storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL, less than 200 GiB for Oracle and less than 20 GiB for SQL Server. 12,000 IOPS otherwise (except for SQL Server where the default is always 3,000 IOPS).
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param network_type: The network type of the DB instance. Default: - IPV4
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7 this is the free tier
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. If not specified, the instance's vpcSubnets will be used to determine if the instance is internet-facing or not. Default: - ``true`` if the instance's ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This property must not be used if ``s3ExportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_export_role: Role that will be associated with this DB instance to enable S3 export. This property must not be used if ``s3ExportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_import_role: Role that will be associated with this DB instance to enable S3 import. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_throughput: The storage throughput, specified in mebibytes per second (MiBps). Only applicable for GP3. Default: - 125 MiBps if allocated storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL, less than 200 GiB for Oracle and less than 20 GiB for SQL Server. 500 MiBps otherwise (except for SQL Server where the default is always 125 MiBps).
        :param storage_type: The storage type. Storage types supported are gp2, io1, standard. Default: GP2
        :param subnet_group: Existing subnet group for the instance. Default: - a new subnet group will be created.
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gibibytes (GiB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param parameters: The parameters in the DBParameterGroup to create automatically. You can only specify parameterGroup or parameters but not both. You need to use a versioned engine to auto-generate a DBParameterGroup. Default: - None
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param credentials: Credentials for the administrative user. Default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param bootstrapper_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param custom_resource_properties: (experimental) Lambda function Custom Resource properties. A custom resource property is going to be created to trigger the boostrapping lambda function. This parameter allows the user to specify additional properties on top of the defaults ones.
        :param pgstac_db_name: (experimental) Name of database that is to be created and onto which pgSTAC will be installed. Default: pgstac
        :param pgstac_username: (experimental) Name of user that will be generated for connecting to the pgSTAC database. Default: pgstac_user
        :param secrets_prefix: (experimental) Prefix to assign to the generated ``secrets_manager.Secret``. Default: pgstac

        :stability: experimental
        '''
        if isinstance(processor_features, dict):
            processor_features = _aws_cdk_aws_rds_ceddda9d.ProcessorFeatures(**processor_features)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258b1c29ccb1e46320eabd0ab87e2a36a78f09de16f1610cc09d0c29f0ad1822)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument cloudwatch_logs_exports", value=cloudwatch_logs_exports, expected_type=type_hints["cloudwatch_logs_exports"])
            check_type(argname="argument cloudwatch_logs_retention", value=cloudwatch_logs_retention, expected_type=type_hints["cloudwatch_logs_retention"])
            check_type(argname="argument cloudwatch_logs_retention_role", value=cloudwatch_logs_retention_role, expected_type=type_hints["cloudwatch_logs_retention_role"])
            check_type(argname="argument copy_tags_to_snapshot", value=copy_tags_to_snapshot, expected_type=type_hints["copy_tags_to_snapshot"])
            check_type(argname="argument delete_automated_backups", value=delete_automated_backups, expected_type=type_hints["delete_automated_backups"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_role", value=domain_role, expected_type=type_hints["domain_role"])
            check_type(argname="argument enable_performance_insights", value=enable_performance_insights, expected_type=type_hints["enable_performance_insights"])
            check_type(argname="argument iam_authentication", value=iam_authentication, expected_type=type_hints["iam_authentication"])
            check_type(argname="argument instance_identifier", value=instance_identifier, expected_type=type_hints["instance_identifier"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument max_allocated_storage", value=max_allocated_storage, expected_type=type_hints["max_allocated_storage"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_role", value=monitoring_role, expected_type=type_hints["monitoring_role"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument option_group", value=option_group, expected_type=type_hints["option_group"])
            check_type(argname="argument parameter_group", value=parameter_group, expected_type=type_hints["parameter_group"])
            check_type(argname="argument performance_insight_encryption_key", value=performance_insight_encryption_key, expected_type=type_hints["performance_insight_encryption_key"])
            check_type(argname="argument performance_insight_retention", value=performance_insight_retention, expected_type=type_hints["performance_insight_retention"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument processor_features", value=processor_features, expected_type=type_hints["processor_features"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument s3_export_buckets", value=s3_export_buckets, expected_type=type_hints["s3_export_buckets"])
            check_type(argname="argument s3_export_role", value=s3_export_role, expected_type=type_hints["s3_export_role"])
            check_type(argname="argument s3_import_buckets", value=s3_import_buckets, expected_type=type_hints["s3_import_buckets"])
            check_type(argname="argument s3_import_role", value=s3_import_role, expected_type=type_hints["s3_import_role"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_throughput", value=storage_throughput, expected_type=type_hints["storage_throughput"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument allow_major_version_upgrade", value=allow_major_version_upgrade, expected_type=type_hints["allow_major_version_upgrade"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument character_set_name", value=character_set_name, expected_type=type_hints["character_set_name"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument storage_encryption_key", value=storage_encryption_key, expected_type=type_hints["storage_encryption_key"])
            check_type(argname="argument bootstrapper_lambda_function_options", value=bootstrapper_lambda_function_options, expected_type=type_hints["bootstrapper_lambda_function_options"])
            check_type(argname="argument custom_resource_properties", value=custom_resource_properties, expected_type=type_hints["custom_resource_properties"])
            check_type(argname="argument pgstac_db_name", value=pgstac_db_name, expected_type=type_hints["pgstac_db_name"])
            check_type(argname="argument pgstac_username", value=pgstac_username, expected_type=type_hints["pgstac_username"])
            check_type(argname="argument secrets_prefix", value=secrets_prefix, expected_type=type_hints["secrets_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
            "engine": engine,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if network_type is not None:
            self._values["network_type"] = network_type
        if option_group is not None:
            self._values["option_group"] = option_group
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if s3_export_buckets is not None:
            self._values["s3_export_buckets"] = s3_export_buckets
        if s3_export_role is not None:
            self._values["s3_export_role"] = s3_export_role
        if s3_import_buckets is not None:
            self._values["s3_import_buckets"] = s3_import_buckets
        if s3_import_role is not None:
            self._values["s3_import_role"] = s3_import_role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_throughput is not None:
            self._values["storage_throughput"] = storage_throughput
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_group is not None:
            self._values["subnet_group"] = subnet_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if database_name is not None:
            self._values["database_name"] = database_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if license_model is not None:
            self._values["license_model"] = license_model
        if parameters is not None:
            self._values["parameters"] = parameters
        if timezone is not None:
            self._values["timezone"] = timezone
        if character_set_name is not None:
            self._values["character_set_name"] = character_set_name
        if credentials is not None:
            self._values["credentials"] = credentials
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key
        if bootstrapper_lambda_function_options is not None:
            self._values["bootstrapper_lambda_function_options"] = bootstrapper_lambda_function_options
        if custom_resource_properties is not None:
            self._values["custom_resource_properties"] = custom_resource_properties
        if pgstac_db_name is not None:
            self._values["pgstac_db_name"] = pgstac_db_name
        if pgstac_username is not None:
            self._values["pgstac_username"] = pgstac_username
        if secrets_prefix is not None:
            self._values["secrets_prefix"] = secrets_prefix

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC network where the DB subnet group should be created.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        :default: true
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Availability Zone where the DB instance will be located.

        :default: - no preference
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The number of days during which automatic DB snapshots are retained.

        Set to zero to disable backups.
        When creating a read replica, you must enable automatic backups on the source
        database instance by setting the backup retention to a value other than zero.

        :default: - Duration.days(1) for source instances, disabled for read replicas
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def ca_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate]:
        '''The identifier of the CA certificate for this DB instance.

        Specifying or updating this property triggers a reboot.

        For RDS DB engines:

        :default: - RDS will choose a certificate authority

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL-certificate-rotation.html
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate], result)

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to CloudWatch Logs.

        :default: - no log exports
        '''
        result = self._values.get("cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cloudwatch_logs_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        :default: - logs never expire
        '''
        result = self._values.get("cloudwatch_logs_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def cloudwatch_logs_retention_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - a new role is created.
        '''
        result = self._values.get("cloudwatch_logs_retention_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        :default: true
        '''
        result = self._values.get("copy_tags_to_snapshot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        :default: true
        '''
        result = self._values.get("delete_automated_backups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance should have deletion protection enabled.

        :default: - true if ``removalPolicy`` is RETAIN, false otherwise
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The Active Directory directory ID to create the DB instance in.

        :default: - Do not join domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        :default: - The role will be created for you if ``DatabaseInstanceNewProps#domain`` is specified
        '''
        result = self._values.get("domain_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable Performance Insights for the DB instance.

        :default: - false, unless ``performanceInsightRetention`` or ``performanceInsightEncryptionKey`` is set.
        '''
        result = self._values.get("enable_performance_insights")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        :default: false
        '''
        result = self._values.get("iam_authentication")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_identifier(self) -> typing.Optional[builtins.str]:
        '''A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        :default: - a CloudFormation generated name
        '''
        result = self._values.get("instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        :default:

        - no provisioned iops if storage type is not specified. For GP3: 3,000 IOPS if allocated
        storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL, less than 200 GiB for Oracle and
        less than 20 GiB for SQL Server. 12,000 IOPS otherwise (except for SQL Server where the default is
        always 3,000 IOPS).
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        :default: - No autoscaling of RDS instance

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        '''
        result = self._values.get("max_allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        :default: - no enhanced monitoring
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Role that will be used to manage DB instance monitoring.

        :default: - A role is automatically created for you
        '''
        result = self._values.get("monitoring_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def multi_az(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the database instance is a multiple Availability Zone deployment.

        :default: false
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def network_type(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType]:
        '''The network type of the DB instance.

        :default: - IPV4
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType], result)

    @builtins.property
    def option_group(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup]:
        '''The option group to associate with the instance.

        :default: - no option group
        '''
        result = self._values.get("option_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup], result)

    @builtins.property
    def parameter_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup]:
        '''The DB parameter group to associate with the instance.

        :default: - no parameter group
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup], result)

    @builtins.property
    def performance_insight_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The AWS KMS key for encryption of Performance Insights data.

        :default: - default master key
        '''
        result = self._values.get("performance_insight_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention]:
        '''The amount of time, in days, to retain Performance Insights data.

        :default: 7 this is the free tier
        '''
        result = self._values.get("performance_insight_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port for the instance.

        :default: - the default port for the chosen engine.
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region. To see the time blocks available, see
        https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region, occurring on a random day of the week. To see
        the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_features(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures]:
        '''The number of CPU cores and the number of threads per core.

        :default:

        - the default number of CPU cores and threads per core for the
        chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        '''
        result = self._values.get("processor_features")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures], result)

    @builtins.property
    def publicly_accessible(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance is an internet-facing instance.

        If not specified,
        the instance's vpcSubnets will be used to determine if the instance is internet-facing
        or not.

        :default: - ``true`` if the instance's ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def s3_export_buckets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''S3 buckets that you want to load data into.

        This property must not be used if ``s3ExportRole`` is used.

        For Microsoft SQL Server:

        :default: - None

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.html
        '''
        result = self._values.get("s3_export_buckets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def s3_export_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Role that will be associated with this DB instance to enable S3 export.

        This property must not be used if ``s3ExportBuckets`` is used.

        For Microsoft SQL Server:

        :default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.html
        '''
        result = self._values.get("s3_export_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def s3_import_buckets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''S3 buckets that you want to load data from.

        This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines.

        This property must not be used if ``s3ImportRole`` is used.

        For Microsoft SQL Server:

        :default: - None

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html
        '''
        result = self._values.get("s3_import_buckets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def s3_import_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Role that will be associated with this DB instance to enable S3 import.

        This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines.

        This property must not be used if ``s3ImportBuckets`` is used.

        For Microsoft SQL Server:

        :default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html
        '''
        result = self._values.get("s3_import_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The security groups to assign to the DB instance.

        :default: - a new security group is created
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def storage_throughput(self) -> typing.Optional[jsii.Number]:
        '''The storage throughput, specified in mebibytes per second (MiBps).

        Only applicable for GP3.

        :default:

        - 125 MiBps if allocated storage is less than 400 GiB for MariaDB, MySQL, and PostgreSQL,
        less than 200 GiB for Oracle and less than 20 GiB for SQL Server. 500 MiBps otherwise (except for
        SQL Server where the default is always 125 MiBps).

        :see: https://docs.aws.amazon.com//AmazonRDS/latest/UserGuide/CHAP_Storage.html#gp3-storage
        '''
        result = self._values.get("storage_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType]:
        '''The storage type.

        Storage types supported are gp2, io1, standard.

        :default: GP2

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#Concepts.Storage.GeneralSSD
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType], result)

    @builtins.property
    def subnet_group(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup]:
        '''Existing subnet group for the instance.

        :default: - a new subnet group will be created.
        '''
        result = self._values.get("subnet_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The type of subnets to add to the created DB subnet group.

        :default: - private subnets
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def engine(self) -> _aws_cdk_aws_rds_ceddda9d.IInstanceEngine:
        '''The database engine.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IInstanceEngine, result)

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The allocated storage size, specified in gibibytes (GiB).

        :default: 100
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow major version upgrades.

        :default: false
        '''
        result = self._values.get("allow_major_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database.

        :default: - no name
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The name of the compute and memory capacity for the instance.

        :default: - m5.large (or, more specifically, db.m5.large)
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def license_model(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel]:
        '''The license model.

        :default: - RDS default license model
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The parameters in the DBParameterGroup to create automatically.

        You can only specify parameterGroup or parameters but not both.
        You need to use a versioned engine to auto-generate a DBParameterGroup.

        :default: - None
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the instance.

        This is currently supported only by Microsoft Sql Server.

        :default: - RDS default timezone
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def character_set_name(self) -> typing.Optional[builtins.str]:
        '''For supported engines, specifies the character set to associate with the DB instance.

        :default: - RDS default character set name
        '''
        result = self._values.get("character_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials]:
        '''Credentials for the administrative user.

        :default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials], result)

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance is encrypted.

        :default: - true if storageEncryptionKey has been provided, false otherwise
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The KMS key that's used to encrypt the DB instance.

        :default: - default master key if storageEncrypted is true, no key otherwise
        '''
        result = self._values.get("storage_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def bootstrapper_lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("bootstrapper_lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def custom_resource_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Lambda function Custom Resource properties.

        A custom resource property is going to be created
        to trigger the boostrapping lambda function. This parameter allows the user to specify additional properties
        on top of the defaults ones.

        :stability: experimental
        '''
        result = self._values.get("custom_resource_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def pgstac_db_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of database that is to be created and onto which pgSTAC will be installed.

        :default: pgstac

        :stability: experimental
        '''
        result = self._values.get("pgstac_db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pgstac_username(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of user that will be generated for connecting to the pgSTAC database.

        :default: pgstac_user

        :stability: experimental
        '''
        result = self._values.get("pgstac_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix to assign to the generated ``secrets_manager.Secret``.

        :default: pgstac

        :stability: experimental
        '''
        result = self._values.get("secrets_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgStacDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StacBrowser(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.StacBrowser",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        github_repo_tag: builtins.str,
        stac_catalog_url: builtins.str,
        bucket_arn: typing.Optional[builtins.str] = None,
        clone_directory: typing.Optional[builtins.str] = None,
        cloud_front_distribution_arn: typing.Optional[builtins.str] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param github_repo_tag: (experimental) Tag of the radiant earth stac-browser repo to use to build the app.
        :param stac_catalog_url: (experimental) STAC catalog URL. Overrides the catalog URL in the stac-browser configuration.
        :param bucket_arn: (experimental) Bucket ARN. If specified, the identity used to deploy the stack must have the appropriate permissions to create a deployment for this bucket. In addition, if specified, ``cloudFrontDistributionArn`` is ignored since the policy of an imported resource can't be modified. Default: - No bucket ARN. A new bucket will be created.
        :param clone_directory: (experimental) Location in the filesystem where to compile the browser code. Default: - DEFAULT_CLONE_DIRECTORY
        :param cloud_front_distribution_arn: (experimental) The ARN of the cloudfront distribution that will be added to the bucket policy with read access. If ``bucketArn`` is specified, this parameter is ignored since the policy of an imported bucket can't be modified. Default: - No cloudfront distribution ARN. The bucket policy will not be modified.
        :param config_file_path: (experimental) Path to config file for the STAC browser. If not provided, default configuration in the STAC browser repository is used.
        :param website_index_document: (experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b97f434cf7e0303d3917f39a4cfe4c59ceea2191b4d779028baa0e95339797a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StacBrowserProps(
            github_repo_tag=github_repo_tag,
            stac_catalog_url=stac_catalog_url,
            bucket_arn=bucket_arn,
            clone_directory=clone_directory,
            cloud_front_distribution_arn=cloud_front_distribution_arn,
            config_file_path=config_file_path,
            website_index_document=website_index_document,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ecbe37640c40a466002fc9a172c97cb647a26279e41e5dc86dbc920737dc8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="bucketDeployment")
    def bucket_deployment(self) -> _aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment, jsii.get(self, "bucketDeployment"))

    @bucket_deployment.setter
    def bucket_deployment(
        self,
        value: _aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5411950c935f7f57a7c1a5f8942992db0e8c4ce327c12cb4114649a606e9a498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketDeployment", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.StacBrowserProps",
    jsii_struct_bases=[],
    name_mapping={
        "github_repo_tag": "githubRepoTag",
        "stac_catalog_url": "stacCatalogUrl",
        "bucket_arn": "bucketArn",
        "clone_directory": "cloneDirectory",
        "cloud_front_distribution_arn": "cloudFrontDistributionArn",
        "config_file_path": "configFilePath",
        "website_index_document": "websiteIndexDocument",
    },
)
class StacBrowserProps:
    def __init__(
        self,
        *,
        github_repo_tag: builtins.str,
        stac_catalog_url: builtins.str,
        bucket_arn: typing.Optional[builtins.str] = None,
        clone_directory: typing.Optional[builtins.str] = None,
        cloud_front_distribution_arn: typing.Optional[builtins.str] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param github_repo_tag: (experimental) Tag of the radiant earth stac-browser repo to use to build the app.
        :param stac_catalog_url: (experimental) STAC catalog URL. Overrides the catalog URL in the stac-browser configuration.
        :param bucket_arn: (experimental) Bucket ARN. If specified, the identity used to deploy the stack must have the appropriate permissions to create a deployment for this bucket. In addition, if specified, ``cloudFrontDistributionArn`` is ignored since the policy of an imported resource can't be modified. Default: - No bucket ARN. A new bucket will be created.
        :param clone_directory: (experimental) Location in the filesystem where to compile the browser code. Default: - DEFAULT_CLONE_DIRECTORY
        :param cloud_front_distribution_arn: (experimental) The ARN of the cloudfront distribution that will be added to the bucket policy with read access. If ``bucketArn`` is specified, this parameter is ignored since the policy of an imported bucket can't be modified. Default: - No cloudfront distribution ARN. The bucket policy will not be modified.
        :param config_file_path: (experimental) Path to config file for the STAC browser. If not provided, default configuration in the STAC browser repository is used.
        :param website_index_document: (experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f9917daa52e4e73b4e07ecf19198c389b259b6ef52a033a26f51c3c8e332a0)
            check_type(argname="argument github_repo_tag", value=github_repo_tag, expected_type=type_hints["github_repo_tag"])
            check_type(argname="argument stac_catalog_url", value=stac_catalog_url, expected_type=type_hints["stac_catalog_url"])
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument clone_directory", value=clone_directory, expected_type=type_hints["clone_directory"])
            check_type(argname="argument cloud_front_distribution_arn", value=cloud_front_distribution_arn, expected_type=type_hints["cloud_front_distribution_arn"])
            check_type(argname="argument config_file_path", value=config_file_path, expected_type=type_hints["config_file_path"])
            check_type(argname="argument website_index_document", value=website_index_document, expected_type=type_hints["website_index_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "github_repo_tag": github_repo_tag,
            "stac_catalog_url": stac_catalog_url,
        }
        if bucket_arn is not None:
            self._values["bucket_arn"] = bucket_arn
        if clone_directory is not None:
            self._values["clone_directory"] = clone_directory
        if cloud_front_distribution_arn is not None:
            self._values["cloud_front_distribution_arn"] = cloud_front_distribution_arn
        if config_file_path is not None:
            self._values["config_file_path"] = config_file_path
        if website_index_document is not None:
            self._values["website_index_document"] = website_index_document

    @builtins.property
    def github_repo_tag(self) -> builtins.str:
        '''(experimental) Tag of the radiant earth stac-browser repo to use to build the app.

        :stability: experimental
        '''
        result = self._values.get("github_repo_tag")
        assert result is not None, "Required property 'github_repo_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stac_catalog_url(self) -> builtins.str:
        '''(experimental) STAC catalog URL.

        Overrides the catalog URL in the stac-browser configuration.

        :stability: experimental
        '''
        result = self._values.get("stac_catalog_url")
        assert result is not None, "Required property 'stac_catalog_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bucket ARN.

        If specified, the identity used to deploy the stack must have the appropriate permissions to create a deployment for this bucket.
        In addition, if specified, ``cloudFrontDistributionArn`` is ignored since the policy of an imported resource can't be modified.

        :default: - No bucket ARN. A new bucket will be created.

        :stability: experimental
        '''
        result = self._values.get("bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clone_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Location in the filesystem where to compile the browser code.

        :default: - DEFAULT_CLONE_DIRECTORY

        :stability: experimental
        '''
        result = self._values.get("clone_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_front_distribution_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the cloudfront distribution that will be added to the bucket policy with read access.

        If ``bucketArn`` is specified, this parameter is ignored since the policy of an imported bucket can't be modified.

        :default: - No cloudfront distribution ARN. The bucket policy will not be modified.

        :stability: experimental
        '''
        result = self._values.get("cloud_front_distribution_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to config file for the STAC browser.

        If not provided, default configuration in the STAC browser
        repository is used.

        :stability: experimental
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_index_document(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket.

        :default: - No index document.

        :stability: experimental
        '''
        result = self._values.get("website_index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StacBrowserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StacIngestor(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.StacIngestor",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_access_role: _aws_cdk_aws_iam_ceddda9d.IRole,
        stac_db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        stac_db_security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
        stac_url: builtins.str,
        stage: builtins.str,
        api_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_lambda_function_options: typing.Any = None,
        api_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        ingestor_domain_name_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        ingestor_lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_access_role: (experimental) ARN of AWS Role used to validate access to S3 data.
        :param stac_db_secret: (experimental) Secret containing pgSTAC DB connection information.
        :param stac_db_security_group: (experimental) Security Group used by pgSTAC DB.
        :param stac_url: (experimental) URL of STAC API.
        :param stage: (experimental) Stage of deployment (e.g. ``dev``, ``prod``).
        :param api_endpoint_configuration: (experimental) API Endpoint Configuration, useful for creating private APIs.
        :param api_env: (experimental) Environment variables to be sent to Lambda.
        :param api_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - default settings are defined in the construct.
        :param api_policy: (experimental) API Policy Document, useful for creating private APIs.
        :param ingestor_domain_name_options: (experimental) Custom Domain Name Options for Ingestor API.
        :param ingestor_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - default settings are defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed if using a VPC.
        :param vpc: (experimental) VPC running pgSTAC DB.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382d10e3afd78d40fe969e19b1c5acb05bd014fc58a430f822916c2bc55c36ea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StacIngestorProps(
            data_access_role=data_access_role,
            stac_db_secret=stac_db_secret,
            stac_db_security_group=stac_db_security_group,
            stac_url=stac_url,
            stage=stage,
            api_endpoint_configuration=api_endpoint_configuration,
            api_env=api_env,
            api_lambda_function_options=api_lambda_function_options,
            api_policy=api_policy,
            ingestor_domain_name_options=ingestor_domain_name_options,
            ingestor_lambda_function_options=ingestor_lambda_function_options,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handlerRole")
    def handler_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "handlerRole"))

    @handler_role.setter
    def handler_role(self, value: _aws_cdk_aws_iam_ceddda9d.Role) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2224388f216581da00708bb900b469d6120a2b7c35c035b435af4a41e5183c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handlerRole", value)

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "table"))

    @table.setter
    def table(self, value: _aws_cdk_aws_dynamodb_ceddda9d.Table) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed605ecda82e38e548e66cc636258322473a42915619fe32d9d803320dcef5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.StacIngestorProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role": "dataAccessRole",
        "stac_db_secret": "stacDbSecret",
        "stac_db_security_group": "stacDbSecurityGroup",
        "stac_url": "stacUrl",
        "stage": "stage",
        "api_endpoint_configuration": "apiEndpointConfiguration",
        "api_env": "apiEnv",
        "api_lambda_function_options": "apiLambdaFunctionOptions",
        "api_policy": "apiPolicy",
        "ingestor_domain_name_options": "ingestorDomainNameOptions",
        "ingestor_lambda_function_options": "ingestorLambdaFunctionOptions",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class StacIngestorProps:
    def __init__(
        self,
        *,
        data_access_role: _aws_cdk_aws_iam_ceddda9d.IRole,
        stac_db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        stac_db_security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
        stac_url: builtins.str,
        stage: builtins.str,
        api_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_lambda_function_options: typing.Any = None,
        api_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        ingestor_domain_name_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        ingestor_lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param data_access_role: (experimental) ARN of AWS Role used to validate access to S3 data.
        :param stac_db_secret: (experimental) Secret containing pgSTAC DB connection information.
        :param stac_db_security_group: (experimental) Security Group used by pgSTAC DB.
        :param stac_url: (experimental) URL of STAC API.
        :param stage: (experimental) Stage of deployment (e.g. ``dev``, ``prod``).
        :param api_endpoint_configuration: (experimental) API Endpoint Configuration, useful for creating private APIs.
        :param api_env: (experimental) Environment variables to be sent to Lambda.
        :param api_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - default settings are defined in the construct.
        :param api_policy: (experimental) API Policy Document, useful for creating private APIs.
        :param ingestor_domain_name_options: (experimental) Custom Domain Name Options for Ingestor API.
        :param ingestor_lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - default settings are defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed if using a VPC.
        :param vpc: (experimental) VPC running pgSTAC DB.

        :stability: experimental
        '''
        if isinstance(api_endpoint_configuration, dict):
            api_endpoint_configuration = _aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration(**api_endpoint_configuration)
        if isinstance(ingestor_domain_name_options, dict):
            ingestor_domain_name_options = _aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions(**ingestor_domain_name_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a57d9ce730427c9464d66460707367708eb0bc9a9f69fbe2eb0cdbfb084ec9)
            check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
            check_type(argname="argument stac_db_secret", value=stac_db_secret, expected_type=type_hints["stac_db_secret"])
            check_type(argname="argument stac_db_security_group", value=stac_db_security_group, expected_type=type_hints["stac_db_security_group"])
            check_type(argname="argument stac_url", value=stac_url, expected_type=type_hints["stac_url"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument api_endpoint_configuration", value=api_endpoint_configuration, expected_type=type_hints["api_endpoint_configuration"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
            check_type(argname="argument api_lambda_function_options", value=api_lambda_function_options, expected_type=type_hints["api_lambda_function_options"])
            check_type(argname="argument api_policy", value=api_policy, expected_type=type_hints["api_policy"])
            check_type(argname="argument ingestor_domain_name_options", value=ingestor_domain_name_options, expected_type=type_hints["ingestor_domain_name_options"])
            check_type(argname="argument ingestor_lambda_function_options", value=ingestor_lambda_function_options, expected_type=type_hints["ingestor_lambda_function_options"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_access_role": data_access_role,
            "stac_db_secret": stac_db_secret,
            "stac_db_security_group": stac_db_security_group,
            "stac_url": stac_url,
            "stage": stage,
        }
        if api_endpoint_configuration is not None:
            self._values["api_endpoint_configuration"] = api_endpoint_configuration
        if api_env is not None:
            self._values["api_env"] = api_env
        if api_lambda_function_options is not None:
            self._values["api_lambda_function_options"] = api_lambda_function_options
        if api_policy is not None:
            self._values["api_policy"] = api_policy
        if ingestor_domain_name_options is not None:
            self._values["ingestor_domain_name_options"] = ingestor_domain_name_options
        if ingestor_lambda_function_options is not None:
            self._values["ingestor_lambda_function_options"] = ingestor_lambda_function_options
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def data_access_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) ARN of AWS Role used to validate access to S3 data.

        :stability: experimental
        '''
        result = self._values.get("data_access_role")
        assert result is not None, "Required property 'data_access_role' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, result)

    @builtins.property
    def stac_db_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) Secret containing pgSTAC DB connection information.

        :stability: experimental
        '''
        result = self._values.get("stac_db_secret")
        assert result is not None, "Required property 'stac_db_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def stac_db_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''(experimental) Security Group used by pgSTAC DB.

        :stability: experimental
        '''
        result = self._values.get("stac_db_security_group")
        assert result is not None, "Required property 'stac_db_security_group' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, result)

    @builtins.property
    def stac_url(self) -> builtins.str:
        '''(experimental) URL of STAC API.

        :stability: experimental
        '''
        result = self._values.get("stac_url")
        assert result is not None, "Required property 'stac_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''(experimental) Stage of deployment (e.g. ``dev``, ``prod``).

        :stability: experimental
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_endpoint_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration]:
        '''(experimental) API Endpoint Configuration, useful for creating private APIs.

        :stability: experimental
        '''
        result = self._values.get("api_endpoint_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration], result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to be sent to Lambda.

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def api_lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - default settings are defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("api_lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def api_policy(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''(experimental) API Policy Document, useful for creating private APIs.

        :stability: experimental
        '''
        result = self._values.get("api_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    @builtins.property
    def ingestor_domain_name_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions]:
        '''(experimental) Custom Domain Name Options for Ingestor API.

        :stability: experimental
        '''
        result = self._values.get("ingestor_domain_name_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions], result)

    @builtins.property
    def ingestor_lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - default settings are defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("ingestor_lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnet into which the lambda should be deployed if using a VPC.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC running pgSTAC DB.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StacIngestorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TiPgApiLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.TiPgApiLambda",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tipg_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to titiler-pgstac runtime.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param tipg_api_domain_name: (experimental) Custom Domain Name for tipg API. If defined, will create the domain name and integrate it with the tipg API. Default: - undefined
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0826d8694d7942b670a22c452863755627ab9af4557bb03a20bfd01dbed22491)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TiPgApiLambdaProps(
            db=db,
            db_secret=db_secret,
            api_env=api_env,
            lambda_function_options=lambda_function_options,
            subnet_selection=subnet_selection,
            tipg_api_domain_name=tipg_api_domain_name,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="tiPgLambdaFunction")
    def ti_pg_lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "tiPgLambdaFunction"))

    @ti_pg_lambda_function.setter
    def ti_pg_lambda_function(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f908f2b03d8624d502ddfeb6d44ceee686d0eaabfb7aaad570a91b6db90b012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tiPgLambdaFunction", value)


@jsii.data_type(
    jsii_type="eoapi-cdk.TiPgApiLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "db_secret": "dbSecret",
        "api_env": "apiEnv",
        "lambda_function_options": "lambdaFunctionOptions",
        "subnet_selection": "subnetSelection",
        "tipg_api_domain_name": "tipgApiDomainName",
        "vpc": "vpc",
    },
)
class TiPgApiLambdaProps:
    def __init__(
        self,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tipg_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to titiler-pgstac runtime.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param tipg_api_domain_name: (experimental) Custom Domain Name for tipg API. If defined, will create the domain name and integrate it with the tipg API. Default: - undefined
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7b315d993cc5100817e9fa2086872db371adea0c52ddee49864f4b2b7a101d)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument db_secret", value=db_secret, expected_type=type_hints["db_secret"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
            check_type(argname="argument lambda_function_options", value=lambda_function_options, expected_type=type_hints["lambda_function_options"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument tipg_api_domain_name", value=tipg_api_domain_name, expected_type=type_hints["tipg_api_domain_name"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db": db,
            "db_secret": db_secret,
        }
        if api_env is not None:
            self._values["api_env"] = api_env
        if lambda_function_options is not None:
            self._values["lambda_function_options"] = lambda_function_options
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tipg_api_domain_name is not None:
            self._values["tipg_api_domain_name"] = tipg_api_domain_name
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def db(self) -> _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance:
        '''(experimental) RDS Instance with installed pgSTAC.

        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IDatabaseInstance, result)

    @builtins.property
    def db_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) Secret containing connection information for pgSTAC database.

        :stability: experimental
        '''
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Customized environment variables to send to titiler-pgstac runtime.

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnet into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def tipg_api_domain_name(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName]:
        '''(experimental) Custom Domain Name for tipg API.

        If defined, will create the
        domain name and integrate it with the tipg API.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("tipg_api_domain_name")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TiPgApiLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="eoapi-cdk.TitilerPgStacApiLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "db_secret": "dbSecret",
        "api_env": "apiEnv",
        "buckets": "buckets",
        "lambda_function_options": "lambdaFunctionOptions",
        "subnet_selection": "subnetSelection",
        "titiler_pgstac_api_domain_name": "titilerPgstacApiDomainName",
        "vpc": "vpc",
    },
)
class TitilerPgStacApiLambdaProps:
    def __init__(
        self,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        titiler_pgstac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to titiler-pgstac runtime. These will be merged with ``defaultTitilerPgstacEnv``. The database secret arn is automatically added to the environment variables at deployment. /
        :param buckets: (experimental) list of buckets the lambda will be granted access to.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param titiler_pgstac_api_domain_name: (experimental) Custom Domain Name Options for Titiler Pgstac API,. Default: - undefined.
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a499007b8913fd5d0af1888afd5f32ef824aa7e21bf2b961981da6df009e2b0d)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument db_secret", value=db_secret, expected_type=type_hints["db_secret"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
            check_type(argname="argument lambda_function_options", value=lambda_function_options, expected_type=type_hints["lambda_function_options"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument titiler_pgstac_api_domain_name", value=titiler_pgstac_api_domain_name, expected_type=type_hints["titiler_pgstac_api_domain_name"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db": db,
            "db_secret": db_secret,
        }
        if api_env is not None:
            self._values["api_env"] = api_env
        if buckets is not None:
            self._values["buckets"] = buckets
        if lambda_function_options is not None:
            self._values["lambda_function_options"] = lambda_function_options
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if titiler_pgstac_api_domain_name is not None:
            self._values["titiler_pgstac_api_domain_name"] = titiler_pgstac_api_domain_name
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def db(self) -> _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance:
        '''(experimental) RDS Instance with installed pgSTAC.

        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IDatabaseInstance, result)

    @builtins.property
    def db_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) Secret containing connection information for pgSTAC database.

        :stability: experimental
        '''
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Customized environment variables to send to titiler-pgstac runtime.

        These will be merged with ``defaultTitilerPgstacEnv``.
        The database secret arn is automatically added to the environment variables at deployment.
        /

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def buckets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) list of buckets the lambda will be granted access to.

        :stability: experimental
        '''
        result = self._values.get("buckets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lambda_function_options(self) -> typing.Any:
        '''(experimental) Can be used to override the default lambda function properties.

        :default: - defined in the construct.

        :stability: experimental
        '''
        result = self._values.get("lambda_function_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnet into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def titiler_pgstac_api_domain_name(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName]:
        '''(experimental) Custom Domain Name Options for Titiler Pgstac API,.

        :default: - undefined.

        :stability: experimental
        '''
        result = self._values.get("titiler_pgstac_api_domain_name")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TitilerPgStacApiLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TitilerPgstacApiLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="eoapi-cdk.TitilerPgstacApiLambda",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
        db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_function_options: typing.Any = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        titiler_pgstac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param api_env: (experimental) Customized environment variables to send to titiler-pgstac runtime. These will be merged with ``defaultTitilerPgstacEnv``. The database secret arn is automatically added to the environment variables at deployment. /
        :param buckets: (experimental) list of buckets the lambda will be granted access to.
        :param lambda_function_options: (experimental) Can be used to override the default lambda function properties. Default: - defined in the construct.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param titiler_pgstac_api_domain_name: (experimental) Custom Domain Name Options for Titiler Pgstac API,. Default: - undefined.
        :param vpc: (experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b90457bc885f0e9a1addcbc1cfd61c2e0b2bb60bb399d941f3cc8776892902)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TitilerPgStacApiLambdaProps(
            db=db,
            db_secret=db_secret,
            api_env=api_env,
            buckets=buckets,
            lambda_function_options=lambda_function_options,
            subnet_selection=subnet_selection,
            titiler_pgstac_api_domain_name=titiler_pgstac_api_domain_name,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="titilerPgstacLambdaFunction")
    def titiler_pgstac_lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "titilerPgstacLambdaFunction"))

    @titiler_pgstac_lambda_function.setter
    def titiler_pgstac_lambda_function(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae429080881692eda11326adbfaae8dacaec10c61b4af3a038e97d46bd181b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "titilerPgstacLambdaFunction", value)


__all__ = [
    "BastionHost",
    "BastionHostProps",
    "DatabaseParameters",
    "PgStacApiLambda",
    "PgStacApiLambdaProps",
    "PgStacDatabase",
    "PgStacDatabaseProps",
    "StacBrowser",
    "StacBrowserProps",
    "StacIngestor",
    "StacIngestorProps",
    "TiPgApiLambda",
    "TiPgApiLambdaProps",
    "TitilerPgStacApiLambdaProps",
    "TitilerPgstacApiLambda",
]

publication.publish()

def _typecheckingstub__f18e4a05ea5338da6442f75b48edb06202da020c3d8bf632551496a430733dea(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    ipv4_allowlist: typing.Sequence[builtins.str],
    user_data: _aws_cdk_aws_ec2_ceddda9d.UserData,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    create_elastic_ip: typing.Optional[builtins.bool] = None,
    ssh_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fb0feedb858fb24741f897aca05b271358cdc74e541cfb7aab020793c77769(
    value: _aws_cdk_aws_ec2_ceddda9d.Instance,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b386a6dcf129df4056c8a5276b48fe035d0e88dfdab638585b346608595de11a(
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    ipv4_allowlist: typing.Sequence[builtins.str],
    user_data: _aws_cdk_aws_ec2_ceddda9d.UserData,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    create_elastic_ip: typing.Optional[builtins.bool] = None,
    ssh_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea09864cfb7ef653ba6117478229014e8f7a29d8b3c241aa363b884a0c943ee(
    *,
    effective_cache_size: builtins.str,
    maintenance_work_mem: builtins.str,
    max_connections: builtins.str,
    max_locks_per_transaction: builtins.str,
    random_page_cost: builtins.str,
    seq_page_cost: builtins.str,
    shared_buffers: builtins.str,
    temp_buffers: builtins.str,
    work_mem: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001e0940684741a8dcd75ad791003ac3ff1c57fce9c2ee18d768c590ee1c200b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    stac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c3356e9c4fcad6133b4d30c2f7d84fd7701ed6e27781d7055d4f617ea74570(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac048adccce72d79219bafd7e28ffb071969e8f3fa9b9b9048c3ff3355fa171(
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    stac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee96e62bc19e035f9c50d6fa57ffa87eec4eddea97361cc3013acc3001e78e01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bootstrapper_lambda_function_options: typing.Any = None,
    custom_resource_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    pgstac_db_name: typing.Optional[builtins.str] = None,
    pgstac_username: typing.Optional[builtins.str] = None,
    secrets_prefix: typing.Optional[builtins.str] = None,
    character_set_name: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
    storage_encrypted: typing.Optional[builtins.bool] = None,
    storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    engine: _aws_cdk_aws_rds_ceddda9d.IInstanceEngine,
    allocated_storage: typing.Optional[jsii.Number] = None,
    allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
    database_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    license_model: typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timezone: typing.Optional[builtins.str] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ca_certificate: typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate] = None,
    cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    cloudwatch_logs_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    cloudwatch_logs_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
    delete_automated_backups: typing.Optional[builtins.bool] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    enable_performance_insights: typing.Optional[builtins.bool] = None,
    iam_authentication: typing.Optional[builtins.bool] = None,
    instance_identifier: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    max_allocated_storage: typing.Optional[jsii.Number] = None,
    monitoring_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    monitoring_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    multi_az: typing.Optional[builtins.bool] = None,
    network_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType] = None,
    option_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
    performance_insight_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    performance_insight_retention: typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    processor_features: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    publicly_accessible: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    s3_export_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    s3_export_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    s3_import_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    s3_import_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_throughput: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType] = None,
    subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff6bc5a4652111b5590ced879fe657007b0fb02fe8dc4e13d41a922474a3ef8(
    instance_type: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e80f4c7855b52d0a5a598524d2fcdafa861926a45a2af11846d99c3bc6d7d9f(
    value: _aws_cdk_aws_rds_ceddda9d.DatabaseInstance,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9f4370761bcda923ab4970fe50e71c6c3ac2b30f7238afa86c49b09a8a3414(
    value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258b1c29ccb1e46320eabd0ab87e2a36a78f09de16f1610cc09d0c29f0ad1822(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ca_certificate: typing.Optional[_aws_cdk_aws_rds_ceddda9d.CaCertificate] = None,
    cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    cloudwatch_logs_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    cloudwatch_logs_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
    delete_automated_backups: typing.Optional[builtins.bool] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    enable_performance_insights: typing.Optional[builtins.bool] = None,
    iam_authentication: typing.Optional[builtins.bool] = None,
    instance_identifier: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    max_allocated_storage: typing.Optional[jsii.Number] = None,
    monitoring_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    monitoring_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    multi_az: typing.Optional[builtins.bool] = None,
    network_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.NetworkType] = None,
    option_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IOptionGroup] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
    performance_insight_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    performance_insight_retention: typing.Optional[_aws_cdk_aws_rds_ceddda9d.PerformanceInsightRetention] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    processor_features: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ProcessorFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    publicly_accessible: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    s3_export_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    s3_export_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    s3_import_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    s3_import_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_throughput: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[_aws_cdk_aws_rds_ceddda9d.StorageType] = None,
    subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    engine: _aws_cdk_aws_rds_ceddda9d.IInstanceEngine,
    allocated_storage: typing.Optional[jsii.Number] = None,
    allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
    database_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    license_model: typing.Optional[_aws_cdk_aws_rds_ceddda9d.LicenseModel] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timezone: typing.Optional[builtins.str] = None,
    character_set_name: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
    storage_encrypted: typing.Optional[builtins.bool] = None,
    storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    bootstrapper_lambda_function_options: typing.Any = None,
    custom_resource_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    pgstac_db_name: typing.Optional[builtins.str] = None,
    pgstac_username: typing.Optional[builtins.str] = None,
    secrets_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b97f434cf7e0303d3917f39a4cfe4c59ceea2191b4d779028baa0e95339797a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    github_repo_tag: builtins.str,
    stac_catalog_url: builtins.str,
    bucket_arn: typing.Optional[builtins.str] = None,
    clone_directory: typing.Optional[builtins.str] = None,
    cloud_front_distribution_arn: typing.Optional[builtins.str] = None,
    config_file_path: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ecbe37640c40a466002fc9a172c97cb647a26279e41e5dc86dbc920737dc8a(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5411950c935f7f57a7c1a5f8942992db0e8c4ce327c12cb4114649a606e9a498(
    value: _aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f9917daa52e4e73b4e07ecf19198c389b259b6ef52a033a26f51c3c8e332a0(
    *,
    github_repo_tag: builtins.str,
    stac_catalog_url: builtins.str,
    bucket_arn: typing.Optional[builtins.str] = None,
    clone_directory: typing.Optional[builtins.str] = None,
    cloud_front_distribution_arn: typing.Optional[builtins.str] = None,
    config_file_path: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382d10e3afd78d40fe969e19b1c5acb05bd014fc58a430f822916c2bc55c36ea(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_access_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    stac_db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    stac_db_security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    stac_url: builtins.str,
    stage: builtins.str,
    api_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    api_lambda_function_options: typing.Any = None,
    api_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ingestor_domain_name_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ingestor_lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2224388f216581da00708bb900b469d6120a2b7c35c035b435af4a41e5183c(
    value: _aws_cdk_aws_iam_ceddda9d.Role,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed605ecda82e38e548e66cc636258322473a42915619fe32d9d803320dcef5c(
    value: _aws_cdk_aws_dynamodb_ceddda9d.Table,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a57d9ce730427c9464d66460707367708eb0bc9a9f69fbe2eb0cdbfb084ec9(
    *,
    data_access_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    stac_db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    stac_db_security_group: _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup,
    stac_url: builtins.str,
    stage: builtins.str,
    api_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    api_lambda_function_options: typing.Any = None,
    api_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ingestor_domain_name_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ingestor_lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0826d8694d7942b670a22c452863755627ab9af4557bb03a20bfd01dbed22491(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tipg_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f908f2b03d8624d502ddfeb6d44ceee686d0eaabfb7aaad570a91b6db90b012(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7b315d993cc5100817e9fa2086872db371adea0c52ddee49864f4b2b7a101d(
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tipg_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a499007b8913fd5d0af1888afd5f32ef824aa7e21bf2b961981da6df009e2b0d(
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    titiler_pgstac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b90457bc885f0e9a1addcbc1cfd61c2e0b2bb60bb399d941f3cc8776892902(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db: _aws_cdk_aws_rds_ceddda9d.IDatabaseInstance,
    db_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_function_options: typing.Any = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    titiler_pgstac_api_domain_name: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IDomainName] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae429080881692eda11326adbfaae8dacaec10c61b4af3a038e97d46bd181b1(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass
