from django.conf.urls import include, url, handler404, handler500, handler403, handler400
from django.contrib import admin
from pds_v3.views import views, user_views, presenter_views, tmp_views, payment_views

urlpatterns = [
    # main pages
    url(r'^$', views.landing, name="home"),
    url(r'^login/$', user_views.login_landing, name="login-landing"),
    url(r'^browse/$', views.browse, name="browse"),
    url(r'^user/join/$', user_views.join, name="join"),
    url(r'^cap_ref/$', tmp_views.cap_ajax, name='cap-ref'),

    # Browse page related views
    url(r'^pd/(?P<pd_id>\d+)/$', views.detail, name="detail"),
    url(r'^pd/session/comment/$', views.comment, name="comment"),
    url(r'^pd/session/comment/delete/$', views.delete_comment, name="delete_comment"),
    url(r'^pd/accred/(?P<pd_id>\d+)/(?P<s_id>\d+)/$', views.accred, name="accred"),
    url(r'^pd/accred/(?P<pd_id>\d+)/$', views.accred, name="accred"),
    url(r'^user/presenter/(?P<p_id>\d+)/$', views.presenter_detail, name="presenter-detail"),

    # User views
    url(r'^user/dash/$', user_views.dash, name="dash"),
    url(r'^user/activate/(?P<link_id>[a-zA-Z0-9]+)/$', user_views.activate, name="activate"),
    url(r'^user/reports/$', user_views.reports, name="reports"),
    url(r'^user/reports/purchase/$', user_views.purchase_report, name="purchase-report"),
    url(r'^user/login/$', user_views.login_user, name="login"),
    url(r'^user/logout/$', user_views.logout_user, name="logout"),
    url(r'^user/recover/$', user_views.recover, name="recover"),
    url(r'^payment-process/$', payment_views.payment_process, name="payment-process"),

    # Footer links
    url(r'^about/$', tmp_views.learn, name="learn"),
    url(r'^contact/$', tmp_views.contact, name="contact-us"),
    url(r'^support/$', views.support_msg, name="support"),
    url(r'^terms/$', tmp_views.terms, name="terms"),
    url(r'^privacy/$', tmp_views.privacy, name="privacy"),
    url(r'^become-a-presenter/$', user_views.become_presenter, name="presenter-info"),

    # User options
    url(r'^user/options/$', user_views.options, name="options"),
    url(r'^user/options/email$', user_views.change_email, name="change-email"),
    url(r'^user/options/pass$', user_views.change_pass, name="change-pass"),
    url(r'^user/options/membership$', user_views.change_membership, name="change-membership"),
    url(r'^user/options/newcard/$', user_views.add_card, name="newcard"),
    url(r'^user/options/delcard/$', user_views.del_card, name="delcard"),
    url(r'^user/options/u_card/$', user_views.default_payment, name="update-payment"),

    # presenter hub
    url(r'^user/presenter/dash/$', presenter_views.dash, name="presenter-dash"),
    url(r'^preview/(?P<id>\d+)/$', views.preview, name="preview-session"),
    url(r'^record/$', presenter_views.record, name="record"),
    url(r'^edit/(?P<id>\d+)/$', presenter_views.edit, name="edit"),
    url(r'^upload/$', presenter_views.presenter_uploads, name="upload"),
    url(r'^analytics/$', presenter_views.analytics_report, name="analytics-report"),

    # file retrieval
    url(r'^audio/(?P<pd_id>\d+)/$', views.getAudio, name="audio"),
    url(r'^recording/(?P<audio_id>\d+)/$', views.getRecordingMp3, name="recording"),
    url(r'^wav/(?P<audio_id>\d+)/$', views.getRecordingWav, name="recording-wav"),
    url(r'^attachment/(?P<a_id>\d+)/$', views.getAttachment, name="attachment"),

    # admin pages
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload-admin/$', views.upload_admin, name="upload-admin"),
    url(r'^upload-admin/(?P<pd_id>\d+)/$', views.upload_admin, name="upload-admin"),
    url(r'^accounting/$', views.accounting_admin, name="accounting"),

]

handler404 = 'pds_v3.views.handler404'
handler500 = 'pds_v3.views.handler500'
handler403 = 'pds_v3.views.handler403'
handler400 = 'pds_v3.views.handler400'
