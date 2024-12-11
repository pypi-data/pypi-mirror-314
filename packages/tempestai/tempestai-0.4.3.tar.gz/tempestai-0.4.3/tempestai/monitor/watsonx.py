import logging
import uuid
import json

from typing import List

def _filter_dict_by_keys(original_dict: dict, keys: List, required_keys: List = []):
    # Ensure all required keys are in the source dictionary
    missing_keys = [key for key in required_keys if key not in original_dict]
    if missing_keys:
        raise KeyError(f"Missing required parameter: {missing_keys}")
    
    # Create a new dictionary with only the key-value pairs where the key is in the list 'keys'
    return {key: original_dict[key] for key in keys if key in original_dict}


class WatsonxExternalPromptMonitoring:
    """Provides functionality to interact with IBM watsonx.governance for monitoring external LLM's.

    Args:
        api_key (str): IBM watsonx.governance API key.
        space_id (str, optional): watsonx.governance space_id, required to create prompt monitor.
        wml_url (str, optional): watsonx.ai Runtime url. Defaults to ``https://us-south.ml.cloud.ibm.com``
        subscription_id (str, optional): watsonx.governance subscription_id, required for payload logging.

    **Example**

    .. code-block:: python

        from tempestai.monitor import WatsonDiscoveryRetriever

        watsonx_monitor = WatsonxExternalPromptMonitoring(api_key="your_api_key",
                                                space_id="your_space_id")
    """
    
    def __init__(self,
                 api_key: str,
                 space_id: str = None,
                 wml_url: str = "https://us-south.ml.cloud.ibm.com",
                 subscription_id: str = None
                 ) -> None:
            try:
                from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
                from ibm_aigov_facts_client import AIGovFactsClient
                from ibm_watson_openscale import APIClient as WosAPIClient
                from ibm_watsonx_ai import APIClient

            except ImportError:
                raise ImportError("""ibm-aigov-facts-client, ibm-watson-openscale or ibm-watsonx-ai not found, 
                                  please install it with `pip install ibm-aigov-facts-client ibm-watson-openscale ibm-watsonx-ai`""")

            self.subscription_id = subscription_id
            self._api_key = api_key
            self._space_id = space_id
            self._wml_url = wml_url
            self._wos_client = None

                    
    def _create_detached_prompt(self) -> str:
            from ibm_aigov_facts_client import DetachedPromptTemplate, PromptTemplate, AIGovFactsClient
            
            try:
                _aigov_client = AIGovFactsClient(
                    api_key=self._api_key,
                    container_id=self._space_id,
                    container_type="space",
                    disable_tracing=True
                    )
                
            except Exception as e:
                logging.error(f"Error connecting to IBM factsheets: {e}")
                raise
            
            detached_information = DetachedPromptTemplate(**self.detached_details)
            prompt_template = PromptTemplate(**self.prompt_details)

            created_pta = _aigov_client.assets.create_detached_prompt(
               **self.external_prompt,
                prompt_details=prompt_template,
                detached_information=detached_information)
            
            return created_pta.to_dict()["asset_id"]
            
            
    def _create_deployment_pta(self, asset_id: str) -> str:
            from ibm_watsonx_ai import APIClient
            
            try:
                _wml_client = APIClient({
                        "url": self._wml_url,
                        "apikey": self._api_key 
                        })
                _wml_client.set.default_space(self._space_id)
                
            except Exception as e:
                logging.error(f"Error connecting to IBM watsonx.ai: {e}")
                raise
            
            meta_props = {
                _wml_client.deployments.ConfigurationMetaNames.PROMPT_TEMPLATE: { "id" : asset_id },
                _wml_client.deployments.ConfigurationMetaNames.DETACHED: {},
                _wml_client.deployments.ConfigurationMetaNames.BASE_MODEL_ID: self.detached_details['model_id'],
                _wml_client.deployments.ConfigurationMetaNames.NAME: self.external_prompt['name'] + " " + "deployment"
            }
            
            created_deployment = _wml_client.deployments.create(asset_id, meta_props)
            
            return _wml_client.deployments.get_uid(created_deployment)
        
        
    def _parse_payload_data(self, data: List, feature_fields: List) -> List[dict]:
            payload_data = []
            generated_text_list = []
            
            for row in data: 
                request = { "parameters": { "template_variables": {}}}
                
                if feature_fields:
                    for field in feature_fields:
                        field_value = str(row.get(field, ''))
                        
                        request["parameters"]["template_variables"][field] = field_value
                
                generated_text = row.get("generated_text", '')
                generated_text_list.append(generated_text)
                
                response = {"results": [{ "generated_text" : generated_text}]}
                
                record = {"request": request, "response": response}
                payload_data.append(record)
        
            return payload_data
        
            
    def create_prompt_monitor(self, prompt_metadata: dict, 
                                  context_fields: List,
                                  question_field: str) -> str:
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
            from ibm_watson_openscale import APIClient as WosAPIClient
            
            try:
                authenticator = IAMAuthenticator(apikey=self._api_key)
                self._wos_client = WosAPIClient(authenticator=authenticator)
                
            except Exception as e:
                logging.error(f"Error connecting to IBM watsonx.governance (openscale): {e}")
                raise
                
            self.prompt_details = _filter_dict_by_keys(prompt_metadata, 
                                                       ["model_version", "prompt_variables", "prompt_instruction",
                                                        "input_prefix", "output_prefix", "input", "model_parameters"])
            self.detached_details = _filter_dict_by_keys(prompt_metadata, 
                                                       ["model_id", "model_provider", "model_name", 
                                                        "model_url", "prompt_url", "prompt_additional_info"],
                                                       ["model_id", "model_provider"])
            self.detached_details['prompt_id'] = "detached_prompt" + str(uuid.uuid4())
            self.external_prompt = _filter_dict_by_keys(prompt_metadata, 
                                                       ["name", "model_id", "task_id", "description", "container_id"],
                                                       ["name", "model_id", "task_id"])
            
            pta_id = self._create_detached_prompt()
            deployment_id =  self._create_deployment_pta(asset_id=pta_id)
            
            monitors = {
                "generative_ai_quality": {
                "parameters": {
                    "min_sample_size": 10,
                    "metrics_configuration":{}
                    }
                }}
            
            generative_ai_monitor_details = self._wos_client.wos.execute_prompt_setup(prompt_template_asset_id = pta_id, 
                                                                   space_id = self._space_id,
                                                                   deployment_id = deployment_id,
                                                                   label_column = "reference_output",
                                                                   context_fields=context_fields,     
                                                                   question_field = question_field,   
                                                                   operational_space_id = "production", 
                                                                   problem_type = self.external_prompt['task_id'],
                                                                   input_data_type = "unstructured_text", 
                                                                   supporting_monitors = monitors, 
                                                                   background_mode = False).result

            generative_ai_monitor_details = generative_ai_monitor_details._to_dict()
            self.subscription_id = generative_ai_monitor_details["subscription_id"]
            
            return self.subscription_id
        
                    
    def payload_logging(self, data: List, subscription_id: str = None) -> None:
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
            
            self.subscription_id = subscription_id
            
            if not self.subscription_id:
                raise ValueError(f"No `subscription_id` provided or exist.")
            
            subscription_details = self._wos_client.subscriptions.get(self.subscription_id).result
            subscription_details = json.loads(str(subscription_details))
            
            feature_fields = subscription_details['entity']['asset_properties']['feature_fields']
            
            payload_data_set_id = self._wos_client.data_sets.list(type=DataSetTypes.PAYLOAD_LOGGING, 
                                                target_target_id=self.subscription_id, 
                                                target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id
            
            payload_data = self._parse_payload_data(data, feature_fields)
            self._wos_client.data_sets.store_records(data_set_id=payload_data_set_id, 
                                                     request_body=payload_data,
                                                     background_mode=False)
            
            return
            
                