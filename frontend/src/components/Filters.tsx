export default function Filters() {
  return (
    <div className="filters panel">
      <div>
        <label>Confidence</label>
        <select>
          <option value="">All</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>
      <div>
        <label>Category</label>
        <select>
          <option value="">All</option>
          <option value="streaming">Streaming</option>
          <option value="newsletters">Newsletters</option>
          <option value="finance">Finance</option>
          <option value="tools">Tools</option>
        </select>
      </div>
      <button className="btn secondary">Export CSV</button>
    </div>
  );
}
