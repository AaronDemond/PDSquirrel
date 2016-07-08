from django.contrib import admin
from pds_v3.models import PdSession, AppUser, LawSociety, \
LawSocietyOverride, Purchase, Subject, PdSessionEdit, Notice, PdAttachment, Address, PdAudio, Comment, Presenter
from pds_v3 import models
import tasks

admin.site.site_header = 'PD Squirrel Administration'


def make_presenter(modeladmin, request, queryset):
    for appuser in queryset:
        appuser.is_presenter = True
        appuser.save()
        p = Presenter(user=appuser.user)
        p.save()



def send_activation(modeladmin, request, queryset):
    for appuser in queryset:
        msg = "Hello " + appuser.user.first_name + " " + appuser.user.last_name + ", and welcome to PD Squirrel!\n\nPlease click on the following link and use your email address to activate your membership account: https://pdsquirrel.ca/user/activate/%s\n\nThanks,\nThe PD Squirrel admin team" % (str(appuser.activation_key) + "/")
        subject = 'PD Squirrel Activation'
        send_to = [appuser.user.email, 'demondsoftware@gmail.com', 'cdemond@cwdlaw.ca']
        tasks.sendMail.apply_async([send_to, subject, msg])
        

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_filter = ('is_presenter','is_premium')
    actions = [send_activation, make_presenter]



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
admin.site.register(Comment)
admin.site.register(models.Presenter)
