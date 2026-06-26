import { API, mediaUrl } from "../lib/api";
import { useState, useEffect } from "react";
import { Send } from "lucide-react";
export function PostCard({post}){
    return(
        <div className="bg-[rgba(69,69,69)] hover:bg-[rgba(89,89,89)] max-w-xl md:max-w-3xl border-b border-gray-200 text-white py-2 px-5">
            <div className="flex justify-start gap-3 mt-3">
                <div>
                  <img src ={`${mediaUrl(post.profile_pic)}`} className="h-15"/>
                </div>
                <div className="flex text-left flex-col gap-0 ">
                    <h2 className="text-white font-bold">{post.added_by}</h2>
                    <p className="text-gray-300 text-xs">{post.full_name}</p>
                    <p className="text-gray-300 text-xs">{post.user_org}</p>
                </div>
                
            </div>
            <p className="text-left text-gray-300 mt-10">{post.post_content}</p>
            <div className="flex justify-center mt-10">
                {post.post_media &&(<img src={`${mediaUrl(post.post_media)}`} className="max-w-100"></img>)}
            </div>
            <div className="flex justify-end">
              <p className='text-xs mt-7 text-gray-400'>{post.post_time}</p>
            </div>
        </div>
    )
}
function PostModal({open, setOpen}){
    const[submitted, setStatus] = useState(false)
    const[formData, setFormData] = useState({
        "post_content":'',
        "post_media":''

    })
    const handleSubmit = async (e) => {
        const data = new FormData();
        data.append('post_content', formData.post_content);
        data.append('post_media', formData.post_media)
        e.preventDefault();
        const res = await fetch(`${API}/addpost`, {
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
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFormData({ ...formData, post_media: file });
    };
    return(
        <div className="bg-[rgba(69,69,69)] px-4 py-2 shadow-2xl">
            <div className="flex justify-end  text-white hover:text-blue-500">
                    <button onClick={()=>setOpen(false)}>x</button>
            </div>
            {submitted ? <div className="w-75 text-xl p-3">
                <h1 className="text-blue-500 font-bold">Post has been sent for review</h1>
            </div>:
            <div>
                
                <h2 className="text-xl text-blue-500 font-bold mb-7">Add Post</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-7">
                        <textarea required type="text" rows={5} name="content" placeholder="Post Content" className="text-gray-300 p-2 w-75 bg-[rgba(89,89,89)]" onChange={(e)=>setFormData({...formData, post_content:e.target.value })}></textarea>
                    </div>
                    <div className="mt-5">
                        <input type="file" name="resume" onChange={handleFileChange} className="text-white  w-75 bg-blue-500 hover:bg-blue-700 px-3 py-1 rounded-full"></input>
                    </div>
                    <div className="flex justify-end mt-7">
                        <button type="submit" className=' h-9 text-blue-500 hover:text-blue-700'><Send /></button>
                    </div>
                </form>
            </div>}
        </div>
    )
}
function ForumSearch({posts, setPosts}){
  const[query,setQuery] = useState('')
  const[results, setResults] = useState([])
  useEffect(() => {
    if (query.trim() === ''){
        fetch(`${API}/getposts`)
        .then(res => res.json())
        .then(data => setPosts(data))
        .catch(err => console.error(err));
    return;
    }

    const delayDebounce = setTimeout(() => {
      fetch(`${API}/postsearch?q=${query}`,{
        credential:"include"
      })
        .then((res) => res.json())
        .then((data) => setPosts(data))
        .catch((err) => console.error("Search error:", err));
    }, 300); 

    return () => clearTimeout(delayDebounce);
  }, [query]);
  return (
    <>
        <div className="flex flex-col justify-center">
          <div className="relative w-full md:w-xl">
            <input className = "w-xs border-0 rounded-3xl md:w-xl md:text-xl px-5 py-2 bg-[rgba(69,69,69)] text-white" placeholder="Search Forum ie. people or topics" autoComplete="on" onChange={(e)=> setQuery(e.target.value)} value={query}/>
          </div>
        </div>
    </>
  )
}
export function Forum(){
    const[posts, setPosts] = useState([]);
    const [open, setOpen] = useState(false);
    useEffect(() => {
    fetch(`${API}/getposts`, {
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
        setPosts(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err.message);
      });
  }, []);
  function handleClick(){
    setOpen(true);
    const element = document.getElementById("modal");
    if (element){
      element.scrollIntoView({behavior: 'smooth', block:'start'});

    }
    }
  return (
    <div className="flex flex-col justify-center">
        <div>
            <h1 className="text-5xl text-blue-500 font-extrabold">Forum</h1>
        </div>
        <div className="flex justify-center m-9">
            <ForumSearch posts={posts} setPosts={setPosts}/>
        </div>
        <div>
            <button onClick={handleClick} className="bg-blue-500 px-4 py-1.5 rounded-full">Start a New Post</button>
            {open &&(<div name="modal"className="fixed inset-0 max-h-200 flex justify-center items-center z-50">
                <PostModal open={open} setOpen={setOpen}/>
            </div>)}
        </div>
        <div className="flex justify-center mt-5">
            <div className="bg-clear">
                    {posts.length === 0 && <p>No posts found.</p>}
            </div>
            <div className="">
                {posts.length >0 && posts.slice().reverse().map((post, index) => (
                <PostCard key={index} post={post} />
                ))}
            </div>
        </div>
    </div>
  )
}
