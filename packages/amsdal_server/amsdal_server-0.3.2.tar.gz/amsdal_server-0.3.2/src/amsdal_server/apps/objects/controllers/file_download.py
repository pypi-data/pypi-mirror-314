import base64
import logging
from hashlib import md5
from typing import Optional
from urllib.parse import quote
from urllib.parse import unquote

from amsdal_utils.models.enums import Versions
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from fastapi import Response

from amsdal_server.apps.common.thumbnail import resize_image
from amsdal_server.apps.objects.router import router
from amsdal_server.apps.objects.services.file_object import ObjectFileApi

logger = logging.getLogger(__name__)


async def _download_file(
    object_id: str,
    request: Request,
    version_id: str = '',
    width: int | None = None,
    height: int | None = None,
) -> Response:
    file_obj = await ObjectFileApi.get_file(
        request.user,
        object_id,
        version_id or Versions.LATEST,
    )

    if not file_obj:
        raise HTTPException(status_code=404, detail='File not found')

    _data = file_obj.data

    if isinstance(_data, bytes) and _data.startswith((b"b'", b'b"')):
        try:
            # legacy corrupted data
            _data = base64.b64decode(eval(_data))  # noqa: S307
        except SyntaxError:
            pass

    etag = generate_etag(_data)

    if request.headers.get('if-none-match') == etag:
        return Response(status_code=304)

    headers = {
        'Cache-Control': 'public, max-age=86400',
        'ETag': etag,
        'Content-Disposition': f'attachment; filename={quote(file_obj.filename)}',
    }

    if width and height:
        size = (width, height)
    else:
        size = None

    try:
        content = resize_image(_data, size=size)
    except Exception as e:
        logger.warning('Unable to resize image (probably it is not an image): %s', e, exc_info=True)
        content = _data

    return Response(
        content=content,
        headers=headers,
        media_type=file_obj.mimetype or 'application/octet-stream',
    )


def generate_etag(content: bytes) -> str:
    return md5(content).hexdigest()  # noqa: S324


@router.get('/api/objects/file-download/{object_id}/')
async def file_download(
    object_id: str,
    request: Request,
    version_id: str = '',
    width: Optional[int] = Query(None),  # noqa: UP007
    height: Optional[int] = Query(None),  # noqa: UP007
) -> Response:
    return await _download_file(object_id, request, version_id, width, height)


@router.get('/api/objects/download-file/')
async def download_file(
    request: Request,
    object_id: str,
    version_id: str = '',
    width: Optional[int] = Query(None),  # noqa: UP007
    height: Optional[int] = Query(None),  # noqa: UP007
) -> Response:
    return await _download_file(unquote(object_id), request, version_id, width, height)
