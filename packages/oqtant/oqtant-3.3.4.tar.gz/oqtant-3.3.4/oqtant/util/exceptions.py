# Copyright 2024 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class JobError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class JobReadError(JobError):
    pass


class JobWriteError(JobError):
    pass


class OqtantError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)


class OqtantAuthorizationError(OqtantError):
    pass


class OqtantTokenError(OqtantError):
    pass


class OqtantRequestError(OqtantError):
    pass


class OqtantJobError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OqtantJobUnsupportedTypeError(OqtantJobError):
    pass


class OqtantJobValidationError(OqtantJobError):
    pass


class OqtantJobParameterError(OqtantJobError):
    pass


class OqtantJobListLimitError(OqtantJobError):
    pass


class SimValueError(ValueError):
    pass


class SimSubmitError(Exception):
    def __init__(self):
        super().__init__("Cannot submit simulations as a batch.")


class JobPlotFitError(OqtantJobError):
    def __init__(self):
        super().__init__("PLOT FIT RESULTS: failed to generate model from provided parameters")


class JobPlotFitMismatchError(OqtantJobError):
    def __init__(self):
        super().__init__("PLOT FIT RESULTS: mismatched parameters and model type")


class VersionWarning(Warning):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
