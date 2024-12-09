#!/usr/bin/env python3
import os
import stat
import sys
import re
import argparse


class Definition(object):
  def __init__(self, filepath, text, append=False, append_if_not_exist=False, ignore_missing=False, make_executable=False):
    super(Definition, self).__init__()
    self.filepath = filepath
    self.text = text
    self.append = append
    self.append_if_not_exist = append_if_not_exist
    self.ignore_missing = ignore_missing
    self.make_executable = make_executable
  def but_replace(self, key, replacement):
    return Definition(filepath=self.filepath,
        append=self.append,
        append_if_not_exist=self.append_if_not_exist,
        ignore_missing=self.ignore_missing,
        make_executable=self.make_executable,
        text=self.text.replace(key, replacement))
  def and_append(self, addendum):
    return Definition(filepath=self.filepath,
        append=self.append,
        append_if_not_exist=self.append_if_not_exist,
        ignore_missing=self.ignore_missing,
        make_executable=self.make_executable,
        text=self.text + addendum)
  def substitute_filepath(self, **args):
    t = self.filepath
    for k in args:
      t = t.replace('{{'+k+'}}', args[k])
    return t
  def substitute_text(self, **args):
    t = self.text
    for k in args:
      t = t.replace('{{'+k+'}}', args[k])
    return t
  def check_file(self, **args):
    filepath = self.substitute_filepath(**args)
    if self.append:
      if not self.ignore_missing and not os.path.exists(filepath):
        raise Exception('append file missing: ' + filepath)
    elif self.append_if_not_exist:
      pass
    else:
      if os.path.exists(filepath):
        raise Exception('write file already exists: ' + filepath)
  def write_file(self, **args):
    filepath = self.substitute_filepath(**args)
    text = self.substitute_text(**args)

    if self.append:
      print('[+] appending to', filepath)
      with open(filepath, 'a') as f:
        f.write(text)

    elif self.append_if_not_exist:
      if not os.path.exists(os.path.dirname(filepath)):
        print('[+] making directory', os.path.dirname(filepath))
        os.makedirs(os.path.dirname(filepath))
      if os.path.exists(filepath):
        with open(filepath, 'r') as f:
          existing_text = f.read()
      else:
        existing_text = ''
      if text not in existing_text:
        print('[+] appending to', filepath)
        with open(filepath, 'a') as f:
          f.write(text)
      else:
        # print('[i] skipping', filepath, 'because it already contains the text:[[', text, ']] as you can see here: [[[[', existing_text, ']]]]')
        print('[i] skipping', filepath, 'because it already contains the text fragment')

    else:
      if not os.path.exists(os.path.dirname(filepath)):
        print('[+] making directory', os.path.dirname(filepath))
        os.makedirs(os.path.dirname(filepath))
      print('[+] writing to', filepath)
      with open(filepath, 'w') as f:
        f.write(text)

    if self.make_executable:
      self.add_executable_permission(filepath)

  def add_executable_permission(self, filepath):
    if not os.path.exists(filepath):
      raise Exception(f"The file {filepath} does not exist.")
    
    current_permissions = stat.S_IMODE(os.lstat(filepath).st_mode)
    new_permissions = current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(filepath, new_permissions)
    # print(f"[+] chmod +x {filepath}")

class ReplaceFileDefinition(Definition):
  def check_file(self, **args):
    filepath = self.substitute_filepath(**args)
    if not os.path.exists(filepath) and not self.append_if_not_exist:
      raise Exception('replace file is missing: ' + filepath)
  def write_file(self, **args):
    filepath = self.substitute_filepath(**args)
    text = self.substitute_text(**args)

    if not os.path.exists(filepath) and self.append_if_not_exist:
      print('[+] making directory', os.path.dirname(filepath))
      os.makedirs(os.path.dirname(filepath))
    print('[+] writing to', filepath)
    with open(filepath, 'w') as f:
      f.write(text)

    if self.make_executable:
      self.add_executable_permission(filepath)


class TemplateDefinition(object):
  def __init__(self, message, arguments, definitions, post_message, unformatted_post_message=None, fixed_args={}):
    super(TemplateDefinition, self).__init__()
    self.message = message
    self.arguments = arguments
    self.definitions = definitions
    self.post_message = post_message
    self.unformatted_post_message = unformatted_post_message
    self.fixed_args = fixed_args

  def parse_arguments(self, **template_args):
    parsed_args = { **self.fixed_args }
    for k in self.arguments:
      if template_args.get(k) is None:
        raise Exception('error: missing argument: ' + k)
      if not re.match(self.arguments[k], template_args[k]):
        raise Exception('error: invalid ' + k + ' arugment: ' + template_args[k] + ' (doesnt match required regex: /' + self.arguments[k] + '/)')
      parsed_args[k] = template_args[k]
    return parsed_args
        
  def mill_template(self, template_args):
    name = self.message.format(**template_args)
    print('[[preping {}...]]'.format(name))
    for d in self.definitions:
      d.check_file(**template_args)
    print('[[milling {}...]]'.format(name))
    for d in self.definitions:
      d.write_file(**template_args)
    print('[[done {}!]]'.format(name))
    print(self.post_message.format(**template_args))
    if self.unformatted_post_message is not None:
      print(self.unformatted_post_message)


base_terraform_main = Definition("infrastructure/main.tf", text='''provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Stage = "${var.stage}"
      Project = "${local.infragroup_fullname}"
    }
  }
}

terraform {
  backend "local" {}
}

variable "company_name" { default = "{{company_name}}" }
variable "group_name" { default = "{{infra_name}}" }
variable "stage" { default = "beta" }
variable "root_domain" { default = "example.org" }

locals {
  metrics_path = "${var.company_name}/${local.infragroup_fullname}"
  infragroup_fullname = "${var.group_name}-${var.stage}"
  domain_name = (var.stage == "prod" ? var.root_domain : "${var.stage}.${var.root_domain}")
  alarm_emails = []
  # alarm_emails = ["example@example.org"]
}

output "domain_name" { value = local.domain_name }

# resource group to track active infrastructure resources
resource "aws_resourcegroups_group" "infra_resource_group" {
name = "${local.infragroup_fullname}-resourcegroup"

  resource_query {
    query = <<JSON
{
  "ResourceTypeFilters": ["AWS::AllSupported"],
  "TagFilters": [
    {
      "Key": "Project",
      "Values": ["${local.infragroup_fullname}"]
    }
  ]
}
JSON
  }
}

# dashboard for monitoring the overall system. add widgets as necessary
resource "aws_cloudwatch_dashboard" "service_monitoring_dashboard" {
  dashboard_name = "${local.infragroup_fullname}-dashboard"
  dashboard_body = <<EOF
{
  "widgets": []
}
EOF
}

# sns alarm topics for configuring metric alarms
resource "aws_sns_topic" "alarm_topic" {
  name = "${local.infragroup_fullname}-alarm_topic"
}
resource "aws_sns_topic_subscription" "alarm_email_target" {
  count     = length(local.alarm_emails)
  topic_arn = aws_sns_topic.alarm_topic.arn
  protocol  = "email"
  endpoint  = local.alarm_emails[count.index]
}
''')

base_backend_beta_config = Definition("./infrastructure/config/backend-config.beta.hcl", text='''''')
base_backend_prod_config = Definition("./infrastructure/config/backend-config.prod.hcl", text='''''')
base_test_sh = Definition("./scripts/test.sh", make_executable=True, text='''#!/bin/bash
''')

base_makefile = Definition("./Makefile", text='''

deploy:
\t./infrastructure/tools/deploy.sh -deploy
destroy:
\t./infrastructure/tools/deploy.sh -destroy

prod_deploy:
\t./infrastructure/tools/deploy.sh -deploy -prod
prod_destroy:
\t./infrastructure/tools/deploy.sh -destroy -prod

output:
\tterraform -chdir=infrastructure output && read _

clean:
\trm -rf build .keys infrastructure/.terraform infrastructure/terraform.tfstate* src/*/modules src/*/node_modules src/*/dist

build:

test:

''')

base_dockerfile = Definition("./docker/Dockerfile", text='''FROM ubuntu:22.04

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gnupg software-properties-common curl \\
  && apt-get install -y nano jq zip make python3-venv python3-pip openssh-client \\
  && apt autoclean && apt autoremove && apt clean \\
  && pip install coverage unittest-xml-reporting

# install terraform, awscli, ssm-plugin
COPY install-tooling.sh .
RUN ./install-tooling.sh

# optional: install development utilities
RUN pip install stonemill weasel-make llm-shell

# safety measure to drop privileges to lowly user
RUN useradd -ms /bin/bash runuser
USER runuser

RUN echo 'source <(weasel --bash-autocompletions-source)' >> ~/.bashrc

CMD bash

''')

base_docker_run = Definition("./docker/run", make_executable=True, text='''#!/bin/bash
(set -o allexport && source 'docker/.env' && set +o allexport && bash docker/aws-authenticate.sh)
IMAGE_TAG=$(echo "local-${PWD##*/}" | tr '[:upper:]' '[:lower:]')
docker image inspect "$IMAGE_TAG" > /dev/null || docker build docker -t "$IMAGE_TAG"
docker run --rm --cap-drop=all \\
  -v "$PWD:/app" \\
  -v "$PWD/docker:/app/docker:ro" \\
  --env-file ".env.temp" \\
  -it $(docker build -q docker -t "$IMAGE_TAG") $@
''')

base_envfile = Definition("./docker/.env", text='''''')
base_aws_authenticate = Definition("./docker/aws-authenticate.sh", make_executable=True, text='''#!/bin/bash
set -e
echo '' > .env.temp

if [[ -z $(aws configure get aws_access_key_id) ]]; then
    echo "no aws credentials found. skipping configuration..."
    exit
fi

AWS_USERNAME=$(aws sts get-caller-identity | jq -r '.Arn | split("/")[1]')
AWS_MFA_DEVICE_ARN=$(aws iam list-mfa-devices --user-name "$AWS_USERNAME" | jq -r '.MFADevices[0].SerialNumber')

if [[ "$AWS_MFA_DEVICE_ARN" != "null" ]]; then
    echo -n "please enter your mfa token for device $AWS_MFA_DEVICE_ARN: "

    MFA_TOKEN=""
    while IFS= read -r -s -n 1 c; do
        if [[ $c == $'\\0' ]]; then
            break
        fi
        MFA_TOKEN="${MFA_TOKEN}$c"
        echo -n "*"
    done
    echo

    AWS_CREDS=$(aws sts get-session-token --serial-number "$AWS_MFA_DEVICE_ARN" --token-code "$MFA_TOKEN" --duration-seconds 7200)
    AWS_ACCESS_KEY_ID=$(echo "$AWS_CREDS" | jq -r ".Credentials.AccessKeyId")
    AWS_SECRET_ACCESS_KEY=$(echo "$AWS_CREDS" | jq -r ".Credentials.SecretAccessKey")
    AWS_SESSION_TOKEN=$(echo "$AWS_CREDS" | jq -r ".Credentials.SessionToken")
    echo "aws configured with 2-hour temporary credentials: $AWS_ACCESS_KEY_ID"
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env.temp
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env.temp
    echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" >> .env.temp

    exit
else
    echo "no mfa device found, configuring with fixed credentials"
    echo "  warning: you will not be able to call any IAM apis with these credentials!"

    AWS_CREDS=$(aws sts get-session-token --duration-seconds 7200)
    AWS_ACCESS_KEY_ID=$(echo "$AWS_CREDS" | jq -r ".Credentials.AccessKeyId")
    AWS_SECRET_ACCESS_KEY=$(echo "$AWS_CREDS" | jq -r ".Credentials.SecretAccessKey")
    AWS_SESSION_TOKEN=$(echo "$AWS_CREDS" | jq -r ".Credentials.SessionToken")
    echo "aws configured with 2-hour temporary credentials: $AWS_ACCESS_KEY_ID"
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env.temp
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env.temp
    echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" >> .env.temp
    exit
fi
''')
base_install_tooling = Definition("./docker/install-tooling.sh", make_executable=True, text='''#!/bin/bash
set -e -x

function amd_terraform_install() {
    curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
    apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    apt-get update
    apt-get install -y terraform
}
function arm_terraform_install() {
    curl https://releases.hashicorp.com/terraform/1.10.1/terraform_1.10.1_linux_arm64.zip -o "/tmp/terraform.zip"
    unzip "/tmp/terraform.zip" -d /tmp
    mv "/tmp/terraform" "/usr/local/bin/terraform"
    rm "/tmp/terraform.zip"
}

function amd_awscli_install() {
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    unzip "/tmp/awscliv2.zip" -d "/tmp"
    /tmp/aws/install
    rm -rf "/tmp/awscliv2.zip" "/tmp/aws"
}
function arm_awscli_install() {
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "/tmp/awscliv2.zip"
    unzip "/tmp/awscliv2.zip" -d "/tmp"
    /tmp/aws/install
    rm -rf "/tmp/awscliv2.zip" "/tmp/aws"
}

function amd_ssm_plugin_install() {
    curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
    dpkg -i "/tmp/session-manager-plugin.deb"
    rm "/tmp/session-manager-plugin.deb"
}
function arm_ssm_plugin_install() {
    curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
    dpkg -i "/tmp/session-manager-plugin.deb"
    rm "/tmp/session-manager-plugin.deb"
}

arch=$(uname -m)
case "$arch" in
    x86_64 | i686 | i386 )
        amd_terraform_install
        amd_awscli_install
        amd_ssm_plugin_install
        ;;
    arm64 | aarch64 )
        arm_terraform_install
        arm_awscli_install
        arm_ssm_plugin_install
        ;;
    * )
        echo "Unsupported CPU architecture: $arch"
        exit 1
        ;;
esac
''')
base_create_keys = Definition("./infrastructure/tools/create-keys.sh", make_executable=True, text='''#!/bin/bash
cd "$(dirname "$0")" && cd ../..

KEYPATH=$1
if [[ ! -f ".keys/$KEYPATH" ]]; then
  mkdir -p .keys/
  ssh-keygen -m PEM -t rsa -b 2048 -f ".keys/$KEYPATH" -q -N ""
fi
''')
base_trigger_codebuild = Definition("./infrastructure/tools/trigger-codebuild.sh", make_executable=True, text='''#!/bin/bash
set -e
cd "$(dirname "$0")" && cd ../..

CODEBUILD_PROJECT_NAME="$1"
aws codebuild start-build --project-name "$CODEBUILD_PROJECT_NAME" --region us-east-1 > /dev/null

CODEBUILD_PROJECT_NAMES="$CODEBUILD_PROJECT_NAME"
COUNT_PROJECT="$CODEBUILD_PROJECT_NAMES"

# get the number of completed builds
function get_codebuild_project_status {
  for project_name in $CODEBUILD_PROJECT_NAMES
  do
    # get project id from name
    project_id=$(aws codebuild list-builds-for-project --project-name "$project_name" --region us-east-1 | jq -r '.ids[0]')
    # get build status
    aws codebuild batch-get-builds --ids "$project_id" --region us-east-1 | jq -r '.builds[].phases[] | select(.phaseType=="COMPLETED") | .phaseType'
  done
}

# get the number of completed builds
function did_codebuild_project_fail {
  for project_name in $CODEBUILD_PROJECT_NAMES
  do
    # get project id from name
    project_id=$(aws codebuild list-builds-for-project --project-name "$project_name" --region us-east-1 | jq -r '.ids[0]')
    # get build status
    aws codebuild batch-get-builds --ids "$project_id" --region us-east-1 | jq -r '.builds[].phases[] | select(.phaseStatus=="FAILED") | .phaseType'
  done
}

# get the number of completed builds
function get_codebuild_project_fail_message {
  for project_name in $CODEBUILD_PROJECT_NAMES
  do
    # get project id from name
    project_id=$(aws codebuild list-builds-for-project --project-name "$project_name" --region us-east-1 | jq -r '.ids[0]')
    # get build status
    aws codebuild batch-get-builds --ids "$project_id" --region us-east-1 | jq -r '.builds[].phases[] | select(.phaseStatus=="FAILED") | .contexts[0].message'
  done
}

# check if deployment is finished
function codebuild_project_await_status {
  while [[ ${#PROJECT_STATUS[@]} != ${#COUNT_PROJECT[@]} ]]
  do
    # echo "completed: ${#PROJECT_STATUS[@]}/${#COUNT_PROJECT[@]}"
    sleep 10
    PROJECT_STATUS=($(get_codebuild_project_status))
  done


}

# aws logs tail "$CODEBUILD_PROJECT_OUTPUT" --follow &
codebuild_project_await_status
# pkill -P $$

FAILED_PROJECTS=($(did_codebuild_project_fail))

if [[ ${#FAILED_PROJECTS[@]} != 0 ]]; then
  FAIL_MESSAGES=$(get_codebuild_project_fail_message)
  echo "got project failures: $FAIL_MESSAGES"
  exit 1
fi
''')
base_deploy = Definition("./infrastructure/tools/deploy.sh", make_executable=True, text='''#!/bin/bash
set -e
cd "$(dirname "$0")" && cd ../..

ACTION=$1
STAGE="beta" # Default stage

usage() {
    echo "Usage: $0 -deploy [-prod]"
    echo "       $0 -autodeploy [-prod]"
    echo "       $0 -destroy [-prod]"
    echo "Options:"
    echo "       -deploy         Deploy the infrastructure"
    echo "       -autodeploy     Deploy the infrastructure without manual confirmation"
    echo "       -destroy        Destroy the infrastructure"
    echo "       -prod           Set the stage to production"
    exit 1
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        -deploy)
            ACTION="deploy"
            shift
            ;;
        -autodeploy)
            ACTION="autodeploy"
            shift
            ;;
        -destroy)
            ACTION="destroy"
            shift
            ;;
        -prod)
            STAGE="prod"
            shift
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "$ACTION" ]; then
    echo "Error: No action specified."
    usage
fi

cd infrastructure

echo "[i] running init"
terraform init "-backend-config=config/backend-config.$STAGE.hcl"

case "$ACTION" in
    deploy)
        echo "[i] running deployment!"
        terraform apply -var "stage=${STAGE}"
        ;;
    autodeploy)
        echo "[i] running auto deployment!"
        terraform apply -auto-approve -var "stage=${STAGE}"
        ;;
    destroy)
        echo "[i] running destroy!!!"
        terraform destroy -var "stage=${STAGE}"
        ;;
esac

echo "[i] done!"
''')
base_server_state = Definition("./scripts/server-state.sh", make_executable=True, text='''#!/bin/bash
set -e
cd "$(dirname "$0")" && cd ..

INSTANCE_ID=$(cat "infrastructure/terraform.tfstate" | jq -r ".outputs.instance_id.value")
echo "INSTANCE_ID: $INSTANCE_ID"

ACTION=$1
if [[ "$ACTION" == "stop" ]]; then
  echo "[i] running stop..."
  aws ec2 stop-instances --region us-east-1 --instance-ids "$INSTANCE_ID"
elif [[ "$ACTION" == "start" ]]; then
  echo "[i] running start"
  aws ec2 start-instances --region us-east-1 --instance-ids "$INSTANCE_ID"
fi

echo "[i] done!"
''')
base_ssh_into = Definition("./scripts/ssh-into.sh", make_executable=True, text='''#!/bin/sh
cd "$(dirname "$0")" && cd ..

INSTANCE_NAME=$1

if [ "$INSTANCE_NAME" = "" ]; then
    echo "[!] missing instance name argument!"
    exit
fi

echo "[+] getting instance ip from infrastructure..."
INSTANCE_ID=$(cat "infrastructure/terraform.tfstate" | jq -r ".outputs.${INSTANCE_NAME}_instance_id.value")

echo "INSTANCE_ID: $INSTANCE_ID"
INSTANCE_IP=$(aws ec2 describe-instances --region "us-east-1" \\
  --filters "Name=instance-state-name,Values=running" "Name=instance-id,Values=$INSTANCE_ID" \\
  --query 'Reservations[*].Instances[*].[PublicIpAddress]' \\
  --output text)
echo "INSTANCE_IP: $INSTANCE_IP"

SSH_COMMAND="ssh -i .keys/${INSTANCE_NAME}_key ubuntu@${INSTANCE_IP} -o StrictHostKeyChecking=no"
echo "[+] executing ssh: $SSH_COMMAND"
sh -c "$SSH_COMMAND"
''')
base_ssm_into = Definition("./scripts/ssm-into.sh", make_executable=True, text='''#!/bin/sh
cd "$(dirname "$0")" && cd ..

INSTANCE_NAME=$1

if [ "$INSTANCE_NAME" = "" ]; then echo "[!] missing instance name argument!"; exit; fi

echo "[i] getting instance id from infrastructure..."
INSTANCE_ID=$(terraform -chdir=infrastructure output -json | jq -r ".${INSTANCE_NAME}_instance_id.value")
if [ "$INSTANCE_ID" = "null" ]; then echo "[!] instance id not found for name '$INSTANCE_NAME'!"; exit; fi

echo "[+] logging in to ssm: $INSTANCE_ID"
aws ssm start-session --target "$INSTANCE_ID" --reason "manual login" --region us-east-1 --document-name AWS-StartInteractiveCommand --parameters command="cd /app && sudo su ubuntu"
''')

