pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh '''
                    python3 --version
                    ansible --version
                    git --version
                '''
            }
        }

        stage('Django Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python manage.py check
                    python manage.py test
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    tar -czf django-release.tar.gz \
                        --exclude=.git \
                        --exclude=.venv \
                        --exclude=venv \
                        --exclude=db.sqlite3 \
                        --exclude=django-release.tar.gz \
                        --exclude=__pycache__ \
                        --exclude=.env \
                        manage.py config web requirements.txt
                '''
            }
        }

        stage('Provision VPS') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-vps-sudo', variable: 'BECOME_PASSWORD')
                ]) {
                    sh '''
                        set +x
                        set -eu
                        umask 077
                        PASSFILE=$(mktemp)
                        trap 'rm -f "$PASSFILE"' EXIT
                        printf '%s\\n' "$BECOME_PASSWORD" > "$PASSFILE"
                        unset BECOME_PASSWORD

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/provision.yml \
                            --become-password-file "$PASSFILE"
                    '''
                }
            }
        }

        stage('Deploy Django') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-vps-sudo', variable: 'BECOME_PASSWORD')
                ]) {
                    sh '''
                        set +x
                        set -eu
                        umask 077
                        PASSFILE=$(mktemp)
                        trap 'rm -f "$PASSFILE"' EXIT
                        printf '%s\\n' "$BECOME_PASSWORD" > "$PASSFILE"
                        unset BECOME_PASSWORD

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/deploy.yml \
                            --become-password-file "$PASSFILE"
                    '''
                }
            }
        }

        stage('Configure Nginx') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-vps-sudo', variable: 'BECOME_PASSWORD')
                ]) {
                    sh '''
                        set +x
                        set -eu
                        umask 077
                        PASSFILE=$(mktemp)
                        trap 'rm -f "$PASSFILE"' EXIT
                        printf '%s\\n' "$BECOME_PASSWORD" > "$PASSFILE"
                        unset BECOME_PASSWORD

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/nginx.yml \
                            --become-password-file "$PASSFILE"
                    '''
                }
            }
        }

        stage('Configure HTTPS SSL') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-vps-sudo', variable: 'BECOME_PASSWORD')
                ]) {
                    sh '''
                        set +x
                        set -eu
                        umask 077

                        PASSFILE=$(mktemp)
                        trap 'rm -f "$PASSFILE"' EXIT
                        printf '%s\\n' "$BECOME_PASSWORD" > "$PASSFILE"
                        unset BECOME_PASSWORD

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/ssl.yml \
                            --become-password-file "$PASSFILE"
                    '''
                }
            }
        }

        stage('Activate HTTPS') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-vps-sudo', variable: 'BECOME_PASSWORD')
                ]) {
                    sh '''
                        set +x
                        set -eu
                        umask 077

                        PASSFILE=$(mktemp)
                        trap 'rm -f "$PASSFILE"' EXIT
                        printf '%s\\n' "$BECOME_PASSWORD" > "$PASSFILE"
                        unset BECOME_PASSWORD

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/nginx.yml \
                            --become-password-file "$PASSFILE"
                    '''
                }
            }
        }

        stage('Verify HTTPS') {
            steps {
                sh '''
                    set -eu

                    curl --fail --show-error --silent \
                        --retry 5 \
                        --retry-delay 3 \
                        https://demo.nachat.co.ke/health/

                    curl --fail --show-error --silent \
                        http://66.23.236.42/health/
                '''
            }
        }

    }

    post {
        success {
            echo 'Django tests, provisioning and deployment completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the Jenkins console output.'
        }
        always {
            sh 'rm -f django-release.tar.gz'
        }
    }
}
