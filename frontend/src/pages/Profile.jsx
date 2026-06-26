import { API, mediaUrl } from "../lib/api";
import { useState } from "react";
import { useEffect } from "react";
import { ArrowUp,ArrowDown, Pencil } from "lucide-react";
import { PostCard } from "./Forum";
import { JobCard, EventCard, VolCard } from "./Cards";
function PostDisplay({posts, user}){
    return(
        <div className="flex overflow-x-auto snap-x snap-mandatory space-x-4">
            {posts.map((post, index) => (
            <div
                key={index}
                className="min-w-[250px] max-w-xs p-4 h-100 bg-[rgba(69,69,69)] flex flex-col justify-between rounded-md shadow-md flex-shrink-0"
            >
                <div className="flex gap-3">
                    <div>
                        {user.profile_pic ?<img
                                src={`${mediaUrl(user.profile_pic)}`}
                                alt="Profile"
                                className="w-15 h-15 rounded-full object-cover bg-[rgba(69,69,69)]"
                            /> : 
                            <img src ={`/YourFuture.png`} className="w-15 h-15 rounded-full object-cover bg-[rgba(69,69,69)]" alt="Image logo"/>}  
                    </div>
                    <div>
                        <h3 className="font-bold text-white text-left text-md">{post.added_by}</h3>
                        <p className="text-xs text-gray-300 text-left">{user.full_name}</p>
                        <p className="text-gray-300 text-xs">{user.user_org}</p>
                    </div>

                </div>
                <p className="text-gray-300 text-sm mt-9 text-left">{post.post_content}</p>
                <div className="flex justify-center mt-9">
                    {post.post_media && (<img src ={`${mediaUrl(post.post_media)}`} className="max-w-100 max-h-100 " alt="Image logo"/>)}
                </div>
                <div className="flex justify-end">
                    <p className="text-gray-400 text-xs">{post.post_time}</p>
                </div>
            </div>
  ))}
        </div>
    )
}
function SavedOpps({ opps }) {
  return (
    <div>
      <h1 className="text-blue-500 text-2xl text-left mt-5 mb-6 font-semibold ">Saved</h1>
      <div className="flex flex-col justify-start">
        {opps.map((item, i) => {
            const { opp_type, opp } = item;

            if (opp_type === 'job') {
            return <JobCard key={i} job={opp} />;
            } else if (opp_type === 'unpaid') {
            return <VolCard key={i} vol={opp} />;
            } else if (opp_type === 'event') {
            return <EventCard key={i} event={opp} />;
            } else {
            return null;
            }
      })}
      </div>
    </div>
  );
}


