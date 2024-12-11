import asyncio
import base64
import os
from copy import deepcopy
from io import BytesIO
from mimetypes import guess_type

import aiohttp
import requests
from loguru import logger
from PIL import Image


def encode_base64_from_local_path(file_path, return_with_mime=True):
    """Encode a local file to a Base64 string, with optional MIME type prefix.
    """
    mime_type, _ = guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"
    with open(file_path, "rb") as file:
        base64_data = base64.b64encode(file.read()).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


async def encode_base64_from_url(url, session: aiohttp.ClientSession, return_with_mime=True):
    """Fetch a file from a URL and encode it to a Base64 string, with optional MIME type prefix.
    """
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        mime_type = response.headers.get("Content-Type", "application/octet-stream")
        base64_data = base64.b64encode(content).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


def encode_base64_from_pil(image: Image.Image, return_with_mime=True):
    """Encode a PIL image object to a Base64 string, with optional MIME type prefix.
    """
    buffer = BytesIO()
    image_format = image.format or "PNG"  # Default to PNG if format is unknown
    mime_type = f"image/{image_format.lower()}"
    image.save(buffer, format=image_format)
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.read()).decode("utf-8")
    if return_with_mime:
        return f"data:{mime_type};base64,{base64_data}"
    return base64_data


# deprecated
def encode_base64_from_url_slow(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")




async def encode_to_base64(
        file_source,
        session: aiohttp.ClientSession,
        return_with_mime: bool = True,
        return_pil: bool = False,
) -> str | tuple[str, Image.Image] | Image.Image:
    """A unified function to encode files to Base64 strings or return PIL Image objects.

    Args:
        file_source: File path, URL, or PIL Image object
        session: aiohttp ClientSession for async URL fetching
        return_with_mime: Whether to include MIME type prefix in base64 string
        return_pil: Whether to return PIL Image object (for image files)

    Returns:
        If return_pil is False: base64 string (with optional MIME prefix)
        If return_pil is True and input is image: (base64_string, PIL_Image) or just PIL_Image
        If return_pil is True and input is not image: base64 string
    """
    mime_type = None
    pil_image = None

    if isinstance(file_source, str):
        if file_source.startswith("file://"):
            file_path = file_source[7:]
            if not os.path.exists(file_path):
                raise ValueError("Local file not found.")
            mime_type, _ = guess_type(file_path)
            if return_pil and mime_type and mime_type.startswith("image"):
                pil_image = Image.open(file_path)
                if return_pil and not return_with_mime:
                    return pil_image
            with open(file_path, "rb") as file:
                content = file.read()

        elif os.path.exists(file_source):
            mime_type, _ = guess_type(file_source)
            if return_pil and mime_type and mime_type.startswith("image"):
                pil_image = Image.open(file_source)
                if return_pil and not return_with_mime:
                    return pil_image
            with open(file_source, "rb") as file:
                content = file.read()

        elif file_source.startswith("http"):
            async with session.get(file_source) as response:
                response.raise_for_status()
                content = await response.read()
                mime_type = response.headers.get("Content-Type", "application/octet-stream")
                if return_pil and mime_type.startswith("image"):
                    pil_image = Image.open(BytesIO(content))
                    if return_pil and not return_with_mime:
                        return pil_image
        else:
            raise ValueError("Unsupported file source type.")

    elif isinstance(file_source, Image.Image):
        pil_image = file_source
        if return_pil and not return_with_mime:
            return pil_image

        buffer = BytesIO()
        image_format = file_source.format or "PNG"
        mime_type = f"image/{image_format.lower()}"
        file_source.save(buffer, format=image_format)
        content = buffer.getvalue()

    else:
        raise ValueError("Unsupported file source type.")

    base64_data = base64.b64encode(content).decode("utf-8")
    result = f"data:{mime_type};base64,{base64_data}" if return_with_mime else base64_data

    if return_pil and pil_image:
        return result, pil_image
    return result


async def encode_image_to_base64(
        image_source,
        session: aiohttp.ClientSession,
        max_side_length: int | None = None,
        return_with_mime: bool = True,
) -> str:
    """Encode an image to base64 string with optional size constraints.

    Args:
        image_source: Can be a file path (str), URL (str), or PIL Image object
        session: aiohttp ClientSession for async URL fetching
        max_side_length: Optional maximum side length for image resizing
        return_with_mime: Whether to include MIME type prefix in the result

    Returns:
        Base64 encoded string (with optional MIME prefix)
    """
    # Get image as PIL Image object
    if isinstance(image_source, Image.Image):
        image = image_source
    else:
        # Use encode_to_base64 with return_pil=True to get PIL Image directly
        result = await encode_to_base64(
            image_source,
            session,
            return_with_mime=False,
            return_pil=True,
        )
        # Handle the return value based on whether it's a tuple or direct PIL Image
        image = result[1] if isinstance(result, tuple) else result

    # Resize image if max_side_length is specified
    if max_side_length:
        original_max_side = max(image.size)
        if max_side_length < original_max_side:
            ratio = max_side_length / original_max_side
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size)

    # Convert processed image to base64
    buffer = BytesIO()
    image_format = image.format or "PNG"
    mime_type = f"image/{image_format.lower()}"
    image.save(buffer, format=image_format)
    buffer.seek(0)

    base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if return_with_mime:
        return f"data:{mime_type};base64,{base64_data}"
    return base64_data


