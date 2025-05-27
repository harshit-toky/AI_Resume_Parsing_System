import React, { useState } from "react";

export default function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState({});

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type !== "application/pdf") {
      alert("Please upload a PDF file.");
      e.target.value = null;
      setFile(null);
    } else {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("resume", file);
      const response = await fetch("http://localhost:5000/check-authenticity", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      console.log("Authenticity result:", result);
      setResult(result);
    } catch (err) {
      alert("Error uploading file: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-black p-6">
      <h1 className="text-4xl font-bold mb-10 border-b border-black pb-2 w-full text-center">
        Resume Authenticity Checker
      </h1>

      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-lg p-8">
        <label
          htmlFor="resume-upload"
          className="block mb-3 font-semibold text-lg text-center"
        >
          Upload your Resume (PDF only)
        </label>
        <input
          id="resume-upload"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="block w-full mb-6 text-black mt-6"
        />

        <div className="flex justify-center">
          <button
            onClick={handleSubmit}
            className="w-[30%] bg-blue-600 text-white mt-2 py-3 rounded-md hover:bg-blue-800 transition"
          >
            <p className="">Check Resume Authenticity</p>
          </button>
        </div>
      </div>


      {loading && (
        <div className="flex justify-center my-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-dashed rounded-full animate-spin"></div>
        </div>
      )}

      {Object.keys(result).length > 0 && !loading && (
        <div className="max-w-3xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-2xl border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Authenticity Result
          </h2>

          <div className="mb-4">
            <p className="text-lg">
              <span className="font-medium">AI Score:</span> {result.ai_score}
            </p>
            <p className="text-lg">
              <span className="font-medium">Authenticity Score:</span>{" "}
              {result.authenticity_score}
            </p>
            <p className="text-lg">
              <span className="font-medium">Suspected AI:</span>{" "}
              <span
                className={
                  result.is_suspected_ai
                    ? "text-red-600 font-bold"
                    : "text-green-600 font-semibold"
                }
              >
                {result.is_suspected_ai ? "Yes" : "No"}
              </span>
            </p>
          </div>

          {result.authenticity_flags?.length > 0 && (
            <div className="mb-4">
              <h3 className="font-semibold text-gray-700 mb-1">
                Authenticity Flags:
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                {result.authenticity_flags.map((flag, idx) => (
                  <li key={idx}>{flag}</li>
                ))}
              </ul>
            </div>
          )}

          {result.unsupported_skills?.length > 0 && (
            <div className="mb-4">
              <h3 className="font-semibold text-gray-700 mb-1">
                Unsupported Skills:
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                {result.unsupported_skills.map((skill, idx) => (
                  <li key={idx}>{skill}</li>
                ))}
              </ul>
            </div>
          )}

          {result.invalid_companies?.length > 0 && (
            <div className="mb-4">
              <h3 className="font-semibold text-gray-700 mb-1">
                Invalid Companies:
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                {result.invalid_companies.map((company, idx) => (
                  <li key={idx}>{company}</li>
                ))}
              </ul>
            </div>
          )}

          {result.triggered_buzzwords?.length > 0 && (
            <div className="mb-4">
              <h3 className="font-semibold text-gray-700 mb-1">
                Triggered Buzzwords:
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                {result.triggered_buzzwords.map((word, idx) => (
                  <li key={idx}>{word}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
