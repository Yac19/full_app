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


# Les éléments constitutifs de notre Projet

### Choix de l'application monolite: 

Pour la mise en place de ce projet, nous avions choisi [OwnCloud](https://owncloud.com/): une plateforme d'hébergement open source proposant des services de stockages et de partages de fichiers en ligne assorti d'une plateforme de collaboration qui s'appuie la suite bureautique OnlyOffice. Elle offre une alternative autogérée aux services de stockage en ligne tels que Dropbox, Google Drive et Microsoft OneDrive, permettant aux utilisateurs de conserver le contrôle total sur leurs données tout en bénéficiant de fonctionnalités de partage et de collaboration.
Pour implémenter notre projet nous avons suivi la documentation présenté sur le site https://doc.owncloud.com/server/next/ , consulté pendant les mois de août et septembre 2023.

### Choix des microservices :

Concernant les micro-services, on en a choisi 2: 

# 1- La gestion des utilisateurs (création des utilisateurs) permettant la création d'un nouvel utilisateur, la suppression ainsi que la mise-à-jour d'un utilisateur.
*Ce micro-service permet l’édition du mot de passe de chaque user. Il est mis dedans un conteneur Docker et est lié à un autre conteneur Docker pour le stockage des logs concernant l’extension pour le framework web Python : le Flask-limiter

2- La gestion des mots de passe (modification de mot de passe pour chaque utilisateur).


### Serveur Nginx:
Nous avons mis en place un conteneur Docker incluant un serveur Nginx, pour l’utilisé comme **reverse proxy** (ou proxy inverse) afin de rediriger le traffic : soit vers l’application monolithique, soit vers les micro-services. Dans ce conteneur on a configurer le framework fail2ban. L’accès à l’instance OwnCloud est configuré pour se réaliser via HTTP, car selon la documentation ( https://doc.owncloud.com/server/10.13/admin_manual/installation/docker/ ) l'accès ne fonctionne qu'avec http, pas avec https. 


### Le pare feu
* On a pas mis le pare feu sur dans un conteneur, car  il est généralement recommandé de configurer et de gérer le pare-feu au niveau de l'hôte. Techniquement, il est possible d'exécuter un pare-feu (firewall) dans un conteneur Docker, mais cela n'est généralement pas recommandé ni pratique. Pour une meilleur sécurisation il faut l’installer au niveau de l'hôte, par exemple via un playbook Ansible. Selon la documentation de Docker ( https://docs-docker-com.translate.goog/network/packet-filtering-firewalls/?_x_tr_sl=auto&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=wapp ) c’est pas recommandable activer le pare feu UFW. 



# L'architecture
Voici l'architecture choisi pour mettre en place notre projet:
  * ![Diagramme_Project_B_](https://github.com/Yac19/full_app/blob/dev/Diagramme__ProjectB_.jpg)


# L’application monolithique 

#### L’application monolithique OwnCloud est composée de trois conteneurs Docker: OnwCloud_server, Mariadb, Redis. Dans un premeir, nous avions réaliser un push de l'image [Owncloud](https://hub.docker.com/r/owncloud/server/) et en faire par la suite un fichier docker-compose afin de déploiement d'applications composées de plusieurs conteneurs tout en définissant les configurations de l'application sous format YAML.  

#### Nous avions transformé cette application monolithique en rajoutant les deux micro-services avec la création d'un fichier en python "app.py". Nous n'avions pas développé la partie front-end pour chaque micro-service.

# Code source du micro-service

#### A REMPLIR PAR JORGE


# Serveur Nginx
  *  Dedans ce conteneur nous avons aussi prévu l’activation d’une interface de gestion de pare-feu: le UFW.


# Pipeline CI/CD

* Le pipeline CI/CD réalisé via Jenkins a permi l'intégration et le déploiement continu de notre application publié sur GitHub:

Intégration continue avec GitHub.
Build des images Docker
Tests automatisés
Déploiement continu sur des environnements
Déploiement.

* Pour la mise en place du pipeline CI/CD nous avons utilisé Jenkins avec un CRONO pour réaliser une mise à jour périodiquement.


# Feuille de route suivi
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
* Déploiement avec Docker
* Intégration et le déploiement continus via Jenkins

		(METTRE DES CAPTURES D'ÉCRAN SUR CHAQUE ÉLÉMENT)


# Installation du projet
* Créer un dossier dans lequel on installera le projet
* On clone le repo
* On active le logiciel Docker
* Sur un terminal PowerShell on se place dedans le répertoire où se trouve le fichier « docker-compise.yaml « 
* Sur le terminal PowerShell on execute la commande « docker-compose up »
* 
