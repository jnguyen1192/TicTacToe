import psycopg2
import docker
import time
import subprocess
import os
from datetime import datetime
import docker_tools as dtt


def run_db(container_name="postgres", image_name="postgres", port=5432):
    """
    Create the postgres container and run it
    :return: 0 if it works else -1
    """
    client = docker.from_env()
    try:
        ports = {'5432/tcp': port}
        environment = ["POSTGRES_DB=postgres",
                       "POSTGRES_USER=postgres",
                       "POSTGRES_PASSWORD=postgres"]
        # restart a container
        dtt.clean_container("c_ttt_" + container_name)

        # to test pg database https://www.enterprisedb.com/download-postgresql-binaries
        # to connect to the database enter the ip of docker
        container = client.containers.run(image="c_ttt_" + image_name,
                                    name="c_ttt_" + container_name,
                                    pid_mode="host",
                                    #volumes=volumes,
                                    ports=ports,
                                    environment=environment,
                                    detach=True)
        # TODO debug log here
        #print(container.logs().decode('utf8'))
        client.close()
        return 0
    except Exception as e:
        print(e)
        client.close()
        return -1


def get_pwd():
    res = subprocess.run(['cmd', '/c', 'echo', '%cd%'], capture_output=True)
    pwd = res.stdout.decode('utf8')
    pwd_path = os.path.join(pwd)
    pwd_path_split = pwd_path.split("\\")
    if "test" in pwd_path_split[-1]:
        pwd = "\\".join(pwd_path_split[:-1])
    return pwd


