from urllib.parse import urlsplit
from json import dumps
import asyncio
import gzip
import zlib

async def http_request(url, method="GET", headers=None, content=None, json=None, connect_timeout=10):
    if not headers:
        headers = {}
    if json:
        content = dumps(json).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if content:
        headers["Content-Length"] = str(len(content))

    url = urlsplit(url)
    req = f"{method.upper()} {url.path or '/'} HTTP/1.1\r\n"
    req += f"Host: {url.netloc}\r\n"
    req += f"Accept-Encoding: gzip, deflate\r\n"
    for k, v in headers.items():
        req += f"{k}: {v}\r\n"
    req += "\r\n"

    if url.scheme == "https":
        fut = asyncio.open_connection(url.hostname, url.port or 443, ssl=True)
    else:
        fut = asyncio.open_connection(url.hostname, url.port or 80)

    reader, writer = await asyncio.wait_for(fut, timeout=connect_timeout)

    writer.write(req.encode("ascii"))
    if content:
        writer.write(content)
    await writer.drain()

    line = await reader.readline()
    if not line:
        raise BrokenPipeError()
    try:
        status = int(line.split(b" ")[1])
    except Exception as e:
        raise Exception(f"Invalid data {line!r}")

    res_headers = {}
    while True:
        line = await reader.readline()
        if line == b"\r\n":
            break
        elif not line:
            raise BrokenPipeError()
        k, v = line.decode("ascii").split(":", 1)
        res_headers[k.lower()] = v.strip()

    res_data = b""
    if res_headers.get("transfer-encoding") == "chunked":
        while True:
            line = await reader.readline()
            if len(line) == 0:
                raise BrokenPipeError()
            if not line.endswith(b"\r\n"):
                raise Exception("Unexpected end of chunked data")
            size = int(line, 16)
            res_data += (await reader.readexactly(size + 2))[:-2]
            if size == 0:
                break
    elif "content-length" in res_headers:
        size = int(res_headers["content-length"])
        res_data = await reader.readexactly(size)

    content_encoding = res_headers.get("content-encoding")
    if content_encoding == "gzip":
        res_data = gzip.decompress(res_data)
    elif content_encoding == "deflate":
        res_data = zlib.decompress(res_data)

    return {
        "headers": res_headers,
        "status": status,
        "data": res_data,
    }
