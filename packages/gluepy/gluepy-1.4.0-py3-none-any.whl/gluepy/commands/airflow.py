import os
import re
from typing import Optional
from jinja2 import Environment, PackageLoader, FileSystemLoader
from gluepy.conf.context import default_settings
import click
from . import cli


@cli.group()
def airflow():
    """Group for all airflow commands"""


@airflow.command()
@click.argument("dest_path", type=str, required=True)
@click.argument("dag", type=str, required=False)
def generate(dest_path: str, dag: Optional[str] = None):
    """Command used to generate Airflow DAG files from Gluepy DAGs

    Args:
        dest_path (str): Path to store Airflow DAG files generated.
        dag (Optional[str], optional): Label of DAG to generate Airflow DAG of.
            Defaults to None.

    """
    from gluepy.exec.dags import REGISTRY

    if dag and dag not in REGISTRY:
        raise KeyError(f"DAG '{dag}' was not found in registry.")

    dags = [dag] if dag else list(REGISTRY.keys())

    for dag_label in dags:
        dag = REGISTRY[dag_label]()
        label = f"{default_settings.AIRFLOW_DAG_PREFIX}_{dag.label or dag.__class__.__name__.lower()}"  # noqa
        _, template = get_jinja(dag)
        with open(os.path.join(dest_path, f"{label}.py"), mode="w") as handle:
            handle.write(
                template.render(
                    **{
                        "dag": dag,
                        "dag_label": label,
                        "links": dag.inject_tasks(),
                        "image": default_settings.AIRFLOW_IMAGE,
                        "configmaps": default_settings.AIRFLOW_CONFIGMAPS or [],
                        "pod_resources": default_settings.AIRFLOW_POD_RESOURCES or {},
                        "k8s_config": default_settings.AIRFLOW_KUBERNETES_CONFIG
                        or None,
                    }
                )
            )


def get_jinja(dag):
    if dag.extra_options.get("airflow_template"):
        env = Environment(
            loader=FileSystemLoader(default_settings.BASE_DIR), autoescape=True
        )
        env.filters["to_identifier"] = to_identifier
        template = env.get_template(dag.extra_options.get("airflow_template"))
    elif default_settings.AIRFLOW_TEMPLATE:
        env = Environment(
            loader=FileSystemLoader(default_settings.BASE_DIR), autoescape=True
        )
        env.filters["to_identifier"] = to_identifier
        template = env.get_template(default_settings.AIRFLOW_TEMPLATE)
    else:
        env = Environment(
            loader=PackageLoader("gluepy", "templates/airflow"), autoescape=True
        )
        env.filters["to_identifier"] = to_identifier
        template = env.get_template("dag.j2")

    return env, template


def to_identifier(value):
    if not value:
        return None

    value = re.sub(r"[^a-zA-Z0-9_-]", "", value)
    value = re.sub(r"[\s-]", "_", value)

    if not value.isidentifier():
        raise ValueError(f"'{value}' is not a valid python identifier.")

    return value
