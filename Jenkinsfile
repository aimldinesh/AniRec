pipeline {
    agent any 

    stages {
        stage("Cloning from github....."){
            steps {
                script{
                    echo 'Cloning from github.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'gitub-token', url: 'https://github.com/aimldinesh/AniRec.git']])
                }
            }
        }
    }
}