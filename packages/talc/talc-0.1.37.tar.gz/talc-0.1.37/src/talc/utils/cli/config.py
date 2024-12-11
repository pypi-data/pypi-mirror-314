from importlib import import_module
import importlib.util
import sys

from talc.synthetic import QuestionGenerationConfig

_added_to_path = set()


def load_config(config_path: str) -> QuestionGenerationConfig:
    """Loads a talcconfig.py file from the given path, executes it, and returns the talc config produced by the file."""

    try:

        if config_path.endswith(".json"):
            with open(config_path, "r") as f:
                config = QuestionGenerationConfig.model_validate_json(f.read())
            return config

        if config_path.endswith(".py"):

            if config_path not in _added_to_path:
                _added_to_path.add(config_path)

                # Remove the last part of the path to get the directory
                config_dir = "/".join(config_path.split("/")[:-1])
                sys.path.insert(0, config_dir)

            spec = importlib.util.spec_from_file_location(
                "config", config_path, submodule_search_locations=[]
            )
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            sys.modules["config"] = module
            spec.loader.exec_module(module)
            config = module.config
            assert isinstance(config, QuestionGenerationConfig)
            return config

        # Load the config file
        config_module = import_module(config_path)

        # Get the config from the module
        config = config_module.config

        assert isinstance(config, QuestionGenerationConfig)

        return config

    except Exception as e:
        raise Exception(f"Failed to load config from {config_path}: {e}") from e
