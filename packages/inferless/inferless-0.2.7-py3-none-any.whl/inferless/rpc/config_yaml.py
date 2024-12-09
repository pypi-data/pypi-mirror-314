import yaml
import subprocess


def get_config_yaml(config_path, gpu):
    # read the file inferless.yaml in the current directory as a json string
    try:
        with open(config_path, "r") as file:
            config_yaml = file.read()
            if gpu:
                config_yaml = config_yaml + f"\ngpu: {gpu}"
            config_yaml = add_inferless_package(config_yaml)
            return config_yaml
    except FileNotFoundError:
        raise Exception("Configuration file inferless.yaml not found in the current directory")
    except Exception as e:
        raise Exception(f"Error reading inferless.yaml file: {e}")


def add_inferless_package(yaml_content):
    # Get the currently installed version of inferless
    result = subprocess.run(["pip", "show", "inferless"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("Version:"):
            current_version = line.split(":")[1].strip()
            break
    else:
        raise Exception("inferless is not installed in the current environment.")

    # Parse the YAML content
    config = yaml.safe_load(yaml_content)
    if "build" not in config:
        config["build"] = {}

    # Ensure the 'python_packages' section exists
    if 'python_packages' not in config.get('build', {}):
        config['build']['python_packages'] = []

    # Update or add the inferless package with the correct version
    updated_packages = []
    inferless_found = False
    for pkg in config['build']['python_packages']:
        if pkg.startswith("inferless"):
            updated_packages.append(f"inferless=={current_version}")
            inferless_found = True
        else:
            updated_packages.append(pkg)

    if not inferless_found:
        updated_packages.append(f"inferless=={current_version}")

    config['build']['python_packages'] = updated_packages

    # Return the updated YAML content
    return yaml.dump(config, default_flow_style=False)

