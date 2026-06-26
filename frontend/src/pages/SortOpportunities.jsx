export function JobSort({ onSortChange }) {
  function handleChange(event) {
    onSortChange(event.target.value);
  }

  return (
    <div className="flex text-xs bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] px-2 py-2 md:px-4 md:py-5 md:text-lg rounded-2xl md:rounded-full text-white">
      <select id="sort" className="" onChange={handleChange}>
        <option value="Oldest">Oldest</option>
        <option value="Latest">Latest</option>
        <option value="pay-asc">Pay asc</option>
        <option value="pay-desc">Pay desc</option>
        <option value="company-az">Alphabetical</option>
      </select>
    </div>
  )
}
export function EventSort({ onSortChange }){
    function handleChange(event) {
    onSortChange(event.target.value);
  }

  return (
    <div className="flex text-xs hover:bg-[rgba(89,89,89,0.5)] bg-[rgba(69,69,69,0.5)] px-2 py-2 md:px-4 md:py-5 md:text-lg rounded-2xl md:rounded-full text-white">
      <select id="sort" className="" onChange={handleChange}>
        <option value="Oldest">Oldest</option>
        <option value="Latest">Latest</option>
        <option value='Event_Date'>Event Date</option>
        <option value="name-az">Alphabetical</option>
      </select>
    </div>
  )
}
export function VolSort({ onSortChange }){
    function handleChange(event) {
    onSortChange(event.target.value);
  }

  return (
    <div className="flex text-xs bg-[rgba(69,69,69,0.5)] hover:bg-[rgba(89,89,89,0.5)] px-2 py-2 md:px-4 md:py-5 md:text-lg rounded-2xl md:rounded-full text-white">
      <select id="sort" className="" onChange={handleChange}>
        <option value="Oldest">Oldest</option>
        <option value="Latest">Latest</option>
        <option value="name-az">Alphabetical</option>
      </select>
    </div>
  )
}