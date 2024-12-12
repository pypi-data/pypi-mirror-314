class Config:
    """
    Model for initing client
    """

    def __init__(
        self,
        token: str = None,
        call_token: str = None,
        endpoint: str = None,
        region: str = None,
    ):
        self.token = token
        self.call_token = call_token
        self.endpoint = endpoint
        self.region = region


class BaseRequest:
    """
    Model for BaseRequest
    """

    def __init__(self):
        self.api = None
        self.method = None
        self.content_type = None
        self.payload = None


class BaseResponse:
    """
    Model for BaseResponse
    """

    def __init__(
        self, code: int = None, data: dict = None, message: str = None, **kwargs
    ):
        self.code = code
        self.data = data
        self.message = message


class TestRequest(BaseRequest):

    def __init__(self):
        super().__init__()
        self.api = '/v1/audio-language-detection/test'
        self.method = 'POST'
        self.content_type = 'application/json'
        self.payload = {}


class TestResponse(BaseResponse):

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )


class AudioLanguageDetectionRequest(BaseRequest):
    """
    Model for AudioLanguageDetectionRequest

    语种识别服务提供全球137种语言的语种识别，帮助您快速判断音频所属语言。结合机器翻译服务，可通过自动的语种识别，快速定位需要翻译的内容，有效提升整体效率。
    """

    def __init__(self, audio: str = None, metadata: dict = None):
        """
        Args:
            audio: 音频文件的本地路径，长度需在5s以内，支持WAV、PCM
            metadata: 音频文件的额外元数据，如音频采样率
        """

        self.audio = audio
        self.metadata = metadata
        self._audio_binary = None

        with open(self.audio, 'rb') as f:
            self._audio_binary = f.read()

        super().__init__()
        self.api = '/v1/audio-language-detection'
        self.method = 'POST'
        self.content_type = 'application/json'
        self.payload = {'audio': self._audio_binary, 'metadata': self.metadata}


class AudioLanguageDetectionResponse(BaseResponse):
    """
    Model for AudioLanguageDetectionResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )


class TranslateTextRequest(BaseRequest):
    """
    Model for TranslateTextRequest

    文本翻译服务提供全球137种语言的文本翻译，支持多种语言间的互译，帮助您快速实现多语言间的文本翻译。
    """

    def __init__(self, text: list = None, source: str = None, target: str = None):
        """
        Args:
            text: list[str] 待翻译的文本
            source: 源语言
            target: 目标语言
        """

        self.text = text
        self.source = source
        self.target = target

        super().__init__()
        self.api = f'/v1/translate/{source}/{target}'
        self.method = 'POST'
        self.content_type = 'application/json'
        self.payload = {'text': self.text}


class TranslateTextResponse(BaseResponse):
    """
    Model for TranslateTextResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )


class ASRRequest(BaseRequest):
    """
    Model for ASRRequest

    语音识别提供高准确率、低时延的语音转文字服务，包含实时语音识别、一句话识别和录音文件识别等多款产品。适用于智能客服、质检、会议纪要、实时字幕等多个企业应用场景。
    """

    def __init__(
        self,
        language: str = None,
        audio_url: str = None,
    ):
        """
        Args:
            language: 语种
            audio_url: 音频文件地址
        """

        self.language = language
        self.audio_url = audio_url

        super().__init__()
        self.api = f'/recognition'
        self.method = 'POST'
        self.content_type = 'application/json'
        # self.payload = {'audio_url': self.audio_url}


class ASRResponse(BaseResponse):
    """
    Model for ASRResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )


# TODO: Implement TTSRequest and TTSResponse
# class TTSRequest(BaseRequest):
#     """
#     Model for TTSRequest
#
#     语音合成服务提供多种音色、多种音频格式的语音合成服务，支持多种语言的语音合成，帮助您快速实现多语言的语音合成。
#     """
#
#     def __init__(self, text: str = None, language: str = None, voice: str = None):
#         """
#         Args:
#             text:
#             language:
#             voice:
#         """
#
#             self.text = text
#             self.language = language
#             self.voice = voice
#
#             super().__init__()
#             self.api = f'/v1/tts/{language}/{voice}'
#             self.method = 'POST'
#             self.content_type = 'application/json'
#             self.payload = {'text': self.text}
#
# class TTSResponse(BaseResponse):
#     """
#     Model for TTSResponse
#     """
#
#     def __init__(self, response: BaseResponse = None, **kwargs):
#         super().__init__(
#             code=response.code if response else None,
#             data=response.data if response else None,
#             message=response.message if response else None,
#             **kwargs,
#         )
