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

ultracold_matter_job = {
    "name": "Example Ultracold Matter Generator Job",
    "job_type": "BEC",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 8.0,
                "image_type": "TIME_OF_FLIGHT",
                "end_time_ms": 0.0,
                "rf_evaporation": {
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.045],
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0],
                },
                "optical_barriers": None,
                "optical_landscape": None,
                "lasers": None,
            },
        }
    ],
}

barrier_manipulator_job = {
    "name": "Example Barrier Manipulator Job",
    "job_type": "BARRIER",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 7.0,
                "image_type": "IN_TRAP",
                "end_time_ms": 20.0,
                "rf_evaporation": {
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.1],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0],
                },
                "optical_barriers": [
                    {
                        "heights_khz": [
                            0.0,
                            5.0,
                            10.0,
                            15.0,
                            20.0,
                            25.0,
                            25.0,
                            25.0,
                            25.0,
                            25.0,
                            25.0,
                        ],
                        "positions_um": [
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                            -10.0,
                        ],
                        "interpolation": "OFF",
                        "widths_um": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        "times_ms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "shape": "GAUSSIAN",
                    },
                    {
                        "heights_khz": [
                            0.0,
                            5.0,
                            10.0,
                            15.0,
                            20.0,
                            25.0,
                            30.0,
                            35.0,
                            40.0,
                            40.0,
                            40.0,
                        ],
                        "positions_um": [
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                            10.0,
                        ],
                        "interpolation": "OFF",
                        "widths_um": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        "times_ms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "shape": "GAUSSIAN",
                    },
                ],
                "optical_landscape": None,
                "lasers": None,
            }
        },
    ],
}
