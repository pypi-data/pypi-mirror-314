import base64
import json
from io import BytesIO
from typing import Optional
from urllib.parse import quote

import websockets
from PIL import Image

from orign.config import GlobalConfig
from orign.models import (
    EmbeddingRequest,
    EmbeddingResponse,
    ErrorResponse,
    ModelReadyResponse,
)


class AsyncEmbeddingModel:
    def __init__(
        self,
        model: Optional[str] = None,
        provider: Optional[str] = None,
    ):
        config = GlobalConfig.read()
        self.model = model
        self.provider = provider
        self.orign_host = config.server.strip("http://").strip("https://")
        self.websocket = None

        # Construct the WebSocket URL
        self.ws_url = f"wss://{self.orign_host}/v1/embedding/stream"
        params = []
        if self.model:
            params.append(f"model={quote(self.model)}")
        if self.provider:
            params.append(f"provider={quote(self.provider)}")

        if params:
            self.ws_url += "?" + "&".join(params)

    async def connect(self):
        """Establish WebSocket connection if not already connected"""
        if not self.websocket:
            config = GlobalConfig.read()
            headers = {"Authorization": f"Bearer {config.api_key}"}
            self.websocket = await websockets.connect(
                self.ws_url, extra_headers=headers
            )

    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def embed(
        self,
        text: Optional[str] = None,
        image: Optional[str | Image.Image] = None,
    ) -> EmbeddingResponse:
        await self.connect()

        if isinstance(image, Image.Image):
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image = "data:image/png;base64," + base64.b64encode(
                buffered.getvalue()
            ).decode("utf-8")

        request = EmbeddingRequest(
            text=text, image=image, model=self.model, provider=self.provider
        )

        if not self.websocket:
            raise ConnectionError("WebSocket connection not established")

        await self.websocket.send(request.model_dump_json())

        try:
            while True:
                response = await self.websocket.recv()
                response_data = json.loads(response)

                if response_data.get("type") == EmbeddingResponse.__name__:
                    resp = EmbeddingResponse.model_validate(response_data)
                    return resp
                elif response_data.get("type") == ModelReadyResponse.__name__:
                    ready = ModelReadyResponse.model_validate(response_data)
                    if not ready.ready:
                        raise ValueError(f"Model not ready: {ready.error}")
                elif response_data.get("type") == ErrorResponse.__name__:
                    error = ErrorResponse.model_validate(response_data)
                    raise ValueError(f"Error: {error.error}")
                else:
                    raise ValueError(f"Unknown response type: {response_data}")

        except websockets.exceptions.ConnectionClosed:
            await self.close()
            raise ConnectionError("WebSocket connection closed unexpectedly")