base_gitignore = Definition("./.gitignore", text='''build
.*
!.github/
!.gitignore
terraform.tfstate*
src/*/modules/*
src/*/node_modules/*
src/*/dist/*
src/**/__pycache__/*
''')

base_lambda_module = Definition("infrastructure/main.tf", append=True, text='''
variable "{{lambda_name}}_build_path" { default = "../build/{{lambda_name}}.zip" }

module "{{lambda_name}}" {
  source = "./{{lambda_name}}"

  metrics_path = local.metrics_path
  infragroup_fullname = local.infragroup_fullname
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn
  lambda_build_path = var.{{lambda_name}}_build_path
}
output "{{lambda_name}}_arn" { value = module.{{lambda_name}}.lambda_arn }
output "{{lambda_name}}_name" { value = module.{{lambda_name}}.lambda_name }
''')

base_lambda_makefile = Definition("./Makefile", append=True, text='''
build: build_{{lambda_name}}
build_{{lambda_name}}:
\t-mkdir build
\tcd src/{{lambda_name}} && bash ./build.sh
''')

base_lambda_definition = Definition("infrastructure/{{lambda_name}}/{{lambda_name}}.tf", text='''
variable "metrics_path" { type = string }
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "lambda_build_path" { type = string }

locals {
  fullname = "${var.infragroup_fullname}-{{lambda_name}}"
  metrics_group = "${var.metrics_path}/{{lambda_name}}"
}

resource "aws_lambda_function" "lambda_function" {
  function_name = "${local.fullname}"
  publish = true

  runtime = "python3.8"
  handler = "main.lambda_handler"

  filename = var.lambda_build_path
  source_code_hash = filebase64sha256(var.lambda_build_path)

  role = aws_iam_role.lambda_execution_role.arn

  memory_size = 512
  timeout = 30

  environment {
    variables = {
      INFRAGROUP_FULLNAME = var.infragroup_fullname
      METRICS_GROUP = local.metrics_group
    }
  }
}

resource "aws_lambda_function_event_invoke_config" "lambda_function_invoke_config" {
  function_name = aws_lambda_function.lambda_function.function_name
  maximum_retry_attempts = 0
}

resource "aws_cloudwatch_log_group" "lambda_function_cloudwatch" {
  name = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = 90
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "${local.fullname}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "${local.fullname}-policy"
  path        = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:CreateLogGroup"
      ]
      Resource = "*"
    }, {
      Effect = "Allow"
      Action = "cloudwatch:PutMetricData"
      Resource = "*"
      Condition = {
        StringEquals = {
          "cloudwatch:namespace" = local.metrics_group
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# # crash alarm, will alarm when the lambda crashes recently
# resource "aws_cloudwatch_metric_alarm" "crash_alarm" {
#   alarm_name = "${local.fullname}-crash_alarm"
#   comparison_operator = "GreaterThanOrEqualToThreshold"
#   evaluation_periods = "1"
#   metric_name = "lambda-crash"
#   namespace = local.metrics_group
#   period = "300"
#   statistic = "Sum"
#   threshold = "1"
#   alarm_actions = [var.sns_alarm_topic_arn]
# }

output "lambda_arn" { value = aws_lambda_function.lambda_function.arn }
output "lambda_name" { value = aws_lambda_function.lambda_function.function_name }

output "monitor_widget_json" {
  value = <<EOF
  {
    "height": 6,
    "width": 6,
    "type": "metric",
    "properties": {
      "metrics": [
        [ "${local.metrics_group}", "lambda-success", { "color": "#98df8a", "label": "lambda-success" } ],
        [ ".", "lambda-error", { "color": "#ffbb78" } ],
        [ ".", "lambda-crash", { "color": "#ff9896" } ]
      ],
      "view": "timeSeries",
      "stacked": true,
      "region": "us-east-1",
      "stat": "Sum",
      "period": 300,
      "title": "{{lambda_name}} metrics"
    }
  }
EOF
}

''')

base_lambda_main = Definition("src/{{lambda_name}}/main.py", text='''import sys
sys.path.append('modules')
import os
import json
import boto3
import traceback

import lambda_routing
import routes



# aws api clients
cloudwatch_client = boto3.client('cloudwatch')
# env variables passed in from infrastructure
metrics_group = os.environ.get('METRICS_GROUP')



def lambda_handler(event, context):
  print('[i] handling event:', event)
  try:
    # perform routing
    res = route_request(event)
    print('[r] response:', res)
    if res.get('success') is not None and res['success']:
      send_metric('lambda-success')
    else:
      send_metric('lambda-error')
    return res
  except Exception as e:
    print('[!] exception thrown:', e, traceback.format_exception(None, e, e.__traceback__))
    # track crash metrics
    send_metric('lambda-crash')
    res = { 'success': False, 'error': 'server-side error' }
    print('[r] response:', res)
    return res

def send_metric(name):
  cloudwatch_client.put_metric_data(Namespace=metrics_group,
    MetricData = [{
      'MetricName': name,
      'Unit': 'Count',
      'Value': 1
    }])

def route_sqs_request(event):
  results = []
  for record in event['Records']:
    results.append(route_request(record))
  return results

def route_request(event):
  # get the path parameter as the action
  action = event.get('rawPath', '')
  if not action:
    print('[!] missing action')
    return {'success': False, 'error': 'invalid request'}

  # get the json data from the body
  try:
    data = json.loads(str(event['body']))
  except ValueError as e:
    print('[!] error parsing json body:', e)
    return { 'success': False, 'error': 'invalid request' }

  # try to route it
  route_fun = lambda_routing.get_route(action)
  if route_fun is None:
    print('[!] invalid action: ', action)
    return { 'success': False, 'error': 'invalid request' }
  
  # handle the routing
  print('[i] executing route: ' + action)
  return route_fun(data, event)
''')

base_lambda_lib = Definition("src/{{lambda_name}}/lambda_routing.py", text='''all_lambda_routes = {}
all_lambda_functions = {}
all_lambda_route_arguments = {}
all_lambda_route_arguments_by_wrapper = {}
def lambda_route(route):
  def lambda_route_lambda_route(f):
    def wrapper(*args, **kwargs):
      return f(*args, **kwargs)
    all_lambda_routes[route] = wrapper
    all_lambda_functions[wrapper] = route
    if f in all_lambda_route_arguments_by_wrapper:
      all_lambda_route_arguments[route] = all_lambda_route_arguments_by_wrapper[f]
    return wrapper
  return lambda_route_lambda_route

def authenticated_lambda_route(route, authentication_fun):
  def lambda_route_authenticated_lambda_route(f):
    def wrapper(data, *args, **kwargs):
      account = authentication_fun(data)
      if account is None:
        print('[-] authentication failed')
        return { 'success': False, 'error': 'unauthenticated' }
      else:
        return f(data, account, *args, **kwargs)
    all_lambda_routes[route] = wrapper
    all_lambda_functions[wrapper] = route
    if f in all_lambda_route_arguments_by_wrapper:
      all_lambda_route_arguments[route] = all_lambda_route_arguments_by_wrapper[f]
    return wrapper
  return lambda_route_authenticated_lambda_route

def with_arguments(*required_data_args):
  def lambda_route_with_arguments(f):
    def wrapper(data, *args, **kwargs):
      for required_arg in required_data_args:
        if required_arg not in data:
          print('[-] argument missing:', required_arg)
          return { 'success': False, 'error': 'missing argument' }
      return f(data, *args, **kwargs)
    all_lambda_route_arguments_by_wrapper[wrapper] = required_data_args
    return wrapper
  return lambda_route_with_arguments

def get_route(route):
  return all_lambda_routes.get(route)
''')

base_lambda_routes = Definition("src/{{lambda_name}}/routes.py", text='''from lambda_routing import *

@lambda_route('/{{lambda_name}}/hello')
@with_arguments('msg')
def hello(data, event):
  if data.get('msg') is None:
    print('[-] missing message')
    return { 'success': True, 'msg': 'hello world!' }
  else:
    return { 'success': True, 'msg': data['msg'] }
''')

base_lambda_build = Definition("src/{{lambda_name}}/build.sh", text='''#!/bin/bash
python3 -m venv my_venv
source my_venv/bin/activate
pip install --upgrade --ignore-installed -r requirements.txt
deactivate

rm -rf modules __pycache__ xml-test-reports .coverage
mkdir modules
# ls -la my_venv/lib/*/site-packages/
rm -rf my_venv/lib/*/site-packages/*.dist-info \\
  my_venv/lib/*/site-packages/setuptools \\
  my_venv/lib/*/site-packages/pip \\
  my_venv/lib/*/site-packages/*/__pycache__
cp -rf my_venv/lib/*/site-packages/* modules
rm -rf my_venv/

zip -r ../../build/{{lambda_name}}.zip . -x build.sh -x "*__pycache__*"
''')

base_lambda_requirements = Definition("src/{{lambda_name}}/requirements.txt", text='''
boto3
botocore
pyjwt
''')
base_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_FUNCTION_NAME=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{lambda_name}}_name.value')
echo "invoking lambda: $INVOKE_FUNCTION_NAME"
aws lambda invoke --region us-east-1 \\
    --function-name $INVOKE_FUNCTION_NAME \\
    --payload $(echo '{"rawPath":"/{{lambda_name}}/hello","body":"{\\"msg\\":\\"yes\\"}"}' | base64 -w 0) \\
    /dev/stdout
''')

sqs_lambda_main = base_lambda_main.but_replace('''res = route_request(event)
    print('[r] response:', res)
    if res.get('success') is not None and res['success']:
      send_metric('lambda-success')
    else:
      send_metric('lambda-error')
    return res''', '''results = route_sqs_request(event)
    print('[r] response:', results)
    # track metrics
    for res in results:
      if res.get('success') is not None and res['success']:
        send_metric('lambda-success')
      else:
        send_metric('lambda-error')

    return results''')
sqs_lambda_module = base_lambda_module.and_append('''
output "{{lambda_name}}_sqs_queue_url" { value = module.{{lambda_name}}.sqs_queue_url }
''')
sqs_lambda_definition = base_lambda_definition.but_replace('''{
    Effect = "Allow"
    Action = "cloudwatch:PutMetricData"
    Resource = "*"
    Condition = {
      StringEquals = {
        "cloudwatch:namespace" = local.metrics_group
      }
    }
  }]''','''{
    Effect = "Allow"
    Action = "cloudwatch:PutMetricData"
    Resource = "*"
    Condition = {
      StringEquals = {
        "cloudwatch:namespace" = local.metrics_group
      }
    }
  }, {
    Effect = "Allow",
    Action = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ],
    Resource = aws_sqs_queue.input_queue.arn
  }]''').and_append('''
resource "aws_sqs_queue" "input_queue" {
  name        = "${local.fullname}-input_queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.input_dlq.arn
    maxReceiveCount     = 4
  })
  visibility_timeout_seconds = 300
}

resource "aws_sqs_queue" "input_dlq" {
  name        = "${local.fullname}-input_dlq"
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_sqs_queue.input_queue.arn
  function_name    = aws_lambda_function.lambda_function.arn
  batch_size = 1
}


output "sqs_queue_arn" { value = aws_sqs_queue.input_queue.arn }
output "sqs_queue_url" { value = aws_sqs_queue.input_queue.url }
''')
sqs_lambda_test = Definition("scripts/test.sh", append=True, text='''
SQS_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{lambda_name}}_sqs_queue_url.value')
aws sqs send-message --region us-east-1 --queue-url "$SQS_URL" --message-body "{\"action\":\"/{{lambda_name}}/hello\"}"
''')

api_lambda_module = base_lambda_module.and_append('''
output "{{lambda_name}}_api_url" { value = module.{{lambda_name}}.api_url }
''')
api_lambda_definition = base_lambda_definition.and_append('''
resource "aws_apigatewayv2_api" "gateway_api" {
  name          = "${local.fullname}-gateway_api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type", "authorization"]
    max_age = 300
  }

  # change this to true when you create a cloudfront distribution for the api
  disable_execute_api_endpoint = false
}

resource "aws_apigatewayv2_stage" "gateway_stage" {
  api_id = aws_apigatewayv2_api.gateway_api.id

  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.apigw_log_group.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }
}

resource "aws_apigatewayv2_integration" "apigw_integration" {
  api_id = aws_apigatewayv2_api.gateway_api.id

  integration_uri    = aws_lambda_function.lambda_function.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "apigw_route" {
  api_id = aws_apigatewayv2_api.gateway_api.id

  route_key = "POST /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.apigw_integration.id}"
}

resource "aws_cloudwatch_log_group" "apigw_log_group" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.gateway_api.name}"
  retention_in_days = 90
}

resource "aws_lambda_permission" "apigw_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.gateway_api.execution_arn}/*/*"
}

# # domain mapping to enable a domain name
# variable "domain_acm_cert_arn" { type = string }
# resource "aws_apigatewayv2_domain_name" "apigw_domain" {
#   domain_name = "api.${local.domain_name}"
#   domain_name_configuration {
#     certificate_arn = var.domain_acm_cert_arn
#     endpoint_type   = "REGIONAL"
#     security_policy = "TLS_1_2"
#   }
# }

# resource "aws_apigatewayv2_api_mapping" "apigw_domain_mapping" {
#   api_id      = aws_apigatewayv2_api.gateway_api.id
#   domain_name = aws_apigatewayv2_domain_name.apigw_domain.id
#   stage  = aws_apigatewayv2_stage.gateway_stage.id
# }

# output "api_url" { value = "https://${aws_apigatewayv2_domain_name.apigw_domain.id}/" }
output "api_url" { value = "${aws_apigatewayv2_stage.gateway_stage.invoke_url}" }
''')
api_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{lambda_name}}_api_url.value')
echo "invoking api: $INVOKE_URL"
curl -X POST "$INVOKE_URL/{{lambda_name}}/hello" -H 'content-type: application/json' -d '{"msg":"working as intended"}'
''')
api_lambda_unit_test = Definition("src/{{lambda_name}}/unit_test.py", text='''#!/usr/bin/env python3
import sys
sys.path.append('modules')
import os
import json
import unittest
import xmlrunner
import coverage

cov = coverage.Coverage()
cov.start()

print('[i] injecting testing env variables...')
os.environ['API_AUTHORIZATION_SECRET_KEY'] = 'test_key'
os.environ['API_DOMAIN_NAME'] = 'test.local'

print('[i] importing runtime modules...')
import routes
print('[+] import successful')

class LambdaUnitTests(unittest.TestCase):
  def test_hello(self):
    res = routes.hello({'msg': 'asdf'}, {})
    self.assertEqual(res, {'success': True, 'msg': 'asdf'})
    res = routes.hello({}, {})
    self.assertFalse(res['success'])
    self.assertEqual(res, {'success': False, 'error': 'missing argument'})

class _LambdaCoverageTest(unittest.TestCase):
  def test_coverage(self):
    cov.stop()
    cov.json_report(['routes.py'], outfile='/tmp/cov.json')
    with open('/tmp/cov.json', 'r') as f:
      data = json.loads(f.read())
    print('[i] total coverage percent:', data['totals']['percent_covered'])
    self.assertGreaterEqual(data['totals']['percent_covered'], 75.0)

unittest.main(testRunner=xmlrunner.XMLTestRunner(output='xml-test-reports'))
''')


graphql_lambda_makefile = base_lambda_makefile.and_append('''
test: test_{{lambda_name}}
test_{{lambda_name}}:
\tcd ./src/{{lambda_name}} && python3 ./unit_test.py
''')

graphql_lambda_main = Definition("src/{{lambda_name}}/main.py", text='''import sys
sys.path.append('modules')
import os
import json
import boto3
import traceback

from schema import schema


# aws api clients
cloudwatch_client = boto3.client('cloudwatch')
# env variables passed in from infrastructure
metrics_group = os.environ.get('METRICS_GROUP')

def internal_lambda_handler(event, context):
  # get the json data from the body
  try:
    body = json.loads(str(event['body']))
  except ValueError as e:
    print('[!] error parsing json body:', e)
    return { 'success': False, 'error': 'invalid request' }
  # check the query
  if body.get('query') is None:
    print('[!] missing query')
    return { 'success': False, 'error': 'invalid request' }

  # execute schema
  result = schema.execute(body['query'],
      variables=body.get('variables', {}),
      context={ 'authorization': event.get('headers', {}).get('authorization') })
  # print('[r] graphql result:', result.data)
  return result.formatted

def lambda_handler(event, context):
  print('[i] handling event:', event)
  try:
    # perform routing
    res = internal_lambda_handler(event, context)
    print('[r] response:', res)
    if res.get('errors') is None:
      send_metric('lambda-success')
    else:
      send_metric('lambda-error')
    return res
  except Exception as e:
    print('[!] exception thrown:', e, traceback.format_exception(None, e, e.__traceback__))
    # track crash metrics
    send_metric('lambda-crash')
    res = { 'data': None, 'errors': 'server-side error' }
    print('[r] response:', res)
    return res

def send_metric(name):
  cloudwatch_client.put_metric_data(Namespace=metrics_group,
    MetricData = [{
      'MetricName': name,
      'Unit': 'Count',
      'Value': 1
    }])
''')

graphql_lambda_authorization = Definition("src/{{lambda_name}}/authorization.py", text='''import sys
sys.path.append('modules')
import os
import json
import traceback
import hashlib
import hmac
import datetime

import jwt

api_authorization_secret_key = os.environ.get('API_AUTHORIZATION_SECRET_KEY')
api_domain_name = os.environ.get('API_DOMAIN_NAME')



def secure_random_hex(length):
  return os.urandom(length).hex()

def sign_jwt_authorization(id, role):
  print('[i] request to sign jwt token from:', id, 'for:', api_domain_name)
  jwt_token = jwt.encode({
      'id': id,
      'role': role,
      'iss': api_domain_name,
      'aud': api_domain_name,
      'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60 * 60 * 24),
    }, api_authorization_secret_key, algorithm='HS256')
  print('[+] signed jwt token:', jwt_token)

  return jwt_token

def verify_jwt_authorization(token):
  print('[i] got jwt token:', token)
  try:
    jwt_payload = jwt.decode(
        token,
        api_authorization_secret_key,
        issuer=api_domain_name,
        audience=api_domain_name,
        algorithms=["HS256"])
    print('[+] got jwt payload:', jwt_payload)

  except Exception as e:
    print('[!] exception thrown during jwt decoding:', e, traceback.format_exception(None, e, e.__traceback__))
    return None

  return {
    'id': jwt_payload['id'],
    'role': jwt_payload['role']
  }

def hash_new_password(password):
  salt = os.urandom(16).hex()
  pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 1000).hex()
  return salt + '/' + pw_hash

def verify_password(password, previous):
  if previous is None or previous == '':
    return False
  salt, old_hash = previous.split('/', 1)
  pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 1000).hex()
  return pw_hash == old_hash

def authorized(authorized_role):
  def inner_authorized(f):
    def wrapper(root, info, *args, **kwargs):
      account = verify_jwt_authorization(info.context.get('authorization'))
      if account is None:
        raise Exception('unauthorized')
      elif account['role'] is None or account['role'] != authorized_role:
        raise Exception('unauthorized')
      else:
        info.context['parsed_authorization'] = account
        return f(root, info, *args, **kwargs)
    return wrapper
  return inner_authorized
''')

