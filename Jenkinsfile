pipeline {
    agent any

    environment {
            OWNCLOUD_VERSION=credentials('OWNCLOUD_VERSION')
            OWNCLOUD_DOMAIN=credentials('OWNCLOUD_DOMAIN')
            OWNCLOUD_TRUSTED_DOMAINS=credentials('OWNCLOUD_TRUSTED_DOMAINS')
            ADMIN_USERNAME=credentials('ADMIN_USERNAME')
            ADMIN_PASSWORD=credentials('ADMIN_PASSWORD')
            HTTP_PORT=credentials('HTTP_PORT')
        }
    
    stages {
        stage('Build the Docker images of the microservice and Nginx') {
            steps {
                sh 'whoami'
                sh 'ls'
                echo 'Initiating the contruction of the App image with the app.py...'
                sh 'if [ -f Dockerfile-flask ]; then echo "Docker file found ! Initiating the construction of the microservice image !"; fi'
                sh "docker build -t flask-app -f Dockerfile-flask ."
                echo 'Initiating the contruction of the Nginx image'
                sh 'if [ -f Dockerfile-nginx ]; then echo "Docker file found ! Initiating the construction of the microservice image !"; fi'
                sh "docker build -t nginx -f Dockerfile-nginx ."        
            }
        }
        stage('Run the containers') {
            steps {
                echo 'Creation of the containers through pre-created docker images...'
                sh 'if [ -f docker-compose.yml ]; then echo "Docker compose found ! Initiating the build of al the images for Owncloud app ! "; fi'
                sh "docker-compose up -d"
            }
        }
    }
}
