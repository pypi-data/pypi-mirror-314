import asyncio
from unittest.mock import MagicMock, Mock, patch

import pytest

from kelvin.application import KelvinApp
from kelvin.krn import KRNAssetDataStream
from kelvin.message import Number


# Workaround for python3.7; for python >= 3.8 we could just use:
# from unittest.mock import AsyncMock
class AsyncMock(Mock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class MockStream:
    connected = False

    def __init__(self, config=None, data: list = []) -> None:
        self.mock_data: list = data
        pass

    async def connect(self):
        if len(self.mock_data) > 0:
            self.connected = True
        else:
            raise ConnectionError()

    async def disconnect(self):
        self.connected = False

    async def read(self):
        await asyncio.sleep(0.1)
        try:
            return self.mock_data.pop(0)
        except IndexError:
            raise ConnectionError()

    async def write(self, msg) -> bool:
        return True


@pytest.mark.asyncio
@patch("kelvin.application.client.KelvinStream")
async def test_connect_disconnect(streamMock: MagicMock):
    streamMock.return_value = MockStream(data=[Number(payload=1, resource=KRNAssetDataStream("foo", "bar"))])

    on_connect = AsyncMock()
    on_disconnect = AsyncMock()

    cli = KelvinApp()

    event = asyncio.Event()
    event.set()
    mock_wait = Mock(side_effect=lambda: event.wait())
    cli.config_received.wait = mock_wait

    # hack for python3.7. can't make @patch work on it
    cli._stream = MockStream(data=[Number(payload=1, resource=KRNAssetDataStream("foo", "bar"))])

    cli.on_connect = on_connect
    cli.on_disconnect = on_disconnect
    await cli.connect()
    await asyncio.sleep(0.1)
    await cli.disconnect()

    on_connect.assert_called_once()
    on_disconnect.assert_called_once()
