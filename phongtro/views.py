from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import KhachHang, ThuePhong, HoaDon,Phong 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import KhachHangForm,PhongForm
from datetime import datetime 


class KhachHangListView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/khachhang_list.html'  # Thay 'ten_template_cua_ban.html' bằng tên template của bạn.

    def get(self, request):
        khachhang_list = KhachHang.objects.all()
        context = {'khachhang_list': khachhang_list}
        return render(request, self.template_name, context)


class KhachHangCreateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/khachhang_form.html'  # Đường dẫn đến template cho form tạo khách hàng

    def get(self, request):
        form = KhachHangForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = KhachHangForm(request.POST)
        if form.is_valid():
            khach_hang = form.save()
            ten_phong = khach_hang.ten_phong
            phong = get_object_or_404(Phong, ten_phong=ten_phong)
    
            if phong.trang_thai=="trống":
                thue_phong=ThuePhong()
                thue_phong.ten_phong=phong
                phong.trang_thai = 'đã thuê'
                phong.save()
                thue_phong.tien_no=0
                thue_phong.ngay_dat=datetime.now()
                thue_phong.so_dien_thoai_nhan_hoa_don=khach_hang.so_dien_thoai
                thue_phong.ten_phong=phong
                thue_phong.save()

            return redirect('/khachhang/')  # URL chuyển hướng sau khi tạo khách hàng thành công
        
        return render(request, self.template_name, {'form': form})


class KhachHangUpdateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/khachhang_form.html'

    def get(self, request, khachhang_id):
        khachhang = get_object_or_404(KhachHang, pk=khachhang_id)
        form = KhachHangForm(instance=khachhang)
        return render(request, self.template_name, {'form': form})

    def post(self, request, khachhang_id):
        khachhang = get_object_or_404(KhachHang, pk=khachhang_id)
        form = KhachHangForm(request.POST, instance=khachhang)
        if form.is_valid():
            form.save()
            return redirect('/khachhang/')
        return render(request, self.template_name, {'form': form})


class KhachHangDeleteView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/khachhang_confirm_delete.html'

    def get(self, request, khachhang_id):
        khachhang = get_object_or_404(KhachHang, pk=khachhang_id)
        return render(request, self.template_name, {'khachhang': khachhang})

    def post(self, request, khachhang_id):
        khachhang = get_object_or_404(KhachHang, pk=khachhang_id)
        khachhang.delete()
        return redirect('/khachhang/')








from .forms import HoaDonForm    

class HoaDonListView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/hoadon_list.html'

    def get(self, request):
        hoadon_list = HoaDon.objects.all()
        return render(request, self.template_name, {'hoadon_list': hoadon_list})


