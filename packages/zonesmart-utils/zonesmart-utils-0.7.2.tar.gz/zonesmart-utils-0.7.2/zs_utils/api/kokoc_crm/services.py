import requests
from urllib.parse import urlparse, parse_qsl
from pprint import pprint
from django.conf import settings
from django.utils import timezone

from zs_utils.api.kokoc_crm import constants


__all__ = [
    "KokocCRMService",
]


class KokocCRMService:
    @classmethod
    def _make_request(cls, method: str, path: str, params: dict = None):
        assert method in ("get", "post", "put", "delete"), f"Недопустимый метод '{method}'"

        request_data = {
            "method": method,
            "url": f"https://my.kokocgroup.ru/rest/2806/{settings.KOKOC_CRM_TOKEN}/{path}",
        }
        if params:
            if params.get("fields"):
                params["fields"] = {k: v for k, v in params["fields"].items() if v}
            params = cls._prepare_params(params=params).encode("utf-8")
            if method == "get":
                request_data["params"] = params
            else:
                request_data["data"] = params

        response = requests.request(**request_data)
        pprint({k: v for k, v in response.request.__dict__.items() if k in ["method", "url", "body"]})
        results = response.json()

        if not response.ok:
            raise requests.exceptions.HTTPError(results["error_description"])

        return {"data": results, "response": response}

    @classmethod
    def _prepare_params(cls, params, prev="") -> str:
        """
        Конвертация данных в массив битрикс
        Source: https://github.com/akopdev/bitrix24-python-rest/blob/master/bitrix24/bitrix24.py
        """
        ret = ""
        if isinstance(params, dict):
            for key, value in params.items():
                if isinstance(value, dict):
                    if prev:
                        key = "{0}[{1}]".format(prev, key)
                    ret += cls._prepare_params(value, key)
                elif (isinstance(value, list) or isinstance(value, tuple)) and len(value) > 0:
                    for offset, val in enumerate(value):
                        if isinstance(val, dict):
                            ret += cls._prepare_params(val, "{0}[{1}][{2}]".format(prev, key, offset))
                        else:
                            if prev:
                                ret += "{0}[{1}][{2}]={3}&".format(prev, key, offset, val)
                            else:
                                ret += "{0}[{1}]={2}&".format(key, offset, val)
                else:
                    if prev:
                        ret += "{0}[{1}]={2}&".format(prev, key, value)
                    else:
                        ret += "{0}={1}&".format(key, value)
        return ret

    @classmethod
    def _list_objects(cls, obj: constants.CRM_OBJECTS, **filter_params) -> dict:
        if obj == constants.CRM_OBJECTS.CONTACT:
            path = "crm.contact.list.json"
        elif obj == constants.CRM_OBJECTS.DEAL:
            path = "crm.deal.list.json"
        elif obj == constants.CRM_OBJECTS.STATUS:
            path = "crm.status.list.json"
        else:
            raise NotImplementedError(f'Получение списка объектов "{constants.CRM_OBJECTS[obj]}" не поддерживается.')

        results = cls._make_request(method="get", path=path, params={"filter": filter_params})
        results["data"] = results["data"]["result"]
        return results

    @classmethod
    def _get_object(cls, obj: constants.CRM_OBJECTS, remote_id: int) -> dict:
        if obj == constants.CRM_OBJECTS.CONTACT:
            path = "crm.contact.get.json"
        elif obj == constants.CRM_OBJECTS.DEAL:
            path = "crm.deal.get.json"
        elif obj == constants.CRM_OBJECTS.STATUS:
            path = "crm.status.get.json"
        else:
            raise NotImplementedError(f'Получение объекта "{constants.CRM_OBJECTS[obj]}" не поддерживается.')

        results = cls._make_request(method="get", path=path, params={"id": remote_id})
        results["data"] = results["data"]["result"]
        return results

    @classmethod
    def get_deal(cls, deal_id: int) -> dict:
        return cls._get_object(obj=constants.CRM_OBJECTS.DEAL, remote_id=deal_id)

    @classmethod
    def get_contact(cls, contact_id: int) -> dict:
        return cls._get_object(obj=constants.CRM_OBJECTS.CONTACT, remote_id=contact_id)

    @classmethod
    def create_contact(
        cls,
        name: str,
        phone: str = None,
        email: str = None,
    ) -> dict:
        """
        Создание контакта в системе кокос
        """
        params = {
            "fields": {
                "NAME": name,
                "PHONE": [{"VALUE": phone}] if phone else None,
                "EMAIL": [{"VALUE": email}] if email else None,
            },
        }
        return cls._make_request(method="post", path="crm.contact.add.json", params=params)

    @classmethod
    def _get_utm_params_from_url(cls, url: str) -> dict:
        parsed_url = urlparse(url=url)
        return {k: v for k, v in parse_qsl(qs=parsed_url.query) if k.startswith("utm_")}

    @classmethod
    def create_deal(
        cls,
        title: str,
        stage: str,
        contact_id: int = None,
        comment: str = None,
        source: str = None,
        assigned_by: str = "2806",
        department: str = "9923",
        utm_params: dict = None,
    ) -> dict:
        """
        Создание сделки в системе кокос
        """
        if utm_params:
            utm_params = {
                key: utm_params.get(key.lower())
                for key in [
                    "UTM_SOURCE",
                    "UTM_MEDIUM",
                    "UTM_CAMPAIGN",
                    "UTM_CONTENT",
                    "UTM_TERM",
                ]
            }
        else:
            utm_params = {}
        params = {
            "fields": {
                "TITLE": title,
                "CATEGORY_ID": "22",
                "STAGE_ID": stage,
                "CONTACT_ID": contact_id,
                "COMMENTS": comment,
                "UF_CRM_DEAL_AMO_OKDUOUUHNSIOPEJZ": source,
                "ASSIGNED_BY_ID": assigned_by,
                "UF_DEPARTMENT": department,
                **utm_params,
            },
        }
        return cls._make_request(method="post", path="crm.deal.add.json", params=params)

    @classmethod
    def update_deal_stage(cls, deal_id: int, stage: str) -> dict:
        params = {
            "id": deal_id,
            "fields": {
                "STAGE_ID": stage,
            },
        }
        return cls._make_request(method="post", path="crm.deal.update.json", params=params)

    @classmethod
    def delete_deal(cls, deal_id: int) -> dict:
        return cls._make_request(method="post", path="crm.deal.delete.json", params={"id": deal_id})

    @classmethod
    def create_deal_todo(cls, deal_id: int, text: str, deadline: timezone.datetime, responsible_id: int = None):
        return KokocCRMService._make_request(
            method="post",
            path="crm.activity.todo.add",
            params={
                "ownerTypeId": 2,  # значение 2 означает сделку
                "ownerId": deal_id,
                "description": text,
                # Дедлайн по московскому времени
                "deadline": deadline.astimezone(timezone.timezone(offset=timezone.timedelta(hours=3))).strftime(
                    "%d.%m.%Y %H:%M:%S"
                ),
                "responsibleId": responsible_id,
            },
        )
