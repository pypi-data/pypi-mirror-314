import json
import yaml


def load_monitor_config(monitor_config):
    # convert yaml or json to dict
    if isinstance(monitor_config, str):
        if monitor_config.endswith('.json'):
            try:
                with open(monitor_config, "r") as file:
                    json_data = json.load(file)
                monitor_config = json_data
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}")
            except FileNotFoundError:
                print(f"找不到文件: {monitor_config}")
            except Exception as e:
                print(f"发生未知错误: {e}")
        elif monitor_config.endswith('.yaml'):
            try:
                with open(monitor_config, "r") as file:
                    yaml_data = yaml.safe_load(file)
                monitor_config = yaml_data
            except FileNotFoundError:
                print(f"找不到文件: {monitor_config}")
            except yaml.YAMLError as e:
                print(f"YAML 解析错误: {e}")
            except Exception as e:
                print(f"发生未知错误: {e}")
        else:
            print("不支持的文件格式，必须为 .json 或 .yaml")

    if isinstance(monitor_config, dict):
        return monitor_config
    else:
        return None
