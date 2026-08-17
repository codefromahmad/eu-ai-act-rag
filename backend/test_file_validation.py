import asyncio
from io import BytesIO

from fastapi import UploadFile

from app.services.file_validation_service import (
    FileValidationService,
)


async def main():

    service = FileValidationService()

    valid_file = UploadFile(
        filename="test_system.txt",
        file=BytesIO(
            b"This AI system ranks candidates."
        ),
    )

    extension = service.validate(
        valid_file
    )

    await service.validate_size(
        valid_file
    )

    print("Valid extension:", extension)
    print("Valid file passed validation.")

    empty_file = UploadFile(
        filename="empty.txt",
        file=BytesIO(
            b""
        ),
    )

    try:
        service.validate(
            empty_file
        )

        await service.validate_size(
            empty_file
        )

    except Exception as exc:
        print(
            "Empty file rejected:",
            str(exc),
        )


asyncio.run(
    main()
)