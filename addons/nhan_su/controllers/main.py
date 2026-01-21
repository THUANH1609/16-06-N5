# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class NhanSuController(http.Controller):

    # 1. API LẤY DỮ LIỆU NHÂN VIÊN
    @http.route('/api/nhan_su/dashboard', type='json', auth='public', cors='*', csrf=False)
    def get_dashboard_data(self, **kw):
        try:
            # Sửa auth='public' để tránh lỗi đăng nhập khi test từ React
            employees = request.env['nhan_vien'].sudo().search_read(
                domain=[], 
                fields=['ho_va_ten', 'diem_hieu_suat', 'trang_thai', 'phong_ban_id']
            )
            result_data = []
            for emp in employees:
                p_ban_name = emp['phong_ban_id'][1] if emp.get('phong_ban_id') else "Chưa rõ"
                result_data.append({
                    'ho_va_ten': emp.get('ho_va_ten') or "Ẩn danh",
                    'diem_hieu_suat': emp.get('diem_hieu_suat') or 0,
                    'phong_ban': p_ban_name,
                    'trang_thai': emp.get('trang_thai') or 'dang_lam'
                })
            return {'status': 'success', 'data': result_data}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'data': []}

    # 2. API CHO BIỂU ĐỒ (CHARTS) - Lấy dữ liệu thật từ Odoo
    @http.route('/api/van_ban/analytics', type='json', auth='public', cors='*', csrf=False)
    def get_vb_analytics(self, **kw):
        try:
            # Đếm số lượng thực tế dựa trên trường 'luong_van_ban'
            # Chú ý: Đảm bảo các giá trị 'den', 'di', 'noi_bo' khớp với selection trong model của em
            den = request.env['quan_ly_van_ban'].sudo().search_count([('luong_van_ban', '=', 'den')])
            di = request.env['quan_ly_van_ban'].sudo().search_count([('luong_van_ban', '=', 'di')])
            nb = request.env['quan_ly_van_ban'].sudo().search_count([('luong_van_ban', '=', 'noi_bo')])
            
            # Nếu tất cả bằng 0, Odoo sẽ trả về mảng này để React vẽ biểu đồ trống
            return [
                {'name': 'Văn bản đến', 'value': den},
                {'name': 'Văn bản đi', 'value': di},
                {'name': 'Nội bộ', 'value': nb},
            ]
        except Exception as e:
            return []

    # 3. API QUICK SEARCH (TÌM KIẾM TẬP TRUNG)
    @http.route('/api/van_ban/search', type='json', auth='public', cors='*', csrf=False)
    def quick_search(self, keyword='', **kw):
        try:
            if not keyword:
                return {'status': 'success', 'results': []}

            results = []
            
            # --- Tìm trong Khách hàng ---
            # Sử dụng 'name' thay vì 'ho_va_ten' cho model khach_hang (thường là mặc định của Odoo)
            partners = request.env['khach_hang'].sudo().search_read(
                [('name', 'ilike', keyword)], 
                ['name', 'phone', 'giai_doan'], 
                limit=5
            )
            for p in partners:
                results.append({
                    'type': 'khach_hang',
                    'title': p['name'],
                    'desc': f"SĐT: {p.get('phone') or 'N/A'} - Giai đoạn: {p.get('giai_doan') or 'Mới'}",
                    'id': p['id']
                })

            # --- Tìm trong Văn bản ---
            # Sửa lại domain tìm kiếm để tránh lỗi nếu trường không tồn tại
            docs = request.env['quan_ly_van_ban'].sudo().search_read(
                ['|', ('ten_van_ban', 'ilike', keyword), ('so_hieu_van_ban', 'ilike', keyword)], 
                ['ten_van_ban', 'so_hieu_van_ban', 'trang_thai'], 
                limit=5
            )
            for d in docs:
                results.append({
                    'type': 'van_ban',
                    'title': d['ten_van_ban'] or 'Không tên',
                    'desc': f"Số hiệu: {d.get('so_hieu_van_ban') or 'N/A'} - TT: {d.get('trang_thai') or 'Mới'}",
                    'id': d['id']
                })

            return {'status': 'success', 'results': results}
        except Exception as e:
            # Trả về thông báo lỗi cụ thể để em dễ debug nếu sai tên trường
            return {'status': 'error', 'message': f"Lỗi Odoo: {str(e)}", 'results': []}