def create_image_using_dockerfile(name):
    """
    Create the image to backup
    :return: 0 if it works else -1
    """
    try:
        # TODO Option 2 : use subprocess to use cmd from win
        # Prod way
        res = subprocess.run(["cmd", "/c", "docker", "build", "-f", os.path.join(get_pwd(), "Dockerfile." + name), get_pwd(), "-t", "c_ttt_" + name],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            print("Error code", res.returncode)
            # Dev way
            res = subprocess.run(["cmd", "/c", "docker", "build", "-f", os.path.join(get_pwd(), "Dockerfile." + name), get_pwd(), "-t", "c_ttt_" + name])

        # docker build -f Dockerfile.backup . -t c_sai_backup
        #print(type(res.returncode), res.returncode)
        return res.returncode
        #client.images.build(fileobj=fo, tag="c_sai_backup", custom_context=True)
    except Exception as e:
        print(e)
        return -1


def run_backup():
    """
    Create the container which will backup the db on a windows share folder
    :return: 0 if it works else -1
    """

    client = docker.from_env()
    try:
        #@source https://github.com/docker/for-win/issues/445
        #docker volume create --name postgres-data-volume -d local
        #volumes = {"/c/Users/johdu/PycharmProjects/SAI/backup_postgres":
        # shared folder on oracle vm : C:\Users\johdu\PycharmProjects\SAI\backup_postgres:/mnt/sda1/var/lib/docker/volumes/postgres-data-volume/_data
        # Backup http://support.divio.com/en/articles/646695-how-to-use-a-directory-outside-c-users-with-docker-toolbox-docker-for-windows
        volumes = {"postgres-data-volume":
                       {'bind': '/var/lib/postgresql/data/', 'mode': 'rw'}
                   }
        environment = ["POSTGRES_DB=postgres",
                       "POSTGRES_USER=postgres",
                       "POSTGRES_PASSWORD=postgres"]
        #print("Image building...")
        #print("Image builded")
        # restart a container
        dtt.clean_container("c_ttt_backup")

        # to test pg database https://www.enterprisedb.com/download-postgresql-binaries
        # to connect to the database enter the ip of docker
        container = client.containers.run(image="c_ttt_backup",
                                    name="c_ttt_backup",
                                    pid_mode="host",
                                    volumes=volumes,
                                    environment=environment,
                                    detach=True)
        # TODO debug log here
        #print(container.logs().decode('utf8'))
        #print("after postgres run")
        client.close()
        return 0
    except Exception as e:
        print(e)
        client.close()
        return -1


def get_last_backup():
    """
    Get the last backup created on directory backup_postgres
    :return: the filename or -1
    """
    try:
        mypath = os.path.join(get_pwd(), "backup_postgres")
        (_, _, filenames) = next(os.walk(mypath))
        return sorted(filenames, reverse=True)[0]
    except Exception as e:
        print(e)
        return -1


def load_last_backup(container_name, db_user="postgres", db_name="postgres"):
    """
    Load the backup into the container call c_sai_[container_name]
    :param container_name: the name of the container
    :return: 0 if it works else -1
    """
    backup_name = get_last_backup()
    try:
        # docker exec -i c_sai_tmp_postgres psql -U postgres -d postgres < backup_postgres/20200101T141905_postgres.sql
        # Prod way
        res = subprocess.run(["cmd", "/c", "docker", "exec", "-i", "c_sai_" + container_name, "psql", "-U", db_user,
                              "-d", db_name, "<", os.path.join(get_pwd(), "backup_postgres/" + backup_name)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            print("Error code", res.returncode)
            # Dev way
            res = subprocess.run(["cmd", "/c", "docker", "exec", "-i", "c_sai_" + container_name, "psql", "-U", db_user,
                                  "-d", db_name, "<", os.path.join(get_pwd(), "backup_postgres/" + backup_name)])
        # docker build -f Dockerfile.backup . -t c_sai_backup
        #print(type(res.returncode), res.returncode)
        return res.returncode
        #client.images.build(fileobj=fo, tag="c_sai_backup", custom_context=True)
    except Exception as e:
        print(e)
        return -1


def new_backup():
    """
    Create a backup using the corresponding container
    :return: the file name if it works else -1
    """
    #   Use this command to connect to the DB on the container
    #       PGPASSWORD=postgres pgsql -h 192.168.99.100 -p 5432 -U postgres
    file_name = datetime.now().replace(microsecond=0).strftime("%Y%m%dT%H%M%S") + "_postgres.sql"
    res = subprocess.run(
        ["cmd", "/c", "docker", "exec", "-t", "c_ttt_postgres", "pg_dump", "-c", "-U", "postgres", ">", os.path.join(get_pwd(), "backup_postgres", file_name)],
        capture_output=True)
    if res.returncode != 0:
        return -1
    return file_name


def new_csv(table_name):
    """
    Create a csv using the corresponding table
    :return: the file name if it works else -1
    """
    #   Use this command to connect to the DB on the container
    #       PGPASSWORD=postgres pgsql -h 192.168.99.100 -p 5432 -U postgres
    file_name = table_name + "_" + datetime.now().replace(microsecond=0).strftime("%Y%m%dT%H%M%S") + ".csv"
    # TODO Update the command to copy the selected table
    res = subprocess.run(
        ["cmd", "/c", "docker", "exec", "-t", "c_ttt_postgres", "pg_dump", "-c", "-U", "postgres", ">", os.path.join(get_pwd(), "csv", file_name)],
        capture_output=True)
    if res.returncode != 0:
        return -1
    return file_name


def remove_backup(file_name):
    """
    Remove the given backup
    :param file_name: the backup file name
    :return: 0 if it works else -1
    """
    res = subprocess.run(
        ["cmd", "/c", "del", "/f", os.path.join(get_pwd(), "backup_postgres", file_name)],
        capture_output=True)
    if res.returncode != 0:
        return -1
    return 0


def wait_db_connection(port=5432, test=False, nb_retry=120, time_sleep=1):
    """
    Wait the database connection
    :return: 0 if it works else -1
    """
    if test:
        port = "5433"
    i = 0
    while i < nb_retry:
        try:
            psycopg2.connect(user="postgres",
                              password="postgres",
                              host="192.168.99.100",
                              port=port,
                              database="postgres")
            #print("Connexion worked")
            return 0
        except Exception as e:
            #print(e)
            # TODO print all the functions called before
            #print(wait_db_connection.__name__, ": I wait", time_sleep, "seconds until try again,", nb_retry - i - 1, "remaining test cycle")
            time.sleep(time_sleep)
            i = i + 1
    return -1


# TODO connect to the database with the correct credentials and refactor


# TODO create function to use a query without parameters
def query_without_parameters(query_without_parameters):
    """
    Create a query on the database without parameters
    :return: 0 if it works else -1
    """
    connection = ""
    cursor = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="pass@#29",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres_db")
        cursor = connection.cursor()


        cursor.execute(query_without_parameters)
        connection.commit()
        print("Query without parameters executed successfully in PostgreSQL ")
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query in PostgreSQL", error)
        return -1
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


# TODO create function to use a query with parameters
def query_with_parameters(query, parameters, port=5432, test=False):
    """
    Create a query on the database without parameters
    :return: 0 if it works else -1
    """
    if test:
        port = "5433"
    connection = ""
    cursor = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="192.168.99.100",
                                      port=port,
                                      database="postgres")
        cursor = connection.cursor()
        #print(query)
        #print(parameters)
        cursor.execute(query, parameters)
        connection.commit()
        #print("Query with parameters executed successfully in PostgreSQL ")
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query with parameters in PostgreSQL", error)
        return -1
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


def select_one_with_parameters(query, parameters, port=5432, test=False):
    """
    Select one result on the database with parameters
    :return: 0 if it works else -1
    """
    if test:
        port = "5433"
    connection = ""
    cursor = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="192.168.99.100",
                                      port=port,
                                      database="postgres")
        cursor = connection.cursor()
        #print(query)
        #print(parameters)
        cursor.execute(query, parameters)
        res = cursor.fetchone()
        #print("Query with parameters executed successfully in PostgreSQL ")
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query with parameters in PostgreSQL", error)
        return -1
    finally:
        if connection:
            # closing database connection.
            cursor.close()
            connection.close()


def select_star_without_parameters(query, port=5432, test=False):
    """
    Select one result on the database with parameters
    :return: 0 if it works else -1
    """
    if test:
        port = "5433"
    connection = ""
    cursor = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="192.168.99.100",
                                      port=port,
                                      database="postgres")
        cursor = connection.cursor()
        #print(query)
        #print(parameters)
        cursor.execute(query)
        res = cursor.fetchall()
        #print("Query with parameters executed successfully in PostgreSQL ")
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query with parameters in PostgreSQL", error)
        return -1
    finally:
        if connection:
            # closing database connection.
            cursor.close()
            connection.close()


def select_star_with_parameters(query, parameters, port=5432, test=False):
    """
    Select one result on the database with parameters
    :return: 0 if it works else -1
    """
    if test:
        port = "5433"
    connection = ""
    cursor = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="192.168.99.100",
                                      port=port,
                                      database="postgres")
        cursor = connection.cursor()
        #print(query)
        #print(parameters)
        cursor.execute(query, parameters)
        res = cursor.fetchall()
        #print("Query with parameters executed successfully in PostgreSQL ")
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query with parameters in PostgreSQL", error)
        return -1
    finally:
        if connection:
            # closing database connection.
            cursor.close()
            connection.close()


def export_table_to_csv(table_name):
    # TODO
    #   First:  raws = Select * from table_name
    #           raws into dataframe
    #   Second: create a file called table_name_YYMMDDSS.csv
    #   Third: write dataframe into table_name_YYMMDDSS.csv
    pass