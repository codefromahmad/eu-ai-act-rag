from pathlib import Path

from fastapi import HTTPException, UploadFile


class FileValidationService:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
    }

    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

    def validate(
        self,
        file: UploadFile,
    ) -> str:

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file must have a filename.",
            )

        extension = Path(
            file.filename
        ).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Supported formats are PDF, DOCX, TXT and MD."
                ),
            )

        return extension

    async def validate_size(
        self,
        file: UploadFile,
    ) -> None:

        content = await file.read()

        size = len(content)

        if size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        if size > self.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    "The uploaded file is too large. "
                    "Maximum allowed size is 10 MB."
                ),
            )

        # Reset the file pointer so the route
        # can read the file again later.
        await file.seek(0)