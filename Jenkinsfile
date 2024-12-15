pipeline {
    agent {label "linux"}

    options {
        // Disable concurrent builds
        disableConcurrentBuilds()
        
        // Keep the last 5 builds
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    stages {
        stage('Build') {
            steps {
                echo 'Hello'
            }
        }
    }
}
