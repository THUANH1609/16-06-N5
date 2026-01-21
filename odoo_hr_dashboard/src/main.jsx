import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
// Thêm dòng này nếu em có file css dùng chung
import './index.css' 

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* Thầy thêm style bọc ngoài để giao diện luôn mượt */}
    <div style={{ margin: 0, padding: 0, boxSizing: 'border-box' }}>
      <App />
    </div>
  </React.StrictMode>,
)