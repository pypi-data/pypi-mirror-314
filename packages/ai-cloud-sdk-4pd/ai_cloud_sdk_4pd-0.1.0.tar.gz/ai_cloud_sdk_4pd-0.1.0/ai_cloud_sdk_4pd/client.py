import base64
import json

import requests
import websockets

from ai_cloud_sdk_4pd import models as ai_cloud_sdk_4pd_models


class Client:
    def __init__(
        self,
        config: ai_cloud_sdk_4pd_models.Config,
    ):
        self._token = config.token
        self._call_token = config.call_token
        self._endpoint = config.endpoint
        self._region = config.region
        self.blacklist_token = []
        self.blacklist_call_token = []

        # 设置region和endpoint
        self._endpoint_map = {
            'China': '172.27.231.79:506/ai/cpp/api',
            # 'China': 'localhost:8090/ai/cpp/api',
            'HongKong': 'https://Hongkong.com',
            'Other': 'https://Other.com',
        }
        self.__set_region_and_endpoint()
        self.__verify_tokens()

    def __set_region_and_endpoint(self) -> None:
        # 如果endpoint已给出且合法，则直接返回
        if self._endpoint and self._endpoint in self._endpoint_map.values():
            self._region = [
                k for k, v in self._endpoint_map.items() if v == self._endpoint
            ][0]
            return

        # 如果endpoint未给出或不合法，且region存在且合法，则根据region确定endpoint
        if self._region and self._region in self._endpoint_map.keys():
            self._endpoint = self._endpoint_map[self._region]
            return

        # 如果endpoint未给出或不合法，且region不存在或不合法，则默认endpoint(China)
        self._region = 'China'
        self._endpoint = self._endpoint_map[self._region]
        return

    def __verify_tokens(self) -> None:
        # 如果token或call_token未给出，则抛出异常
        if self._token is None or self._call_token is None:
            raise ValueError('token and call_token is required')

    def send(
        self,
        request: ai_cloud_sdk_4pd_models.BaseRequest = None,
    ) -> ai_cloud_sdk_4pd_models.BaseResponse:

        # 如果token或call_token在黑名单中，则抛出异常
        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f'http://{self._endpoint}{request.api}'
        headers = {
            'token': self._token,
            'call_token': self._call_token,
            'content-type': request.content_type,
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            json=request.payload,
        )

        # 如果返回码为503，则将token和call_token加入黑名单
        if response.json().get('code', None) == 503:
            self.blacklist_token.append(self._token)
            self.blacklist_call_token.append(self._call_token)
            raise ValueError('token or call_token is invalid')

        return ai_cloud_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )

    async def asr_ws_send(
        self,
        request: ai_cloud_sdk_4pd_models.ASRRequest = None,
        on_ready: callable = None,
        on_response: callable = None,
        on_completed: callable = None,
    ) -> None:

        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f"ws://{self._endpoint.split('/')[0]}{request.api}"
        headers = {
            'token': self._token,
            'call_token': self._call_token,
        }
        # 设置 ping 的超时时间和 ping 的间隔
        ping_timeout = 120  # 秒
        ping_interval = 5  # 秒
        close_timeout = 60  # 当尝试关闭连接时，等待关闭帧的最长时间（秒）
        async with websockets.connect(
            full_url,
            extra_headers=headers,
            ping_timeout=ping_timeout,
            ping_interval=ping_interval,
            close_timeout=close_timeout,
        ) as websocket:
            #  把wav文件进行base64编码
            file_url = request.audio_url
            try:
                with open(file_url, 'rb') as f:
                    audio_data = f.read()
                    audio_base64 = base64.b64encode(audio_data)
                    audio_base64 = audio_base64.decode('utf-8')
            except FileNotFoundError:
                raise ValueError('File not found. Please check the path and try again.')

            # 发送音频数据
            message = {
                "enableWords": True,
                "lang": "zh",
                "waitTime": 5,
                "chunkSize": 1024,
                "fileBase64": str(audio_base64),
            }

            if (
                self._token in self.blacklist_token
                or self._call_token in self.blacklist_call_token
            ):
                raise ValueError('token or call_token is forbidden to send request')
            await websocket.send(json.dumps(message))

            # 4. 接收返回数据
            try:
                while websocket.open:
                    if (
                        self._token in self.blacklist_token
                        or self._call_token in self.blacklist_call_token
                    ):
                        raise ValueError(
                            'token or call_token is forbidden to send request'
                        )

                    recv_data = await websocket.recv()
                    if isinstance(recv_data, str):
                        recv_data = str(recv_data)
                        recv_data = json.loads(recv_data)

                        if recv_data.get('success', False):
                            await on_ready()
                            continue

                        if recv_data.get('code', None) == 503:
                            self.blacklist_token.append(self._token)
                            self.blacklist_call_token.append(self._call_token)
                            raise ValueError('token or call_token is invalid')

                        if recv_data.get('end', False):
                            await on_completed()
                            break

                        await on_response(recv_data)

                    else:
                        raise Exception("Received data is not str")

            except Exception as e:
                raise e
            finally:
                if not websocket.closed:
                    await websocket.close()
