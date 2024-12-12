from pathlib import Path
import yaml
import os

CONFIG_FILE = Path.home() / '.xmlapply.yml'

def get_config() -> dict:
    """Read config file or return defaults"""
    if not CONFIG_FILE.exists():
        return {'default_directory': str(Path.cwd())}
    
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f) or {'default_directory': str(Path.cwd())}

def save_config(config: dict) -> None:
    """Save config to file"""
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

def set_default_directory(directory: str) -> None:
    """Set the default project directory"""
    config = get_config()
    config['default_directory'] = str(Path(directory).expanduser().resolve())
    save_config(config)

def get_default_directory() -> Path:
    """Get the default project directory"""
    config = get_config()
    return Path(config['default_directory'])