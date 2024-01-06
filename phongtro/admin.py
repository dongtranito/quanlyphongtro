from django.contrib import admin

# Register your models here.

from . import models

admin.site.site_header="Quản Lý Phòng Trọ 9B"

class HoaDonAdmin(admin.ModelAdmin):
    list_display=["ten_phong","tong_cong","trang_thai"]
from django.shortcuts import get_object_or_404

class KhachHangAdmin(admin.ModelAdmin):
    list_display = ["ten", "ten_phong"]
    def save_model(self, request, obj, form, change):
        if obj.pk is None:  # Kiểm tra xem đối tượng có phải là mới hay không
            phong = get_object_or_404(models.Phong,ten_phong=obj.ten_phong)
            phong.trang_thai = 'đã thuê'
            phong.save()
        super().save_model(request, obj, form, change)

    
class PhongAdmin(admin.ModelAdmin):
    list_display=["ten_phong","trang_thai"]

admin.site.register(models.HoaDon,HoaDonAdmin)
admin.site.register(models.KhachHang,KhachHangAdmin)
admin.site.register(models.Phong,PhongAdmin)
admin.site.register(models.ThuePhong)

