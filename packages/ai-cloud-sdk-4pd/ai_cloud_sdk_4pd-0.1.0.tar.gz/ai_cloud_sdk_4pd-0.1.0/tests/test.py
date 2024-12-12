import ai_cloud_sdk_4pd.client as ai_cloud_sdk_4pd_client
import ai_cloud_sdk_4pd.models as ai_cloud_sdk_4pd_models


def test():
    print('-------------test client-------------')
    token = ''
    call_token = ''
    region = 'China'
    config = ai_cloud_sdk_4pd_models.Config(
        token=token,
        call_token=call_token,
        region=region,
    )
    client = ai_cloud_sdk_4pd_client.Client(config=config)
    request = ai_cloud_sdk_4pd_models.TranslateTextRequest(
        text=["hfdih"],
        source="en",
        target="zh",
    )
    response = client.send(request=request)
    print(request.payload)
    print(response.code)
    print(response.data)
    print(response.message)
    print('-------------------------------------')
