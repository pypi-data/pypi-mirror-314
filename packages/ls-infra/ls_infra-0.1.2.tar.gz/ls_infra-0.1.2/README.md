# ls-infra

ls-infra is a framework for collecting cloud infrastructure information and transforming it into useful formats. Its extensible design allows users to easily add support   for new cloud providers and output formats.

## Core Concepts

ls-infra operates in three distinct stages:
1. Collection
Each collector must implement two methods to standardize how data is gathered:

fetch_raw_data: Retrieves raw data from the provider
serialize: Transforms the raw data into the standardized format required by the formatter

2. Pipeline Processing
Services that process the standardized data:

Run sequentially in the order defined
Can target specific provider data or all data using the target property
Transform, filter, or enrich the data

3. Formatting
Takes all processed data and generates the final output.
The formatter effectively dictates the required data format that collectors must serialize to.
Flow Definition
A flow is defined in YAML and describes the complete data processing pipeline:
yamlCopyversion: "1.0"
metadata:
  name: example_flow
  description: "Flow description"

collect:
  aws:
    service: aws_instance_collector
    enabled: true
    config:
      regions: ["us-east-1"]

  alicloud:
    service: alicloud_instance_collector
    enabled: true
    config:
      regions: ["cn-beijing"]

pipelines:
  - service: filter_terminated
    target: all
    config:
      states: ["terminated"]

  - service: filter_vpc
    target: aws
    config:
      vpc_ids: ["vpc-123"]

format:
  service: generate_inventory_ansible
  config:
    group_by: ["Environment"]
Flow Execution

Collection Phase (Parallel):

Collectors run in parallel
Each collector:

Fetches raw data
Transforms to standard format


Results are aggregated


Pipeline Phase (Sequential):

Services run in defined order
Each service processes based on target:

target: all - processes all data
target: provider - processes specific provider data




Format Phase:

Takes all processed data
Generates final output



Key Design Points

Collection Standardization:

Collectors handle both fetching and transformation
Raw provider data is immediately standardized
Format is dictated by formatter needs


Pipeline Flexibility:

Services can target all or specific data
Sequential processing ensures data consistency
Common operations can be applied to all data


Extensibility:

New collectors can be added for different providers
Pipeline services can be created for custom needs
Formatters can be developed for different outputs



Development Guidelines
Collectors
Must implement:

fetch_raw_data: Provider-specific retrieval
serialize: Standardization to formatter requirements

Pipeline Services
Should:

Accept standardized data format
Clearly define their target scope
Maintain data format compatibility

Formatters
Should:

Define their expected data format
Provide clear configuration options
Handle partial or failed data gracefully

CLI Usage
bashCopy# Run a flow
ls-infra run -f flow.yml

# Validate flow
ls-infra validate -f flow.yml

# List available services
ls-infra list-services

# Initialize new flow
ls-infra init
Environment Variables
The framework supports environment variable substitution:

${VAR_NAME}: Simple substitution
${VAR_NAME:-default}: With default value

Security Considerations

Credential Management:

Use environment variables for sensitive data
Support cloud provider credential chains
Never log sensitive information


Input Validation:

Validate all configuration
Sanitize input data
Verify service permissions



Error Handling

Collection Errors:

Failed collectors don't halt entire process
Proper error reporting
Retry mechanisms for transient failures


Pipeline Errors:

Configurable failure behavior (fail/warn)
Clear error messages
Data validation between services


Formatter Errors:

Validate input data
Clear error reporting
Partial output on failures when possible

## Future Plans

- [ ] Implement plugin system architecture
- [ ] Move default plugins to separate repository for better maintainability
- [ ] Allow third-party plugin development and integration
