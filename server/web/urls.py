from django.conf.urls import url

from . import views
from tmdt.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    url(r'^admin', views.index, name='index'),
    url(r'^$', views.home, name='home'),
    url(r'^404/$', views.wrong, name='notfound'),
    url(r'^histories/$', views.histories),
    url(r'^login/$', views.login),
    url(r'^my_account/$', views.my_account),
    url(r'^logout/$', views.logout),
    url(r'^users/$', views.users), 
    url(r'^changepassword/$', views.changepassword),
    url(r'^product/$', views.product),
    url(r'^types/$', views.types),
    url(r'^type/$', views.type),
    url(r'^material/$', views.material),
    url(r'^blog/$', views.blog),
    url(r'^profile/$', views.profile),
    url(r'^privacy/$', views.privacy),
    url(r'^product_detail/$', views.product_detail),
    url(r'^voucher/$', views.voucher),
    url(r'^policy/$', views.policy),
    url(r'^order/$', views.order),
    url(r'^blog_detail/$', views.blog_detail),
    url(r'^cart/$', views.cart),
    url(r'^blogs/$', views.blogs),
    url(r'^shops/$', views.shops),
    url(r'^comments/$', views.comment),
    url(r'^order_review/$', views.order_review),
]
handler404 = views.notfound
