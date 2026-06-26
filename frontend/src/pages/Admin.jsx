import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../lib/api";

const TYPES = {
  job: {
    label: "Job",
    endpoint: "jobs",
    fields: [
      ["company", "Company", true],
      ["company_role", "Role", true],
      ["apply_url", "Apply URL (https://...)", true],
      ["pay", "Pay (e.g. $20/hr)", false],
      ["job_location", "Location", false],
      ["company_logo_url", "Logo image URL", false],
      ["job_description", "Description", false, "textarea"],
    ],
  },
  unpaid: {
    label: "Internship / Volunteer",
    endpoint: "unpaid",
    fields: [
      ["organization", "Organization", true],
      ["unpaid_role", "Role", true],
      ["apply_url", "Apply URL (https://...)", true],
      ["unpaid_location", "Location", false],
      ["org_logo", "Logo image URL", false],
      ["unpaid_desc", "Description", false, "textarea"],
    ],
  },
  event: {
    label: "Event",
    endpoint: "events",
    fields: [
      ["organization", "Organization", true],
      ["event_name", "Event name", true],
      ["apply_url", "Register URL (https://...)", true],
      ["event_location", "Location", false],
      ["event_date", "Date (YYYY-MM-DD)", false],
      ["org_logo", "Logo image URL", false],
      ["event_desc", "Description", false, "textarea"],
    ],
  },
};

const input = "bg-[rgba(89,89,89)] text-white px-3 py-2 rounded w-full";

function ListingForm({ onCreated }) {
  const [type, setType] = useState("job");
  const [form, setForm] = useState({});
  const [msg, setMsg] = useState(null);
  const cfg = TYPES[type];

  const submit = async (e) => {
    e.preventDefault();
    setMsg(null);
    const res = await fetch(`${API}/admin/${cfg.endpoint}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      setMsg({ ok: true, text: `${cfg.label} created.` });
      setForm({});
      e.target.reset();
      onCreated();
    } else {
      setMsg({ ok: false, text: data.error || "Failed to create listing." });
    }
  };

  return (
    <form onSubmit={submit} className="bg-[rgba(69,69,69)] p-5 rounded text-white flex flex-col gap-3">
      <h2 className="text-blue-500 text-xl font-semibold">Create a listing</h2>
      <select
        value={type}
        onChange={(e) => { setType(e.target.value); setForm({}); }}
        className="bg-blue-500 hover:bg-blue-700 text-white px-3 py-2 rounded w-full"
      >
        {Object.entries(TYPES).map(([k, v]) => (
          <option key={k} value={k}>{v.label}</option>
        ))}
      </select>
      {cfg.fields.map(([name, label, required, kind]) => (
        kind === "textarea" ? (
          <textarea key={name} name={name} placeholder={label} rows={3}
            className={input}
            value={form[name] || ""}
            onChange={(e) => setForm({ ...form, [name]: e.target.value })} />
        ) : (
          <input key={name} name={name} placeholder={label + (required ? " *" : "")}
            className={input}
            value={form[name] || ""}
            onChange={(e) => setForm({ ...form, [name]: e.target.value })} />
        )
      ))}
      {msg && <p className={msg.ok ? "text-green-400" : "text-red-400"}>{msg.text}</p>}
      <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white py-2 rounded">
        Publish {cfg.label}
      </button>
    </form>
  );
}

function ListingRow({ title, subtitle, onDelete }) {
  return (
    <div className="flex justify-between items-center bg-[rgba(69,69,69)] p-3 rounded">
      <div className="text-left">
        <p className="text-white">{title}</p>
        <p className="text-gray-400 text-sm">{subtitle}</p>
      </div>
      <button onClick={onDelete} className="text-red-400 hover:text-red-300 px-3">Delete</button>
    </div>
  );
}

export default function Admin() {
  const nav = useNavigate();
  const [listings, setListings] = useState({ jobs: [], unpaid: [], events: [] });

  const load = useCallback(() => {
    fetch(`${API}/admin/listings`, { credentials: "include" })
      .then((res) => {
        if (res.status === 401 || res.status === 403) { nav("/"); return null; }
        return res.json();
      })
      .then((data) => data && setListings(data))
      .catch((err) => console.error(err));
  }, [nav]);

  useEffect(() => { load(); }, [load]);

  const del = async (endpoint, id) => {
    await fetch(`${API}/admin/${endpoint}/${id}`, { method: "DELETE", credentials: "include" });
    load();
  };

  const logout = async () => {
    await fetch(`${API}/logout`, { method: "POST", credentials: "include" });
    nav("/");
  };

  return (
    <div className="min-h-screen bg-[rgba(49,49,49)] p-6">
      <div className="flex justify-between items-center mb-6">
        <img src="/YourFuture.png" className="invert w-32" alt="YourFuture" />
        <div className="flex gap-4">
          <span className="text-gray-300 self-center">Admin</span>
          <button onClick={logout} className="text-blue-400 hover:text-blue-300">Log out</button>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
        <ListingForm onCreated={load} />

        <div className="flex flex-col gap-4">
          <div>
            <h3 className="text-blue-500 text-lg mb-2 text-left">Jobs</h3>
            <div className="flex flex-col gap-2">
              {listings.jobs.map((j) => (
                <ListingRow key={j.job_id} title={`${j.company_role} · ${j.company}`}
                  subtitle={j.apply_url} onDelete={() => del("jobs", j.job_id)} />
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-blue-500 text-lg mb-2 text-left">Internships / Volunteer</h3>
            <div className="flex flex-col gap-2">
              {listings.unpaid.map((u) => (
                <ListingRow key={u.unpaid_id} title={`${u.unpaid_role} · ${u.organization}`}
                  subtitle={u.apply_url} onDelete={() => del("unpaid", u.unpaid_id)} />
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-blue-500 text-lg mb-2 text-left">Events</h3>
            <div className="flex flex-col gap-2">
              {listings.events.map((e) => (
                <ListingRow key={e.event_id} title={`${e.event_name} · ${e.organization}`}
                  subtitle={e.apply_url} onDelete={() => del("events", e.event_id)} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
