#    Copyright 2022 邹涛

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import json
import os
from app_logging import getLogger

__log = getLogger("config")

__CONFIG_PATH = os.path.join(os.path.curdir, "data")
__DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser('~'),".pyserialtool", "data")
__log.debug(__CONFIG_PATH)
__log.debug(__DEFAULT_CONFIG_PATH)

__CONFIG_FILE_NAME = "app.json"

__config_instance = None


if not os.path.exists(__CONFIG_PATH):
    __config_url = os.path.join(__DEFAULT_CONFIG_PATH, __CONFIG_FILE_NAME)
    __log.debug("config path not exists")
    try:
        __config_instance = json.loads(__config_url)
    except Exception as e:
        __log.error(f"config file not found\n{e}")

__log.info(__config_instance)

