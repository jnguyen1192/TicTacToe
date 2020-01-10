import docker
import subprocess
from docker.utils import kwargs_from_env


def is_package_exist(package_name, image_name):
    """
    Check if a package exists on an image
    :param package_name: the name of the package
    :param image_name: the name of the image
    :return: True if it exists else False
    """
    #   run the corresponding image with the package to test and get the output
    res = subprocess.run(
        ["cmd", "/c", "docker", "run", "-t", "--name", "c_sai_" + image_name,  "c_sai_" + image_name, "dpkg", "-s", package_name],
            capture_output=True)
    return_code = res.returncode
    output = res.stdout.decode("utf-8")
    #   remove the container
    res = subprocess.run(
        ["cmd", "/c", "docker", "rm", "c_sai_" + image_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if return_code != 0:
        return False
    #   find on the output the correct message
    str_ok = "Status: install ok installed"
    #   return the corresponding boolean
    if str_ok not in output:
        return False
    return True


def is_image_exist(name):
    """
    Check if an image exists
    :param name: the name of the image
    :return: True if it works else False
    """
    client = docker.from_env()
    images_raws = client.images.list()
    images = [image.tags[0] for image in images_raws if image.tags != []]
    client.close()
    if name not in [image.split(":")[0] for image in images if image != ""]:
        return False
    return True


def is_container_exist(name):
    """
    Check if a container exists
    :param name: the name of the container
    :return: True if it works else False
    """
    client = docker.from_env()
    containers_raws = client.containers.list()
    containers = [container.name for container in containers_raws]
    client.close()
    if name not in containers:
        return False
    return True


def clean_container(name):
    """
    Run the correponding container using the same image and container name
    :param client: the docker client
    :param api_client: the docker client api
    :param name_container: the container name
    :return: 0 if it works else -1
    """
    client = docker.from_env()
    kwargs = kwargs_from_env()
    api_client = docker.APIClient(**kwargs)
    try:
        # TODO stop current c_sai_daemon
        for c in client.containers.list():
            if c.__getattribute__("name") == name:#"c_sai_postgres":
                api_client.kill(name)#"c_sai_postgres")
        # TODO rm current c_sai_daemon
        for c in client.containers.list(all=True):
            if c.__getattribute__("name") == name:#"c_sai_postgres":
                api_client.remove_container(name)#"c_sai_postgres")
        client.close()
        api_client.close()
        return 0
    except Exception as e:
        print(e)
        client.close()
        api_client.close()
        return -1

