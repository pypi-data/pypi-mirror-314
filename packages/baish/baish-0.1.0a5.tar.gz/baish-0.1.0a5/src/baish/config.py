from dataclasses import dataclass
from typing import Dict, Optional
import os
import yaml
from pathlib import Path
from urllib.parse import urlparse

@dataclass
class LLMConfig:
    name: str
    provider: str
    model: str
    api_key: Optional[str] = None
    temperature: float = 0.1
    token_limit: int = 8000
    url: Optional[str] = None

    def __post_init__(self):
        if self.provider == 'ollama':
            if not self.url:
                self.url = 'http://localhost:11434'
            else:
                self._validate_url(self.url)

    def _validate_url(self, url: str) -> None:
        try:
            result = urlparse(url)
            if not all([result.scheme in ['http', 'https'], result.netloc]):
                raise ValueError
        except ValueError:
            raise ValueError(f"Invalid URL for Ollama provider: {url}")

@dataclass
class Config:
    llms: Dict[str, LLMConfig]
    default_llm: Optional[str] = None
    baish_dir: Path = Path.home() / ".baish"
    current_id: Optional[str] = None
    current_date: Optional[str] = None

    SUPPORTED_PROVIDERS = ['groq', 'anthropic', 'ollama']

    @staticmethod
    def validate_llm_name(name: str) -> bool:
        import re
        return bool(re.match(r'^[a-zA-Z0-9_]{1,32}$', name))

    @classmethod
    def load(cls, config_file=None) -> 'Config':
        """Load config from file"""
        if config_file:
            if not os.path.exists(config_file):
                raise ValueError(f"Config file not found: {config_file}")
            config_path = config_file
        else:
            # Try default locations
            config_locations = [
                os.path.expanduser('~/.baish/config.yaml'),
                os.path.expanduser('~/.config/baish/config.yaml'),
                '/etc/baish/config.yaml'
            ]
            
            config_path = next((f for f in config_locations if os.path.exists(f)), None)
            
            if not config_path:
                raise ValueError("No config file found. Please create a config file in one of these locations:\n" + 
                               "\n".join(f"  - {loc}" for loc in config_locations))

        with open(config_path) as f:
            config_data = yaml.safe_load(f) or {}

        if not config_data.get('llms'):
            raise ValueError(f"No LLMs configured in config file: {config_path}")
        
        baish_dir = Path(config_data.get('baish_dir', Path.home() / ".baish"))
        
        llms_data = config_data.get('llms', {})
        configured_llms = {}
        
        for name, llm_data in llms_data.items():
            if not cls.validate_llm_name(name):
                raise ValueError(f"Invalid LLM name: {name}")
            
            provider = llm_data['provider']
            if provider not in cls.SUPPORTED_PROVIDERS:
                raise ValueError(f"Unsupported LLM provider: {provider}")
            
            api_key = (
                llm_data.get('api_key') or 
                os.getenv(f"{provider.upper()}_API_KEY")
            )
            
            if not api_key and provider != 'ollama':
                raise ValueError(f"No API key found for {provider}. Set it in config or {provider.upper()}_API_KEY environment variable")
            
            configured_llms[name] = LLMConfig(
                name=name,
                provider=provider,
                model=llm_data['model'],
                api_key=api_key,
                temperature=llm_data.get('temperature', 0.1),
                token_limit=llm_data.get('token_limit', 4000),
                url=llm_data.get('url')
            )
        
        default_llm = config_data.get('default_llm')
        if not default_llm:
            raise ValueError("No default LLM specified in config file or via CLI")
            
        return cls(
            llms=configured_llms,
            default_llm=default_llm,
            baish_dir=baish_dir
        )

    @property
    def llm(self) -> LLMConfig:
        """Get the current LLM configuration"""
        return self.llms[self.default_llm]
