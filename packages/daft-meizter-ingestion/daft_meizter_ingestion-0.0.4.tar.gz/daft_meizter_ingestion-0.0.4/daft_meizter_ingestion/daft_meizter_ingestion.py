from dotenv import load_dotenv
import requests
import os
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField,
    StringType
)
import pyarrow.fs as fs
import pyarrow as pa
import pyarrow.parquet as pq
import daft
from daft.datatype import DataType
from daft.io import IOConfig, S3Config
import pandas as pd
from datetime import datetime, timedelta
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import IdentityTransform
from daft.expressions import lit
import boto3
from urllib.parse import urlparse
from pyiceberg.catalog import Catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, IntegerType, FloatType, BooleanType
from daft.datatype import DataType

# Classe de segredos
class secret:
    @staticmethod
    def get_secrets(keys):
        load_dotenv()
        service_token = os.getenv('AWS')
        url = "https://api.doppler.com/v3/configs/config/secrets/download?format=json"

        headers = {
            "Authorization": f"Bearer {service_token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            secrets = response.json()

            selected_secrets = {key: secrets.get(key) for key in keys if key in secrets}
            return selected_secrets
        else:
            print(f"Erro ao buscar segredos: {response.status_code}, {response.text}")
            return None


class daft_mzr_ingestion:

    def __init__(self):
        secrets = secret.get_secrets(["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "REGION", "ENDPOINT", "BUCKET", "URI", "TOKEN_CATALOG"])
        if secrets:
            self.AWS_ACCESS_KEY_ID = secrets.get("AWS_ACCESS_KEY_ID")
            self.AWS_SECRET_ACCESS_KEY = secrets.get("AWS_SECRET_ACCESS_KEY")
            self.ENDPOINT = secrets.get("ENDPOINT")
            self.REGION = secrets.get("REGION")
            self.BUCKET = secrets.get("BUCKET")
            self.URI = secrets.get("URI")
            self.TOKEN_CATALOG = secrets.get("TOKEN_CATALOG")
            
            # Inicializando o catálogo dentro do __init__
            self.catalog_name = "rest_catalog"
            self.catalog_properties = {
                "type": "rest",
                "uri": self.URI,  
                "token": self.TOKEN_CATALOG,
                "s3.endpoint": self.ENDPOINT,
                "s3.access-key-id": self.AWS_ACCESS_KEY_ID,
                "s3.secret-access-key": self.AWS_SECRET_ACCESS_KEY,
                "s3.region": self.REGION
            }
            self.catalog = load_catalog(self.catalog_name, **self.catalog_properties)

    def listar_tabelas(self, namespace_filter=None):

        data = []
    
        # Listar namespaces e tabelas
        namespaces = self.catalog.list_namespaces()
        for namespace in namespaces:
            tables = self.catalog.list_tables(namespace)
            for table in tables:
                if isinstance(table, tuple):
                    namespace_name, table_name = table  #
                else:
                    namespace_name = namespace  
                    table_name = table          #
                data.append({"Namespace": namespace_name, "Tabela": table_name})
    

        df = pd.DataFrame(data)
    
        if namespace_filter:
            df = df[df["Namespace"] == namespace_filter]
    
        display(df)


    def conn_s3(self):
        s3 = fs.S3FileSystem(
        access_key=self.AWS_ACCESS_KEY_ID,
        secret_key=self.AWS_SECRET_ACCESS_KEY,
        region=self.REGION
        )
        return s3

    def to_transient(self, df, source, sub_source, table, engine='daft'):
        s3 = self.conn_s3()

        catalogo = f'transient/{source}/{sub_source}{table}.parquet'
        bucket = self.BUCKET
        caminho_s3 = f"{bucket}/{catalogo}"

        if not catalogo.strip():
            print('Caminho incorreto, verificar informações')
            return

        try:
            if engine == 'daft':
                try:
                
                    arrow_table = df.to_arrow()
                except AttributeError:
                    
                    pandas_df = df.to_pandas()
                    arrow_table = pa.Table.from_pandas(pandas_df)
                
                pq.write_table(arrow_table, caminho_s3, filesystem=s3)
                print(f'Dados escritos com sucesso em: {caminho_s3}')
            
            elif engine == 'pandas':
                arrow_table = pa.Table.from_pandas(df)
                pq.write_table(arrow_table, caminho_s3, filesystem=s3)
                print(f'Dados escritos com sucesso em: {caminho_s3}')
            
            else:
                print(f"Engine '{engine}' não é suportado.")
        
        except Exception as e:
            print(f'Erro ao escrever no S3: {e}')      

    def to_bronze(self, parquet_file_path, catalog, table, type, delete_files=False):
        # Configuração do S3
        s3_config = S3Config(
            key_id=self.AWS_ACCESS_KEY_ID,
            access_key=self.AWS_SECRET_ACCESS_KEY
        )
        io_config = IOConfig(s3=s3_config)

        # Leitura inicial para inferir as colunas
        sample_df = daft.read_parquet(
            [parquet_file_path],
            io_config=io_config
        )
        colunas = sample_df.column_names
        colunas.append("dt_ingestion")
        print("Colunas detectadas:", colunas)
        # Criar o esquema manualmente, todas as colunas como StringType
        fields = [
            NestedField(field_id=i, name=col, field_type=StringType(), required=False)
            for i, col in enumerate(colunas, start=1)
        ]

        # Criar o esquema PyIceberg
        schema = Schema(*fields)

        df = daft.read_parquet(
            [parquet_file_path],
            schema={col: DataType.string() for col in colunas},
            infer_schema=False,
            io_config=io_config
        )
        # Adicionar a coluna 'dt_ingestion' com a data atual
        hoje = datetime.now()
        hoje = hoje.strftime("%d-%m-%Y")
        df = df.with_column("dt_ingestion", lit(hoje))

        table_identifier = f"{catalog}.{table}"
        try:
            # Criar a tabela no catálogo
            self.catalog.create_table_if_not_exists(
                identifier=table_identifier,
                schema=schema,
                location=f"s3://{self.BUCKET}/bronze/{catalog}/{table}"
            )
            print("Tabela criada com sucesso!")

            # Carrega a tabela Iceberg
            iceberg_table = self.catalog.load_table(table_identifier)
            if iceberg_table:
                df.write_iceberg(
                    table=iceberg_table,
                    mode=type  # 'overwrite' ou 'append', dependendo do uso
                )
                print("Dados escritos com sucesso!")
        except Exception as e:
            print(f'{e}')
        if delete_files:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY
            )

            from urllib.parse import urlparse
            parsed_url = urlparse(parquet_file)
            bucket_name = parsed_url.netloc
            prefix = parsed_url.path.lstrip('/')

            bucket = s3.Bucket(bucket_name)

            try:
                for obj in bucket.objects.filter(Prefix=prefix):
                    obj.delete()
                print(f"Todos os arquivos em '{parquet_file}' foram removidos.")
            except Exception as e:
                print(f"Erro ao remover os arquivos do S3: {e}")

    def drop_table(self, catalog, table):
        # Construi o caminho S3 com base no padrão
        s3_path = f"s3://{self.BUCKET}/bronze/{catalog}/{table}/"

        # Exclui a tabela do catálogo
        try:
            self.catalog.drop_table(f"{catalog}.{table}")
            print(f"Tabela '{catalog}.{table}' removida do catálogo.")
        except Exception as e:
            print(f"Erro ao remover a tabela do catálogo: {e}")
            return

        # Conecta ao S3 usando as credenciais da classe
        s3 = boto3.resource(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY
        )
        bucket_name, prefix = s3_path.replace("s3://", "").split("/", 1)
        bucket = s3.Bucket(bucket_name)

        try:
            # Deleta todos os objetos no prefixo
            bucket.objects.filter(Prefix=prefix).delete()
            print(f"Todos os arquivos em '{s3_path}' foram removidos.")
        except Exception as e:
            print(f"Erro ao remover os arquivos do S3: {e}")
        
    
    def read_lakehouse(self, catalog, table):
        # Nome da tabela
        table_identifier = f"{catalog}.{table}"
        iceberg_table = self.catalog.load_table(table_identifier)
        df = daft.read_iceberg(iceberg_table)
         # Exibi os dados carregados
        return df
    
    def daft_schema_to_iceberg(self, daft_schema):
        from pyiceberg.schema import Schema
        from pyiceberg.types import (
            NestedField, StringType, IntegerType, FloatType,
            BooleanType, DoubleType, TimestampType, DateType,
            DecimalType, BinaryType
        )
        from daft.datatype import DataType
    
        daft_to_iceberg_type = {
            DataType.string(): StringType(),
            DataType.bool(): BooleanType(),
            DataType.int8(): IntegerType(),
            DataType.int16(): IntegerType(),
            DataType.int32(): IntegerType(),
            DataType.int64(): IntegerType(),
            DataType.float32(): FloatType(),
            DataType.float64(): DoubleType(),
            DataType.date(): DateType(),
            # Timestamp tratado dinamicamente abaixo
        }
    
        iceberg_fields = []
        for idx, field in enumerate(daft_schema, start=1):
            field_name = field.name
            daft_type = field.dtype
    
            if hasattr(daft_type, 'is_timestamp') and daft_type.is_timestamp():
                iceberg_type = TimestampType()
            else:
                iceberg_type = daft_to_iceberg_type.get(daft_type)
            
            if iceberg_type is None:
                raise ValueError(f"Tipo Daft não suportado: {daft_type}")
    
            # Tente usar 'dtype.nullable' se existir
            # Caso não exista, consulte a documentação do Daft para encontrar o atributo correto.
            if hasattr(daft_type, 'nullable'):
                required = not daft_type.nullable
            else:
                # Se não houver informação de nulabilidade, defina um padrão. Por exemplo, tudo como não-obrigatório:
                required = False
    
            iceberg_fields.append(
                NestedField(field_id=idx, name=field_name, field_type=iceberg_type, required=required)
            )
    
        return Schema(*iceberg_fields)

    
    def write_lakehouse(self, df, catalog, table, layer, mode="append"):
        daft_schema = df.schema()
        iceberg_schema = self.daft_schema_to_iceberg(daft_schema)
        table_identifier = f"{catalog}.{table}"
    
        try:
            self.catalog.create_table_if_not_exists(
                identifier=table_identifier,
                schema=iceberg_schema,
                location=f"s3://{self.BUCKET}/{layer}/{catalog}/{table}"
            )
            print("Tabela criada com sucesso!")
    
            iceberg_table = self.catalog.load_table(table_identifier)
            if iceberg_table:
                df.write_iceberg(table=iceberg_table, mode=mode)
                print("Dados escritos com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar no lakehouse: {e}")