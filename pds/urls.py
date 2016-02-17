from django.conf.urls import include, url
from django.contrib import admin
from pds_v3 import views, user_views, bootsnip_views, final_views, presenter_views, tmp_views, payment_views, ajax_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

   #Home Page
    url(r'^$', views.landing, name="home"),
    #Browse/Search Page
    url(r'^pd/$', views.browse, name="browse"),
    url(r'^pd/(?P<pd_id>\d+)/$', views.detail, name="detail"),
    url(r'^pd/session/(?P<pd_id>\d+)/$', views.watch, name="watch"),
    url(r'^pd/accred/(?P<pd_id>\d+)/(?P<s_id>\d+)/$', views.accred, name="accred"),
    url(r'^pd/accred/(?P<pd_id>\d+)/$', views.accred, name="accred"),
    url(r'^browse/$', views.browse, name="browse"),
    url(r'^user/join/$', user_views.join, name="join"),
    url(r'^user/options/$', user_views.options, name="options"),
    url(r'^user/dash/$', user_views.dash, name="dash"),
    url(r'^user/reports/$', user_views.reports, name="reports"),
    url(r'^user/reports/purchase/$', user_views.purchase_report, name="purchase-report"),
    url(r'^user/presenter/(?P<p_id>\d+)/$', views.presenter_detail, name="presenter-detail"),
    url(r'^preview/(?P<id>\d+)/$', views.preview, name="preview-session"),
    url(r'^user/presenter/edit/(?P<pd_id>\d+)/$', presenter_views.edit, name="presenter-edit-pd"),
    url(r'^user/login/$', user_views.login_user, name="login"),
    url(r'^user/update/$', user_views.update, name="user-update"),
    url(r'^user/logout/$', user_views.logout_user, name="logout"),
    url(r'^login/$', user_views.login_landing, name="login-landing"),
    url(r'^debug/', views.debug, name="debug"),
    url(r'^ajax/', include('ajax.urls')),
    url(r'^bootsnip/', bootsnip_views.bootsnip, name="bootsnip"),
    url(r'^payment-example/$', payment_views.payment_process, name="payment-process"),
    url(r'^accred/(?P<pd_id>\d+)/$', views.accred, name="accred"),
    url(r'^about/$', tmp_views.about, name="about"),
    url(r'^learn/$', tmp_views.learn, name="learn"),
    url(r'^contact/$', tmp_views.contact, name="contact-us"),
    url(r'^terms/$', tmp_views.terms, name="terms"),
    url(r'^presenter-terms/$', tmp_views.presenter_terms, name="presenter-terms"),
    url(r'^cap/$', tmp_views.cap, name="cap"),
    url(r'^privacy/$', tmp_views.privacy, name="privacy"),
    url(r'^become-a-presenter/$', user_views.become_presenter, name="presenter-info"),
    url(r'^user/options/email$', user_views.change_email, name="change-email"),
    url(r'^user/activate/(?P<link_id>\d+)/$', user_views.activate, name="activate"),
    url(r'^user/options/pass$', user_views.change_pass, name="change-pass"),
    url(r'^user/options/membership$', user_views.change_membership, name="change-membership"),
    url(r'^user/options/newcard/$', user_views.add_card, name="newcard"),
    url(r'^user/options/delcard/$', user_views.del_card, name="delcard"),
    url(r'^ajax/cap_ref/$', views.cap_refresh, name='ajax-captcha'),
    url(r'^cap_ref/$', tmp_views.cap_ajax, name='cap-ref'),

    url(r'^upload-admin/$', views.upload_admin, name="upload-admin"),
    url(r'^upload-admin/(?P<pd_id>\d+)/$', views.upload_admin, name="upload-admin"),

    url(r'^accounting/$', views.accounting_admin, name="accounting"),


    #presenter urls
    #Home page for presenter
    url(r'^user/presenter/dash/$', presenter_views.dash, name="presenter-dash"),
    url(r'^user/presenter/dash/edit/$', presenter_views.edit, name="presenter-edit"),

    url(r'^user/recover/$', user_views.recover, name="recover"),
    url(r'^support/$', views.support_msg, name="support"),

    url(r'^record/$', presenter_views.record, name="record"),
    url(r'^pd/session/(?P<pd_id>\d+)/$', views.watch, name="watch"),
    url(r'^record/(?P<r_id>\d+)/$', presenter_views.editRecording, name="edit-recording"),


    url(r'^edit/(?P<id>\d+)/$', presenter_views.edit, name="edit"),

    url(r'^ajax-test/$', ajax_views.ajax_test, name="ajax-test"),

    url(r'^analytics/$', presenter_views.analytics_report, name="analytics-report"),

]
