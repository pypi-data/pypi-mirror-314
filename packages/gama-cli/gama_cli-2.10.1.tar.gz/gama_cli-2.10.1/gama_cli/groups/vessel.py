import os
from typing import List, Optional
import click
import subprocess
from pathlib import Path

from gama_config.gama_vessel import (
    Variant,
    Network,
    Mode,
    DEFAULT_VARIANT_CONFIGS_MAP,
    read_vessel_config,
    serialise_vessel_config,
    get_vessel_config_path,
    write_vessel_config,
    VariantVesselConfig,
)
from gama_cli.helpers import (
    call,
    docker_compose_path,
    get_project_root,
    docker_bake,
    get_gama_version,
    maybe_ignore_build,
    maybe_ignore_prod,
    make_dir_set_permission,
)
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath
from greenstream_config.types import Camera


DOCKER_VESSEL = docker_compose_path("vessel/docker-compose.yaml")
DOCKER_VESSEL_PROD = docker_compose_path("vessel/docker-compose.prod.yaml")
DOCKER_VESSEL_DEV = docker_compose_path("vessel/docker-compose.dev.yaml")
DOCKER_VESSEL_NETWORK_SHARED = docker_compose_path("vessel/docker-compose.network-shared.yaml")
DOCKER_VESSEL_NETWORK_HOST = docker_compose_path("vessel/docker-compose.network-host.yaml")

SERVICES = [
    "gama_ui",
    "gama_chart_tiler",
    "gama_chart_api",
    "gama_vessel",
    "gama_vessel_base",
    "gama_greenstream",
    "gama_docs",
]


def change_registry(image_with_registry: str, new_registry: str):
    # replace the leading part of the image with the new registry
    return new_registry + "/" + "/".join(image_with_registry.split("/")[1:])


def execute_command_on_seperate_registry(func: callable, host: str, service: Optional[str] = None):
    config = read_vessel_config()

    docker = DockerClient(
        compose_files=_get_compose_files(
            variant=config.variant,
        ),
        compose_project_directory=get_project_root(),
    )
    images = docker.compose.config().services
    mapper = {}
    for service_name, service_config in images.items():
        if service and service_name != service:
            continue
        image = service_config.image
        if image:
            mapper[image] = change_registry(image, host)

    for service_name, service_config in images.items():
        if service and service_name != service:
            continue
        image = service_config.image
        if image:
            func(docker, image, mapper[image])


def tag_and_push(docker: DockerClient, local_image_tag: str, target_image_tag: str):
    docker.image.tag(local_image_tag, target_image_tag)
    docker.image.push(target_image_tag)


def pull_and_tag(docker: DockerClient, local_image_tag: str, target_image_tag: str):
    docker.image.pull(target_image_tag)
    docker.image.tag(target_image_tag, local_image_tag)


def _get_compose_files(
    network: Network = Network.SHARED,
    variant: Variant = Variant.ARMIDALE,
    prod: bool = False,
) -> List[ValidPath]:
    compose_files: List[ValidPath] = [DOCKER_VESSEL]
    if not prod:
        compose_files.append(DOCKER_VESSEL_DEV)

    compose_files.append(
        docker_compose_path(f"vessel/docker-compose.variant.{variant.value}.yaml")
    )

    if network == Network.SHARED:
        compose_files.append(DOCKER_VESSEL_NETWORK_SHARED)
    if network == Network.HOST:
        compose_files.append(DOCKER_VESSEL_NETWORK_HOST)
    if prod:
        compose_files.append(DOCKER_VESSEL_PROD)

    return compose_files


def log_config(config: VariantVesselConfig):
    click.echo(click.style("[+] GAMA Vessel Config:", fg="green"))
    click.echo(click.style(f" ⠿ Path: {get_vessel_config_path()}", fg="white"))
    for attr, value in config.__dict__.items():
        click.echo(
            click.style(f" ⠿ {attr}: ".ljust(35), fg="white") + click.style(str(value), fg="green")
        )


@click.group(help="Commands for the vessel")
def vessel():
    pass


@click.command(name="build")
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
@click.option("--pull", is_flag=True, help="Pull the latest images")
@click.argument("args", nargs=-1)
def build(service: str, args: List[str], pull: bool = False):  # type: ignore
    """Build the vessel"""
    config = read_vessel_config()

    docker = DockerClient(
        compose_files=_get_compose_files(variant=config.variant, prod=False),
        compose_project_directory=get_project_root(),
    )

    os.environ["GAMA_VARIANT"] = config.variant
    os.environ["GAMA_NAMESPACE_VESSEL"] = config.namespace_vessel
    os.environ["GAMA_NAMESPACE_GROUNDSTATION"] = config.namespace_groundstation

    if service:
        docker.compose.build([service], pull=pull)
        return

    docker.compose.build(pull=pull)


