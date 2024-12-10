from django.contrib import admin
from .models import ApiCallLog

# Register your models here.


class ApiCallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'status_code', 'source_ip',
                    'session_id', 'app_token_id', 'created_at')
    search_fields = ['id', 'url', 'status_code',
                     'source_ip', 'session_id', 'app_token_id']
    search_help_text = 'Search with Id, URL and session id, token id, message, status code, or IP address.'
    list_per_page = 500
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['id', 'url', 'message', 'status_code', 'source_ip',
                       'session_id', 'app_token_id', 'created_at']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(ApiCallLog, ApiCallLogAdmin)
