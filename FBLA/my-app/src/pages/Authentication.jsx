import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {User, Lock, ArrowRight} from 'lucide-react'
function Login({method, setMethod}){
    const nav = useNavigate()
    const [formData, setFormData] = useState({
        'name':'',
        'password': ''
    })
    const handleSubmit = async (e) => {
        const data = new FormData();
        data.append('username', formData.name);
        data.append('password', formData.password)
        e.preventDefault();
        const res = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        body: data,
        credentials:"include"
        });

        if (res.ok) {
        const data = await res.json();
        console.log('Submitted:', data);
        nav(`/${data}`)
        } else {
        console.log("this failed "+res)
        console.error('Submit failed');
        }
    }
    return (
        <>
            <div className="my-20 mx-25 md:my-25 md:mx-60 pb-10 bg-[rgba(69,69,69)] text-white items-center">
                <div className="flex ml-5 justify-start w-30 ">
                    <img src="./YourFuture.png" className="invert"></img>
                </div>
                <h1 className="text-blue-500 pb-4 text-4xl font-bold">Login</h1>
                <div className="mx-10 text-gray-400 text-s mb-4">
                    <h3> Enter you login credentials to continue into YourFuture</h3>
                </div>
                <form>
                    <div className="flex flex-col jusfity-center gap-4 py-4">
                        <div className="flex justify-center gap-3 my-3">
                            <User className="text-blue-500 h-10"/>
                            <input onChange={(e)=> setFormData({...formData, name: e.target.value})} className="bg-[rgba(89,89,89)] text-white px-3 py-1.5 rounded-full w-xs md:w-xl" placeholder="Username"name="username" id="username"></input>
                        </div>
                        <div className="flex justify-center gap-3 mb-3">
                            <Lock className="text-blue-500 h-10"/>
                            <input onChange={(e)=> setFormData({...formData, password: e.target.value})} className="bg-[rgba(89,89,89)] text-white px-3 py-1.5 rounded-full w-xs md:w-xl" placeholder="Password" name="password" id="password"></input>
                        </div>
                        <button onClick={handleSubmit} className="bg-blue-500 hover:bg-blue-700 text-white mx-10 py-2 rounded-full">Login</button>
                    </div>
                </form>
                <div className="flex justify-center pt-3 gap-2">
                    <h2>Don't have an account?</h2>
                    <button onClick={()=>setMethod('register')}>
                        <ArrowRight className="text-blue-500 hover:text-blue-700"/>
                    </button>
                </div>
            </div>
        </>
    )
}
function Register({method, setMethod}){
    const nav = useNavigate();
    const [type, setType] = useState('student');
    const [formData, setFormData] = useState({
        'name':'',
        'password': '',
        "conf":'',
        'org':''
    })
    const handleSubmit = async (e) => {
        const data = new FormData();
        data.append('username', formData.name);
        data.append('password', formData.password)
        data.append('confirm_password', formData.conf)
        data.append('user_type', type)
        data.append('user_org', formData.org);
        e.preventDefault();
        const res = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        body: data,
        credentials:"include"
        });

        if (res.ok) {
        const data = await res.json();
        console.log('Submitted:', data);
        setMethod('login')
        } else {
        console.log("this failed "+res)
        console.error('Submit failed');
        }
    }
    function handleChange(event){
        setType(event.target.value)
    }
    return(
        <>
            <div className="my-20 mx-25 md:my-25 md:mx-60 pb-10 bg-[rgba(69,69,69)] text-white items-center">
                <div className="flex ml-5 justify-start w-30 ">
                    <img src="./YourFuture.png" className="invert"></img>
                </div>
                <h1 className="text-blue-500 pb-4 text-4xl font-bold">Register</h1>
                <div className="mx-10 text-gray-400 text-s mb-4">
                    <h3> Enter your credentials to create an account in YourFuture</h3>
                </div>
                <form>
                    <div className="flex flex-col justify-center gap-4">
                        <div>
                            <div className="flex justify-center mt-3 gap-4">
                                <h2>Account Type: </h2>
                                <select className="text-white bg-blue-500 hover:bg-blue-700 px-3 rounded-full py-1" value={type} onChange={handleChange}>
                                    <option value="student">Student</option>
                                    <option value="employer">Employer</option>
                                </select>
                            </div>
        
                            <input onChange={(e)=>setFormData({...formData, name: e.target.value})}name="username" placeholder="Username" className="bg-[rgba(89,89,89)] my-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                            <input onChange={(e)=>setFormData({...formData, password: e.target.value})}name="password" placeholder="Password" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                            <input onChange={(e)=>setFormData({...formData, conf: e.target.value})}name="confirm-password" placeholder="Confirm Password" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>
                            {(type==='employer' && <input onChange={(e)=>setFormData({...formData, org: e.target.value})}name ="company" placeholder='Company'className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>)}
                            {(type==='student'&& <input onChange={(e)=>setFormData({...formData, org: e.target.value})} name="school" placeholder="School" className="bg-[rgba(89,89,89)] mb-5 rounded-full w-xs md:w-xl px-3 py-1.5"></input>)}
                        </div>
                        <button onClick={handleSubmit}className="bg-blue-500 hover:bg-blue-700 text-white mx-10 py-2 rounded-full">Register</button>
                    </div>
                </form>
                <div className="flex justify-center pt-3 gap-2">
                    <h2>Already have an account?</h2>
                    <button onClick={ ()=> setMethod('login')}>
                        <ArrowRight className="text-blue-500 hover:text-blue-700"/>
                    </button>
                </div>
            </div>
        </>
    )
}
function Authentication(){
    const [method, setMethod] = useState('login')
    return(
        <>
            <div>
                {(method === 'login' && <div>
                    <Login method={method} setMethod={setMethod}/>
                </div>)}
                {(method === 'register' && <div>
                    <Register method={method} setMethod={setMethod}/>
                </div>)}
            </div>
        </>
    )
}
export default Authentication;
