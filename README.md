<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP được áp dụng vào học phần Thực tập doanh nghiệp dựa trên mã nguồn mở Odoo. 

Hệ thống Quản lý Khách hàng, Văn bản và Nhân sự được xây dựng nhằm hỗ trợ doanh nghiệp tối ưu hóa công tác quản trị nội bộ và quan hệ khách hàng trong một môi trường làm việc số thống nhất. Thay vì quản lý rời rạc qua các tệp hồ sơ giấy hay file Excel thủ công, hệ thống mang đến một giải pháp tập trung, giúp số hóa toàn bộ hợp đồng, tài liệu pháp lý và hồ sơ nhân sự.

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Các chức năng chính


### 3.1. Module Quản lý khách hàng
#### 1. Quản lý Khách hàng tiềm năng
Đây là giai đoạn "đầu vào", quản lý những khách quan tâm đến dịch vụ nhưng chưa ký hợp đồng.

- Thu thập dữ liệu: Lưu trữ thông tin cơ bản 

- Phân loại giai đoạn: Theo dõi tiến độ từ Tiếp cận -> Đàm phán -> Ký kết/Thất bại.


![alt text](./images/khachhangtiemnang.jpg)

![alt text](./images/khachhangtiemnang2.jpg)

#### 2. Quản lý Khách hàng chính thức 
Khi Lead chốt thành công, hệ thống tự động chuyển đổi sang hồ sơ khách hàng chính thức.

- Đồng bộ hóa dữ liệu: Tự động kế thừa thông tin từ Lead sang bảng Khách hàng (loại bỏ nhập liệu thủ công).

- Cấp mã định danh (ID): Tự động sinh mã khách hàng chuẩn  để quản lý chuyên nghiệp.

- Lưu trữ hồ sơ

![alt text](./images/khachhang.jpg)

#### 3. Quản lý Hợp đồng & Pháp lý

Chức năng cốt lõi để hiện thực hóa doanh thu.

- Theo dõi vòng đời hợp đồng: Quản lý ngày bắt đầu, ngày kết thúc và tự động cảnh báo thời hạn.

- Quản lý thanh toán: Theo dõi trạng thái Chưa thanh toán, Đã thanh toán hoặc Thanh toán một phần.

- Lưu trữ tài liệu: Đính kèm bản quét hợp đồng (PDF/Ảnh) trực tiếp vào hồ sơ để tra cứu nhanh.

![alt text](./images/hopdong.jpg)

![alt text](./images/hopdong2.jpg)

#### 4. Hệ thống Tương tác & Chăm sóc khách hàng (CSKH)
Cầu nối liên lạc giữa doanh nghiệp và khách hàng.

- Gửi Email tự động: Chức năng gửi thông báo phê duyệt hợp đồng với chữ ký chuyên nghiệp (AAHK CSKH).

- Chatter (Thảo luận): Lưu lại toàn bộ lịch sử trao đổi, ghi chú của nhân viên về khách hàng đó.

Quản lý văn bản: Liên kết các hồ sơ pháp lý, báo giá liên quan đến từng khách hàng cụ thể.

![alt text](./images/chamsockhachhang.jpg)

![alt text](./images/mail.jpg)

![alt text](./images/chatter.jpg)

#### 5. Phân tích & Trợ lý ảo AI
Công cụ thông minh giúp nhà quản lý tối ưu hóa vận hành.

Dashboard chuyển đổi: Trực quan hóa 

Trợ lý AI (Gemini): Chatbot thông minh hỗ trợ tư vấn 

![alt text](./images/dashboard.jpg)

### 3.2 Quản lý văn bản

#### 1. Số hóa và Lưu trữ văn bản
Đây là chức năng cơ bản để chuyển đổi các hồ sơ giấy thành dữ liệu số.

- Phân loại văn bản: phân loại theo loại hình (Hợp đồng, Báo giá, Hồ sơ pháp lý, Công văn).

#### 2. Quản lý quy trình Phê duyệt
Kiểm soát trạng thái và tính pháp lý của văn bản trước khi ban hành.

- Theo dõi trạng thái: Cập nhật luồng xử lý từ Dự thảo -> Chờ duyệt -> Đã ký -> Lưu trữ/Hủy bỏ.

- Phân quyền xử lý: Chỉ định rõ ràng nhân viên soạn thảo và cấp quản lý có thẩm quyền phê duyệt.

#### 3. Cảnh báo và Bảo mật
Đảm bảo văn bản luôn được theo dõi sát sao và đúng thời hạn.

- Cảnh báo hết hạn: các văn bản sắp hết hiệu lực hoặc cần tái ký.

- Bảo mật truy cập: Phân quyền chặt chẽ, chỉ những người có liên quan mới được quyền xem hoặc tải tệp đính kèm.

- Lịch sử thay đổi: Ghi lại chi tiết ai đã chỉnh sửa hoặc phê duyệt văn bản vào lúc nào

![alt text](./images/tatcavanban.jpg)

![alt text](./images/vanbanchoduyet.jpg)

![alt text](./images/danhsachvanban.jpg)


# 4. Ghi chú về sự thay đổi kế thừa từ Module QLVB K15

| Thay đổi | Chi tiết |
|---------|---------|
| **Luồng văn bản** | Giữ Công văn đến/đi, mở rộng thêm Văn bản nội bộ. |
| **Thông báo & Chatter** | Tích hợp mail.thread, tự động thông báo và ghi nhận lịch sử xử lý. Giúp tăng tính chủ động – Minh bạch quá trình xử lý |
| **Ràng buộc bảo mật** | Chặn xóa văn bản đã ban hành. Đảm bảo tính pháp lý và toàn vẹn dữ liệu |
| **Workflow chi tiết** | Chia nhỏ trạng thái xử lý văn bản. Kiểm soát rõ trách nhiệm và tiến độ |



# 5. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 5.1. Clone project.

```
git clone https://github.com/THUANH1609/16-06-N5.git
git checkout 
```

## 5.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 5.3. khởi tạo môi trường ảo.

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
python3.10 -m venv ./venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

## 5.4. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo apt install docker-compose
```
```
sudo docker-compose up -d
```

## 5.5. Setup tham số chạy cho hệ thống

- Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

## 5.6 Chạy hệ thống và cài đặt các ứng dụng cần thiết

Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```


Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
    

© 2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---

    
