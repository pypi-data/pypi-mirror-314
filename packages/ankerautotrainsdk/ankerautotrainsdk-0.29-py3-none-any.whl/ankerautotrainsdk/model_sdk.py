import logging
from urllib.parse import urljoin
from typing import Optional, Dict, Any, List
import requests
import hashlib
import os
import json
import base64
from requests.exceptions import HTTPError, RequestException, ConnectionError, Timeout

# 配置日志（在模块级别配置一次即可）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AnkerAutoTrainModelSDK:
    def __init__(self, 
                 bg: str, 
                 owner: str, 
                 is_test_env: bool = True,  # True 表示测试环境，False 表示正式环境
                 url: Optional[str] = None,  # 用户自定义 URL
                 timeout: int = 10  # 默认超时时间（秒）
                ):
        """
        初始化 AnkerAutoTrainModelSDK 类，设置基础 URL、背景信息和所有者信息。

        :param bg: 背景信息
        :param owner: 所有者信息
        :param is_test_env: 是否使用正式环境，True 表示测试环境，False 表示正式环境
        :param url: 自定义 URL，如果提供，将覆盖 is_test_env 的默认 URL
        :param timeout: 请求超时时间（秒）
        """
        # 定义正式环境和测试环境的 URL
        default_urls = {
            False: 'https://aidc-us.anker-in.com',  # 正式环境
            True: 'https://aidc-dev.anker-in.com'  # 测试环境
        }

        # 优先使用自定义 URL，否则根据环境布尔值选择默认 URL
        self.url = url.rstrip('/') if url else default_urls[is_test_env]
        
        # 存储背景信息和所有者
        self.bg = bg
        self.owner = owner

        # 存储默认超时时间
        self.timeout = timeout

        # 获取类级别的日志记录器
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 初始化会话和头信息
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })


    def calculate_md5(self, file_path: str) -> str:
        """
        计算文件的 Base64 编码的 MD5 校验和。

        :param file_path: 文件路径
        :return: Base64 编码的 MD5 校验和
        """
        md5_hash = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            md5_digest = md5_hash.digest()
            md5_b64 = base64.b64encode(md5_digest).decode('utf-8')
            self.logger.debug(f"计算文件 {file_path} 的 MD5 校验和: {md5_b64}")
            return md5_b64
        except FileNotFoundError:
            self.logger.error(f"未找到文件: {file_path}")
            raise
        except Exception as e:
            self.logger.error(f"计算文件 MD5 时发生错误: {e}")
            raise

    def get_url(
        self, 
        model_name: str, 
        model_version_name: str, 
        path: str, 
        url_type: str, 
        bg: Optional[str] = None, 
        owner: Optional[str] = None, 
    ) -> Optional[str]:
        """
        获取上传或下载文件的 URL。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param path: 文件路径
        :param url_type: URL 类型（'upload' 或 'download'）
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :param interface: API 端点接口
        :return: URL 字符串或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        interface = '/api/model/internal/getUploadUrl'
        url_interface = urljoin(self.url + '/', interface.lstrip('/'))
        self.logger.info(f"请求的接口 URL: {url_interface}")

        payload = {
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersionName": model_version_name,
            "type": url_type,
            "path": path
        }
        self.logger.debug(f"获取 URL 的请求体: {json.dumps(payload, indent=4, ensure_ascii=False)}")

        try:
            response = self.session.post(url_interface, json=payload, timeout=self.timeout)
            response.raise_for_status()
            response_data = response.json()
            self.logger.debug(f"获取 URL 的响应: {json.dumps(response_data, indent=4, ensure_ascii=False)}")

            if response_data.get('ok'):
                url = response_data.get('data')
                if url:
                    self.logger.info(f"获取到的 URL: {url}")
                    return url
                else:
                    self.logger.warning("响应中未找到 URL。")
                    return None
            else:
                self.logger.error(f"获取 URL 失败: {response_data.get('msg', '未提供消息')}")
                return None
        except HTTPError as http_err:
            self.logger.error(f"获取 URL 时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return None
        except RequestException as req_err:
            self.logger.error(f"获取 URL 时发生请求异常: {req_err}")
            return None
        except ValueError:
            self.logger.error("获取 URL 时无法解析 JSON 响应。")
            return None
        except Exception as e:
            self.logger.error(f"获取 URL 时发生未知错误: {e}")
            return None

    def upload_file(self, upload_url: str, file_path: str) -> bool:
        """
        上传文件到指定的 URL，添加 MD5 校验。

        :param upload_url: 上传的目标 URL
        :param file_path: 本地文件路径
        :return: 如果上传成功返回 True，否则返回 False
        """
        self.logger.info(f"开始上传文件到: {upload_url}")
        try:
            md5_value = self.calculate_md5(file_path)
            with open(file_path, 'rb') as file:
                headers = {
                    'Content-Type': 'application/octet-stream',
                    'Content-MD5': md5_value
                }
                response = self.session.put(upload_url, data=file, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                self.logger.info(f"文件成功上传到 {upload_url}")
                return True
        except FileNotFoundError:
            self.logger.error(f"未找到文件: {file_path}")
            return False
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else '未知状态码'
            self.logger.error(f"上传文件时发生 HTTP 错误: {http_err} - 状态码: {status_code}")
            return False
        except RequestException as req_err:
            self.logger.error(f"上传文件时发生请求异常: {req_err}")
            return False
        except Exception as e:
            self.logger.error(f"上传文件时发生未知错误: {e}")
            return False

    def upload_model_file(self, 
                          model_name: str, 
                          model_version_name: str, 
                          file_path: str,
                          bg: Optional[str] = None, 
                          owner: Optional[str] = None
                         ) -> Optional[str]:
        """
        上传模型文件并返回上传的 URL。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param file_path: 本地文件路径
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: 上传 URL 或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        file_name = os.path.basename(file_path)
        upload_url = self.get_url(
            model_name=model_name, 
            model_version_name=model_version_name, 
            path=file_name, 
            url_type="upload",
            bg=bg,
            owner=owner
        )
        if not upload_url:
            self.logger.error("无法获取上传 URL，文件上传中止。")
            return None

        success = self.upload_file(upload_url, file_path)
        if success:
            self.logger.info(f"文件上传成功。上传 URL: {upload_url}")
            return upload_url
        else:
            self.logger.error("文件上传失败。")
            return None

    def download_model_file(self, 
                            model_name: str, 
                            model_version_name: str, 
                            file_path: str, 
                            save_to: str,
                            bg: Optional[str] = None, 
                            owner: Optional[str] = None
                           ) -> bool:
        """
        获取模型文件的下载链接并将文件下载到本地。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param file_path: 服务器上的文件路径
        :param save_to: 本地保存路径
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: 如果下载成功返回 True，否则返回 False
        """
        bg = bg or self.bg
        owner = owner or self.owner

        download_url = self.get_url(
            model_name=model_name,
            model_version_name=model_version_name,
            path=os.path.basename(file_path),
            url_type="download",
            bg=bg,
            owner=owner,
        )
        if not download_url:
            self.logger.error("无法获取下载 URL，文件下载中止。")
            return False

        self.logger.info(f"开始下载文件从: {download_url} 到 {save_to}")
        try:
            response = self.session.get(download_url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            with open(save_to, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            self.logger.info(f"文件成功下载并保存到 {save_to}")
            return True
        except HTTPError as http_err:
            self.logger.error(f"下载模型文件时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return False
        except RequestException as req_err:
            self.logger.error(f"下载模型文件时发生请求异常: {req_err}")
            return False
        except Exception as e:
            self.logger.error(f"下载模型文件时发生未知错误: {e}")
            return False

    def download_file(self, url: str, local_path: str) -> bool:
        """
        从指定的 URL 下载文件并保存到本地路径。

        :param url: 文件的 URL
        :param local_path: 本地保存路径
        :return: 如果下载成功返回 True，否则返回 False
        """
        self.logger.info(f"开始从 URL 下载文件: {url}")
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            with open(local_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            self.logger.info(f"文件成功下载到 {local_path}")
            return True
        except HTTPError as http_err:
            self.logger.error(f"下载文件时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return False
        except RequestException as req_err:
            self.logger.error(f"下载文件时发生请求异常: {req_err}")
            return False
        except Exception as e:
            self.logger.error(f"下载文件时发生未知错误: {e}")
            return False

    def get_model_list(
        self, 
        model_name: Optional[str] = None, 
        model_version_name: Optional[str] = None, 
        bg: Optional[str] = None, 
        owner: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        获取模型列表。

        :param model_name: 模型名称（可选）
        :param model_version_name: 模型版本名称（可选）
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: API 响应的字典或 None
        """
        bg = bg if bg is not None else str(self.bg )
        owner = owner if owner is not None else self.owner

        url = f"{self.url}/api/model/internal/version/list"
        # payload = { 
        #     "bg": "zx",
        #     "owner": "wenxiang",
        #     "modelName": "multi_det",
        #     "modelVersion": "20241211_01534191"
        # }
        payload = { 
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name
        }
        # 移除值为 None 的键
        payload = {k: v for k, v in payload.items() if v is not None}
        print(f"payload: {payload}")

        self.logger.info(f"请求获取模型列表的接口: {url}")
        self.logger.debug(f"获取模型列表的请求体: {json.dumps(payload, indent=4, ensure_ascii=False)}")

        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            response_data = response.json()
            self.logger.debug(f"获取模型列表的响应: {json.dumps(response_data, indent=4, ensure_ascii=False)}")
            return response_data
        except requests.HTTPError as http_err:
            self.logger.error(f"获取模型列表时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return None
        except requests.RequestException as req_err:
            self.logger.error(f"获取模型列表时发生请求异常: {req_err}")
            return None
        except json.JSONDecodeError as json_err:
            self.logger.error(f"解析响应 JSON 时发生错误: {json_err} - 响应内容: {response.text}")
            return None
        except Exception as e:
            self.logger.error(f"获取模型列表时发生未知错误: {e}")
            return None
        
        

    def get_model_id(self, 
                    model_name: str, 
                    model_version_name: str,
                    bg: Optional[str] = None, 
                    owner: Optional[str] = None
                   ) -> Optional[str]:
        """
        获取特定模型版本的 ID。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: 模型版本 ID 或 None
        """
        model_list = self.get_model_list(
            model_name=model_name, 
            model_version_name=model_version_name,
            bg=bg,
            owner=owner
        )
        if model_list and model_list.get('code') == 0 and model_list.get('data'):
            # 确保 'data' 是列表并包含 'modelVersionId'
            first_entry = model_list['data'][0]
            model_version_id = first_entry.get('modelVersionId')
            if model_version_id:
                self.logger.info(f"找到模型版本 ID: {model_version_id}")
                return model_version_id
            else:
                self.logger.warning(f"模型列表中的第一项未包含 'modelVersionId': {first_entry}")
                return None
        else:
            self.logger.warning(f"未找到模型 ID: {model_name} - {model_version_name}")
            return None

    def register_model(
        self,
        model_name: str, 
        model_version: str, 
        task_type: str, 
        model_arc: str,
        url_model_library: str, 
        url_data_base: str,
        optimizer: str,
        frame_type: str, 
        model_format: str, 
        learning_rate: float, 
        batch_size: int, 
        epochs: int, 
        img_size: int, 
        pulled_data_number: int,
        bg: Optional[str] = None, 
        owner: Optional[str] = None, 
        train_set_ids: Optional[List[str]] = None, 
        test_set_ids: Optional[List[str]] = None,
        united_training: Optional[Any] = None
    ) -> Optional[Dict[str, Any]]:
        """
        注册或更新模型版本信息。

        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :param model_name: 模型名称
        :param model_version: 模型版本名称
        :param task_type: 任务类型（例如：检测）
        :param model_arc: 模型架构（例如：yolov5）
        :param url_model_library: 模型库的 URL
        :param url_data_base: 数据库的 URL
        :param train_set_ids: 训练集 ID 列表
        :param test_set_ids: 测试集 ID 列表
        :param frame_type: 框架类型（默认：'pytorch'）
        :param model_format: 模型格式（默认：'onnx'）
        :param optimizer: 优化器（默认：'Adamw'）
        :param learning_rate: 学习率（默认：0.001）
        :param batch_size: 批大小（默认：32）
        :param epochs: 训练轮数（默认：10）
        :param img_size: 图片大小（默认：224）
        :param pulled_data_number: 拉取的数据数量（默认：0）
        :param united_training: 联合训练信息（可选）
        :return: API 响应的字典或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        endpoint = '/api/model/internal/version'
        url = urljoin(self.url + '/', endpoint.lstrip('/'))
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version,
            "modelType": task_type,
            "modelArc": model_arc,
            "url": url_model_library,
            "url_data_base": url_data_base,
            "pulledDataNumber": pulled_data_number,
            "trainSetIds": train_set_ids,
            "testSetIds": test_set_ids,
            "frameType": frame_type,
            "modelFormat": model_format,
            "optimizer": optimizer,
            "hyperParameter": {
                "learning_rate": learning_rate,
                "batch_size": batch_size,
                "epochs": epochs,
                "img_size": img_size
            }
        }

        if united_training is not None:
            payload["united_training"] = united_training

        # 移除值为 None 的键
        payload = {k: v for k, v in payload.items() if v is not None}
        self.logger.info("注册/更新模型版本的 payload:")
        self.logger.debug(json.dumps(payload, indent=4, ensure_ascii=False))

        try:
            response = self.session.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            self.logger.debug(f"注册/更新模型版本的响应: {json.dumps(data, indent=4, ensure_ascii=False)}")

            if data.get("ok"):
                self.logger.info("模型版本注册/更新成功。")
                return data
            else:
                self.logger.error(f"模型版本注册/更新失败: {data.get('msg', '未知错误')}")
                return data

        except HTTPError as http_err:
            self.logger.error(f"模型注册/更新时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
        except ConnectionError as conn_err:
            self.logger.error(f"模型注册/更新时发生连接错误: {conn_err}")
        except Timeout as timeout_err:
            self.logger.error(f"模型注册/更新时发生请求超时: {timeout_err}")
        except RequestException as req_err:
            self.logger.error(f"模型注册/更新时发生请求异常: {req_err}")
        except ValueError:
            self.logger.error("模型注册/更新时无法解析 JSON 响应。")
        except Exception as e:
            self.logger.error(f"模型注册/更新时发生未知错误: {e}")

        return None

    def add_model_to_db(
        self, 
        model_name: str, 
        model_version_name: str, 
        tar_md5: str, 
        onnx_md5: str, 
        rknn_md5: str, 
        model_arc: str, 
        region: str,
        test_result: Optional[List[Any]], 
        test_set_ids: Optional[List[str]], 
        train_set_ids: Optional[List[str]], 
        show: Optional[Any], 
        model_id: Optional[str] = None,
        quant_set_ids: Optional[List[str]] = None, 
        params: Optional[Any] = None, 
        bg: Optional[str] = None, 
        owner: Optional[str] = None, 
        task_type: str = 'detection', 
        desc: Optional[Any] = None, 
        code_id: Optional[Any] = None, 
        docker_image_id: Optional[Any] = None, 
        frame_type: str = 'pytorch', 
        model_format: str = 'onnx', 
        model_type: str = '目标检测',
        version_id: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        将模型信息添加到数据库。

        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param tar_md5: tar 文件的 MD5 校验和
        :param onnx_md5: onnx 文件的 MD5 校验和
        :param rknn_md5: rknn 文件的 MD5 校验和
        :param model_arc: 模型架构
        :param region: 区域信息
        :param model_id: 模型 ID（可选）
        :param test_result: 测试结果（可选）
        :param test_set_ids: 测试集 ID 列表（可选）
        :param train_set_ids: 训练集 ID 列表（可选）
        :param quant_set_ids: 量化集 ID 列表（可选）
        :param params: 参数（可选）
        :param show: 显示信息（可选）
        :param task_type: 任务类型（默认：'detection'）
        :param desc: 描述（可选）
        :param code_id: 代码 ID（可选）
        :param docker_image_id: Docker 镜像 ID（可选）
        :param frame_type: 框架类型（默认：'pytorch'）
        :param model_format: 模型格式（默认：'onnx'）
        :param model_type: 模型类型（默认：'目标检测'）
        :return: API 响应的字典或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        if model_id is None:
            version_id = self.get_model_id(
                model_name=model_name, 
                model_version_name=model_version_name,
                bg=bg,
                owner=owner
            )
            if version_id is None:
                self.logger.error("无法获取模型版本 ID，模型添加中止。")
                return None

        endpoint = '/api/model/internal/version/update'
        url = urljoin(self.url + '/', endpoint.lstrip('/'))

        payload = {
            "versionId": version_id,
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name,
            "region": region,
            "taskType": task_type,
            "modelArc": model_arc,
            "params": params,
            "testResult": test_result,
            "show": show,
            "trainSetIds": train_set_ids,
            "testSetIds": test_set_ids,
            "quantSetIds": quant_set_ids,
            "codeId": code_id,
            "dockerImageId": docker_image_id,
            "modelFile": {
                "tar": tar_md5,
                "onnx": onnx_md5,
                "rknn": rknn_md5
            },
            "modelDescription": desc,
            "modelType": model_type,
            "frameType": frame_type,
            "modelFormat": model_format
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        # self.logger.info(f"将模型添加到数据库的请求体: {json.dumps(payload, indent=4, ensure_ascii=False)}")
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            response_data = response.json()
            self.logger.debug(f"将模型添加到数据库的响应: {json.dumps(response_data, indent=4, ensure_ascii=False)}")
            return response_data
        except HTTPError as http_err:
            self.logger.error(f"将模型添加到数据库时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
        except RequestException as req_err:
            self.logger.error(f"将模型添加到数据库时发生请求异常: {req_err}")
        except ValueError:
            self.logger.error("将模型添加到数据库时无法解析 JSON 响应。")
        except Exception as e:
            self.logger.error(f"将模型添加到数据库时发生未知错误: {e}")

        return None

    def get_model_version_files(self, 
                                model_name: str, 
                                model_version_name: str,
                                bg: Optional[str] = None, 
                                owner: Optional[str] = None
                               ) -> Optional[List[Dict[str, Any]]]:
        """
        获取特定模型版本下的所有文件信息。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: 文件信息字典的列表或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        endpoint = '/api/model/internal/getDirectory'
        url = urljoin(self.url + '/', endpoint.lstrip('/'))
        payload = {
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersionName": model_version_name
        }

        self.logger.info(f"请求获取模型版本文件信息的接口: {url}")
        self.logger.debug(f"获取模型版本文件信息的请求体: {json.dumps(payload, indent=4, ensure_ascii=False)}")

        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            response_data = response.json()
            self.logger.debug(f"获取模型版本文件信息的响应: {json.dumps(response_data, indent=4, ensure_ascii=False)}")

            if response_data.get("code") == 0 and response_data.get("ok"):
                files = response_data["data"]["records"]
                self.logger.info(f"找到的文件总数: {len(files)}")
                for file in files:
                    self.logger.debug(f"名称: {file['name']}, 大小: {file['size']}, 最后修改: {file['lastModified']}")
                return files
            else:
                self.logger.error(f"获取模型版本文件信息失败: {response_data.get('msg', '未提供消息')}")
                return None

        except HTTPError as http_err:
            self.logger.error(f"获取模型版本文件信息时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return None
        except RequestException as req_err:
            self.logger.error(f"获取模型版本文件信息时发生请求异常: {req_err}")
            return None
        except ValueError:
            self.logger.error("获取模型版本文件信息时无法解析 JSON 响应。")
            return None
        except Exception as e:
            self.logger.error(f"获取模型版本文件信息时发生未知错误: {e}")
            return None

    def add_board_result_to_db(
        self, 
        model_name: str, 
        model_version_name: str, 
        board_result: List[Any], 
        chip: str, 
        test_set_ids: List[str], 
        input_h: int, 
        input_w: int, 
        infer_time: float, 
        memory: int, 
        flash: int, 
        project: str, 
        projectId: str, 
        modelPath: str, 
        boardTestVersion: str, 
        testResultPath: str, 
        bad_case_ids: List[str],
        model_id: Optional[str] = None,
        quant_algo: str = "normal", 
        quant_method: str = "channel",
        bg: Optional[str] = None, 
        owner: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        将板测试结果上传到数据库。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param board_result: 板测试结果
        :param chip: 芯片信息
        :param test_set_ids: 测试集 ID 列表
        :param input_h: 输入高度
        :param input_w: 输入宽度
        :param infer_time: 推理时间
        :param memory: 内存使用
        :param flash: 闪存大小
        :param project: 项目名称
        :param projectId: 项目 ID
        :param modelPath: 模型路径
        :param boardTestVersion: 板测试版本
        :param testResultPath: 测试结果路径
        :param bad_case_ids: 不良案例 ID 列表
        :param model_id: 模型 ID（可选）
        :param quant_algo: 量化算法（默认："normal"）
        :param quant_method: 量化方法（默认："channel"）
        :param bg: 背景信息（可选）
        :param owner: 所有者信息（可选）
        :return: API 响应的字典或 None
        """
        bg = bg or self.bg
        owner = owner or self.owner

        if model_id is None:
            model_id = self.get_model_id(
                model_name=model_name, 
                model_version_name=model_version_name,
                bg=bg,
                owner=owner
            )
            if model_id is None:
                self.logger.error(f"未找到模型 ID: {model_name} - {model_version_name}。跳过板测试结果上传。")
                return None

        endpoint = '/api/model/internal/versionTest'
        url = urljoin(self.url + '/', endpoint.lstrip('/'))
        
        payload = {
            "bg": bg,
            "owner": owner,
            "modelVersionId": model_id,
            "projectId": projectId,
            "projectName": project,
            "chipName": chip,
            "modelPath": modelPath,
            "boardTestVersion": boardTestVersion,
            "quantAlgo": quant_algo,
            "quantMethod": quant_method,
            "testResultBoard": board_result,
            "testResultPath": testResultPath,
            "testSetIds": test_set_ids,
            "badCaseIds": bad_case_ids,
            "inputH": input_h,
            "inputW": input_w,
            "inferTime": infer_time,
            "memory": memory,
            "flash": flash
        }

        # 移除值为 None 的键
        payload = {k: v for k, v in payload.items() if v is not None}
        
        # self.logger.info(f"上传板测试结果的请求体: {json.dumps(payload, indent=4, ensure_ascii=False)}")

        try:
            response = self.session.post(url, json=payload, timeout=30)  # 下载方法超时为30秒
            response.raise_for_status()
            response_data = response.json()
            self.logger.debug(f"上传板测试结果的响应: {json.dumps(response_data, indent=4, ensure_ascii=False)}")
            return response_data
        except HTTPError as http_err:
            self.logger.error(f"上传板测试结果时发生 HTTP 错误: {http_err} - 响应内容: {response.text}")
            return None
        except RequestException as req_err:
            self.logger.error(f"上传板测试结果时发生请求异常: {req_err}")
            return None
        except ValueError:
            self.logger.error("上传板测试结果时无法解析 JSON 响应。")
            return None
        except Exception as e:
            self.logger.error(f"上传板测试结果时发生未知错误: {e}")
            return None

