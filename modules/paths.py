import os
import folder_paths

comfy_path = os.path.dirname(folder_paths.__file__)
custom_nodes_path = os.path.join(comfy_path, 'custom_nodes')
extension_path = os.path.join(comfy_path, 'web', 'extensions')
service_modules_path = os.path.dirname(__file__)
service_path = os.path.dirname(service_modules_path)
configs_path = os.path.join(service_path, 'configs.json')
git_script_path = os.path.join(service_modules_path, 'git_script.py')
startup_script_path = os.path.join(service_path, "startup-scripts")