class HoaDonDetailView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/hoadon_detail.html'

    def get(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        return render(request, self.template_name, {'hoadon': hoadon, 'form': HoaDonForm(instance=hoadon)})

    def post(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        form = HoaDonForm(request.POST, instance=hoadon)
        if form.is_valid():
            form.save()
            return redirect('hoadon-list')
        return HttpResponse('Lỗi: Dữ liệu không hợp lệ')


class HoaDonCreateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/hoadon_form.html'  # Tên template cho trang tạo hóa đơn

    def get(self, request):
        # Hiển thị form tạo hóa đơn trống
        form = HoaDonForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Xử lý việc gửi form tạo hóa đơn
        form = HoaDonForm(request.POST)
        if form.is_valid():
            ngay_hien_tai = datetime.now()
            phong = Phong.objects.get(ten_phong=form.instance.ten_phong) 
            if phong.trang_thai=="trống":
                return HttpResponse("Phòng trống không tạo hóa đơn được")
            thuephong = ThuePhong.objects.get(ten_phong=form.instance.ten_phong)

            so_dien_dau = phong.chi_so_dien  # Di chuyển phần này lên đầu
            so_nuoc_dau = phong.chi_so_nuoc  # Di chuyển phần này lên đầu

            phong.chi_so_dien = form.instance.so_dien_cuoi
            phong.chi_so_nuoc = form.instance.so_nuoc_cuoi
            
           

            gia_dien = phong.gia_dien
            gia_nuoc = phong.gia_nuoc
            tien_dien = (form.instance.so_dien_cuoi - so_dien_dau) * gia_dien
            tien_nuoc = (form.instance.so_nuoc_cuoi - so_nuoc_dau) * gia_nuoc
            

            thuephong.tien_no = thuephong.tien_no + phong.gia_phong + tien_dien + tien_nuoc
            thuephong.save()
            tong_tien =  thuephong.tien_no

            form.instance.so_dien_dau = so_dien_dau
            form.instance.so_nuoc_dau = so_nuoc_dau
            form.instance.tien_dien = tien_dien
            form.instance.tong_tien_nuoc = tien_nuoc
            form.instance.tong_cong = tong_tien
            form.instance.ngay_co_hoa_don = ngay_hien_tai

            phong.save()
            form.save()
            return redirect('hoadon-list')  # Chuyển hướng đến danh sách hóa đơn hoặc trang khác nếu cần

        # Trong trường hợp form không hợp lệ, bạn có thể xử lý lỗi ở đây
        return HttpResponse("lỗi form không hợp lệ")

    

class HoaDonUpdateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/hoadon_form.html'

    def get(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        form = HoaDonForm(instance=hoadon)
        return render(request, self.template_name, {'form': form})

    def post(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        form = HoaDonForm(request.POST, instance=hoadon)
        if form.is_valid():
            form.save()
            return redirect('hoadon-list')
        return render(request, self.template_name, {'form': form})

class HoaDonDeleteView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/hoadon_confirm_delete.html'

    def get(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        return render(request, self.template_name, {'hoadon': hoadon})

    def post(self, request, hoadon_id):
        hoadon = get_object_or_404(HoaDon, pk=hoadon_id)
        hoadon.delete()
        return redirect('hoadon-list')
    








class PhongListView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/phong_list.html'

    def get(self, request):
        phong_list = Phong.objects.all()
        context = {'phong_list': phong_list}
        return render(request, self.template_name, context)



from .forms import PhongForm  # Đảm bảo bạn đã tạo một form cho mô hình "Phong"

class PhongCreateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/phong_form.html'  # Đường dẫn đến template cho form tạo phòng

    def get(self, request):
        form = PhongForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/phong/')  # URL chuyển hướng sau khi tạo phòng thành công
        
        return render(request, self.template_name, {'form': form})
    


class PhongUpdateView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/phong_form.html'  # Đường dẫn đến template cho form sửa phòng

    def get(self, request, ten_phong):
        phong = Phong.objects.get(ten_phong=ten_phong)
        form = PhongForm(instance=phong)
        return render(request, self.template_name, {'form': form})

    def post(self, request, ten_phong):
        phong = Phong.objects.get(ten_phong=ten_phong)
        form = PhongForm(request.POST, request.FILES, instance=phong)
        if form.is_valid():
            form.save()
            return redirect('/phong/')  # URL chuyển hướng sau khi sửa phòng thành công
        return render(request, self.template_name, {'form': form})
    

class PhongDeleteView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/phong_confirm_delete.html'  # Đường dẫn đến template xác nhận xóa phòng

    def get(self, request, ten_phong):
        phong = Phong.objects.get(ten_phong=ten_phong)
        return render(request, self.template_name, {'phong': phong})

    def post(self, request, ten_phong):
        phong = Phong.objects.get(ten_phong=ten_phong)
        phong.delete()
        return redirect('/phong/')  # URL chuyển hướng sau khi xóa phòng thành công
    








class TraPhongView(LoginRequiredMixin,View):
    login_url="/login"

    template_name = 'phongtro/confirm_traphong.html'
    def get(self, request, ten_phong):
        try:
            phong = Phong.objects.get(ten_phong=ten_phong)
            if phong.trang_thai == 'đã thuê':
                return render(request, self.template_name, {'phong': phong})
            else:
                return HttpResponse("Phòng không ở trạng thái đã thuê.")
        except Phong.DoesNotExist:
            return HttpResponse("Phòng không tồn tại.")

    def post(self, request, ten_phong):
        
            phong = Phong.objects.get(ten_phong=ten_phong)
            phong.trang_thai = 'trống'
            phong.save()
            KhachHang.objects.filter(ten_phong=phong).delete()
                # Xóa các đối tượng ThuePhong liên quan
            ThuePhong.objects.filter(ten_phong=phong).delete()
            HoaDon.objects.filter(ten_phong=phong).delete()
            # Thực hiện các công việc khác liên quan đến việc trả phòng (ví dụ: tạo hóa đơn, cập nhật thông tin khách hàng, v.v.)
            return redirect('/phong/')  # Chuyển hướng đến trang danh sách phòng sau khi trả phòng thành công
        





class ThanhToanView(LoginRequiredMixin,View):
    login_url="/login"
    template_name = 'phongtro/confirm_thanhtoan.html'

    def get(self, request, hoadon_id):
        
        try:
            hoadon = HoaDon.objects.get(id=hoadon_id)
            if hoadon.trang_thai == 'chưa thanh toán':
                return render(request, self.template_name, {'hoa_don': hoadon})
            else:
                return HttpResponse("Hóa đơn đã thanh toán rồi")
        except HoaDon.DoesNotExist:
            return HttpResponse("Hóa đơn không tồn tại.")


    def post(self, request,hoadon_id):
            hoadon = HoaDon.objects.get(id=hoadon_id)
            hoadon.trang_thai="đã thanh toán"
            thuephong=ThuePhong.objects.get(ten_phong=hoadon.ten_phong)
            thuephong.tien_no=0
            thuephong.save()
            hoadon.ngay_thanh_toan=datetime.now()
            hoadon.save()

            return redirect('/hoadon/') 




from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Sau khi đăng nhập thành công, chuyển hướng người dùng đến trang khác
            return redirect('home')  # Thay 'home' bằng tên URL pattern của trang chào mừng của bạn
    else:
        form = AuthenticationForm()
    return render(request, 'phongtro/login.html', {'form': form})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/login')  # Thay 'home' bằng tên URL pattern của trang chào mừng hoặc trang bạn muốn chuyển hướng người dùng đến sau khi đăng xuất.


from django.shortcuts import render
from .models import Phong

class HomePageView (LoginRequiredMixin,View):
    login_url="/login"
    def get(self,request):
        # Lấy danh sách phòng và thông tin liên quan
        danh_sach_phong = Phong.objects.all().order_by('ten_phong')

        # Tạo danh sách dữ liệu tổng quan
        tong_quan_du_lieu = []
        
        for phong in danh_sach_phong:
            thuephong_moi_nhat = phong.thuephong_set.latest('ngay_dat') if phong.thuephong_set.exists() else None
            hoadon_moi_nhat = phong.hoadon_set.latest('ngay_co_hoa_don') if phong.hoadon_set.exists() else None
            
            # Tạo một bản ghi tổng quan cho từng phòng
            tong_quan_phong = {
                'ten_phong': phong.ten_phong,
                'trang_thai': phong.trang_thai,
                'so_dien_thoai_nhan_hoa_don':thuephong_moi_nhat.so_dien_thoai_nhan_hoa_don if thuephong_moi_nhat else "====",
                'ngay_dat': thuephong_moi_nhat.ngay_dat if thuephong_moi_nhat else "====",
                'trang_thai_thanh_toan': hoadon_moi_nhat.trang_thai if hoadon_moi_nhat else "====",
                
            }
            
            tong_quan_du_lieu.append(tong_quan_phong)

        return render(request, 'phongtro/homepage.html', {'tong_quan_du_lieu': tong_quan_du_lieu})


class quancao(View):

    def get (self, request):
        return render(request, "phongtro/index.html")