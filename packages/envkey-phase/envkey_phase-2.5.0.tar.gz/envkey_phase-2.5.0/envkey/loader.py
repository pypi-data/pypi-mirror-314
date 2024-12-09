import os
import sys
from dotenv import dotenv_values
from phase import GetAllSecretsOptions, Phase
from .fetch import fetch_env

def load(is_init=False, cache_enabled=None, dot_env_path=None):
    _env = dotenv_values()
    phase_token = _env.get('PHASE_SERVICE_TOKEN', "")
    if phase_token:
        print("Loading envvars from phase")
        return _load_from_phase()

    if is_init and os.environ.get("ENVKEY_DISABLE_AUTOLOAD"):
        return dict()

    print("Loading envvars from envkey")
    fetch_res = fetch_env(cache_enabled=cache_enabled, dot_env_path=dot_env_path)

    vars_set = dict()

    for k in fetch_res:
        if os.environ.get(k) is None:  # noqa: SIM102
            if k is not None and fetch_res[k] is not None:
                val = to_env(fetch_res[k])
                os.environ[to_env(k)] = val
                vars_set[to_env(k)] = val

    return vars_set


def to_env(s):
    if sys.version_info[0] == 2:
        return s.encode(sys.getfilesystemencoding() or "utf-8")
    return s


def _config():
    cfg = dotenv_values()
    return cfg


def _load_from_phase():
    cfg = _config()
    phase = Phase(
        init=False,
        pss=cfg["PHASE_SERVICE_TOKEN"],
        host="https://console.phase.dev",
    )
    get_options = GetAllSecretsOptions(
        env_name=os.environ.get('SERVER_ENV'),
        app_name=cfg["PHASE_PROJECT"],
    )
    vars_set = dict()
    secrets = phase.get_all_secrets(get_options)
    for secret in secrets:
        k = secret.key
        v = secret.value
        if os.environ.get(k, None) is None:  # noqa: SIM102
            if k is not None and k is not None:
                key = to_env(k)
                val = to_env(v)
                os.environ[key] = val
                vars_set[key] = val
    return vars_set
