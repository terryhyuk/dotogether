import { useState } from 'react'
import '../../../App.css'
import { login } from '../repositories/auth'
import { useNavigate } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const handleLogin = async(e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        try{
            const data = await login(email,password)
            localStorage.setItem('access_token', data.access_token)
            navigate('/calendar')

        }catch(error){
            console.log(error)
        }
    }

    return (
        <div className="login-container">
            <div className="login-box">
                <h1>DoTogether</h1>
                <p>Plan together. Achieve together.</p>

                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button type="submit">
                        Login
                    </button>
                </form>
            </div>
        </div>
    )
}

export default Login
