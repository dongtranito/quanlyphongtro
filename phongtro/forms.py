from django import forms
from .models import KhachHang

class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = '__all__'  # Lấy tất cả các trường từ model KhachHang


from django import forms
from .models import HoaDon,Phong

class HoaDonForm(forms.ModelForm):
    class Meta:
        model = HoaDon
        fields =['ten_phong', 'so_dien_cuoi', 'so_nuoc_cuoi']

class PhongForm(forms.ModelForm):
    class Meta:
        model = Phong
        exclude = ['chi_so_dien','chi_so_nuoc']


