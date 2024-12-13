import os
import re
import subprocess

import click


def get_running_ports():
    """
    Get running ports of Jupyter servers

    Args:
        None
    Returns:
        list: list of running ports
    """
    res = subprocess.getoutput("jupyter notebook list")

    pattern = r"http://localhost:(\d+)"
    regex = re.compile(pattern)

    running_ports = regex.findall(res)
    return running_ports


@click.command()
@click.option("--port", default=8888)
def start_notebook(port):
    """
    Start Jupyter server, and kill previously running Jupyter servers if any exist

    Args:
        port (int, optional): Port to run the Jupyter server on
    Returns:
        None
    """
    running_ports = get_running_ports()
    if running_ports:
        resp = click.confirm(
            "There are running Jupyter servers on ports: "
            + ", ".join(str(port) for port in running_ports)
            + ". Do you want to stop them? (You will not be able to start and log into another instance of Qqtant without doing so.)"
        )
        if resp:
            os.system(f"killport {' '.join(running_ports)}")
            click.echo("Killed running Jupyter servers")

    subprocess.run(["jupyter", "notebook", "--port", str(port)])


if __name__ == "__main__":
    start_notebook()
