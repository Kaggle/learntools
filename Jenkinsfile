pipeline {
    agent { label 'ephemeral-linux' }
    options {
        disableConcurrentBuilds()
    }
    environment {
        GIT_COMMIT_SHORT = sh(returnStdout: true, script:"git rev-parse --short=7 HEAD").trim()
        GIT_COMMIT_SUBJECT = sh(returnStdout: true, script:"git log --format=%s -n 1 HEAD").trim()
        GIT_COMMIT_AUTHOR = sh(returnStdout: true, script:"git log --format='%an' -n 1 HEAD").trim()
        GIT_COMMIT_SUMMARY = "`<https://github.com/Kaggle/learntools/commit/${GIT_COMMIT}|${GIT_COMMIT_SHORT}>` ${GIT_COMMIT_SUBJECT} - ${GIT_COMMIT_AUTHOR}"
        MATTERMOST_CHANNEL = "#learnops"
        KAGGLE_KEY = credentials('KAGGLE_API_KEY')
        KAGGLE_USERNAME = 'dansbecker'
    }

    stages {
        stage('Initialize Test Environment') {
            steps {
                sh '''#!/bin/bash
                    set -exo pipefail
                    # Ensures the currently released Docker Python image is used.
                    docker pull gcr.io/kaggle-images/python:staging
		    docker pull gcr.io/kaggle-images/python@sha256:287c4e0e224e592dc6113940a6cf3d099b814c7bff0c1e8da57f8e6bad123ac5
                '''
            }
        }
        stage('Tests') {
            steps {
                sh '''#!/bin/bash
                    set -exo pipefail
                    ./test.sh
                '''
            }
        }
    }

    post {
        failure {
            mattermostSend color: 'danger', message: "*<${env.BUILD_URL}console|${JOB_NAME} failed>* ${GIT_COMMIT_SUMMARY} @kernels-backend-ops", channel: env.MATTERMOST_CHANNEL
        }        
        success {
            mattermostSend color: 'good', message: "*<${env.BUILD_URL}console|${JOB_NAME} passed>* ${GIT_COMMIT_SUMMARY} @kernels-backend-ops", channel: env.MATTERMOST_CHANNEL
        }
        aborted {
            mattermostSend color: 'warning', message: "*<${env.BUILD_URL}console|${JOB_NAME} aborted>* ${GIT_COMMIT_SUMMARY} @kernels-backend-ops", channel: env.MATTERMOST_CHANNEL
        }
    }
}
