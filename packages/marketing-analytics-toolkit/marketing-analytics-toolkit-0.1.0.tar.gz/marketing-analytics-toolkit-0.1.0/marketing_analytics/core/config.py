from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import yaml
import json
from pathlib import Path
import os
from datetime import datetime
import logging
from .exceptions import ConfigurationError

@dataclass
class ModelConfig:
    """Model konfigürasyon sınıfı"""
    name: str
    version: str
    params: Dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: Optional[str] = None
    dependencies: Dict[str, str] = field(default_factory=dict)
    performance_thresholds: Dict[str, float] = field(default_factory=dict)
    
@dataclass
class SystemConfig:
    """Sistem konfigürasyon sınıfı"""
    random_state: int = 42
    n_jobs: int = -1
    verbose: bool = False
    log_level: str = 'INFO'
    cache_dir: str = '.cache'
    max_memory_usage: str = '8G'
    timeout: int = 3600
    retry_attempts: int = 3
    
@dataclass
class ValidationConfig:
    """Doğrulama konfigürasyon sınıfı"""
    strict_mode: bool = True
    allowed_missing_ratio: float = 0.1
    data_quality_checks: List[str] = field(default_factory=list)
    validation_rules: Dict[str, Any] = field(default_factory=dict)

class ConfigManager:
    """Gelişmiş Konfigürasyon Yönetici Sınıfı"""
    
    def __init__(self,
                 config_path: Optional[str] = None,
                 env: str = 'development'):
        self.env = env
        self.model_configs: Dict[str, ModelConfig] = {}
        self.system_config = SystemConfig()
        self.validation_config = ValidationConfig()
        self.logger = self._setup_logging()
        
        if config_path:
            self.load_config(config_path)
            
    def _setup_logging(self) -> logging.Logger:
        """Loglama yapılandırması"""
        logger = logging.getLogger('ConfigManager')
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
        
    def load_config(self, path: str) -> None:
        """Konfigürasyon yükleme"""
        try:
            if path.endswith('.yaml') or path.endswith('.yml'):
                with open(path, 'r') as f:
                    config_data = yaml.safe_load(f)
            elif path.endswith('.json'):
                with open(path, 'r') as f:
                    config_data = json.load(f)
            else:
                raise ConfigurationError(f"Unsupported config file format: {path}")
                
            self._parse_config(config_data)
            self.logger.info(f"Configuration loaded from {path}")
            
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            raise ConfigurationError(f"Failed to load config: {str(e)}")
            
    def _parse_config(self, config_data: Dict) -> None:
        """Konfigürasyon ayrıştırma"""
        # Sistem konfigürasyonu
        if 'system' in config_data:
            self.system_config = SystemConfig(**config_data['system'])
            
        # Doğrulama konfigürasyonu
        if 'validation' in config_data:
            self.validation_config = ValidationConfig(**config_data['validation'])
            
        # Model konfigürasyonları
        if 'models' in config_data:
            for model_name, model_config in config_data['models'].items():
                self.add_model_config(ModelConfig(
                    name=model_name,
                    **model_config
                ))
                
    def add_model_config(self, model_config: ModelConfig) -> None:
        """Model konfigürasyonu ekleme"""
        self.model_configs[model_config.name] = model_config
        self.logger.debug(f"Added config for model: {model_config.name}")
        
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Model konfigürasyonunu getir"""
        return self.model_configs.get(model_name)
        
    def update_system_config(self, **kwargs) -> None:
        """Sistem konfigürasyonunu güncelle"""
        for key, value in kwargs.items():
            if hasattr(self.system_config, key):
                setattr(self.system_config, key, value)
                self.logger.debug(f"Updated system config: {key}={value}")
            else:
                raise ConfigurationError(f"Invalid system config parameter: {key}")
                
    def save_config(self, path: str) -> None:
        """Konfigürasyonu kaydet"""
        config_data = {
            'system': self.system_config.__dict__,
            'validation': self.validation_config.__dict__,
            'models': {
                name: config.__dict__
                for name, config in self.model_configs.items()
            }
        }
        
        try:
            if path.endswith('.yaml') or path.endswith('.yml'):
                with open(path, 'w') as f:
                    yaml.dump(config_data, f)
            elif path.endswith('.json'):
                with open(path, 'w') as f:
                    json.dump(config_data, f, indent=4)
            else:
                raise ConfigurationError(f"Unsupported config file format: {path}")
                
            self.logger.info(f"Configuration saved to {path}")
            
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
            raise ConfigurationError(f"Failed to save config: {str(e)}")
            
    def validate_config(self) -> bool:
        """Konfigürasyon doğrulama"""
        try:
            # Sistem konfigürasyonu doğrulama
            if self.system_config.n_jobs < -1:
                raise ConfigurationError("Invalid n_jobs value")
                
            # Model konfigürasyonları doğrulama
            for model_name, config in self.model_configs.items():
                if not config.version:
                    raise ConfigurationError(f"Missing version for model {model_name}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False