graphql_lambda_schema = Definition("src/{{lambda_name}}/schema.py", text='''import sys
sys.path.append('modules')

from graphene import ObjectType, String, Schema
from authorization import authorized, sign_jwt_authorization

class Query(ObjectType):
  hello = String(name=String(default_value="stranger"))
  login = String(email=String(), password=String())
  verify = String()

  def resolve_hello(root, info, name):
    return f'Hello {name}!'
  def resolve_login(root, info, email, password):
    return sign_jwt_authorization(email, 'user')
  @authorized('user')
  def resolve_verify(root, info):
    return 'verified'

schema = Schema(query=Query)
''')

graphql_lambda_unit_test = Definition("src/{{lambda_name}}/unit_test.py", text='''#!/usr/bin/env python3
import sys
sys.path.append('modules')
import os
import json
import unittest
import xmlrunner
import coverage

cov = coverage.Coverage()
cov.start()

print('[i] injecting testing env variables...')
os.environ['API_AUTHORIZATION_SECRET_KEY'] = 'test_key'
os.environ['API_DOMAIN_NAME'] = 'test.local'

print('[i] importing runtime modules...')
from schema import schema
# from models import *
print('[+] import successful')

class LambdaUnitTests(unittest.TestCase):
  def test_hello(self):
    res = schema.execute('query { hello }').formatted
    self.assertEqual(res['data']['hello'], 'Hello stranger!')
  def test_hello_name(self):
    res = schema.execute('query { hello(name:"world") }').formatted
    self.assertEqual(res['data']['hello'], 'Hello world!')
  def test_error(self):
    res = schema.execute('query { missing_action }').formatted
    self.assertIsNone(res['data'])
    self.assertIsNotNone(res['errors'])
  def test_login(self):
    res = schema.execute('{ login(email:"asdf@example.com", password:"asdfasdf") }').formatted
    self.assertIsNotNone(res['data']['login'])
  def test_verify(self):
    res = schema.execute('{ login(email:"asdf@example.com", password:"asdfasdf") }').formatted
    self.assertIsNotNone(res['data']['login'])
    login_token = res['data']['login']
    res = schema.execute('{ verify }', context={ 'authorization': login_token }).formatted
    self.assertEqual(res['data']['verify'], 'verified')

class _LambdaCoverageTest(unittest.TestCase):
  def test_coverage(self):
    cov.stop()
    cov.json_report(['schema.py'], outfile='/tmp/cov.json')
    with open('/tmp/cov.json', 'r') as f:
      data = json.loads(f.read())
    print('[i] total coverage percent:', data['totals']['percent_covered'])
    self.assertGreaterEqual(data['totals']['percent_covered'], 100.0)

unittest.main(testRunner=xmlrunner.XMLTestRunner(output='xml-test-reports'))
''')

graphql_lambda_requirements = Definition("src/{{lambda_name}}/requirements.txt", text='''
boto3
botocore
pyjwt
graphene
''')
graphql_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{lambda_name}}_api_url.value')
echo "invoking api: $INVOKE_URL"
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -d '{"query":"{ hello login(email:\"asdf\", password:\"asdf\") }"}'
''')

usermanager_lambda_schema = Definition("src/{{lambda_name}}/schema.py", append=True, text='''import sys
sys.path.append('modules')

import uuid
import datetime
from graphene import ObjectType, Field, String, Schema, List
from authorization import *
from models import *

class Userdata(ObjectType):
  id = String()
  email = String()
  created_at = String()

class Query(ObjectType):
  current_user = Field(Userdata)

  @authorized('customer')
  def resolve_current_user(root, info):
    try:
      print('[i] querying user by id:', info.context['parsed_authorization']['id'])
      user = UserModel.get(info.context['parsed_authorization']['id'])
      return Userdata(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
      )
    except UserModel.DoesNotExist:
      print('[!] user not found!')
      return None

class Mutation(ObjectType):
  login_user = String(email=String(), password=String())
  add_user = String(email=String())
  register_user = String(email=String(), reset_token=String(), password=String())
  forgot_password = String(email=String())

  def resolve_login_user(root, info, email, password):
    print('[!] querying users for email:', email)
    users = [ u for u in UserModel.email_index.query(email) ]
    if len(users) == 0:
      print('[!] user doesnt exist')
      return None
    user = UserModel.get(users[0].id)
    print('[+] got user:', user)
    if user.account_state != 'activated':
      print('[!] user not activated:', user.account_state)
      return None

    if verify_password(password, user.password_hash):
      print('[+] password verified, logging in user with role:', user.role)
      user.last_login_at = datetime.datetime.now(tz=datetime.timezone.utc)
      user.save()
      print('[+] user saved, returning token')
      return sign_jwt_authorization(user.id, user.role)
    else:
      print('[!] incorrect password, rejecting')
      return None
  def resolve_add_user(root, info, email):
    print('[!] querying users for email:', email)
    users = [ u for u in UserModel.email_index.query(email) ]
    if len(users) > 0:
      print('[!] user already exists:', users)
      return None
    else:
      new_id = str(uuid.uuid4())
      reset_token = secure_random_hex(64)
      print('[i] adding user:', new_id)
      user = UserModel(new_id,
          email=email,
          password_hash='',
          reset_token=reset_token,
          role='customer',
          account_state='awaiting_activation',
          created_at=datetime.datetime.now(tz=datetime.timezone.utc))
      user.save()
      print('[+] user added:', user)
      return 'ok'
  def resolve_register_user(root, info, email, reset_token, password):
    print('[!] querying users for email:', email)
    users = [ u for u in UserModel.email_index.query(email) ]
    if len(users) == 0:
      print('[!] user doesnt exist')
      return None
    user = UserModel.get(users[0].id)
    print('[+] got user:', user)
    if user.reset_token is None or user.reset_token == '':
      print('[!] reset token already consumed')
      return None
    if user.reset_token != reset_token:
      print('[!] reset token doesnt match:', reset_token)
      return None
    if len(password) < 10:
      print('[!] password must be at least 10 characters')
      return None

    print('[i] registering user:', user.id)
    user.password_hash = hash_new_password(password)
    user.reset_token = ''
    user.account_state = 'activated'
    user.save()
    print('[+] user registered successfully')
    return 'ok'
  def resolve_forgot_password(root, info, email):
    print('[!] querying users for email:', email)
    users = [ u for u in UserModel.email_index.query(email) ]
    if len(users) == 0:
      print('[!] user doesnt exist')
      return None
    user = UserModel.get(users[0].id)
    print('[+] got user:', user)

    if user.account_state != 'activated' and user.account_state != 'awaiting_activation':
      print('[!] user account_state incorrect:', user.account_state)
      return None

    user.reset_token = secure_random_hex(64)
    user.save()
    print('[+] user reset_token updated')
    return 'ok'

schema = Schema(query=Query, mutation=Mutation)
''')
usermanager_lambda_models = Definition("src/{{lambda_name}}/models.py", append=True, ignore_missing=True, text='''import os
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

class UserModelIndex(GlobalSecondaryIndex):
  class Meta:
    index_name = os.environ.get('USERS_TABLE_INDEX')
    projection = KeysOnlyProjection()
  email = UnicodeAttribute(hash_key=True)

class UserModel(Model):
  class Meta:
    table_name = os.environ.get('USERS_TABLE_ID')
  id = UnicodeAttribute(hash_key=True)
  email = UnicodeAttribute()
  email_index = UserModelIndex()
  password_hash = UnicodeAttribute()
  reset_token = UnicodeAttribute()
  role = UnicodeAttribute()
  account_state = UnicodeAttribute()
  created_at = UTCDateTimeAttribute()
  last_login_at = UTCDateTimeAttribute(null=True)
''')
usermanager_lambda_requirements = Definition("src/{{lambda_name}}/requirements.txt", append_if_not_exist=True, text='''graphene
pynamodb
''')
usermanager_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.usermanager_lambda_api_url.value')
echo "invoking api: $INVOKE_URL"
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ addUser(email:\"qwer\", password:\"asdf\") }"}'
# curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ login(email:\"qwer\", password:\"asdf\") }"}'
# token="YOUR_TOKEN_HERE"
# curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ verify }"}'
''')
usermanager_lambda_unit_test = Definition("src/{{lambda_name}}/test.py", append=True, ignore_missing=True, text='''#!/usr/bin/env python3
import sys
sys.path.append('modules')
import os
import json

print('[i] loading environment from terraform state...')
with open('../infrastructure/terraform.tfstate', 'r') as f:
  data = json.loads(f.read())

for k in data['outputs']:
  # print(k, data['outputs'][k]['value'])
  os.environ[k.upper()] = data['outputs'][k]['value']
print('[+] loaded {} values from state!'.format(len(data['outputs'])))

os.environ['API_DOMAIN_NAME'] = 'test.local'
os.environ['API_AUTHORIZATION_SECRET_KEY'] = 'TESTKEY'
print('[+] added test secret key and domain name')


print('[i] importing runtime modules...')
from schema import schema
from models import *
print('[+] import successful')

email = "hello11@world.com"
password = "asdfasdfasdf"

print('[---------] testing addUser')
res = schema.execute('mutation { addUser(email:"' + email + '") }', context={ 'authorization': None }).formatted
print(res)

user_indexed = [ u for u in UserModel.email_index.query(email) ][0]
user = UserModel.get(user_indexed.id)
print("found own user:", user)

print('[---------] testing registerUser')
res = schema.execute('mutation { registerUser(email:"' + email + '", resetToken:"' + user.reset_token + '", password:"' + password + '") }', context={ 'authorization': None }).formatted
print(res)

print('[---------] testing loginUser')
res = schema.execute('mutation { loginUser(email:"' + email + '", password:"' + password + '") }', context={ 'authorization': None }).formatted
print(res)
auth_token = res['data']['loginUser']

print('[---------] testing currentUser')
res = schema.execute('{ currentUser { id createdAt email } }', context={ 'authorization': auth_token }).formatted
print(res)

print('[---------] testing forgotPassword')
res = schema.execute('mutation { forgotPassword(email:"' + email + '") }', context={ 'authorization': None }).formatted
print(res)
user = UserModel.get(user_indexed.id)
print("new reset token:", user.reset_token)

''')


crud_lambda_authorization = Definition("src/{{lambda_name}}/authorization.py", append_if_not_exist=True, ignore_missing=True, text='''
def get_model_by_class(object_model, id, owner_id):
  print('[i] getting ', object_model ,':', id, 'for', owner_id)
  try:
    model = object_model.get(id)
  except object_model.DoesNotExist:
    print('[!] model not found')
    return None
  if model.owner_id == owner_id:
    print('[+] model found')
    return model
  else:
    print('[!] model owner incorrect')
    return None

def get_model_by_owner(object_model, owner_id):
  print('[i] getting ', object_model ,'by owner:', owner_id)
  objs = [ o for o in object_model.index.query(owner_id) ]
  if len(objs) < 1:
    print('[!] model not found')
    return None
  try:
    model = object_model.get(objs[0].id)
    print('[+] model found')
  except object_model.DoesNotExist:
    print('[!] model not found')
    return None
  if model.owner_id != owner_id:
    print('[!] model owner incorrect')
    return None
  return model

def with_model(object_model):
  def inner_with_object(f):
    def wrapper(root, info, id, *args, **kwargs):
      model = get_model_by_class(object_model, id, info.context['parsed_authorization']['id'])
      if model is None:
        return None
      else:
        return f(root, info, model, *args, **kwargs)
    return wrapper
  return inner_with_object

def with_singleton_model(object_model):
  def inner_with_object(f):
    def wrapper(root, info, *args, **kwargs):
      model = get_model_by_owner(object_model, info.context['parsed_authorization']['id'])
      if model is None:
        return None
      else:
        return f(root, info, model, *args, **kwargs)
    return wrapper
  return inner_with_object
''')

crud_lambda_models = Definition("src/{{lambda_name}}/models.py", append=True, ignore_missing=True, text='''import os
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

class {{table_name}}_ModelIndex(GlobalSecondaryIndex):
  class Meta:
    index_name = os.environ.get('{{table_name}}_INDEX')
    projection = KeysOnlyProjection()
  owner_id = UnicodeAttribute(hash_key=True)

class {{table_name}}_Model(Model):
  class Meta:
    table_name = os.environ.get('{{table_name}}_TABLE')
  id = UnicodeAttribute(hash_key=True)
  owner_id = UnicodeAttribute()
  content = UnicodeAttribute()
''')

crud_lambda_schema = Definition("src/{{lambda_name}}/schema.py", append=True, text='''import sys
sys.path.append('modules')
import uuid
import datetime

from graphene import ObjectType, Field, String, Schema, List
from authorization import *
from models import *

class Query(ObjectType):
  list_{{table_name}}s = List(String)
  {{table_name}} = String(id=String())

  @authorized('customer')
  def resolve_list_{{table_name}}s(root, info):
    results = []
    print("[i] querying dashboards for user:", info.context['parsed_authorization']['id'])
    for {{table_name}} in {{table_name}}_Model.index.query(info.context['parsed_authorization']['id']):
      results.append({{table_name}}.id)
    print("[+] got dashboards:", results)
    return results
  @authorized('customer')
  @with_model({{table_name}}_Model)
  def resolve_{{table_name}}(root, info, {{table_name}}):
    return {{table_name}}.content

class Mutation(ObjectType):
  add_{{table_name}} = String(content=String())
  update_{{table_name}} = String(id=String(), content=String())
  delete_{{table_name}} = String(id=String())

  @authorized('customer')
  def resolve_add_{{table_name}}(root, info, content):
    new_id = str(uuid.uuid4())
    print('[i] adding {{table_name}}:', new_id, 'for user:', info.context['parsed_authorization']['id'])
    {{table_name}} = {{table_name}}_Model(new_id, owner_id=info.context['parsed_authorization']['id'], content=content)
    {{table_name}}.save()
    print('[+] {{table_name}} added:', {{table_name}})
    return new_id
  @authorized('customer')
  @with_model({{table_name}}_Model)
  def resolve_update_{{table_name}}(root, info, {{table_name}}, content):
    print("[i] updating {{table_name}}:", {{table_name}}.id)
    {{table_name}}.content = content
    {{table_name}}.save()
    return 'ok'
  @authorized('customer')
  @with_model({{table_name}}_Model)
  def resolve_delete_{{table_name}}(root, info, {{table_name}}):
    print("[i] deleting {{table_name}}:", {{table_name}}.id)
    {{table_name}}.delete()
    return 'ok'

schema = Schema(query=Query, mutation=Mutation)
''')
crud_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.usermanager_lambda_api_url.value')
echo "invoking api: $INVOKE_URL"
token=$(curl -s -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ login(email:\"asdf\", password:\"asdf\") }"}' | jq -r '.data.login')
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ addUserDashboard(content:\"hello\") }"}'
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ listUserDashboards }"}'
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ getUserDashboard(id:\"13254f58-fa90-406b-bbf9-e1b6291efee1\") }"}'
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ updateUserDashboard(id:\"13254f58-fa90-406b-bbf9-e1b6291efee1\", content:\"zxcvzxcv\") }"}'
curl -X POST "$INVOKE_URL" -H 'content-type: application/json' -H "authorization: $token" -d '{"query":"{ deleteUserDashboard(id:\"13254f58-fa90-406b-bbf9-e1b6291efee1\") }"}'
''')
crud_lambda_unit_test = Definition("src/{{lambda_name}}/test.py", append=True, ignore_missing=True, text='''#!/usr/bin/env python3
import sys
sys.path.append('modules')
import os
import json

print('[i] loading environment from terraform state...')
with open('../infrastructure/terraform.tfstate', 'r') as f:
  data = json.loads(f.read())

for k in data['outputs']:
  # print(k, data['outputs'][k]['value'])
  os.environ[k.upper()] = data['outputs'][k]['value']
print('[+] loaded {} values from state!'.format(len(data['outputs'])))

os.environ['API_DOMAIN_NAME'] = 'test.local'
os.environ['API_AUTHORIZATION_SECRET_KEY'] = 'TESTKEY'
print('[+] added test secret key and domain name')


print('[i] importing runtime modules...')
from schema import schema
from models import *
print('[+] import successful')

print('[---------] testing add{{table_name}}')
res = schema.execute('mutation { add{{table_name}}(content:"hello world") }', context={ 'authorization': auth_token }).formatted
print(res)

print('[---------] testing list{{table_name}}s')
res = schema.execute('{ list{{table_name}}s }', context={ 'authorization': auth_token }).formatted
print(res)
{{table_name}}_id = res['data']['list{{table_name}}s'][0]

print('[---------] testing {{table_name}}')
res = schema.execute('{ {{table_name}}(id:"'+{{table_name}}_id+'") }', context={ 'authorization': auth_token }).formatted
print(res)

print('[---------] testing delete{{table_name}}')
res = schema.execute('mutation { delete{{table_name}}(id:"'+{{table_name}}_id+'") }', context={ 'authorization': auth_token }).formatted
print(res)
''')

singleton_crud_lambda_schema = Definition("src/{{lambda_name}}/schema.py", append=True, text='''import sys
sys.path.append('modules')
import uuid
import datetime
from graphene import ObjectType, Field, String, Schema, List
from authorization import *
from models import *

class Query(ObjectType):
  {{table_name}} = String()

  @authorized('customer')
  @with_singleton_model({{table_name}}_Model)
  def resolve_{{table_name}}(root, info, {{table_name}}):
    return {{table_name}}.content

class Mutation(ObjectType):
  add_{{table_name}} = String(content=String())
  update_{{table_name}} = String(content=String())

  @authorized('customer')
  def resolve_add_{{table_name}}(root, info, content):
    existing_model = get_model_by_owner({{table_name}}_Model, info.context['parsed_authorization']['id'])
    if existing_model is not None:
      print('[!] singleton already exists:', existing_model)
      raise Exception('already exists')
    new_id = str(uuid.uuid4())
    print('[i] adding {{table_name}}:', new_id, 'for user:', info.context['parsed_authorization']['id'])
    {{table_name}} = {{table_name}}_Model(new_id, owner_id=info.context['parsed_authorization']['id'], content=content)
    {{table_name}}.save()
    print('[+] {{table_name}} added:', {{table_name}})
    return new_id
  @authorized('customer')
  @with_singleton_model({{table_name}}_Model)
  def resolve_update_{{table_name}}(root, info, {{table_name}}, content):
    print("[i] updating {{table_name}}:", {{table_name}}.id)
    {{table_name}}.content = content
    {{table_name}}.save()
    return 'ok'
''')
singleton_crud_lambda_unit_test = Definition("src/{{lambda_name}}/test.py", append=True, ignore_missing=True, text='''#!/usr/bin/env python3
import sys
sys.path.append('modules')
import os
import json

print('[i] loading environment from terraform state...')
with open('../infrastructure/terraform.tfstate', 'r') as f:
  data = json.loads(f.read())

for k in data['outputs']:
  # print(k, data['outputs'][k]['value'])
  os.environ[k.upper()] = data['outputs'][k]['value']
print('[+] loaded {} values from state!'.format(len(data['outputs'])))

os.environ['API_DOMAIN_NAME'] = 'test.local'
os.environ['API_AUTHORIZATION_SECRET_KEY'] = 'TESTKEY'
print('[+] added test secret key and domain name')


