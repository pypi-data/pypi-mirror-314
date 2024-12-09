import subprocess
import os
import shutil
from script_builder.argument_processor import ArgumentProcessor
from script_builder.password import get_strong_password, generate_strong_password
from importlib.metadata import version
from .package_dir import package_dir
from .docker_compose_helper import docker_compose_helper
import requests
from concierge_util import load_config, write_config
from .set_env import set_env
from .docker_containers import keycloak_exists, opensearch_exists


def do_install(
    argument_processor: ArgumentProcessor, environment="production", is_local=False
):
    # this disables TLS verification and warning
    session = requests.Session()
    session.verify = False
    # the development environment uses different docker compose files which should already be in the cwd
    if environment != "development":
        # for production we need to copy the compose files from the package into the cwd because docker compose reads the .env file from the same directory as the launched files
        shutil.copytree(
            os.path.join(package_dir, "docker_compose"), os.getcwd(), dirs_exist_ok=True
        )
    config = load_config()
    # Keycloak needs the host and port to be set before as these are piped into the initial realm config
    set_env("WEB_HOST", argument_processor.parameters["host"])
    set_env("WEB_PORT", str(argument_processor.parameters["port"]))
    if argument_processor.parameters["security_level"] != "None":
        set_env("CONCIERGE_SECURITY_ENABLED", "True")
        set_env("CONCIERGE_SERVICE", "concierge-enable-security")
        # we only configure Keycloak if it wasn't already present
        if not keycloak_exists():
            keycloak_password = get_strong_password(
                "Enter password for initial Keycloak admin account: "
            )
            db_password = generate_strong_password()
            set_env("KEYCLOAK_INITIAL_ADMIN_PASSWORD", keycloak_password)
            set_env("POSTGRES_DB_PASSWORD", db_password)
            full_path = os.path.join(os.getcwd(), "docker-compose-launch-keycloak.yml")
            # pull latest versions before launching Keycloak, otherwise the instance gets broken if new images are pulled during the next step
            subprocess.run(["docker", "compose", "-f", full_path, "pull"])
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    full_path,
                    "up",
                    "-d",
                ]
            )
            # TODO: some kind of timeout on this?
            print(
                "Waiting for Keycloak to start so we can get the OpenID credentials..."
            )
            print("This can take a few minutes, please be patient!")
            while True:
                try:
                    response = session.post(
                        "https://localhost:8443/realms/master/protocol/openid-connect/token",
                        {
                            "client_id": "admin-cli",
                            "grant_type": "password",
                            "username": "admin",
                            "password": keycloak_password,
                        },
                    )
                    token = response.json()["access_token"]
                    headers = {
                        "content-type": "application/json",
                        "Authorization": f"Bearer {token}",
                    }
                    # TODO: we should get the client ID from the realm JSON file to avoid errors
                    response = session.get(
                        "https://localhost:8443/admin/realms/concierge/clients/7a3ec428-36f2-49c4-91b1-8288dc44acb0/client-secret",
                        headers=headers,
                    )
                    keycloak_secret = response.json()["value"]
                    break
                except Exception:
                    pass

            set_env("KEYCLOAK_CLIENT_ID", "concierge-auth")
            set_env("KEYCLOAK_CLIENT_SECRET", keycloak_secret)
        # we only configure OpenSearch if it's missing or running the security disabled version
        if (
            not opensearch_exists()
            or os.getenv("OPENSEARCH_SERVICE") != "opensearch-node-enable-security"
        ):
            opensearch_password = generate_strong_password()
            set_env("OPENSEARCH_INITIAL_ADMIN_PASSWORD", opensearch_password)
        set_env("OPENSEARCH_SERVICE", "opensearch-node-enable-security")
        set_env(
            "OPENSEARCH_DASHBOARDS_SERVICE",
            "opensearch-dashboards-enable-security",
        )

        set_env("KEYCLOAK_SERVICE_FILE", "docker-compose-keycloak.yml")
    else:
        set_env("CONCIERGE_SERVICE", "concierge")
        set_env("CONCIERGE_SECURITY_ENABLED", "False")
        set_env("OPENSEARCH_SERVICE", "opensearch-node-disable-security")
        set_env(
            "OPENSEARCH_DASHBOARDS_SERVICE",
            "opensearch-dashboards-disable-security",
        )
        set_env("KEYCLOAK_SERVICE_FILE", "docker-compose-blank.yml")
    set_env("ENVIRONMENT", environment)
    set_env("CONCIERGE_VERSION", version("launch_concierge"))
    set_env(
        "OLLAMA_SERVICE",
        "ollama-gpu"
        if argument_processor.parameters["compute_method"].lower() == "gpu"
        else "ollama",
    )
    write_config(config)
    # docker compose
    docker_compose_helper(environment, is_local, True)
    # ollama model load
    subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            "ollama",
            "ollama",
            "pull",
            argument_processor.parameters["language_model"],
        ]
    )
