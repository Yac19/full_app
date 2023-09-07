/* This Jenkinsfile defines a pipeline with three stages: Clone, Build and Test. 
The pipeline starts by checking out the source code from the version control system. Then it will 
builds the docker images through the Dockerfile for jenkins and the flask-app. Finally, we build
all the containers throught the pre-created images in order to deploy the application to a remote 
server using SCP.*/

pipeline {
    agent any

    stages {
        stage('Build the Docker images of the microservice and jenkins') {
            steps {
                echo 'Initiating the contruction of the App image with the app.py....'
                sh 'whoami'
                sh 'ls'
                sh 'if [ -f Dockerfile_flask_app ]; then echo "Docker file found ! Initiating the construction of the microservice image !"; fi'
                sh "docker build -t flask-app -f Dockerfile_flask_app ."
                sh 'if [ -f Dockerfile ]; then echo "Docker file found ! Initiating the build of Jenkins image !"; fi'
                sh "docker build -t jenkins_microservice -f Dockerfile ."
            }
        }
        stage('Test') {
            steps {
                echo 'Creation of the containers through pre-created docker images...'
                sh 'if [ -f docker-compose.yaml ]; then echo "Docker compose found ! Initiating the build of al the images for Owncloud app ! "; fi'
                sh "docker-compose up -d"
            }
        }
    }
}
