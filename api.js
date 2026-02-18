const API = "http://localhost:8000/api";

export const fetchStats = async () => {
    const res = await fetch(`${API}/tickets/stats/`);
    return res.json();
};

export const createTicket = async (data) => {
    const res = await fetch(`${API}/tickets/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
};

export const fetchTickets = async () => {
    const res = await fetch(`${API}/tickets/`);
    return res.json();
};

