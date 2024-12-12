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

import logging

from v1.execution.exec_command import ExecutionCommand
from v1.execution.exec_info import ExecutionInfo
from v1.jenkins_client import JenkinsClient

class RunPipeline(ExecutionCommand):
    def _validate(self):
        names = [
            "paths.input.params",
            "paths.output.params",
            "systems.jenkins.url",
            "systems.jenkins.username",
            "systems.jenkins.password",
            "params.pipeline_path",
            # "params.pipeline_params", optional, since the job may have no params of can be executed with default values
            # "timeout_seconds", 600, # optional
            # "wait_seconds", 1 # optional
        ]
        return self.context.validate(names)

    def _execute(self):
        logging.info("Running jenkins run_pipeline...")
        jenkins = JenkinsClient(self.context.input_param_get("systems.jenkins.url"),
                                self.context.input_param_get("systems.jenkins.username"),
                                self.context.input_param_get("systems.jenkins.password"))
        logging.info(f"Successfully initialized Jenkins client")
        execution = jenkins.run_pipeline(self.context.input_param_get("params.pipeline_path"),
                                         self.context.input_param_get("params.pipeline_params", {}))
        if execution.get_status() == ExecutionInfo.STATUS_IN_PROGRESS:
            logging.info(f"Pipeline successfully started. Waiting for execution to complete")
            execution = jenkins.wait_pipeline_execution(execution,
                                                        self.context.input_param_get("params.timeout_seconds", 1800),
                                                        self.context.input_param_get("params.wait_seconds", 1))
        else:
            logging.info(f"Pipeline was not started. Status {execution.get_status()}")
        logging.info(f"Ready to write output parameters")
        self.context.output_param_set("params.build.url", execution.get_url())
        self.context.output_param_set("params.build.id", execution.get_id())
        self.context.output_param_set("params.build.status", execution.get_status())
        self.context.output_param_set("params.build.date", execution.get_time_start().isoformat())
        self.context.output_param_set("params.build.duration", execution.get_duration_str())
        self.context.output_param_set("params.build.name", execution.get_name())
        self.context.output_params_save()
        logging.info(f"Status: {execution.get_status()}")