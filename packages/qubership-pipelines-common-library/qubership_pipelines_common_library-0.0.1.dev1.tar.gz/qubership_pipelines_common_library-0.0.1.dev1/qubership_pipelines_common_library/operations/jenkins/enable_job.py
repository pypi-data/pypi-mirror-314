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

import os
import logging

from v1.utils.utils_file import UtilsFile
from v1.execution.exec_command import ExecutionCommand
from v1.jenkins_client import JenkinsClient

class EnableJob(ExecutionCommand):
    def _validate(self):
        names = ["paths.input.params",
                 "paths.output.params",
                 "paths.output.files",
                 "systems.jenkins.url",
                 "systems.jenkins.username",
                 "systems.jenkins.password",
                 "params.job_name"]
        return self.context.validate(names)

    def _execute(self):
        logging.info("Running enable_job...")
        jenkins = JenkinsClient(self.context.input_param_get("systems.jenkins.url"),
                                self.context.input_param_get("systems.jenkins.username"),
                                self.context.input_param_get("systems.jenkins.password"))
        logging.info(f"Successfully initialized Jenkins client")
        jenkins.turn_on_job(self.context.input_param_get("params.job_name"))
        logging.info(f"Job successfully enabled")
        result_path = os.path.join(self.context.input_param_get("paths.output.files"),
                                      "execution_result.yaml")
        logging.info(f"Ready to write execution result to a file with path '{result_path}'")
        UtilsFile.write_yaml(result_path, {self.context.input_param_get("params.job_name"): "enabled"})
        logging.info(f"Ready to write output parameters")
        self.context.output_param_set("files.result_path", result_path)
        self.context.output_params_save()
        logging.info(f"Status: SUCCESS")