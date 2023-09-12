# full_app

### Le projet B a pour finalité de transformer une **application monolithique** en **micro-services** et l’intégrer de manière automatisée via **pipeline CI/CD** en veillant à intégrer les principes suivants :

1. **DevSec**
  * Sécurité du code source
  * tests fonctionnels
2. **SecOps**
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

### L'architecture
Voici l'architecture choisi pour mettre en place notre projet:
  * ![Diagramme_Project_B_](https://github.com/Yac19/full_app/blob/dev/Diagramme__ProjectB_.jpg)

### Les éléments constitutifs de notre Projet

## Choix de l'application monolite: 

Pour la mise en place de ce projet, nous avions choisi [OwnCloud](https://owncloud.com/): une plateforme d'hébergement open source proposant des services de stockages et de partages de fichiers en ligne assorti d'une plateforme de collaboration qui s'appuie la suite bureautique OnlyOffice. Elle offre une alternative autogérée aux services de stockage en ligne tels que Dropbox, Google Drive et Microsoft OneDrive, permettant aux utilisateurs de conserver le contrôle total sur leurs données tout en bénéficiant de fonctionnalités de partage et de collaboration.
Pour implémenter notre projet nous avons suivi la documentation présenté sur le site https://doc.owncloud.com/server/next/ , consulté pendant les mois de août et septembre 2023.

* L’application monolithique OwnCloud est composée de trois conteneurs Docker: OnwCloud_server, Mariadb, Redis. Dans un premeir, nous avions réaliser un push de l'image [Owncloud](https://hub.docker.com/r/owncloud/server/) et en faire par la suite un fichier docker-compose afin de déploiement d'applications composées de plusieurs conteneurs tout en définissant les configurations de l'application sous format YAML.  

* Nous avions transformé cette application monolithique en rajoutant les deux micro-services avec la création d'un fichier en python "app.py". Nous n'avions pas développé la partie front-end pour chaque micro-service.


## Les microservices :

Concernant les micro-services, on en a choisi créer 2: 

* 1- La gestion des utilisateurs (création des utilisateurs) permettant la création d'un nouvel utilisateur, la suppression ainsi que la mise-à-jour d'un utilisateur.
*Ce micro-service permet l’édition du mot de passe de chaque user. Il a été conteneurisé via Docker et lié à un autre conteneur pour le stockage des logs concernant l’extension pour le framework web Python : le Flask-limiter

* 2- La gestion des mots de passe (modification de mot de passe pour chaque utilisateur).


## Serveur Nginx:
Nous avons mis en place un conteneur Docker incluant un serveur Nginx, pour l’utilisé comme **reverse proxy** (ou proxy inverse) afin de rediriger le traffic : soit vers l’application monolithique, soit vers les micro-services. Dans ce conteneur on a configurer le framework fail2ban. L’accès à l’instance OwnCloud est configuré pour se réaliser via HTTP, car selon la documentation ( https://doc.owncloud.com/server/10.13/admin_manual/installation/docker/ ) l'accès ne fonctionne qu'avec http, pas avec https. 


## Le pare feu
* On a pas mis le pare feu sur dans un conteneur, car  il est généralement recommandé de configurer et de gérer le pare-feu au niveau de l'hôte. Techniquement, il est possible d'exécuter un pare-feu (firewall) dans un conteneur Docker, mais cela n'est généralement pas recommandé ni pratique. Pour une meilleur sécurisation il faut l’installer au niveau de l'hôte, par exemple via un playbook Ansible. Selon la documentation de [Docker](https://docs-docker-com.translate.goog/network/packet-filtering-firewalls/?_x_tr_sl=auto&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=wapp ), il n'est pas recommandé d'activer le pare feu UFW (Unprotected FireWall). 


## La stack d’observabilité

* En ce qui concerne la stack d’observabilité, on a mis en place un conteneur docker avec Grafana, un avec Prometheus, un avec Netdata et un autre avec Jaeger. Ils sont accessibles seulement au niveau local. On n’a pas fait la configuration de la stack d’observabilité, elle doit être réalisé manuellement via un navigateur.

* Netdata est installé sur le serveur à superviser. Netdata fournit des visualisations en temps réel des métriques système et applicatives (CPU, mémoire, utilisation disque, i/O, métriques Nginx, Redis). Toutes ces données sont collectées et stockées dans Prometheus. Ensuite pour analyser ces données, et en sortir des graphiques on utilise Grafana.
Jaeger est une plateforme open-source de traçage distribué. On le utilise pour le suivi des transactions et le diagnostic des performances dans les architectures micro-services. Il permet de suivre le cheminement des requêtes à travers différents composants d'une application distribuée. Il peut aider à identifier les goulots d'étranglement, à améliorer les performances et à résoudre les problèmes de latence dans les systèmes complexes. 

### Code source du micro-service

#### A REMPLIR PAR JORGE


### Pipeline CI/CD

* Le pipeline CI/CD réalisé via Jenkins a permi l'intégration et le déploiement continu de notre application publié sur GitHub:

Intégration continue avec GitHub.
Build des images Docker
Tests automatisés
Déploiement continu sur des environnements
Déploiement.

* Pour la mise en place du pipeline CI/CD nous avons utilisé Jenkins avec un CRONO pour réaliser une mise à jour périodiquement.


### Feuille de route suivi
* Découpage de l'application monolithique
* Choix de la technologie : Flask (Python)
* Mise en place de l'environnement de développement
	Configuration de l'environnement de développement local avec une base de données Sqlite
* Développement de la API avec des fonctionnalités
	Configuration de l'environnement (Installation des dépendances, Configuration de la base de données)
	Connexion au monolithe (Intégration de l'API OwnCloud dans les micro-services)
	Définition du modèle de données (Modélisation de la commande dans SQLAlchemy) .
	Implémentation des routes.
	Gestion des erreurs .
	Optimisation et sécurité (Gestion des taux d'appels avec Flask-Limiter ; utilisation des variables d'environnement).
* Tests
* Déploiement avec Docker (en mode rootless, pour une question de sécurité)
* Intégration et le déploiement continus via Jenkins

		(METTRE DES CAPTURES D'ÉCRAN SUR CHAQUE ÉLÉMENT)


### Installation du projet
* Créer un dossier dans lequel on installera le projet
* On clone le repo
* On active le logiciel Docker
* Sur un terminal PowerShell on se place dedans le répertoire où se trouve le fichier « docker-compise.yaml « 
* Sur le terminal PowerShell on execute la commande « docker-compose up »
* 
