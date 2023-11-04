import os.path
import sys

import git
from aiohttp import web

import folder_paths
import server
from .modules.configs import get_config
from .modules.git_script import git_pull
from .modules.install_script import \
    unzip_install, \
    copy_install, \
    copy_uninstall, \
    copy_set_active, \
    git_clone_update, \
    git_clone_install, \
    try_install_script, \
    git_clone_uninstall, \
    git_clone_set_active, \
    check_nodes_installed, \
    execute_install_script
from .modules.paths import comfy_path
from .modules.tools import fetch_data

from .modules.custom_nodes import \
    NODE_MAPPINGS, \
    NODE_NAME_MAPPINGS


# ----------------------------------------------------------------------------------------------------------------------
# 自定义节点管理
# ----------------------------------------------------------------------------------------------------------------------
# 获取节点列表
@server.PromptServer.instance.routes.get('/service/node/list')
async def get_node_list(request):
    if "skip_update" in request.rel_url.query and request.rel_url.query["skip_update"] == "true":
        skip_update = True
    else:
        skip_update = False

    url = get_config('channel_url') + '/custom-node-list.json'
    res = await fetch_data(url)
    check_nodes_installed(res, False, not skip_update)
    return web.json_response(res, content_type='application/json')


# 安装节点
@server.PromptServer.instance.routes.post('/service/node/install')
async def install_node(request):
    json_data = await request.json()
    install_name = json_data['title']
    install_files = json_data['files']
    install_type = json_data['install_type']

    print(f"***安装自定义节点 '{install_name}'***")

    res = False
    if len(install_files) == 0:
        return web.Response(status=400, text='文件列表为空')

    if install_type == 'unzip':
        res = unzip_install(install_files)

    if install_type == 'copy':
        js_path_name = json_data['js_path'] if 'js_path' in json_data else '.'
        res = copy_install(install_files, js_path_name)

    elif install_type == 'git-clone':
        res = git_clone_install(install_files)

    if 'pip' in json_data:
        for pname in json_data['pip']:
            install_cmd = [sys.executable, '-m', 'pip', 'install', pname]
            try_install_script(install_files[0], '.', install_cmd)

    if res:
        print(f"***自定义节点 '{install_name}' 安装成功***")
        return web.json_response({'status': '安装成功'}, content_type='application/json')

    return web.Response(status=400, text='安装失败')


# 卸载节点
@server.PromptServer.instance.routes.post('/service/node/uninstall')
async def uninstall_node(request):
    json_data = await request.json()
    install_name = json_data['title']
    install_files = json_data['files']
    install_type = json_data['install_type']

    print(f"***卸载自定义节点 {install_name} ***")
    res = False

    if install_type == 'copy':
        js_path_name = json_data['js_path'] if 'js_path' in json_data else '.'
        res = copy_uninstall(install_files, js_path_name)

    elif install_type == 'git-clone':
        res = git_clone_uninstall(install_files)

    if res:
        print(f"***自定义节点 {install_name} 卸载成功***")
        return web.json_response({'status': '卸载成功'}, content_type='application/json')

    return web.Response(status=400, text='卸载失败')


# 更新节点
@server.PromptServer.instance.routes.post('/service/node/update')
async def update_node(request):
    json_data = await request.json()
    install_name = json_data['title']
    install_files = json_data['files']
    install_type = json_data['install_type']

    print(f"***更新自定义节点 {install_name} ***")
    res = False

    if install_type == 'git-clone':
        res = git_clone_update(install_files)

    if res:
        print(f"***自定义节点 {install_name} 更新成功***")
        return web.json_response({'status': '更新成功'}, content_type='application/json')

    return web.Response(status=400, text='更新失败')


# 切换节点状态
@server.PromptServer.instance.routes.post('/service/node/toggle')
async def toggle_node(request):
    json_data = await request.json()
    install_name = json_data['title']
    install_files = json_data['files']
    install_type = json_data['install_type']
    is_disabled = json_data['install_status'] == 'Disabled'

    print(f"***切换自定义节点 {install_name} 状态***")
    res = False

    if install_type == 'git-clone':
        res = git_clone_set_active(install_files, not is_disabled)
    elif install_type == 'copy':
        res = copy_set_active(install_files, not is_disabled, json_data.get('js_path', None))

    if res:
        print(f"***自定义节点 {install_name} 状态切换成功***")
        return web.json_response({'status': '状态切换成功'}, content_type='application/json')

    return web.Response(status=400, text='状态切换失败')


# 获取节点映射
@server.PromptServer.instance.routes.get("/service/node/get_mappings")
async def fetch_customnode_mappings(request):
    url = get_config('channel_url') + '/extension-node-map.json'

    res = await fetch_data(url)

    return web.json_response(res, content_type='application/json')


# 获取节点更新
@server.PromptServer.instance.routes.get("/service/node/fetch_updates")
async def fetch_updates(request):
    try:
        url = get_config('channel_url') + '/custom-node-list.json'

        res = await fetch_data(url)
        check_nodes_installed(res, True)

        update_exists = any(
            'custom_nodes' in res and 'installed' in node and node['install_status'] == 'Update' for node in
            res['custom_nodes'])

        if update_exists:
            return web.Response(status=201)

        return web.Response(status=200)
    except Exception:
        return web.Response(status=400)


# ----------------------------------------------------------------------------------------------------------------------
# Comfy 管理
# ----------------------------------------------------------------------------------------------------------------------
# 更新 Comfy 本体
@server.PromptServer.instance.routes.get("/service/update_comfy")
async def update_comfy(request):
    print("***更新 Comfy***")

    try:
        repo_path = comfy_path
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"Comfy 更新失败: 当前 Comfy 不是从 git 仓库中安装的")
            return web.Response(status=400)

        repo = git.Repo(repo_path)
        current_branch = repo.active_branch
        branch_name = current_branch.name

        remote_name = 'origin'
        remote = repo.remote(remote_name)
        remote.fetch()

        commit_hash = repo.head.commit.hexsha
        remote_commit_hash = repo.commit(f'{remote_name}/{branch_name}').hexsha

        if commit_hash != remote_commit_hash:
            git_pull(repo_path)
            execute_install_script("ComfyMC", repo_path)
            return web.Response(status=201)
        else:
            return web.Response(status=200)

    except Exception as e:
        print(f"Comfy 更新失败: {e}")
        pass

    return web.Response(status=400)


# ----------------------------------------------------------------------------------------------------------------------
# Model 预览
# ----------------------------------------------------------------------------------------------------------------------
@server.PromptServer.instance.routes.get("/view_model/{type}")
async def view_model(request):
    type_name = request.match_info.get("type", None)
    if type_name is None:
        return web.Response(status=404)
    if not "filename" in request.rel_url.query:
        return web.Response(status=404)

    filename = request.rel_url.query["filename"]
    model_path = folder_paths.get_full_path(type_name, filename)
    if model_path is None:
        return web.Response(status=404)

    model_path = os.path.splitext(model_path)[0]
    for ext in ['png', 'jpg', 'webp', 'gif']:
        for appendix in ['', '_preview.', 'preview', 'previews.']:
            img_path = model_path + '.' + appendix + ext
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    return web.Response(body=f.read(), content_type=f'image/{ext}')
    return web.Response(status=404)


NODE_CLASS_MAPPINGS = NODE_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = NODE_NAME_MAPPINGS
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
