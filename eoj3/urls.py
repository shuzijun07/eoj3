"""eoj3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import re

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.static import serve

from account.views import my_login, RegisterView, FeedbackView
from blog.views import GenericView
from home.views import home_view, faq_view, TestView
from submission.views import SubmissionView, SubmissionRejudgeView, pure_submission_api
from tests.views import test_view, test_contest_view
from .settings import UPLOAD_DIR, DEBUG, STATIC_DIR, MEDIA_URL, MEDIA_ROOT

UPLOAD_ROOT = '/upload/'
STATIC_ROOT = '/static/'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('eoj3.api_urls', namespace='api')),
    url(r'^$', home_view, name='home'),
    url(r'^faq/$', faq_view, name='faq'),
    url(r'^problem/', include('problem.urls', namespace='problem')),
    url(r'^submission/(?P<pk>\d+)/$', SubmissionView.as_view(), name='submission'),
    url(r'^submission/rendered/(?P<pk>\d+)/$', pure_submission_api),
    url(r'^rejudge/(?P<pk>\d+)/$', SubmissionRejudgeView.as_view(), name='rejudge'),
    url(r'^contest/', include('contest.urls', namespace='contest')),
    url(r'^login/$', my_login, name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^backstage/', include('backstage.urls', namespace='backstage')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^generic/(?P<name>.*)', GenericView.as_view(), name='generic'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^feedback/', FeedbackView.as_view(), name='feedback'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^polygon/', include('polygon.urls', namespace='polygon')),
    url(r'^message/', include('message.urls', namespace='message')),
]


if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^test/', test_view, name='test'),
        url(r'^test_contest', test_contest_view, name='test_contest'),
        url(r'^%s(?P<path>.*)$' % re.escape(STATIC_ROOT.lstrip('/')), serve, name='static',
            kwargs={'document_root': STATIC_DIR}),
        url(r'^%s(?P<path>.*)$' % re.escape(UPLOAD_ROOT.lstrip('/')), serve, name='upload',
            kwargs={'document_root': UPLOAD_DIR}),
        # url(r'^%s(?P<path>.*)$' % re.escape(UPLOAD_ROOT.lstrip('/')), serve, name='media',
        #     kwargs={'document_root': MEDIA_DIR}),
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r't/', TestView.as_view())
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)


handler403 = 'home.views.forbidden_view'
handler404 = 'home.views.not_found_view'
# handler500 = 'home.views.server_error_view'
