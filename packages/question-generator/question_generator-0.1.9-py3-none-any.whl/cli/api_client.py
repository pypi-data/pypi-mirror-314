import os
import json
import aiohttp
from typing import Optional, Dict, Any
from pathlib import Path
from platformdirs import user_config_dir

def get_config_path():
    """Get the platform-specific config directory"""
    config_dir = user_config_dir("question-generator", "devfactory")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'config.json')

class PromptGeneratorClient:
    """API client for the Prompt Generator service."""
    
    def __init__(self):
        # Try to get API key from environment first
        self.api_key = os.getenv('PROMPT_GENERATOR_API_KEY')
        
        # If not in environment, try to load from config file
        if not self.api_key:
            config_path = get_config_path()
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
            except (FileNotFoundError, json.JSONDecodeError):
                pass
                
        if not self.api_key:
            raise ValueError("API key not configured. Run 'qg config -k YOUR_KEY' to set it up.")
            
        self.api_base = 'https://fdchqspik1.execute-api.us-east-1.amazonaws.com/Prod'
        self.session = aiohttp.ClientSession()
        
        # Common headers for all requests
        self.headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict:
        """Make an HTTP request to the API with error handling."""
        url = f"{self.api_base}{endpoint}"
        
        # Remove None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        async with self.session.request(method, url, params=params, json=json_data, headers=self.headers) as response:
            response_json = await response.json()
            
            if response.status >= 400:
                error_msg = response_json.get('error', 'Unknown error')
                raise ValueError(f"API request failed: {error_msg}")
            
            return response_json
    
    async def list_items(self, type: Optional[str] = None, section: Optional[str] = None,
                        doc_type: Optional[str] = None, include_archived: bool = False) -> Dict:
        """List items from the API."""
        params = {
            'type': type,
            'section': section,
            'doc_type': doc_type,
            'archive': str(include_archived).lower()
        }
        return await self._make_request('GET', '/items', params=params)
    
    async def get_item(self, type: str, doc_type: str, name: str) -> Dict:
        """Get a specific item from the API."""
        params = {
            'doc_type': doc_type
        }
        return await self._make_request('GET', f'/items/{type}/{name}', params=params)
    
    async def create_item(self, type: str, section: str, content: str,
                         doc_type: Optional[str] = None) -> Dict:
        """Create a new item via the API."""
        data = {
            'type': type,
            'section': section,
            'content': content,
            'doc_type': doc_type
        }
        return await self._make_request('POST', '/items', json_data=data)
    
    async def delete_items(self, type: Optional[str] = None, section: Optional[str] = None,
                          doc_type: Optional[str] = None, archive_only: bool = False) -> Dict:
        """Delete items via the API."""
        params = {
            'type': type,
            'section': section,
            'doc_type': doc_type,
            'archive': str(archive_only).lower()
        }
        return await self._make_request('DELETE', '/items', params=params)
    
    async def generate_questions(self, guidance_content: str, template_content: str) -> Dict:
        """Generate questions via the API."""
        data = {
            'prompt_type': 'questions',
            'guidance_content': guidance_content,
            'template_content': template_content
        }
        return await self._make_request('POST', '/generate', json_data=data)
    
    async def generate_prompt(self, template_content: Dict) -> Dict:
        """Generate a prompt via the API."""
        data = {
            'prompt_type': 'prompt',
            'template_content': template_content
        }
        return await self._make_request('POST', '/generate', json_data=data)

    async def update_item(self, type: str, section: str, content: str,
                         doc_type: Optional[str] = None) -> Dict:
        """Update an existing item via the API."""
        if type != 'questions':
            raise ValueError("Only questions can be updated")
            
        data = {
            'section': section,
            'content': content,
            'doc_type': doc_type
        }
        return await self._make_request('PATCH', f'/items/{type}', json_data=data)
