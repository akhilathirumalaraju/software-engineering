import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");  // State for input text
  const [summary, setSummary] = useState("");  // State for summary response

  const handleSummarize = async () => {
    try {
        const response = await axios.post(
            "http://localhost:5000/summarize", 
            { text },
            { headers: { "Content-Type": "application/json" } }
        );
        setSummary(response.data.summary);  // Set the summary from backend response
    } catch (error) {
        console.error("Error summarizing:", error);  // Log detailed error information
        if (error.response) {
            console.error("Response data:", error.response.data);  // Log the error response data
        }
        setSummary("Something went wrong!");  // Error message if something goes wrong
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
        onChange={(e) => setText(e.target.value)}  // Update text state on change
      />
      <br />
      <button onClick={handleSummarize}>Summarize</button>
      <h3>Summary:</h3>
      <div>{summary}</div>  {/* Display the summary */}
    </div>
  );
}

export default App;
