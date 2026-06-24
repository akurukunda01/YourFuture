import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import {StudentLayout} from './pages/Layout'
import Jobs from './pages/Jobs'
import {JobDetail, VolDetail, EventDetail} from './pages/OppDetail'
import JobSearchResults from './pages/JobSearchResults.jsx'
import Authentication from './pages/Authentication.jsx'
import Connection from './pages/Connection.jsx'
import {Forum} from './pages/Forum.jsx'
import './App.css'
import { MyProfile } from './pages/Profile.jsx'
function App(){
  return (
    <Router>
      <Routes>
        <Route path = "/"element={<Authentication />}/>
        <Route path = "/student" element={<StudentLayout />}>
          <Route path = "/student/jobs" element={<Jobs />}/>
          <Route path="/student/jobs/:id" element={<JobDetail />} />
          <Route path="/student/unpaid/:id" element={<VolDetail />} />
          <Route path="/student/events/:id" element={<EventDetail />}/>
          <Route path="/student/searchResults" element={<JobSearchResults />}/>
          <Route path="/student/connection" element={<Connection />}/>
          <Route path="/student/forum" element={<Forum />}/>
          <Route path="/student/profile" element={<MyProfile />} />
        </Route>
      </Routes>
    </Router>
     
  )
}

export default App
