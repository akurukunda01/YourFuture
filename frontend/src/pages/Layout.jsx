import { Outlet, Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { House, Sparkle, Handshake, Waypoints, PersonStanding } from 'lucide-react';
import React from 'react';
function Sidebar({ open, setOpen }){
    const location = useLocation();
    return (
        <div>
             <button
            onClick={() => setOpen(!open)}
            className={`md:hidden p-4 text-white fixed top-0 left-0 transform transition-transform duration-400 z-50
        ${open ? "translate-x-20" : "left-0"} md:translate-x-0`}>
            ☰
            </button>
            <div className={`fixed w-30 mr-4 h-screen text-xs h-fixed text-white bg-[rgba(69,69,69,0.5)] bg-top-0 left-0 md:w-100 md:text-2xl transform transition-transform duration-300 z-40
                ${open ? "translate-x-0" : "-translate-x-full"} md:translate-x-0`}>
                <ul className = "py-4 ">
                    <li className="">
                        <img src="/YourFuture.png" className=" invert md:max-w-50 md:ml-25"></img>
                    </li>
                    <li className={` py-4 md:pt-8 md:py-6
                        ${location.pathname ==="/student" && "bg-[rgba(89,89,89,0.5)]"}`}>
                        <div className="flex justify-between md:flex md:justify-center md:gap-3 px-2">
                            <Link to="/student" className="mt-2 md:mt-0 " >Home</Link>
                            <House className="text-blue-500 md:h-8" />
                        </div>
                    </li>
                    <li className={` py-4 md:pt-8 md:py-6
                        ${location.pathname === "/student/jobs" && "bg-[rgba(89,89,89,0.5)]"}`}>
                        <div className="flex justify-between px-2 md:justify-center">
                            <Link to="/student/jobs" className="mt-3" >Opportunities</Link>
                            <Sparkle className="text-blue-500 md:h-9 md:mt-2.5 md:ml-2" />
                        </div>
                    </li>
                    <li className={`py-4 md:pt-8 md:py-6
                        ${location.pathname === "/student/connection" && "bg-[rgba(89,89,89,0.5)]"}`}>
                        <div className="flex justify-between px-2 md:justify-center">
                            <Link to="/student/connection" className="mt-2 md:0" >Connections</Link>
                            <Handshake className="text-blue-500 mt-1 md:h-9 md:mt-2.5 md:ml-2" />
                        </div>
                    </li>
                    <li className={`py-4 md:pt-8 md:py-6
                        ${location.pathname === "/student/forum" && "bg-[rgba(89,89,89,0.5)]"}`}>
                        <div className="flex justify-between px-2 md:justify-center">
                            <Link to="/student/forum" className="mt-2 md:0" >Forum</Link>
                            <Waypoints className="text-blue-500 mt-1 md:h-9 md:mt-2.5 md:ml-2" />
                        </div>
                    </li>
                    <li className={`py-4 md:pt-8 md:py-6
                        ${location.pathname === "/student/profile" &&"bg-[rgba(89,89,89,0.5)]"}`}>
                        <div className="flex justify-between px-2 md:justify-center">
                            <Link to="/student/profile" className="mt-2 md:0" >Profile</Link>
                            <PersonStanding className="text-blue-500 mt-1 md:h-9 md:mt-2.5 md:ml-2" />
                        </div>
                    </li>
                </ul>
            </div>
        </div>
  );
    
}
export function StudentLayout(){
    const [open, setOpen] = useState(true);
    return(
        <div className = "grid grid-cols-12 ">
            <div className = "h-fixed col-span-2 md:col-span-3">
                <Sidebar open={open} setOpen={setOpen}/>
            </div>
            <div className = "col-span-9  py-4 justify-content-center md:col-span-9">
                <main className ={`transform translate-transform duration-300 ${open ? "translate-x-10": "-translate-x-5"}`}>
                    <Outlet/>
                </main>
            </div>
        </div>
    )
}
