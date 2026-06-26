import { API } from "../lib/api";
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import {JobCard, VolCard, EventCard} from "./Cards";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function SearchResultsPage() {
  const query = useQuery().get("q");
  const nav = useNavigate()
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }

    setLoading(true);
    fetch(`${API}/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => setResults(data))
      .catch((err) => console.error("Fetch error:", err))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <div className="p-4">
      <button onClick={()=>nav(-1)} className="text-white text-3xl  md:text-5xl flex justify-start hover:text-blue-500">˂</button>
      <h1 className="text-xl md:text-3xl text-white font-semibold mb-8 md:mb-13">Search Results for "{query}"</h1>
      {loading && <p>Loading...</p>}
      {!loading && results.length === 0 && <p>No results found.</p>}
      <div>
        {results.map((opp, index) => {
          if (opp.type === "job") {
            return <JobCard key={index} job={opp} />;
          } else if (opp.type === "unpaid") {
            return <VolCard key={index} vol={opp} />;
          } else if (opp.type === "event") {
            return <EventCard key={index} event={opp} />;
          } else {
            return null;
          }
        })}
      </div>
    </div>
  );
}

export default SearchResultsPage;
