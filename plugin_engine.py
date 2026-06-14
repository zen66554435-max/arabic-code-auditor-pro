"""
Arabic Code Auditor Pro - Plugin Engine
محرك الإضافات - محمي بترخيص
"""
import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json


class PluginType(Enum):
    ANALYZER = "analyzer"
    FIXER = "fixer"
    SECURITY = "security"
    REPORT = "report"
    AI = "ai"
    CUSTOM = "custom"

@dataclass
class Plugin:
    id: str
    name: str
    name_ar: str
    version: str
    author: str
    description: str
    description_ar: str
    plugin_type: PluginType
    entry_point: str
    config: Dict[str, Any]
    enabled: bool = True
    sandboxed: bool = True

class PluginEngine:
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        self.loaded_modules: Dict[str, Any] = {}
        os.makedirs(plugins_dir, exist_ok=True)

    def discover_plugins(self) -> List[Plugin]:
        discovered = []
        if not os.path.exists(self.plugins_dir):
            return discovered
        for item in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, item)
            if os.path.isdir(plugin_path):
                manifest_path = os.path.join(plugin_path, "manifest.json")
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                        plugin = Plugin(
                            id=manifest.get('id', item),
                            name=manifest.get('name', item),
                            name_ar=manifest.get('name_ar', manifest.get('name', item)),
                            version=manifest.get('version', '1.0.0'),
                            author=manifest.get('author', 'Unknown'),
                            description=manifest.get('description', ''),
                            description_ar=manifest.get('description_ar', ''),
                            plugin_type=PluginType(manifest.get('type', 'custom')),
                            entry_point=manifest.get('entry_point', 'main.py'),
                            config=manifest.get('config', {}),
                            enabled=manifest.get('enabled', True),
                            sandboxed=manifest.get('sandboxed', True)
                        )
                        discovered.append(plugin)
                    except Exception as e:
                        print(f"Error loading plugin {item}: {e}")
        return discovered

    def load_plugin(self, plugin: Plugin) -> bool:
        try:
            plugin_path = os.path.join(self.plugins_dir, plugin.id)
            entry_path = os.path.join(plugin_path, plugin.entry_point)
            if not os.path.exists(entry_path):
                return False
            spec = importlib.util.spec_from_file_location(f"aca_plugin_{plugin.id}", entry_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.loaded_modules[plugin.id] = module
            self.plugins[plugin.id] = plugin
            if hasattr(module, 'register_hooks'):
                module.register_hooks(self)
            return True
        except Exception as e:
            print(f"Failed to load plugin {plugin.id}: {e}")
            return False

    def unload_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self.loaded_modules:
            del self.loaded_modules[plugin_id]
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
        return True

    def register_hook(self, event: str, callback: Callable):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)

    def trigger_hook(self, event: str, *args, **kwargs) -> List[Any]:
        results = []
        for callback in self.hooks.get(event, []):
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Error in hook {event}: {e}")
        return results

    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        return self.plugins.get(plugin_id)

    def list_plugins(self) -> List[Plugin]:
        return list(self.plugins.values())

    def enable_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = True
            return True
        return False

    def disable_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = False
            return True
        return False

_plugin_engine = None

def get_plugin_engine(plugins_dir: str = "plugins") -> PluginEngine:
    global _plugin_engine
    if _plugin_engine is None:
        _plugin_engine = PluginEngine(plugins_dir)
    return _plugin_engine
