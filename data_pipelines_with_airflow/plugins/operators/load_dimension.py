from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table_name = "",
                 sql_queries = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table_name = table_name
        self.sql_queries = sql_queries

    def execute(self, context):
        self.log.info('LoadDimensionOperator ready for execution')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f"Running query to load data into Dimension Table {self.table_name}")
        redshift_hook.run(self.sql_queries)
        self.log.info(f"Dimension Table {self.table_name} completed loading.")
