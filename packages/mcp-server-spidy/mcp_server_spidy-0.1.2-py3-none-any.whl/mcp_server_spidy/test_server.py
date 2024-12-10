import pytest
import asyncio
from mcp_server_spidy.server import crawl_website

@pytest.mark.asyncio
async def test_crawl_website(mocker):
    mock_arguments = {
        "url": "http://example.com",
        "output_file": "output.txt"
    }

    mock_response = mocker.patch("aiohttp.ClientSession.get")
    mock_response.return_value.__aenter__.return_value.status = 200
    mock_response.return_value.__aenter__.return_value.text = asyncio.Future()
    mock_response.return_value.__aenter__.return_value.text.set_result("<html></html>")

    with mocker.patch("builtins.open", mocker.mock_open()) as mock_file:
        result = await crawl_website(mock_arguments)

    assert result[0].text == "Crawled http://example.com and saved results to output.txt"
    mock_file.assert_called_once_with("output.txt", 'w')
    mock_file().write.assert_called_once_with("<html></html>") 