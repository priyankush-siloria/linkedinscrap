from django.contrib import admin
from .models import *


class GeographyAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

class SeniorityLevelAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

class YearAtCompanyAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

class FunctionAtComapnyAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Geography, GeographyAdmin)
admin.site.register(SeniorityLevel, SeniorityLevelAdmin)
admin.site.register(YearAtCompany, YearAtCompanyAdmin)
admin.site.register(FunctionAtComapny, FunctionAtComapnyAdmin)
admin.site.register(Automations)
admin.site.register(LinkedIn)
admin.site.register(AutomationData)
admin.site.register(ScriptInterval)