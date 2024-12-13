# vim: set fileencoding=utf-8 :
from django.contrib import admin

import proxy.models as models


class TraceActiviteAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'demandeur',
        'RAE_concerne',
        'service_concerne',
        'horodate',
    )
    list_filter = (
        'demandeur',
        'service_concerne',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.TraceActivite, TraceActiviteAdmin)
