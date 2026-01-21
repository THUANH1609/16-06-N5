import React from 'react';
import Dashboard from './pages/Dashboard';

function App() {
  // Vì chỉ dùng 1 trang duy nhất, ta không cần State currentPage nữa
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* NỘI DUNG CHÍNH 
          Đã loại bỏ thẻ <aside> (Sidebar) và class 'flex' ở bao ngoài
      */}
      <main className="w-full">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
