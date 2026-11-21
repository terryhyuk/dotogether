import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Calendar from './features/calendar/views/Calendar'
import Login from './features/auth/views/Login'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/calendar" element={<Calendar />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App