function appliedJobs(){

}
export function MyProfile(){
    const [profile,setProfile] = useState([])
    useEffect(()=>{fetch(`${API}/myprofile`, {
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
        setProfile(data);
    })
    .catch((err) => {
        console.error("Fetch error:", err.message);
    });
    }, []);
    const [showAll, setShowAll] = useState(false);

    const experiencesToShow = showAll
    ? profile.experiences
    : profile.experiences?.slice(0, 3);
    const [isEditing, setIsEditing] = useState(false);
    const [fullName, setFullName] = useState(profile.user?.full_name || '');
    const [age, setAge] = useState(profile.user?.age || '');
    const [bio, setBio] = useState(profile.user?.bio || '');
    const [profilePic, setProfilePic] = useState(null);

    const handleSave = () => {
    // Upload logic (API calls) goes here
    console.log('Saving:', { fullName, age, bio, profilePic });

    // After save, exit edit mode
    setIsEditing(false);
    };
    const[postAll, setPostAll] = useState(false)
    const postsToShow = postAll
    ? profile.posts
    : profile.posts?.slice(0, 3);



    return (
        <div className="p-4 ">
            <div className="flex flex-col items-center mb-6 bg-[rgba(69,69,69)] p-4">
                <div className="flex justify-between items-center w-full">
                    <div className="flex justify-start gap-5 md:gap-10 w-full">
                        <div className="w-24 p-3h-24 rounded-full object-cover">
                            {profile.user?.profile_pic ?<img
                                src={`${mediaUrl(profile.user.profile_pic)}`}
                                alt="Profile"
                                className="w-24 h-24 rounded-full object-cover"
                            /> : 
                            <img src ={`/YourFuture.png`} alt="Image logo"/>}    
                        </div>
                        <div>
                            <h2 className="text-white font-semibold text-left text-2xl mb-3">{profile.user?.username}</h2>
                            <p className="text-gray-400 text-md">{profile.user?.user_org}</p>
                        </div>
                    </div>
                    <div>
                        <button onClick={() => setIsEditing(!isEditing)}>
                            <Pencil className="text-blue-500" />
                        </button>

                    </div>
                </div>
                <div className="mt-5 text-left">
                    {isEditing ? (
                        <div className="flex flex-col gap-7">
                        <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            placeholder="Full Name"
                            className="bg-[rgba(89,89,89)] p-2 text-gray-300 rounded"
                        />
                        <input
                            type="number"
                            value={age}
                            onChange={(e) => setAge(e.target.value)}
                            placeholder="Age"
                            className="bg-[rgba(89,89,89)] text-gray-300 p-2 rounded"
                        />
                        <textarea
                            value={bio}
                            onChange={(e) => setBio(e.target.value)}
                            placeholder="Bio"
                            className="bg-[rgba(89,89,89)] text-gray-300 p-2 rounded"
                        />
                        <div>
                            <label htmlFor="profile" className="text-white">Profile picture: </label>
                            <input
                                name="profile"
                                type="file"
                                accept="image/*"
                                onChange={(e) => setProfilePic(e.target.files[0])}
                                className="bg-blue-500 hover:bg-blue-700 text-white rounded-full p-2"
                            />
                        </div>
                        <button
                            onClick={handleSave}
                            className="mt-2 bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded"
                        >
                            Save
                        </button>
                        </div>
                    ) : (
                        <>
                        {profile.user?.full_name && (
                            <h1 className="text-white font-bold mb-2">{profile.user.full_name}</h1>
                        )}
                        {profile.user?.age && (
                            <h1 className="text-white mb-5">{profile.user.age}</h1>
                        )}
                        {profile.user?.bio && (
                            <div>
                            <p className="text-gray-300">{profile.user.bio}</p>
                            </div>
                        )}
                        </>
                    )}
                    </div>

            </div>

            {profile.experiences && (<div>
                <h1 className="mt-7 mb-5 font-semibold text-2xl text-left text-blue-500">Experiences</h1>
                <div className="bg-[rgba(69,69,69)] p-4">
                {experiencesToShow.map((exp, i) => (
                    <div key={i} className="text-left mb-4 border-b border-gray-200">
                        <p className="font-semibold text-white mb-1">{exp?.exp_head}</p>
                        <p className="text-gray-200 mb-2">{exp?.exp_org}</p>
                        <p className="text-gray-300">{exp?.exp_desc}</p>
                        <div className="flex justify-center mt-5 mb-3">
                            <img src = {`${mediaUrl(exp.exp_media)}`} alt="a" className="max-w-24 max-h-24"/>
                        </div>
                    </div>
                )
                )}
                <div>
                    <button
                        onClick={()=>setShowAll(!showAll)}
                        className="text-blue-500 bg-clear"
                    >{showAll ? 
                    <div className="flex"><p>See less</p><ArrowUp /></div> :
                        <div className="flex"><p>See All</p><ArrowDown /></div>}</button>
                </div>
            </div></div>)}
            {profile.posts && (<div className="mt-5"><h1 className="mt-7 mb-5 font-semibold text-2xl text-left text-blue-500">Forum Activity</h1><PostDisplay posts={profile.posts} user={profile.user}/>
            </div>)}
            {profile.saved_opps && <div><SavedOpps opps={profile.saved_opps}/></div>}
        </div>
    );

}
