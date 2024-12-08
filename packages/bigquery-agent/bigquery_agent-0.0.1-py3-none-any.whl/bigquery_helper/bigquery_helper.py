from google.cloud import bigquery


class BigQueryHelper:

    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        """
        Initialize the BigQueryHelper with the provided project, dataset, and table IDs.
        This constructor also initializes the BigQuery client and table reference.

        :param project_id: GCP project ID
        :param dataset_id: BigQuery dataset ID
        :param table_id:   BigQuery table ID
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id

        # Initialize the BigQuery client
        self.client = bigquery.Client(project=self.project_id)

        # Fully-qualified table ID in standard SQL format
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    def get_schema(self) -> str:
        """
        Retrieves the schema of the configured BigQuery table.

        :return: A list of SchemaField objects describing the table schema.
        """
        table = self.client.get_table(self.table_ref)
        return table.schema

    def run_query(self, sql_query: str) -> str:
        """
        Executes a provided SQL query on the configured BigQuery project and dataset,
        and returns the results as a string.

        :param sql_query: The SQL query to execute.
        :return: A newline-separated string representation of the query results.
        """
        query_job = self.client.query(sql_query)
        results = query_job.result()

        result_str_list = []
        for row in results:
            # Convert the row to a dictionary for readability
            row_dict = dict(row)
            result_str_list.append(str(row_dict))

        return "\n".join(result_str_list)


    def get_table_ref(self) -> str:
        """
        Returns the fully-qualified table reference string.

        :return: The table reference in the format project_id.dataset_id.table_id
        """
        return self.table_ref