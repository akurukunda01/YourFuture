import { useState, useEffect } from 'react';
import { useParams,useNavigate } from 'react-router-dom';
import { useRef } from 'react';
import { MapPin, Pencil, BookMarked, ArrowRight, Circle, ArrowLeft } from 'lucide-react';
function StepOne({nextStep, formData, setFormData}){
  return(
    <>
    <h1 className="flex justify-center font-semibold text-lg">Application</h1>
    <p className="text-gray-300 text-s mt-2">Completely fill out the following form to submit your application. All fields must be filled.</p>
    <div className="mt-3">
      <label htmlFor="name">Name:</label>
      <input name="name" id="name" value={formData.name} onChange={(e)=>setFormData({...formData, name:e.target.value})} className="bg-[rgba(89,89,89,0.5)] w-full md:h-7 mt-1.5"></input>
    </div>
    <div className="mt-3">
      <label htmlFor="email">Email:</label>
      <input name="email" id="email" value={formData.email} onChange={(e)=>setFormData({...formData, email: e.target.value})} className="bg-[rgba(89,89,89,0.5)] w-full md:h-7 mt-1.5"></input>
    </div>
    <div className="flex justify-end mt-7">
      <button type="button" className=" text-blue-500 hover:text-blue-900 px-3 py-1"onClick={nextStep}>
        <ArrowRight />
      </button>
    </div>

    </>
  )
}
function StepTwo({nextStep, prevStep, formData, setFormData}){
  return(
    <>
      <div className="flex flex-col text-white">
        <label htmlFor="want" className="py-3">Why do you want this opportunity?</label>
        <textarea className="bg-[rgba(89,89,89,0.5)]" id="want" value={formData.q1} onChange={(e)=>setFormData({...formData, q1: e.target.value})} name="want" rows={5}></textarea>
      </div>
      <div className="flex flex-col mt-6">
        <label htmlFor="s&w" className="py-3">What are your strengths and weaknesses?</label>
        <textarea className="bg-[rgba(89,89,89,0.5)]" id="s&w" value={formData.q2} onChange={(e)=>setFormData({...formData, q2: e.target.value})}name="s&w" rows={5}></textarea>
      </div>
      <div className="flex flex-col mt-6">
        <label htmlFor="experience" className="py-3">Describe how your experiences make you a suitable candidate?</label>
        <textarea className="bg-[rgba(89,89,89,0.5)]" id="experience" value={formData.q3} onChange={(e)=>setFormData({...formData, q3: e.target.value})}name="experience" rows={5}></textarea>
      </div>
      <div className="flex justify-end mt-7">
        <button type="button" className=" text-blue-500 hover:text-blue-900 px-3 py-1"onClick={prevStep}>
        <ArrowLeft />
      </button>
      <button type="button" className=" text-blue-500 hover:text-blue-900 px-3 py-1"onClick={nextStep}>
        <ArrowRight />
      </button>
    </div>
      
      
    </>
  )
}
function StepThree({submitRef, prevStep, formData, setFormData}){
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFormData({ ...formData, resume: file });
  };
  return(
    <>
      <div className="flex flex-col">
        <label>Please upload a picture of your resume:</label>
        <input type="file" name="resume"  onChange={handleFileChange}className="text-white mt-3 w-75 bg-blue-500 hover:bg-blue-700 px-3 py-1 rounded-full"></input>
      </div>
      <div className="flex justify-end mt-7">
        <button type="button" className=" text-blue-500 hover:text-blue-900 px-3 py-1"onClick={prevStep}>
          <ArrowLeft />
        </button>
        <button onClick={()=> submitRef.current.requestSubmit()} type="submit" className= "text-blue-500 bg-[rgba(69,69,69,0.5)] outline-1 rounded-full px-2 outline-blue-500 hover:bg-[rgba(89,89,89,0.5)]">Submit</button>
      </div>
    </>
  )
}

