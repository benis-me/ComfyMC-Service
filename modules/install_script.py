import os
import sys
import git
import zipfile
import platform
import urllib.request
from torchvision.datasets.utils import download_url

from .git_script import git_pull
from .git_helper import git_repo_has_updates
from .tools import comfy_version, comfy_required_version, run_script, rmtree
from .paths import startup_script_path, custom_nodes_path, extension_path, git_script_path


### Install Scripts
def try_install_script(url, repo_path, install_cmd):
    int_comfy_version = 0

    if type(comfy_version) == int:
        int_comfy_version = comfy_version
    elif comfy_version.isdigit():
        int_comfy_version = int(comfy_version)

    if platform.system() == "Windows" and int_comfy_version >= comfy_required_version:
        if not os.path.exists(startup_script_path):
            os.makedirs(startup_script_path)

        script_path = os.path.join(startup_script_path, "install-scripts.txt")
        with open(script_path, "a") as file:
            obj = [repo_path] + install_cmd
            file.write(f"{obj}\n")

        return True
    else:
        print(f"\n## ComfyUI-Manager: EXECUTE => {install_cmd}")
        code = run_script(install_cmd, cwd=repo_path)

        if platform.system() == "Windows":
            try:
                if int(comfy_version) < comfy_required_version:
                    print("\n\n###################################################################")
                    print(f"[WARN] ComfyMC-Service: Comfy 版本 ({comfy_version}) 过旧. 请更新最新版.")
                    print(f"[WARN] 扩展在当前版本的 Comfy 可能会运行出错.")
                    print("###################################################################\n\n")
            except:
                pass

        if code != 0:
            print(f"安装脚本出错: {url}")
            return False


def execute_install_script(url, repo_path):
    install_script_path = os.path.join(repo_path, "install.py")
    requirements_path = os.path.join(repo_path, "requirements.txt")

    if os.path.exists(requirements_path):
        print("Install: pip packages")
        with open(requirements_path, "r") as requirements_file:
            for line in requirements_file:
                package_name = line.strip()
                if package_name:
                    install_cmd = [sys.executable, "-m", "pip", "install", package_name]
                    if package_name.strip() != "":
                        try_install_script(url, repo_path, install_cmd)

    if os.path.exists(install_script_path):
        print(f"安装: install script")
        install_cmd = [sys.executable, "install.py"]
        try_install_script(url, repo_path, install_cmd)

    return True


# 检查节点是否已安装
def check_node_installed(node, fetch=False, update_check=True):
    node['install_status'] = 'None'

    if node['install_type'] == 'git-clone' and len(node['files']) == 1:
        dir_name = os.path.splitext(os.path.basename(node['files'][0]))[0].replace('.git', '')
        dir_path = os.path.join(custom_nodes_path, dir_name)
        if os.path.exists(dir_path):
            try:
                if update_check and git_repo_has_updates(dir_path, fetch):
                    node['install_status'] = 'Update'
                else:
                    node['install_status'] = 'Installed'
            except Exception as e:
                print(f"*** WARNING: 无法检查位于 {dir_path} 的更新. ***")
                node['install_status'] = 'Error'

        elif os.path.exists(dir_path + '.disabled'):
            node['install_status'] = 'Disabled'
        else:
            node['install_status'] = 'Not-Installed'

    elif node['install_type'] == 'copy' and len(node['files']) == 1:
        dir_name = os.path.basename(node['files'][0])

        if node['files'][0].endswith('.py'):
            base_path = custom_nodes_path
        elif 'js_path' in node:
            base_path = os.path.join(extension_path, node['js_path'])
        else:
            base_path = extension_path

        file_path = os.path.join(base_path, dir_name)
        if os.path.exists(file_path):
            node['install_status'] = 'Installed'
        elif os.path.exists(file_path + '.disabled'):
            node['install_status'] = 'Disabled'
        else:
            node['install_status'] = 'Not-Installed'


def check_nodes_installed(nodes, fetch=False, update_check=True):
    for node in nodes['custom_nodes']:
        check_node_installed(node, fetch, update_check)


### Unzip Install
def unzip_install(files):
    temp_filename = 'manager-temp.zip'
    for url in files:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            data = response.read()

            with open(temp_filename, 'wb') as f:
                f.write(data)

            with zipfile.ZipFile(temp_filename, 'r') as zip_ref:
                zip_ref.extractall(custom_nodes_path)

            os.remove(temp_filename)
        except Exception as e:
            print(f"安装失败(unzip): {url} / {e}")
            return False

    print("安装成功")
    return True


### Copy Uninstall
def copy_install(files, js_path_name=None):
    for url in files:
        try:
            if url.endswith(".py"):
                download_url(url, custom_nodes_path)
            else:
                path = os.path.join(extension_path, js_path_name) if js_path_name is not None else extension_path
                if not os.path.exists(path):
                    os.makedirs(path)
                download_url(url, path)

        except Exception as e:
            print(f"安装失败(copy): {url} / {e}")
            return False

    print("安装成功")
    return True


