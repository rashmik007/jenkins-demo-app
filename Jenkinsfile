@Library('jenkins-shared-library@v1') _

pipeline {
    agent any

    environment {
        APP_NAME = 'demo-flask-api'
        CONTAINER_NAME = 'demo-flask-app'
        HOST_PORT = '5001'
        CONTAINER_PORT = '5000'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
      
        stage('Checkout') {
            steps {                                           
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

       
        stage('Setup') {
            steps {                                           // Setup Python environment
                pythonSetup(
                    requirementsFile: 'requirements.txt'
                )
            }
        }

        
        stage('Lint') {
            steps {                                           // Lint code
                pythonLint(
                    targetDirs: ['app/'],
                    failOnError: true
                )
            }
        }

        
        stage('Test') {
            steps {                                           // Run tests
                pythonTest(
                    testDir: 'tests/',
                    coverageSource: 'app',
                    junitReport: true,              
                    htmlReport: true
                )
            }
        }

        
        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'release/*'                          // Build on main, master, or release branches
                }
            }
            steps {
                script {
                    def image = dockerBuild(
                        imageName: env.APP_NAME,
                        additionalTags: ['latest']
                    )
                    echo "Built image: ${image}"
                }
            }
        }

        
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'                               // Deploy to main or master
                    branch 'master'
                }
            }
            steps {
                dockerDeploy(
                    imageName: "${APP_NAME}:latest",
                    containerName: env.CONTAINER_NAME,
                    hostPort: env.HOST_PORT,
                    containerPort: env.CONTAINER_PORT,
                    healthCheckUrl: "http://host.docker.internal:${HOST_PORT}/",
                    healthCheckRetries: 3,
                    healthCheckDelay: 5
                )
            }
        }
    }


    post {
        success {
            pipelineNotify(status: 'SUCCESS')
        }
        failure {                                           // Post-build actions
            pipelineNotify(status: 'FAILURE')
        }
        aborted {
            pipelineNotify(status: 'ABORTED')
        }
        always {
            cleanupWorkspace(
                deleteVenv: true,
                deleteCoverage: true,
                deleteTestResults: true
            )
        }
    }
}