function Application({opp_id, opp_type}){
  const formRef = useRef()
  const [step, setStep] = useState(1)
  const nextStep = ()=> setStep((prev)=>prev+1)
  const prevStep = ()=> setStep((prev)=>prev-1)
  const [formData, setFormData] = useState({
    name:'',
    email: '',
    q1:'',
    q2:'',
    q3:'',
    resume_path: null,
  })
  const [submitStatus, setSubmitStatus] = useState(false)
  const handleSubmit = async (e) => {
    const data = new FormData();
    data.append('name', formData.name);
    data.append('email', formData.email)
    data.append('q1', formData.q1)
    data.append('q2', formData.q2)
    data.append('q3', formData.q3);
    data.append('resume', formData.resume)
    data.append('opp_id', opp_id)
    data.append('opp_type', opp_type)
    e.preventDefault();
    const res = await fetch('http://localhost:8000/api/apply', {
      method: 'POST',
      body: data
    });

    if (res.ok) {
      const data = await res.json();
      console.log('Submitted:', data);
      setSubmitStatus(true)
    } else {
      console.log("this failed "+res)
      console.error('Submit failed');
    }
  };
  return(
    <div className="bg-[rgba(69,69,69,0.5)] text-white p-4 px-9 text-left">
      {submitStatus === false ? (<form ref={formRef} onSubmit={handleSubmit}>
        <div className="flex justify-end gap-7 flex-row">
          <div className="flex justify-start gap-3 text-blue-500 outline-0">
            <Circle className={`${step ===1 ? "w-4":"w-2"}`}/>
            <Circle className={`${step ===2 ? "w-4":"w-2"}`}/>
            <Circle className={`${step ===3 ? "w-4":"w-2"}`}/>
          </div>
          <div className="flex justify-end text-s text-blue-500">
            {step}/3
          </div>
        </div>
        {step===1 && <StepOne nextStep={nextStep} formData = {formData} setFormData={setFormData} />}
        {step===2 && <StepTwo nextStep={nextStep} prevStep={prevStep} formData = {formData} setFormData={setFormData}/>}
        {step===3 && <StepThree submitRef={formRef} prevStep={prevStep} formData = {formData} setFormData={setFormData}/>}
        
      </form>
      ):(<div>
        <h3 className="text-blue-500 font-bold">Congrats your application has been submitted</h3>
      </div>
        )}
      </div>
  )
}
export function JobDetail(){
  const [open, setOpen] = useState(false);
  const { id } = useParams();
  const [details, setDetails] = useState({});
  const nav = useNavigate();
  useEffect(()=>{fetch(`http://localhost:8000/api/job/${id}`, {
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
      setDetails(data);
    })
    .catch((err) => {
      console.error("Fetch error:", err.message);
    });
    }, [id]);
  function handleClick(){
    setOpen(true);
    const element = document.getElementById("application");
    if (element){
      element.scrollIntoView({behavior:"smooth"});
    }
    }
  const data = {
    "opp_type": "job",
    "opp_key": id
  }
  const save = async () => {
    const res = await fetch('http://localhost:8000/api/saveopp',{
      method:'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result =>{
      console.log(result)
    });
  }
  return(
    <>
      <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
          <div className="flex justify-between">
              <div className=" flex gap-4">
                  <img src ={`http://localhost:8000/api/${details.company_logo_url}`} alt="Image logo" className="max-w-15 max-h-15 md:w-3xl md:h-auto"></img>
                  <h2 className="text-xl md:text-2xl mt-2.5">{details.company}</h2>
              </div>
              <div>
                  <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
              </div>
          </div>
          <h1 className="text-3xl text-left mt-4 ml-4">{details.company_role}</h1>
          <div className="flex gap-0 mt-4">
              <MapPin className="text-blue-500 mt-3.5 ml-3"/>
              <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.location} </p>
          </div>
          
          <p className="text-gray-300 text-left mt-3 ml-5 text-md" >${details.pay} / hour </p>
          <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
              <button onClick={handleClick} className="flex bg-blue-500 hover:bg-blue-600 px-6 rounded-3xl text-white py-3">
                Apply
                <Pencil className="ml-1 h-5 mt-1"/>
              </button>
              <button onClick={save} className = "flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
                Save
                <BookMarked className="ml-1 h-5 mt-1"/>
              </button>
          </div>
          <h2 className="text-lg text-left font-bold ml-4 mt-3 text-white">About this Opportunity:</h2>
          <p className = "leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.description} </p>

      </div>
      {open && <div id="application" className="mt-7 md:mt-13">
        <Application opp_id={id} opp_type = "job"/>
      </div>}
    </>
  )
}

