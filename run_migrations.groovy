pipeline {
    agent any
    stages {
        stage('Database init') {
            steps {
                cmd = """#!/bin/sh -e\n' + 'python3 run_migrations.py  ${TENANT_NAMES} ${MIGRATION_NAME}"""
                sh(script: cmd)
            }
    }
    }
}

