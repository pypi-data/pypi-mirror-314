import mariadb
import secrets
import string
from getpass import getpass
from dotenv import load_dotenv, set_key
from pathlib import Path
from .view import error, success, warning
import sys
import os


def get_env_file_path():
    config_dir = os.path.join(str(Path.home()), ".config", "lefaire")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, ".env")


env_path = get_env_file_path()


def setup():
    try:
        ## Ask for a root access
        (root_password, root_host) = get_credentials()

        # Establish a root connexion
        root_conn = mariadb.connect(user="root", host=root_host, password=root_password)
        success("Connexion établie !")
        cur = root_conn.cursor()

        ## delete user if it exists
        flush_user(cur, root_host)

        # create databases
        create_databases(cur)

        # generate securely a password
        new_password = generate_password()

        ## Create new user with secure password and give access to databases
        grant_privileges(cur, new_password, root_host)

        # Store the password to the env
        set_key(env_path, "LEFAIRE_PASSWORD", new_password)
        set_key(env_path, "LEFAIRE_HOST", root_host)

        # load variables from .env

        load_dotenv(env_path)
        root_conn.commit()
        root_conn.close()
        return

    except Exception:
        raise Exception("Accès refusé ...")


def get_credentials():
    print("Connexion à MariaDB")
    print("Utilisateur : root")
    host = input("Host (laissez vide pour localhost) :")
    if not host:
        host = "localhost"

    root_password = getpass("Mot de passe : ")
    return (root_password, host)


def flush_user(cur, host):
    print(
        "Supression de l'utilisateur MariaDB (anciennement MySQL) 'lefaire' s'il existe... "
    )
    cur.execute(f"DROP USER IF EXISTS 'lefaire'@'{host}'")


def create_tables(cur, db):
    cur.execute(
        f" CREATE TABLE IF NOT EXISTS {db}.Project ( `ID` int(11) NOT NULL AUTO_INCREMENT, `Created` timestamp NOT NULL,`Started` timestamp NULL DEFAULT NULL,`CompletionDate` timestamp NULL DEFAULT NULL,`DueDate` datetime DEFAULT NULL,`Description` text DEFAULT NULL,`IsComplete` tinyint(1) NOT NULL DEFAULT 0,`Name` varchar(255) NOT NULL,PRIMARY KEY (`ID`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci "
    )
    cur.execute(
        f"""
                CREATE TABLE IF NOT EXISTS {db}.Task (
                `ID` int(11) NOT NULL AUTO_INCREMENT,
                `ProjectID` int(11) NOT NULL,
                `Rank` int(11) NOT NULL,
                `Body` text NOT NULL,
                `Created` timestamp NULL DEFAULT current_timestamp(),
                `Started` timestamp NULL DEFAULT NULL,
                `CompletionDate` timestamp NULL DEFAULT NULL,
                `IsComplete` tinyint(1) NOT NULL DEFAULT 0,
                PRIMARY KEY (`ID`)
)
            """
    )


def create_databases(cur):
    print("Création de la base de donnée ...")
    cur.execute("CREATE DATABASE IF NOT EXISTS lefaire")
    create_tables(cur, "lefaire")  # if doesn't exist
    print("Création de la base de donnée de test ...")
    cur.execute("CREATE DATABASE IF NOT EXISTS lefaire_test")
    create_tables(cur, "lefaire_test")  # if doesn't exist


def generate_password():
    print("Création d'un mot de passe sécurisé ...")
    safe_punctuation = "!@#$%/&*()[]{}_-+=:;.,<>?"
    alphabet = string.ascii_letters + string.digits + safe_punctuation
    password = "".join(secrets.choice(alphabet) for i in range(16))
    return password


def grant_privileges(cur, password, host):
    print("Autorisation d'accès à la base de données lefaire...")
    cur.execute(
        f"""
            GRANT ALL PRIVILEGES ON lefaire.* TO 'lefaire'@'{host}' IDENTIFIED BY '{password}' ;
        """
    )
    print("Autorisation d'accès à la base de données de test...")
    cur.execute(
        f"GRANT ALL PRIVILEGES ON lefaire_test.* TO 'lefaire'@'{host}' IDENTIFIED BY '{password}' ;"
    )


def connect(test: bool = False):

    load_dotenv(env_path)
    DB_PASSWORD = os.environ.get("LEFAIRE_PASSWORD")

    if not DB_PASSWORD:
        setup(env_path)
        DB_PASSWORD = os.environ.get("LEFAIRE_PASSWORD")

    DB = "lefaire"
    if test:
        DB = "lefaire_test"
    try:
        conn = get_connect(DB)
        if test:
            cur = conn.cursor()
            increment_reset(cur)
            conn.commit()
        return conn

    except mariadb.Error as e:
        pass
        error(f"Erreur de connection ({e})")
        setup()
        load_dotenv(env_path)
        print(warning("La connection a été réinitialisée. Veuillez réessayer"))
        sys.exit(1)


def get_connect(db):
    conn = mariadb.connect(
        user="lefaire",
        host=os.environ["LEFAIRE_HOST"],
        password=os.environ["LEFAIRE_PASSWORD"],
        database=db,
    )
    return conn


def increment_reset(cur):
    cur.execute("ALTER TABLE Project AUTO_INCREMENT=1")
    cur.execute("ALTER TABLE Task AUTO_INCREMENT=1")
