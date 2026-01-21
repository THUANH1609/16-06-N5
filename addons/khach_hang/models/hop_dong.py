# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date

class HopDong(models.Model):
    _name = "hop_dong"
    _description = "Hợp đồng khách hàng"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Thêm để dùng Chatter
    _rec_name = 'so_hop_dong'

    so_hop_dong = fields.Char(string="Số hợp đồng", required=True, copy=False, readonly=True, 
                             default=lambda self: _('Mới'))
    ten = fields.Char(string="Tiêu đề hợp đồng", required=True)
    
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên đại diện")
    
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, default=fields.Date.context_today)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)
    
    gia_tri_hop_dong = fields.Float(string="Giá trị hợp đồng (VNĐ)", required=True)

    thanh_toan = fields.Selection([
        ('chua_thanh_toan', 'Chưa thanh toán'),
        ('da_thanh_toan', 'Đã thanh toán'),
        ('thanh_toan_mot_phan', 'Thanh toán một phần')
    ], string="Trạng thái thanh toán", default='chua_thanh_toan', tracking=True)
    
    trang_thai = fields.Selection([
        ('moi', 'Dự thảo'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy bỏ')
    ], string="Trạng thái", default='moi', copy=False, tracking=True)

    file_hop_dong = fields.Binary(string="Bản quét hợp đồng (PDF/Ảnh)")
    file_name = fields.Char(string="Tên file")
    ghi_chu = fields.Text(string="Ghi chú điều khoản")

    # --- CÁC TRƯỜNG TÍNH TOÁN ĐỂ HIỂN THỊ GIAO DIỆN ĐẸP ---
    display_info_contract = fields.Html(compute='_compute_display_html', string="Thông tin hợp đồng")
    display_customer_info = fields.Html(compute='_compute_display_html', string="Bên A (Khách hàng)")
    display_staff_info = fields.Html(compute='_compute_display_html', string="Bên B (Nhân viên)")

    def _compute_display_html(self):
        for rec in self:
            # 1. Tính toán cột Thông tin hợp đồng
            color = "green" if rec.ngay_ket_thuc and rec.ngay_ket_thuc >= date.today() else "red"
            status_limit = "Còn hạn" if color == "green" else "Hết hạn"
            rec.display_info_contract = f"""
                <div>
                    <strong style="color: #2c3e50; font-size: 14px;">{rec.ten}</strong><br/>
                    <span style="color: #7f8c8d; font-size: 12px;">ID: {rec.so_hop_dong}</span><br/>
                    <span style="color: {color}; font-size: 11px; border: 1px solid {color}; padding: 0px 5px; border-radius: 3px;">
                        ● {status_limit}
                    </span>
                </div>
            """

            # 2. Tính toán cột Bên A (Khách hàng)
            customer_name = rec.khach_hang_id.name or "N/A"
            customer_phone = rec.khach_hang_id.phone or "Chưa có SĐT"
            rec.display_customer_info = f"""
                <div>
                    <i class="fa fa-user" style="color: #3498db;"></i> <b>{customer_name}</b><br/>
                    <small style="color: #95a5a6;">📞 {customer_phone}</small>
                </div>
            """

            # 3. Tính toán cột Bên B (Nhân viên)
            staff_name = rec.nhan_vien_id.ho_va_ten or "Chưa phân công"
            staff_job = rec.nhan_vien_id.chuc_vu or "Nhân viên"
            staff_dept = rec.nhan_vien_id.phong_ban_id.ten_phong_ban or "Kinh doanh"
            
            rec.display_staff_info = f"""
                <div>
                    <i class="fa fa-briefcase" style="color: #e67e22;"></i> <b>{staff_name}</b><br/>
                    <small style="color: #95a5a6;">{staff_job} - {staff_dept}</small>
                </div>
            """

    # --- TÍNH NĂNG GỬI EMAIL HỢP ĐỒNG ---
    def action_send_contract_email(self):
        self.ensure_one()
        if not self.khach_hang_id.email:
            raise ValidationError(_("Khách hàng này chưa có địa chỉ email!"))
        
        # Xác định tên người gửi (Ưu tiên nhân viên phụ trách, sau đó là người dùng hiện tại)
        sender_name = self.nhan_vien_id.ho_va_ten or self.env.user.name or 'Ban Quản trị'

        # Tạo nội dung email chuyên nghiệp
        body_html = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6;">
                <h2 style="color: #2c3e50;">Xác nhận Phê duyệt Hợp đồng</h2>
                <p>Kính chào quý khách <b>{self.khach_hang_id.name}</b>,</p>
                <p>Công ty <b>AAHK</b> xin trân trọng thông báo hợp đồng của quý khách đã được phê duyệt chính thức:</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 15px 0;">
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li><b>Mã số:</b> {self.so_hop_dong}</li>
                        <li><b>Dịch vụ:</b> {self.ten}</li>
                        <li><b>Giá trị:</b> <span style="color: #e74c3c; font-weight: bold;">{self.gia_tri_hop_dong:,.0f} VNĐ</span></li>
                        <li><b>Thời hạn:</b> {self.ngay_bat_dau} đến {self.ngay_ket_thuc}</li>
                    </ul>
                </div>
                
                <p>Vui lòng kiểm tra file đính kèm để xem chi tiết các điều khoản. Nếu có thắc mắc, quý khách có thể phản hồi trực tiếp qua email này.</p>
                
                <p style="margin-top: 25px;">Trân trọng,</p>
                <div>
                    <strong style="font-size: 15px; color: #2c3e50;">{sender_name}</strong><br/>
                    <span style="color: #7f8c8d;">Bộ phận Chăm sóc khách hàng - AAHK CSKH</span>
                </div>
            </div>
        """
        
        mail_values = {
            'subject': f'[AAHK] Xác nhận Hợp đồng {self.so_hop_dong} - {self.ten}',
            'body_html': body_html,
            'email_to': self.khach_hang_id.email,
            # 👇 Cấu hình tên hiển thị + Email gửi/nhận như em yêu cầu
            'email_from': 'AAHK CSKH <khanhhuyen8324@gmail.com>',
            'reply_to': 'AAHK CSKH <khanhhuyen8324@gmail.com>',
        }
        
        # Đính kèm file hợp đồng nếu có
        if self.file_hop_dong:
            attachment = self.env['ir.attachment'].create({
                'name': self.file_name or f'Hop_dong_{self.so_hop_dong}.pdf',
                'type': 'binary',
                'datas': self.file_hop_dong,
                'res_model': 'hop_dong',
                'res_id': self.id,
            })
            mail_values['attachment_ids'] = [(4, attachment.id)]

        # Tạo và gửi mail
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
        
        # Ghi chú vào Chatter
        self.message_post(body=f"✅ Đã gửi email xác nhận hợp đồng đến {self.khach_hang_id.name} (Gửi bởi: {self.env.user.name})")
        return True

    # --- LOGIC TỰ ĐỘNG ---
    @api.model
    def create(self, vals):
        if vals.get('so_hop_dong', _('Mới')) == _('Mới'):
            vals['so_hop_dong'] = self.env['ir.sequence'].next_by_code('hop_dong.code') or _('Mới')
        return super(HopDong, self).create(vals)

    @api.onchange('ngay_bat_dau')
    def _onchange_ngay_bat_dau(self):
        if self.ngay_bat_dau:
            self.ngay_ket_thuc = fields.Date.to_date(self.ngay_bat_dau) + relativedelta(years=1)

    # --- RÀNG BUỘC ---
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay_hop_dong(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau and record.ngay_ket_thuc <= record.ngay_bat_dau:
                raise ValidationError(_("Ngày kết thúc phải sau ngày bắt đầu."))

    @api.constrains('gia_tri_hop_dong')
    def _check_gia_tri(self):
        for record in self:
            if record.gia_tri_hop_dong <= 0:
                raise ValidationError(_("Giá trị hợp đồng phải là số dương."))
# # -*- coding: utf-8 -*-
# from odoo import _, api, fields, models
# from odoo.exceptions import ValidationError
# from dateutil.relativedelta import relativedelta
# from datetime import date

# class HopDong(models.Model):
#     _name = "hop_dong"
#     _description = "Hợp đồng khách hàng"
#     _inherit = ['mail.thread', 'mail.activity.mixin'] # Thêm để dùng Chatter
#     _rec_name = 'so_hop_dong'

#     so_hop_dong = fields.Char(string="Số hợp đồng", required=True, copy=False, readonly=True, 
#                              default=lambda self: _('Mới'))
#     ten = fields.Char(string="Tiêu đề hợp đồng", required=True)
    
#     khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True, ondelete='cascade')
#     nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên đại diện")
    
#     ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, default=fields.Date.context_today)
#     ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)
    
#     gia_tri_hop_dong = fields.Float(string="Giá trị hợp đồng (VNĐ)", required=True)

#     thanh_toan = fields.Selection([
#         ('chua_thanh_toan', 'Chưa thanh toán'),
#         ('da_thanh_toan', 'Đã thanh toán'),
#         ('thanh_toan_mot_phan', 'Thanh toán một phần')
#     ], string="Trạng thái thanh toán", default='chua_thanh_toan', tracking=True)
    
#     trang_thai = fields.Selection([
#         ('moi', 'Dự thảo'),
#         ('dang_thuc_hien', 'Đang thực hiện'),
#         ('hoan_thanh', 'Hoàn thành'),
#         ('huy', 'Hủy bỏ')
#     ], string="Trạng thái", default='moi', copy=False, tracking=True)

#     file_hop_dong = fields.Binary(string="Bản quét hợp đồng (PDF/Ảnh)")
#     file_name = fields.Char(string="Tên file")
#     ghi_chu = fields.Text(string="Ghi chú điều khoản")

#     # --- CÁC TRƯỜNG TÍNH TOÁN ĐỂ HIỂN THỊ GIAO DIỆN ĐẸP ---
#     display_info_contract = fields.Html(compute='_compute_display_html', string="Thông tin hợp đồng")
#     display_customer_info = fields.Html(compute='_compute_display_html', string="Bên A (Khách hàng)")
#     display_staff_info = fields.Html(compute='_compute_display_html', string="Bên B (Nhân viên)")

#     def _compute_display_html(self):
#         for rec in self:
#             # 1. Tính toán cột Thông tin hợp đồng (Tên + Số + Icon hạn)
#             color = "green" if rec.ngay_ket_thuc and rec.ngay_ket_thuc >= date.today() else "red"
#             status_limit = "Còn hạn" if color == "green" else "Hết hạn"
#             rec.display_info_contract = f"""
#                 <div>
#                     <strong style="color: #2c3e50; font-size: 14px;">{rec.ten}</strong><br/>
#                     <span style="color: #7f8c8d; font-size: 12px;">ID: {rec.so_hop_dong}</span><br/>
#                     <span style="color: {color}; font-size: 11px; border: 1px solid {color}; padding: 0px 5px; border-radius: 3px;">
#                         ● {status_limit}
#                     </span>
#                 </div>
#             """

#             # 2. Tính toán cột Bên A (Khách hàng)
#             customer_name = rec.khach_hang_id.name or "N/A"
#             customer_phone = rec.khach_hang_id.phone or "Chưa có SĐT"
#             rec.display_customer_info = f"""
#                 <div>
#                     <i class="fa fa-user" style="color: #3498db;"></i> <b>{customer_name}</b><br/>
#                     <small style="color: #95a5a6;">📞 {customer_phone}</small>
#                 </div>
#             """

#             # 3. Tính toán cột Bên B (Nhân viên)
#             staff_name = rec.nhan_vien_id.ho_va_ten or "Chưa phân công"
#             staff_job = rec.nhan_vien_id.chuc_vu or "Nhân viên"
#             staff_dept = rec.nhan_vien_id.phong_ban_id.ten_phong_ban or "Kinh doanh"
            
#             rec.display_staff_info = f"""
#                 <div>
#                     <i class="fa fa-briefcase" style="color: #e67e22;"></i> <b>{staff_name}</b><br/>
#                     <small style="color: #95a5a6;">{staff_job} - {staff_dept}</small>
#                 </div>
#             """

#     # --- TÍNH NĂNG GỬI EMAIL HỢP ĐỒNG ---
#     def action_send_contract_email(self):
#         self.ensure_one()
#         if not self.khach_hang_id.email:
#             raise ValidationError(_("Khách hàng này chưa có địa chỉ email!"))
        
#         # Tạo nội dung email chuyên nghiệp
#         body_html = f"""
#             <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #333;">
#                 <p>Chào chị <b>{self.khach_hang_id.name}</b>,</p>
#                 <p>Công ty AAHK xin gửi tới chị thông tin hợp đồng đã được phê duyệt:</p>
#                 <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 10px 0;">
#                     <ul style="list-style: none; padding: 0;">
#                         <li><b>Số hợp đồng:</b> {self.so_hop_dong}</li>
#                         <li><b>Dịch vụ:</b> {self.ten}</li>
#                         <li><b>Giá trị:</b> {self.gia_tri_hop_dong:,.0f} VNĐ</li>
#                         <li><b>Thời hạn:</b> {self.ngay_bat_dau} đến {self.ngay_ket_thuc}</li>
#                     </ul>
#                 </div>
#                 <p>Vui lòng kiểm tra các điều khoản đính kèm. Nếu có bất kỳ thắc mắc nào, chị có thể phản hồi trực tiếp qua email này hoặc gửi yêu cầu hỗ trợ lên hệ thống của chúng tôi.</p>
#                 <p>Trân trọng,</p>
#                 <p><b>{self.nhan_vien_id.ho_va_ten or 'Ban Quản trị Gemini'}</b></p>
#             </div>
#         """
        
#         mail_values = {
#             'subject': f'[Xác nhận] Hợp đồng {self.so_hop_dong} - {self.ten}',
#             'body_html': body_html,
#             'email_to': self.khach_hang_id.email,
#         }
        
#         # Nếu có file đính kèm thì đính vào mail luôn
#         if self.file_hop_dong:
#             attachment = self.env['ir.attachment'].create({
#                 'name': self.file_name or f'Hop_dong_{self.so_hop_dong}.pdf',
#                 'type': 'binary',
#                 'datas': self.file_hop_dong,
#                 'res_model': 'hop_dong',
#                 'res_id': self.id,
#             })
#             mail_values['attachment_ids'] = [(4, attachment.id)]

#         mail = self.env['mail.mail'].create(mail_values)
#         mail.send()
        
#         # Thông báo vào phần Chatter để theo dõi
#         self.message_post(body=f"Đã gửi email hợp đồng cho khách hàng {self.khach_hang_id.name}")
#         return True

#     # --- LOGIC TỰ ĐỘNG ---
#     @api.model
#     def create(self, vals):
#         if vals.get('so_hop_dong', _('Mới')) == _('Mới'):
#             vals['so_hop_dong'] = self.env['ir.sequence'].next_by_code('hop_dong.code') or _('Mới')
#         return super(HopDong, self).create(vals)

#     @api.onchange('ngay_bat_dau')
#     def _onchange_ngay_bat_dau(self):
#         if self.ngay_bat_dau:
#             self.ngay_ket_thuc = fields.Date.to_date(self.ngay_bat_dau) + relativedelta(years=1)

#     # --- RÀNG BUỘC ---
#     @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
#     def _check_ngay_hop_dong(self):
#         for record in self:
#             if record.ngay_ket_thuc and record.ngay_bat_dau and record.ngay_ket_thuc <= record.ngay_bat_dau:
#                 raise ValidationError(_("Ngày kết thúc phải sau ngày bắt đầu."))

#     @api.constrains('gia_tri_hop_dong')
#     def _check_gia_tri(self):
#         for record in self:
#             if record.gia_tri_hop_dong <= 0:
#                 raise ValidationError(_("Giá trị hợp đồng phải là số dương."))
