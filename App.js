import React, { useState, useEffect } from "react";
import { classifyTicket, createTicket, fetchTickets, fetchStats } from "./api";

export default function App() {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [category, setCategory] = useState("general");
    const [priority, setPriority] = useState("low");
    const [tickets, setTickets] = useState([]);
    const [stats, setStats] = useState({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadTickets();
        loadStats();
    }, []);

    const loadTickets = async () => {
        const data = await fetchTickets();
        setTickets(data);
    };

    const loadStats = async () => {
        const data = await fetchStats();
        setStats(data);
    };

    const handleClassify = async () => {
        if (!description) return;
        setLoading(true);
        const result = await classifyTicket(description);
        if (result.suggested_category) setCategory(result.suggested_category);
        if (result.suggested_priority) setPriority(result.suggested_priority);
        setLoading(false);
    };

    const handleSubmit = async () => {
        await createTicket({ title, description, category, priority });
        setTitle("");
        setDescription("");
        loadTickets();
        loadStats();
    };

    return (
        <div style={{ padding: 20 }}>
            <h1>Support Ticket System</h1>

            <h2>Create Ticket</h2>
            <input
                placeholder="Title"
                value={title}
                maxLength={200}
                onChange={e => setTitle(e.target.value)}
            />
            <br /><br />
            <textarea
                placeholder="Description"
                value={description}
                onChange={e => setDescription(e.target.value)}
                onBlur={handleClassify}
            />
            <br />
            {loading && <p>Classifying...</p>}
            <br />
            <select value={category} onChange={e => setCategory(e.target.value)}>
                <option value="billing">Billing</option>
                <option value="technical">Technical</option>
                <option value="account">Account</option>
                <option value="general">General</option>
            </select>

            <select value={priority} onChange={e => setPriority(e.target.value)}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
            </select>

            <br /><br />
            <button onClick={handleSubmit}>Submit</button>

            <h2>Stats</h2>
            <pre>{JSON.stringify(stats, null, 2)}</pre>

            <h2>Tickets</h2>
            {tickets.map(t => (
                <div key={t.id} style={{ border: "1px solid gray", margin: 10, padding: 10 }}>
                    <b>{t.title}</b>
                    <p>{t.description}</p>
                    <p>{t.category} | {t.priority} | {t.status}</p>
                </div>
            ))}
        </div>
    );
}
