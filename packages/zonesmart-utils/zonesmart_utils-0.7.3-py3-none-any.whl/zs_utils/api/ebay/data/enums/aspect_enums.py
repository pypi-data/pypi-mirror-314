from model_utils import Choices


AspectApplicableTo = Choices(
    ("ITEM", "Групповой товар"),
    ("PRODUCT", "Товар"),
)

AspectDataTypeEnum = Choices(
    ("DATE", "Date"),
    ("NUMBER", "Number"),
    ("STRING", "String"),
    ("STRING_ARRAY", "Array of strings"),
)

AspectModeEnum = Choices(
    ("FREE_TEXT", "Free text"),
    ("SELECTION_ONLY", "Selection only"),
)

AspectUsageEnum = Choices(
    ("RECOMMENDED", "Recommended"),
    ("OPTIONAL", "Optional"),
)

ItemToAspectCardinalityEnum = Choices(
    ("MULTI", "Multi"),
    ("SINGLE", "Single"),
)


GroupAspectType = Choices(
    ("SHARED", "Общий"),
    ("UNIQUE", "Уникальный"),
    ("NOT_USED", "Не используется"),
)
