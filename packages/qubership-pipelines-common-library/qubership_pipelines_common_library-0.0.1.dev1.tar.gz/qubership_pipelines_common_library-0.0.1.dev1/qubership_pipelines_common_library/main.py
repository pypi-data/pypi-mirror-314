# Copyright 2024 NetCracker Technology Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys, logging, click, urllib3

from v1.execution.exec_logger import ExecutionLogger

from operations.jenkins.get_job_config import GetJobConfig
from operations.jenkins.disable_job import DisableJob
from operations.jenkins.enable_job import EnableJob
from operations.jenkins.run_pipeline import RunPipeline as JenkinsRunPipeline
from operations.git.get_file import GetFile
from operations.git.run_pipeline import RunPipeline
from operations.git.get_pipeline import GetPipeline
from v1.utils.utils_file import UtilsFile
from v1.utils.utils_context import init_context


DEFAULT_CONTEXT_FILE_PATH = 'context.yaml'

@click.group(chain=True)
def cli():
    logging.basicConfig(stream=sys.stdout, format=ExecutionLogger.DEFAULT_FORMAT, level=logging.INFO)
    # add this folder to path
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_path)
    logging.info(f"Current path: {current_path}")
    # suppress InsecureRequestWarning: Unverified HTTPS request is being made to host
    urllib3.disable_warnings()


@cli.command("init_context")
@click.option('--context_path', required=False, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def init_context_cmd(context_path):
    logging.info("Default context.yaml creation starting")
    init_context(context_path)
    context = UtilsFile.read_yaml(context_path)
    logging.info(context)

@cli.command("get_job_config")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _get_job_config(context_path):
    logging.info("CLI get_job operation calling for %s", context_path)
    command = GetJobConfig(context_path)
    command.run()

@cli.command("enable_job")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _enable_job(context_path):
    logging.info("CLI enable_job operation calling for %s", context_path)
    command = EnableJob(context_path)
    command.run()

@cli.command("disable_job")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _disable_job(context_path):
    logging.info("CLI disable_job operation calling for %s", context_path)
    command = DisableJob(context_path)
    command.run()

@cli.command("get_file")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _get_file(context_path):
    logging.info("CLI get_file operation calling for %s", context_path)
    command = GetFile(context_path)
    command.run()

@cli.command("run_pipeline")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _run_pipeline(context_path):
    logging.info("CLI run_pipeline operation calling for %s", context_path)
    command = RunPipeline(context_path)
    command.run()

@cli.command("get_pipeline")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _get_pipeline(context_path):
    logging.info("CLI get_pipeline operation calling for %s", context_path)
    command = GetPipeline(context_path)
    command.run()

@cli.command("jenkins_run_pipeline")
@click.option('--context_path', required=True, default=DEFAULT_CONTEXT_FILE_PATH, type=str, help="Path to context")
def _jenkins_run_pipeline(context_path):
    logging.info("CLI jenkins_run_pipeline operation calling for %s", context_path)
    command = JenkinsRunPipeline(context_path)
    command.run()
