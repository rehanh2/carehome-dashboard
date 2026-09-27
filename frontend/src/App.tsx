import { useState, type FormEvent } from "react";

const API_URL = "http://127.0.0.1:8000";

// Synthetic data matching schema.sql — later these come from GET endpoints
const RESIDENTS = [{ id: 1, name: "John Smith" }, { id: 2, name: "Margaret Brown" }];
const EMPLOYEES = [{ id: 1, name: "Sarah Jones" }, { id: 2, name: "Tom Evans" }];
const CATEGORIES = ["incident", "medication", "wellbeing", "nutrition", "general"];

export default function App() {
  const [residentId, setResidentId] = useState(1);
  const [employeeId, setEmployeeId] = useState(1);
  const [category, setCategory] = useState("general");
  const [shift, setShift] = useState("day");
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setMessage("Saving...");
    try {
      const res = await fetch(`${API_URL}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resident_id: residentId,
          employee_id: employeeId,
          category,
          shift,
          content,
        }),
      });
      if (res.status === 201) {
        const saved = await res.json();
        setMessage(`Saved note #${saved.id}`);
        setContent("");
      } else {
        setMessage(`Error ${res.status}: note not saved`);
      }
    } catch {
      setMessage("Can't reach the API — is the backend running?");
    }
  }

  return (
    <main style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Carehome Dashboard</h1>
      <h2>Add carer note</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
        <label>
          Resident
          <select value={residentId} onChange={(e) => setResidentId(Number(e.target.value))}>
            {RESIDENTS.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
          </select>
        </label>
        <label>
          Carer
          <select value={employeeId} onChange={(e) => setEmployeeId(Number(e.target.value))}>
            {EMPLOYEES.map((emp) => <option key={emp.id} value={emp.id}>{emp.name}</option>)}
          </select>
        </label>
        <label>
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label>
          Shift
          <select value={shift} onChange={(e) => setShift(e.target.value)}>
            <option value="day">day</option>
            <option value="night">night</option>
          </select>
        </label>
        <label>
          Note
          <textarea rows={5} value={content} onChange={(e) => setContent(e.target.value)} required />
        </label>
        <button type="submit">Save note</button>
      </form>
      {message && <p>{message}</p>}
    </main>
  );
}