from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_queries = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table_name = table_name
        self.sql_queries = sql_queries

    def execute(self, context):
        self.log.info('LoadFactOperator preparing for execution')
        redshift_hook = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        redshift_hook.run(self.sql_queries)
        
