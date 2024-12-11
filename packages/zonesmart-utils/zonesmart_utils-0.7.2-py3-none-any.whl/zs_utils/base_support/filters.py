from django_filters import filterset, filters

from zs_utils.base_support import constants, models


__all__ = [
    "SupportTicketFilter",
]


class SupportTicketFilter(filterset.FilterSet):
    active = filters.BooleanFilter(method="filter_active")
    client_status = filters.ChoiceFilter(
        choices=constants.SUPPORT_TICKET_CLIENT_STATUSES,
        method="filter_by_client_status",
    )
    ordering = filters.OrderingFilter(fields=["created"])

    class Meta:
        model = models.SupportTicket
        fields = [
            "user",
            "manager",
            "status",
            "question_type",
            "number",
        ]

    def get_responded_ticket_ids(self, queryset) -> list[str]:
        responded_ids = []
        for ticket in queryset.filter(status=constants.SUPPORT_TICKET_STATUSES.OPEN):
            if ticket.manager:
                last_message = ticket.last_message
                if last_message and (ticket.last_message.sender == ticket.manager):
                    responded_ids.append(ticket.id)
        return responded_ids

    def filter_by_client_status(self, queryset, name, value):
        if value == constants.SUPPORT_TICKET_CLIENT_STATUSES.PENDING:
            return queryset.filter(status__in=constants.SUPPORT_TICKET_ACTIVE_STATUSES_LIST).exclude(
                id__in=self.get_responded_ticket_ids(queryset=queryset)
            )
        if value == constants.SUPPORT_TICKET_CLIENT_STATUSES.RESPONDED:
            return queryset.filter(id__in=self.get_responded_ticket_ids(queryset=queryset))
        if value == constants.SUPPORT_TICKET_CLIENT_STATUSES.CLOSED:
            return queryset.exclude(status__in=constants.SUPPORT_TICKET_ACTIVE_STATUSES_LIST)

    def filter_active(self, queryset, name, value):
        filter_kwargs = {"status__in": constants.SUPPORT_TICKET_ACTIVE_STATUSES_LIST}
        if value:
            return queryset.filter(**filter_kwargs)
        else:
            return queryset.exclude(**filter_kwargs)
