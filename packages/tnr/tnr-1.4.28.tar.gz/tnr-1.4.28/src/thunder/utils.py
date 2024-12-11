import os
from os.path import join
import requests
import platform
import getpass
import subprocess
import json

from rich.console import Console
from rich.table import Table
from rich import box
import click

BASEURL = "https://api.thundercompute.com:8443"
# For debug mode
if os.environ.get('API_DEBUG_MODE') == "1":
    BASEURL = 'http://localhost:8080'

CONFIG_PATH = join(join(os.path.expanduser("~"), ".thunder"), "config.json")

session = requests.Session()

def setup_instance(token):
    basedir = join(os.path.expanduser("~"), ".thunder")
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    scriptfile = join(basedir, "setup.sh")
    script_contents_file = join(os.path.dirname(__file__), "tnr_setup.sh")
    with open(script_contents_file, "r", encoding="utf-8") as f:
        setup_sh = f.read()

    if not os.path.exists(scriptfile):
        with open(scriptfile, "w+", encoding="utf-8") as f:
            f.write(setup_sh)
        os.chmod(scriptfile, 0o555)

        # Only add this if it doesn't exist inside the bashrc already
        bashrc = join(os.path.expanduser("~"), ".bashrc")
        if f". {scriptfile}" not in bashrc:
            with open(bashrc, "a", encoding="utf-8") as f:
                f.write(f"\n# start tnr setup\n. {scriptfile}\n# end tnr setup\n")
    else:
        with open(scriptfile, "r", encoding="utf-8") as f:
            current_contents = f.read()

        if current_contents != setup_sh:
            os.chmod(scriptfile, 0o777)
            with open(scriptfile, "w+", encoding="utf-8") as f:
                f.write(setup_sh)
            os.chmod(scriptfile, 0o555)

    setup_config(token)

def setup_config(token):
    if not os.path.exists(CONFIG_PATH):
        # Identify current computer
        try:
            endpoint = f"{BASEURL}/next_id"
            response = session.get(
                endpoint, headers={"Authorization": f"Bearer {token}"}
            )
            device_id = str(response.json()["id"])
        except Exception as e:
            click.echo(
                click.style(
                    f"Unable to identify device. Please report this error to the developers",
                    fg="red",
                    bold=True,
                )
            )
            exit(1)

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "instanceId": -1,
                    "deviceId": device_id,
                    "gpuType": "t4",
                    "gpuCount": 1,
                },
                f,
            )

def enable_default_tnr_activate():
    with open(os.path.expanduser("~/.bashrc"), "r") as f:
        if "tnr activate" not in f.read():
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("\ntnr activate\n")

def get_available_gpus():
    endpoint = f"{BASEURL}/hosts2"
    try:
        response = session.get(endpoint, timeout=10)
        if response.status_code != 200:
            return None

        return response.json()
    except Exception as e:
        return None


