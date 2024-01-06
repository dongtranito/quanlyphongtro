from django.db import models

# Create your models here.

class Phong(models.Model):
    ten_phong = models.CharField(max_length=100,primary_key=True)
    gia_phong = models.IntegerField()
    gia_nuoc = models.IntegerField()
    gia_dien = models.IntegerField()
    mo_ta = models.TextField()
    anh_phong = models.ImageField(upload_to='images/',blank=True)
    tien_coc = models.DecimalField(max_digits=10, decimal_places=2)
    TRANG_THAI_CHOICES = [('trống', 'Trống'), ('đã thuê', 'Đã Thuê')]
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES, default='trống')
    chi_so_dien =models.IntegerField(default=0)
    chi_so_nuoc =models.IntegerField(default=0)

    def __str__(self):
        return self.ten_phong

class KhachHang(models.Model):
    ten_phong = models.ForeignKey(Phong, on_delete=models.CASCADE)
    ten = models.CharField(max_length=100)
    can_cuoc = models.CharField(max_length=12)
    bien_so_xe = models.CharField(max_length=10,blank=True)
    so_dien_thoai = models.CharField(max_length=10)
    van_tay = models.CharField(max_length=100,blank=True,default="chưa có")

    def __str__(self):
        return self.ten

class ThuePhong(models.Model):
    ten_phong = models.ForeignKey(Phong, on_delete=models.CASCADE)
    ngay_dat = models.DateField()
    tien_no = models.DecimalField(max_digits=10, decimal_places=2)
    so_dien_thoai_nhan_hoa_don = models.CharField(max_length=10)

    def __str__(self):
        return f'Phong {self.ten_phong}'

class HoaDon(models.Model):
    ten_phong = models.ForeignKey(Phong, on_delete=models.CASCADE)
    ngay_co_hoa_don = models.DateField(blank=True)
    ngay_thanh_toan = models.DateField(blank=True,null=True)
    TRANG_THAI_CHOICES = [('chưa thanh toán', 'Chưa Thanh Toán'), ('đã thanh toán', 'Đã Thanh Toán')]
    trang_thai = models.CharField(max_length=15, choices=TRANG_THAI_CHOICES, default='chưa thanh toán')
    so_dien_dau = models.IntegerField(blank=True)
    so_dien_cuoi = models.IntegerField()
    tien_dien = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    so_nuoc_dau = models.IntegerField(blank=True)
    so_nuoc_cuoi = models.IntegerField()
    tong_tien_nuoc = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=20000)
    tong_cong=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

    def __str__(self):
        return f'Hóa Đơn Phòng {self.ten_phong}'