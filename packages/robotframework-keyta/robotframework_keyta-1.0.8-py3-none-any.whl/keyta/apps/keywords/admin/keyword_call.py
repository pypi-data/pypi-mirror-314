from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.common.widgets import open_link_in_modal

from ..models import (
    KeywordCall,
    KeywordCallReturnValue
)
from .keywordcall_parameters_inline import KeywordCallParametersInline


class KeywordCallReturnValueInline(admin.TabularInline):
    model = KeywordCallReturnValue
    fields = ['name']
    extra = 1
    max_num = 1
    verbose_name = 'Rückgabewert'
    verbose_name_plural = 'Rückgabewert'
    can_delete = False


@admin.register(KeywordCall)
class KeywordCallAdmin(BaseAdmin):
    fields = [
        'keyword_doc',
        'return_value'
    ]
    readonly_fields = [
        'keyword_doc',
        'return_value'
    ]

    def get_inlines(self, request, obj):
        kw_call: KeywordCall = obj

        if kw_call.parameters.exists():
            return [KeywordCallParametersInline]
        else:
            return []

    @admin.display(description='Dokumentation')
    def keyword_doc(self, obj: KeywordCall):
        return open_link_in_modal(
            obj.to_keyword.get_docadmin_url(),
            obj.to_keyword.name
        )

    @admin.display(description='Rückgabewert')
    def return_value(self, obj):
        kw_call: KeywordCall = obj
        return_value: KeywordCallReturnValue = kw_call.return_value.first()

        if return_value and return_value.is_set:
            return str(return_value)

        return 'Kein Rückgabewert'