@click.command(name="pull-local")
@click.option(
    "--host",
    "-h",
    type=str,
    required=True,
    help="The host to pull the images from, ie localhost:5555",
)
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
def pull_local(host: str, service: Optional[str] = None):  # type: ignore
    execute_command_on_seperate_registry(pull_and_tag, host, service)


@click.command(name="push-local")
@click.option(
    "--host",
    "-h",
    type=str,
    required=True,
    help="The host  push the images to, ie localhost:5555",
    default="localhost:5555",
)
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
def push_local(host: str, service: Optional[str] = None):  # type: ignore
    # pass the context to execute_command_on_seperate_registry
    execute_command_on_seperate_registry(tag_and_push, host, service)


@click.command(name="bake")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    help="The variant to bake",
    default=Variant.ARMIDALE,
)
@click.option(
    "--version",
    type=str,
    default="latest",
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
def bake(variant: Variant, version: str, push: bool, services: List[str]):  # type: ignore
    """Bakes the vessel docker containers"""
    compose_files = _get_compose_files(variant=variant)
    docker_bake(
        version=version,
        services=services,
        push=push,
        compose_files=compose_files,
    )


@click.command(name="test-ui")
def test_ui():  # type: ignore
    """Runs test for the ui"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_ui", ["npm", "run", "test"])


@click.command(name="test-ros")
def test_ros():  # type: ignore
    """Runs test for the ros nodes"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run(
        "gama_vessel",
        ["platform", "ros", "test"],
    )


@click.command(name="test-scenarios")
@click.option(
    "--restart",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we restart the containers? Default: False",
)
@click.option(
    "--sim-speed",
    type=float,
    default=25.0,
    help="What speed should the scenarios be run at? Default: 25",
)
@click.argument("name", required=False, type=str)
def test_scenarios(restart: bool, sim_speed: float, name: Optional[str]):
    """Runs the scenario tests"""

    raise Exception("This command is not supported yet")

    if restart:
        call("missim down")
        call("gama vessel down")

    call("missim up")
    call("gama vessel up --scenario-test")

    config = read_vessel_config()
    log_config(config)

    docker = DockerClient(
        compose_files=_get_compose_files(
            network=config.network,
            variant=config.variant,
            prod=False,
        ),
        compose_project_directory=get_project_root(),
    )

    docker.compose.execute(
        "gama_vessel",
        [
            "bash",
            "-l",
            "-c",
            f"SCENARIO_NAME='{name or ''}' SCENARIO_SIM_SPEED={sim_speed} python3 -m pytest ./src/gama_scenarios/gama_scenarios/test_scenarios_armidale.py -s -v",
        ],
    )


@click.command(name="test-e2e")
def test_e2e():  # type: ignore
    """Runs UI e2e tests (assuming all the containers are up)"""
    call("cd ./projects/gama_ui && npm run test:e2e")


@click.command(name="test")
def test():  # type: ignore
    """Runs test for the all vessel code"""
    call("gama_cli vessel test-ui")
    call("gama_cli vessel test-ros")


