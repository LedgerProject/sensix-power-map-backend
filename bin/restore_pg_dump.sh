#!/usr/bin/env bash

# Usage examples:

# sudo ./bin/restore_pg_dump.sh dev sensix_map_backend ./tmp/sensix_map_backend.custom
# sudo ./bin/restore_pg_dump.sh prod sensix_map_backend /sensix/backup/dumps/postgres2021-02-14-daily/sensix_map_backend.custom

ENV_ID="$1"
DATABASE_NAME="$2"
DATABASE_USER="$2_user"
DUMP_FILE_PATH="$3"

check_error() {
    # Function. Parameter 1 is the return code
    # Para. 2 is text to display on failure.
    if [[ "${1}" -ne "0" ]]; then
        echo "[ERROR] # ${1} : ${2}"
        # as a bonus, make our script exit with the right error code.
        exit ${1}
    fi
}

function drop_database() {
    dropdb -h localhost -U ${DATABASE_USER} ${DATABASE_NAME}
}

function provision_postgres() {
    salt-call -l info --local --id ${ENV_ID} state.apply postgres
    check_error $? "Fail to provision postgres"
}

function restore_database() {
    pg_restore --verbose --clean --no-acl --no-owner -h localhost -d ${DATABASE_NAME} -U ${DATABASE_USER} ${DUMP_FILE_PATH}
}

function migrate_database() {
    salt-call -l info --local --id ${ENV_ID} state.apply sensix_map_backend.django
    check_error $? "Fail to migrate database and rebuild indexes"
}

echo "WARNING: You are about to completely delete the ${DATABASE_NAME} database, within ${ENV_ID} environment!"

drop_database
provision_postgres
restore_database
migrate_database
