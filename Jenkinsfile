/* This Jenkinsfile defines a pipeline with three stages: Clone, Build and Test. 
The pipeline starts by checking out the source code from the version control system. Then it will 
builds the docker images through the Dockerfile for jenkins and the flask-app. Finally, we build
all the containers throught the pre-created images in order to deploy the application to a remote 
server using SCP.*/

pipeline {
    agent any

    stages {
        stage("Clone the content of my Project repo on GitHub") {
            steps {
                echo 'Analyzing the files on my repo GitHub on the 1st stage..'
                sh 'if [ -d "Microservice" ]; then rm -rf Microservice/; fi'
                sh 'git clone https://github.com/Yac19/full_app.git'
                sh 'cd full_app'
                sh 'ls'
            }
        }
        stage('Build the Docker images of the microservice and jenkins') {
            steps {
                echo 'Initiating the contruction of the App image with the app.py....' 
                sh 'if [ -f Dockerfile_flask_app ];'
                sh 'then echo "Docker file found ! Initiating the construction of the microservice image !"'
                sh "docker build -t flask-app -f Dockerfile_flask_app ."
                sh 'if [ -f Dockerfile ];'
                sh 'then echo "Docker file found ! Initiating the build of Jenkins image !"'
                sh "docker build -t jenkins_microservice -f Dockerfile ."
            }
        }
        stage('Test') {
            steps {
                echo 'Creation of the containers through pre-created docker images...'
                sh 'if [ -f docker-compose.yaml ];'
                sh 'then echo "Docker compose found ! Initiating the build of al the images for Owncloud app ! "'
                sh "docker-compose up -d"
            }
        }
    }
}