export function VolDetail(){
  const [open, setOpen] = useState(false);
    const { id } = useParams();
    const [details, setDetails] = useState({});
    const nav = useNavigate();
    useEffect(()=>{fetch(`http://localhost:8000/api/unpaid/${id}`, {
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
        setDetails(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
      }, [id]);
    function handleClick(){
      setOpen(true);
      const element = document.getElementById("application");
      if (element){
        element.scrollIntoView({behavior:"smooth"});
      }
    }
    const save = async () => {
    const res = await fetch('http://localhost:8000/api/saveopp',{
      method:'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result =>{
      console.log(result)
    });
  }
  return(
    <>
      <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
          <div className="flex justify-between">
              <div className=" flex gap-4">
                  <img src ={`http://localhost:8000/api/${details.org_logo}`} alt="Image logo" className="max-w-15 max-h-15 md:w-3xl md:h-auto"></img>
                  <h2 className="text-xl md:text-2xl mt-2.5">{details.organization}</h2>
              </div>
              <div>
                  <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
              </div>
          </div>
          <h1 className="text-3xl text-left mt-4 ml-4">{details.unpaid_role}</h1>
          <div className="flex gap-0 mt-4">
              <MapPin className="text-blue-500 mt-3.5 ml-3"/>
              <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.unpaid_location} </p>
          </div>

          <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
              <button onClick={handleClick} className="flex bg-blue-500 hover:bg-blue-600 px-6 rounded-3xl text-white py-3">
                Apply
                <Pencil className="ml-1 h-5 mt-1"/>
              </button>
              <button onClick={save} className = "flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
                Save
                <BookMarked className="ml-1 h-5 mt-1"/>
              </button>
          </div>
          <p className="text-xs text-left ml-5 text-gray-500">Opportunity added on {details.date_added}</p>
          <h2 className="text-lg text-left font-bold ml-4 mt-3 text-white">About this Opportunity:</h2>
          <p className = "leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.unpaid_desc} </p>

      </div>
      {open && <div id="application" className="mt-7 md:mt-13">
        <Application opp_id={id} opp_type = "unpaid"/>
      </div>}
    </>
  )
}

export function EventDetail(){
  const [open, setOpen] = useState(false);
    const { id } = useParams();
    const [details, setDetails] = useState({});
    const nav = useNavigate();
    useEffect(()=>{fetch(`http://localhost:8000/api/events/${id}`, {
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
        setDetails(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
      }, [id]);
      function handleClick(){
        return
      }
      const save = async () => {
    const res = await fetch('http://localhost:8000/api/saveopp',{
      method:'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result =>{
      console.log(result)
    });
  }
  return(
    <>
      <div className="bg-[rgba(69,69,69,0.5)] text-white md:max-w-4xl p-5 md:px-7 ">
          <div className="flex justify-between">
              <div className=" flex gap-4">
                  <img src ={`http://localhost:8000/api/${details.org_logo}`} alt="Image logo" className="max-w-15 max-h-15 md:w-3xl md:h-auto"></img>
                  <h2 className="text-xl md:text-2xl mt-2.5">{details.organization}</h2>
              </div>
              <div>
                  <button onClick={()=> nav(-1)} className="text-white md:text-lg hover:text-blue-500">x</button>
              </div>
          </div>
          <h1 className="text-3xl text-left mt-4 ml-4">{details.event_name}</h1>
          <div className="flex gap-0 mt-4">
              <MapPin className="text-blue-500 mt-3.5 ml-3"/>
              <p className="text-gray-300 text-left mt-4 ml-0 text-lg"> {details.event_location} </p>
          </div>
          <p className="text-gray-300 text-left ml-5 mt-3">Join us on {details.event_date} for this event</p>

          <div className="flex gap-9 mt-5 ml-4 text-lg mb-5">
              <button onClick={handleClick} className="flex bg-blue-500 hover:bg-blue-600 px-6 rounded-3xl text-white py-3">
                Join
                <Pencil className="ml-1 h-5 mt-1"/>
              </button>
              <button onClick={save} className = "flex bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] outline-1 outline-blue-500 px-6 rounded-3xl text-blue-500 py-3">
                Save
                <BookMarked className="ml-1 h-5 mt-1"/>
              </button>
          </div>
          <p className="text-xs text-left ml-5 text-gray-500"> Event was added on {details.date_added}</p>

          <h2 className="text-lg text-left font-bold ml-4 mt-4 text-white">About this Opportunity:</h2>
          <p className = "leading-loose text-md text-left ml-4 mt-2 text-gray-300"> {details.event_desc} </p>

      </div>
    </>
  )
}
