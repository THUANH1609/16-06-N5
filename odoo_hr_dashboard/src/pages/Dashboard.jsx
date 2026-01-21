import React, { useEffect, useState, useRef } from 'react';
import { ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import { ChevronLeft, ChevronRight, Calendar, ChevronDown, Search } from 'lucide-react'; // Nếu bạn chưa cài lucide-react, có thể dùng icon text hoặc svg thường. Ở đây mình dùng SVG trực tiếp để không cần cài thêm lib.

// --- ICONS (SVG) ĐỂ KHÔNG CẦN CÀI THƯ VIỆN NGOÀI ---
const IconCalendar = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
);
const IconChevronDown = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
);
const IconChevronLeft = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
);
const IconChevronRight = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
);

// --- COMPONENT BỘ LỌC THÔNG MINH (SMART TIME FILTER) ---
const SmartTimeFilter = ({ onFilterChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLabel, setSelectedLabel] = useState("Tháng này");
  const [viewYear, setViewYear] = useState(new Date().getFullYear());
  const filterRef = useRef(null);

  // Đóng dropdown khi click ra ngoài
  useEffect(() => {
    function handleClickOutside(event) {
      if (filterRef.current && !filterRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [filterRef]);

  const handlePreset = (type) => {
    const now = new Date();
    let label = "";
    let month = "";
    let year = now.getFullYear();

    switch (type) {
      case 'this_month':
        month = now.getMonth() + 1;
        label = "Tháng này";
        break;
      case 'last_month':
        if (now.getMonth() === 0) {
          month = 12;
          year = now.getFullYear() - 1;
        } else {
          month = now.getMonth();
        }
        label = "Tháng trước";
        break;
      case 'this_year':
        month = ""; // Tất cả các tháng
        label = "Năm nay";
        break;
      default:
        break;
    }

    setSelectedLabel(label === "Năm nay" ? `Năm ${year}` : `Tháng ${month}/${year}`);
    setViewYear(year);
    onFilterChange(month, year);
    setIsOpen(false);
  };

  const handleSelectSpecific = (m, y) => {
    setSelectedLabel(`Tháng ${m}/${y}`);
    onFilterChange(m, y);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={filterRef}>
      {/* NÚT KÍCH HOẠT (TRIGGER BUTTON) */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 bg-white border border-slate-200 hover:border-emerald-500 text-slate-700 px-4 py-2 rounded-lg shadow-sm transition-all min-w-[180px] justify-between group"
      >
        <div className="flex items-center gap-2">
            <span className="text-emerald-600"><IconCalendar /></span>
            <span className="text-sm font-bold">{selectedLabel}</span>
        </div>
        <span className="text-slate-400 group-hover:text-emerald-500"><IconChevronDown /></span>
      </button>

      {/* MENU SỔ XUỐNG (DROPDOWN PANEL) */}
      {isOpen && (
        <div className="absolute top-12 left-0 bg-white rounded-xl shadow-2xl border border-slate-100 z-50 flex overflow-hidden animate-fade-in-up w-[480px]">
            {/* CỘT TRÁI: PRESETS */}
            <div className="w-1/3 bg-slate-50 border-r border-slate-100 p-2 space-y-1">
                <div className="text-[10px] font-bold text-slate-400 uppercase px-3 py-2">Chọn nhanh</div>
                <button onClick={() => handlePreset('this_month')} className="w-full text-left text-xs font-bold text-slate-600 hover:bg-white hover:text-emerald-600 hover:shadow-sm px-3 py-2 rounded-lg transition-all">
                    Tháng này
                </button>
                <button onClick={() => handlePreset('last_month')} className="w-full text-left text-xs font-bold text-slate-600 hover:bg-white hover:text-emerald-600 hover:shadow-sm px-3 py-2 rounded-lg transition-all">
                    Tháng trước
                </button>
                <div className="border-t border-slate-200 my-1"></div>
                 <button onClick={() => handlePreset('this_year')} className="w-full text-left text-xs font-bold text-slate-600 hover:bg-white hover:text-emerald-600 hover:shadow-sm px-3 py-2 rounded-lg transition-all">
                    Năm nay ({new Date().getFullYear()})
                </button>
                 <button onClick={() => { setViewYear(viewYear - 1); handleSelectSpecific("", viewYear - 1); }} className="w-full text-left text-xs font-bold text-slate-600 hover:bg-white hover:text-emerald-600 hover:shadow-sm px-3 py-2 rounded-lg transition-all">
                    Năm trước ({new Date().getFullYear() - 1})
                </button>
            </div>

            {/* CỘT PHẢI: CHỌN CỤ THỂ */}
            <div className="w-2/3 p-4">
                {/* Header chọn năm */}
                <div className="flex items-center justify-between mb-4">
                    <button onClick={() => setViewYear(viewYear - 1)} className="p-1 hover:bg-slate-100 rounded-full text-slate-400 hover:text-emerald-600"><IconChevronLeft /></button>
                    <span className="text-sm font-black text-slate-800">Năm {viewYear}</span>
                    <button onClick={() => setViewYear(viewYear + 1)} className="p-1 hover:bg-slate-100 rounded-full text-slate-400 hover:text-emerald-600"><IconChevronRight /></button>
                </div>

                {/* Grid chọn tháng */}
                <div className="grid grid-cols-3 gap-2">
                    {[1,2,3,4,5,6,7,8,9,10,11,12].map(m => (
                        <button 
                            key={m}
                            onClick={() => handleSelectSpecific(m, viewYear)}
                            className={`py-2 text-xs font-bold rounded-lg border transition-all ${
                                selectedLabel === `Tháng ${m}/${viewYear}` 
                                ? 'bg-emerald-500 text-white border-emerald-500 shadow-md' 
                                : 'bg-white text-slate-600 border-slate-100 hover:border-emerald-500 hover:text-emerald-600'
                            }`}
                        >
                            Tháng {m}
                        </button>
                    ))}
                </div>
            </div>
        </div>
      )}
    </div>
  );
};


// --- MAIN DASHBOARD ---
export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ totalLeads: 0, converted: 0, conversionRate: 0, pendingDocs: 0 });
  const [chatHistory, setChatHistory] = useState([]);
  
  // DATA
  const [kpiData, setKpiData] = useState([]); 
  const [perfMonth, setPerfMonth] = useState(""); 
  const [perfYear, setPerfYear] = useState(""); 

  const [conversionData, setConversionData] = useState({ leads: 0, customers: 0, conversionRate: 0 });
  const [conversionMonth, setConversionMonth] = useState(""); 
  const [conversionYear, setConversionYear] = useState(""); 
  
  const [availableYears, setAvailableYears] = useState([]); 
  const [searchTerm, setSearchTerm] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [allEmployees, setAllEmployees] = useState([]); 
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [userMsg, setUserMsg] = useState("");
  const chatEndRef = useRef(null);

  const PIE_COLORS = ['#E36D59', '#059669']; 

  const employeeSuggestions = allEmployees.filter(name => 
    name.toLowerCase().includes(searchTerm.toLowerCase()) && searchTerm !== ""
  );

  const fetchEmployees = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/employees');
      const data = await res.json();
      setAllEmployees(data);
    } catch (err) { console.error("⚠️ Lỗi tải nhân viên:", err); }
  };

  const fetchRealData = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchTerm) params.append('employeeName', searchTerm);
      
      // LOGIC GHÉP THÁNG NĂM TỪ BỘ LỌC MỚI
      if (perfMonth && perfYear) {
        const dateStr = `${perfYear}-${String(perfMonth).padStart(2, '0')}`;
        params.append('date', dateStr);
      } else if (perfYear) {
         // Nếu chỉ chọn năm (logic tùy biến phía BE)
         params.append('year', perfYear);
      }

      const res = await fetch(`http://localhost:5000/api/dashboard-extended?${params}`);
      const d = await res.json();

      setStats({
        totalLeads: d.totalLeads,
        converted: d.successfulSales,
        conversionRate: d.conversionRate,
        pendingDocs: d.pendingDocsCount
      });
      setKpiData(d.kpiData);

      if (chatHistory.length === 0) {
        setChatHistory([{ role: 'ai', text: `Chào bạn! Tôi là trợ lý AI. Hãy nhấn vào biểu tượng ở góc dưới để trò chuyện nhé!` }]);
      }
    } catch (err) { console.error("⚠️ Lỗi đồng bộ:", err); } finally { setLoading(false); }
  };

  const fetchConversionData = async () => {
    try {
      const params = new URLSearchParams();
      if (conversionMonth) params.append('month', conversionMonth);
      if (conversionYear) params.append('year', conversionYear);

      const res = await fetch(`http://localhost:5000/api/conversion-chart?${params}`);
      const d = await res.json();

      setConversionData({ leads: d.leads, customers: d.customers, conversionRate: d.conversionRate });
    } catch (err) { console.error("⚠️ Lỗi conversion chart:", err); }
  };

  const fetchAvailableYears = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/available-periods');
      const data = await res.json();
      setAvailableYears(data.years || []);
    } catch (err) { console.error("⚠️ Lỗi available periods:", err); }
  };

  const handleSendChat = async () => {
    if (!userMsg.trim()) return;
    const history = [...chatHistory, { role: 'user', text: userMsg }];
    setChatHistory(history);
    setUserMsg("");
    try {
      const res = await fetch('http://localhost:5000/api/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
      });
      const data = await res.json();
      setChatHistory([...history, { role: 'ai', text: data.reply }]);
    } catch (err) { console.error("Lỗi AI"); }
  };

  useEffect(() => {
    fetchEmployees();
    fetchRealData();
    fetchAvailableYears();
    fetchConversionData();
  }, []);

  useEffect(() => {
    fetchRealData();
  }, [perfMonth, perfYear]); // Trigger khi bộ lọc thông minh thay đổi

  useEffect(() => {
    fetchConversionData();
  }, [conversionMonth, conversionYear]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isChatOpen]);

  const conversionPieData = [
    { name: 'Leads', value: conversionData.leads },
    { name: 'Khách hàng', value: conversionData.customers }
  ];

  return (
    <div 
      className="max-w-7xl mx-auto p-6 bg-slate-50 min-h-screen font-sans antialiased text-slate-600 relative"
      style={{ fontFamily: "'Inter', sans-serif" }}
    >
      {/* HEADER: ĐỎ VÀ NỀN XANH NHƯ YÊU CẦU */}
      <div className="flex justify-end mb-8">
        <div className="flex items-center gap-3 bg-sky-50 px-4 py-2 rounded-full border border-slate-100 shadow-sm">
          <span className="text-[10px] font-black uppercase tracking-widest" style={{ color: '#FF3333' }}>
            Odoo Server Live
          </span>
          <div className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </div>
        </div>
      </div>

      {/* KPI CARDS: GIỮ NGUYÊN GRADIENT */}
      <div className="grid grid-cols-4 gap-6 mb-10">
        <StatCard label="Tổng Leads" val={stats.totalLeads} icon="📈" subtitle="Khách tiềm năng"
            bgStyle="bg-gradient-to-br from-blue-50 to-white border-blue-100"
            iconBoxStyle="bg-gradient-to-br from-blue-500 to-blue-600 shadow-blue-200"
            textStyle="text-blue-700"
        />
        <StatCard label="Hợp Đồng" val={stats.converted} icon="💎" subtitle="Thành công"
            bgStyle="bg-gradient-to-br from-emerald-50 to-white border-emerald-100"
            iconBoxStyle="bg-gradient-to-br from-emerald-400 to-emerald-600 shadow-emerald-200"
            textStyle="text-emerald-700"
        />
        <StatCard label="Chờ Duyệt" val={stats.pendingDocs} icon="🔥" subtitle="Văn bản gấp"
            bgStyle="bg-gradient-to-br from-orange-50 to-white border-orange-100"
            iconBoxStyle="bg-gradient-to-br from-orange-400 to-red-500 shadow-orange-200"
            textStyle="text-orange-700"
        />
        <StatCard label="Tỷ Lệ Chốt" val={`${stats.conversionRate}%`} icon="🎯" subtitle="Hiệu suất"
            bgStyle="bg-gradient-to-br from-purple-50 to-white border-purple-100"
            iconBoxStyle="bg-gradient-to-br from-purple-500 to-pink-500 shadow-purple-200"
            textStyle="text-purple-700"
        />
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* 1. BIỂU ĐỒ TRÁI: ĐÃ THÊM BỘ LỌC THÔNG MINH (SMART FILTER) */}
        <div className="col-span-12 lg:col-span-8">
          <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 h-[480px] flex flex-col">
            <div className="flex items-center justify-between mb-8 pb-4 border-b">
                <div className="flex items-center gap-6 w-full">
                    {/* SEARCH INPUT */}
                    <div className="relative flex-1 group">
                      <label className="whitespace-nowrap font-bold mr-3 md:pt-2 capitalize text-black dark:text-white">Nhân Viên</label>
                        {/* <label className="text-[10px] font-black text-slate-400 uppercase mr-4">Nhân Viên</label> */}
                        <input 
                            type="text"
                            placeholder="Tìm nhân viên..."
                            className="w-1/2 border-b border-slate-200 focus:border-blue-500 outline-none py-1 text-sm font-bold bg-transparent"
                            value={searchTerm}
                            onChange={(e) => {setSearchTerm(e.target.value); setShowSuggestions(true);}}
                        />
                        {showSuggestions && employeeSuggestions.length > 0 && (
                            <div className="absolute left-20 top-10 w-1/2 bg-white shadow-2xl rounded-xl z-50 overflow-hidden border">
                                {employeeSuggestions.map((name, i) => (
                                    <div key={i} className="p-3 hover:bg-blue-50 cursor-pointer text-xs font-bold" onClick={() => {setSearchTerm(name); setShowSuggestions(false); setTimeout(fetchRealData, 100);}}>
                                        👤 {name}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                    
                    {/* BỘ LỌC MỚI Ở ĐÂY */}
                    <SmartTimeFilter 
                        onFilterChange={(m, y) => {
                            setPerfMonth(m);
                            setPerfYear(y);
                        }} 
                    />

                </div>
            </div>
            <h3 className="text-[#059669] font-black mb-6 uppercase text-[12px] tracking-widest flex items-center">
              <span className="w-2 h-2 bg-[#059669] rounded-full mr-2"></span>
              Thống kê hiệu suất nhân sự
            </h3>

            {/* <h3 className="text-slate-800 font-black mb-6 uppercase text-[10px] tracking-widest flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span> Thống kê hiệu suất nhân sự
            </h3> */}
            
            <div className="flex-1">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={kpiData}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} />
                        <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} />
                        <Tooltip contentStyle={{borderRadius: '15px', border: 'none', boxShadow: '0 10px 15px rgba(0,0,0,0.1)'}} />
                        <Bar dataKey="leads" name="Khách tiềm năng" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={25} />
                        <Bar dataKey="sales" name="Hợp đồng chốt" fill="#10b981" radius={[4, 4, 0, 0]} barSize={25} />
                    </BarChart>
                </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* 2. BIỂU ĐỒ PHẢI: GIỮ NGUYÊN BỘ LỌC CŨ CHO ĐỒNG BỘ HOẶC CÓ THỂ THAY THẾ LUÔN NẾU MUỐN */}
        <div className="col-span-12 lg:col-span-4">
          <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 h-[480px] flex flex-col">
            {/* Nếu muốn bên này cũng xịn như bên kia thì thay bằng SmartTimeFilter */}
            <div className="mb-6 pb-4 border-b border-slate-100">
               {/* Thay thế bộ lọc cũ bằng cái mới cho đồng bộ (hoặc giữ nguyên nếu muốn) */}
               <div className="flex justify-end">
                 <SmartTimeFilter 
                    onFilterChange={(m, y) => {
                        setConversionMonth(m);
                        setConversionYear(y);
                    }} 
                 />
               </div>
            </div>

            <h3 className="text-[#059669] font-black mb-6 uppercase text-[12px] tracking-widest flex items-center">
              <span className="w-2 h-2 bg-[#059669] rounded-full mr-2"></span>
              Phân bổ chuyển đổi khách hàng
            </h3>
 
            {/* <h3 className="text-slate-800 font-black mb-6 uppercase text-[10px] tracking-widest flex items-center">
              <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2"></span> Phân bổ chuyển đổi khách hàng
            </h3> */}
            
            <div className="flex-1">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={conversionPieData} outerRadius={100} paddingAngle={5} dataKey="value">
                    {conversionPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      {/* CHAT BOT */}
      <div className="fixed bottom-8 right-8 z-50">
        {isChatOpen && (
          <div className="absolute bottom-24 right-0 w-80 h-[480px] bg-white rounded-3xl shadow-2xl shadow-blue-900/20 border border-slate-100 flex flex-col overflow-hidden animate-fade-in-up">
            <div className="p-4 bg-gradient-to-r from-slate-900 to-slate-800 flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse shadow-[0_0_10px_rgba(74,222,128,0.5)]"></div>
                <span className="text-white font-bold text-[10px] uppercase tracking-widest">AI Assistant</span>
              </div>
              <button onClick={() => setIsChatOpen(false)} className="text-slate-400 hover:text-white transition-colors">✕</button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
              {chatHistory.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] p-3 text-[11px] font-medium leading-relaxed rounded-2xl shadow-sm ${
                    m.role === 'user' ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-tr-none' : 'bg-white text-slate-700 border border-slate-100 rounded-tl-none'
                  }`}>
                    {m.text}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <div className="p-3 bg-white border-t border-slate-100 flex gap-2">
              <input type="text" className="flex-1 bg-slate-100 border-none rounded-xl text-[11px] font-medium text-slate-700 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Hỏi AI..." value={userMsg} onChange={(e) => setUserMsg(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSendChat()} />
              <button onClick={handleSendChat} className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white w-9 h-9 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all">➔</button>
            </div>
          </div>
        )}
        <button onClick={() => setIsChatOpen(!isChatOpen)} className={`w-16 h-16 rounded-full shadow-2xl shadow-purple-500/40 flex items-center justify-center text-2xl transition-all duration-300 hover:scale-110 active:scale-95 border-4 border-white z-50 ${isChatOpen ? 'bg-slate-800 rotate-180' : 'bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 text-white'}`}>
          {isChatOpen ? '✕' : '🤖'}
          {!isChatOpen && (
            <span className="absolute -top-1 -right-1 flex h-5 w-5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-pink-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-5 w-5 bg-gradient-to-r from-pink-500 to-rose-500 text-[10px] text-white flex items-center justify-center font-bold border-2 border-white">1</span>
            </span>
          )}
        </button>
      </div>
    </div>
  );
}

// COMPONENT STAT CARD
function StatCard({ label, val, icon, subtitle, bgStyle, iconBoxStyle, textStyle }) {
  return (
    <div className={`${bgStyle} p-6 rounded-[2rem] shadow-lg shadow-slate-200/50 border flex items-center space-x-4 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 cursor-default group`}>
      <div className={`${iconBoxStyle} w-12 h-12 rounded-2xl flex items-center justify-center text-xl text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
        {icon}
      </div>
      <div>
        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">{label}</p>
        <h4 className={`text-2xl font-black leading-none tabular-nums tracking-tight mt-1 ${textStyle}`}>{val}</h4>
        <p className="text-[10px] text-slate-400 font-semibold italic mt-1">{subtitle}</p>
      </div>
    </div>
  );
}
