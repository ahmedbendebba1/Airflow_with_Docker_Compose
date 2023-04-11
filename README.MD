


# Airflow avec Docker Compose

Ce projet fournit une configuration simple pour exécuter Apache Airflow avec Docker Compose, y compris les services webserver, scheduler, worker et une base de données PostgreSQL.


![Airflow UI](./img/airflow.png)

![DAG](./img/dag.png)



## Prérequis

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Mise en place

1. Clonez ce dépôt ou copiez les fichiers `docker-compose.yml`, `dags` et `plugins` dans un répertoire de votre choix.

2. Générez une clé Fernet en utilisant la bibliothèque `cryptography` de Python:

   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print(key.decode())
Remplacez <FERNET_KEY> dans le fichier docker-compose.yml par la clé générée.

Ouvrez un terminal, accédez au répertoire où se trouve le fichier docker-compose.yml, et exécutez la commande suivante pour démarrer les services Airflow:

  ```sh
    docker-compose up -d
```

Vous pouvez maintenant accéder à l'interface utilisateur web d'Airflow à l'adresse http://localhost:8080 dans votre navigateur.

Créer un nouveau utilisateru airflow en lancant la commande et en changeant les valeurs ("ahmed" , mail") par les valeurs de votre choix. le username et le password seront utiliser pour vous permettre de vous connecter à l'interface web de airflow
  ```sh
     docker-compose exec webserver airflow users create \
    --username ahmed \
    --password ahmed \
    --firstname ahmed \
    --lastname ahmed \
    --role Admin \
    --email mail
```


Utilisation
Ajoutez ou modifiez des DAGs dans le répertoire dags.
Ajoutez ou modifiez des plugins Airflow dans le répertoire plugins.

Commandes utiles
Vérifier l'état des conteneurs Airflow:

  ```sh
dooker-compose ps
  ```
Consulter les journaux de chaque service:

  ``` sh
docker-compose logs -f <service_name>
  ```
Arrêter les services Airflow:

  ```sh
docker-compose down
  ```
Mettre à jour les images Docker utilisées par les services Airflow:

  ```sh
docker-compose up -d
  ```
Accéder à l'interface de ligne de commande (CLI) d'Airflow:


Exécuter une commande à l'intérieur d'un conteneur spécifique:

  ```sh
docker-compose exec <service_name> <command>
  ```

## Possible bug et correction 

si vous rencontreez ce bug : 
  ```sh
psycopg2.errors.UndefinedTable: relation "dag" does not exist
LINE 2: FROM dag
  ```
Lancer cette commande :

  ```sh
docker-compose exec webserver airflow db init
  ```
Cette commande crée toutes les tables nécessaires dans la base de données PostgreSQL pour le bon fonctionnement d'Airflow.
Après avoir initialisé la base de données, redémarrez les services Airflow :
  ```sh
docker-compose down
docker-compose up -d
  ```
  
  ## Explication de code de composer-yml
  
  Le fichier docker-compose.yml est un fichier de configuration utilisé par Docker Compose pour définir et exécuter des services multi-conteneurs. Voici une explication détaillée de chaque section du fichier docker-compose.yml pour un déploiement Airflow :

  ```sh
services:
  ```
Cette section décrit les services que vous souhaitez déployer avec Docker Compose. Chaque service représente un conteneur Docker.


  ```sh
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
    volumes:
      - postgres-data:/var/lib/postgresql/data
```
Ce bloc définit le service postgres, qui utilise l'image Docker postgres:13. Les variables d'environnement définissent l'utilisateur, le mot de passe et la base de données. Le volume postgres-data est utilisé pour stocker les données de la base de données de manière persistante.

  ```sh
  webserver:
    image: apache/airflow:2.2.0
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=<FERNET_KEY>
      - AIRFLOW__WEBSERVER__SECRET_KEY=<SECRET_KEY>
    volumes:
      - ./dags:/opt/airflow/dags
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    command: airflow webserver
 ```
Ce bloc définit le service webserver, qui utilise l'image Docker apache/airflow:2.2.0. Le service webserver dépend du service postgres. Les variables d'environnement définissent la configuration d'Airflow, y compris l'exécuteur, la connexion à la base de données, la clé Fernet et la clé secrète. Les volumes ./dags et ./plugins montent les dossiers locaux dans le conteneur. Le port 8080 est exposé pour accéder à l'interface utilisateur Web. La commande airflow webserver est exécutée lors du démarrage du conteneur.

  ```sh
  scheduler:
    image: apache/airflow:2.2.0
    depends_on:
      - postgres
      - webserver
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=<FERNET_KEY>
      - AIRFLOW__WEBSERVER__SECRET_KEY=<SECRET_KEY>
    volumes:
      - ./dags:/opt/airflow/dags
      - ./plugins:/opt/airflow/plugins
    command: airflow scheduler
```
Ce bloc définit le service scheduler, qui utilise la même image Docker que le service webserver. Le service scheduler dépend des services postgres et webserver. Les variables d'environnement sont similaires à celles du service webserver, définissant la configuration d'Airflow, y compris l'exécuteur, la connexion à la base de données, la clé Fernet et la clé secrète. Les volumes ./dags et ./plugins montent les dossiers locaux dans le conteneur. La commande airflow scheduler est exécutée lors du démarrage du conteneur.

```sh
  worker:
    image: apache/airflow:2.0.0
    depends_on:
      - postgres
      - webserver
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=<FERNET_KEY>
      - AIRFLOW__WEBSERVER__SECRET_KEY=<SECRET_KEY>
    volumes:
      - ./dags:/opt/airflow/dags
      - ./plugins:/opt/airflow/plugins
    command: airflow celery worker
```
Ce bloc définit le service worker, qui utilise également la même image Docker que les services webserver et scheduler. Le service worker dépend des services postgres et webserver. Les variables d'environnement sont similaires aux autres services, définissant la configuration d'Airflow. Les volumes ./dags et ./plugins montent les dossiers locaux dans le conteneur. La commande airflow celery worker est exécutée lors du démarrage du conteneur.

```sh
volumes:
  postgres-data:
   ```
Cette section définit le volume postgres-data, qui est utilisé pour stocker les données de la base de données de manière persistante. Le volume est associé au service postgres.

.
  
Auteur
Ahmed Ben Debba
