from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^user/login$', views.login, name='login'),
    url(r'^user/logout$', views.logout, name='logout'),    
    url(r'^user/changePassword$', views.ChangePassword, name='ChangePassword'),
    url(r'^user/get$', views.GetUser),
    url(r'^user/gets$', views.GetUserList),
    url(r'^user/update$', views.UpdateUser),
    url(r'^user/delete$', views.DeleteUser),
    url(r'^user/checkViewAble$', views.CheckViewAbleUser),
    url(r'^user/sendOTP$', views.MissPassword),
    url(r'^user/checkOTP$', views.CheckOTPPassword),
    url(r'^product/update$', views.UpdateProduct),
    url(r'^product/gets$', views.GetProductList),
    url(r'^product/delete$', views.DeleteProduct),
    url(r'^voucher/update$', views.UpdateVoucher),
    url(r'^voucher/gets$', views.GetVoucherList),
    url(r'^voucher/delete$', views.DeleteVoucher),
    url(r'^order/add$', views.CreateOrder),
    url(r'^order/getMyNew$', views.GetMyNewOrderList),
    url(r'^order/getMyOrder$', views.GetMyOrderList),
    url(r'^order/updatePay$', views.UpdatePayOrder),
    url(r'^order/confirm$', views.ConfirmOrder),
    url(r'^order/gets$', views.GetOrderList),
    url(r'^order/delete$', views.DeleteOrder),
    url(r'^order/buy$', views.BuyOrder),
    url(r'^order/completed$', views.CompletedOrder),
    url(r'^evaluate/update$', views.UpdateEvaluate),
    url(r'^evaluate/gets$', views.GetEvaluateList),
    url(r'^evaluate/delete$', views.DeleteEvaluate),
    url(r'^shop/update$', views.UpdateShop),
    url(r'^shop/gets$', views.GetShopList),
    url(r'^shop/delete$', views.DeleteShop),
    url(r'^shop/get$', views.GetShop),
]