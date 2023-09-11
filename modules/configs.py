import os
import json
from .paths import configs_path

configs = None
def load_configs():
    # 是否存在配置文件，如果不存在则创建
    if not os.path.exists(configs_path):
        with open(configs_path, 'w', encoding='utf-8') as f:
            json.dump({
                "channel_url": "https://raw.githubusercontent.com/benis-me/ComfyMC-Service-CustomNodes/main"
            }, f, indent=4)
    try:
        with open(configs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"*** WARNING: 打开配置文件 {configs_path} 失败 ***")
        return {
            "channel_url": "https://raw.githubusercontent.com/benis-me/ComfyMC-Service-CustomNodes/main"
        }


def get_config(key):
    global configs
    if configs is None:
        configs = load_configs()
    return configs.get(key)