def decode_base64_to_pil(base64_string):
    """将base64字符串解码为PIL Image对象"""
    try:
        # 如果base64字符串包含header (如 'data:image/jpeg;base64,')，去除它
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # 解码base64为二进制数据
        image_data = base64.b64decode(base64_string)

        # 转换为PIL Image对象
        image = Image.open(BytesIO(image_data))
        return image
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为图像: {e!s}")


def decode_base64_to_file(base64_string, output_path, format="JPEG"):
    """将base64字符串解码并保存为图片文件"""
    try:
        # 获取PIL Image对象
        image = decode_base64_to_pil(base64_string)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 保存图像
        image.save(output_path, format=format)
        return True
    except Exception as e:
        raise ValueError(f"无法将base64字符串保存为文件: {e!s}")


def decode_base64_to_bytes(base64_string):
    """将base64字符串解码为字节数据"""
    try:
        # 如果base64字符串包含header，去除它
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # 解码为字节数据
        return base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为字节数据: {e!s}")


async def process_content_recursive(content, session, inplace=True, **kwargs):
    """Recursively process a content dictionary, replacing any URL with its Base64 equivalent.
    """
    if isinstance(content, dict):
        for key, value in content.items():
            if key == "url" and isinstance(value, str):  # Detect URL fields
                base64_data = await encode_image_to_base64(value, session, max_side_length=kwargs.get("max_side_length"))
                if base64_data:
                    content[key] = base64_data
            else:
                await process_content_recursive(value, session, **kwargs)
    elif isinstance(content, list):
        for item in content:
            await process_content_recursive(item, session, **kwargs)


async def messages_preprocess(messages, inplace=False, **kwargs):
    """Process a list of messages, converting URLs in any type of content to Base64.
    """
    if not inplace:
        messages = deepcopy(messages)
    async with aiohttp.ClientSession() as session:
        tasks = [process_content_recursive(message, session, **kwargs) for message in messages]
        await asyncio.gather(*tasks)
    return messages


async def batch_process_messages(
        messages_list,
        max_concurrent=5,
        inplace=False,
        **kwargs,
):
    """Process a list of messages_list, supporting concurrent batch processing.

    Args:
        messages_list (list): List of messages to be processed in batches.
        max_concurrent (int): Maximum number of concurrent batch processes.
        inplace (bool): Whether to modify the messages in place.
        **kwargs: Additional arguments for `messages_preprocess`.

    Returns:
        list: Processed messages lists.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(messages):
        async with semaphore:
            try:
             messages = await messages_preprocess(messages, inplace=inplace, **kwargs)
            except Exception as e:
                logger.error(f"{e=}\n")
                messages = messages
            return messages

    tasks = [process_batch(messages) for messages in messages_list]
    results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    from sparrow import relp
    # Example usage:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述这几张图片"},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": f"{relp('./test_img.jpg')}"}},
            ],
        },
    ]
    from rich import print

    from sparrow import MeasureTime
    mt = MeasureTime()

    processed_messages = asyncio.run(messages_preprocess(messages))
    message = processed_messages[0]
    print(message)
    mt.show_interval()
