from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = '',
                 tables = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.tables = tables

    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Check records in tables')
        # make sure there are records in table by performing a row count
        for table in self.tables:
            records_count = redshift_hook.get(f"SELECT COUNT(*) FROM {table}")
            self.log.info(f"table {table} : {records_count[0][0]} records")
            if records_count < 1 or len(records[0]) < 1 or records[0][0] < 1:
                raise ValueError(f"table {table} contains no records")
            else:
                self.log.info(f"Data quality check for table {table} is successful!")
                