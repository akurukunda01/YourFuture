import { Link } from 'react-router-dom';
import { MapPin, Briefcase, Lightbulb, CalendarCheck } from 'lucide-react';
export function JobCard({ job }){
    return(
    <div className=" bg-[rgba(69,69,69,0.5)] my-1.5 p-4 max-w-md md:max-w-3xl mx-auto transition-transform duration-300 hover:-translate-y-0.5">
      <div className="flex justify-between md:gap-39">
        <div className="flex gap-7 md:flex md:gap-10">
          <img src={`http://localhost:8000/api/${job.company_logo_url}`}  alt="Image logo" className="max-w-16 max-h-16 md:w-3xl md:h-auto"></img>
          <div className="items-start">
            <div className="flex flex-col justify-start ">
              <h2 className="flex justify-start text-md md:text-xl text-blue-500 font-semibold">
                {job.company_role}
              </h2>
              <div className="flex justify-start md:gap-3 gap-1 text-xs md:text-lg">
                <p className="text-white">{job.company}</p>
                <p className="text-white">-</p>
                <p className="text-white">${job.pay}</p>
              </div>
              <div className="flex gap-5 md:gap-8">
                <div className="flex gap-1.5">
                  <MapPin className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-lg">{job.job_location}</p>
                </div>
                <div className="flex gap-1.5">
                  <Briefcase className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-xl">Job</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Link to={`/student/jobs/${job.job_id}`} className=" md:text-xl text-white px-4 max-h-20  rounded hover:text-blue-500 transition">
          →
        </Link>
      </div>
    </div>
    )
}
export function VolCard({ vol }){
  return (
  <div className=" bg-[rgba(69,69,69,0.5)] my-1.5 p-4 max-w-lg md:max-w-3xl mx-auto transition-transform duration-300 hover:-translate-y-0.5">
      <div className="flex justify-between gap-7 md:gap-56">
        <div className="flex gap-8 md:gap-10">
          <img src={`http://localhost:8000/api/${vol.org_logo}`}  alt="Image logo" className="max-w-16 max-h-16 md:w-3xl md:h-auto"></img>
          <div className="items-start">
            <div className="flex flex-col justify-start ">
              <h2 className="flex justfiy-start text-md md:text-xl text-blue-500 font-semibold">
                {vol.unpaid_role}
              </h2>
              <div className="flex justify-start md:gap-5 gap-3 text-xs md:text-lg">
                <p className="text-white">{vol.organization}</p>
              </div>
              <div className="flex gap-5 md:gap-8">
                <div className="flex gap-1.5">
                  <MapPin className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-lg">{vol.unpaid_location}</p>
                </div>
                <div className="flex gap-1.5">
                  <Lightbulb className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-xl">Unpaid</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Link to={`/student/unpaid/${vol.unpaid_id}`} className=" md:text-xl text-white px-4 max-h-20  rounded hover:text-blue-500 transition">
          →
        </Link>
      </div>
    </div>
  )
}
export function EventCard({ event }){
  return(
    <div className=" bg-[rgba(69,69,69,0.5)] my-1.5 p-4 w-full max-w-md md:max-w-3xl mx-auto transition-transform duration-300 hover:-translate-y-0.5">
      <div className="flex justify-between">
        <div className="flex gap-7 md:flex md:gap-10">
          <img src={`http://localhost:8000/api/${event.org_logo}`}  alt="Image logo" className="max-w-16 max-h-16 md:w-24 md:h-24"></img>
          <div className="items-start">
            <div className="flex flex-col justify-start">
              <h2 className="flex justify-start text-md md:text-xl text-blue-500 font-semibold">
                {event.event_name}
              </h2>
              <div className="flex justify-start md:gap-5 gap-3 text-xs md:text-lg">
                <p className="text-white">{event.organization}</p>
                <p className="text-white">{event.event_date}</p>
              </div>
              <div className="flex gap-5 md:gap-8">
                <div className="flex gap-1.5">
                  <MapPin className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-lg">{event.event_location}</p>
                </div>
                <div className="flex gap-1.5">
                  <CalendarCheck className="text-blue-500 h-5 md:h-8" />
                  <p className="text-gray-300 text-xs mt-1 md:text-xl">Event</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Link to={`student/events/${event.event_id}`} className=" md:text-xl text-white px-4 max-h-20  rounded hover:text-blue-500 transition">
          →
        </Link>
      </div>
    </div>
  )

}
