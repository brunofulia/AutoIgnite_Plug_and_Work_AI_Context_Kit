import os
import configparser
from pathlib import Path

def get_config():
    """
    Reads and returns the configuration from autoignite.ini.
    If the file does not exist, it creates it with default values.
    """
    config_file = Path("autoignite.ini")
    config = configparser.ConfigParser()
    
    if not config_file.exists():
        # Default values (Native Mode)
        config["Paths"] = {
            "core_path": "./core",
            "target_path": "./"
        }
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception:
            pass
    else:
        config.read(config_file, encoding="utf-8")
        
        needs_save = False
        if "Paths" not in config:
            config["Paths"] = {}
            needs_save = True
            
        paths = config["Paths"]
        
        if "core_path" not in paths:
            paths["core_path"] = "./core"
            needs_save = True
        if "target_path" not in paths:
            paths["target_path"] = "./"
            needs_save = True
            
        if needs_save:
            try:
                with open(config_file, "w", encoding="utf-8") as f:
                    config.write(f)
            except Exception:
                pass
                
    return config

def get_core_path() -> Path:
    config = get_config()
    val = config["Paths"]["core_path"].strip()
    return Path(val)

def get_target_path() -> Path:
    config = get_config()
    val = config["Paths"]["target_path"].strip()
    return Path(val)

def is_mirror_mode() -> bool:
    """
    Determines if target_path points to an external directory,
    which activates the Observer Mode (Ghost Mirror).
    """
    config = get_config()
    raw_target = config["Paths"]["target_path"].strip()
    return raw_target not in [".", "./", ".\\"]
