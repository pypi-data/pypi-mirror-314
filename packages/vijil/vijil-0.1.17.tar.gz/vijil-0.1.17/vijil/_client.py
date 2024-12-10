import os
import uuid
import pandas as pd
import json
import numpy as np
from typing import List, Optional, Any
from dataclasses import field
from datetime import datetime, timezone
import jinja2
from fpdf import FPDF

from vijil.api import make_api_request, get_api_proxy_dict, BASE_URL, SUPPORTED_HUBS
from vijil.types import VijilClient

ERROR_SKIP_KEYS = ['ERROR', 'SKIP']
HUB_CONFIG_FIELDS = {
    "vertex": ["region", "project_id", "client_id", "client_secret", "refresh_token"],
    "digitalocean": ["agent_id","agent_key"]
}
HUBS_NEEDING_URL = ["custom", "bedrock_custom", "azure", "digitalocean"]
HUBS_NOT_NEEDING_MODEL_NAME = ["digitalocean"]

def modify_hub(model_hub: str):
    
    if model_hub == "bedrock":
        return "bedrock_custom"
    return model_hub

class APIKeys:
    """
    Class for managing model hub API keys, which are required to query models.

    :param client: The Vijil client instance.
    :type client: VijilClient
    """
    
    def __init__(self, client: VijilClient) -> None:
        """Constructor class

        :param client: The Vijil client instance.
        :type client: VijilClient
        """
        self.endpoint = "api-keys"
        self.client = client
        pass
    
    def list(self):
        """List all stored model hub API keys.

        :return: List of dictionaries. Each dictionary contains information about an API key.
        :rtype: List(dict)
        """
        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint, token=self.client.api_key)
        return response
    
    def get_id_by_name(self, name: str):
        """ Get the id of a key by its name. Used by other functions to get the id of a key to modify.

        :param name: The name of the key.
        :type name: str
        :return: The id of the key.
        :rtype: str
        """

        if not self.name_exists(name):
            raise ValueError(f"Key '{name}' does not exist. Please specify an existing name.")

        #get id of key to modify
        response = self.list()
        return [item['id'] for item in response if item['name'] == name][0]
    
    def check_model_hub(self, model_hub: str):
        """Used by other functions to check that the model hub is valid and the key name is unique

        :param model_hub: The name of the model hub.
        :type model_hub: str
        :raises ValueError: If the model hub is not supported.
        """
        
        model_hub = modify_hub(model_hub)

        # check if model_hub is valid
        if (model_hub is not None) and (model_hub not in SUPPORTED_HUBS.keys()):
            raise ValueError(f"Model hub {model_hub} is not supported.")
    
    def name_exists(self, name: str):
        """Check whether the API key name already exists. Some functions need it to be exist, others need it to not exist.
        
        :param name: The name of the key.
        :type name: str
        :return: True if the name exists among the stored API keys, False otherwise.
        :rtype: bool
        """
        
        response = self.list()
        if response is not None and name in [item['name'] for item in response]:
            return True
        else:
            return False

    def create(self, name: str, model_hub: str, rate_limit_per_interval: int=60, rate_limit_interval: int=10, api_key: Optional[str]=None, hub_config: Optional[dict[Any, Any]]=None):
        """Create a new model hub API key.

        :param name: Name for the API key. This must be unique.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        :raises ValueError: If you try to create a key with a name that belongs to an existing key.
        :return: Response to the API request.
        :rtype: dict
        :param api_key: The API key.
        :type api_key: str, optional
        :param hub_config: A dictionary containing additional configuration for the model hub. Defaults to None.
        :type hub_config: dict, optional
        """
        # conditional checks for fields
        model_hub = modify_hub(model_hub)
        
        # hub name     
        self.check_model_hub(model_hub=model_hub)

        # api key name
        if self.name_exists(name):
            raise ValueError(f"Key name '{name}' already exists. Please specify a different name.")
        
        # hub config and api key for vertex
        if model_hub in HUB_CONFIG_FIELDS.keys():
            api_key = ""
            if hub_config is None or not all([field in hub_config for field in HUB_CONFIG_FIELDS[model_hub]]):
                raise ValueError(f"Please provide the following fields in the hub_config for {SUPPORTED_HUBS[model_hub]}: {HUB_CONFIG_FIELDS[model_hub]}")
        else:
            if hub_config is not None:
                raise ValueError(f"Hub config is only needed for {SUPPORTED_HUBS[model_hub]}. Please remove it for other model hubs.")
            if api_key is None:
                raise ValueError("Please provide an API key.")

        # construct the payload
        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
        }
        if hub_config:
            payload["hub_config"] = hub_config
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
    
    def rename(self, name: str, new_name: str):
        """Rename a stored API key
        
        :param name: The current name of the key.
        :type name: str
        :param new_name: The new name of the key.
        :type new_name: str
        """

        key_id = self.get_id_by_name(name=name)
        
        payload = {
            "name": new_name
        }

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key
        )

    
    def modify(self, name: str, model_hub: str, api_key:Optional[str] = None, rate_limit_per_interval=None, rate_limit_interval=None):
        """Modify model hub, key, or rate limits of a stored API key. Cannot be used to rename key.
        
        :param name: The name of the key you want to modify.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str, optional
        :param api_key: The API key.
        :type api_key: str, optional
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        """

        #check that model hub is supported and key name refers to existing name
        self.check_model_hub(model_hub=model_hub)        
        
        key_id = self.get_id_by_name(name=name)

        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
        }

        #remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key
        )

    def delete(self, name: str):
        """Delete API key with specified name
        
        :param name: The name of the key you want to delete
        :type name: str
        :return: Response to the API request.
        :rtype: dict
        """

        key_id = self.get_id_by_name(name=name)

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="delete",
            token=self.client.api_key
        )


