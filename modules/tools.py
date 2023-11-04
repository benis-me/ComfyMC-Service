import os
import git
import time
import json
import torch
import shutil
import urllib
import aiohttp
import platform
import threading
import subprocess
import folder_paths

from .paths import custom_nodes_path, extension_path

comfy_required_version = 1240

def handle_stream(stream, prefix):
    for line in stream:
        print(prefix, line, end="")

def run_script(cmd, cwd='.'):
    process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    stdout_thread = threading.Thread(target=handle_stream, args=(process.stdout, ""))
    stderr_thread = threading.Thread(target=handle_stream, args=(process.stderr, "[!]"))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    return process.wait()


comfy_version = 'unknown'
def get_comfy_version():
    global comfy_version
    try:
        repo = git.Repo(os.path.dirname(folder_paths.__file__))
        comfy_version = len(list(repo.iter_commits('HEAD')))
        current_branch = repo.active_branch.name
        git_hash = repo.head.object.hexsha

        print(f"\n***Comfy 版本: {comfy_version} - 分支: {current_branch} - Hash: {git_hash}***\n")
    except:
        print("*** WARNING: 无法获取 Comfy 的版本信息. ***")



async def fetch_data(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as resp:
            return json.loads(await resp.text())


def download_url_with_agent(url, save_path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        with open(save_path, 'wb') as f:
            f.write(data)

    except Exception as e:
        print(f"***下载失败: {url} / {e}***")
        return False

    print("***安装成功***")
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
            print(f"***{action_name}(copy)失败: {url} / {e}***")

            return False

    print(f"***{action_name}成功.***")
    return True


def rmtree(path):
    retry_count = 3

    while True:
        try:
            retry_count -= 1

            if platform.system() == "Windows":
                run_script(['attrib', '-R', path + '\\*', '/S'])
            shutil.rmtree(path)

            return True

        except Exception as ex:
            print(f"ex: {ex}")
            time.sleep(3)

            if retry_count < 0:
                raise ex

            print(f"Uninstall retry({retry_count})")


import numpy as np
import PIL.Image as Image

def tensor_to_pil(img_tensor, batch_index=0):
    img_tensor = img_tensor[batch_index].unsqueeze(0)
    i = 255. * img_tensor.cpu().numpy()
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
    return img


def pil_to_tensor(image):
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image).unsqueeze(0)
    if len(image.shape) == 3:
        image = image.unsqueeze(-1)
    return image