def save_token(filename, token):
    if os.path.isfile(filename):
        if platform.system() == "Windows":
            subprocess.run(
                ["icacls", rf"{filename}", "/grant", f"{getpass.getuser()}:R"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            os.chmod(filename, 0o600)

    with open(filename, "w") as f:
        f.write(token)

    if platform.system() == "Windows":
        subprocess.run(
            [
                "icacls",
                rf"{filename}",
                r"/inheritance:r",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["icacls", f"{filename}", "/grant:r", rf"{getpass.getuser()}:(R)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        os.chmod(filename, 0o400)


def delete_unused_keys():
    pass


def get_key_file(uuid):
    basedir = join(os.path.expanduser("~"), ".thunder")
    basedir = join(basedir, "keys")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    return join(basedir, f"id_rsa_{uuid}")


def get_instances(token):
    if get_instances.cache is not None:
        return get_instances.cache

    endpoint = f"{BASEURL}/instances/list"
    try:
        response = session.get(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text, {}

        get_instances.cache = (True, None, response.json())
        return True, None, response.json()
    except Exception as e:
        return False, str(e), {}


get_instances.cache = None


def create_instance(token, cpu_cores):
    endpoint = f"{BASEURL}/instances/create/{cpu_cores}"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        data = response.json()

        token_file = get_key_file(data["uuid"])
        save_token(token_file, data["key"])
        return True, None
    except Exception as e:
        return False, str(e)


def delete_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/delete"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def start_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/up"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def stop_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/down"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)
    
def get_current_disk_size_ssh(ssh):
    """Retrieve the current disk size using SSH."""
    _, stdout, _ = ssh.exec_command("lsblk -b -o SIZE -n -d /dev/sda")
    size_bytes = stdout.read().strip()
    if not size_bytes:
        return None
    try:
        # Convert bytes to GB
        size_gb = int(size_bytes) / (1024 ** 3)
        return round(size_gb)
    except ValueError:
        return None


def resize_instance(instance_id, new_size, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/resize"
    msg_dict = {
        'requested_size': new_size,
    }
    try:
        response = session.post(
            endpoint, 
            headers={"Authorization": f"Bearer {token}"}, 
            timeout=30,
            json=msg_dict
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def get_active_sessions(token):
    endpoint = f"{BASEURL}/active_sessions"
    try:
        response = session.get(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return None, []

        data = response.json()
        ip_address = data.get("ip", "N/A")
        sessions = data.get("sessions", [])
        return ip_address, sessions
    except Exception as e:
        return None, []



def add_key_to_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/add_key"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        data = response.json()
        token_file = get_key_file(data["uuid"])
        save_token(token_file, data["key"])
        return True, None

    except Exception as e:
        return False, str(e)


# Updating ~/.ssh/config automatically
SSH_DIR = os.path.join(os.path.expanduser("~"), ".ssh")
SSH_CONFIG_PATH = os.path.join(SSH_DIR, "config")


def read_ssh_config():
    if os.path.exists(SSH_CONFIG_PATH):
        with open(SSH_CONFIG_PATH, "r") as f:
            return f.readlines()
    return []


def write_ssh_config(lines):
    # TODO: If ~/.ssh folder doesn't exist create it
    try:
        if not os.path.exists(SSH_DIR):
            os.mkdir(SSH_DIR)
        with open(SSH_CONFIG_PATH, "w+", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        pass


def add_instance_to_ssh_config(hostname, key_path, host_alias=None):
    config_lines = read_ssh_config()
    host_alias = host_alias or hostname

    new_entry = [
        f"Host {host_alias}\n",
        f"    HostName {hostname}\n",
        f"    User ubuntu\n",
        f"    IdentityFile {key_path}\n",
    ]

    if not any(line.startswith(f"Host {host_alias}") for line in config_lines):
        config_lines.append("\n")  # Ensure there's a new line before adding a new entry
        config_lines.extend(new_entry)

    write_ssh_config(config_lines)


def remove_instance_from_ssh_config(host_alias):
    config_lines = read_ssh_config()
    start_idx = None
    end_idx = None

    for i, line in enumerate(config_lines):
        if line.startswith(f"Host {host_alias}"):
            start_idx = i
        if start_idx is not None and line.strip() == "":
            end_idx = i + 1
            break

    if start_idx is not None:
        del config_lines[start_idx:end_idx]

    write_ssh_config(config_lines)


def get_ssh_config_entry(instance_name):
    if not os.path.exists(SSH_CONFIG_PATH):
        return False, None
    with open(SSH_CONFIG_PATH, "r") as config_file:
        entry_exists = False
        ip_address = None
        for line in config_file:
            if line.strip() == f"Host {instance_name}":
                entry_exists = True
            if entry_exists and line.strip().startswith("HostName"):
                ip_address = line.split()[1]
                break
    return entry_exists, ip_address


def update_ssh_config_ip(instance_name, new_ip_address):
    temp_path = os.path.join(
        os.path.join(os.path.expanduser("~"), ".ssh"), "config_tmp"
    )
    if not os.path.exists(SSH_CONFIG_PATH):
        with open(SSH_CONFIG_PATH, "w+", encoding="utf-8") as f:
            pass

    with open(SSH_CONFIG_PATH, "r") as config_file, open(temp_path, "w") as temp_file:
        entry_exists = False
        for line in config_file:
            if line.strip() == f"Host {instance_name}":
                entry_exists = True
            if entry_exists and line.strip().startswith("HostName"):
                temp_file.write(f"    HostName {new_ip_address}\n")
                entry_exists = False  # Reset to avoid further modifications in the loop
            else:
                temp_file.write(line)

    os.replace(temp_path, SSH_CONFIG_PATH)
    print(f"Updated IP address for {instance_name} in SSH config to {new_ip_address}.")

def validate_token(token):
    endpoint = f"https://api.thundercompute.com:8443/uid"
    response = session.get(endpoint, headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 200:
        return True, None
    elif response.status_code == 401:
        return False, "Invalid token, please update the TNR_API_TOKEN environment variable or login again"
    else:
        return False, "Failed to authenticate token, please use `tnr logout` and try again."


def display_available_gpus():
    available_gpus = get_available_gpus()
    if available_gpus is not None:
        console = Console()
        available_gpus_table = Table(
            title="🌐 Available GPUs:",
            title_style="bold cyan",
            title_justify="left",
            box=box.ROUNDED,
        )
        available_gpus_table.add_column(
            "GPU Type",
            justify="center",
        )
        available_gpus_table.add_column(
            "Node Size",
            justify="center",
        )

        for gpu_type, count in available_gpus.items():
            available_gpus_table.add_row(
                gpu_type,
                ", ".join(map(str, count)),
            )
        console.print(available_gpus_table)


def read_config():
    if not os.path.exists(CONFIG_PATH):
        click.echo(
            click.style(
                f"Unable to find ~/.thunder/config.json. Please report this error to the developers.",
                fg="red",
                bold=True,
            )
        )
        exit(1)

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except Exception as e:
        click.echo(
            click.style(
                f"Failed to read config. Please delete ~/.thunder/config.json and try again.",
                fg="red",
                bold=True,
            )
        )
        exit(1)

    return config


def write_config(data):
    with open(CONFIG_PATH, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def validate_config():
    config = read_config()

    if "instanceId" not in config:
        raise click.ClickException("Config error: instanceId not found")

    if "deviceId" not in config:
        raise click.ClickException("Config error: deviceId not found")

    if type(config["deviceId"]) != str:
        config["deviceId"] = str(config["deviceId"])
        write_config(config)

    if "gpuType" not in config:
        raise click.ClickException("Config error: gpuType not found")

    if "gpuCount" not in config:
        raise click.ClickException("Config error: gpuCount not found")

    if type(config["gpuCount"]) != int:
        raise click.ClickException("Config error: gpuCount must be an integer")


def get_instance_id(token):
    config = read_config()
    if config["instanceId"] == -1:
        ip_address = session.get("https://ifconfig.co/json").json()["ip"]
        success, error, instances = get_instances(token)
        if not success:
            click.echo(
                click.style(
                    f"Failed to list Thunder Compute instances: {error}",
                    fg="red",
                    bold=True,
                )
            )
            return -1

        for instance_id, metadata in instances.items():
            if "ip" in metadata and metadata["ip"] == ip_address:
                break
        else:
            instance_id = None

        config["instanceId"] = instance_id
        write_config(config)
    else:
        instance_id = read_config()["instanceId"]
    return str(instance_id) if instance_id is not None else instance_id

def get_uid(token):
    endpoint = f"{BASEURL}/uid"
    response = requests.get(endpoint, headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        raise click.ClickException(
            "Failed to get info about user, is the API token correct?"
        )
    return response.text
    