pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
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

        stage('Provision VPS') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'django-vps-sudo',
                        variable: 'BECOME_PASSWORD'
                    )
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
    }

    post {
        success {
            echo 'Jenkins pipeline completed successfully.'
        }
        failure {
            echo 'Jenkins pipeline failed. Check the console output.'
        }
    }
}
