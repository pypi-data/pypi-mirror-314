# Nimble-AWS

Nimble-AWS is a Python library designed to simplify and accelerate interactions with AWS services. It provides asynchronous adapters for efficient communication and includes middleware to streamline event handling and AWS Lambda integration. Whether you're working on a small project or building large-scale distributed systems, Nimble-AWS helps you focus on your application logic by abstracting the complexities of AWS.

## Features

- **Asynchronous Communication**: Execute AWS service operations asynchronously for high performance.
- **Simplified Abstractions**: Adapters that make interacting with AWS services intuitive and less error-prone.
- **Middleware Support**: Built-in middlewares for event-driven architectures and Lambda functions.
- **Optimized Performance**: Designed for minimal latency and high throughput.

## Installation

Install Nimble-AWS using pip:

```bash
pip install nimble-aws
```

## Example Usage

### S3 Adapter
The following example demonstrates how to use the S3 adapter to retrieve files from an S3 bucket asynchronously:

```python
from nimble_aws.adapter import S3


async def handler():
    region = "us-east-1"
    bucket = "example-bucket"
    paths = ["path/to/file1.json", "path/to/file2.json"]
    files = await S3().get_files(bucket=bucket, paths=paths, decode=True, region=region)
    print(files)


def lambda_handler():
    loop = asyncio.get_running_loop()
    loop.run_until_complete(handler())

```


## Environment Configuration

The library uses an `env` module to retrieve default configurations such as the AWS region. Ensure your AWS credentials and environment variables are properly configured before using Nimble-AWS.

## Contributing

We welcome contributions to Nimble-AWS! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

## License

Nimble-AWS is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Feedback

If you encounter any issues or have suggestions, please open an issue on our [GitHub repository](https://github.com/Doki-Labs/nimble).
