import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './Signup.css';



async function registerUser(credentials) {
  return fetch('http://127.0.0.1:8000/api/register/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
  .then(data => data.json())
}


export default function Signup(){
    const [email, setEmail] = useState();
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const navigate = useNavigate();
    const gotoLoginPage = () => navigate("/dashboard");


    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = await registerUser({
          username,
          email,
          password
        });
        gotoLoginPage()
    };
  
    return (
        <div className='register-wrapper'>
            <h2>Sign up </h2>
            <form onSubmit={handleSubmit}>
                <p htmlFor='email'>Email Address</p>
                <input
                    type='email'
                    name='email'
                    id='email'
                    value={email}
                    required
                    onChange={(e) => setEmail(e.target.value)}
                />
                <p htmlFor='username'>Username</p>
                <input
                    type='text'
                    id='username'
                    name='username'
                    value={username}
                    required
                    onChange={(e) => setUsername(e.target.value)}
                />
                <p htmlFor='password'>Password</p>
                <input
                    type='password'
                    name='password'
                    id='password'
                    minLength={8}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /><div>                <button type="submit">SIGN UP</button></div>
                <p>
                    Already have an account?{" "}
                    <span className='link' onClick={gotoLoginPage}>
                        Login
                    </span>
                </p>
            </form>
        </div>
    );
};

