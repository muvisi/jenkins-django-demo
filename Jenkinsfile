
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        // Replace with your actual domain and email
        DJANGO_DOMAIN = 'demo.nachat.co.ke'
        LETSENCRYPT_EMAIL = 'mwangangimuvisi@gmail.com'
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
                    set -eu
                    python3 --version
                    ansible --version
                    git --version
                '''
            }
        }

        stage('Django Tests') {
            steps {
                sh '''
                    set -eu
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
                    set -eu
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

        stage('Configure HTTPS / SSL') {
            when {
                expression {
                    return env.DJANGO_DOMAIN?.trim() &&
                           env.LETSENCRYPT_EMAIL?.trim()
                }
            }

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
                            --become-password-file "$PASSFILE" \
                            --extra-vars "django_domain=$DJANGO_DOMAIN letsencrypt_email=$LETSENCRYPT_EMAIL"
                    '''
                }
            }
        }

        stage('Verify HTTPS') {
            when {
                expression {
                    return env.DJANGO_DOMAIN?.trim() &&
                           env.LETSENCRYPT_EMAIL?.trim()
                }
            }

            steps {
                sh '''
                    set -eu
                    curl --fail --show-error --silent \
                        --retry 5 \
                        --retry-delay 3 \
                        --max-time 20 \
                        "https://${DJANGO_DOMAIN}/health/"
                '''
            }
        }
    }

    post {
        success {
            echo 'Django pipeline completed successfully.'
            echo 'Review the HTTPS stages to confirm whether SSL was configured.'
        }

        failure {
            echo 'Pipeline failed. Review Jenkins console output.'
        }

        always {
            sh 'rm -f django-release.tar.gz'
        }
    }
}
