from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('fbvisualize.app.views',
	url(r'^$', 'index', name='index'),
	url(r'^callback$', 'callback', name='callback'),
	url(r'^process$', 'process', name='process'),
	# Examples:
    # url(r'^$', 'fbvisualize.views.home', name='home'),
    # url(r'^fbvisualize/', include('fbvisualize.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
