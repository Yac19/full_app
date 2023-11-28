
 # App_OwnCloud_Project-B

### Le projet B a pour finalité de transformer une **application monolithique** en **micro-services** et l’intégrer de manière automatisée via **pipeline CI/CD** en veillant à intégrer les principes suivants :

### 1. **DevSec**
  * Sécurité du code source
  * tests fonctionnels
### 2. **SecOps**
  * sécurité des configurations
  * sécurité des environnements
  * sécuriser les accès
  * mise en place d’une stack d’observabilité

# Contributeurs
* [Yacine BEN HAMIDA](https://github.com/Yac19)
* [Jorge DOS SANTOS](https://github.com/Jrgds)
* [Haythem CHAABANI](https://github.com/HaythemCH69)


# Pré-requis
Pour réaliser ce projet on a installé sur la machine :
* **[VScode](https://code.visualstudio.com/)**, un éditeur de code source gratuit et open source développé par Microsoft permettant de créer, éditer et déboguer du code source dans divers langages de programmation.  
* **[Jenkins](https://www.jenkins.io/)**, un outil **d'intégration continue (CI)** et de **livraison continue (CD)** open source ayant pour objectif l'automatisation du processus de construction, de test et de déploiement des applications logicielles. 
* **[Docker](https://www.docker.com/)**, une plateforme de **conteneurisation** qui permet d'emballer une application et ses dépendances dans un conteneur léger, isolé et portable. 
* **[AWS](https://eu-west-1.console.aws.amazon.com/console/home?region=eu-west-1), notre 

# L'architecture
Voici l'architecture choisi pour mettre en place notre projet:
  * ![Diagramme_Project_B_]( https://github.com/Yac19/full_app/blob/dev/Diagramme__Project_B.jpg?raw=true )


# Les éléments constitutifs de notre Projet

## Choix de l'application monolithique: 

Pour la mise en place de ce projet, nous avions choisi [OwnCloud](https://owncloud.com/): une plateforme d'hébergement open source proposant des services de stockages et de partages de fichiers en ligne assorti d'une plateforme de collaboration qui s'appuie la suite bureautique OnlyOffice. Elle offre une alternative autogérée aux services de stockage en ligne tels que Dropbox, Google Drive et Microsoft OneDrive, permettant aux utilisateurs de conserver le contrôle total sur leurs données tout en bénéficiant de fonctionnalités de partage et de collaboration.
Pour implémenter notre projet nous avons suivi la documentation présenté sur le site https://doc.owncloud.com/server/next/ , consulté pendant les mois de août et septembre 2023.

* L’application monolithique OwnCloud est composée de trois conteneurs Docker: OnwCloud_server, Mariadb, Redis. On a installé l’application monolithique via le script docker-compose.yml présenté dans la documentation OwnCloud sur la page web https://doc.owncloud.com/server/10.13/admin_manual/installation/docker/ .  

* Nous avions transformé cette application monolithique en rajoutant les deux micro-services avec la création d'un fichier en python "app.py". Nous n'avions pas développé la partie front-end pour chaque micro-service.


## Les micro-services :

On a choisi de créer deux micro-services: 

* 1- La gestion des utilisateurs (création des utilisateurs) permettant la création d'un nouvel utilisateur, la suppression ainsi que la mise-à-jour d'un utilisateur.
 Ce micro-service permet l’édition du mot de passe de chaque user. Il est mis dedans un conteneur Docker et est lié à un autre conteneur Docker pour le stockage des logs concernant l’extension pour le framework web Python : le Flask-limiter

* 2- La gestion des mots de passe (modification de mot de passe pour chaque utilisateur).


## Serveur Nginx:
Nous avons mis en place un conteneur Docker incluant un serveur Nginx, pour l’utilisé comme **reverse proxy** (ou proxy inverse) afin de rediriger le trafic : soit vers l’application monolithique, soit vers les micro-services. Dans ce conteneur on a configurer le framework fail2ban. L’accès à l’instance OwnCloud est configuré pour se réaliser via le port 80 (HTTP), car selon la documentation ( https://doc.owncloud.com/server/10.13/admin_manual/installation/docker/ ) l'accès ne fonctionne qu'avec http, pas avec https. 


## Le pare feu :
* On a pas mis le pare feu dedans un conteneur, car  il est généralement recommandé de configurer et de gérer le pare-feu au niveau de l'hôte. Techniquement, il est possible d'exécuter un pare-feu (firewall) dans un conteneur Docker, mais cela n'est généralement pas recommandé ni pratique. Pour une meilleur sécurisation il faut l’installer au niveau de l'hôte, par exemple via un playbook Ansible. Selon la documentation de Docker ( https://docs.docker.com/network/packet-filtering-firewalls/ ) c’est pas recommandable activer le pare feu UFW. 


## La stack d’observabilité

* En ce qui concerne la stack d’observabilité on a mis en place un conteneur docker avec Grafana, autre avec Prometheus, autre avec Netdata et autre avec Jaeger. Ils sont accessibles seulement au niveau local. On n’a pas fait la configuration de la stack d’observabilité, elle doit être réalisé manuellement via un navigateur.

* Netdata est installé sur le serveur à superviser. Netdata fournit des visualisations en temps réel des métriques système et applicatives (CPU, mémoire, utilisation disque, ...). Toutes ces données sont collectées et stockées dans Prometheus. Ensuite pour analyser ces données, et en sortir des graphiques on utilise Grafana.
Jaeger est une plateforme open-source de traçage distribué. On le utilise pour le suivi des transactions et le diagnostic des performances dans les architectures micro-services. Il permet de suivre le cheminement des requêtes à travers différents composants d'une application distribuée. Il peut aider à identifier les goulots d'étranglement, à améliorer les performances et à résoudre les problèmes de latence dans les systèmes complexes. 


# Feuille de route suivi
Voici un résumé des étapes que nous avons suivies pour transformer une application monolithique en micro-services et l’intégrer de manière automatisée via pipeline CI/CD :
      	
### Découpage de l'application monolithique
### Choix de la technologie : Flask (Python)
### Mise en place de l'environnement de développement
      
* Configuration de l'environnement de développement local avec Flask (Installation des dépendances, Configuration de la base de données) en installant des bibliothèques nécessaires, telles que Flask, Flask-Limiter et Flask-SQLAlchemy.  
      
### Développement de la API avec des fonctionnalités
* Configuration de l'environnement 
* Connexion au monolithe (Intégration de l'API OwnCloud dans les micro-services)
* Définition du modèle de données (Modélisation de la commande dans SQLAlchemy).
    * Concernant le micro-service pour la gestion des utilisateurs nous avons défini un modèle SQLAlchemy pour la table OwnCloud Users qui inclut un identifiant et un nom d'utilisateur.
    * On a fait de façon pareil pour la table OwnCloud Groups concernant le micro-service « gestion des mots de passe ». Vous pouvez ajouter d'autres colonnes au modèle au besoin.   
* Implémentation des routes.  
	* Nous avons créé des routes pour l'application, notamment:   
	* Une route racine qui vérifie si l'application fonctionne correctement.   
	* Une route pour la redirection vers OwnCloud.   
	* Des routes pour l'enregistrement, la suppression, la mise à jour et la synchronisation des utilisateurs (concernant le micro-service pour la gestion des utilisateurs). 
	* Une route pour éditer le mot de passe (concernant le micro-service pour la gestion des mots de passe) 
	* Une route pour obtenir la liste des utilisateurs. 
* Gestion des erreurs.
    * Nous avons géré les erreurs et les exceptions à l'aide de codes de statut HTTP appropriés et de réponses JSON pour indiquer le succès ou l'échec des opérations.   
* Optimisation et sécurité
    * Gestion des taux d'appels avec Flask-Limiter, utilisation des variables d'environnement, etc.   
    * Dans le micro-service concernant la gestion des mots de passe on a mis la base de données backup pour Flask-Limiter dans un autre conteneur.
* Utilisation de Docker
    * On a configuré un environnement Docker pour l'application en créant des fichiers Dockerfile pour Flask et Nginx et on a utilisé Docker Compose pour gérer les conteneurs.   
* Configuration de Nginx comme proxy inverse 
	* Nous avons configuré Nginx dans un autre conteneur en tant que proxy inverse pour diriger le trafic depuis le port 80 vers notre application Flask et vers l'application monolithique.   
* Communication entre les conteneurs Docker 
	* La communication entre les conteneurs Docker est assuré en utilisant les noms de service (ou les adresses IP privées) définis dans le fichier Docker Compose pour que Nginx puisse rediriger le trafic vers Flask et OwnCloud.   
* Gestion de la base de données OwnCloud 
	* On a vérifié le bon fonctionnement des opérations sur une base de données SQLite OwnCloud à l'aide de Python et de l'extension SQLite3 sur VSCode.     
* Utilisation de Curl (et le ThunderClient sur VSCode) pour tester l'API   
	* On a testé les différentes fonctionnalités de l'API, telles que l'enregistrement, la synchronisation, la suppression, etc.   
	* La communication entre les conteneurs Docker et l’application monolithique est assuré en utilisant les noms de service (ou les adresses IP privées) définis dans le fichier Docker Compose pour que Nginx puisse rediriger le trafic vers Flask et OwnCloud.   
### Tests
* On a crée des tests pour vérifier le bon fonctionnement et intégration des micro-services.
### Déploiement avec Docker (en mode rootless, pour une question de sécurité).   
### Intégration et le déploiement continus via Jenkins
* On a ajouté des secrets sur Jenkins en ce qui concerne les mots de passe, les identifiants, etc.


# Pipeline CI/CD

* Le pipeline CI/CD réalisé via Jenkins a permis l'intégration et le déploiement continu de notre application publié sur GitHub:

  * Intégration continue avec GitHub.  
  * Build des images Docker  
  * Tests automatisés  
  * Déploiement continu sur des environnements  
  * Déploiement  

* Pour la mise en place du pipeline CI/CD nous avons utilisé Jenkins avec un CRONO pour réaliser une mise à jour périodiquement.


# Installation du projet
* Créer un dossier dans lequel on installera le projet: ```mkdir project-B```
* On clone le repo: ```git clone https://github.com/Yac19/full_app.git```
* Lancer le logiciel Docker (en mode rootless, pour une question de sécurité)
* Sur un terminal PowerShell, on se place dedans le répertoire où se trouve le fichier « docker-compose.yml « 
* Sur le terminal PowerShell, on execute la commande « docker-compose up »
* On peut vérifier le fonctionnement et l’intégration des micro-services avec l'application monolithique via le ThunderClient sur VSCode.   
