from django.contrib import admin

from .models import Route, Measurement


class MeasurementInline(admin.TabularInline):
    model = Measurement


class RouteAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


admin.site.register(Route, RouteAdmin)