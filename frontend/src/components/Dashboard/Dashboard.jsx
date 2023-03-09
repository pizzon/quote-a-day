import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useToken from '../App/useToken';


export default function Dashboard() {

  const {token} = useToken();
  const [user, setUser] = useState([]);
  const [nums, setPhoneList] = useState([]);
  const [emails, setEmailList] = useState([]);
  const [email, setEmail] = useState();
  const [number, setNumber] = useState();


  useEffect( () => {
    async function UserDetails() {
      const res = await fetch(`http://54.90.8.129/api/user/`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Token ${token}`
        },
      })
      const body = await res.json()
      console.log(body)
      setUser(body)
      setPhoneList(body.phone_number)
      setEmailList(body.secondary_email)
    }
    UserDetails()
  },[])

  async function handlePhoneRemove(phone_number){
    await fetch(`http://54.90.8.129/api/user/`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':`Token ${token}`,
      },
      body: JSON.stringify({"phone_number": phone_number})
    })
    const idx = nums.indexOf(phone_number)
    setPhoneList(nums.filter( n => (n !== phone_number)))
  }

  async function handleEmailRemove(email){
    await fetch(`http://54.90.8.129/api/user/`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':`Token ${token}`,
      },
      body: JSON.stringify({"email": email})
    })
    setEmailList(emails.filter( n => (n !== email)))
  }

  async function handleEmailAdd(){
    await fetch(`http://54.90.8.129/api/user/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':`Token ${token}`,
      },
      body: JSON.stringify({"email": email})
    })
    setEmailList(emails => ([...emails, email]))
  }

  async function handlePhoneAdd(){
    await fetch(`http://54.90.8.129/api/user/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':`Token ${token}`,
      },
      body: JSON.stringify({"phone_number": number})
    })
    setPhoneList(nums => ([...nums, number]))
  }

  const createEmailList = () => {
    return emails.map( e => <p key={e}>{e}<button onClick={() => handleEmailRemove(e)}>Delete</button></p>)
  }

  const createPhoneList = () => {
    return nums.map( p => <p key={p}>{p}<button onClick={() => handlePhoneRemove(p)}>Delete</button></p>)
  }

  const logout = () => {
    sessionStorage.removeItem('token');
    window.location.reload()
  }

  return(
    <div>
      <h1>Welcome, {user.username}!</h1>
      <h2>Your currently registered emails:</h2>
      <p>{user.email}</p>
      {createEmailList()}
      <label htmlFor='email'>Add an email: </label>
      <input type='email' minLength={5} onChange={(e) => setEmail(e.target.value)}></input>
      <button onClick={handleEmailAdd}>Register</button>

      <h2>Your currently registered phone numbers:</h2>
      {createPhoneList()}
      <label htmlFor='phone'>Add a phone number: </label>
      <input type='tel' minLength={10} maxLength={10} onChange={(p) => setNumber(p.target.value)}></input>
      <button onClick={handlePhoneAdd}>Register</button>
      <div><button onClick={logout}>Log Out</button></div>
      </div>
  );
}