print('[i] importing runtime modules...')
from schema import schema
from models import *
print('[+] import successful')

print('[---------] testing add{{table_name}}')
res = schema.execute('mutation { add{{table_name}}(content:"asdf") }', context={ 'authorization': auth_token }).formatted
print(res)

print('[---------] testing {{table_name}}')
res = schema.execute('{ {{table_name}} }', context={ 'authorization': auth_token }).formatted
print(res)

print('[---------] testing update{{table_name}}')
res = schema.execute('mutation { update{{table_name}}(content:"hello world!") }', context={ 'authorization': auth_token }).formatted
print(res)
''')


authn_lambda_definition = base_lambda_definition.but_replace('''METRICS_GROUP = local.metrics_group''', '''METRICS_GROUP = local.metrics_group
      API_AUTHORIZATION_SECRET_KEY = random_id.api_authorization_random_secret.hex
      API_DOMAIN_NAME = var.domain_name''').but_replace('''resource "aws_lambda_function" "lambda_function" {''', '''
resource "random_id" "api_authorization_random_secret" { byte_length = 64 }
resource "aws_lambda_function" "lambda_function" {''').but_replace('''variable "lambda_build_path" { type = string }''', '''variable "lambda_build_path" { type = string }
variable "domain_name" { type = string }''')
authn_lambda_module = base_lambda_module.but_replace('''lambda_build_path = var.{{lambda_name}}_build_path''', '''lambda_build_path = var.{{lambda_name}}_build_path
  domain_name = local.domain_name
''')
authn_lambda_routes = Definition("src/{{lambda_name}}/routes.py", text='''from lambda_routing import *
from authorization import *

@lambda_route('/v1/authn_lambda/sign_token')
@with_arguments('id')
def sign_token(data, event):
  print('debug:', data['id'])
  return { 'success': True, 'token': sign_jwt_authorization(data['id'], 'user') }

@lambda_route('/v1/authn_lambda/verify_token')
@with_arguments('token')
def verify_token(data, event):
  jwt_data = verify_jwt_authorization(data['token'])
  if jwt_data is not None:
    return { 'success': True, 'data': jwt_data }
  else:
    return { 'success': False, 'error': 'invalid token' }
''')
authn_lambda_test = Definition("scripts/test.sh", append=True, text='''
INVOKE_FUNCTION_NAME=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{lambda_name}}_name.value')
aws lambda invoke --region us-east-1 \\
    --function-name "$INVOKE_FUNCTION_NAME" \\
    --payload $(echo '{"rawPath":"/v1/authn_lambda/sign_token","body":"{\\"id\\":\\"asdf\\"}"}' | base64 -w 0) \\
    output.json
TOKEN=$(cat output.json | jq -r '.token')
aws lambda invoke --region us-east-1 \\
    --function-name "$INVOKE_FUNCTION_NAME" \\
    --payload $(echo '{"rawPath":"/v1/authn_lambda/verify_token","body":"{\\"token\\":\\"'$TOKEN'\\"}"}' | base64 -w 0) \\
    /dev/stdout
''')

base_ecr_image_module = Definition("infrastructure/main.tf", append=True, text='''
module "{{lambda_name}}_image" {
  source = "./{{lambda_name}}_image"

  name = "{{lambda_name}}_image"
  metrics_path = local.metrics_path
  infragroup_fullname = local.infragroup_fullname
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn

  package_build_path = var.{{lambda_name}}_build_path
}

# lambda_image_ecr = "${module.{{lambda_name}}_image.repository_url}:latest"

''')
base_ecr_image_definition = Definition("infrastructure/{{lambda_name}}_image/ecr_image.tf", text='''
variable "name" { type = string }
variable "metrics_path" { type = string }
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "package_build_path" { type = string }


locals {
  fullname = "${var.infragroup_fullname}-${var.name}"
  metrics_group = "${var.metrics_path}/${var.name}"
}


data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_ecr_repository" "lambda_image_repo" {
  name = "${local.fullname}/image"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "random_id" "deploy_bucket_random_id" { byte_length = 24 }
resource "aws_s3_bucket" "package_bucket" {
  bucket = "packagebucket-${random_id.deploy_bucket_random_id.hex}"
  force_destroy = true
}

resource "aws_s3_object" "package_file" {
  bucket = aws_s3_bucket.package_bucket.id
  key = "package.zip"
  source = var.package_build_path
  etag = filemd5(var.package_build_path)
}

resource "null_resource" "codebuild_project_build_trigger" {
  provisioner "local-exec" {
    command = "./tools/trigger-codebuild.sh '${aws_codebuild_project.codebuild_project.name}'"
  }
  lifecycle {
    replace_triggered_by = [aws_s3_object.package_file]
  }
}

resource "aws_codebuild_project" "codebuild_project" {
  name = "${local.fullname}-image_build_codebuild_project"
  description = "Codebuild for lambda image"
  build_timeout = "120"
  service_role = aws_iam_role.codebuild_pipeline_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  source {
    type = "S3"
    location = "${aws_s3_bucket.package_bucket.id}/${aws_s3_object.package_file.key}"
  }

  environment {
    privileged_mode = true
    image = "aws/codebuild/standard:4.0"
    type = "LINUX_CONTAINER"
    compute_type = "BUILD_GENERAL1_SMALL"

    dynamic "environment_variable" {
      for_each = {
        AWS_ACCOUNT_ID = data.aws_caller_identity.current.account_id
        AWS_ACCOUNT_REGION = data.aws_region.current.name
        REPOSITORY_URI = aws_ecr_repository.lambda_image_repo.repository_url
      }
      content {
        name = environment_variable.key
        value = environment_variable.value
      }
    }
  }

  logs_config {
    cloudwatch_logs {
      group_name = "/codebuild/${local.fullname}/image_build_log"
      stream_name = "image_build_stream"
    }
  }
}


resource "aws_iam_role" "codebuild_pipeline_role" {
  name = "${local.fullname}-codebuild-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "codebuild.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "codebuild_policy" {
  name        = "${local.fullname}-codebuild-policy"
  path        = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "*"
    }, {
      Effect = "Allow"
      Action = "ecr:*"
      Resource = "*"
    },
    {
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "codebuild:CreateReportGroup",
        "codebuild:CreateReport",
        "codebuild:UpdateReport",
      ],
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "codebuild_policy_attachment" {
  role       = aws_iam_role.codebuild_pipeline_role.name
  policy_arn = aws_iam_policy.codebuild_policy.arn
}

output "codebuild_project_name" {
  value = aws_codebuild_project.codebuild_project.name
  depends_on = [null_resource.codebuild_project_build_trigger]
}

output "repository_url" {
  value = aws_ecr_repository.lambda_image_repo.repository_url
  depends_on = [null_resource.codebuild_project_build_trigger]
}
''')
base_ecr_image_buildspec = Definition("src/{{lambda_name}}/buildspec.yaml", text='''version: 0.2
phases:
  pre_build:
    commands:
      - echo logging in to Amazon ECR
      - docker login -u AWS -p $(aws ecr get-login-password --region $AWS_ACCOUNT_REGION) $AWS_ACCOUNT_ID.dkr.ecr.$AWS_ACCOUNT_REGION.amazonaws.com
  build:
    commands:
      - echo build started on `date`
      - docker build -t $REPOSITORY_URI:latest .
  post_build:
    commands:
      - echo build finished on `date`
      - docker push $REPOSITORY_URI:latest
''')
base_ecr_image_dockerfile = Definition("src/{{lambda_name}}/Dockerfile", text='''FROM public.ecr.aws/lambda/python:3.12

# copy in requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}
# install requirements
RUN pip install -r requirements.txt

# extra dependencies
# RUN dnf -y install git

# copy function code
COPY . ${LAMBDA_TASK_ROOT}

# handler
CMD [ "main.lambda_handler" ]
''')
base_ecr_image_build = ReplaceFileDefinition("src/{{lambda_name}}/build.sh", append_if_not_exist=True, text='''#!/bin/bash
zip ../../build/{{lambda_name}}.zip -FSr .
''')
base_ecr_image_module_variable = Definition("infrastructure/{{lambda_name}}/{{lambda_name}}.tf", append=True, text='''
variable "lambda_image_repo_url" { type = string }
''')

base_fargate_server_module = Definition("infrastructure/main.tf", append=True, text='''
variable "{{fargate_server}}_build_path" { default = "../build/{{fargate_server}}.zip" }

module "{{fargate_server}}" {
  source = "./{{fargate_server}}"
  name = "{{fargate_server}}"

  infragroup_fullname = local.infragroup_fullname
  metrics_path = local.metrics_path
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn
  package_build_path = var.{{fargate_server}}_build_path
}

output "{{fargate_server}}_hostname" { value = module.{{fargate_server}}.alb_hostname }
output "{{fargate_server}}_url" { value = module.{{fargate_server}}.alb_url }
''')
base_fargate_server_app_template = Definition("infrastructure/{{fargate_server}}/app.json.template", text='''[
  {
    "name": "${fullname}",
    "image": "${app_image}",
    "cpu": ${fargate_cpu},
    "memory": ${fargate_memory},
    "networkMode": "awsvpc",
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${loggroup}",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "portMappings": [{
      "containerPort": ${app_port},
      "hostPort": ${app_port}
    }]
  }
]''')
base_fargate_server_network = Definition("infrastructure/{{fargate_server}}/network.tf", text='''
variable "az_count" { default = 2 }

data "aws_availability_zones" "available" {}
data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

resource "aws_vpc" "main" {
  cidr_block = "10.1.0.0/16"
}

# locals {
#   fargate_cpu
# }

resource "aws_subnet" "private" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "public" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, var.az_count + count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id = aws_vpc.main.id
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route" "internet_access" {
  route_table_id = aws_vpc.main.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.gw.id
}

resource "aws_eip" "gw_eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat_gw" {
  subnet_id = aws_subnet.public[0].id
  allocation_id = aws_eip.gw_eip.id
}

resource "aws_route_table" "private_rt" {
  count = var.az_count
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw.id
  }
}

resource "aws_route_table_association" "private_rt_association" {
  count = var.az_count
  subnet_id = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private_rt.*.id, count.index)
}
''')
base_fargate_server_instance = Definition("infrastructure/{{fargate_server}}/instance.tf", text='''
variable "infragroup_fullname" { type = string }
variable "metrics_path" { type = string }
variable "sns_alarm_topic_arn" { type = string }

variable "name" { type = string }

locals {
  fargate_cpu = 1024
  fargate_memory = 2048
  app_port = 3000
  # app_image = "bradfordhamilton/crystal_blockchain:latest"

  fullname = "${var.infragroup_fullname}-${var.name}"
  metrics_group = "${var.metrics_path}/${var.name}"
}


resource "aws_security_group" "alb_security_group" {
  name        = "${local.fullname}-alb_security_group"
  description = "Security group for ${local.fullname} ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = local.app_port
    to_port     = local.app_port
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "ecs_task_security_group" {
  name        = "${local.fullname}-ecs_task_security_group"
  description = "Security group for ${local.fullname} tasks (allows inbound access from the ALB only)"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = local.app_port
    to_port     = local.app_port
    protocol    = "TCP"
    security_groups = [aws_security_group.alb_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_alb" "main_alb" {
  name = replace("${var.name}-alb", "_", "-")
  subnets = aws_subnet.public.*.id
  security_groups = [aws_security_group.alb_security_group.id]
}

resource "aws_alb_target_group" "app_target_group" {
  name = replace(replace("${var.name}-lbtg", "-", ""), "_", "")
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold = 3
    unhealthy_threshold = 2
    interval = 30
    timeout = 3
    protocol = "HTTP"
    matcher = "200"
    path = "/"
  }
}

resource "aws_alb_listener" "alb_listener" {
  load_balancer_arn = aws_alb.main_alb.id
  port = local.app_port
  protocol = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.app_target_group.id
    type = "forward"
  }
}


resource "aws_ecs_cluster" "main_cluster" {
  name = "${local.fullname}-ecs_cluster"
}

data "template_file" "ecs_app_template" {
  template = file("${path.module}/app.json.template")
  vars = {
    fullname = "${local.fullname}-app"
    loggroup = "/ecs/${local.fullname}-app"
    # app_image = local.app_image
    app_image = aws_ecr_repository.lambda_image_repo.repository_url
    app_port = local.app_port
    fargate_cpu = local.fargate_cpu
    fargate_memory = local.fargate_memory
    aws_region = data.aws_region.current.name
  }
}

resource "aws_ecs_task_definition" "ecs_task_def" {
  family = "${local.fullname}-task"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = local.fargate_cpu
  memory = local.fargate_memory
  container_definitions = data.template_file.ecs_app_template.rendered
}

resource "aws_ecs_service" "ecs_service" {
  name = "${local.fullname}-ecs_service"
  cluster = aws_ecs_cluster.main_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_def.arn
  desired_count = 1
  launch_type = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.ecs_task_security_group.id]
    subnets = aws_subnet.private.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.app_target_group.id
    container_name = "${local.fullname}-app"
    container_port = local.app_port
  }
}

output "alb_hostname" { value = aws_alb.main_alb.dns_name }
output "alb_url" { value = "http://${aws_alb.main_alb.dns_name}:${local.app_port}" }


## logs

resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name = "/ecs/${local.fullname}-app"
  retention_in_days = 30

  tags = {
    Name = "${local.fullname}-ecs_log_group"
  }
}

## role

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = [
        "ecs-tasks.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${local.fullname}-ecs_task_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "ecs_task_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "ecs_task_policy" {
  name = "${local.fullname}-ecs_task_policy"
  policy = data.aws_iam_policy_document.ecs_task_policy_document.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_attachment" {
  role = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}
''')
base_fargate_dockerfile = Definition("src/{{fargate_server}}/Dockerfile", text='''
# Use the official Ubuntu image as a base
FROM ubuntu:latest

# Update the package list and install necessary packages
RUN apt-get update && \\
    apt-get install -y apache2 curl unzip && \\
    apt-get clean

# Create a simple Hello World HTML page
RUN echo '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Hello World</title></head><body><h1>Hello World!</h1></body></html>' > /var/www/html/index.html

# Change the default Apache port from 80 to 3000
RUN sed -i 's/80/3000/g' /etc/apache2/ports.conf /etc/apache2/sites-available/000-default.conf

# Enable mod_rewrite for Apache
RUN a2enmod rewrite

# Install AWS Systems Manager (SSM) agent
RUN curl "https://s3.amazonaws.com/amazon-ssm-us-east-1/latest/debian_amd64/amazon-ssm-agent.deb" -o "amazon-ssm-agent.deb" && \\
    dpkg -i amazon-ssm-agent.deb && \\
    rm amazon-ssm-agent.deb

# Start the SSM agent and Apache service
CMD /usr/bin/amazon-ssm-agent & apachectl -D FOREGROUND
''')
base_fargate_build = Definition("src/{{fargate_server}}/build.sh", text='''#!/bin/bash
zip -r ../../build/{{fargate_server}}.zip .
''')
base_fargate_makefile = Definition("./Makefile", append=True, text='''
build: build_{{fargate_server}}
build_{{fargate_server}}:
\t-mkdir build
\tcd src/{{fargate_server}} && bash ./build.sh
''')


website_s3_module = Definition("infrastructure/main.tf", append=True, text='''
variable "{{website_name}}_build_path" { default = "../src/{{website_name}}/dist" }

module "{{website_name}}" {
  source = "./{{website_name}}"

  domain_name = "{{domain_name}}"
  build_directory = var.{{website_name}}_build_path
}

output "{{website_name}}_endpoint" { value = "${module.{{website_name}}.website_endpoint}" }
''')

website_s3_definition = Definition("infrastructure/{{website_name}}/{{website_name}}.tf", text='''
variable "domain_name" { type = string }
variable "build_directory" { type = string }

locals {
  content_types = {
    css  = "text/css"
    html = "text/html"
    js   = "application/javascript"
    json = "application/json"
    txt  = "text/plain"
  }
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.domain_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "bucket_access_block" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = "*"
      Action = "s3:GetObject"
      Resource = "arn:aws:s3:::${var.domain_name}/*"
    }]
  })
}

resource "aws_s3_bucket_website_configuration" "bucket_website_configuration" {
  bucket = aws_s3_bucket.bucket.id

  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}

resource "aws_s3_object" "build_file" {
  for_each = fileset(var.build_directory, "**")

  bucket = aws_s3_bucket.bucket.id
  key    = each.value
  source = "${var.build_directory}/${each.value}"

  content_type = lookup(local.content_types, element(split(".", each.value), length(split(".", each.value)) - 1), "text/plain")
  etag   = filemd5("${var.build_directory}/${each.value}")
}

output "website_endpoint" { value = "${aws_s3_bucket_website_configuration.bucket_website_configuration.website_endpoint}" }



# # cf distribution fronting the website, enable when useful
# variable "domain_acm_cert_arn" { type = string }
# resource "aws_cloudfront_distribution" "s3_distribution" {
#   origin {
#     domain_name              = aws_s3_bucket_website_configuration.bucket_website_configuration.website_endpoint
#     # domain_name              = aws_s3_bucket.bucket.bucket_regional_domain_name
#     # origin_access_control_id = aws_cloudfront_origin_access_control.default.id
#     origin_id                = "website_origin"
#     custom_origin_config {
#       http_port                = 80
#       https_port               = 443
#       origin_keepalive_timeout = 5
#       origin_protocol_policy   = "http-only"
#       origin_read_timeout      = 30
#       origin_ssl_protocols     = [
#         "TLSv1.2",
#       ]
#     }
#   }

#   aliases = [ var.domain_name ]

#   enabled             = true
#   is_ipv6_enabled     = true
#   default_root_object = "index.html"

#   default_cache_behavior {
#     allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
#     cached_methods   = ["GET", "HEAD"]
#     target_origin_id = "website_origin"

#     forwarded_values {
#       query_string = false

#       cookies {
#         forward = "none"
#       }
#     }

#     viewer_protocol_policy = "allow-all"
#     min_ttl                = 0
#     default_ttl            = 3600
#     max_ttl                = 86400
#   }

#   restrictions {
#     geo_restriction {
#       restriction_type = "none"
#       locations        = []
#     }
#   }

#   price_class = "PriceClass_100"

#   viewer_certificate {
#     acm_certificate_arn = var.domain_acm_cert_arn
#     ssl_support_method = "sni-only"
#   }
# }

# output "distribution_id" { value = "${aws_cloudfront_distribution.s3_distribution.id}" }
''')
website_s3_dockerfile = Definition("src/{{website_name}}/docker/Dockerfile", text='''FROM ubuntu:20.04
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \\
  && apt-get install -y curl nano jq zip

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \\
  && apt-get install -y openssh-client \\
  && apt-get install -y nodejs \\
  && apt autoclean \\
  && apt autoremove \\
  && apt clean

RUN useradd -ms /bin/bash runuser
USER runuser

CMD npm start
''')
website_s3_docker_run = Definition("src/{{website_name}}/docker/run", text='''#!/bin/bash
IMAGE_TAG="local-${PWD##*/}"
docker image inspect "$IMAGE_TAG" > /dev/null || docker build docker -t "$IMAGE_TAG"
docker run -v $PWD:/app -p3000:3000 --rm --cap-drop=all -it $(docker build -q docker -t "$IMAGE_TAG") $@
''')
website_s3_build = Definition("src/{{website_name}}/build.sh", text='''#!/bin/bash
set -e

