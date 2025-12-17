@Library('jenkins-shared-library@v1') _

/**
 * Demo Flask API - CI/CD Pipeline
 * 
 * Uses jenkins-shared-library for reusable pipeline steps.
 * Branch logic is defined here; execution steps are in the library.
 * 
 * Branch behavior:
 *   - main/master: Full pipeline (lint → test → build → deploy)
 *   - release/*:   Lint → test → build (no deploy)
 *   - feature/*:   Lint → test only
 *   - All others:  Lint → test only
 */

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
        // ============================================
        // Stage 1: Checkout Code
        // ============================================
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        // ============================================
        // Stage 2: Setup Python Environment
        // ============================================
        stage('Setup') {
            steps {
                pythonSetup(
                    requirementsFile: 'requirements.txt'
                )
            }
        }

        // ============================================
        // Stage 3: Code Quality - Linting
        // ============================================
        stage('Lint') {
            steps {
                pythonLint(
                    targetDirs: ['app/'],
                    failOnError: true
                )
            }
        }

        // ============================================
        // Stage 4: Run Tests
        // ============================================
        stage('Test') {
            steps {
                pythonTest(
                    testDir: 'tests/',
                    coverageSource: 'app',
                    junitReport: true,
                    htmlReport: true
                )
            }
        }

        // ============================================
        // Stage 5: Build Docker Image
        // Branch rule: Only on main, master, or release/*
        // ============================================
        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'release/*'
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

        // ============================================
        // Stage 6: Deploy
        // Branch rule: Only on main or master
        // ============================================
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
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

    // ============================================
    // Post-build Actions
    // ============================================
    post {
        success {
            pipelineNotify(status: 'SUCCESS')
        }
        failure {
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

// Full webhook test: Wed Dec 17 12:28:24 CST 2025
