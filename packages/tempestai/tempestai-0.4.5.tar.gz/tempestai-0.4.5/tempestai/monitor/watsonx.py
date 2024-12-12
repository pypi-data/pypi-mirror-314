import logging
import uuid
import json

from typing import List, Literal

def _filter_dict_by_keys(original_dict: dict, keys: List, required_keys: List = []):
    # Ensure all required keys are in the source dictionary
    missing_keys = [key for key in required_keys if key not in original_dict]
    if missing_keys:
        raise KeyError(f"Missing required parameter: {missing_keys}")
    
    # Create a new dictionary with only the key-value pairs where the key is in the list 'keys'
    return {key: original_dict[key] for key in keys if key in original_dict}


class WatsonxExternalPromptMonitoring:
    """**(Beta)** – Provides functionality to interact with IBM watsonx.governance for monitoring external LLM's.

    Args:
        api_key (str): IBM watsonx.governance API key.
        space_id (str, optional): watsonx.governance space_id, required to create prompt monitor.
        wml_url (str, optional): watsonx.ai Runtime url. Defaults to ``https://us-south.ml.cloud.ibm.com``

    **Example**

    .. code-block:: python

        from tempestai.monitor import WatsonDiscoveryRetriever

        watsonx_monitor = WatsonxExternalPromptMonitoring(api_key="*******",
                                                space_id="5d62977c-a53d-4b6d-bda1-7b79b3b9d1a0")
    """
    
    def __init__(self,
                 api_key: str,
                 space_id: str = None,
                 wml_url: str = "https://us-south.ml.cloud.ibm.com"
                 ) -> None:
        try:
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
            from ibm_aigov_facts_client import AIGovFactsClient
            from ibm_watson_openscale import APIClient as WosAPIClient
            from ibm_watsonx_ai import APIClient

        except ImportError:
            raise ImportError("""ibm-aigov-facts-client, ibm-watson-openscale or ibm-watsonx-ai not found, 
                                please install it with `pip install ibm-aigov-facts-client ibm-watson-openscale ibm-watsonx-ai`""")

        self._api_key = api_key
        self._space_id = space_id
        self._wml_url = wml_url
        self._wos_client = None

                    
    def _create_detached_prompt(self, detached_details: dict, 
                                prompt_template_details: dict, 
                                external_prompt: dict) -> str:
        from ibm_aigov_facts_client import DetachedPromptTemplate, PromptTemplate, AIGovFactsClient
            
        try:
             aigov_client = AIGovFactsClient(
                 api_key=self._api_key,
                 container_id=self._space_id,
                 container_type="space",
                 disable_tracing=True
                 )
                
        except Exception as e:
            logging.error(f"Error connecting to IBM watsonx.governance (factsheets): {e}")
            raise
            
        detached_information = DetachedPromptTemplate(**detached_details)
        prompt_template = PromptTemplate(**prompt_template_details)

        created_external_pta = aigov_client.assets.create_detached_prompt(
            **external_prompt,
            prompt_details=prompt_template,
            detached_information=detached_information)
            
        return created_external_pta.to_dict()["asset_id"]
            
            
    def _create_deployment_pta(self, asset_id: str,
                               name: str,
                               model_id: str) -> str:
        from ibm_watsonx_ai import APIClient
            
        try:
            wml_client = APIClient({
                "url": self._wml_url,
                "apikey": self._api_key 
                })
            wml_client.set.default_space(self._space_id)
                
        except Exception as e:
            logging.error(f"Error connecting to IBM watsonx.ai Runtime: {e}")
            raise
            
        meta_props = {
            wml_client.deployments.ConfigurationMetaNames.PROMPT_TEMPLATE: { "id" : asset_id },
            wml_client.deployments.ConfigurationMetaNames.DETACHED: {},
            wml_client.deployments.ConfigurationMetaNames.NAME: name + " " + "deployment",
            wml_client.deployments.ConfigurationMetaNames.BASE_MODEL_ID: model_id
        }
            
        created_deployment = wml_client.deployments.create(asset_id, meta_props)
            
        return wml_client.deployments.get_uid(created_deployment)
        
    @staticmethod
    def _parse_payload_data(records: List[dict], feature_fields: List[str]) -> List[dict]:
        
        payload_data = []
        response_fields = ["generated_text", "input_token_count", "generated_token_count"]
            
        for record in records: 
            request = { "parameters": { "template_variables": {}}}
            results = {}
                
            request["parameters"]["template_variables"] = {field: str(record.get(field, '')) for field in feature_fields}
            
            results = {field: record.get(field) for field in response_fields if record.get(field)}
                
            pl_record = {"request": request, "response": {"results": [results]}}
            payload_data.append(pl_record)
           
        return payload_data
        
            
    def create_prompt_monitor(self,
                              name: str,
                              model_id: str,
                              model_provider: str,
                              context_fields: List[str] = None,
                              question_field: str = None,
                              model_name: str = None,
                              model_version: str = None,
                              model_parameters: dict = None,
                              model_url: str = None,
                              prompt_variables: dict = None,
                              prompt_instruction: str = None,
                              input_prefix: str = None,
                              output_prefix: str = None,
                              input: str = None,
                              prompt_url: str = None,
                              prompt_additional_info: dict = None,
                              description: str = None,
                              task_id: Literal["retrieval_augmented_generation", "summarization"] = None) -> str:
        """**(Beta)** – Create a Detached/External Prompt Template Asset and setup monitors for a given prompt template asset.

        Args:
            name (str): The name of the external prompt.
            model_id (str): Id of the model associated with the prompt.
            model_provider (str): The provider of the model.
            context_fields (List[str], optional): A list of fields that will provide context to the prompt. Applicable only for ``retrieval_augmented_generation`` problem type.
            question_field (str, optional): The field containing the question to be answered. Applicable only for ``retrieval_augmented_generation`` problem type.
            model_name (str, optional): The name of the model.
            model_version (str, optional): The version of the model.
            model_parameters (dict, optional): Model parameters and their respective values.
            model_url (str, optional): URL of the model.
            input (str, optional): The input data for the prompt.
            input_prefix (str, optional): A prefix to add to the input.
            output_prefix (str, optional): A prefix to add to the output.
            prompt_variables (dict, optional): Values for prompt variables.
            prompt_instruction (str, optional): Instruction for using the prompt.
            prompt_url (str, optional): URL of the prompt.
            prompt_additional_info (dict, optional): Additional information related to the prompt.
            description (str, optional): Description of the external prompt to be created.
            task_id (Literal["retrieval_augmented_generation", "summarization"], optional): The task identifier.
            
        Returns:
            str: subscription_id.

        **Example**

        .. code-block:: python

            watsonx_monitor.create_prompt_monitor(name="External prompt (model AWS Anthropic)"
                                                    model_id="anthropic.claude-v2"
                                                    model_provider="AWS Bedrock"
                                                    context_fields=["context1", "context2"]
                                                    question_field="input_query"
                                                    model_name="Anthropic Claude 2.0"
                                                    model_url="https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html"
                                                    prompt_variables={"context1":"", "context2":"", "input_query":""}
                                                    input="Prompt text to be given")
            
        """
        prompt_metadata = locals()
        prompt_metadata.pop('context_fields', None)
        prompt_metadata.pop('question_field', None)
        
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        from ibm_watson_openscale import APIClient as WosAPIClient
        
        if not self._wos_client:    
            try:
                authenticator = IAMAuthenticator(apikey=self._api_key)
                self._wos_client = WosAPIClient(authenticator=authenticator)
                    
            except Exception as e:
                logging.error(f"Error connecting to IBM watsonx.governance (openscale): {e}")
                raise
            
        detached_details = _filter_dict_by_keys(prompt_metadata, 
                                                     ["model_id", "model_provider", "model_name", 
                                                      "model_url", "prompt_url", "prompt_additional_info"],
                                                     ["model_id", "model_provider"])
        detached_details['prompt_id'] = "detached_prompt" + str(uuid.uuid4())
        
        prompt_details = _filter_dict_by_keys(prompt_metadata, 
                                                   ["model_version", "prompt_variables", "prompt_instruction",
                                                    "input_prefix", "output_prefix", "input", "model_parameters"])
        
        external_prompt = _filter_dict_by_keys(prompt_metadata, 
                                                    ["name", "model_id", "task_id", "description"],
                                                    ["name", "model_id", "task_id"])
            
        external_pta_id = self._create_detached_prompt(detached_details, prompt_details, external_prompt)
        deployment_id =  self._create_deployment_pta(external_pta_id, name, model_id)
            
        monitors = {
            "generative_ai_quality": {
                "parameters": {
                    "min_sample_size": 10,
                    "metrics_configuration":{}
                    }
                }}
            
        generative_ai_monitor_details = self._wos_client.wos.execute_prompt_setup(prompt_template_asset_id = external_pta_id, 
                                                                                  space_id = self._space_id,
                                                                                  deployment_id = deployment_id,
                                                                                  label_column = "reference_output",
                                                                                  context_fields=context_fields,     
                                                                                  question_field = question_field,   
                                                                                  operational_space_id = "production", 
                                                                                  problem_type = task_id,
                                                                                  input_data_type = "unstructured_text", 
                                                                                  supporting_monitors = monitors, 
                                                                                  background_mode = False).result

        generative_ai_monitor_details = generative_ai_monitor_details._to_dict()
            
        return generative_ai_monitor_details["subscription_id"]
        
                    
    def payload_logging(self, payload_records: List[dict], subscription_id: str) -> None:
        """**(Beta)** – Store records to payload logging.

        Args:
            payload_records (List[dict]): 
            subscription_id (str): 

        **Example**

        .. code-block:: python

            watsonx_monitor.payload_logging(data=[{"context1": "value_context1",
                                                    "context2": "value_context1",
                                                    "input_query": "what's tempestai?",
                                                    "input_token_count": 25,
                                                    "generated_token_count": 150}], 
                                            subscription_id="5d62977c-a53d-4b6d-bda1-7b79b3b9d1a0")
        """
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        from ibm_watson_openscale import APIClient as WosAPIClient
        from ibm_watson_openscale.supporting_classes.enums import DataSetTypes, TargetTypes
        if not self._wos_client:
            try:
                authenticator = IAMAuthenticator(apikey=self._api_key)
                self._wos_client = WosAPIClient(authenticator=authenticator)
                
            except Exception as e:
                logging.error(f"Error connecting to IBM watsonx.governance (openscale): {e}")
                raise
        
        subscription_details = self._wos_client.subscriptions.get(subscription_id).result
        subscription_details = json.loads(str(subscription_details))
            
        feature_fields = subscription_details['entity']['asset_properties']['feature_fields']
            
        payload_data_set_id = self._wos_client.data_sets.list(type=DataSetTypes.PAYLOAD_LOGGING,
                                                              target_target_id=subscription_id, 
                                                              target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id
            
        payload_data = self._parse_payload_data(payload_records, feature_fields)
        self._wos_client.data_sets.store_records(data_set_id=payload_data_set_id, 
                                                 request_body=payload_data,
                                                 background_mode=False)
            
        return        
                