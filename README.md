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

Pour la mise en place de ce projet nous avons choisi OwnCloud: un logiciel libre que offre une plateforme de services de stockage et partage de fichiers et d'applications diverses en ligne.


# Contributeurs
* Haythem
* Jorge
* Yacine


# Pré-requis
Pour réaliser ce projet on a installé sur la machine :
* git ou un IDE intégrant git (le VSCode)
* Jenkins
* Docker


# Les éléments constitutifs de notre Projet
  * Une a application monolithique
  * Micro-service Gestion Users
  * Micro-service Édition de Mot de Passe
  * Serveur Nginx


# L'architecture
Voici l'architecture choisi pour mettre en place notre projet:
  * ![Diagramme_Project_B_-1](https://github.com/Yac19/full_app/assets/133639660/f2e3c603-b56d-4133-90d2-e943cfd637a6)



# L’application monolithique 
  * L’application monolithique OwnCloud est composée par trois conteneurs Docker: OnwCloud_server, Mariadb, Redis.
  * Nous avons transformé cette application monolithique en rajoutant deux micro-services. Cependant, nous n'avons pas développé la partie front-end pour chaque micro-service.
 

# Micro-service Gestion Users
* Ce micro-service permet la création d'un nouveau utilisateur et aussi la suppression et mise-à-jour d'un utilisateur. Il est mis dedans un conteneur Docker.

# Micro-service Édition de Mot de Passe
  * Ce micro-service permet l’édition du mot de passe de chaque user. Il est mis dedans un conteneur Docker et est lié à un autre conteneur Docker pour le stockage des logs concernant l’extension pour le framework web Python : le Flask-limiter


# Serveur Nginx
  * Nous avons mis en place un conteneur Docker incluant un serveur Nginx, pour l’utilisé comme proxy inverse à fin de rediriger le trafic : soit vers l’application monolithique, soit vers les micro-services. Dedans ce conteneur nous avons aussi prévu l’activation d’une interface de gestion de pare-feu: le UFW.


# Pipeline CI/CD

Le pipeline CI/CD permet l'intégration et le déploiement continus:

- Intégration continue avec GitHub.
- Build des images Docker
- Tests automatisés
- Déploiement continu sur des environnements de DEV, TEST, PROD
- Déploiement.

Pour la mise en place du pipeline CI/CD nous avons utilisé Jenkins.


		PLACER LES CAPTURES D'ÉCRAN ICI










