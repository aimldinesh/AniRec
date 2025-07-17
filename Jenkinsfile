pipeline {
    agent any 

    // Define environment variables used across stages
    environment {
        VENV_DIR = 'venv'  // Directory name for Python virtual environment
        GCP_PROJECT = 'mlops-project-462105'  // Your GCP project ID
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"  // Path to gcloud SDK inside Jenkins container
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"   // Path to kubectl/GKE auth plugin
    }

    stages {

        // 🧬 Stage 1: Clone the GitHub repository
        stage("Cloning from GitHub") {
            steps {
                script {
                    echo 'Cloning from GitHub...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'gitub-token',  // Your GitHub personal access token ID from Jenkins credentials
                            url: 'https://github.com/aimldinesh/AniRec.git'
                        ]]
                    )
                }
            }
        }

        // 🐍 Stage 2: Set up a virtual environment and install dependencies
        stage("Making a Virtual Environment") {
            steps {
                script {
                    echo 'Creating virtual environment and installing dependencies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .    # Install your package if setup.py is present
                    pip install dvc     # Install DVC for versioned data pulling
                    '''
                }
            }
        }

        // 📦 Stage 3: Pull versioned data using DVC
        stage('DVC Pull') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Pulling data with DVC...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull  # Downloads required data files from remote storage
                        '''
                    }
                }
            }
        }

        // 🛠️ Stage 4: Build Docker image and push to Google Container Registry (GCR)
        stage('Build and Push Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        // 🚀 Stage 5: Deploy the application to Kubernetes (GKE)
        stage('Deploying to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying application to GKE cluster...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}