npm i
npm run build
''')
website_s3_makefile = Definition("./Makefile", append=True, text='''
build: build_{{website_name}}
build_{{website_name}}:
\t-mkdir build
\tcd src/{{website_name}} && bash ./build.sh
''')
website_s3_package_json = Definition("src/{{website_name}}/package.json", text='''{
  "name": "react-site",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "webpack serve",
    "build": "rm -rf dist && webpack . --mode production && cp -rf public/* dist && rm dist/**.map",
    "test": "test"
  },
  "author": "",
  "devDependencies": {
    "@babel/cli": "^7.19.3",
    "@babel/core": "^7.20.5",
    "@babel/eslint-parser": "^7.19.1",
    "@babel/plugin-transform-runtime": "^7.19.6",
    "@babel/preset-env": "^7.20.2",
    "@babel/preset-react": "^7.18.6",
    "@babel/runtime": "^7.20.6",
    "babel-loader": "^9.1.0",
    "html-webpack-plugin": "^5.5.0",
    "webpack": "^5.75.0",
    "webpack-cli": "^5.0.0",
    "webpack-dev-server": "^4.11.1"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.4.4"
  }
}''')
website_s3_webpack_config = Definition("src/{{website_name}}/webpack.config.js", text='''const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

/*We are basically telling webpack to take index.js from entry. Then check for all file extensions in resolve. 
After that apply all the rules in module.rules and produce the output and place it in main.js in the public folder.*/

module.exports={
  /** "mode"
   * the environment - development, production, none. tells webpack 
   * to use its built-in optimizations accordingly. default is production 
   */
  mode: "development", 
  /** "entry"
   * the entry point 
   */
  entry: "./index.js", 
  devtool: 'source-map',
  output: {
    filename: "bundle.[hash].js",
    path: path.resolve(__dirname, "dist"),
  },
  /** "target"
   * setting "node" as target app (server side), and setting it as "web" is 
   * for browser (client side). Default is "web"
   */
  target: "web",
  devServer: {
    /** "port" 
     * port of dev server
    */
    port: "3000",
    /** "static" 
     * This property tells Webpack what static file it should serve
    */
    static: ["./public"],
    /** "open" 
     * opens the browser after server is successfully started
    */
    open: true,
    /** "hot"
     * enabling and disabling HMR. takes "true", "false" and "only". 
     * "only" is used if enable Hot Module Replacement without page 
     * refresh as a fallback in case of build failures
     */
    hot: false ,
    /** "liveReload"
     * disable live reload on the browser. "hot" must be set to false for this to work
    */
    liveReload: true,
    historyApiFallback: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./src/index.html",
    }),
  ],
  resolve: {
    /** "extensions" 
     * If multiple files share the same name but have different extensions, webpack will 
     * resolve the one with the extension listed first in the array and skip the rest. 
     * This is what enables users to leave off the extension when importing
     */
    modules: [__dirname, "src", "node_modules"],
    extensions: ['.js','.jsx','.json', ".tsx", ".ts"] 
  },
  module:{
    /** "rules"
     * This says - "Hey webpack compiler, when you come across a path that resolves to a '.js or .jsx' 
     * file inside of a require()/import statement, use the babel-loader to transform it before you 
     * add it to the bundle. And in this process, kindly make sure to exclude node_modules folder from 
     * being searched"
     */
    rules: [
      {
        test: /\.(js|jsx)$/,    //kind of file extension this rule should look for and apply in test
        exclude: /node_modules/, //folder to be excluded
        use:  'babel-loader' //loader which we are going to use
      }
    ]
  }
}''')
website_s3_babelrc = Definition("src/{{website_name}}/babel.config.js", text='''module.exports = {
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ],
  "plugins": [
    "@babel/plugin-transform-runtime"
  ]
}''')
website_s3_index_js = Definition("src/{{website_name}}/index.js", text='''import React from "react";
import reactDom from "react-dom";
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from "react-router-dom";
import App from "./src/App"

const root = createRoot(document.getElementById('root'));
root.render(<BrowserRouter>
    <App />
  </BrowserRouter>);
''')
website_s3_index_html = Definition("src/{{website_name}}/src/index.html", text='''<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{website_name}}</title>
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/styles.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>''')
website_s3_app_js = Definition("src/{{website_name}}/src/App.js", text='''import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";

const App = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={ <Home/> } />
      </Routes>
    </div>
  )
}

export default App
''')
website_s3_home_js = Definition("src/{{website_name}}/src/pages/Home.jsx", text='''import React from "react";

const Home = () => {
  return (
    <div className="homepage">
      hello world
    </div>
  )
}
export default Home
''')
website_s3_styles_css = Definition("src/{{website_name}}/public/css/styles.css", text='''''')
website_s3_test = Definition("scripts/test.sh", append=True, text='''
WEBSITE_URL=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{website_name}}_endpoint.value')
echo "website endpoint: $WEBSITE_URL"
curl "$WEBSITE_URL"
''')



ec2_server_module = Definition("infrastructure/main.tf", append=True, text='''
variable "{{server_name}}_build_path" { default = "../build/{{server_name}}.zip" }

module "{{server_name}}" {
  source = "./{{server_name}}"

  metrics_path = local.metrics_path
  infragroup_fullname = local.infragroup_fullname
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn
  package_build_path = var.{{server_name}}_build_path
  server_config = {}
}

output "{{server_name}}_server_ip" { value = module.{{server_name}}.server_ip }
output "{{server_name}}_instance_id" { value = module.{{server_name}}.instance_id }
''')
ec2_server_makefile = Definition("./Makefile", append=True, text='''
build: build_{{server_name}}_package
build_{{server_name}}_package:
\t-mkdir build
\tcd src && zip ../build/{{server_name}}.zip -FSr {{server_name}}/
''')
ec2_server_definition = Definition("infrastructure/{{server_name}}/{{server_name}}.tf", text='''
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "metrics_path" { type = string }

variable "package_build_path" { type = string }
variable "ingress_ports" { default = [] }
variable "server_config" { default = {} }

locals {
  servername = "{{server_name}}"
  fullname = "${var.infragroup_fullname}-{{server_name}}"
  metrics_group = "${var.metrics_path}/{{server_name}}"
}

resource "aws_instance" "instance" {
  ami           = "ami-0e14491966b97e8bc"
  instance_type = "t2.medium"

  security_groups = [aws_security_group.instance_security_group.name]
  iam_instance_profile = aws_iam_instance_profile.instance_profile.id

  root_block_device {
    volume_size = 20
  }

  user_data = <<-EOT
  #cloud-config
  runcmd:
    - sleep 5
    - sudo env DEBIAN_FRONTEND=noninteractive apt -y update
    - sudo env DEBIAN_FRONTEND=noninteractive apt install -y unzip curl awscli jq
    - sudo mkdir -p /app/log
    - sudo mkdir -p /app/config
    - sudo chown -R ubuntu:ubuntu /app
    - echo '${local.fullname}' > /app/config/server_fullname
    - echo '${local.metrics_group}' > /app/config/metrics_group
    - echo '${jsonencode(var.server_config)}' > /app/config/server_config.json
    - echo 's3://${aws_s3_bucket.deploy_bucket.id}/'
    - aws s3 cp s3://${aws_s3_bucket.deploy_bucket.id}/package.zip /app/package.zip
    - unzip /app/package.zip -d /app
    - sudo chown -R ubuntu:ubuntu /app
    - cd /app/{{server_name}} && chmod +x *.sh && ./install.sh 2>&1 >> /app/log/init.log
  EOT
}

resource "aws_security_group" "instance_security_group" {
  name        = "${local.fullname}-security_group"
  description = "Security group for ${local.fullname}"

  dynamic "ingress" {
    for_each = var.ingress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "${local.fullname}-instance_profile"
  role = aws_iam_role.instance_role.name
}

resource "aws_iam_role" "instance_role" {
  name = "${local.fullname}-instance_role"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "instance_policy" {
  name = "${local.fullname}-instance_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "instance_policy_attachment" {
  name       = "${local.fullname}-instance_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = aws_iam_policy.instance_policy.arn
}
# SSM policy is needed for AWS SSM to work on the instance
resource "aws_iam_policy_attachment" "instance_managed_policy_attachment" {
  name       = "${local.fullname}-instance_managed_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}


resource "random_id" "deploy_bucket_random_id" { byte_length = 24 }
resource "aws_s3_bucket" "deploy_bucket" {
  bucket = "deploypackage-${random_id.deploy_bucket_random_id.hex}"
  force_destroy = true
}

resource "aws_s3_object" "build_file" {
  bucket = aws_s3_bucket.deploy_bucket.id
  key = "package.zip"
  source = var.package_build_path
  etag = filemd5(var.package_build_path)
}

# log group for server logs
resource "aws_cloudwatch_log_group" "server_log_group" {
  name = "/${local.metrics_group}/server-logs"
  retention_in_days = 90
}

# # CPU Utilization alarm, will sound when utilization is over 80 percent for two periods
# resource "aws_cloudwatch_metric_alarm" "cpu_utilization_alarm" {
#   alarm_name                = "${local.fullname}-cpu_utilization_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "CPUUtilization"
#   namespace                 = "AWS/EC2"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 80
#   alarm_description         = "This metric monitors ec2 cpu utilization"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#   }
# }

# # Disk Utilization alarm, will sound when disk is over 80 percent capacity
# resource "aws_cloudwatch_metric_alarm" "disk_used_alarm" {
#   alarm_name                = "${local.fullname}-disk_used_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "disk_used_percent"
#   namespace                 = "CWAgent"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 80
#   alarm_description         = "This metric monitors ec2 disk used percent"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#     device = "xvda1"
#     fstype = "ext4"
#     path = "/"
#   }
# }

# # Memory Utilization alarm, will sound when memory utilization is over 90 percent for two periods
# resource "aws_cloudwatch_metric_alarm" "mem_used_alarm" {
#   alarm_name                = "${local.fullname}-mem_used_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "mem_used_percent"
#   namespace                 = "CWAgent"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 90
#   alarm_description         = "This metric monitors ec2 memory used percent"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#   }
# }


output "monitor_widget_json" {
  value = <<EOF
  {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "AWS/EC2", "CPUUtilization", "InstanceId", "${aws_instance.instance.id}", { "region": "us-east-1", "id": "m1", "color": "#555" } ]
          ],
          "region": "us-east-1",
          "period": 300,
          "title": "${local.servername} CPU Stats",
          "stat": "Average"
      }
  },
  {
      "type": "metric",
      "x": 6,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "metrics": [
              [ "AWS/EC2", "NetworkOut", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "NetworkIn", ".", "." ]
          ],
          "region": "us-east-1",
          "title": "${local.servername} Network Stats",
          "stacked": true
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 0,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "CWAgent", "disk_used_percent", "path", "/", "InstanceId", "${aws_instance.instance.id}", "device", "xvda1", "fstype", "ext4" ]
          ],
          "title": "${local.servername} Percent Disk Used",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 3,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "CWAgent", "mem_used_percent", "InstanceId", "${aws_instance.instance.id}" ]
          ],
          "title": "${local.servername} Percent Memory Used",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 6,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": false,
          "metrics": [
              [ "CWAgent", "netstat_tcp_listen", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "netstat_tcp_established", ".", "." ]
          ],
          "title": "${local.servername} Network Connections",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 9,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": false,
          "metrics": [
              [ "CWAgent", "processes_running", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "processes_total", ".", "." ]
          ],
          "title": "${local.servername} Process Counts",
          "region": "us-east-1"
      }
  }
EOF
}

# output "alarm_widget_json" {
#   value = <<EOF
#   {
#       "type": "metric",
#       "x": 0,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.cpu_utilization_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} CPU Alarm",
#           "stacked": false
#       }
#   },
#   {
#       "type": "metric",
#       "x": 6,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.disk_used_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} Disk Alarm",
#           "stacked": false
#       }
#   },
#   {
#       "type": "metric",
#       "x": 0,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.mem_used_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} Memory Alarm",
#           "stacked": false
#       }
#   }
# EOF
# }

