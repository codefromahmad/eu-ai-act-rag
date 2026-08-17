from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile

from app.services.file_validation_service import (
    FileValidationService,
)


@pytest.mark.asyncio
async def test_valid_txt_file_passes():

    service = FileValidationService()

    file = UploadFile(
        filename="system.txt",
        file=BytesIO(
            b"This AI system ranks candidates."
        ),
    )

    extension = service.validate(
        file
    )

    await service.validate_size(
        file
    )

    assert extension == ".txt"


@pytest.mark.asyncio
async def test_empty_file_is_rejected():

    service = FileValidationService()

    file = UploadFile(
        filename="empty.txt",
        file=BytesIO(b""),
    )

    with pytest.raises(
        HTTPException
    ) as exc:

        service.validate(
            file
        )

        await service.validate_size(
            file
        )

    assert exc.value.status_code == 400


def test_unsupported_extension_is_rejected():

    service = FileValidationService()

    file = UploadFile(
        filename="image.jpg",
        file=BytesIO(b"fake image"),
    )

    with pytest.raises(
        HTTPException
    ) as exc:

        service.validate(
            file
        )

    assert exc.value.status_code == 400