@click.command(name="lint-ui")
@click.argument("args", nargs=-1)
def lint_ui(args: List[str]):  # type: ignore
    """Runs lints for the ui"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_ui", ["npm", "run", "lint", *args])


@click.command(name="type-generate")
def type_generate():  # type: ignore
    """Generates typescript types & schemas for all ros messages"""
    click.echo(
        click.style("Generating typescript types & schemas for all ros messages", fg="green")
    )

    # check the version of node
    node_version = subprocess.run(["node", "--version"], stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )
    if int(node_version.split(".")[0][1:]) < 20:
        click.echo(click.style("Node version less than 20, please upgrade", fg="red"))
        return

    config = read_vessel_config()
    docker = DockerClient(
        compose_files=_get_compose_files(
            network=config.network, variant=config.variant, prod=False
        ),
        compose_project_directory=get_project_root(),
    )
    subprocess.run(["npm", "run", "generate"], cwd=get_project_root() / "projects/gama_ui")

    docker.compose.execute(
        "gama_vessel",
        [
            "bash",
            "-l",
            "-c",
            "python3 src/gama_packages/mission_plan/mission_plan/generate_schemas.py",
        ],
    )
    docker.compose.execute("gama_vessel", ["npx", "ros-typescript-generator"])


@click.command(name="up")
@click.option(
    "--build",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we rebuild the docker containers? Default: False",
)
@click.option(
    "--nowatch",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we prevent gama_vessel from watching for changes? Default: False",
)
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
@click.argument("args", nargs=-1)
def up(
    build: bool,
    nowatch: bool,
    service: str,
    args: List[str],
):
    """Starts the vessel"""
    dev_mode = os.environ["GAMA_CLI_DEV_MODE"] == "true"

    config = read_vessel_config()
    build = maybe_ignore_build(dev_mode, build)
    prod = maybe_ignore_prod(dev_mode, config.prod)
    log_config(config)

    if prod and build:
        raise click.UsageError("Cannot build in production mode. Run `gama vessel build` instead")

    # Make the log and chart tiles directories
    log_directory = Path(config.log_directory).expanduser()
    charts_dir = Path(config.charts_directory).expanduser()
    get_vessel_config_path().chmod(0o777)
    make_dir_set_permission(log_directory)
    make_dir_set_permission(charts_dir)

    # If charts_dir is empty, copy the default charts
    if not os.listdir(charts_dir):
        if dev_mode:
            default_charts_dir = Path(get_project_root()) / "data/charts"
            call(f"cp -r {default_charts_dir}/* {charts_dir}")
        else:
            raise click.UsageError(f"Charts are missing. Add some charts to {charts_dir}")

    docker = DockerClient(
        compose_files=_get_compose_files(
            network=config.network,
            variant=config.variant,
            prod=prod,
        ),
        compose_project_directory=get_project_root(),
    )

    if prod:
        gama_vessel_command = "ros2 launch ./src/gama_bringup/launch/configure.launch.py"
    else:
        # build packages and watch for changes
        gama_vessel_command_args = "--build"
        if not nowatch:
            gama_vessel_command_args += " --watch"

        gama_vessel_command = f"platform ros run {gama_vessel_command_args} ros2 launch ./src/gama_bringup/launch/configure.launch.py"

    os.environ["GAMA_VESSEL_CONFIG"] = serialise_vessel_config(config)
    os.environ["GAMA_VERSION"] = get_gama_version()
    os.environ["GAMA_VESSEL_HOST"] = config.discovery_server_ip
    os.environ["GAMA_VARIANT"] = config.variant
    os.environ["GAMA_NAMESPACE_VESSEL"] = config.namespace_vessel
    os.environ["GAMA_NAMESPACE_GROUNDSTATION"] = config.namespace_groundstation
    os.environ["GAMA_VESSEL_COMMAND"] = gama_vessel_command
    os.environ["GAMA_LOG_DIR"] = str(log_directory)
    os.environ["GAMA_CHARTS_DIR"] = str(charts_dir)
    os.environ["ROS_DOMAIN_ID"] = str(config.ros_domain_id)

    services = (
        [service]
        if service
        else [
            "gama_ui",
            "gama_chart_tiler",
            "gama_chart_api",
            "gama_vessel",
            "gama_greenstream",
            "gama_docs",
        ]
    )

    docker.compose.up(
        services,
        detach=True,
        build=build,
    )


@click.command(name="down")
@click.argument("args", nargs=-1)
def down(args: List[str]):  # type: ignore
    """Stops the vessel"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    # set timeout to 20 secs (default 10) to allow for graceful shutdown of rosbag et al
    docker.compose.down(timeout=20)


@click.command(name="install")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    help="Which variant of GAMA to install?",
)
def install(variant: Variant):  # type: ignore
    """Install GAMA on a vessel"""
    config = read_vessel_config()
    variant = variant or config.variant
    docker = DockerClient(
        compose_files=_get_compose_files(variant=variant),
        compose_project_directory=get_project_root(),
    )
    try:
        docker.compose.pull(
            [
                "gama_ui",
                "gama_chart_tiler",
                "gama_chart_api",
                "gama_vessel",
                "gama_greenstream",
                "gama_docs",
            ]
        )
    except Exception:
        click.echo(
            click.style(
                "Failed to pull GAMA files. Have you ran `gama authenticate` ?",
                fg="yellow",
            )
        )


@click.command(name="configure")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    help="The Variant",
    required=True,
    prompt="Which variant of GAMA to configure?",
)
@click.option(
    "--mode",
    type=click.Choice(Mode),  # type: ignore
    help="The Mode",
    required=True,
    prompt="Which mode to run in?",
)
@click.option(
    "--prod",
    type=bool,
    help="Whether to run in production mode",
    is_flag=True,
)
@click.option(
    "--skip-confirm",
    type=bool,
    help="Skip confirmation",
    is_flag=True,
)
def configure(variant: Variant, mode: Mode, prod: bool, skip_confirm: bool):  # type: ignore
    """Configure GAMA Vessel"""
    config = DEFAULT_VARIANT_CONFIGS_MAP[variant]
    if mode is not None:
        config.mode = mode
    if prod is not None:
        config.prod = prod

    config.cameras = [
        Camera(
            name="bow",
            type="color",
            order=0,
            ptz=False,
        )
    ]

    # Check if the file exists
    if os.path.exists(get_vessel_config_path()):
        click.echo(
            click.style(
                f"GAMA Vessel config already exists: {get_vessel_config_path()}",
                fg="yellow",
            )
        )
        result = skip_confirm or click.prompt(
            "Do you want to overwrite it?", default="y", type=click.Choice(["y", "n"])
        )
        if result == "n":
            return

    write_vessel_config(config)


@click.command(name="config")
def config():  # type: ignore
    """Read Config"""
    config = read_vessel_config()
    log_config(config)
