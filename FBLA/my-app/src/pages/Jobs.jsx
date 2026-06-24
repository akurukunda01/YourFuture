import { useState, useEffect } from "react";
import { Link , useNavigate } from "react-router-dom";
import { Search, Briefcase, Lightbulb, CalendarCheck, ArrowRight} from 'lucide-react';
import {JobCard, VolCard, EventCard } from "./Cards"
import {JobSort, VolSort, EventSort} from "./SortOpportunities"
function JobsBoard({ sortMethod }){
  const [jobs, setJobs] = useState([])
   useEffect(() => {
    fetch("http://localhost:8000/api/viewjobs", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Fetched data:", data);
        setJobs(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
  }, []);

  function getSortedJobs() {
    const sortedJobs = [...jobs];
    if (sortMethod === "pay-asc") sortedJobs.sort((a, b) => Number(a.pay) - Number(b.pay));
    else if (sortMethod === "Latest") sortedJobs.reverse();
    else if (sortMethod === "pay-desc") sortedJobs.sort((a, b) => b.pay - a.pay);
    else if (sortMethod === "company-az") sortedJobs.sort((a, b) => a.company_role.localeCompare(b.company_role));
    return sortedJobs;
  }

  return (
    <div>
      {getSortedJobs().length === 0 && <p>No jobs found.</p>}
      {getSortedJobs().map((job, index) => (
        <JobCard key={index} job={job} />
      ))}
    </div>
  );
}

function JobSearch(){
  const[query,setQuery] = useState('')
  const[results, setResults] = useState([])
  const navigate = useNavigate()
  useEffect(() => {
    if (query.trim() === ''){
      setResults([]);
      return;
    }

    const delayDebounce = setTimeout(() => {
      fetch(`http://localhost:8000/api/search?q=${query}`,{
        credential:"include"
      })
        .then((res) => res.json())
        .then((data) => setResults(data))
        .catch((err) => console.error("Search error:", err));
    }, 300); 

    return () => clearTimeout(delayDebounce);
  }, [query]);
  function handleSubmit(event){
    event.preventDefault();
    if (query.trim()===''){
      return;
    }
    navigate(`/student/SearchResults?q=${query}`)
  }
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="flex flex-col justify-center">
          <div className="flex items-center w-md rounded-full px-2 bg-[rgba(69,69,69,0.5)] md:w-xl">
            <button type="submit" className="rounded-full ">
              <Search className="text-blue-500 hover:text-blue-700 h-7"/>
            </button>
            <input className = "w-xs border-0 rounded-3xl md:w-xl md:text-xl px-5 py-2 outline-0  text-white" placeholder="Search Opportunities" autoComplete="on" onChange={(e)=> setQuery(e.target.value)} value={query}/>
            
          </div>
          <div className=" flex-flex-row bg-[rgba(69,69,69,0.5)] text-blue-500 mt-3 md:w-xl w-xs ml-14 md:ml-0 overflow-y-auto">
            {Array.isArray(results) && results.slice(0,4).map((opp, i) => (
                <SearchResults key={i} opp={opp}/>
            ))}
          </div>
        </div>
      </form>
    </>
  )
}

function SearchResults({ opp }){
  const[open, setOpen] = useState(true)
  function content(){
    if (opp.type === "job"){
      return(
        (open && (<div className={` flex justify-between bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] text-left py-2 text-blue-500 w-xs md:w-xl`}>
          <div className="flex ">
            <div>
              <img src={`http://localhost:8000/api/${opp.company_logo_url}`} className="max-h-10 px-3"></img>
            </div>
            <div>
              <Link to={`/jobs/${opp.job_id}`} className=" hover:text-blue-900">{opp.company_role}</Link>
              <div className="flex text-xs text-white gap-1.5">
                <p>{opp.company}</p>
                <div className="flex">
                  <Briefcase className="h-4 text-blue-500"/>
                  <p>Job</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <button onClick={()=> setOpen(false)} className="text-white md:text-lg hover:text-blue-500 px-3">x</button>
          </div>
        </div>))
      )
    }
    else if (opp.type === "unpaid"){
      return(
        (open && (<div className={` flex justify-between bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] text-left py-2 text-blue-500 w-xs md:w-xl`}>
          <div className="flex ">
            <div>
              <img src={`http://localhost:8000/api/${opp.org_logo}`} className="max-h-10 px-3"></img>
            </div>
            <div>
              <Link to={`/unpaid/${opp.unpaid_id}`} className=" hover:text-blue-900">{opp.unpaid_role}</Link>
              <div className="flex text-xs text-white gap-1.5">
                <p>{opp.organization}</p>
                <div className="flex">
                  <Lightbulb className="h-4 text-blue-500"/>
                  <p>Unpaid</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <button onClick={()=> setOpen(false)} className="text-white md:text-lg hover:bg-[rgba(89,89,89,0.5)] px-3">x</button>
          </div>
        </div>))
      )
    }
    else if (opp.type === "event"){
      return(
        (open && (<div className={` flex justify-between bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] text-left py-2 text-blue-500 w-xs md:w-xl`}>
          <div className="flex ">
            <div>
              <img src={`http://localhost:8000/api/${opp.org_logo}`} className="max-h-10 px-3"></img>
            </div>
            <div>
              <Link to={`/events/${opp.event_id}`} className=" hover:text-blue-900">{opp.event_name}</Link>
              <div className="flex text-xs text-white gap-1.5">
                <p>{opp.organization}</p>
                <div className="flex">
                  <CalendarCheck className="h-4 text-blue-500"/>
                  <p>Event</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <button onClick={()=> setOpen(false)} className="text-white md:text-lg hover:text-blue-500 px-3">x</button>
          </div>
        </div>))
      )
    }
    return null;
  }
  return (
    <>{content()}</>
  )
}
function VolBoard({sortMethod}){
  const [list, setList] = useState([])
   useEffect(() => {
    fetch("http://localhost:8000/api/viewunpaid", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Fetched data:", data);
        setList(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
  }, []);

  function getSortedList() {
    const sortedList = [...list];
    if (sortMethod === "Latest") sortedList.reverse();
    else if (sortMethod === "Oldest") return sortedList;
    else if (sortMethod === "name-az") sortedList.sort((a, b) => a.unpaid_role.localeCompare(b.unpaid_role));
    return sortedList;
  }

  return(
    <div>
      {getSortedList().length === 0 && <p>No unpaid opportunities found.</p>}
      {getSortedList().map((vol, index) => (
        <VolCard key={index} vol={vol} />
      ))}
    </div>
  )
}
function EventBoard({sortMethod}){
  const [list, setList] = useState([])
   useEffect(() => {
    fetch("http://localhost:8000/api/viewevents", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Fetched data:", data);
        setList(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
  }, []);
  function getSortedList() {
    const sortedList = [...list];
    if (sortMethod === "Latest") sortedList.reverse();
    else if (sortMethod === "Oldest") return sortedList;
    else if (sortMethod === "Event_Date") sortedList.sort((a,b)=> new Date(a.event_date) - new Date(b.event_date));
    else if (sortMethod === "name-az") sortedList.sort((a, b) => a.event_name.localeCompare(b.event_name));
    return sortedList;
  }

  return(
    <div>
      {getSortedList().length === 0 && <p>No events found.</p>}
      {getSortedList().map((event, index) => (
        <EventCard key={index} event={event} />
      ))}
    </div>
  )
}
function ToggleOpportunity(){
  const [active,setActive] = useState('jobs')
  const [sortMethod, setSortMethod] = useState("")

  function handleSortChange(newSortOption){
    setSortMethod(newSortOption);
    console.log(newSortOption)
  }
  return(
    <div className="md:w-3xl">
      <div className="flex justify-between">
        <div className="flex flex-row text-xs md:text-lg">
          <button onClick={()=>setActive('jobs')} className={`flex px-3 md:px-4 pt-2 md:pt-4 rounded-l-full ${active ==='jobs' ? "bg-blue-500 text-white":"bg-[rgba(69,69,69,0.5)] text-white"}`}>
            Jobs
            <Briefcase className="h-4 md:h-6 ml-1" />
          </button>
          <button onClick={()=>setActive('vol')} className={`flex px-3 pt-2 md:pt-4 ${active ==='vol' ? "bg-blue-500 text-white":"bg-[rgba(69,69,69,0.5)] text-white"}`}>
            Unpaid
            <Lightbulb className="h-4 md:h-6 ml-1" />
          </button>
          <button onClick={()=>setActive('events')} className={`flex px-3 pt-2 md:pt-4 rounded-r-full ${active ==='events' ? "bg-blue-500 text-white":"bg-[rgba(69,69,69,0.5)] text-white"}`}>
            Events
            <CalendarCheck className="h-4 md:h-6 ml-1" />
          </button>
        </div>
        <div className="md:mr-12">
          {active==='jobs' && <JobSort onSortChange={handleSortChange} />}
          {active ==='vol' && <VolSort onSortChange={handleSortChange} />}
          {active ==='events' && <EventSort onSortChange={handleSortChange} />}
        </div>
      </div>
      <div className="flex justify-items-center w-max mt-4 md:mt-8">
        {active ==='jobs' && <JobsBoard sortMethod={sortMethod}/>}
        {active === 'vol' && <VolBoard sortMethod={sortMethod}/>}
        {active === 'events' && <EventBoard sortMethod={sortMethod}/>}
      </div>
    </div>
  )
}



function Jobs(){
    return(
        <div className="items-center md:flex md:flex-col md:justify-center">
          <div>
            <h1 className="text-center text-blue-500 font-extrabold mb-7 text-5xl">
               Opportunities 
            </h1>
          </div>
          <div className="mb-12 mt-10 md:mb-12">
            <JobSearch />
          </div>
          <div className="">
            <ToggleOpportunity /> 
          </div>
        </div>
    )
}
export default Jobs