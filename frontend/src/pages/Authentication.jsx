import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { User, Lock, ArrowRight } from 'lucide-react'
import { API } from "../lib/api";

function Login({ setMethod }){
    const nav = useNavigate()
    const [error, setError] = useState("")
    const [formData, setFormData] = useState({ name: '', password: '' })
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("")
        const data = new FormData();
        data.append('username', formData.name);
        data.append('password', formData.password)
        const res = await fetch(`${API}/login`, {
            method: 'POST',
            body: data,
            credentials: "include"
        });
        if (res.ok) {
            const user = await res.json();
            nav(user.user_type === 'admin' ? '/admin' : '/student/jobs')
        } else {
            const err = await res.json().catch(() => ({}));
            setError(err.error || 'Login failed');
        }
    }
    return (
        <div className="my-20 mx-25 md:my-25 md:mx-60 pb-10 bg-[rgba(69,69,69)] text-white items-center">
            <div className="flex ml-5 justify-start w-30 ">
                <img src="/YourFuture.png" className="invert" alt="YourFuture" />
            </div>
            <h1 className="text-blue-500 pb-4 text-4xl font-bold">Login</h1>
            <div className="mx-10 text-gray-400 text-s mb-4">
                <h3>Enter your login credentials to continue into YourFuture</h3>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="flex flex-col jusfity-center gap-4 py-4">
                    <div className="flex justify-center gap-3 my-3">
                        <User className="text-blue-500 h-10"/>
                        <input onChange={(e)=> setFormData({...formData, name: e.target.value})} className="bg-[rgba(89,89,89)] text-white px-3 py-1.5 rounded-full w-xs md:w-xl" placeholder="Username" name="username" id="username"></input>
                    </div>
                    <div className="flex justify-center gap-3 mb-3">
                        <Lock className="text-blue-500 h-10"/>
                        <input type="password" onChange={(e)=> setFormData({...formData, password: e.target.value})} className="bg-[rgba(89,89,89)] text-white px-3 py-1.5 rounded-full w-xs md:w-xl" placeholder="Password" name="password" id="password"></input>
                    </div>
                    {error && <p className="text-red-400 text-center text-sm">{error}</p>}
                    <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white mx-10 py-2 rounded-full">Login</button>
                </div>
            </form>
            <div className="flex justify-center pt-3 gap-2">
                <h2>Don't have an account?</h2>
                <button onClick={()=>setMethod('register')}>
                    <ArrowRight className="text-blue-500 hover:text-blue-700"/>
                </button>
            </div>
        </div>
    )
}

function Register({ setMethod }){
    const [error, setError] = useState("")
    const [formData, setFormData] = useState({ name: '', password: '', conf: '', org: '' })
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("")
        const data = new FormData();
        data.append('username', formData.name);
        data.append('password', formData.password)
        data.append('confirm_password', formData.conf)
        data.append('user_org', formData.org);
        const res = await fetch(`${API}/register`, {
            method: 'POST',
            body: data,
            credentials: "include"
        });
        if (res.ok) {
            setMethod('login')
        } else {
            const err = await res.json().catch(() => ({}));
            setError(err.error || 'Registration failed');
        }
    }
    return(
        <div className="my-20 mx-25 md:my-25 md:mx-60 pb-10 bg-[rgba(69,69,69)] text-white items-center">
            <div className="flex ml-5 justify-start w-30 ">
                <img src="/YourFuture.png" className="invert" alt="YourFuture" />
            </div>
            <h1 className="text-blue-500 pb-4 text-4xl font-bold">Register</h1>
            <div className="mx-10 text-gray-400 text-s mb-4">
                <h3>Enter your credentials to create a student account in YourFuture</h3>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="flex flex-col justify-center gap-4">
                    <div>
                        <input onChange={(e)=>setFormData({...formData, name: e.target.value})} name="username" placeholder="Username" className="bg-[rgba(89,89,89)] my-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                        <input type="password" onChange={(e)=>setFormData({...formData, password: e.target.value})} name="password" placeholder="Password" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                        <input type="password" onChange={(e)=>setFormData({...formData, conf: e.target.value})} name="confirm-password" placeholder="Confirm Password" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                        <input onChange={(e)=>setFormData({...formData, org: e.target.value})} name="school" placeholder="School" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                    </div>
                    {error && <p className="text-red-400 text-center text-sm">{error}</p>}
                    <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white mx-10 py-2 rounded-full">Register</button>
                </div>
            </form>
            <div className="flex justify-center pt-3 gap-2">
                <h2>Already have an account?</h2>
                <button onClick={()=> setMethod('login')}>
                    <ArrowRight className="text-blue-500 hover:text-blue-700"/>
                </button>
            </div>
        </div>
    )
}

function Authentication(){
    const [method, setMethod] = useState('login')
    return(
        <div>
            {method === 'login'
                ? <Login setMethod={setMethod}/>
                : <Register setMethod={setMethod}/>}
        </div>
    )
}
export default Authentication;
