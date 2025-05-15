# we need to include new view here
from .user import login, logout, GetUser, ChangePassword, ResetPassword, CheckOTPPassword, MissPassword, GetUserList, UpdateUser, DeleteUser, CheckViewAbleUser
# from .history import GetHistoryList
from .product import UpdateProduct, GetProductList, DeleteProduct
# from .activity import  GetActivityList, AddActivity
from .voucher import GetVoucherList, UpdateVoucher, DeleteVoucher
from .evaluate import GetEvaluateList, UpdateEvaluate, DeleteEvaluate
from .shop import GetShopList, UpdateShop, DeleteShop, GetShop
from .order import CreateOrder, GetMyNewOrderList, CompletedOrder, DeleteOrder, UpdatePayOrder, ConfirmOrder, GetOrderList, GetMyOrderList, BuyOrder