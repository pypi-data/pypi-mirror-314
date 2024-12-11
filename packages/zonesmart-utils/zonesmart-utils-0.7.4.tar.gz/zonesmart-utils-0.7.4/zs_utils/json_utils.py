import simplejson
import datetime
import decimal
import uuid
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS

from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.functional import Promise


class CustomJSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Exception):
            return getattr(obj, "message", str(obj))

        # Код ниже взят из rest_framework.utils.encoders.JSONEncoder

        # For Date Time string spec, see ECMA 262
        # https://ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
        if isinstance(obj, Promise):
            return force_str(obj)
        elif isinstance(obj, datetime.datetime):
            representation = obj.isoformat()
            # TODO: Разобраться, зачем это было нужно
            # if representation.endswith("+00:00"):
            #     representation = representation[:-6]  # + "Z"
            return representation
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            if timezone and timezone.is_aware(obj):
                raise ValueError("JSON can't represent timezone-aware times.")
            representation = obj.isoformat()
            return representation
        elif isinstance(obj, datetime.timedelta):
            return str(obj.total_seconds())
        elif isinstance(obj, decimal.Decimal):
            # Serializers will coerce decimals to strings by default.
            return float(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, QuerySet):
            return tuple(obj)
        elif isinstance(obj, bytes):
            # Best-effort for binary blobs. See #4187.
            return obj.decode()
        elif hasattr(obj, "tolist"):
            # Numpy arrays and array scalars.
            return obj.tolist()
        elif hasattr(obj, "__getitem__"):
            cls = list if isinstance(obj, (list, tuple)) else dict
            try:
                return cls(obj)
            except Exception:
                pass
        elif hasattr(obj, "__iter__"):
            return tuple(item for item in obj)

        return super().default(obj)


def custom_json_dumps(obj, **kwargs):
    return simplejson.dumps(obj, cls=CustomJSONEncoder, **kwargs)


def custom_json_loads(obj, **kwargs):
    return simplejson.loads(obj, **kwargs)


def pretty_json(data: dict, safe: bool = True) -> str:
    try:
        return simplejson.dumps(data, indent=True, cls=CustomJSONEncoder, ensure_ascii=False)
    except TypeError as error:
        if not safe:
            raise error
    return str(data)


class CustomJSONRenderer(JSONRenderer):
    encoder_class = CustomJSONEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b""

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        # Замена json на simplejson ради параметра ignore_nan
        ret = simplejson.dumps(
            data,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=self.ensure_ascii,
            separators=separators,
            ignore_nan=True,
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        return ret.encode()
