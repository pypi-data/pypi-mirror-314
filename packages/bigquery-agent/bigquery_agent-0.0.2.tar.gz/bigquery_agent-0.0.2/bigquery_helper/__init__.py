
from .bigquery_helper import BigQueryHelper
from gemini_agents_toolkit import agent

def create_bigquery_agent(
    bigquery_project_id: str,
    dataset_id: str,
    table_id: str,
    model_name: str,
    debug: bool = False,
    add_scheduling_functions: bool = False,
    gcs_bucket: str = None,
    gcs_blob: str = None,
    delegation_function_prompt: str = None,
    delegates: list = None,
    on_message = None,
    generation_config: dict = None,
    system_instruction: str = ""
):
    """
    Creates and returns an agent initialized with functions from BigQueryHelper 
    that can interact with a specific BigQuery table.

    :param bigquery_project_id: GCP project ID for BigQuery.
    :param dataset_id: BigQuery dataset ID.
    :param table_id: BigQuery table ID.
    :param model_name: The Vertex AI model name to be used by the agent.
    :param debug: Optional debug mode for the agent.
    :param add_scheduling_functions: Whether to add scheduling functions to the agent.
    :param gcs_bucket: GCS bucket name for agent storage (if any).
    :param gcs_blob: GCS blob name for agent storage (if any).
    :param delegation_function_prompt: Prompt for delegation functions.
    :param delegates: List of delegate configurations.
    :param on_message: A callback that fires on each message from the agent.
    :param generation_config: Additional generation configuration parameters.
    :param system_instruction: Instruction message.
    :return: An agent instance configured to query the specified BigQuery table.
    """



    # Initialize the BigQuery helper with the bigquery_project_id
    helper = BigQueryHelper(
        project_id=bigquery_project_id,
        dataset_id=dataset_id,
        table_id=table_id
    )

    # Define the agent with helper's functions
    all_functions = [helper.get_schema, helper.run_query, helper.get_table_ref]

    # Prepend prompt to the system_instruction
    updated_system_instruction = f"""You have access to a BigQuery database table in a GCP project. Before doing any query, check the DB schema
      (you have a function for it) and check the table/db name by calling the ref function to make sure that you will constract correct query. {system_instruction}""".strip()

    # Create and return the agent instance
    todo_agent = agent.create_agent_from_functions_list(
        functions=all_functions,
        model_name=model_name,
        debug=debug,
        add_scheduling_functions=add_scheduling_functions,
        gcs_bucket=gcs_bucket,
        gcs_blob=gcs_blob,
        delegation_function_prompt=delegation_function_prompt,
        delegates=delegates,
        on_message=on_message,
        generation_config=generation_config,
        system_instruction=updated_system_instruction
    )

    return todo_agent
