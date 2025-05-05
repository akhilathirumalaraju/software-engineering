import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");  // State for input text
  const [summary, setSummary] = useState("");  // State for summary response

  const handleSummarize = async () => {
    try {
      const response = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Server error:", errorData);
        throw new Error("Failed to summarize");
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error("Error summarizing:", error);
      setSummary("Something went wrong!");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Telugu Text Summarizer</h2>
      <textarea
        rows="10"
        cols="80"
        placeholder="Enter text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <br />
      <button onClick={handleSummarize}>Summarize</button>
      <h3>Summary:</h3>
      <div>{summary}</div>
    </div>
  );
}

export default App;