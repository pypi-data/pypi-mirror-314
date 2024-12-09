r'''
# redis-cloud-database

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Redis::Cloud::Database` v1.0.0.

## Description

CloudFormation template for Pro Database.

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Redis::Cloud::Database \
  --publisher-id 991a427d4922adc55ddc491f1a3a0421a61120bc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/991a427d4922adc55ddc491f1a3a0421a61120bc/Redis-Cloud-Database \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Redis::Cloud::Database`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fredis-cloud-database+v1.0.0).
* Issues related to `Redis::Cloud::Database` should be reported to the [publisher](undefined).

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


class CfnDatabase(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/redis-cloud-database.CfnDatabase",
):
    '''A CloudFormation ``Redis::Cloud::Database``.

    :cloudformationResource: Redis::Cloud::Database
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        dataset_size_in_gb: builtins.str,
        subscription_id: builtins.str,
        alerts: typing.Optional[builtins.str] = None,
        average_item_size_in_bytes: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        client_tls_certificates: typing.Optional[builtins.str] = None,
        data_eviction_policy: typing.Optional[builtins.str] = None,
        data_persistence: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.str] = None,
        enable_default_user: typing.Optional[builtins.str] = None,
        enable_tls: typing.Optional[builtins.str] = None,
        import_from_uri: typing.Optional[builtins.str] = None,
        local_throughput_measurement: typing.Optional[builtins.str] = None,
        modules: typing.Optional[builtins.str] = None,
        on_demand_backup: typing.Optional[builtins.str] = None,
        on_demand_import: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_performance_factor: typing.Optional[builtins.str] = None,
        regex_rules: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        remote_backup: typing.Optional[builtins.str] = None,
        replica: typing.Optional[builtins.str] = None,
        replication: typing.Optional[builtins.str] = None,
        resp_version: typing.Optional[builtins.str] = None,
        sasl_password: typing.Optional[builtins.str] = None,
        sasl_username: typing.Optional[builtins.str] = None,
        source_ip: typing.Optional[builtins.str] = None,
        source_type: typing.Optional[builtins.str] = None,
        support_oss_cluster_api: typing.Optional[builtins.str] = None,
        throughput_measurement: typing.Optional[builtins.str] = None,
        use_external_endpoint_for_oss_cluster_api: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Redis::Cloud::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: [Required]. Database name (Database name must be up to 40 characters long, include only letters, digits, or hyphen ('-'), start with a letter, and end with a letter or digit). Example: Redis-database-example
        :param dataset_size_in_gb: [Required]. The maximum amount of data in the dataset for this specific database is in GB. You can not set both datasetSizeInGb and totalMemoryInGb. if 'replication' is true, the database's total memory will be twice as large as the datasetSizeInGb.if 'replication' is false, the database's total memory of the database will be the datasetSizeInGb value. Minimum: 0.1. ExclusiveMinimum: false. Example: 1
        :param subscription_id: [Required]. The Subscription ID under which the Database is created.
        :param alerts: [Optional. Input as JSON]. Redis database alerts.
        :param average_item_size_in_bytes: [Optional]. Relevant only to ram-and-flash clusters. Estimated average size (measured in bytes) of the items stored in the database. Default: 1000
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param client_tls_certificates: [Optional. Input as a JSON]. A list of TLS/SSL certificates (public keys) with new line characters replaced by . If specified, mTLS authentication (with enableTls not specified or set to true) will be required to authenticate user connections. If empty list is received, SSL certificates will be removed and mTLS will not be required (note that TLS connection may still apply, depending on the value of the enableTls property). Default: 'null'
        :param data_eviction_policy: [Optional]. Data items eviction method. List of options: [ allkeys-lru, allkeys-lfu, allkeys-random, volatile-lru, volatile-lfu, volatile-random, volatile-ttl, noeviction ]. Default: 'volatile-lru'
        :param data_persistence: [Optional]. Rate of database data persistence (in persistent storage). List of options: [ none, aof-every-1-second, aof-every-write, snapshot-every-1-hour, snapshot-every-6-hours, snapshot-every-12-hours ]. Example: none. Default: 'none'.
        :param dry_run: [Optional]. When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.
        :param enable_default_user: [Optional. Can only be modified upon Update request from a Cloud Formation stack]. When 'true', enables connecting to the database with the 'default' user. Default: 'true'. Can only be set if Database Protocol is REDIS
        :param enable_tls: [Optional]. When 'true', requires TLS authentication for all connections (mTLS with valid clientSslCertificate, regular TLS when the clientSslCertificate is not provided. Default: 'false'
        :param import_from_uri: [Required for Import. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true']. One or more URIs to source data files or Redis databases, as appropriate to specified source type (example: ['http://mydomain.com/redis-backup-file1', 'http://mydomain.com/redis-backup-file2'])
        :param local_throughput_measurement: [Optional. Input as JSON]. Throughput measurement for an active-active subscription
        :param modules: [Optional. Input as JSON]. Redis modules to be provisioned in the database.
        :param on_demand_backup: [Required to enable Backup. Can only be modified upon Update request from a Cloud Formation stack. Requires 'remoteBackup' to be active]. If 'true', creates a backup of the current database and disables all other parameters set for Update except for 'RegionName'. Default 'false'.
        :param on_demand_import: [Required to enable Import. Can only be modified upon Update request from a Cloud Formation stack]. If 'true', imports the previous created backup of a database and disables all other parameters set for Update except for 'SourceType' and 'ImportFromUri'. Default 'false'.
        :param password: [Optional]. Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is REDIS
        :param port: [Optional]. TCP port on which the database is available (10000-19999). Generated automatically if omitted. Example: 10000
        :param protocol: [Optional]. Database protocol: either 'redis' or 'memcached'. Default: 'redis'
        :param query_performance_factor: [Optional]. The query performance factor adds extra compute power specifically for search and query. For databases with search and query, you can increase your search queries per second by the selected factor. Example: 2x
        :param regex_rules: [Optional. Can only be modified upon Update request from a Cloud Formation stack]. Shard regex rules. Relevant only for a sharded database.
        :param region_name: [Optional. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandBackup' set to 'true']. Name of cloud provider region where the local database is located. When backing up an active-active database, backup is done separately for each local database at a specified region. Example for active-active database: 'us-east-1'. For single-region deployment, the value MUST be 'null'.
        :param remote_backup: [Optional. Input as JSON]. Database remote backup configuration
        :param replica: [Optional. Input as JSON]. Replica Of configuration
        :param replication: [Optional]. Databases replication. Default: 'true'
        :param resp_version: [Optional]. RESP version must be compatible with Redis version. Example: resp3. Allowed values: resp2/resp3.
        :param sasl_password: [Optional]. Memcached (SASL) Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is MEMCACHED
        :param sasl_username: [Optional]. Memcached (SASL) Username to access the database. If omitted, the username will be set to a 'mc-' prefix followed by a random 5 character long alphanumeric. Can only be set if Database Protocol is MEMCACHED
        :param source_ip: [Optional]. List of source IP addresses or subnet masks. If specified, Redis clients will be able to connect to this database only from within the specified source IP addresses ranges. Example value: '['192.168.10.0/32', '192.168.12.0/24']'
        :param source_type: [Required for Import. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true']. Type of storage source from which to import the database file (RDB files) or data (Redis connection). List of options: [ http, redis, ftp, aws-s3, azure-blob-storage, google-blob-storage ].
        :param support_oss_cluster_api: [Optional]. Support Redis open-source (OSS) Cluster API. Default: 'false'
        :param throughput_measurement: [Optional. Input as JSON]. Throughput measurement method. Default: 25000 ops/sec
        :param use_external_endpoint_for_oss_cluster_api: [Optional]. Should use external endpoint for open-source (OSS) Cluster API. Can only be enabled if OSS Cluster API support is enabled'. Default: 'false'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e58e9ef6b1090f1a8892433c825c5e35e56954e8ad02838ea67ae7262c849e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatabaseProps(
            database_name=database_name,
            dataset_size_in_gb=dataset_size_in_gb,
            subscription_id=subscription_id,
            alerts=alerts,
            average_item_size_in_bytes=average_item_size_in_bytes,
            base_url=base_url,
            client_tls_certificates=client_tls_certificates,
            data_eviction_policy=data_eviction_policy,
            data_persistence=data_persistence,
            dry_run=dry_run,
            enable_default_user=enable_default_user,
            enable_tls=enable_tls,
            import_from_uri=import_from_uri,
            local_throughput_measurement=local_throughput_measurement,
            modules=modules,
            on_demand_backup=on_demand_backup,
            on_demand_import=on_demand_import,
            password=password,
            port=port,
            protocol=protocol,
            query_performance_factor=query_performance_factor,
            regex_rules=regex_rules,
            region_name=region_name,
            remote_backup=remote_backup,
            replica=replica,
            replication=replication,
            resp_version=resp_version,
            sasl_password=sasl_password,
            sasl_username=sasl_username,
            source_ip=source_ip,
            source_type=source_type,
            support_oss_cluster_api=support_oss_cluster_api,
            throughput_measurement=throughput_measurement,
            use_external_endpoint_for_oss_cluster_api=use_external_endpoint_for_oss_cluster_api,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDatabaseID")
    def attr_database_id(self) -> builtins.str:
        '''Attribute ``Redis::Cloud::Database.DatabaseID``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatabaseID"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDatabaseProps":
        '''Resource props.'''
        return typing.cast("CfnDatabaseProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/redis-cloud-database.CfnDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "dataset_size_in_gb": "datasetSizeInGb",
        "subscription_id": "subscriptionId",
        "alerts": "alerts",
        "average_item_size_in_bytes": "averageItemSizeInBytes",
        "base_url": "baseUrl",
        "client_tls_certificates": "clientTlsCertificates",
        "data_eviction_policy": "dataEvictionPolicy",
        "data_persistence": "dataPersistence",
        "dry_run": "dryRun",
        "enable_default_user": "enableDefaultUser",
        "enable_tls": "enableTls",
        "import_from_uri": "importFromUri",
        "local_throughput_measurement": "localThroughputMeasurement",
        "modules": "modules",
        "on_demand_backup": "onDemandBackup",
        "on_demand_import": "onDemandImport",
        "password": "password",
        "port": "port",
        "protocol": "protocol",
        "query_performance_factor": "queryPerformanceFactor",
        "regex_rules": "regexRules",
        "region_name": "regionName",
        "remote_backup": "remoteBackup",
        "replica": "replica",
        "replication": "replication",
        "resp_version": "respVersion",
        "sasl_password": "saslPassword",
        "sasl_username": "saslUsername",
        "source_ip": "sourceIp",
        "source_type": "sourceType",
        "support_oss_cluster_api": "supportOssClusterApi",
        "throughput_measurement": "throughputMeasurement",
        "use_external_endpoint_for_oss_cluster_api": "useExternalEndpointForOssClusterApi",
    },
)
class CfnDatabaseProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        dataset_size_in_gb: builtins.str,
        subscription_id: builtins.str,
        alerts: typing.Optional[builtins.str] = None,
        average_item_size_in_bytes: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        client_tls_certificates: typing.Optional[builtins.str] = None,
        data_eviction_policy: typing.Optional[builtins.str] = None,
        data_persistence: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.str] = None,
        enable_default_user: typing.Optional[builtins.str] = None,
        enable_tls: typing.Optional[builtins.str] = None,
        import_from_uri: typing.Optional[builtins.str] = None,
        local_throughput_measurement: typing.Optional[builtins.str] = None,
        modules: typing.Optional[builtins.str] = None,
        on_demand_backup: typing.Optional[builtins.str] = None,
        on_demand_import: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_performance_factor: typing.Optional[builtins.str] = None,
        regex_rules: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        remote_backup: typing.Optional[builtins.str] = None,
        replica: typing.Optional[builtins.str] = None,
        replication: typing.Optional[builtins.str] = None,
        resp_version: typing.Optional[builtins.str] = None,
        sasl_password: typing.Optional[builtins.str] = None,
        sasl_username: typing.Optional[builtins.str] = None,
        source_ip: typing.Optional[builtins.str] = None,
        source_type: typing.Optional[builtins.str] = None,
        support_oss_cluster_api: typing.Optional[builtins.str] = None,
        throughput_measurement: typing.Optional[builtins.str] = None,
        use_external_endpoint_for_oss_cluster_api: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CloudFormation template for Pro Database.

        :param database_name: [Required]. Database name (Database name must be up to 40 characters long, include only letters, digits, or hyphen ('-'), start with a letter, and end with a letter or digit). Example: Redis-database-example
        :param dataset_size_in_gb: [Required]. The maximum amount of data in the dataset for this specific database is in GB. You can not set both datasetSizeInGb and totalMemoryInGb. if 'replication' is true, the database's total memory will be twice as large as the datasetSizeInGb.if 'replication' is false, the database's total memory of the database will be the datasetSizeInGb value. Minimum: 0.1. ExclusiveMinimum: false. Example: 1
        :param subscription_id: [Required]. The Subscription ID under which the Database is created.
        :param alerts: [Optional. Input as JSON]. Redis database alerts.
        :param average_item_size_in_bytes: [Optional]. Relevant only to ram-and-flash clusters. Estimated average size (measured in bytes) of the items stored in the database. Default: 1000
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param client_tls_certificates: [Optional. Input as a JSON]. A list of TLS/SSL certificates (public keys) with new line characters replaced by . If specified, mTLS authentication (with enableTls not specified or set to true) will be required to authenticate user connections. If empty list is received, SSL certificates will be removed and mTLS will not be required (note that TLS connection may still apply, depending on the value of the enableTls property). Default: 'null'
        :param data_eviction_policy: [Optional]. Data items eviction method. List of options: [ allkeys-lru, allkeys-lfu, allkeys-random, volatile-lru, volatile-lfu, volatile-random, volatile-ttl, noeviction ]. Default: 'volatile-lru'
        :param data_persistence: [Optional]. Rate of database data persistence (in persistent storage). List of options: [ none, aof-every-1-second, aof-every-write, snapshot-every-1-hour, snapshot-every-6-hours, snapshot-every-12-hours ]. Example: none. Default: 'none'.
        :param dry_run: [Optional]. When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.
        :param enable_default_user: [Optional. Can only be modified upon Update request from a Cloud Formation stack]. When 'true', enables connecting to the database with the 'default' user. Default: 'true'. Can only be set if Database Protocol is REDIS
        :param enable_tls: [Optional]. When 'true', requires TLS authentication for all connections (mTLS with valid clientSslCertificate, regular TLS when the clientSslCertificate is not provided. Default: 'false'
        :param import_from_uri: [Required for Import. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true']. One or more URIs to source data files or Redis databases, as appropriate to specified source type (example: ['http://mydomain.com/redis-backup-file1', 'http://mydomain.com/redis-backup-file2'])
        :param local_throughput_measurement: [Optional. Input as JSON]. Throughput measurement for an active-active subscription
        :param modules: [Optional. Input as JSON]. Redis modules to be provisioned in the database.
        :param on_demand_backup: [Required to enable Backup. Can only be modified upon Update request from a Cloud Formation stack. Requires 'remoteBackup' to be active]. If 'true', creates a backup of the current database and disables all other parameters set for Update except for 'RegionName'. Default 'false'.
        :param on_demand_import: [Required to enable Import. Can only be modified upon Update request from a Cloud Formation stack]. If 'true', imports the previous created backup of a database and disables all other parameters set for Update except for 'SourceType' and 'ImportFromUri'. Default 'false'.
        :param password: [Optional]. Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is REDIS
        :param port: [Optional]. TCP port on which the database is available (10000-19999). Generated automatically if omitted. Example: 10000
        :param protocol: [Optional]. Database protocol: either 'redis' or 'memcached'. Default: 'redis'
        :param query_performance_factor: [Optional]. The query performance factor adds extra compute power specifically for search and query. For databases with search and query, you can increase your search queries per second by the selected factor. Example: 2x
        :param regex_rules: [Optional. Can only be modified upon Update request from a Cloud Formation stack]. Shard regex rules. Relevant only for a sharded database.
        :param region_name: [Optional. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandBackup' set to 'true']. Name of cloud provider region where the local database is located. When backing up an active-active database, backup is done separately for each local database at a specified region. Example for active-active database: 'us-east-1'. For single-region deployment, the value MUST be 'null'.
        :param remote_backup: [Optional. Input as JSON]. Database remote backup configuration
        :param replica: [Optional. Input as JSON]. Replica Of configuration
        :param replication: [Optional]. Databases replication. Default: 'true'
        :param resp_version: [Optional]. RESP version must be compatible with Redis version. Example: resp3. Allowed values: resp2/resp3.
        :param sasl_password: [Optional]. Memcached (SASL) Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is MEMCACHED
        :param sasl_username: [Optional]. Memcached (SASL) Username to access the database. If omitted, the username will be set to a 'mc-' prefix followed by a random 5 character long alphanumeric. Can only be set if Database Protocol is MEMCACHED
        :param source_ip: [Optional]. List of source IP addresses or subnet masks. If specified, Redis clients will be able to connect to this database only from within the specified source IP addresses ranges. Example value: '['192.168.10.0/32', '192.168.12.0/24']'
        :param source_type: [Required for Import. Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true']. Type of storage source from which to import the database file (RDB files) or data (Redis connection). List of options: [ http, redis, ftp, aws-s3, azure-blob-storage, google-blob-storage ].
        :param support_oss_cluster_api: [Optional]. Support Redis open-source (OSS) Cluster API. Default: 'false'
        :param throughput_measurement: [Optional. Input as JSON]. Throughput measurement method. Default: 25000 ops/sec
        :param use_external_endpoint_for_oss_cluster_api: [Optional]. Should use external endpoint for open-source (OSS) Cluster API. Can only be enabled if OSS Cluster API support is enabled'. Default: 'false'

        :schema: CfnDatabaseProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2800d2ee472767c3f1c86b7de1eda79efff70e39e3ea72adc91e86293ae2c43)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument dataset_size_in_gb", value=dataset_size_in_gb, expected_type=type_hints["dataset_size_in_gb"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument alerts", value=alerts, expected_type=type_hints["alerts"])
            check_type(argname="argument average_item_size_in_bytes", value=average_item_size_in_bytes, expected_type=type_hints["average_item_size_in_bytes"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument client_tls_certificates", value=client_tls_certificates, expected_type=type_hints["client_tls_certificates"])
            check_type(argname="argument data_eviction_policy", value=data_eviction_policy, expected_type=type_hints["data_eviction_policy"])
            check_type(argname="argument data_persistence", value=data_persistence, expected_type=type_hints["data_persistence"])
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument enable_default_user", value=enable_default_user, expected_type=type_hints["enable_default_user"])
            check_type(argname="argument enable_tls", value=enable_tls, expected_type=type_hints["enable_tls"])
            check_type(argname="argument import_from_uri", value=import_from_uri, expected_type=type_hints["import_from_uri"])
            check_type(argname="argument local_throughput_measurement", value=local_throughput_measurement, expected_type=type_hints["local_throughput_measurement"])
            check_type(argname="argument modules", value=modules, expected_type=type_hints["modules"])
            check_type(argname="argument on_demand_backup", value=on_demand_backup, expected_type=type_hints["on_demand_backup"])
            check_type(argname="argument on_demand_import", value=on_demand_import, expected_type=type_hints["on_demand_import"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query_performance_factor", value=query_performance_factor, expected_type=type_hints["query_performance_factor"])
            check_type(argname="argument regex_rules", value=regex_rules, expected_type=type_hints["regex_rules"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument remote_backup", value=remote_backup, expected_type=type_hints["remote_backup"])
            check_type(argname="argument replica", value=replica, expected_type=type_hints["replica"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument resp_version", value=resp_version, expected_type=type_hints["resp_version"])
            check_type(argname="argument sasl_password", value=sasl_password, expected_type=type_hints["sasl_password"])
            check_type(argname="argument sasl_username", value=sasl_username, expected_type=type_hints["sasl_username"])
            check_type(argname="argument source_ip", value=source_ip, expected_type=type_hints["source_ip"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument support_oss_cluster_api", value=support_oss_cluster_api, expected_type=type_hints["support_oss_cluster_api"])
            check_type(argname="argument throughput_measurement", value=throughput_measurement, expected_type=type_hints["throughput_measurement"])
            check_type(argname="argument use_external_endpoint_for_oss_cluster_api", value=use_external_endpoint_for_oss_cluster_api, expected_type=type_hints["use_external_endpoint_for_oss_cluster_api"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "dataset_size_in_gb": dataset_size_in_gb,
            "subscription_id": subscription_id,
        }
        if alerts is not None:
            self._values["alerts"] = alerts
        if average_item_size_in_bytes is not None:
            self._values["average_item_size_in_bytes"] = average_item_size_in_bytes
        if base_url is not None:
            self._values["base_url"] = base_url
        if client_tls_certificates is not None:
            self._values["client_tls_certificates"] = client_tls_certificates
        if data_eviction_policy is not None:
            self._values["data_eviction_policy"] = data_eviction_policy
        if data_persistence is not None:
            self._values["data_persistence"] = data_persistence
        if dry_run is not None:
            self._values["dry_run"] = dry_run
        if enable_default_user is not None:
            self._values["enable_default_user"] = enable_default_user
        if enable_tls is not None:
            self._values["enable_tls"] = enable_tls
        if import_from_uri is not None:
            self._values["import_from_uri"] = import_from_uri
        if local_throughput_measurement is not None:
            self._values["local_throughput_measurement"] = local_throughput_measurement
        if modules is not None:
            self._values["modules"] = modules
        if on_demand_backup is not None:
            self._values["on_demand_backup"] = on_demand_backup
        if on_demand_import is not None:
            self._values["on_demand_import"] = on_demand_import
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query_performance_factor is not None:
            self._values["query_performance_factor"] = query_performance_factor
        if regex_rules is not None:
            self._values["regex_rules"] = regex_rules
        if region_name is not None:
            self._values["region_name"] = region_name
        if remote_backup is not None:
            self._values["remote_backup"] = remote_backup
        if replica is not None:
            self._values["replica"] = replica
        if replication is not None:
            self._values["replication"] = replication
        if resp_version is not None:
            self._values["resp_version"] = resp_version
        if sasl_password is not None:
            self._values["sasl_password"] = sasl_password
        if sasl_username is not None:
            self._values["sasl_username"] = sasl_username
        if source_ip is not None:
            self._values["source_ip"] = source_ip
        if source_type is not None:
            self._values["source_type"] = source_type
        if support_oss_cluster_api is not None:
            self._values["support_oss_cluster_api"] = support_oss_cluster_api
        if throughput_measurement is not None:
            self._values["throughput_measurement"] = throughput_measurement
        if use_external_endpoint_for_oss_cluster_api is not None:
            self._values["use_external_endpoint_for_oss_cluster_api"] = use_external_endpoint_for_oss_cluster_api

    @builtins.property
    def database_name(self) -> builtins.str:
        '''[Required].

        Database name (Database name must be up to 40 characters long, include only letters, digits, or hyphen ('-'), start with a letter, and end with a letter or digit). Example: Redis-database-example

        :schema: CfnDatabaseProps#DatabaseName
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_size_in_gb(self) -> builtins.str:
        '''[Required].

        The maximum amount of data in the dataset for this specific database is in GB. You can not set both datasetSizeInGb and totalMemoryInGb. if 'replication' is true, the database's total memory will be twice as large as the datasetSizeInGb.if 'replication' is false, the database's total memory of the database will be the datasetSizeInGb value. Minimum: 0.1. ExclusiveMinimum: false. Example: 1

        :schema: CfnDatabaseProps#DatasetSizeInGb
        '''
        result = self._values.get("dataset_size_in_gb")
        assert result is not None, "Required property 'dataset_size_in_gb' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_id(self) -> builtins.str:
        '''[Required].

        The Subscription ID under which the Database is created.

        :schema: CfnDatabaseProps#SubscriptionID
        '''
        result = self._values.get("subscription_id")
        assert result is not None, "Required property 'subscription_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alerts(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Redis database alerts.

        :schema: CfnDatabaseProps#Alerts
        '''
        result = self._values.get("alerts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def average_item_size_in_bytes(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Relevant only to ram-and-flash clusters. Estimated average size (measured in bytes) of the items stored in the database. Default: 1000

        :schema: CfnDatabaseProps#AverageItemSizeInBytes
        '''
        result = self._values.get("average_item_size_in_bytes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''[Required].

        The Base URL where the API calls are sent.

        :schema: CfnDatabaseProps#BaseUrl
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_tls_certificates(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as a JSON]. A list of TLS/SSL certificates (public keys) with new line characters replaced by
        . If specified, mTLS authentication (with enableTls not specified or set to true) will be required to authenticate user connections. If empty list is received, SSL certificates will be removed and mTLS will not be required (note that TLS connection may still apply, depending on the value of the enableTls property). Default: 'null'

        :schema: CfnDatabaseProps#ClientTlsCertificates
        '''
        result = self._values.get("client_tls_certificates")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_eviction_policy(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Data items eviction method. List of options: [ allkeys-lru, allkeys-lfu, allkeys-random, volatile-lru, volatile-lfu, volatile-random, volatile-ttl, noeviction ]. Default: 'volatile-lru'

        :schema: CfnDatabaseProps#DataEvictionPolicy
        '''
        result = self._values.get("data_eviction_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_persistence(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Rate of database data persistence (in persistent storage). List of options: [ none, aof-every-1-second, aof-every-write, snapshot-every-1-hour, snapshot-every-6-hours, snapshot-every-12-hours ]. Example: none. Default: 'none'.

        :schema: CfnDatabaseProps#DataPersistence
        '''
        result = self._values.get("data_persistence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dry_run(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        When 'false': Creates a deployment plan and deploys it (creating any resources required by the plan). When 'true': creates a read-only deployment plan without any resource creation. Example: false. Default: 'false'.

        :schema: CfnDatabaseProps#DryRun
        '''
        result = self._values.get("dry_run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_default_user(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Can only be modified upon Update request from a Cloud Formation stack]. When 'true', enables connecting to the database with the 'default' user. Default: 'true'. Can only be set if Database Protocol is REDIS

        :schema: CfnDatabaseProps#EnableDefaultUser
        '''
        result = self._values.get("enable_default_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_tls(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        When 'true', requires TLS authentication for all connections (mTLS with valid clientSslCertificate, regular TLS when the clientSslCertificate is not provided. Default: 'false'

        :schema: CfnDatabaseProps#EnableTls
        '''
        result = self._values.get("enable_tls")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_from_uri(self) -> typing.Optional[builtins.str]:
        '''[Required for Import.

        Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true'].  One or more URIs to source data files or Redis databases, as appropriate to specified source type (example: ['http://mydomain.com/redis-backup-file1', 'http://mydomain.com/redis-backup-file2'])

        :schema: CfnDatabaseProps#ImportFromUri
        '''
        result = self._values.get("import_from_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_throughput_measurement(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Throughput measurement for an active-active subscription

        :schema: CfnDatabaseProps#LocalThroughputMeasurement
        '''
        result = self._values.get("local_throughput_measurement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modules(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Redis modules to be provisioned in the database.

        :schema: CfnDatabaseProps#Modules
        '''
        result = self._values.get("modules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_backup(self) -> typing.Optional[builtins.str]:
        '''[Required to enable Backup.

        Can only be modified upon Update request from a Cloud Formation stack. Requires 'remoteBackup' to be active]. If 'true', creates a backup of the current database and disables all other parameters set for Update except for 'RegionName'. Default 'false'.

        :schema: CfnDatabaseProps#OnDemandBackup
        '''
        result = self._values.get("on_demand_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_import(self) -> typing.Optional[builtins.str]:
        '''[Required to enable Import.

        Can only be modified upon Update request from a Cloud Formation stack]. If 'true', imports the previous created backup of a database and disables all other parameters set for Update except for 'SourceType' and 'ImportFromUri'. Default 'false'.

        :schema: CfnDatabaseProps#OnDemandImport
        '''
        result = self._values.get("on_demand_import")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is REDIS

        :schema: CfnDatabaseProps#Password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        TCP port on which the database is available (10000-19999). Generated automatically if omitted. Example: 10000

        :schema: CfnDatabaseProps#Port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Database protocol: either 'redis' or 'memcached'. Default: 'redis'

        :schema: CfnDatabaseProps#Protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_performance_factor(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        The query performance factor adds extra compute power specifically for search and query. For databases with search and query, you can increase your search queries per second by the selected factor. Example: 2x

        :schema: CfnDatabaseProps#QueryPerformanceFactor
        '''
        result = self._values.get("query_performance_factor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_rules(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Can only be modified upon Update request from a Cloud Formation stack]. Shard regex rules. Relevant only for a sharded database.

        :schema: CfnDatabaseProps#RegexRules
        '''
        result = self._values.get("regex_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandBackup' set to 'true']. Name of cloud provider region where the local database is located. When backing up an active-active database, backup is done separately for each local database at a specified region. Example for active-active database: 'us-east-1'. For single-region deployment, the value MUST be 'null'.

        :schema: CfnDatabaseProps#RegionName
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_backup(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Database remote backup configuration

        :schema: CfnDatabaseProps#RemoteBackup
        '''
        result = self._values.get("remote_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Replica Of configuration

        :schema: CfnDatabaseProps#Replica
        '''
        result = self._values.get("replica")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Databases replication. Default: 'true'

        :schema: CfnDatabaseProps#Replication
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resp_version(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        RESP version must be compatible with Redis version. Example: resp3. Allowed values: resp2/resp3.

        :schema: CfnDatabaseProps#RespVersion
        '''
        result = self._values.get("resp_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_password(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Memcached (SASL) Password to access the database. If omitted, a random 32 character long alphanumeric password will be automatically generated. Can only be set if Database Protocol is MEMCACHED

        :schema: CfnDatabaseProps#SaslPassword
        '''
        result = self._values.get("sasl_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_username(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Memcached (SASL) Username to access the database. If omitted, the username will be set to a 'mc-' prefix followed by a random 5 character long alphanumeric. Can only be set if Database Protocol is MEMCACHED

        :schema: CfnDatabaseProps#SaslUsername
        '''
        result = self._values.get("sasl_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ip(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        List of source IP addresses or subnet masks. If specified, Redis clients will be able to connect to this database only from within the specified source IP addresses ranges. Example value: '['192.168.10.0/32', '192.168.12.0/24']'

        :schema: CfnDatabaseProps#SourceIp
        '''
        result = self._values.get("source_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''[Required for Import.

        Can only be modified upon Update request from a Cloud Formation stack. Requires 'OnDemandImport' set to 'true']. Type of storage source from which to import the database file (RDB files) or data (Redis connection). List of options: [ http, redis, ftp, aws-s3, azure-blob-storage, google-blob-storage ].

        :schema: CfnDatabaseProps#SourceType
        '''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_oss_cluster_api(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Support Redis open-source (OSS) Cluster API. Default: 'false'

        :schema: CfnDatabaseProps#SupportOSSClusterApi
        '''
        result = self._values.get("support_oss_cluster_api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def throughput_measurement(self) -> typing.Optional[builtins.str]:
        '''[Optional.

        Input as JSON]. Throughput measurement method. Default: 25000 ops/sec

        :schema: CfnDatabaseProps#ThroughputMeasurement
        '''
        result = self._values.get("throughput_measurement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_external_endpoint_for_oss_cluster_api(
        self,
    ) -> typing.Optional[builtins.str]:
        '''[Optional].

        Should use external endpoint for open-source (OSS) Cluster API. Can only be enabled if OSS Cluster API support is enabled'. Default: 'false'

        :schema: CfnDatabaseProps#UseExternalEndpointForOSSClusterApi
        '''
        result = self._values.get("use_external_endpoint_for_oss_cluster_api")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDatabase",
    "CfnDatabaseProps",
]

publication.publish()

def _typecheckingstub__3e58e9ef6b1090f1a8892433c825c5e35e56954e8ad02838ea67ae7262c849e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    database_name: builtins.str,
    dataset_size_in_gb: builtins.str,
    subscription_id: builtins.str,
    alerts: typing.Optional[builtins.str] = None,
    average_item_size_in_bytes: typing.Optional[builtins.str] = None,
    base_url: typing.Optional[builtins.str] = None,
    client_tls_certificates: typing.Optional[builtins.str] = None,
    data_eviction_policy: typing.Optional[builtins.str] = None,
    data_persistence: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.str] = None,
    enable_default_user: typing.Optional[builtins.str] = None,
    enable_tls: typing.Optional[builtins.str] = None,
    import_from_uri: typing.Optional[builtins.str] = None,
    local_throughput_measurement: typing.Optional[builtins.str] = None,
    modules: typing.Optional[builtins.str] = None,
    on_demand_backup: typing.Optional[builtins.str] = None,
    on_demand_import: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query_performance_factor: typing.Optional[builtins.str] = None,
    regex_rules: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
    remote_backup: typing.Optional[builtins.str] = None,
    replica: typing.Optional[builtins.str] = None,
    replication: typing.Optional[builtins.str] = None,
    resp_version: typing.Optional[builtins.str] = None,
    sasl_password: typing.Optional[builtins.str] = None,
    sasl_username: typing.Optional[builtins.str] = None,
    source_ip: typing.Optional[builtins.str] = None,
    source_type: typing.Optional[builtins.str] = None,
    support_oss_cluster_api: typing.Optional[builtins.str] = None,
    throughput_measurement: typing.Optional[builtins.str] = None,
    use_external_endpoint_for_oss_cluster_api: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2800d2ee472767c3f1c86b7de1eda79efff70e39e3ea72adc91e86293ae2c43(
    *,
    database_name: builtins.str,
    dataset_size_in_gb: builtins.str,
    subscription_id: builtins.str,
    alerts: typing.Optional[builtins.str] = None,
    average_item_size_in_bytes: typing.Optional[builtins.str] = None,
    base_url: typing.Optional[builtins.str] = None,
    client_tls_certificates: typing.Optional[builtins.str] = None,
    data_eviction_policy: typing.Optional[builtins.str] = None,
    data_persistence: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.str] = None,
    enable_default_user: typing.Optional[builtins.str] = None,
    enable_tls: typing.Optional[builtins.str] = None,
    import_from_uri: typing.Optional[builtins.str] = None,
    local_throughput_measurement: typing.Optional[builtins.str] = None,
    modules: typing.Optional[builtins.str] = None,
    on_demand_backup: typing.Optional[builtins.str] = None,
    on_demand_import: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query_performance_factor: typing.Optional[builtins.str] = None,
    regex_rules: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
    remote_backup: typing.Optional[builtins.str] = None,
    replica: typing.Optional[builtins.str] = None,
    replication: typing.Optional[builtins.str] = None,
    resp_version: typing.Optional[builtins.str] = None,
    sasl_password: typing.Optional[builtins.str] = None,
    sasl_username: typing.Optional[builtins.str] = None,
    source_ip: typing.Optional[builtins.str] = None,
    source_type: typing.Optional[builtins.str] = None,
    support_oss_cluster_api: typing.Optional[builtins.str] = None,
    throughput_measurement: typing.Optional[builtins.str] = None,
    use_external_endpoint_for_oss_cluster_api: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
