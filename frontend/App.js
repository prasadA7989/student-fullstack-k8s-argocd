import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState({
    name: "",
    year_of_join: "",
    department: ""
  });

  const fetchStudents = async () => {
    const res = await axios.get(`${API_URL}/students`);
    setStudents(res.data);
  };

  const addStudent = async (e) => {
    e.preventDefault();

    await axios.post(`${API_URL}/students`, {
      name: form.name,
      year_of_join: parseInt(form.year_of_join),
      department: form.department
    });

    setForm({
      name: "",
      year_of_join: "",
      department: ""
    });

    fetchStudents();
  };

  const deleteStudent = async (id) => {
    await axios.delete(`${API_URL}/students/${id}`);
    fetchStudents();
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Student Records</h1>

      <form onSubmit={addStudent}>
        <input
          placeholder="Student Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Year of Join"
          value={form.year_of_join}
          onChange={(e) => setForm({ ...form, year_of_join: e.target.value })}
        />

        <input
          placeholder="Department"
          value={form.department}
          onChange={(e) => setForm({ ...form, department: e.target.value })}
        />

        <button type="submit">Add Student</button>
      </form>

      <h2>Student List</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Year of Join</th>
            <th>Department</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td>{s.id}</td>
              <td>{s.name}</td>
              <td>{s.year_of_join}</td>
              <td>{s.department}</td>
              <td>
                <button onClick={() => deleteStudent(s.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
