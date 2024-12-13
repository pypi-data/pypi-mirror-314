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

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str = "coldquanta.auth0.com"
    auth0_client_id: str = "cTWqizVsJj2WrLtBgzgo3KZFgEY3k2OC"
    auth0_scope: str = "profile openid mail"
    auth0_audience: str = "https://oqtant.infleqtion.com/oqtant"
    auth0_notebook_redirect_uri: str = "http://localhost:8888/callback/"
    auth0_response_type: str = "token id_token"
    base_url: str = "https://oqtant.infleqtion.com/api"
    max_ind_var: int = 2
    run_list_limit: int = 30
