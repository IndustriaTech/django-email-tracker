try:
    from django.urls import url, include
except ImportError:
    from django.conf.urls import url, include

from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
