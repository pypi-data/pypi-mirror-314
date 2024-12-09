from envix.config.v1.envs.raw_envs_v1 import RawEnvsV1

from .google_cloud_secret_manager_envs_v1 import GoogleCloudSecretManagerEnvsV1
from .local_envs_v1 import LocalEnvsV1


EnvsV1 = RawEnvsV1 | LocalEnvsV1 | GoogleCloudSecretManagerEnvsV1
