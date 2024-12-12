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
from v1.git_client import GitClient

class GetPipeline(ExecutionCommand):

    def _validate(self):
        names = ["paths.input.params",
                 "paths.output.params",
                 "paths.output.files",
                 "systems.git.url",
                 "systems.git.username",
                 "systems.git.password",
                 "systems.git.email",
                 "params.project_id",
                 "params.pipeline_id"]
        return self.context.validate(names)

    def _execute(self):
        logging.info("Running get_pipeline...")
        git = GitClient(self.context.input_param_get("systems.git.url"),
                        self.context.input_param_get("systems.git.username"),
                        self.context.input_param_get("systems.git.password"),
                        self.context.input_param_get("systems.git.email"))
        logging.info(f"Successfully initialized Git client")
        test_git = git.get_pipeline_status(self.context.input_param_get("params.project_id"),
                                        self.context.input_param_get("params.pipeline_id"))
        logging.info(f"Successfully retrieved get_pipeline")
        result_path = os.path.join(self.context.input_param_get("paths.output.files"),
                                      "execution_result.yaml")
        logging.info(f"Ready to write parameter set to a file with path '{result_path}'")
        UtilsFile.write_yaml(result_path, test_git)
        logging.info(f"Ready to write output parameters")
        self.context.output_param_set("files.param_set_path", result_path)
        self.context.output_params_save()
        logging.info(f"Status: SUCCESS")