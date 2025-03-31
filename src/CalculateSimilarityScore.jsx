import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function CalculateSimilarityScore() {
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [score, setScore] = useState(null);

  useEffect(() => {
    document.title = "Calculate Similarity Score";
  }, []);

  const calculateScore = async () => {
    if (!jobDescription.trim()) {
      setResult({ error: "Please enter a job description." });
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/compare-resume", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ jobDescription }),
      });

      const data = await response.json();

      if (response.ok) {
        setScore(data.similarityScore);
        setResult(data);
        setShowPopup(true);
      } else {
        setResult({ error: data.error || "An error occurred." });
      }
    } catch (error) {
      setResult({ error: "Failed to fetch data. Please try again." });
    }
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  const getScoreCategory = (score) => {
    if (score < 50) return "Bad";
    if (score < 75) return "Good";
    return "Excellent";
  };

  const scoreCategory = score !== null ? getScoreCategory(score) : null;
  const scoreEmoji = {
    Bad: "😞",
    Good: "🙂",
    Excellent: "😁",
  };
  const emojiColor = {
    Bad: "text-red-500",
    Good: "text-yellow-500",
    Excellent: "text-green-500",
  };

  return (
    <div className="relative max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-16">
      <h1 className="text-2xl font-semibold text-gray-800 mb-8">
        Calculate Similarity Score
      </h1>

      {/* Textarea Input */}
      <textarea
        className="w-full h-40 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        placeholder="Enter the job description..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      ></textarea>

      {/* Button */}
      <button
        className="mt-4 w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
        onClick={calculateScore}
      >
        Calculate Score
      </button>

      {/* Display Result */}
      {result && !result.error && (
        <div className="mt-4 p-3 bg-gray-100 text-gray-800 rounded text-left">
          <h2 className="text-lg font-bold text-center">Analysis Result</h2>
          {/* <p className="mt-2"><strong>Job Education:</strong> {result.jobEducation?.join(", ") || "N/A"}</p>
          <p className="mt-2"><strong>Matched Education:</strong> {result.matchedEducation || "None"}</p> */}

          <h3 className="mt-3 font-bold">Matched Skills:</h3>
          {Object.keys(result.matchedSkills).length > 0 ? (
            <ul className="list-disc ml-5">
              {Object.keys(result.matchedSkills).map((skill) => (
                <li key={skill} className="text-green-600">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="text-red-500">None</p>
          )}

          <h3 className="mt-3 font-bold">Unmatched Skills:</h3>
          {result.unmatchedSkills.length > 0 ? (
            <ul className="list-disc ml-5">
              {result.unmatchedSkills.map((skill, index) => (
                <li key={index} className="text-red-600">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="text-green-500">All skills matched!</p>
          )}

          <h3 className="mt-3 font-bold">Similarity Score:</h3>
          <p className={`text-lg font-bold ${emojiColor[scoreCategory]}`}>
            {score}%
          </p>
        </div>
      )}

      {/* Error Message */}
      {result?.error && (
        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded">{result.error}</div>
      )}

      {/* Popup Modal */}
      <AnimatePresence>
        {showPopup && (
          <motion.div
            className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-white p-6 w-[300px] rounded-lg shadow-lg text-center relative"
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.8 }}
            >
              <h2 className="text-xl font-semibold">Similarity Score</h2>
              <p className={`mt-2 text-lg font-bold ${emojiColor[scoreCategory]}`}>
                {scoreCategory} - {score}%
              </p>

              {/* Animated Emoji */}
              <motion.div
                className={`mt-4 text-6xl ${emojiColor[scoreCategory]}`}
                animate={scoreCategory === "Excellent" ? { y: [-10, 10, -10] } : {}}
                transition={scoreCategory === "Excellent" ? { repeat: Infinity, duration: 1.2 } : {}}
              >
                {scoreEmoji[scoreCategory]}
              </motion.div>

              <button
                className="mt-4 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                onClick={closePopup}
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
