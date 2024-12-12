**AI云平台SDK**

这是第四范式提供的AI云平台SDK。通过该sdk可以调用AI云平台提供的各种模型服务。

## 安装

```shell
pip install websockets==10.4
pip install ai-cloud-sdk-4pd
```

## 使用

```python

import ai_cloud_sdk_4pd.client as ai_cloud_sdk_4pd_client
import ai_cloud_sdk_4pd.models as ai_cloud_sdk_4pd_models

count = 0


async def on_ready():
    print('ready')


async def on_response(response):
    global count
    print('-------------------------------------')
    print(count)
    count += 1
    print(response)


async def on_completed():
    print('completed')


async def test_asr():
    print('-------------test asr flow-------------')
    token = 'your token'
    call_token = 'your call token'
    region = 'China'
    config = ai_cloud_sdk_4pd_models.Config(
        token=token,
        call_token=call_token,
        region=region,
    )
    client = ai_cloud_sdk_4pd_client.Client(config=config)
    request = ai_cloud_sdk_4pd_models.ASRRequest(
        audio_url='your local audio file path',
        language='zh',
    )

    await client.asr_ws_send(
        request=request,
        on_ready=on_ready,
        on_response=on_response,
        on_completed=on_completed,
    )
    print('---------------------------------')


if __name__ == '__main__':
    import asyncio

    asyncio.get_event_loop().run_until_complete(test_asr())

```

