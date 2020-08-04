from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    query = """
                COPY {}
                FROM '{}'
                ACCESS_KEY_ID '{}'
                SECRET_ACCESS_KEY '{}'
                REGION '{}'
                FORMAT AS JSON {};
            """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_conn_id="",
                 table_name = "",
                 s3_bucket = "",
                 region="",
                 data_format="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.table_name = table_name
        self.s3_bucket = s3_bucket
        self.region = region
        self.file_format = file_format
        self.execution_date = kwargs.get('execution_date')
        
    def execute(self, context):
        self.log.info('StageToRedshiftOperator prepared for execution')
        aws=AwsHook(self.aws_conn_id)
        credentials = aws.get_credentials()
        redshift_hook=PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Copy data from S3 to Redshift starting process....")
        copy_records = self.query.format(self.table_name, self.s3_bucket, credentials.access_key, credentials.secret_key, self.region, self.file_format)
        self.log.info("Query in place")
        redshift_hook.run(copy_records)
        self.log.info(f"Copying process of table {table_name} successful")
        





