from django.contrib import admin
from pds_v3.models import PdSession, AppUser, LawSociety, \
LawSocietyOverride, Purchase, Subject, PdSessionEdit, Notice, PdAttachment, Address, PdAudio
from pds_v3 import models

admin.site.site_header = 'PD Squirrel Administration'


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
	list_filter = ('is_presenter','is_premium')

admin.site.register(PdSession)
admin.site.register(PdAudio)
admin.site.register(Address)
admin.site.register(PdAttachment)
admin.site.register(Notice)
admin.site.register(Subject)
admin.site.register(LawSociety)
admin.site.register(LawSocietyOverride)
admin.site.register(Purchase)
admin.site.register(PdSessionEdit)

admin.site.register(models.Presenter)
