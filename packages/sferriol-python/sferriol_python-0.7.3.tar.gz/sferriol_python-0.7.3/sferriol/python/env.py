import os
import tomllib


def load(default=None, env_file=None, os_env_prefix=None):
    """
    Return env dictionary loaded from, in order:
      1. a default dictionary
      2. a toml file where path is, in order, in env_file or in OS_ENV_PREFIX__ENV_FILE os env. variable
      3. os env. variables OS_ENV_PREFIX__K where K is each key in previous dictionary in uppercase 
    """
    di = default.copy() if default else dict()
    os_env_prefix = os_env_prefix.upper() + '__' if os_env_prefix else None

    # from the env file
    if os_env_prefix:
        env_file = os.getenv(os_env_prefix + 'ENV_FILE', env_file)
    if env_file is not None:
        with open(env_file, "rb") as f:
            di.update(tomllib.load(f))

    # from os env variables
    if os_env_prefix:
        for k in di.keys():
            di[k] = os.getenv(os_env_prefix + str(k).upper(), di[k])

    return di
