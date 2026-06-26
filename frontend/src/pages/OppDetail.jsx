import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapPin, BookMarked, ArrowRight } from 'lucide-react';
import { API, mediaUrl } from "../lib/api";

function saveOpp(opp_type, opp_key) {
  return fetch(`${API}/saveopp`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ opp_type, opp_key }),
  })
    .then((res) => res.json())
    .then((result) => console.log(result))
    .catch((err) => console.error(err));
}

function ApplyButton({ url, label = "Apply" }) {
  if (!url) return null;
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex bg-blue-500 hover:bg-blue-600 px-6 rounded-3xl text-white py-3"
    >
      {label}
      <ArrowRight className="ml-1 h-5 mt-1" />
    </a>
  );
}

function useDetails(path, id) {
  const [details, setDetails] = useState({});
  useEffect(() => {
    fetch(`${API}/${path}/${id}`, { method: "GET", credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        return res.json();
      })
      .then(setDetails)
      .catch((err) => console.error("Fetch error:", err.message));
  }, [path, id]);
  return details;
}

export function JobDetail(){
  const { id } = useParams();
  const nav = useNavigate();
  const details = useDetails("job", id);
  return (
    <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
      <div className="flex justify-between">
        <div className=" flex gap-4">
          <img src={mediaUrl(details.company_logo_url)} alt="" className="max-w-15 max-h-15 md:w-3xl md:h-auto" />
          <h2 className="text-xl md:text-2xl mt-2.5">{details.company}</h2>
        </div>
        <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
      </div>
      <h1 className="text-3xl text-left mt-4 ml-4">{details.company_role}</h1>
      <div className="flex gap-0 mt-4">
        <MapPin className="text-blue-500 mt-3.5 ml-3"/>
        <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.location} </p>
      </div>
      {details.pay && <p className="text-gray-300 text-left mt-3 ml-5 text-md">{details.pay}</p>}
      <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
        <ApplyButton url={details.apply_url} />
        <button onClick={()=> saveOpp("job", id)} className="flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
          Save
          <BookMarked className="ml-1 h-5 mt-1"/>
        </button>
      </div>
      <h2 className="text-lg text-left font-bold ml-4 mt-3 text-white">About this Opportunity:</h2>
      <p className="leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.description} </p>
    </div>
  )
}

export function VolDetail(){
  const { id } = useParams();
  const nav = useNavigate();
  const details = useDetails("unpaid", id);
  return (
    <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
      <div className="flex justify-between">
        <div className=" flex gap-4">
          <img src={mediaUrl(details.org_logo)} alt="" className="max-w-15 max-h-15 md:w-3xl md:h-auto" />
          <h2 className="text-xl md:text-2xl mt-2.5">{details.organization}</h2>
        </div>
        <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
      </div>
      <h1 className="text-3xl text-left mt-4 ml-4">{details.unpaid_role}</h1>
      <div className="flex gap-0 mt-4">
        <MapPin className="text-blue-500 mt-3.5 ml-3"/>
        <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.unpaid_location} </p>
      </div>
      <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
        <ApplyButton url={details.apply_url} />
        <button onClick={()=> saveOpp("unpaid", id)} className="flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
          Save
          <BookMarked className="ml-1 h-5 mt-1"/>
        </button>
      </div>
      <p className="text-xs text-left ml-5 text-gray-500">Opportunity added on {details.date_added}</p>
      <h2 className="text-lg text-left font-bold ml-4 mt-3 text-white">About this Opportunity:</h2>
      <p className="leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.unpaid_desc} </p>
    </div>
  )
}

export function EventDetail(){
  const { id } = useParams();
  const nav = useNavigate();
  const details = useDetails("events", id);
  return (
    <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
      <div className="flex justify-between">
        <div className=" flex gap-4">
          <img src={mediaUrl(details.org_logo)} alt="" className="max-w-15 max-h-15 md:w-3xl md:h-auto" />
          <h2 className="text-xl md:text-2xl mt-2.5">{details.organization}</h2>
        </div>
        <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
      </div>
      <h1 className="text-3xl text-left mt-4 ml-4">{details.event_name}</h1>
      <div className="flex gap-0 mt-4">
        <MapPin className="text-blue-500 mt-3.5 ml-3"/>
        <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.event_location} </p>
      </div>
      <p className="text-gray-300 text-left ml-5 mt-3">Join us on {details.event_date} for this event</p>
      <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
        <ApplyButton url={details.apply_url} label="Register" />
        <button onClick={()=> saveOpp("event", id)} className="flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
          Save
          <BookMarked className="ml-1 h-5 mt-1"/>
        </button>
      </div>
      <p className="text-xs text-left ml-5 text-gray-500"> Event was added on {details.date_added}</p>
      <h2 className="text-lg text-left font-bold ml-4 mt-4 text-white">About this Opportunity:</h2>
      <p className="leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.event_desc} </p>
    </div>
  )
}
