"use client";

import { useState } from "react";

export default function TeachPanel() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState<string>("");

  async function teach() {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/teach`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const data = await response.json();
    setResult(JSON.stringify(data, null, 2));
  }

  return (
    <div className="rounded-2xl border p-6">
      <input
        value={topic}
        onChange={(event) => setTopic(event.target.value)}
        className="w-full rounded-xl border px-4 py-3"
        placeholder="Teach me backpropagation..."
      />
      <button onClick={teach} className="mt-3 rounded-xl bg-black px-4 py-2 text-white">
        Generate lesson
      </button>
      {result && <pre className="mt-4 whitespace-pre-wrap text-sm">{result}</pre>}
    </div>
  );
}
