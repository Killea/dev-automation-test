pipeline {
    agent any
    stages {
        stage('Database init') {
            steps {
                sh 'mysql -h db -u root -p$MYSQL_ROOT_PASSWORD  < /home/database.sql'
            }
    }
    }
}