class Harnesses:
    """Class for handling harnesses API requests.
    
    :param client: The VijilClient instance.
    :type client: VijilClient
    """
    
    def __init__(self, client: VijilClient) -> None:
        """Initialize the Harnesses class.

        :param VijilClient client: The VijilClient instance.
        :type client: VijilClient
        """
        self.endpoint = "harness-configs"
        self.client = client
        pass

    def list(self):
        """List all harnesses.

        :return: List of dicts where each dict contains the metadata for a harness.
        :rtype: List(dict)
        """
        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint, token=self.client.api_key)
        return response["results"]
    
    def create(self, harness_name: str, component_list: List[str], component_type: str = "probe"):
        """Not implemented yet.
        """
        raise NotImplementedError("Create harnesses is not implemented yet.")

        if component_type not in ["probe", "scenario"]:
            raise ValueError("component_type must be either 'probe' or 'scenario'")
        payload = {
            "id": str(uuid.uuid4()),
            "harness_name": harness_name,
            "component_list": component_list,
            "component_type": component_type
        }
        
        #if request is succeessful, return the harness id, name, and a "submitted" message
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
    def delete(self, harness_id: str):
        """
        Not implemented yet.
        """
        raise NotImplementedError("Delete harnesses is not implemented yet.")
        
        #if request is succeessful, return the harness id, name, and a "submitted" message
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=f"harness-configs/{harness_id}",
            method="delete",
            token=self.client.api_key
        )


    
