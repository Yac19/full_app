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
            }
        }
        stage('Run') {
            steps {
                echo 'Creation of the containers through pre-created docker images...'
                sh 'if [ -f docker-compose.yaml ]; then echo "Docker compose found ! Initiating the build of al the images for Owncloud app ! "; fi'
                sh "docker-compose up -d"
            }
        }
        stage('Performance tests') {
            steps {
                script {
                    // Téléchargez JMeter (si nécessaire) et décompressez-le
                    echo 'Downloading JMeter app for performance tests... Please be patient'
                    sh 'wget -q http://downloads.apache.org/jmeter/binaries/apache-jmeter-5.4.1.tgz'
                    sh 'tar -xzf apache-jmeter-5.4.1.tgz'

                    // Création d'un dossier pour les tests
                    sh 'mkdir perf_test'

                    // Exécutez le test JMeter
                    echo 'Executing JMEter app'
                    
                    sh './apache-jmeter-5.4.1/bin/jmeter -n -t perf_test/test-plan.jmx -l results.jtl'

                    // Générez un rapport HTML à partir des résultats
                    echo 'Generating an HTML log'
                    sh './apache-jmeter-5.4.1/bin/jmeter -g results.jtl -o report/'

                    // Archivage du rapport
                    archiveArtifacts 'report/**'
                }
            }
        }
    }
}
