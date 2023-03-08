import React, { useState } from 'react';
import './App.css';
import { Route, Routes, useLocation} from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Login/Login';
import Signup from './components/Login/Signup';
import Preferences from './components/Preferences/Preferences';
import useToken from './components/App/useToken';

function App() {

  const { token, setToken } = useToken();
  
  if(!token && useLocation().pathname != "/register") {
    return <Login setToken={setToken} />
  }
  return (
    <div className="wrapper">
      <h1>Quote A Day</h1>
        <Routes>
          <Route path="/dashboard" element={<Dashboard/>} />
          <Route path="/register" element={<Signup />} />
          <Route path="/preferences" element={<Preferences/>} />
        </Routes>
    </div>
  );
}

export default App;