class Evaluations:
    """Class for handling evaluations API requests.
    
    :param client: The VijilClient instance.
    :type client: VijilClient
    """
    
    def __init__(
        self,
        client: VijilClient
    ) -> None:
        self.endpoint = "evaluations"
        self.client = client
        self.api_proxy_dict: dict = field(default_factory=dict)
    
    def list(self, limit=10):
        """List all valuations. Will return only 10 evaluations unless specified.
        
        :param limit: The number of evaluations to return, defaults to 10.
        :type limit: int, optional
        """

        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint+"?limit="+str(limit), token=self.client.api_key)
        return response['results']
    
    def create(self, model_hub: str, model_name: Optional[str]=None, name: Optional[str]=None, api_key_name: Optional[str]=None, model_url: Optional[str]=None, model_params={}, harness_params={}, harnesses=[]):
        """Create a new evaluation.

        :param model_hub: The model hub you want to use. Supported options are "openai", "together", "digitalocean", "custom".
        :type model_hub: str
        :param model_name: The name of the model you want to use. Check the model hub's API documentation to find valid names.
        :type model_name: str, optional
        :param name: The name of the evaluation. If not specified, model hub will be concatenated with model name.
        :type name: str, optional
        :param api_key_name: The name of the model hub API key you want to use. If not specified, will use the first key we find for the specified model_hub.
        :type api_key_name: str, optional
        :param model_url: The URL of the model you want to use. Only required for custom model hub. Defaults to None
        :type model_url: str, optional
        :param model_params: A dictionary specifying inference parameters like temperature and top_p. If none are specified, model hub defaults will be used. Defaults to {}
        :type model_params: dict, optional
        :param harness_params: Set optional parameters like is_lite, defaults to {}
        :type harness_params: dict, optional
        :param harnesses: A list of harnesses you want to include in the evaluation, defaults to []
        :type harnesses: List[str], optional
        :raises TypeError: If you have no API keys stored.
        :raises ValueError: If you have no API keys stored for the specified model hub.
        :raises ValueError: If you supply an api_key_name that does not exist.
        :raises ValueError: If you specify lite mode for any harness other than ethics.
        :return: API response containing evaluation ID of the newly created evaluation.
        :rtype: dict
        """

        model_hub = modify_hub(model_hub)

        # store all api keys in a dictionary if not there
        if self.api_proxy_dict.__class__.__name__=="Field":
            try:
                self.api_proxy_dict = get_api_proxy_dict(base_url=self.client.base_url, token=self.client.api_key)
            except TypeError:
                raise TypeError("No API keys found. Please upload an API key first.")
            
        # get api key proxy for the model hub
        try:
            hub_api_proxy_dict = self.api_proxy_dict[model_hub]
        except KeyError: 
            raise ValueError(f"No API key stored for model hub {model_hub}")
        
        # get api key proxy for the model hub
        if api_key_name is not None:
            #find api key id for the api key name
            if api_key_name not in hub_api_proxy_dict.keys():
                raise ValueError(f"No API key found for name {api_key_name}")
            else:
                api_key_proxy = hub_api_proxy_dict[api_key_name]
        else: #if no key specified, use first value in hub dictionary
            api_key_proxy = next(iter(hub_api_proxy_dict.values()))

        # create the payload
        payload = {
            "name": name if name else f"{SUPPORTED_HUBS[model_hub]}-{model_name}",
            "id": str(uuid.uuid4()),
            "hub": model_hub,
            "api_key_proxy": api_key_proxy,
            "scenario_config_filters": [],
            "agent_params": {"temperature": 0, "top_p": 1, "max_tokens": 125},
            "is_lite": False,
            "tags": [""],
            "version": "1.0.16"
        }
        if model_hub in HUBS_NOT_NEEDING_MODEL_NAME:
            payload["model"] = "n/a"
        else:
            try:
                payload["model"] = model_name
            except KeyError:
                raise ValueError(f"No model name specified for {model_hub}. Please specify a model name.")
            
        if model_hub in HUBS_NEEDING_URL:
            if model_url is None:
                raise ValueError("For this model hub, you must specify a model URL.")
            if model_hub=="custom" and api_key_name is None:
                raise ValueError("For custom model hubs, you must specify an API key name. Use `api_keys.list()` to see available keys.")
            payload["url"] = model_url
        
        if model_params:
            for key, value in model_params.items():
                payload["agent_params"][key] = value
            if model_params.get("num_generations"):
                payload["num_generations"] = model_params["num_generations"]
        for option in ["sample_size", "is_lite"]:
            if harness_params.get(option):
                payload[option] = harness_params[option]
        
        if "trust_score" in harnesses:
            if len(harnesses)==1:
                harnesses_modified = ["security","privacy","hallucination","robustness","toxicity","stereotype","fairness","ethics","OpenLLM"]
            else:
                raise ValueError("The `trust_score` harness is available only as a standalone harness.")
        else:
            harnesses_modified = harnesses
        payload["harness_config_ids"] = [f"vijil.harnesses.{h}" for h in harnesses_modified]        

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
        
    def get_status(self, evaluation_id: str):
        """Retrieve the status of an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dict with the id, status, and other metadata of the evaluation
        :rtype: dict
        """

        response = make_api_request(base_url=self.client.base_url, endpoint=f"evaluations/{evaluation_id}", token=self.client.api_key)
        return response
    
    def summarize(self, evaluation_id: str):
        """
        Return summary dataframe of the evaluation results, aggregated at every level
        (overall eval, dimension, scenario, probe)

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dataframe with the level, level_name, and score of the evaluation
        :rtype: pandas.DataFrame
        """

        #initalize list of dicts where keys are level, level_name, score
        summary_rows = []
        
        # get status of evaluation
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e: # for when evaluation doesn't exist
            raise e
        
        # evaluation level
        if status_dict['status']=='COMPLETED':
            row = dict()
            row['level'] = 'overall'
            row['level_name'] = 'evaluation'
            row['score'] = round(status_dict['score']*100, 2)
            summary_rows.append(row)            
        else:
            raise ValueError("Evaluation is not completed yet, check back later.")
        
        # harness level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"harness?evaluation_id={evaluation_id}", token=self.client.api_key)
        for harness in response['results']:
            if harness['harness_type']=='DIMENSION' and harness['score'] is not None:
                row = dict()
                row['level'] = 'harness'
                row['level_name'] = harness['name']
                row['score'] = round(harness['score']*100, 2)
                summary_rows.append(row)   
                
        # scenario level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"scenarios?evaluation_id={evaluation_id}", token=self.client.api_key)
        for scenario in response['results']:
            if scenario['score'] is not None:
                row = dict()
                row['level'] = 'scenario'
                row['level_name'] = scenario['name']
                row['score'] = round(scenario['score']*100, 2)
                summary_rows.append(row)
                
        # probe level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"probes?evaluation_id={evaluation_id}", token=self.client.api_key)
        for probe in response['results']:           
            if probe['score'] is not None:
                row = dict()
                row['level'] = 'probe'
                row['level_name'] = probe['name']
                row['score'] = round(probe['score']*100, 2)
                summary_rows.append(row)
                
        return pd.DataFrame(summary_rows)
        
    def export_summary(self, evaluation_id: str, output_dir: str = './', format: str='pdf'):
        """
        Export a PDF or HTML report of the evaluation results containing evaluation metadata
        plus stats from summarize() function

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param output_dir: The directory to save the report to. Defaults to current directory
        :type output_dir: str
        :param format: The format of the report. Defaults to pdf. Options are 'pdf' and 'html'
        :type format: str
        :raises ValueError: If specified format is not 'pdf' or 'html'
        """
        #get dataframe of summary stats
        summary = self.summarize(evaluation_id=evaluation_id)

        #get evaluation metadata
        status_dict = self.get_status(evaluation_id=evaluation_id)

        #set jinja settings
        HOME = os.path.join(os.path.dirname(__file__), ".")
        templateLoader = jinja2.FileSystemLoader(
            searchpath=HOME + "/templates"
        )
        templateEnv = jinja2.Environment(loader=templateLoader)
        header_template = templateEnv.get_template("vijil_header.jinja")
        footer_template = templateEnv.get_template("vijil_footer.jinja")
        pdf_template = templateEnv.get_template("whole_pdf.jinja")

        filename = evaluation_id + '_summary.' + format

        data_fields = {
            "reportfile": filename,
            "run_uuid": evaluation_id,
            "start_time": str(datetime.fromtimestamp(status_dict['created_at'], tz=timezone.utc)) + " UTC",
            "created_by": status_dict['created_by'],
            "end_time": str(datetime.fromtimestamp(status_dict['completed_at'], tz=timezone.utc)) + " UTC",
            "model_name": status_dict["model"],
            'total_test_count': status_dict['total_test_count'],
            'completed_test_count': status_dict['completed_test_count'],
            'error_test_count': status_dict['error_test_count'],
            "results": summary.to_html(index=False)
        }

        #write to file
        if format=='html': #use header and footer templates for html

            # render the header.
            digest_content = header_template.render(data_fields)            
            # render the footer
            digest_content += footer_template.render()

            with open(os.path.join(output_dir, filename), "w") as f:
                f.write(digest_content)

        elif format=='pdf': #use whole_pdf template which leaves out CSS and JS
            digest_content = pdf_template.render(data_fields)            
            pdf = FPDF()
            pdf.add_page()
            pdf.write_html(digest_content)
            pdf.output(os.path.join(output_dir, filename))
        else:
            raise ValueError("format must be 'html' or 'pdf'") 
    
    def describe(self, evaluation_id: str, limit: int = 1000, format: str = "dataframe", prettify: bool = True, hits_only: bool=False):
        """
        Return either list or dataframe of prompt-level metadata and evaluation results,
        with metadata and evaluation scores for each prompt/response in the given evaluation id.

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in description. Defaults to 1000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "dataframe". Options are "dataframe" and "list"
        :type format: str, optional
        :raises ValueError: If specified format is not 'dataframe' or 'list'
        :param prettify: If True, will remove the "vijil.probes." prefix from the probe names to make it more readable. Defaults to True.
        :type prettify: bool, optional
        :type hits_only: bool, optional
        :param hits_only: If True, will only return prompts that had undesirable responses (according to our detectors). Defaults to False.
        """
        if limit is None:
            limit = 1000000
        
        response = make_api_request(base_url=self.client.base_url, endpoint=f"responses?evaluation_id={evaluation_id}&limit={limit}", token=self.client.api_key)

        # change detector ids to list if it is a string
        results = response['results']
        if len(results) == 0:
            raise ValueError(f"No results found for evaluation id {evaluation_id}. Please check that you have the correct id.")
        for idx, res in enumerate(results):
            if isinstance(res['detector_ids'], str):
                results[idx]['detector_ids'] = [res['detector_ids']]

        prompt_list = [
            {
                "probe": res['probe_config_id'].replace("vijil.probes.", "") if prettify else res['probe_config_id'],
                "input_prompt_id": res['input_prompt_id'],
                "prompt": res['input_prompt'],
                "prompt_list": res['prompt'],
                'prompt_group': res['prompt_group'],
                "response": res['response'],
                "detectors": [
                    det.replace("garak.detectors.", "").replace("autoredteam.detectors.", "")
                    for det in res['detector_ids']
                ],
                "score": res['detector_scores'],
                "triggers": res['triggers'],
                'generation': res['generation'],
                'status': res['status'],
                'error_message': res['error_message']
                
            }
            for res in results
        ]

        #calculate summary stats for detectors
        prompt_list_df = pd.DataFrame(prompt_list)
        prompt_list_df['avg_detector_score'] = prompt_list_df['score'].apply(lambda x: sum([sum(list(item.values())) for item in x]) / len(x) if len(x) and not any([y in ERROR_SKIP_KEYS for item in x for y in item.keys()]) else np.nan)
        prompt_list_df['min_detector_score'] = prompt_list_df['score'].apply(lambda x: min([min(list(item.values())) for item in x]) if len(x) and not any([y in ERROR_SKIP_KEYS for item in x for y in item.keys()]) else np.nan)
        prompt_list_df['max_detector_score'] = prompt_list_df['score'].apply(lambda x: max([max(list(item.values())) for item in x]) if len(x) and not any([y in ERROR_SKIP_KEYS for item in x for y in item.keys()]) else np.nan)
        prompt_list_df.sort_values('probe', inplace=True)    

        #joins for displaying second prompt in pairwise prompts
        prompt_list_df['prompt_group_len'] = prompt_list_df['prompt_group'].apply(lambda x:  len(x))
        pairwise = prompt_list_df[prompt_list_df['prompt_group_len'] == 2]
        nonpairwise = prompt_list_df[prompt_list_df['prompt_group_len'] != 2]
        pairwise['input_prompt_id2'] = pairwise['prompt_group'].apply(lambda x: x[1])
        pairwise_with_prompt2_text = pairwise.merge(pairwise[['input_prompt_id', 'prompt', 'response']].rename(columns={'input_prompt_id': 'input_prompt_id2', 'prompt': 'prompt2', 'response': 'response2'}), on='input_prompt_id2', how='inner')
        #filter out rows with skipped responses---these do not add any information since their reversed counterparts will be included
        pairwise_with_prompt2_text = pairwise_with_prompt2_text[pairwise_with_prompt2_text['score'].apply(lambda x: not any(['SKIP' in item for item in x]))]
        #add empty columns to nonpairwise rows
        nonpairwise['input_prompt_id2'] = None
        nonpairwise['prompt2'] = None
        nonpairwise['response2'] = None
        #concatenate pairwise and nonpairwise dfs row-wise
        output_df = pd.concat([pairwise_with_prompt2_text, nonpairwise], axis=0)
        #drop prompt_group_len column which we needed only for processing
        output_df.drop(columns=['prompt_group_len'], inplace=True)

        if hits_only:
            output_df = output_df[output_df['min_detector_score'] > 0.001] #ToxicCommentModel threshold

        if format=='list':
            return output_df.to_dict(orient='records')
        elif format=='dataframe':
            return output_df
        else:
            raise ValueError("format must be 'list' or 'dataframe'")

    
    def export_report(self, evaluation_id: str, limit: int=1000000, format: str='csv', output_dir: str = './', prettify: bool = True, hits_only: bool=False):
        """
        Exports output of describe() into csv, jsonl, json, or parquet 

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in the report. Defaults to 1000000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "csv". Options are "csv", "parquet", "json" and "jsonl"
        :type format: str, optional
        :raises ValueError: If specified format is not 'csv', 'parquet', 'json' or 'jsonl'
        :param output_dir: The directory to save the report. Defaults to the current directory.
        :type output_dir: str, optional
        :param prettify: If True, will remove the "vijil.probes." prefix from the probe names to make it more readable. Defaults to True.
        :type prettify: bool, optional
        :type hits_only: bool, optional
        :param hits_only: If True, will only return prompts that had undesirable responses (according to our detectors). Defaults to False.        
        """

        if format=='csv':
            prompt_list_df = self.describe(evaluation_id=evaluation_id, limit=limit, format="dataframe", prettify=prettify, hits_only=hits_only)
            filename = evaluation_id + '_report.csv'
            filepath = os.path.join(output_dir, filename)            
            prompt_list_df.to_csv(filepath, index=False)
            print("report exported to " + filepath)
        elif format=='json':
            prompt_list = self.describe(evaluation_id=evaluation_id, limit=limit, format="list", prettify=prettify, hits_only=hits_only)
            filename = evaluation_id + '_report.json'
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(prompt_list, f, indent=4)
            print("report exported to " + filepath)
        elif format=='jsonl':
            prompt_list = self.describe(evaluation_id=evaluation_id, limit=limit, format="list", prettify=prettify, hits_only=hits_only)
            filename = evaluation_id + '_report.jsonl'
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                for item in prompt_list:
                    f.write(json.dumps(item) + '\n')
            print("report exported to " + filepath)
        elif format=='parquet':
            prompt_list_df = self.describe(evaluation_id=evaluation_id, limit=limit, format="dataframe", prettify=prettify, hits_only=hits_only)
            filename = evaluation_id + '_report.parquet'
            filepath = os.path.join(output_dir, filename)
            prompt_list_df.to_parquet(filepath, index=False)
            print("report exported to " + filepath)
        else:
            raise ValueError("format must be 'csv', 'parquet', 'json', or 'jsonl'")

    def cancel(self, evaluation_id: str):
        """
        Cancels an in-progress evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation is not in progress
        :returns: The response from the API
        :rtype: dict
        """

        #check eval status
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e
        
        if status_dict['status'] != 'IN_PROGRESS':
            raise ValueError(f"Evaluation {evaluation_id} is not in progress. Cannot cancel.")
        
        payload = {
                    "type": "CANCEL_EVALUATION",
                    "data": {
                        "evaluation_id": evaluation_id
                    }
                  }
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint="events",
            method="post",
            data=payload,
            token=self.client.api_key
        )
    
    def delete(self, evaluation_id: str):
        """
        Deletes an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation does not exist
        :returns: The response from the API
        :rtype: dict
        """

        #check eval status. This will raise an error if the eval doesn't exist.
        try:
            self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e
        
        payload = {
                    "type": "DELETE_EVALUATION",
                    "data": {
                        "evaluation_id": evaluation_id
                    }
                  }
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint="events",
            method="post",
            data=payload,
            token=self.client.api_key
        )

class Vijil:
    """Base class for the Vijil API client.
    
    :param base_url: The base URL for the Vijil API
    :type base_url: str
    :param api_key: The API key for the Vijil API
    :type api_key: str
    """
    client: VijilClient
    evaluations: Evaluations
    harnesses: Harnesses
    api_keys: APIKeys
    
    def __init__(self, base_url: str = BASE_URL, api_key: Optional[str] = None):
        """Constructor class for VijilClient

        :param base_url: Base URL for API, defaults to BASE_URL as specified in `api.py`
        :type base_url: str, optional
        :param api_key: Vijil API key, defaults to None
        :type api_key: str, optional
        :raises ValueError: if no Vijil API key is provided in api_key and VIJIL_API_KEY is not set as an environment variable
        """
                
        if api_key is None:
            api_key = os.environ["VIJIL_API_KEY"]
        if api_key is None:
            raise ValueError(
                "No API key found! Please set VIJIL_API_KEY as environment variable or supply the `api_key` parameter."
            )
            
        self.client = VijilClient(base_url=base_url, api_key=api_key)
        self.evaluations = Evaluations(self.client)
        self.harnesses = Harnesses(self.client)
        self.api_keys = APIKeys(self.client)