def copy_uninstall(files, js_path_name='.'):
    for url in files:
        dir_name = os.path.basename(url)
        base_path = custom_nodes_path if url.endswith('.py') else os.path.join(extension_path, js_path_name)
        file_path = os.path.join(base_path, dir_name)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            elif os.path.exists(file_path + ".disabled"):
                os.remove(file_path + ".disabled")
        except Exception as e:
            print(f"卸载失败(copy): {url} / {e}")
            return False

    print("卸载成功")
    return True


def copy_set_active(files, is_disable, js_path_name='.'):
    if is_disable:
        action_name = "禁用"
    else:
        action_name = "启用"

    for url in files:
        dir_name = os.path.basename(url)
        base_path = custom_nodes_path if url.endswith('.py') else os.path.join(extension_path, js_path_name)
        file_path = os.path.join(base_path, dir_name)

        try:
            if is_disable:
                current_name = file_path
                new_name = file_path + ".disabled"
            else:
                current_name = file_path + ".disabled"
                new_name = file_path

            os.rename(current_name, new_name)

        except Exception as e:
            print(f"{action_name}失败(copy): {url} / {e}")

            return False

    print(f"{action_name}成功")
    return True


### Git Clone Install
def git_clone_install(files):
    print(f"安装: {files}")
    for url in files:
        try:
            print(f"Download: git clone '{url}'")
            repo_name = os.path.splitext(os.path.basename(url))[0]
            repo_path = os.path.join(custom_nodes_path, repo_name)

            # Clone the repository from the remote URL
            if platform.system() == 'Windows':
                run_script([sys.executable, git_script_path, "--clone", custom_nodes_path, url])
            else:
                repo = git.Repo.clone_from(url, repo_path, recursive=True)
                repo.git.clear_cache()
                repo.close()

            if not execute_install_script(url, repo_path):
                return False

        except Exception as e:
            print(f"安装失败(git-clone): {url} / {e}")
            return False

    print("安装成功.")
    return True


def git_clone_uninstall(files):
    print(f"卸载: {files}")
    for url in files:
        try:
            dir_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            dir_path = os.path.join(custom_nodes_path, dir_name)

            # safety check
            if dir_path == '/' or dir_path[1:] == ":/" or dir_path == '':
                print(f"卸载(git-clone)失败: 无效路径 '{dir_path}' : '{url}'")
                return False

            install_script_path = os.path.join(dir_path, "uninstall.py")
            disable_script_path = os.path.join(dir_path, "disable.py")
            if os.path.exists(install_script_path):
                uninstall_cmd = [sys.executable, "uninstall.py"]
                code = run_script(uninstall_cmd, cwd=dir_path)

                if code != 0:
                    print(f"An error occurred during the execution of the uninstall.py script. Only the '{dir_path}' will be deleted.")
            elif os.path.exists(disable_script_path):
                disable_script = [sys.executable, "disable.py"]
                code = run_script(disable_script, cwd=dir_path)
                if code != 0:
                    print(f"An error occurred during the execution of the disable.py script. Only the '{dir_path}' will be deleted.")

            if os.path.exists(dir_path):
                rmtree(dir_path)
            elif os.path.exists(dir_path + ".disabled"):
                rmtree(dir_path + ".disabled")
        except Exception as e:
            print(f"卸载失败(git-clone): {url} / {e}")
            return False

    print("卸载成功")
    return True


def git_clone_set_active(files, is_disable):
    if is_disable:
        action_name = "禁用"
    else:
        action_name = "启用"

    print(f"{action_name}: {files}")
    for url in files:
        try:
            dir_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            dir_path = os.path.join(custom_nodes_path, dir_name)

            # safey check
            if dir_path == '/' or dir_path[1:] == ":/" or dir_path == '':
                print(f"{action_name}失败(git-clone): 无效路径 '{dir_path}' : '{url}'")
                return False

            if is_disable:
                current_path = dir_path
                new_path = dir_path + ".disabled"
            else:
                current_path = dir_path + ".disabled"
                new_path = dir_path

            os.rename(current_path, new_path)

            if is_disable:
                if os.path.exists(os.path.join(new_path, "disable.py")):
                    disable_script = [sys.executable, "disable.py"]
                    try_install_script(url, new_path, disable_script)
            else:
                if os.path.exists(os.path.join(new_path, "enable.py")):
                    enable_script = [sys.executable, "enable.py"]
                    try_install_script(url, new_path, enable_script)

        except Exception as e:
            print(f"{action_name}失败(git-clone): {url} / {e}")
            return False

    print(f"{action_name}成功")
    return True


def git_clone_update(files):
    import os

    print(f"更新: {files}")
    for url in files:
        try:
            repo_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            repo_path = os.path.join(custom_nodes_path, repo_name)
            git_pull(repo_path)

            if not execute_install_script(url, repo_path):
                return False

        except Exception as e:
            print(f"更新失败(git-clone): {url} / {e}")
            return False

    print("更新失败")
    return True
