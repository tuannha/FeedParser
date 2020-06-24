from django.views.generic import ListView
from django.db.models import Q

from material.frontend.views.list import ListModelView


class BaseModelListView(ListModelView, ListView):
    ajax_searchable = False
    ajax_search_fields = []

    def generate_search_query(self, search_value):
        if not search_value:
            return None

        all_qs = None
        for field in self.ajax_search_fields:
            q_statement = {'%s__icontains' % field: search_value}
            if all_qs is None:
                all_qs = Q(**q_statement)
                continue
            all_qs = all_qs | Q(**q_statement)

        return all_qs

    def get_datatable_config(self):
        config = super().get_datatable_config()
        config['ajax']['url'] = self.request.get_full_path()
        config['bFilter'] = self.ajax_searchable
        config['aLengthMenu'] = [[10, 25, 50, 100], [10, 25, 50, 100]]
        config['bLengthChange'] = True
        config['bAutoWidth'] = False
        return config

    def get_object_list(self):
        queryset = super().get_object_list()

        search_value = self.request.GET.get('datatable-search[value]')
        search_query = self.generate_search_query(search_value)
        if search_query is not None:
            queryset = queryset.filter(
                self.generate_search_query(search_value)
            )

        return queryset.distinct()
