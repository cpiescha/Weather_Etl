from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json

class PostgresFileOperator(BaseOperator):
    @apply_defaults
    def __init__(self,
                 operation,
                 config={},
                 *args,
                 **kwargs):
        super(PostgresFileOperator, self).__init__(*args,**kwargs)
        self.operation=operation
        self.config=config
        self.postgres_hook=PostgresHook(postgres_conn_id='postgres_default')
        
    def execute(self,context):
        if self.operation=="write":
            pass
        elif self.operation=="read":
            pass
        
    def writeinDb(self):
        self.postgres_hook.bulk_load(self.config.get('table_name'), 'C:/Users/USUARIO/Desktop/weather_etl/plugins/tmp/weather_data.tsv')
            
        
