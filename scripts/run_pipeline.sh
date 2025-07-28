#!/bin/bash

#Settings
LOG_DIR="logs"
OUTPUT_DIR="reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/pipeline_${TIMESTAMP}.log"

#Create diretories if they do not exist 
mkdir -p ${LOG_DIR}
mkdir -p ${OUTPUT_DIR}

#Start Logging
echo "Starting Github Analysis Pipeline - ${TIMESTAMP}" | tee -a ${LOG_FILE}

#Check Docker
echo "Checking docker..." | tee -a ${LOG_LIFE}
if ! docker ps > /dev/null 2>&1; then
    echo "Docker is not running. Starting Docker... " | tee -a ${LOG_FILE}
    sudo systemctl start docker || {echo "Error starting docker"; exit 1; }
fi

#Start PostgreSQL
echo "Starting PostgreSQL..." | tee -a ${LOG_LIFE}
docker-compose up -d || { echo "Error starting PostgreSQL "; exit 1; }

#Wait for PostgreSQL to be ready 
