import os
import time
from functools import wraps


def retry(exceptions, tries=5, delay=1):
    """
    重试装饰器，当函数抛出指定的异常时，自动重试。
    :param exceptions: 触发重试的异常类型
    :param tries: 最大重试次数
    :param delay: 初始延迟时间
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"警告：{func.__name__} - {e}, 正在重试...")
                    time.sleep(mdelay)
                    mtries -= 1
            return func(*args, **kwargs)
        return wrapper
    return decorator


@retry(Exception, tries=10, delay=1)
def get_connected_project_name_info(client):
    """
    获取当前 Wwise 工程名称
    """
    try:
        result_wwise_version = client.call("ak.wwise.core.getInfo")
        result_project_name = client.call("ak.wwise.core.object.get", {"from": {"ofType": ["Project"]}})

        if 'version' in result_wwise_version and 'return' in result_project_name:
            wwise_version = result_wwise_version['version']['displayName'].replace("v", "Wwise ")
            project_name = result_project_name['return'][0]['name']
            print(f"成功获取项目信息: {project_name} - {wwise_version}")
            return project_name, wwise_version
        else:
            raise ValueError("获取项目信息失败： Wwise Authoring 可能正在初始化...")
    except Exception as e:
        print(f"调用 ak.wwise.core.getProjectInfo 时出错: {e}")
        raise


@retry(Exception, tries=10, delay=1)
def get_object(client, object_path):
    """
    获取 Wwise 对象信息
    """
    try:
        args = {
            "from": {
                "path": [object_path]
            }
        }
        result = client.call("ak.wwise.core.object.get", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.get 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def get_object_waql(client, waql):
    """
    获取 Wwise 对象信息
    """
    try:
        args = {
            "waql": waql
        }
        result = client.call("ak.wwise.core.object.get", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.get 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def get_selected_objects(client):
    """
    获取当前 Wwise 工程选中的对象
    """
    try:
        opts = {
            "return": [
                "id",
                "name",
                "type",
                "path",
                "RandomOrSequence",
            ]
        }
        result = client.call("ak.wwise.ui.getSelectedObjects", options=opts)
        if 'objects' in result:
            # 分离 RandomOrSequence 类型
            for obj in result['objects']:
                if 'RandomOrSequence' in obj:
                    obj['type'] = 'SequenceContainer' if obj['RandomOrSequence'] == 0 else 'RandomContainer'
            return result
        else:
            return None
    except Exception as e:
        print(f"调用 ak.wwise.ui.getSelectedObjects 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def create_object(client, object_type, parent_path, object_name, on_name_conflict="merge", children=None, output_bus=None):
    """
    创建 Wwise 对象
    """
    try:
        args = {
            "parent": parent_path,
            "type": object_type,
            "name": object_name,
            "onNameConflict": on_name_conflict,
        }
        if children:
            args["children"] = children
        if output_bus:
            args["@OutputBus"] = output_bus
            args['@OverrideOutput'] = True
        result = client.call("ak.wwise.core.object.create", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.create 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def set_object(client, objects):
    """
    设置 Wwise 对象属性
    """
    try:
        args = {
            "objects": []
        }
        for obj in objects:
            arg = {}
            for key, value in obj.items():
                arg[key] = value
            args["objects"].append(arg)
        result = client.call("ak.wwise.core.object.set", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.setProperty 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def set_soundbank_inclusion(client, soundbank, obj, operation="add", inclusions_filter=None):
    """
    设置 SoundBank 包含的对象
    """
    try:
        if inclusions_filter is None:
            inclusions_filter = [
                "events",
                "structures",
                "media"
            ]
        args = {
            "soundbank": soundbank,
            "operation": operation,
            "inclusions": [
                {
                    "object": obj,
                    "filter": inclusions_filter
                }
            ]
        }
        result = client.call("ak.wwise.core.soundbank.setInclusions", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.soundbank.setInclusions 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def import_audio_file(client, **kwargs):
    """
    导入音频文件到 Wwise
    """
    try:
        args = {
            "importOperation": "useExisting",
            "default": {
                "importLanguage": kwargs.get("importLanguage", "")
            },
            "imports": [
                {
                    "audioFile": kwargs.get("audioFile", ""),
                    "originalsSubFolder": kwargs.get("originalsSubFolder", ""),
                    "objectPath": kwargs.get("objectPath", "")
                }
            ]
        }
        if kwargs.get("isLoopingEnabled", False):
            args["imports"][0]["@IsLoopingEnabled"] = True
        if kwargs.get("notes", ""):
            args["imports"][0]["notes"] = kwargs.get("notes", "")
        result = client.call("ak.wwise.core.audio.import", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.audio.import 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def get_wwise_originals_sfx_path(client):
    """
    获取 Wwise Originals 文件夹路径
    """
    try:
        result = client.call("ak.wwise.core.getProjectInfo")
        if 'directories' in result:
            originals_path = result['directories']['originals']
            return os.path.join(originals_path, "SFX")
        else:
            raise ValueError("获取 Wwise Originals 文件夹路径失败")
    except Exception as e:
        print(f"调用 ak.wwise.core.getProjectInfo 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def add_switch_assignment(client, child, stateOrSwitch):
    """
    添加 Switch Assignment
    """
    try:
        args = {
            "child": child,
            "stateOrSwitch": stateOrSwitch
        }
        result = client.call("ak.wwise.core.switchContainer.addAssignment", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.switchContainer.addAssignment 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def copy_object(client, obj, parent, on_name_conflict="rename"):
    """
    复制 Wwise 对象
    """
    try:
        args = {
            "object": obj,
            "parent": parent,
            "onNameConflict": on_name_conflict
        }
        result = client.call("ak.wwise.core.object.copy", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.copy 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def move_object(client, obj, parent, on_name_conflict="rename"):
    """
    移动 Wwise 对象
    """
    try:
        args = {
            "object": obj,
            "parent": parent,
            "onNameConflict": on_name_conflict
        }
        result = client.call("ak.wwise.core.object.move", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.move 时出错: {e}")
        return None


@retry(Exception, tries=10, delay=1)
def set_name(client, obj, name):
    """
    设置 Wwise 对象名称
    """
    try:
        args = {
            "object": obj,
            "value": name
        }
        result = client.call("ak.wwise.core.object.setName", args)
        return result
    except Exception as e:
        print(f"调用 ak.wwise.core.object.setName 时出错: {e}")
        return None
