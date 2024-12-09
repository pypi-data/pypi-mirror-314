# Stonemill

Stonemill is a command-line tool designed to scaffold AWS infrastructure using Terraform. It streamlines the process of setting up various AWS services such as Lambda functions, EC2 servers, S3 buckets, DynamoDB tables, and more. The tool generates the necessary Terraform files to get your infrastructure up and running quickly.

## Installation

To install Stonemill, you will need to have Python installed on your system. You can install Stonemill using pip:

```sh
pip install stonemill
```

Alternatively, you can clone the repository and install it manually:

```sh
git clone https://github.com/mirror12k/stonemill.git
cd stonemill
pip install .
```

## Usage

Once installed, you can run Stonemill commands directly from the command line. For example, to create a basic Terraform configuration for an AWS infrastructure:

```sh
stonemill --infra-base mycompany myproject
```

To scaffold an AWS Lambda function:

```sh
stonemill --lambda-function my_lambda
```

For more detailed usage instructions, run:

```sh
stonemill --help
```

## Contributing

Contributions are welcome! If you have ideas for improvements or have found a bug, feel free to open an issue or submit a pull request. Please ensure that your code adheres to the project's style and conventions.

## License

Stonemill is open-sourced software licensed under the [MIT license](LICENSE).
