pipeline {
    agent any
    stages {
        stage('Database init') {
            steps {
               script { cmd = """python3 /home/run_migrations.py  ${TENANT_NAMES} ${MIGRATION_NAME} ${RUN_TYPE}"""
                result = sh(returnStdout:true , script: cmd).trim()
                echo "Python output: ${result}"     
            }
            }
    }
    }
}