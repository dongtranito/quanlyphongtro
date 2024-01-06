from django.urls import path
from .views import HoaDonListView,HoaDonDeleteView,HoaDonCreateView,HoaDonDetailView,HoaDonUpdateView

from .import views
urlpatterns = [
    path('khachhang/', views.KhachHangListView.as_view(), name='khachhang-list'),
    path('khachhang/new/', views.KhachHangCreateView.as_view(), name='khachhang-new'),
    path('khachhang/<str:khachhang_id>/update/', views.KhachHangUpdateView.as_view(), name='khachhang-update'),
    path('khachhang/<str:khachhang_id>/delete/', views.KhachHangDeleteView.as_view(), name='khachhang-delete'), 

    # path('khachhang/<int:khachhang_id>/', KhachHangDetailView.as_view(), name='khachhang-detail'),
    # path('khachhang/<int:khachhang_id>/delete/', KhachHangDeleteView.as_view(), name='khachhang-delete'),
    # path('hoadon/new/', HoaDonView.as_view(), name='hoadon-new'),



    path('hoadon/', HoaDonListView.as_view(), name='hoadon-list'),
    path('hoadon/<int:hoadon_id>/', HoaDonDetailView.as_view(), name='hoadon-detail'),
    path('hoadon/new/', HoaDonCreateView.as_view(), name='hoadon-new'),
    path('hoadon/<int:hoadon_id>/update/', HoaDonUpdateView.as_view(), name='hoadon-update'),
    path('hoadon/<int:hoadon_id>/delete/', HoaDonDeleteView.as_view(), name='hoadon-delete'), 
   


    path('phong/', views.PhongListView.as_view(), name='phong-list'),
    # path('phong/<str:ten_phong>/', views.PhongDetailView.as_view(), name='phong-detail'),
    path('phong/create/', views.PhongCreateView.as_view(), name='phong-new'),    
    path('phong/<str:ten_phong>/update/', views.PhongUpdateView.as_view(), name='phong-update'),
    path('phong/<str:ten_phong>/delete/', views.PhongDeleteView.as_view(), name='phong-delete'),



    path('tra_phong/<str:ten_phong>/', views.TraPhongView.as_view(), name='tra_phong'),

    path('thanh_toan/<str:hoadon_id>/', views.ThanhToanView.as_view(), name='thanh_toan'),


    path('home', views.HomePageView.as_view(), name='home'),  # URL cho trang chính

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path("",views.quancao.as_view(),name='quancao')
]