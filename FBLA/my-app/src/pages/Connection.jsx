import { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Mailbox, Plus, Send} from 'lucide-react'

function SResults({result}){
  const[open, setOpen] = useState(true);
  return (
    (open && (<div className="flex justify-between px-3 py-1 text-white bg-[rgba(69,69,69,0.5)] text-left border-1 border-blue-500 hover:bg-[rgba(69,69,69)]">
      {result}
      <button className="hover:text-blue-500" onClick={()=>setOpen(false)}>x</button>
    </div>))
  )
}

function MessageModal({open, setOpen}){
    const [submitted, setStatus] = useState(false);
    const[query, setQuery] = useState('')
    const [formData, setFormData] = useState({
      "reciever":'',
      "msg_content": ''
    })
    const[results, setResults] = useState([])
    useEffect(() => {
      if (query.trim() === ''){
        setResults([]);
        return;
      }

      const delayDebounce = setTimeout(() => {
        fetch(`http://localhost:8000/api/reciever?q=${query}`,{
          credentials:"include"
        })
          .then((res) => res.json())
          .then((data) => {
            setResults(data);
            setFormData((prev) =>({prev, reciever:query}));
          })
          .catch((err) => console.error("Search error:", err));
      }, 300); 

      return () => clearTimeout(delayDebounce);
    } , [query]);
    const handleSubmit = async (e) => {
        const data = new FormData();
        data.append('reciever', formData.reciever);
        data.append('msg_content', formData.msg_content)
        e.preventDefault();
        const res = await fetch('http://localhost:8000/api/sendmessages', {
        method: 'POST',
        body: data,
        credentials:"include"
        });

        if (res.ok) {
        const data = await res.json();
        console.log('Submitted:', data);
        setStatus(true)
        
        } else {
        console.log("this failed "+res)
        console.error('Submit failed');
        }
    }
    return(
        <>
        <div className=" bg-[rgba(69,69,69)] px-3 py-2 shadow-2xl ">
            <div className="flex justify-end">
              <button onClick={()=>setOpen(false)}>
                <div className=" text-white hover:text-blue-500">
                  X
                </div>
              </button>
            </div>
            {submitted === false && (<div>
              <div className="flex justify-center">
                <h2 className="text-blue-500 font-bold text-xl">Message</h2>
              </div>
                <form onSubmit={handleSubmit}>
                  <div className="p-7">
                    <div>
                      <input required value={query} onChange={(e)=> setQuery(e.target.value)}className="bg-[rgba(89,89,89)] text-white p-3 mb-5 rounded-2xl "name="reciever" placeholder="Sending to..."></input>
                    </div>
                    {Array.isArray(results) && results.slice(0, 4).map((result,i) => (
                      <div onClick={() => {
                          setQuery(result);
                          setFormData((prev) => ({ ...prev, reciever: result})); // updates formData
                          setResults([]); 
                        }}className="mb-0.5">
                        <SResults key={i} result={result} />
                      </div>
                    ))}

                    <div>
                    <textarea required onChange={(e)=>setFormData({...formData, msg_content: e.target.value})}className="bg-[rgba(89,89,89)] text-white p-3 rounded-2xl " name="content" rows={5} placeholder="Add Message Content"></textarea>
                    </div>
                  </div>
                  <div className="flex justify-end">
                      <button type="submit" className="text-blue-500 hover:text-blue-700"><Send /></button>
                  </div>
                </form>
            </div>)}
            {submitted && (<div className="p-5 font-semibold text-blue-500">
              Message has been sent
              </div>)}
          </div>
        </>
    )
}
function Connection(){
    const[open, setOpen] = useState(false);
    const[list, setList] = useState({});
    const[selectedSender, setSelectedSender] = useState(null);
    useEffect(() => {
        fetch("http://localhost:8000/api/getmessages", {
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
    function AddMessage(){
        setOpen(true);
    }
    const messages = selectedSender ? list[selectedSender] : [];
    return (
    <div>
      <h1 className="text-blue-500 text-5xl font-bold mb-10">Connections</h1>
      <div className="grid grid-cols-12 min-h-200 max-h-200 overflow-y-auto">
        <div className="col-span-4 md:col-span-3 p-4 bg-[rgba(69,69,69,0.5)]">
            <div className="flex gap-2 ">
                <h2 className="text-lg text-white mb-4">Inbox</h2>
                <Mailbox className="text-blue-500 h-7"/>
            </div>
            <div className="flex">
                <button onClick={AddMessage} className="bg-blue-500 text hover:bg-blue-700 mb-5 px-2  md:px-2 py-1 rounded-full ">
                    <div className="flex gap-1">
                        <p>Message</p>
                        <Plus />
                    </div>
                    </button>
            </div>

            {Object.keys(list).length === 0 ? (
            <p className="text-gray-300">No message threads yet.</p>
            ) : (
            Object.entries(list)
                .sort(([, aMessages], [, bMessages]) => {
                const aLast = new Date(aMessages[aMessages.length - 1]?.date || 0);
                const bLast = new Date(bMessages[bMessages.length - 1]?.date || 0);
                return bLast - aLast;
                })
                .map(([username]) => (
                <button
                    key={username}
                    onClick={() => setSelectedSender(username)}
                    className={`block w-full text-left p-2 rounded mb-1 ${
                    selectedSender === username
                        ? "bg-blue-500 text-white"
                        : "hover:bg-[rgba(69,69,69,0.5)] text-gray-400"
                    }`}
                >
                    {username}
                </button>
                ))
            )}
        </div>

        <div className="col-span-8 md:col-span-9 p-6 overflow-y-auto max-h-200">
          {selectedSender ? (
            <>
              
              {messages.length > 0 ? (
                <ul className="space-y-4">
                  {messages.map((msg) => (
                    <li key={msg.id} className="w-full px-4 py-1">
                      <div
                        className={`flex ${
                          msg.sender_username === selectedSender ? "justify-start" : "justify-end"
                        }`}
                      >
                        <div
                          className={`max-w-xs p-3 rounded-lg ${
                            msg.sender_username === selectedSender
                              ? "bg-[rgba(69,69,69,0.5)] text-white"
                              : "bg-blue-500 text-white"
                          }`}
                        >
                          <div className="text-xs mb-1">
                            {new Date(msg.date).toLocaleString()}
                          </div>
                          <div>{msg.content}</div>
                        </div>
                      </div>
                    </li>

                  ))}
                </ul>
              ) : (
                <p className="text-gray-300">No messages from this sender.</p>
              )}
            </>
          ) : (
            <div className="flex justify-center">
              <div className="m-5">
                <p className="text-gray-300 text-center mb-5">Select a sender to view messages.</p>
                <Send className="text-blue-500 w-50 h-12"/>
              </div>
            </div>
          )}
        </div>
      </div>
      {(open && <div className=" fixed inset-0 flex justify-center items-center z-50">
            <MessageModal open={open} setOpen={setOpen} />
        </div>)}
    </div>
  );
}
export default Connection;