output "server_ip" { value = "${aws_instance.instance.public_ip}" }
output "instance_id" { value = "${aws_instance.instance.id}" }
''')
ec2_server_install_sh = Definition("src/{{server_name}}/install.sh", text='''#!/bin/sh
echo "[+] chmoding everything"
cd /app/{{server_name}}
chmod +x ./*.sh

echo "[+] installing unattended-upgrades for automated package updates"
env DEBIAN_FRONTEND=noninteractive apt install -y unattended-upgrades apt-listchanges

ARG_METRICS_GROUP=`cat /app/config/metrics_group`

echo "[+] prep aws logs file"
cat awslogs.cfg.template \\
  | sed "s#{metrics_group}#$ARG_METRICS_GROUP#g" \\
  > /app/config/awslogs.cfg

echo "[+] setup aws logs"
env DEBIAN_FRONTEND=noninteractive apt install -y python2
curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O
python2 awslogs-agent-setup.py --region us-east-1 -c /app/config/awslogs.cfg -n
rm awslogs-agent-setup.py

echo "[+] setup aws metrics"
wget https://s3.amazonaws.com/amazoncloudwatch-agent/debian/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb
rm amazon-cloudwatch-agent.deb
echo "[+] configuring aws metrics config file"
cat amazon-cloudwatch-agent.json.template \\
  | sed "s#{metrics_group}#$ARG_METRICS_GROUP#g" \\
  > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
echo "[+] restarting metrics daemon"
systemctl restart amazon-cloudwatch-agent
# this enabled the agent starting every time the server is rebooted
systemctl enable amazon-cloudwatch-agent

echo "[+] installing reboot script"
ln -s /app/{{server_name}}/reboot.sh /var/lib/cloud/scripts/per-boot/reboot-init.sh
echo "[+] running main server startup"
su -c /app/{{server_name}}/server-startup.sh ubuntu 2>&1 >> /app/log/init.log
''')
ec2_server_startup_sh = Definition("src/{{server_name}}/server-startup.sh", text='''#!/bin/sh
echo "[i] server startup..."
cd /app/{{server_name}}
echo "[+] server startup complete!"
''')
ec2_server_reboot_sh = Definition("src/{{server_name}}/reboot.sh", text='''#!/bin/sh
echo "[+] server rebooted..." 2>&1 >> /app/log/init.log
su -c /app/{{server_name}}/server-startup.sh ubuntu 2>&1 >> /app/log/init.log
''')
ec2_server_daemonize_sh = Definition("src/{{server_name}}/daemonize.sh", text='''#!/bin/sh
DIRPATH=`dirname "$0"`

echo "[+] adding user '$1'"
sudo useradd "$1" && {
  echo "[+] user created, initializing home folder"
  sudo mkdir "/home/$1"
  sudo chown $1:$1 "/home/$1"

  echo "[+] initializing log"
  touch "$3"
  sudo chown $1:$1 "$3"
} || echo "[-] user already exists"

echo "[+] starting daemon"
sudo su "$1" -c "nohup \\"$DIRPATH/keepalive.sh\\" \\"$2\\" < \\"$4\\" >> \\"$3\\" 2>&1 &"
''')
ec2_server_keepalive_sh = Definition("src/{{server_name}}/keepalive.sh", text='''#!/bin/sh
TIMEOUT_TIME=30
until $1; do
    echo "[!] command '$1' crashed with exit code $?, sleeping for $TIMEOUT_TIME"
    sleep $TIMEOUT_TIME
    echo "[!] respawning..."
    TIMEOUT_TIME=$(($TIMEOUT_TIME+30))
done
''')
ec2_server_awslogs_cfg = Definition("src/{{server_name}}/awslogs.cfg.template", text='''[general]
state_file = push-state

[logstream1]
file = /app/log/init.log
log_group_name = /{metrics_group}/server-logs
log_stream_name = {instance_id}/init.log
initial_position = start_of_file
buffer_duration = 300000
''')
ec2_server_cwagent_cfg = Definition("src/{{server_name}}/amazon-cloudwatch-agent.json.template", text='''{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "cwagent"
  },
  "metrics": {
    "append_dimensions": {
      "InstanceId": "${aws:InstanceId}"
    },
    "metrics_collected": {
      "disk": {
        "measurement": [ "used_percent" ],
        "metrics_collection_interval": 60,
        "resources": [ "/" ]
      },
      "mem": {
        "measurement": [ "mem_available", "mem_free", "mem_used", "mem_used_percent" ],
        "metrics_collection_interval": 60,
        "resources": [ "/" ]
      },
      "netstat": {
        "measurement": [ "netstat_tcp_established", "netstat_tcp_listen" ],
        "metrics_collection_interval": 60,
        "resources": [ "/" ]
      },
      "processes": {
        "measurement": [ "processes_running", "processes_total" ],
        "metrics_collection_interval": 60,
        "resources": [ "/" ]
      }
    }
  }
}''')



bastion_ec2_server_module = ec2_server_module.but_replace('''server_config = {}''', '''server_config = {}
  domain_name = local.domain_name
  # domain_acm_cert_arn = local.domain_acm_cert_arn
''')
bastion_ec2_server_definition = Definition("infrastructure/{{server_name}}/{{server_name}}.tf", text='''
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "metrics_path" { type = string }

variable "package_build_path" { type = string }
variable "ingress_ports" { default = [3000] }
variable "availability_zones" { default = ["us-east-1a", "us-east-1b", "us-east-1c"] }
variable "server_config" { default = {} }

variable "domain_name" { type = string }
# variable "domain_acm_cert_arn" { type = string }

locals {
  servername = "{{server_name}}"
  fullname = "${var.infragroup_fullname}-{{server_name}}"
  metrics_group = "${var.metrics_path}/{{server_name}}"
}

resource "aws_instance" "instance" {
  ami           = "ami-0e14491966b97e8bc"
  instance_type = "t2.medium"

  key_name = aws_key_pair.instance_aws_key.id
  iam_instance_profile = aws_iam_instance_profile.instance_profile.id

  # security_groups = [aws_security_group.instance_security_group.name]
  subnet_id = aws_subnet.instance_vpc_public_subnet["subnet_d"].id
  vpc_security_group_ids = [aws_security_group.instance_security_group.id]

  root_block_device {
    volume_size = 20
  }

  user_data = <<-EOT
  #cloud-config
  runcmd:
    - sleep 5
    - sudo env DEBIAN_FRONTEND=noninteractive apt -y update
    - sudo env DEBIAN_FRONTEND=noninteractive apt install -y unzip curl awscli jq
    - sudo mkdir -p /app/log
    - sudo mkdir -p /app/config
    - sudo chown -R ubuntu:ubuntu /app
    - echo '${local.fullname}' > /app/config/server_fullname
    - echo '${local.metrics_group}' > /app/config/metrics_group
    - echo '${jsonencode(var.server_config)}' > /app/config/server_config.json
    - echo 's3://${aws_s3_bucket.deploy_bucket.id}/'
    - aws s3 cp s3://${aws_s3_bucket.deploy_bucket.id}/package.zip /app/package.zip
    - unzip /app/package.zip -d /app
    - sudo chown -R ubuntu:ubuntu /app
    - cd /app/{{server_name}} && chmod +x *.sh && ./install.sh 2>&1 >> /app/log/init.log
  EOT
}

resource "aws_security_group" "instance_security_group" {
  vpc_id = aws_vpc.instance_vpc.id

  name        = "${local.fullname}-security_group"
  description = "Security group for ${local.fullname}"

  dynamic "ingress" {
    for_each = var.ingress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      security_groups = [aws_security_group.instance_alb_security_group.id]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


####################################
# instance IAM role and policy attachments
resource "aws_iam_instance_profile" "instance_profile" {
  name = "${local.fullname}-instance_profile"
  role = aws_iam_role.instance_role.name
}

resource "aws_iam_role" "instance_role" {
  name = "${local.fullname}-instance_role"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# primary IAM policy for the instance
resource "aws_iam_policy" "instance_policy" {
  name = "${local.fullname}-instance_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData",
        "logs:PutLogEvents",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
}
resource "aws_iam_policy_attachment" "instance_policy_attachment" {
  name       = "${local.fullname}-instance_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = aws_iam_policy.instance_policy.arn
}
# SSM policy is needed for AWS SSM to work on the instance
resource "aws_iam_policy_attachment" "instance_managed_policy_attachment" {
  name       = "${local.fullname}-instance_managed_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
####################################



####################################
# S3 deployment bucket (optional if you don't need a deployment package)
resource "random_id" "deploy_bucket_random_id" { byte_length = 24 }
resource "aws_s3_bucket" "deploy_bucket" {
  bucket = "deploypackage-${random_id.deploy_bucket_random_id.hex}"
  force_destroy = true
}

resource "aws_s3_object" "build_file" {
  bucket = aws_s3_bucket.deploy_bucket.id
  key = "package.zip"
  source = var.package_build_path
  etag = filemd5(var.package_build_path)
}
####################################


####################################
# VPC and networking for the instance
resource "aws_vpc" "instance_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "instance_vpc_private_subnet" {
  for_each = {
      subnet_a = {
        range = "10.0.1.0/24"
        availability_zone = var.availability_zones[0]
      },
      subnet_b = {
        range = "10.0.2.0/24"
        availability_zone = var.availability_zones[1]
      },
      subnet_c = {
        range = "10.0.3.0/24"
        availability_zone = var.availability_zones[2]
      },
  }

  vpc_id = aws_vpc.instance_vpc.id
  cidr_block = each.value["range"]
  availability_zone = each.value["availability_zone"]
}

resource "aws_subnet" "instance_vpc_public_subnet" {
  for_each = {
      subnet_d = {
        range = "10.0.4.0/24"
        availability_zone = var.availability_zones[0]
      },
      subnet_e = {
        range = "10.0.5.0/24"
        availability_zone = var.availability_zones[1]
      },
      subnet_f = {
        range = "10.0.6.0/24"
        availability_zone = var.availability_zones[2]
      },
  }

  vpc_id = aws_vpc.instance_vpc.id
  cidr_block = each.value["range"]
  availability_zone = each.value["availability_zone"]
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "instance_vpc_internet_gateway" {
  vpc_id = aws_vpc.instance_vpc.id
}
resource "aws_route_table" "instance_vpc_route_table" {
  vpc_id = aws_vpc.instance_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.instance_vpc_internet_gateway.id
  }
}
resource "aws_route_table_association" "instance_vpc_private_route_table_association" {
  for_each = aws_subnet.instance_vpc_private_subnet
  subnet_id      = each.value.id
  route_table_id = aws_route_table.instance_vpc_route_table.id
}
resource "aws_route_table_association" "instance_vpc_public_route_table_association" {
  for_each = aws_subnet.instance_vpc_public_subnet
  subnet_id      = each.value.id
  route_table_id = aws_route_table.instance_vpc_route_table.id
}

# VPC DNS Query Logging
resource "aws_route53_resolver_query_log_config_association" "dns_query_log_config_association" {
  resolver_query_log_config_id = aws_route53_resolver_query_log_config.dns_query_log_config.id
  resource_id                  = aws_vpc.instance_vpc.id
}
resource "aws_route53_resolver_query_log_config" "dns_query_log_config" {
  name            = "${local.fullname}-dns_query_log_config"
  destination_arn = aws_cloudwatch_log_group.aws_route53_resolver_log_group.arn
}
resource "aws_cloudwatch_log_group" "aws_route53_resolver_log_group" {
  name = "/aws/cloudwatch_resolver/${local.fullname}"
  retention_in_days = 30
}

####################################

####################################
# ALB and targeting
resource "aws_lb" "instance_alb" {
  name               = replace("${var.infragroup_fullname}-alb", "_", "-")
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.instance_alb_security_group.id]
  subnets            = [
    aws_subnet.instance_vpc_public_subnet["subnet_d"].id,
    aws_subnet.instance_vpc_public_subnet["subnet_e"].id
  ]
}
resource "aws_security_group" "instance_alb_security_group" {
  vpc_id = aws_vpc.instance_vpc.id

  name        = "${local.fullname}-alb_security_group"
  description = "Allows only 443 for the ALB"

  dynamic "ingress" {
    for_each = [ 443 ]
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_lb_listener" "instance_alb_listener" {
  load_balancer_arn = aws_lb.instance_alb.arn

  port              = 443
  protocol          = "HTTPS"

  # ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.domain_acm_cert_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.instance_alb_target_group.arn
  }
}
resource "aws_lb_target_group" "instance_alb_target_group" {
  name = replace("${var.infragroup_fullname}-atg", "_", "-")
  port = 3000
  protocol    = "HTTP"
  # target_type = "ip"
  vpc_id      = aws_vpc.instance_vpc.id

  health_check {
    interval = 300
    protocol = "HTTP"
    path = "/"
  }
}
resource "aws_lb_target_group_attachment" "instance_alb_target_group_attachment" {
  target_group_arn = aws_lb_target_group.instance_alb_target_group.arn
  target_id        = aws_instance.instance.id
  port             = 3000
}
####################################

# ####################################
# # CloudFront distribution for fronting the LB
# resource "aws_cloudfront_distribution" "instance_distribution" {
#   origin {
#     domain_name              = aws_lb.instance_alb.dns_name
#     origin_id                = "alb_origin"

#     custom_origin_config {
#       http_port                = 80
#       https_port               = 443
#       origin_keepalive_timeout = 5
#       origin_protocol_policy   = "https-only"
#       origin_read_timeout      = 30
#       origin_ssl_protocols     = [ "TLSv1.2" ]
#     }
#   }

#   aliases = [ var.domain_name ]

#   enabled             = true
#   is_ipv6_enabled     = true
#   default_root_object = "/"

#   default_cache_behavior {
#     allowed_methods  = [ "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT" ]
#     cached_methods   = [ "GET", "HEAD" ]
#     target_origin_id = "alb_origin"

#     cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
#     origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa07d3"

#     viewer_protocol_policy = "allow-all"
#   }

#   restrictions {
#     geo_restriction {
#       restriction_type = "none"
#       locations        = []
#     }
#   }

#   price_class = "PriceClass_100"

#   viewer_certificate {
#     acm_certificate_arn = var.domain_acm_cert_arn
#     ssl_support_method = "sni-only"
#   }
# }
# ####################################

# log group for server logs
resource "aws_cloudwatch_log_group" "server_log_group" {
  name = "/${local.metrics_group}/server-logs"
  retention_in_days = 90
}

# # CPU Utilization alarm, will sound when utilization is over 80 percent for two periods
# resource "aws_cloudwatch_metric_alarm" "cpu_utilization_alarm" {
#   alarm_name                = "${local.fullname}-cpu_utilization_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "CPUUtilization"
#   namespace                 = "AWS/EC2"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 80
#   alarm_description         = "This metric monitors ec2 cpu utilization"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#   }
# }

# # Disk Utilization alarm, will sound when disk is over 80 percent capacity
# resource "aws_cloudwatch_metric_alarm" "disk_used_alarm" {
#   alarm_name                = "${local.fullname}-disk_used_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "disk_used_percent"
#   namespace                 = "CWAgent"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 80
#   alarm_description         = "This metric monitors ec2 disk used percent"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#     device = "xvda1"
#     fstype = "ext4"
#     path = "/"
#   }
# }

# # Memory Utilization alarm, will sound when memory utilization is over 90 percent for two periods
# resource "aws_cloudwatch_metric_alarm" "mem_used_alarm" {
#   alarm_name                = "${local.fullname}-mem_used_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "mem_used_percent"
#   namespace                 = "CWAgent"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 90
#   alarm_description         = "This metric monitors ec2 memory used percent"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.instance.id
#   }
# }

# # Uptime alarm, will sound when uptime fails for >15 minutes
# resource "aws_cloudwatch_metric_alarm" "uptime_alarm" {
#   alarm_name                = "${local.fullname}-uptime_alarm"
#   comparison_operator       = "LessThanThreshold"
#   evaluation_periods        = "3"
#   metric_name               = "HealthyHostCount"
#   namespace                 = "AWS/ApplicationELB"
#   period                    = 300
#   statistic                 = "Average"
#   threshold                 = 0.8
#   alarm_description         = "This metric monitors ec2 uptime percent"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     TargetGroup = aws_lb_target_group.instance_alb_target_group.arn_suffix
#     LoadBalancer = aws_lb.instance_alb.arn_suffix
#   }
# }


output "monitor_widget_json" {
  value = <<EOF
  {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "AWS/EC2", "CPUUtilization", "InstanceId", "${aws_instance.instance.id}", { "region": "us-east-1", "id": "m1", "color": "#555" } ]
          ],
          "region": "us-east-1",
          "period": 300,
          "title": "${local.servername} CPU Stats",
          "stat": "Average"
      }
  },
  {
      "type": "metric",
      "x": 6,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "metrics": [
              [ "AWS/EC2", "NetworkOut", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "NetworkIn", ".", "." ]
          ],
          "region": "us-east-1",
          "title": "${local.servername} Network Stats",
          "stacked": true
      }
  },
  {
      "type": "metric",
      "x": 12,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "title": "${local.servername} Requests",
          "metrics": [
              [ "AWS/CloudFront", "Requests", "Region", "Global", "DistributionId", "${aws_cloudfront_distribution.instance_distribution.id}", { "region": "us-east-1", "color": "#aec7e8" } ]
          ],
          "view": "timeSeries",
          "stacked": true,
          "region": "us-east-1",
          "period": 300,
          "stat": "Average"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 0,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "CWAgent", "disk_used_percent", "path", "/", "InstanceId", "${aws_instance.instance.id}", "device", "xvda1", "fstype", "ext4" ]
          ],
          "title": "${local.servername} Percent Disk Used",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 3,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "CWAgent", "mem_used_percent", "InstanceId", "${aws_instance.instance.id}" ]
          ],
          "title": "${local.servername} Percent Memory Used",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 6,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": false,
          "metrics": [
              [ "CWAgent", "netstat_tcp_listen", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "netstat_tcp_established", ".", "." ]
          ],
          "title": "${local.servername} Network Connections",
          "region": "us-east-1"
      }
  },
  {
      "type": "metric",
      "x": 18,
      "y": 9,
      "width": 6,
      "height": 3,
      "properties": {
          "view": "timeSeries",
          "stacked": false,
          "metrics": [
              [ "CWAgent", "processes_running", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "processes_total", ".", "." ]
          ],
          "title": "${local.servername} Process Counts",
          "region": "us-east-1"
      }
  },
  {
      "height": 3,
      "width": 6,
      "y": 6,
      "x": 12,
      "type": "metric",
      "properties": {
          "view": "timeSeries",
          "stacked": false,
          "metrics": [
              [ "AWS/ApplicationELB", "HealthyHostCount", "TargetGroup", "${aws_lb_target_group.instance_alb_target_group.arn_suffix}", "LoadBalancer", "${aws_lb.instance_alb.arn_suffix}", { "label": "metric", "id": "m1" } ]
          ],
          "title": "${local.servername} Healthy",
          "region": "us-east-1"
      }
  },
  {
      "height": 3,
      "width": 6,
      "y": 9,
      "x": 12,
      "type": "metric",
      "properties": {
          "sparkline": true,
          "title": "${local.servername} Uptime Percent",
          "metrics": [
              [ "AWS/ApplicationELB", "HealthyHostCount", "TargetGroup", "${aws_lb_target_group.instance_alb_target_group.arn_suffix}", "LoadBalancer", "${aws_lb.instance_alb.arn_suffix}", { "label": "metric", "id": "m1", "visible": false } ],
              [ { "expression": "m1 < 1", "label": "Value for higher than warning", "id": "warning_or_higher", "visible": false } ],
              [ { "expression": "m1 >= 1", "label": "Value for lower than warning", "id": "ok", "visible": false } ],
              [ { "expression": "100*RUNNING_SUM(ok)/(RUNNING_SUM(ok)+RUNNING_SUM(warning_or_higher))", "label": "Uptime", "id": "uptime", "visible": true } ]
          ],
          "view": "timeSeries",
          "stacked": true,
          "region": "us-east-1",
          "period": 300,
          "stat": "Average"
      }
  }
EOF
}

# output "alarm_widget_json" {
#   value = <<EOF
#   {
#       "type": "metric",
#       "x": 0,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.cpu_utilization_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} CPU Alarm",
#           "stacked": false
#       }
#   },
#   {
#       "type": "metric",
#       "x": 6,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.disk_used_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} Disk Alarm",
#           "stacked": false
#       }
#   },
#   {
#       "type": "metric",
#       "x": 0,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.mem_used_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} Memory Alarm",
#           "stacked": false
#       }
#   },
#   {
#       "type": "metric",
#       "x": 6,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.uptime_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "${local.servername} Uptime Alarm",
#           "stacked": false
#       }
#   }
# EOF
# }

output "server_ip" { value = "${aws_instance.instance.public_ip}" }
output "instance_id" { value = "${aws_instance.instance.id}" }
''')
bastion_ec2_server_install_sh = ec2_server_install_sh.but_replace('''/var/lib/cloud/scripts/per-boot/reboot-init.sh''', '''/var/lib/cloud/scripts/per-boot/reboot-init.sh

echo "[i] installing dependencies..."
env DEBIAN_FRONTEND=noninteractive apt install -y docker.io docker-compose
echo "[+] dependencies installed!"

echo "[+] adding user to docker group"
usermod -aG docker ubuntu

''')
bastion_ec2_server_startup_sh = Definition("src/{{server_name}}/server-startup.sh", text='''#!/bin/sh
# this script runs every time the server is started or restarted
# it runs with ubuntu user privileges. use sudo where necessary

echo "[i] server startup..."
cd "$(dirname "$0")"

mkdir server
cp docker-compose.yml.template server/docker-compose.yml

echo "[+] details prepared, starting docker-compose..."
./daemonize.sh ubuntu "$(dirname "$0")/run-docker.sh" /app/log/server.log /dev/null

echo "[+] server startup complete!"
''')
bastion_ec2_server_rundocker_sh = Definition("src/{{server_name}}/run-docker.sh", text='''#!/bin/sh
# this is where your server magic runs
cd "$(dirname "$0")" && cd ./server
docker-compose up
''')
bastion_ec2_server_dockercompose_template = Definition("src/{{server_name}}/docker-compose.yml.template", text='''
put your magic here
''')



windows_ec2_server_definition = Definition("infrastructure/{{server_name}}/{{server_name}}.tf", text='''
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "metrics_path" { type = string }

variable "package_build_path" { type = string }
variable "ingress_ports" { default = [3389] }
variable "server_config" { default = {} }

locals {
  fullname = "${var.infragroup_fullname}-{{server_name}}"
  metrics_group = "${var.metrics_path}/{{server_name}}"
}

data "aws_ami" "windows_ami_image" {
  most_recent = true
  filter {
    name   = "name"
    values = ["Windows_Server-2019-English-Full-Base-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["801119661308"]
}


resource "aws_instance" "instance" {
  ami           = data.aws_ami.windows_ami_image.id
  instance_type = "t2.medium"

  security_groups = [aws_security_group.instance_security_group.name]
  iam_instance_profile = aws_iam_instance_profile.instance_profile.id

  root_block_device {
    volume_size = 60
  }

  # user_data = <<-EOT
  # #cloud-config
  # runcmd:
  #   - sleep 5
  #   - sudo env DEBIAN_FRONTEND=noninteractive apt -y update
  #   - sudo env DEBIAN_FRONTEND=noninteractive apt install -y unzip curl awscli jq
  #   - sudo mkdir -p /app/log
  #   - sudo mkdir -p /app/config
  #   - sudo chown -R ubuntu:ubuntu /app
  #   - echo '${local.fullname}' > /app/config/server_fullname
  #   - echo '${local.metrics_group}' > /app/config/metrics_group
  #   - echo '${jsonencode(var.server_config)}' > /app/config/server_config.json
  #   - echo 's3://${aws_s3_bucket.deploy_bucket.id}/'
  #   - aws s3 cp s3://${aws_s3_bucket.deploy_bucket.id}/package.zip /app/package.zip
  #   - unzip /app/package.zip -d /app
  #   - sudo chown -R ubuntu:ubuntu /app
  #   - cd /app/{{server_name}} && chmod +x *.sh && ./install.sh 2>&1 >> /app/log/init.log
  # EOT
}

resource "aws_security_group" "instance_security_group" {
  name        = "${local.fullname}-security_group"
  description = "Security group for ${local.fullname}"

  dynamic "ingress" {
    for_each = var.ingress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "${local.fullname}-instance_profile"
  role = aws_iam_role.instance_role.name
}

resource "aws_iam_role" "instance_role" {
  name = "${local.fullname}-instance_role"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "instance_policy" {
  name = "${local.fullname}-instance_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.deploy_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "instance_policy_attachment" {
  name       = "${local.fullname}-instance_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = aws_iam_policy.instance_policy.arn
}
# SSM policy is needed for AWS SSM to work on the instance
resource "aws_iam_policy_attachment" "instance_managed_policy_attachment" {
  name       = "${local.fullname}-instance_managed_policy_attachment"
  roles      = [aws_iam_role.instance_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}


resource "random_id" "deploy_bucket_random_id" { byte_length = 24 }
resource "aws_s3_bucket" "deploy_bucket" {
  bucket = "deploypackage-${random_id.deploy_bucket_random_id.hex}"
  force_destroy = true
}

resource "aws_s3_object" "build_file" {
  bucket = aws_s3_bucket.deploy_bucket.id
  key = "package.zip"
  source = var.package_build_path
  etag = filemd5(var.package_build_path)
}

# # CPU Utilization alarm, will sound when utilization is over 80 percent for two periods
# resource "aws_cloudwatch_metric_alarm" "cpu_utilization_alarm" {
#   alarm_name                = "${local.fullname}-cpu_utilization_alarm"
#   comparison_operator       = "GreaterThanOrEqualToThreshold"
#   evaluation_periods        = "2"
#   metric_name               = "CPUUtilization"
#   namespace                 = "AWS/EC2"
#   period                    = "120" # seconds
#   statistic                 = "Average"
#   threshold                 = "80"
#   alarm_description         = "This metric monitors ec2 cpu utilization"
#   alarm_actions = [var.sns_alarm_topic_arn]
#   dimensions = {
#     InstanceId = aws_instance.example.id
#   }
# }

output "monitor_widget_json" {
  value = <<EOF
  {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "stacked": true,
          "metrics": [
              [ "AWS/EC2", "CPUUtilization", "InstanceId", "${aws_instance.instance.id}", { "region": "us-east-1", "id": "m1", "color": "#555" } ]
          ],
          "region": "us-east-1",
          "period": 300,
          "title": "{{server_name}} CPU Stats",
          "stat": "Average"
      }
  },
  {
      "type": "metric",
      "x": 6,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "view": "timeSeries",
          "metrics": [
              [ "AWS/EC2", "NetworkOut", "InstanceId", "${aws_instance.instance.id}" ],
              [ ".", "NetworkIn", ".", "." ]
          ],
          "region": "us-east-1",
          "title": "{{server_name}} Network Stats",
          "stacked": true
      }
  }
EOF
}

# output "alarm_widget_json" {
#   value = <<EOF
#   {
#       "type": "metric",
#       "x": 0,
#       "y": 0,
#       "width": 6,
#       "height": 3,
#       "properties": {
#           "annotations": {
#               "alarms": [
#                   "${aws_cloudwatch_metric_alarm.cpu_utilization_alarm.arn}"
#               ]
#           },
#           "view": "timeSeries",
#           "title": "{{server_name}} CPU Alarm",
#           "stacked": false
#       }
#   }
# EOF
# }

output "server_ip" { value = "${aws_instance.instance.public_ip}" }
output "instance_id" { value = "${aws_instance.instance.id}" }
''')




dynamodb_tables_header_module = Definition("infrastructure/main.tf", append_if_not_exist=True, text='''
module "database_tables" {
  source = "./database_tables"

  infragroup_fullname = local.infragroup_fullname
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn
}
''')

dynamodb_tables_header_definition = Definition("infrastructure/database_tables/database_tables.tf", append_if_not_exist=True, text='''
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }

locals {
  fullname = "${var.infragroup_fullname}"
}
''')

dynamodb_table_module = Definition("infrastructure/main.tf", append_if_not_exist=True, text='''
output "{{table_name}}_table_id" { value = "${module.database_tables.{{table_name}}_table_id}" }
''')

dynamodb_table_definition = Definition("infrastructure/database_tables/database_tables.tf", append=True, ignore_missing=True, text='''

resource "random_id" "{{table_name}}_table_random_id" { byte_length = 8 }
resource "aws_dynamodb_table" "{{table_name}}_table" {
  name             = "${local.fullname}-{{table_name}}_table-${random_id.{{table_name}}_table_random_id.hex}"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = false

  hash_key         = "{{hash_key}}"
  attribute {
    name = "{{hash_key}}"
    type = "S"
  }
}

output "{{table_name}}_table_id" { value = "${aws_dynamodb_table.{{table_name}}_table.id}" }
output "{{table_name}}_widget_json" {
  value = <<EOF
  {
    "type": "metric",
    "width": 6,
    "height": 6,
    "properties": {
      "metrics": [
        [ "AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", "${aws_dynamodb_table.{{table_name}}_table.id}", { "label": "{{table_name}} Consumed Read" } ],
        [ ".", "ConsumedWriteCapacityUnits", ".", ".", { "label": "{{table_name}} Consumed Write" } ],
      ],
      "view": "timeSeries",
      "stacked": false,
      "region": "us-east-1",
      "period": 300,
      "stat": "Average",
      "title": "{{table_name}} ddb usage"
    }
  }
EOF
}
''')
dynamodb_table_test = Definition("scripts/test.sh", append=True, text='''
TABLE_ID=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{table_name}}_table_id.value')
echo "table id: $TABLE_ID"

# insert/update an item
aws dynamodb update-item --table-name "$TABLE_ID" --region us-east-1 \\
  --key '{"{{hash_key}}": {"S": "mykey"} }' \\
  --update-expression 'SET #var = :var' \\
  --expression-attribute-names '{ "#var": "myvar" }' \\
  --expression-attribute-values '{ ":var": {"S": "myvalue"} }'
# get a single item
aws dynamodb get-item --table-name "$TABLE_ID" --region us-east-1 --key '{"{{hash_key}}": {"S": "mykey"} }' --attributes-to-get '["{{hash_key}}","myvar"]'
# list the table
aws dynamodb scan --table-name "$TABLE_ID" --region us-east-1

''')

indexed_dynamodb_table_module = Definition("infrastructure/main.tf", append_if_not_exist=True, text='''
output "{{table_name}}_table_id" { value = "${module.database_tables.{{table_name}}_table_id}" }
output "{{table_name}}_table_index_id" { value = "${module.database_tables.{{table_name}}_table_index_id}" }
''')
indexed_dynamodb_table_definition = Definition("infrastructure/database_tables/database_tables.tf", append=True, ignore_missing=True, text='''
resource "random_id" "{{table_name}}_table_random_id" { byte_length = 8 }
resource "aws_dynamodb_table" "{{table_name}}_table" {
  name             = "${local.fullname}-{{table_name}}_table-${random_id.{{table_name}}_table_random_id.hex}"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = false

  hash_key         = "{{hash_key}}"

  attribute {
    name = "{{hash_key}}"
    type = "S"
  }

  attribute {
    name = "{{index_key}}"
    type = "S"
  }

  global_secondary_index {
    name               = "${local.fullname}-{{table_name}}_table-index-${random_id.{{table_name}}_table_random_id.hex}"
    hash_key           = "{{index_key}}"
    projection_type    = "INCLUDE"
    non_key_attributes = ["{{hash_key}}"]
  }
}

output "{{table_name}}_table_id" { value = "${aws_dynamodb_table.{{table_name}}_table.id}" }
output "{{table_name}}_table_index_id" { value = "${local.fullname}-{{table_name}}_table-index-${random_id.{{table_name}}_table_random_id.hex}" }
output "{{table_name}}_widget_json" {
  value = <<EOF
  {
    "type": "metric",
    "width": 6,
    "height": 6,
    "properties": {
      "metrics": [
          [ "AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", "${aws_dynamodb_table.{{table_name}}_table.id}", { "label": "{{table_name}} Consumed Read" } ],
          [ ".", "ConsumedWriteCapacityUnits", ".", ".", { "label": "{{table_name}} Consumed Write" } ],
      ],
      "view": "timeSeries",
      "stacked": false,
      "region": "us-east-1",
      "period": 300,
      "stat": "Average",
      "title": "{{table_name}} ddb usage"
    }
  }
EOF
}
''')



firehose_s3_module = Definition("infrastructure/main.tf", append=True, text='''
module "{{firehose_name}}" {
  source = "./{{firehose_name}}"
  infragroup_fullname = local.infragroup_fullname
  sns_alarm_topic_arn = aws_sns_topic.alarm_topic.arn
}
output "{{firehose_name}}_stream_name" { value = module.{{firehose_name}}.firehose_stream_name }
output "{{firehose_name}}_bucket_id" { value = module.{{firehose_name}}.bucket_id }

''')

firehose_s3_definition = Definition("infrastructure/{{firehose_name}}/{{firehose_name}}.tf", text='''
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }

locals {
  fullname = "${var.infragroup_fullname}-{{firehose_name}}"
}

resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream" {
  name        = "${local.fullname}"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.data_bucket.arn
  }
}

resource "random_id" "data_bucket_random_id" { byte_length = 8 }
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${local.fullname}-databkt-${random_id.data_bucket_random_id.hex}"
}

resource "aws_iam_role" "firehose_role" {
  name               = "${local.fullname}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "firehose.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "firehose_policy" {
  name        = "${local.fullname}-policy"
  path        = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      "Effect" = "Allow",
      "Action" = [
        "logs:PutLogEvents"
      ],
      "Resource" = [
        "arn:aws:logs:us-east-1:*:log-group:/aws/kinesisfirehose/${aws_kinesis_firehose_delivery_stream.extended_s3_stream.name}:log-stream:*",
      ]
    }, {
      "Effect" = "Allow",
      "Action" = [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:PutObject"
      ],
      "Resource" = [
        "arn:aws:s3:::${aws_s3_bucket.data_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.data_bucket.id}/*"
      ]
    }]
  })
}

resource "aws_cloudwatch_log_group" "firehose_log_group" {
  name = "/aws/kinesisfirehose/${aws_kinesis_firehose_delivery_stream.extended_s3_stream.name}"
  retention_in_days = 30
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = aws_iam_policy.firehose_policy.arn
}

output "firehose_stream_name" { value = aws_kinesis_firehose_delivery_stream.extended_s3_stream.name }
output "bucket_id" { value = aws_s3_bucket.data_bucket.id }

# output "monitor_widget_json" {
#   value = <<EOF
#   {
#     "height": 6,
#     "width": 6,
#     "type": "metric",
#     "properties": {
#       "metrics": [
#         [ "${local.metrics_group}", "lambda-success", { "color": "#98df8a", "label": "lambda-success" } ],
#         [ ".", "lambda-error", { "color": "#ffbb78" } ],
#         [ ".", "lambda-crash", { "color": "#ff9896" } ]
#       ],
#       "view": "timeSeries",
#       "stacked": true,
#       "region": "us-east-1",
#       "stat": "Sum",
#       "period": 300,
#       "title": "{{firehose_name}} metrics"
#     }
#   }
# EOF
# }

''')

firehose_s3_test = Definition("scripts/test.sh", append=True, text='''
FIREHOSE_STREAM_NAME=$(cat infrastructure/terraform.tfstate | jq -r '.outputs.{{firehose_name}}_stream_name.value')
echo "putting event into firehose: $FIREHOSE_STREAM_NAME"
aws firehose put-record --region us-east-1 --delivery-stream-name $FIREHOSE_STREAM_NAME --record '{"Data":"SGVsbG8gd29ybGQhCg=="}'

''')

lambda_schedule_definition = Definition("infrastructure/{{lambda_name}}/{{lambda_name}}.tf", append=True, text='''
# event bridge scheduled event
resource "random_id" "event_api_key" { byte_length = 32 }
resource "aws_cloudwatch_event_rule" "lambda_recurring_event" {
  name = "${local.fullname}-recurring_event"
  schedule_expression = "rate(1 day)"
}
resource "aws_cloudwatch_event_target" "lambda_recurring_event_target" {
  rule = aws_cloudwatch_event_rule.lambda_recurring_event.name
  arn = aws_lambda_function.lambda_function.arn
  input = jsonencode({
    body = jsonencode({
      action = "/{{lambda_name}}/hello"
      event_api_key = random_id.event_api_key.hex
    })
  })
}
resource "aws_lambda_permission" "lambda_recurring_event_permission" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.lambda_recurring_event.arn
}
''')

s3_bucket_definition = Definition("infrastructure/{{module_name}}/{{module_name}}.tf", append=True, text='''

locals {
  {{bucket_name}}_fullname = replace("${var.infragroup_fullname}-{{bucket_name}}", "_", "-")
}

resource "random_id" "{{bucket_name}}_random_id" { byte_length = 8 }
resource "aws_s3_bucket" "{{bucket_name}}" {
  bucket = "${local.{{bucket_name}}_fullname}-databkt-${random_id.{{bucket_name}}_random_id.hex}"
}

output "bucket_id" { value = aws_s3_bucket.{{bucket_name}}.id }

resource "random_id" "{{bucket_name}}_access_log_bucket_random_id" { byte_length = 8 }
resource "aws_s3_bucket" "{{bucket_name}}_access_log_bucket" {
  bucket = "${local.{{bucket_name}}_fullname}-logbkt-${random_id.{{bucket_name}}_access_log_bucket_random_id.hex}"
}
resource "aws_s3_bucket_metric" "{{bucket_name}}_metric_filter" {
  bucket = aws_s3_bucket.{{bucket_name}}.id
  name   = "${local.{{bucket_name}}_fullname}-databkt-filter"
}
resource "aws_s3_bucket_lifecycle_configuration" "{{bucket_name}}_access_log_bucket_lifecycle_configuration" {
  bucket = aws_s3_bucket.{{bucket_name}}_access_log_bucket.id

  rule {
    id = "expiration_rule"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }
    expiration {
      days = 90
    }
  }
}

resource "aws_s3_bucket_policy" "{{bucket_name}}_access_log_bucket_policy" {
  bucket = aws_s3_bucket.{{bucket_name}}_access_log_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "logging.s3.amazonaws.com"
      }
      Action = "s3:PutObject"
      Resource = "${aws_s3_bucket.{{bucket_name}}_access_log_bucket.arn}/logs/*"
      Condition = {
        ArnLike = {
          "aws:SourceArn" = aws_s3_bucket.{{bucket_name}}.arn
        }
      }
    }]
  })
}

resource "aws_s3_bucket_logging" "{{bucket_name}}_logging" {
  bucket = aws_s3_bucket.{{bucket_name}}.id
  target_bucket = aws_s3_bucket.{{bucket_name}}_access_log_bucket.id
  target_prefix = "logs/"
}

output "access_logging_bucket_id" { value = aws_s3_bucket.{{bucket_name}}_access_log_bucket.id }

output "monitor_widget_json" {
  value = <<EOF
  {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
          "metrics": [
              [ "AWS/S3", "AllRequests", "BucketName", "${aws_s3_bucket.{{bucket_name}}.id}", "FilterId", "${aws_s3_bucket_metric.{{bucket_name}}_metric_filter.name}" ],
              [ ".", "4xxErrors", ".", ".", ".", "." ],
              [ ".", "5xxErrors", ".", ".", ".", ".", { "color": "#d62728" } ]
          ],
          "view": "timeSeries",
          "stacked": false,
          "region": "us-east-1",
          "stat": "Average",
          "period": 300
      }
  }
EOF
}
''')

terraform_s3_backend = Definition("infrastructure/main.tf", append_if_not_exist=True, text='''
terraform {
  backend "s3" {
    bucket = "{{state_bucket}}"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
''')

githubactions_deploy_workflow = Definition(".github/workflows/deploy.yml", text='''name: Infra Deploy

on:
  push:
    branches:
      - deploy

jobs:
  deploy_infra:
    runs-on: ubuntu-22.04
    permissions:
      id-token: write # required to use OIDC authentication
      contents: read
    steps:
      - uses: actions/checkout@v3
      - uses: aws-actions/configure-aws-credentials@v1
        name: configure aws credentials
        with:
          role-to-assume: {{role_arn}}
          role-duration-seconds: 900
          aws-region: us-east-1
      - name: build
        run: |
          touch .env
          make build
      - name: deploy
        run: |
          ./infrastructure/tools/deploy.sh -autodeploy

''')

ses_domain_module = Definition("infrastructure/main.tf", append=True, text='''
resource "aws_ses_domain_identity" "ses_domain_identity" {
  domain = local.domain_name
}

resource "aws_ses_domain_dkim" "ses_domain_dkim" {
  domain = local.domain_name
}
''')






####################################################################################################
# template definitions
####################################################################################################


infra_base_template = TemplateDefinition('{infra_name} infra', {
  'company_name': r"^[a-zA-Z_]+$",
  'infra_name': r"^[a-zA-Z_][a-zA-Z0-9_\-]+$"
}, [
  base_terraform_main,
  base_backend_beta_config,
  base_backend_prod_config,
  base_makefile,
  base_dockerfile,
  base_docker_run,
  base_envfile,
  base_aws_authenticate,
  base_install_tooling,
  base_create_keys,
  base_trigger_codebuild,
  base_deploy,
  base_server_state,
  base_ssh_into,
  base_ssm_into,
  base_test_sh,
  base_gitignore,
], '''
base infrastructure established...

to run:
  put your aws configuration properties into `docker/.env`, such as: `AWS_PROFILE=my_profile`
  execute with `./docker/run`

[optional] set up your s3 backend config:
  Change the backend in main.tf to be `backend "s3"`,
  and put the following into your backend-config.beta.hcl:
```
bucket = "my-tfstate-bucket"
key    = "{company_name}/{infra_name}/beta/terraform.tfstate"
region = "us-east-1"
```

deploy with `weasel deploy`
destroy and clean with `weasel destroy clean`
''')


ec2_server_template = TemplateDefinition('{server_name} server', {
  'server_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  ec2_server_module,
  ec2_server_makefile,
  ec2_server_definition,
  ec2_server_install_sh,
  ec2_server_startup_sh,
  ec2_server_reboot_sh,
  ec2_server_daemonize_sh,
  ec2_server_keepalive_sh,
  ec2_server_awslogs_cfg,
  ec2_server_cwagent_cfg,
], '''
ec2 server scaffolding established...
build with `weasel build_{server_name}_package`
Use SSM to login to the server: `./scripts/ssm-into.sh {server_name}`
''')


windows_ec2_server_template = TemplateDefinition('{server_name} windows server', {
  'server_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  ec2_server_module,
  ec2_server_makefile,
  windows_ec2_server_definition,
  ec2_server_awslogs_cfg,
], '''
windows ec2 server scaffolding established...
build with `weasel build_{server_name}_package`.
make sure you have an rdp client installed to log into the server.
download the rdp file from aws console.
run the following command to get your login password:
`aws ec2 get-password-data --instance-id "<instance-id>" --priv-launch-key .keys/{server_name}_key --region us-east-1`
rdp into the server to access it.

helpful one-liner to install chrome from powershell:
`$Path = $env:TEMP; $Installer = 'chrome_installer.exe'; Invoke-WebRequest -Uri 'http://dl.google.com/chrome/install/375.126/chrome_installer.exe' -OutFile $Path\\$Installer; Start-Process -FilePath $Path\\$Installer -Args '/silent /install' -Verb RunAs -Wait; Remove-Item -Path $Path\\$Installer`
''')


bastion_ec2_server_template = TemplateDefinition('{server_name} bastion server', {
  'server_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  bastion_ec2_server_module,
  ec2_server_makefile,
  bastion_ec2_server_definition,
  bastion_ec2_server_install_sh,
  bastion_ec2_server_startup_sh,
  ec2_server_reboot_sh,
  ec2_server_daemonize_sh,
  ec2_server_keepalive_sh,
  ec2_server_awslogs_cfg,
  ec2_server_cwagent_cfg,
  bastion_ec2_server_rundocker_sh,
  bastion_ec2_server_dockercompose_template,
], '''
bastion ec2 server scaffolding established...
build with `weasel build_{server_name}_package`
Use SSM to login to the server: `./scripts/ssm-into.sh {server_name}`

this server is configured to be protected behind an ALB and a CloudFront distribution, with a strict security group preventing direct access
keep in mind that ALBs and EC2 servers are expensive to run!
''')


website_s3_bucket_template = TemplateDefinition('{website_name} bucket', {
  'website_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'domain_name': r"^[a-zA-Z_][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+$",
}, [
  website_s3_module,
  website_s3_definition,
  website_s3_dockerfile,
  website_s3_docker_run,
  website_s3_build,
  website_s3_makefile,
  website_s3_package_json,
  website_s3_webpack_config,
  website_s3_babelrc,
  website_s3_index_js,
  website_s3_index_html,
  website_s3_app_js,
  website_s3_home_js,
  website_s3_styles_css,
  website_s3_test,
], '''
website bucket scaffolding established...
build the website by doing:
  cd src/{website_name}
  chmod +x docker/run
  ./docker/run npm i -dev
  ./docker/run npm run build
then deploy your infra as normal
''')


base_lambda_template = TemplateDefinition('{lambda_name} lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  base_lambda_definition,
  base_lambda_makefile,
  base_lambda_module,
  base_lambda_main,
  base_lambda_lib,
  base_lambda_routes,
  base_lambda_build,
  base_lambda_requirements,
  base_lambda_test,
], '''
basic lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
''', '''

test your lambda by invoking:
  aws lambda invoke --region us-east-1 \\
    --function-name <LAMBDA_FULL_NAME> \\
    --payload $(echo '{"rawPath":"/<MYLAMBDA_NAME>/hello","body":"{\\"msg\\":\\"yes\\"}"}' | base64 -w 0) \\
    /dev/stdout

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


graphql_lambda_template = TemplateDefinition('{lambda_name} gql lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  base_lambda_definition,
  graphql_lambda_makefile,
  base_lambda_module,
  graphql_lambda_main,
  graphql_lambda_authorization,
  graphql_lambda_schema,
  graphql_lambda_unit_test,
  base_lambda_build,
  graphql_lambda_requirements,
], '''
graphql lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
''', '''

test your graphql lambda by invoking:
  aws lambda invoke --region us-east-1 \\
    --function-name <LAMBDA_FULL_NAME> \\
    --payload $(echo '{ "body": "{\\"query\\":\\"{ hello }\\"}" }' | base64 -w 0) \\
    /dev/stdout

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


api_lambda_template = TemplateDefinition('{lambda_name} lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  api_lambda_definition,
  graphql_lambda_makefile,
  api_lambda_module,
  base_lambda_main,
  base_lambda_lib,
  base_lambda_routes,
  base_lambda_build,
  base_lambda_requirements,
  api_lambda_test,
  api_lambda_unit_test,
], '''
api lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
test the lambda by executing `./scripts/test.sh`

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


api_graphql_lambda_template = TemplateDefinition('{lambda_name} gql lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  api_lambda_definition,
  graphql_lambda_makefile,
  api_lambda_module,
  graphql_lambda_main,
  graphql_lambda_authorization,
  graphql_lambda_schema,
  graphql_lambda_unit_test,
  base_lambda_build,
  graphql_lambda_requirements,
  graphql_lambda_test,
], '''
api lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
test the lambda by executing `./scripts/test.sh`

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


sqs_lambda_template = TemplateDefinition('{lambda_name} lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  sqs_lambda_definition,
  base_lambda_makefile,
  sqs_lambda_module,
  sqs_lambda_main,
  base_lambda_lib,
  base_lambda_routes,
  base_lambda_build,
  base_lambda_requirements,
  sqs_lambda_test,
], '''
sqs lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
test the lambda by executing `./scripts/test.sh`

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


dynamodb_table_template = TemplateDefinition('{table_name} table', {
  'table_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'hash_key': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  dynamodb_tables_header_module,
  dynamodb_tables_header_definition,
  dynamodb_table_module,
  dynamodb_table_definition,
  dynamodb_table_test,
], '''
dynamodb table scaffolded...
test the table by executing `./scripts/test.sh`
use the table with PynamoDB:
  $ pip install pynamodb
then:

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
class {table_name}(Model):
  class Meta:
    table_name = os.environ.get('{table_name}_TABLE')
  {hash_key} = UnicodeAttribute(hash_key=True)

''', '''
remember to add to the policy the following:
{
  "Effect" = "Allow",
  "Action" = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource" = [
    "arn:aws:dynamodb:us-east-1:*:table/${var.arg_table}",
  ]
}


enjoy responsibly...
''')


indexed_dynamodb_table_template = TemplateDefinition('{table_name} table', {
  'table_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'hash_key': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'index_key': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  dynamodb_tables_header_module,
  dynamodb_tables_header_definition,
  indexed_dynamodb_table_module,
  indexed_dynamodb_table_definition,
  dynamodb_table_test,
], '''
indexed dynamodb table scaffolded...
test the table by executing `./scripts/test.sh`
use the table with PynamoDB:
  $ pip install pynamodb
then:

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
class {table_name}(Model):
  class Meta:
    table_name = os.environ.get('{table_name}_TABLE')
  {hash_key} = UnicodeAttribute(hash_key=True)

''', '''
remember to add to the policy the following:
{
  "Effect" = "Allow",
  "Action" = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource" = [
    "arn:aws:dynamodb:us-east-1:*:table/${var.arg_table}",
  ]
}


enjoy responsibly...
''')


usermanager_ddb_table_template = TemplateDefinition('{lambda_name} usermanager lambda', {
  'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'table_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  dynamodb_tables_header_module,
  dynamodb_tables_header_definition,
  indexed_dynamodb_table_module,
  indexed_dynamodb_table_definition,
  dynamodb_table_test,
  usermanager_lambda_schema,
  usermanager_lambda_models,
  usermanager_lambda_requirements,
  usermanager_lambda_test,
  usermanager_lambda_unit_test,
], '''
usermanager dynamodb table scaffolded...
graphql endpoint additions added to {table_name} lambda...
test the user system by executing `./scripts/test.sh`

''', '''
remember to add to the policy the following:
{
  "Effect" = "Allow",
  "Action" = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource" = [
    "arn:aws:dynamodb:us-east-1:*:table/${var.arg_table}",
  ]
}

and add the env variables to the lambda terraform:
  resource "random_id" "random_api_authentication_secret_key" { byte_length = 64 }
  ...
  API_AUTHORIZATION_SECRET_KEY = random_id.random_api_authentication_secret_key.hex
  API_DOMAIN_NAME = "example.com"
  USERS_TABLE = var.users_table


enjoy responsibly...
''', fixed_args={ 'hash_key': 'id', 'index_key': 'email' })


crud_ddb_table_template = TemplateDefinition('{lambda_name} lambda', {
  'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'table_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  dynamodb_tables_header_module,
  dynamodb_tables_header_definition,
  indexed_dynamodb_table_module,
  indexed_dynamodb_table_definition,
  dynamodb_table_test,
  crud_lambda_authorization,
  crud_lambda_models,
  crud_lambda_schema,
  crud_lambda_test,
  crud_lambda_unit_test,
], '''
CRUD dynamodb table scaffolded...
graphql endpoint additions added to {table_name} lambda...
test the crud apis by executing `./scripts/test.sh`

''', '''
remember to add to the policy the following:
{
  "Effect" = "Allow",
  "Action" = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource" = [
    "arn:aws:dynamodb:us-east-1:*:table/${var.arg_table}"
  ]
}

enjoy responsibly...
''', fixed_args={ 'hash_key': 'id', 'index_key': 'owner_id' })


singleton_crud_ddb_table_template = TemplateDefinition('{lambda_name} lambda', {
  'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
  'table_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$",
}, [
  dynamodb_tables_header_module,
  dynamodb_tables_header_definition,
  indexed_dynamodb_table_module,
  indexed_dynamodb_table_definition,
  dynamodb_table_test,
  crud_lambda_authorization,
  crud_lambda_models,
  singleton_crud_lambda_schema,
  crud_lambda_test,
  singleton_crud_lambda_unit_test,
], '''
singleton CRUD dynamodb table scaffolded...
graphql endpoint additions added to {table_name} lambda...
test the crud apis by executing `./scripts/test.sh`

''', '''
remember to add to the policy the following:
{
  "Effect" = "Allow",
  "Action" = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource" = [
    "arn:aws:dynamodb:us-east-1:*:table/${var.arg_table}/*"
  ]
}

enjoy responsibly...
''', fixed_args={ 'hash_key': 'id' })


authn_lambda_template = TemplateDefinition('{lambda_name} lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  authn_lambda_definition,
  base_lambda_makefile,
  authn_lambda_module,
  base_lambda_main,
  graphql_lambda_authorization,
  base_lambda_lib,
  authn_lambda_routes,
  base_lambda_build,
  base_lambda_requirements,
  authn_lambda_test,
], '''
authn lambda scaffolded...
build the lambda package with `weasel build_{lambda_name}`
''', '''
test your lambda with: ./scripts/test.sh

Use the following command to tail logs in cli:
  aws logs tail /aws/lambda/<LAMBDA_FULL_NAME> --follow --region us-east-1 &
''')


base_ecr_image_template = TemplateDefinition('{lambda_name} lambda', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  base_ecr_image_module,
  base_ecr_image_definition,
  base_ecr_image_buildspec,
  base_ecr_image_dockerfile,
  base_ecr_image_build,
  base_ecr_image_module_variable,
], '''
ECR image template added to {lambda_name}...

In your `infrastructure/main.tf`, add the following variable to your lambda module:
```
  lambda_image_repo_url = module.{lambda_name}_image
```

And in your `infrastructure/{lambda_name}/{lambda_name}.tf`, replace `runtime,handler,filename,source_code_hash` with:
''', '''
```
  package_type = "Image"
  image_uri = "${var.lambda_image_repo_url}:latest"
  source_code_hash = filebase64sha256(var.lambda_build_path)
```
''')


base_fargate_server_template = TemplateDefinition('{fargate_server} server', { 'fargate_server': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  base_fargate_server_module,
  base_fargate_server_app_template,
  base_fargate_server_network,
  base_fargate_server_instance,
  base_fargate_dockerfile,
  base_fargate_build,
  base_fargate_makefile,
  Definition(filepath="src/{{fargate_server}}/buildspec.yaml", text=base_ecr_image_buildspec.text),
  Definition(filepath="infrastructure/{{fargate_server}}/ecr_image.tf", text=base_ecr_image_definition.text).but_replace('''
variable "name" { type = string }
variable "metrics_path" { type = string }
variable "infragroup_fullname" { type = string }
variable "sns_alarm_topic_arn" { type = string }
variable "package_build_path" { type = string }


locals {
  fullname = "${var.infragroup_fullname}-${var.name}"
  metrics_group = "${var.metrics_path}/${var.name}"
}


data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
''', '''
variable "package_build_path" { type = string }
'''),
], '''
fargate server scaffolded...
''', '''
connect to it via the server url after deploying.
''')


firehose_s3_template = TemplateDefinition('{firehose_name} firehose', {
  'firehose_name': r"^[a-zA-Z][a-zA-Z0-9]+$",
}, [
  firehose_s3_module,
  firehose_s3_definition,
  firehose_s3_test,
], '''
s3-backed firehose scaffolded...
test the firehose by executing `./scripts/test.sh`
''', '''
use the firehose with Python:

import boto3
firehose_client = boto3.client('firehose', region_name='us-east-1')
firehose_client.put_record(
  DeliveryStreamName='STREAM NAME HERE!!!!',
  Record={ 'Data': b'bytes' })


remember to add the following policy:
{
  "Effect" = "Allow",
  "Action" = [
    "firehose:PutRecord",
  ],
  "Resource" = [
    "arn:aws:firehose:us-east-1:*:deliverystream/*",
  ]
}


drink up...
''')


s3_bucket_template = TemplateDefinition('{bucket_name} s3 bucket', { 'module_name': r"^[a-zA-Z_][a-zA-Z0-9_\-]+$", 'bucket_name': r"^[a-zA-Z_][a-zA-Z0-9_]{1,15}$" }, [
  s3_bucket_definition,
], '''
s3 bucket created in module {module_name}...
the bucket has access logging and metrics are enabled by default
''')

lambda_schedule_template = TemplateDefinition('{lambda_name} lambda schedule event', { 'lambda_name': r"^[a-zA-Z_][a-zA-Z0-9_]+$" }, [
  lambda_schedule_definition,
], '''
lambda event bridge job schedule created on a 1-per-day...
add `EVENT_API_KEY_HASH = sha256(random_id.event_api_key.hex)` to your lambda env to verify that the invocation came from the eventbridge
''')

githubactions_deploy_template = TemplateDefinition('github actions deploy', { 'role_arn': r"^\S+$", 'state_bucket': r"^\S{3,63}$" }, [
  terraform_s3_backend,
  githubactions_deploy_workflow,
], '''
Follow this guide for how to set up the role:
https://benoitboure.com/securely-access-your-aws-resources-from-github-actions

also make sure to create your state bucket
!!! Make sure your bucket has all access disabled !!!
your aws role should have sufficient permissions to access the bucket
no public access is necessary...

once your role and state bucket are set up, you should just push to your `deploy` branch, and everything will deploy automatically

use `aws s3 cp s3://{state_bucket}/terraform.tfstate infrastructure/terraform.tfstate` in your test.sh to keep it working
''')

ses_domain_template = TemplateDefinition('ses domain', {}, [
  ses_domain_module,
], '''
Make sure to enter your AWS account and get the necessary DKIM records to very.
After verifying, make sure to add a test identity, before leaving sandbox and entering live.
''', '''
insert SES emails with:
```
ses_client = boto3.client('ses', region_name='us-east-1')
res = ses_client.send_email(
  Destination={ 'ToAddresses': [ email_address ] },
  Source='noreply@example.org',
  Message={
    'Subject': { 'Charset': 'UTF-8', 'Data': email_subject },
    'Body': { 'Html': { 'Charset': 'UTF-8', 'Data': email_body } },
  },
)
```

and add the following permission to your lambda:
{
  "Effect" = "Allow",
  "Action" = "ses:SendEmail",
  Resource = "*"
},
''')


####################################################################################################
# main
####################################################################################################

def main():
  # parse arguments
  parser = argparse.ArgumentParser(prog='stonemill', description='A terraform scaffolding tool')
  parser.add_argument('--infra-base', nargs=2, help='creates the starter Makefile and main.tf;\t stonemill --infra-base mycompany myproject')
  parser.add_argument('--lambda-function', nargs=1, help='creates a py3 lambda;\t stonemill --lambda-function my_lambda')
  parser.add_argument('--api-lambda-function', nargs=1, help='creates a py3 lambda with an api gateway;\t stonemill --api-lambda-function my_lambda')
  parser.add_argument('--sqs-lambda-function', nargs=1, help='creates a py3 lambda with an sqs input queue;\t stonemill --sqs-lambda-function my_lambda')
  parser.add_argument('--gql-lambda-function', nargs=1, help='creates a py3 graphql lambda;\t stonemill --gql-lambda-function my_lambda')
  parser.add_argument('--api-gql-lambda-function', nargs=1, help='creates a py3 graphql lambda with an api gateway;\t stonemill --api-gql-lambda-function my_lambda')
  parser.add_argument('--authn-lambda', nargs=1, help='creates a py3 lambda;\t stonemill --authn-lambda my_lambda')
  parser.add_argument('--ecr-image-autobuild', nargs=1, help='augments a lambda definition with an ecr-image which auto-builds with codebuild;\n\t defines a dockerfile for you to quickly scaffold complex lambda builds;\n\t stonemill --ecr-image-autobuild my_lambda')
  parser.add_argument('--website-s3-bucket', nargs=2, help='creates an s3 bucket for hosting a react site;\t stonemill --website-s3-bucket my_website myspecialfrontend.com')
  parser.add_argument('--ec2-server', nargs=1, help='creates an ec2 server with ssm access;\t stonemill --ec2-server my_server')
  parser.add_argument('--windows-ec2-server', nargs=1, help='creates a windows ec2 server;\t stonemill --windows-ec2-server my_windows_server')
  parser.add_argument('--bastion-ec2-server', nargs=1, help='creates a bastion ec2 server with CF and ALB;\t stonemill --bastion-ec2-server my_bastion')
  parser.add_argument('--fargate-server', nargs=1, help='creates a fargate server with an ALB;\t stonemill --fargate-server my_application')
  parser.add_argument('--dynamodb-table', nargs=2, help='creates a basic dynamodb table;\t stonemill --dynamodb-table my_accounts account_id')
  parser.add_argument('--indexed-dynamodb-table', nargs=2, help='creates a dynamodb table with a global secondary index;\t stonemill --indexed-dynamodb-table my_accounts account_id email')
  parser.add_argument('--usermanager-ddb-table', nargs=2, help='creates a users dynamodb table with graphql endpoints for addUser and login;\n\t uses strong password salting and hashing for security;\t stonemill --usermanager-ddb-table my_lambda users')
  parser.add_argument('--crud-ddb-table', nargs=2, help='creates a dynamodb table with graphql endpoints for Create/Read/Update/Delete/List;\n\t uses uuid4 for ids and has strong authentication on the user;\t stonemill --crud-ddb-table my_lambda my_item')
  parser.add_argument('--singleton-crud-ddb-table', nargs=2, help='creates a dynamodb table with graphql endpoints for Create/Read/Update;\n\t only one singleton exists per user;\n\t uses uuid4 for ids and has strong authentication on the user;\t stonemill --singleton-crud-ddb-table my_lambda my_singleton')
  parser.add_argument('--firehose-s3', nargs=1, help='creates a kinesis firehose that puts to an s3 bucket;\t stonemill --firehose-s3 my_firehose_name')
  parser.add_argument('--s3-bucket', nargs=2, help='creates an s3 bucket in an existing module, with access logging and metrics enabled;\t stonemill --s3-bucket my_lambda data_bucket')
  parser.add_argument('--lambda-schedule-event', nargs=1, help='creates an eventbridge job that triggers lambda on a schedule;\t stonemill --lambda-schedule-event my_lambda')
  parser.add_argument('--githubactions-deploy', nargs=2, help='creates the deployment workflows for github actions to push the terraform infrastructure;\t stonemill --githubactions-deploy "arn:aws:iam::123456789012:role/GithubActionsAccessRole" "tfstate-abcdef0123456789"\n\t follow this guide for how to create your role and secure it to only allow github access: https://benoitboure.com/securely-access-your-aws-resources-from-github-actions')
  parser.add_argument('--ses-domain', action='store_true', help='creates the DKIM records to start the validation process for an SES domain;\t stonemill --ses-domain')
  args = parser.parse_args()

  if args.infra_base:
    template_args = infra_base_template.parse_arguments(company_name=args.infra_base[0], infra_name=args.infra_base[1])
    infra_base_template.mill_template(template_args)

  elif args.ec2_server:
    template_args = ec2_server_template.parse_arguments(server_name = args.ec2_server[0])
    ec2_server_template.mill_template(template_args)

  elif args.windows_ec2_server:
    template_args = windows_ec2_server_template.parse_arguments(server_name = args.windows_ec2_server[0])
    windows_ec2_server_template.mill_template(template_args)

  elif args.bastion_ec2_server:
    template_args = bastion_ec2_server_template.parse_arguments(server_name = args.bastion_ec2_server[0])
    bastion_ec2_server_template.mill_template(template_args)

  elif args.website_s3_bucket:
    template_args = website_s3_bucket_template.parse_arguments(website_name = args.website_s3_bucket[0], domain_name = args.website_s3_bucket[1])
    website_s3_bucket_template.mill_template(template_args)

  elif args.lambda_function:
    template_args = base_lambda_template.parse_arguments(lambda_name = args.lambda_function[0])
    base_lambda_template.mill_template(template_args)

  elif args.gql_lambda_function:
    template_args = graphql_lambda_template.parse_arguments(lambda_name = args.gql_lambda_function[0])
    graphql_lambda_template.mill_template(template_args)

  elif args.api_gql_lambda_function:
    template_args = api_graphql_lambda_template.parse_arguments(lambda_name = args.api_gql_lambda_function[0])
    api_graphql_lambda_template.mill_template(template_args)

  elif args.api_lambda_function:
    template_args = api_lambda_template.parse_arguments(lambda_name = args.api_lambda_function[0])
    api_lambda_template.mill_template(template_args)

  elif args.sqs_lambda_function:
    template_args = sqs_lambda_template.parse_arguments(lambda_name = args.sqs_lambda_function[0])
    sqs_lambda_template.mill_template(template_args)

  elif args.authn_lambda:
    template_args = authn_lambda_template.parse_arguments(lambda_name = args.authn_lambda[0])
    authn_lambda_template.mill_template(template_args)

  elif args.ecr_image_autobuild:
    template_args = base_ecr_image_template.parse_arguments(lambda_name = args.ecr_image_autobuild[0])
    base_ecr_image_template.mill_template(template_args)

  elif args.dynamodb_table:
    template_args = dynamodb_table_template.parse_arguments(table_name = args.dynamodb_table[0], hash_key = args.dynamodb_table[1])
    dynamodb_table_template.mill_template(template_args)

  elif args.indexed_dynamodb_table:
    template_args = indexed_dynamodb_table_template.parse_arguments(table_name = args.indexed_dynamodb_table[0], hash_key = args.indexed_dynamodb_table[1], index_key = args.indexed_dynamodb_table[2])
    indexed_dynamodb_table_template.mill_template(template_args)

  elif args.usermanager_ddb_table:
    template_args = usermanager_ddb_table_template.parse_arguments(lambda_name = args.usermanager_ddb_table[0], table_name = args.usermanager_ddb_table[1])
    usermanager_ddb_table_template.mill_template(template_args)

  elif args.crud_ddb_table:
    template_args = crud_ddb_table_template.parse_arguments(lambda_name = args.crud_ddb_table[0], table_name = args.crud_ddb_table[1])
    crud_ddb_table_template.mill_template(template_args)

  elif args.singleton_crud_ddb_table:
    template_args = singleton_crud_ddb_table_template.parse_arguments(lambda_name = args.crud_ddb_table[0], table_name = args.crud_ddb_table[1])
    singleton_crud_ddb_table_template.mill_template(template_args)

  elif args.fargate_server:
    template_args = base_fargate_server_template.parse_arguments(fargate_server = args.fargate_server[0])
    base_fargate_server_template.mill_template(template_args)

  elif args.firehose_s3:
    template_args = firehose_s3_template.parse_arguments(firehose_name = args.firehose_s3[0])
    firehose_s3_template.mill_template(template_args)

  elif args.s3_bucket:
    template_args = s3_bucket_template.parse_arguments(module_name = args.s3_bucket[0], bucket_name = args.s3_bucket[1])
    s3_bucket_template.mill_template(template_args)

  elif args.lambda_schedule_event:
    template_args = lambda_schedule_template.parse_arguments(lambda_name = args.lambda_schedule_event[0])
    lambda_schedule_template.mill_template(template_args)

  elif args.githubactions_deploy:
    template_args = githubactions_deploy_template.parse_arguments(role_arn = args.githubactions_deploy[0], state_bucket = args.githubactions_deploy[1])
    githubactions_deploy_template.mill_template(template_args)

  elif args.ses_domain:
    template_args = ses_domain_template.parse_arguments()
    ses_domain_template.mill_template(template_args)

  else:
    parser.print_help()

if __name__ == '__main__':
  main()
