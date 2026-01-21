import axios from 'axios';

const ODOO_URL = 'http://localhost:8069'; // Link Odoo của em
// Thay đổi dòng này
// const AI_GATEWAY_URL = 'http://127.0.0.1:5000';
const AI_GATEWAY_URL = 'http://localhost:5000';


export const OdooService = {
  // 1. Tìm kiếm và lấy danh sách văn bản (Dữ liệu từ Odoo)
  // Trong OdooService.js
    quickSearch: async () => {
        try {
            // Gọi qua Node.js (Port 5000) để không bị lỗi CORS
            const res = await axios.get('http://localhost:5000/api/odoo-docs');
            return res.data || [];
        } catch (e) { return []; }
    },

  // 2. Lấy dữ liệu biểu đồ (Dữ liệu từ Odoo)
  getAnalytics: async () => {
    try {
      const res = await axios.post(`${ODOO_URL}/api/van_ban/analytics`, {jsonrpc: "2.0", params: {}});
      return res.data.result || [];
    } catch (e) { return []; }
  },

  // 3. Lấy dữ liệu nhân sự (Dữ liệu từ Odoo)
  getEmployees: async () => {
    try {
      const res = await axios.post(`${ODOO_URL}/api/nhan_su/dashboard`, {jsonrpc: "2.0", params: {}});
      return res.data.result?.data || [];
    } catch (e) { return []; }
  },

  // 4. Hàm tổng hợp (Thống kê Dashboard)
  getDashboardStats: async function() {
    try {
      const allDocs = await this.quickSearch('');
      const analytics = await this.getAnalytics();
      const employees = await this.getEmployees();
      
      return {
        recentDocs: allDocs.filter(d => d.type === 'van_ban'),
        totalDocs: analytics.reduce((sum, item) => sum + item.value, 0) || allDocs.length,
        totalStaff: employees.length
      };
    } catch (e) { return { recentDocs: [], totalDocs: 0, totalStaff: 0 }; }
  },

  // --- MỚI: HÀM GỌI AI TÓM TẮT (Dữ liệu từ Trạm trung chuyển Node.js) ---
  getAISummary: async (title, content) => {
    try {
      const res = await axios.post(`${AI_GATEWAY_URL}/api/ai-summary`, {
        title: title,
        content: content
      });
      return res.data.summary; // Trả về đoạn tóm tắt 3 dòng từ Gemini
    } catch (e) {
      console.error("Lỗi gọi AI:", e);
      return "Không thể kết nối với trí tuệ nhân tạo. Vui lòng kiểm tra Server Backend (Port 5000).";
    }
  }
};

