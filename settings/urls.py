"""pib URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from resources.sitemaps import ResourcesViewSitemap, TextBookProblemsViewSitemap, TextBookSolutionsViewSitemap
from curricula.sitemaps import CurriculaViewSitemap

# from .views import discussion_app, \
from .views import codesandbox_static_proxy_view

sitemaps = {
    'resources': ResourcesViewSitemap,
    'textbook_problems': TextBookProblemsViewSitemap,
    'textbook_solutions': TextBookSolutionsViewSitemap,
    'curricula': CurriculaViewSitemap,
}

urlpatterns = [
    # url(r'^', include('homepage.urls')),
    # # TODO remove all unused urls
    # # must be upper than curriculum/
    # url(r'^curriculum/profile/', include(('editor.urls', 'editor'), namespace='curriculum_profile')),
    # # namespace - a fix for api/v1/editor/curricula url (drf router)
    # url(r'^curriculum/', include('curricula.urls', namespace='main_curricula')),
    # # url(r'^editor/', include('editor.urls')),
    # url(r'^studio/', include(('editor.urls', 'studio'), namespace='studio')),
    # url(r'^browse/', include(('editor.urls', 'browse'), namespace='browse')),
    # url(r'^classroom/', include('classroom.urls')),
    # url(r'^resources/', include('resources.urls')),

    # # TODO add only necessary urls from allauth we will use only models from allauth
    # we use confirm-email url now
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/', include('pib_auth.urls')), # TODO remove (mobile version related urls)?
    # TODO exclude url reverse for user-profile in code
    # url(r'^profile/', include('profiles.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^discussion1/', include('djeddit.urls')),
    # url(r'^discussion/', discussion_app, name='discussion_app'),
    # due https://github.com/encode/django-rest-framework/issues/2760 namespace do not work
    # url(r'^api/v1/', include('settings.urls_api', namespace='api')),
    url(r'^api/v1/', include('settings.urls_api')),
    url(r'^proxy/static/courses/js/codesandbox-apps/(?P<path>.*)', codesandbox_static_proxy_view),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    import urllib
    from django.views.generic import RedirectView
    from django.http import HttpResponse

    def proxy_view(request, pt_uuid, material_uuid, lesson_uuid, path):
        remoteurl = f'{request.scheme}://{request.get_host()}/media/mpt_builds/{pt_uuid}/build/' + path
        body = None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        request = urllib.request.Request(remoteurl, body, headers)
        try:
            response = urllib.request.urlopen(request)
            response_body = response.read()
            status = response.getcode()
        except urllib.error.HTTPError as e:
            status = e.code
            response_body = e.msg

        return HttpResponse(response_body, status=status)

    urlpatterns = [
        # use only in debug mode, use nginx rewrite in production
        # see for details
        # .platform/nginx/conf.d/elasticbeanstalk/00_application.conf
        # todo create regex for path string with slashed
        # path(r'e/<uuid:pt_uuid>/<uuid:material_uuid>/<uuid:lesson_uuid>/<path>',
        #     proxy_view, name='eval-production'),
        re_path(r'^e/(?P<pt_uuid>[^/]*)/(?P<material_uuid>[^/]*)/(?P<lesson_uuid>[^/]*)/(?P<path>.*)',
             proxy_view, name='eval-production'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^favicon.ico$',
            RedirectView.as_view(url='/static/curricula/images/favicon/favicon.ico')),
    ] + urlpatterns

# catch all urls in main SPA app
urlpatterns += [path(r'', include('courses.urls', namespace='main')), ]
