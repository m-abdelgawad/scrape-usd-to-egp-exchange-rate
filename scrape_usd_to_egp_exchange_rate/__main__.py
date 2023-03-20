import os
import yaml
import traceback
from packages.file import file
from packages.logger import logger
from packages.helpers import helpers
from packages.postgredb import postgredb
from packages.datetimetools import datetimetools

# Initiate logger
log = logger.get(app_name='logs', enable_logs_file=True)


def main():

    log.info('Start program execution...')

    proj_abs = file.caller_dir_path()

    # Import configurations
    config_path = os.path.join(proj_abs, 'config.yaml')
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Get the path of the chrome driver
    # driver_path = os.path.join(proj_abs, 'data/input/chromedriver_linux')
    driver_path = os.path.join(proj_abs, 'data/input/chromedriver_win.exe')

    egp_rate = helpers.get_egp_rate(driver_path)

    # Get current timestamp
    current_timestamp = datetimetools.get_current_timestamp()
    log.info(
        '1USD to EGP = {0} on {1}'.format(
            egp_rate,
            current_timestamp
        )
    )

    # Create a database instance
    db = postgredb.PostgreSQLDB(
        host=config['database']['host'],
        db_name=config['database']['database_name'],
        username=config['database']['username'],
        password=config['database']['password']
    )

    log.info('Start creating the database\'s table if not already exists...')
    # Read query
    create_table_query = file.read(
        os.path.join(
            proj_abs,
            'data/input/create_table_query.txt'
        )
    )
    # Execute query
    db.run_query(query=create_table_query)
    # Commit the transaction
    db.commit()
    log.info('Finished creating the database\'s table')

    log.info('Start checking number of rows in the table...')
    results = db.get_rows_count(table_name=config['database']['table_name'])
    rows_count = results[0][0]
    log.info('There are {0} rows in the table {1}'.format(
        rows_count, config['database']['table_name']
    ))
    log.info('Finished checking number of rows in the table')

    # Insert a row if there are no rows in the table OR update the top row
    # if there is a row already.
    if rows_count == 0:
        log.info('Start inserting a new row into the database')
        # Insert the USD to EGP rate into the database
        insert_query = file.read(
            os.path.join(
                proj_abs,
                'data/input/insert_query.txt'
            )
        )
        values_list = [
            current_timestamp,
            egp_rate
        ]
        db.insert(insert_query=insert_query, values_list=values_list)
        log.info('finished inserting a new row into the database')
    else:
        log.info('Start updating a row into the database')
        # Insert the USD to EGP rate into the database
        insert_query = file.read(
            os.path.join(
                proj_abs,
                'data/input/update_query.txt'
            )
        )
        values_list = [
            current_timestamp,
            egp_rate
        ]
        db.update(update_query=insert_query, values_list=values_list)
        log.info('finished updating a row into the database')

    log.info('Finished program execution')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log.error(e)
        log.error('Error Traceback: \n {0}'.format(traceback.format_exc()))
