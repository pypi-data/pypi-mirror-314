import requests
import logging
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Set
from urllib3.exceptions import InsecureRequestWarning
from .models import ChatRequest, ChatResponse, APIError

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoliathClient:
    """Client for interacting with the Goliath LLM API."""
    
    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://api.goliath-routing.duckdns.org/",
        verify_ssl: bool = False  # Add SSL verification parameter
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.verify = verify_ssl  # Set SSL verification
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        logger.info(f'Initialized GoliathClient with base URL: {self.base_url} (SSL verify: {verify_ssl})')

    def list_models(self) -> List[str]:
        """Get list of available models from local YAML file."""
        try:
            # Get the path to the list_models.yaml file
            yaml_path = Path(__file__).parent / 'list_models.yaml'
            
            with open(yaml_path, 'r') as file:
                yaml_data = yaml.safe_load(file)
                logger.debug(f'Loaded providers: {list(yaml_data["providers"].keys())}')

            # Collect all unique model names
            models = set()
            for provider_data in yaml_data['providers'].values():
                models.update(provider_data.get('models', {}).keys())
            
            sorted_models = sorted(models)
            logger.debug(f'Available models: {sorted_models}')
            return sorted_models

        except Exception as e:
            logger.error(f'Failed to load models: {str(e)}')
            raise APIError(f"Failed to load models: {str(e)}")

    def get_model_providers(self, model: str) -> List[Dict[str, float]]:
        """Get list of providers and their costs for a specific model."""
        try:
            yaml_path = Path(__file__).parent / 'list_models.yaml'
            
            with open(yaml_path, 'r') as file:
                yaml_data = yaml.safe_load(file)

            providers = []
            for provider_name, provider_data in yaml_data['providers'].items():
                if model in provider_data.get('models', {}):
                    providers.append({
                        'name': provider_name,
                        'cost': provider_data['models'][model].get('price_per_output_token', 0)
                    })
            
            return sorted(providers, key=lambda x: x['cost'])

        except Exception as e:
            logger.error(f'Failed to get providers for model {model}: {str(e)}')
            raise APIError(f"Failed to get model providers: {str(e)}")

    def chat(
        self,
        prompt: str,
        model: str,
        history: Optional[List[Dict[str, str]]] = None,
        provider: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """Send a chat request to the Goliath API."""
        # Validate model is available
        available_models = self.list_models()
        if model not in available_models:
            raise APIError(f"Model '{model}' not found. Available models: {available_models}")

        # If no provider specified, validate model has providers
        if not provider:
            providers = self.get_model_providers(model)
            if not providers:
                raise APIError(f"No providers available for model '{model}'")

        logger.info('Sending chat request')
        logger.debug(f'Chat request - Model: {model}, Message length: {len(prompt)}')
        
        request = ChatRequest(
            model=model,
            prompt=prompt,
            history=history or [],
            provider=provider,
            temperature=temperature,
            max_tokens=max_tokens
        )

        try:
            logger.debug(f'Sending request to API at {self.base_url}/generate')
            response = self.session.post(
                f"{self.base_url}/generate",
                json=request.model_dump(),
                verify=self.verify_ssl  # Use SSL verification setting
            )

            if response.status_code == 403:
                logger.error('Authentication failed')
                raise APIError("Authentication failed")
            elif response.status_code == 200:
                logger.info('Successfully received response from API')
                data = response.json()
                logger.debug(f'Response metrics: {data.get("metrics")}')
                return ChatResponse(**data)
            else:
                logger.error(f'API request failed with status {response.status_code}: {response.text}')
                raise APIError(
                    f"API request failed with status {response.status_code}: {response.text}"
                )

        except requests.exceptions.SSLError as e:
            logger.error(f'SSL verification failed: {str(e)}')
            raise APIError(
                "SSL verification failed. If you trust this endpoint, "
                "you can disable SSL verification by setting verify_ssl=False"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {str(e)}')
            raise APIError(f"Request failed: {str(e)}")
