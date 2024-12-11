from model_utils import Choices


__all__ = [
    "FILE_EXTENSIONS",
    "FILE_EXTENSION_TO_CONTENT_TYPE",
    "CONTENT_TYPE_TO_FILE_EXTENSION",
]


FILE_EXTENSIONS = Choices(
    "csv",
    "pdf",
    "xlsx",
    "yml",
    "xml",
)

FILE_EXTENSION_TO_CONTENT_TYPE = {
    FILE_EXTENSIONS.csv: "text/csv",
    FILE_EXTENSIONS.pdf: "application/pdf",
    FILE_EXTENSIONS.xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    FILE_EXTENSIONS.yml: "application/xml",
    FILE_EXTENSIONS.xml: "application/xml",
}

CONTENT_TYPE_TO_FILE_EXTENSION = {
    **{value: key for key, value in FILE_EXTENSION_TO_CONTENT_TYPE.items()},
    "application/csv": FILE_EXTENSIONS.csv,
    "application/xml": FILE_EXTENSIONS.xml,
}
