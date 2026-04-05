from fastapi import UploadFile

from app.exception import BadRequestError

ALLOWED_IMAGE_FILE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024


async def validate_images(images: list[UploadFile]) -> list[UploadFile]:
    if not images:
        return []

    if len(images) > 10:
        raise BadRequestError(detail="No more than 10 files")

    for image in images:
        await validate_image(image)

    return images


async def validate_image(image: UploadFile) -> UploadFile:
    if image.content_type not in ALLOWED_IMAGE_FILE_TYPES:
        raise BadRequestError(detail="Invalid file format")

    file_size = len(await image.read())
    await image.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise BadRequestError(
            detail=f"File too big (max {MAX_FILE_SIZE // (1024 ** 2)} MB)"
        )

    return image
