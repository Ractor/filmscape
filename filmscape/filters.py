from django.db.models.functions import Lower
from rest_framework.filters import OrderingFilter


class CaseInsensitiveOrderingFilter(OrderingFilter):
    """
    Extension to the OrderingFilter providing case-insensitive ordering.
    """
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering is None:
            return queryset

        for o in ordering:
            if o.startswith('-'):
                queryset = queryset.order_by(Lower(o[1:])).reverse()
            else:
                queryset = queryset.order_by(Lower(o))
        return queryset
