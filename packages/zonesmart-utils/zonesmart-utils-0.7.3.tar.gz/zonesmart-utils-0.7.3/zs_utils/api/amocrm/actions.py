from django.utils import timezone
from django.conf import settings

from zs_utils.api.amocrm.base_action import AmocrmAction
from zs_utils.api.amocrm import core


__all__ = [
    "RemoteGetAmocrmContactByLead",
    "RemoteCreateAmocrmContact",
    "RemoteCreateAmocrmLead",
    "RemoteUpdateAmocrmLead",
    "RemoteCreateAmocrmTask",
]


class RemoteGetAmocrmContactByLead(AmocrmAction):
    description = "Получение информации о сделке amoCRM"
    api_class = core.GetAmocrmLeadAPI
    required_params = ["lead_id"]
    allowed_params = ["with"]

    def get_params(self, **kwargs) -> dict:
        kwargs["with"] = "contacts"
        return super().get_params(**kwargs)

    def format_success_results(self, results: dict, **kwargs) -> dict:
        return {"contact_id": results["_embedded"]["contacts"][0]["id"]}


class RemoteCreateAmocrmContact(AmocrmAction):
    description = "Создание контакта на amoCRM"
    api_class = core.CreateAmocrmContactAPI
    SAVE_REQUEST_LOG = True
    CUSTOM_FIELDS_MAPPING = settings.AMOCRM_CONTACT_CUSTOM_FIELDS
    required_params = []
    allowed_params = [
        "name",
        "first_name",
        "last_name",
        "custom_fields_values",
        "responsible_user_id",
    ]

    def get_params(self, responsible_user_id: int = None, **kwargs) -> dict:
        if not responsible_user_id:
            responsible_user_id = settings.AMOCRM_DEFAULT_MANAGER_ID
        return super().get_params(responsible_user_id=responsible_user_id, **kwargs)

    def format_success_results(self, results: dict, **kwargs) -> dict:
        return {"contact_id": results["_embedded"]["contacts"][0]["id"]}


class RemoteCreateAmocrmLead(AmocrmAction):
    description = "Создание сделки на amoCRM"
    api_class = core.CreateAmocrmLeadAPI
    SAVE_REQUEST_LOG = True
    CUSTOM_FIELDS_MAPPING = settings.AMOCRM_LEAD_CUSTOM_FIELDS
    required_params = [
        "pipeline_id",
        "_embedded",
    ]
    allowed_params = [
        "created_by",
        "updated_by",
        "status_id",
        "custom_fields_values",
        "name",
        "price",
        "responsible_user_id",
    ]

    def get_params(
        self,
        pipeline_id: int,
        contact_id: int,
        status_id: int,
        responsible_user_id: int = None,
        **kwargs,
    ) -> dict:
        if not responsible_user_id:
            responsible_user_id = settings.AMOCRM_DEFAULT_MANAGER_ID

        kwargs.update(
            {
                "pipeline_id": pipeline_id,
                "status_id": status_id,
                "responsible_user_id": responsible_user_id,
                "_embedded": {
                    "contacts": [{"id": contact_id}],
                    "tags": [],
                },
            }
        )

        # Теги
        tags = kwargs.pop("tags", [])
        for tag in tags:
            kwargs["_embedded"]["tags"].append({"name": tag})

        return super().get_params(**kwargs)

    def format_success_results(self, results: dict, **kwargs) -> dict:
        return {"lead_id": results["_embedded"]["leads"][0]["id"]}


class RemoteUpdateAmocrmLead(AmocrmAction):
    description = "Обновление сделки amoCRM"
    api_class = core.UpdateAmocrmLeadAPI
    SAVE_REQUEST_LOG = True
    CUSTOM_FIELDS_MAPPING = settings.AMOCRM_LEAD_CUSTOM_FIELDS
    required_params = [
        "id",
    ]
    allowed_params = [
        "name",
        "price",
        "pipeline_id",
        "_embedded",
        "status_id",
        "created_by",
        "updated_by",
        "responsible_user_id",
        "loss_reason_id",
        "custom_fields_values",
    ]

    def get_params(self, lead_id: int, **kwargs) -> dict:
        kwargs["id"] = lead_id
        return super().get_params(**kwargs)


class RemoteCreateAmocrmTask(AmocrmAction):
    description = "Создание задачи на amoCRM"
    api_class = core.CreateAmocrmTaskAPI
    SAVE_REQUEST_LOG = True
    required_params = [
        "text",
        "complete_till",
    ]
    allowed_params = [
        "responsible_user_id",
        "created_by",
        "updated_by",
        "entity_id",
        "entity_type",
        "is_completed",
        "task_type_id",
        "duration",
        "result",
    ]

    def get_params(
        self,
        lead_id: str,
        responsible_user_id: int = None,
        created_user_id: int = None,
        complete_till: timezone.datetime = None,
        **kwargs,
    ) -> dict:
        if not responsible_user_id:
            responsible_user_id = settings.AMOCRM_DEFAULT_MANAGER_ID
        if not created_user_id:
            created_user_id = settings.AMOCRM_MAIN_MANAGER_ID
        kwargs.update(
            {
                "responsible_user_id": responsible_user_id,
                "created_by": created_user_id,
                "complete_till": int(complete_till.timestamp()),
                "entity_id": lead_id,
                "entity_type": "leads",
            }
        )
        return super().get_params(**kwargs)

    def format_success_results(self, results: dict, **kwargs) -> dict:
        return {"task_id": results["_embedded"]["tasks"][0]["id"]}
