pipeline {
    agent any

    environment {
        APP_NAME = 'demo-flask-api'
        DOCKER_IMAGE = "demo-flask-api:${BUILD_NUMBER}"
        CONTAINER_NAME = 'demo-flask-app'
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
        // Stage 2: Install Dependencies
        // ============================================
        stage('Install Dependencies') {
            steps {
                echo '📦 Setting up Python virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // ============================================
        // Stage 3: Code Quality - Linting
        // ============================================
        stage('Lint') {
            steps {
                echo '🔍 Running flake8 linter...'
                sh '''
                    . venv/bin/activate
                    flake8 app/ --count --show-source --statistics
                '''
            }
        }

        // ============================================
        // Stage 4: Run Tests
        // ============================================
        stage('Test') {
            steps {
                echo '🧪 Running pytest with coverage...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
                '''
            }
            post {
                always {
                    echo '📊 Test stage completed'
                }
            }
        }

        // ============================================
        // Stage 5: Build Docker Image
        // ============================================
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE} .
                    docker tag ${DOCKER_IMAGE} ${APP_NAME}:latest
                '''
            }
        }

        // ============================================
        // Stage 6: Deploy
        // ============================================
        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                sh '''
                    # Stop and remove existing container if running
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    # Run new container (using port 5001 to avoid macOS AirPlay conflict)
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 5001:5000 \
                        ${APP_NAME}:latest

                    # Wait for container to start
                    sleep 5

                    # Health check (using host.docker.internal to reach host from Jenkins container)
                    curl -f http://host.docker.internal:5001/ || exit 1

                    echo '✅ Application deployed successfully!'
                    echo '🌐 Access the API at: http://localhost:5001'
                '''
            }
        }
    }

    // ============================================
    // Post-build Actions
    // ============================================
    post {
        success {
            echo '''
            ✅ ========================================
            ✅ Pipeline completed successfully!
            ✅ ========================================
            '''
        }
        failure {
            echo '''
            ❌ ========================================
            ❌ Pipeline failed! Check the logs above.
            ❌ ========================================
            '''
        }
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv || true'
        }
    }
}

