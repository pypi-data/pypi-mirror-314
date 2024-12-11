from typing import List, Optional
import click
import os

from gama_config.gama_gs import (
    Network,
    Mode,
    LogLevel,
    read_gs_config,
    GamaGsConfig,
    get_gs_config_path,
    write_gs_config,
    serialise_gs_config,
)
from gama_cli.helpers import (
    docker_compose_path,
    get_project_root,
    docker_bake,
    maybe_ignore_build,
    maybe_ignore_prod,
)

from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath

DOCKER_GS = docker_compose_path("./gs/docker-compose.yaml")
DOCKER_GS_DEV = docker_compose_path("./gs/docker-compose.dev.yaml")
DOCKER_GS_NETWORK_SHARED = docker_compose_path("./gs/docker-compose.network-shared.yaml")
DOCKER_GS_NETWORK_HOST = docker_compose_path("./gs/docker-compose.network-host.yaml")
DOCKER_GS_WARTHOG_COMBO = docker_compose_path("./gs/docker-compose.warthog-combo.yaml")


def _get_compose_files(
    mode: Optional[Mode] = None, network: Network = Network.SHARED, prod: bool = False
) -> List[ValidPath]:
    compose_files: List[ValidPath] = [DOCKER_GS]

    if not prod:
        compose_files.append(DOCKER_GS_DEV)
    if mode == Mode.WARTHOG_COMBO:
        compose_files.append(DOCKER_GS_WARTHOG_COMBO)
    if network == Network.SHARED:
        compose_files.append(DOCKER_GS_NETWORK_SHARED)
    if network == Network.HOST:
        compose_files.append(DOCKER_GS_NETWORK_HOST)

    return compose_files


def log_config(config: GamaGsConfig):
    click.echo(click.style("[+] GAMA GS Config:", fg="green"))
    click.echo(click.style(f" ⠿ Path: {get_gs_config_path()}", fg="white"))
    for attr, value in config.__dict__.items():
        click.echo(
            click.style(f" ⠿ {attr}: ".ljust(35), fg="white") + click.style(str(value), fg="green")
        )


@click.group(help="Commands for the ground-station")
def gs():
    pass


@click.command(name="up")
@click.option(
    "--build",
    type=bool,
    default=False,
    help="Should we rebuild the docker containers? Default: False",
)
@click.argument("args", nargs=-1)
def up(
    build: bool,
    args: List[str],
):
    """Starts the ground-station"""
    dev_mode = os.environ["GAMA_CLI_DEV_MODE"] == "true"

    config = read_gs_config()
    build = maybe_ignore_build(dev_mode, build)
    prod = maybe_ignore_prod(dev_mode, config.prod)

    gama_gs_command = "platform ros launch gama_gs_bringup gs.launch.py"
    if not prod:
        gama_gs_command += " --watch --build"

    os.environ["GAMA_GS_CONFIG"] = serialise_gs_config(config)
    os.environ["GAMA_GS_COMMAND"] = gama_gs_command
    os.environ["ROS_DOMAIN_ID"] = str(config.ros_domain_id)
    os.environ["GAMA_VARIANT"] = config.variant.value
    os.environ["GAMA_VESSEL_HOST"] = config.discovery_server_ip
    os.environ["GAMA_NAMESPACE_VESSEL"] = config.namespace_vessel
    os.environ["GAMA_NAMESPACE_GROUNDSTATION"] = config.namespace_groundstation

    log_config(config)

    docker = DockerClient(
        compose_files=_get_compose_files(mode=config.mode, network=config.network, prod=prod),
        compose_project_directory=get_project_root(),
    )
    docker.compose.up(detach=True, build=build)


@click.command(name="down")
@click.argument("args", nargs=-1)
def down(args: List[str]):
    """Stops the ground-station"""
    config = read_gs_config()

    docker = DockerClient(
        compose_files=_get_compose_files(config.mode),
        compose_project_directory=get_project_root(),
    )
    docker.compose.down()


@click.command(name="install")
def install():  # type: ignore
    """Install GAMA on a gs"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    try:
        docker.compose.pull()
    except Exception:
        click.echo(
            click.style(
                "Failed to pull GAMA files. Have you ran `gama authenticate` ?",
                fg="yellow",
            )
        )


@click.command(name="configure")
@click.option("--default", is_flag=True, help="Use default values")
def configure(default: bool):  # type: ignore
    """Configure GAMA Ground Station"""

    if default:
        config = GamaGsConfig()
        write_gs_config(config)
        return

    # Check if the file exists
    if os.path.exists(get_gs_config_path()):
        click.echo(
            click.style(
                f"GAMA Ground Station config already exists: {get_gs_config_path()}",
                fg="yellow",
            )
        )
        result = click.prompt(
            "Do you want to overwrite it?", default="y", type=click.Choice(["y", "n"])
        )
        if result == "n":
            return

    try:
        config_current = read_gs_config()
    except Exception:
        config_current = GamaGsConfig()

    config = GamaGsConfig(
        ros_domain_id=click.prompt(
            "ROS Domain ID", type=int, default=config_current.ros_domain_id
        ),
        namespace_vessel=click.prompt("Namespace Vessel", default=config_current.namespace_vessel),
        namespace_groundstation=click.prompt(
            "Namespace Groundstation", default=config_current.namespace_groundstation
        ),
        mode=click.prompt(
            "Mode", type=click.Choice([mode.value for mode in Mode]), default=config_current.mode
        ),
        network=click.prompt(
            "Network",
            type=click.Choice([network.value for network in Network]),
            default=config_current.network,
        ),
        prod=click.prompt("Prod", type=bool, default=config_current.prod),
        log_level=click.prompt(
            "Log Level",
            type=click.Choice([log_level.value for log_level in LogLevel]),
            default=config_current.log_level,
        ),
    )
    write_gs_config(config)


@click.command(name="build")
@click.option("--pull", is_flag=True, help="Pull the latest images")
def build(pull: bool = False):
    """Builds the ground-station"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.build(pull=pull)


@click.command(name="bake")
@click.option(
    "--version",
    type=str,
    required=True,
    help="The version to bake. Default: latest",
)
@click.option(
    "--push",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we push the images to the registry? Default: False",
)
@click.argument("services", nargs=-1)
def bake(version: str, push: bool, services: List[str]):  # type: ignore
    """Bakes the gs docker containers"""
    compose_files = _get_compose_files()
    docker_bake(
        version=version,
        services=services,
        push=push,
        compose_files=compose_files,
    )


@click.command(name="test")
def test():
    """Tests the ground-station"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_gs", list("platform ros test".split(" ")))


@click.command(name="config")
def config():  # type: ignore
    """Read Config"""
    config = read_gs_config()
    log_config(config)
