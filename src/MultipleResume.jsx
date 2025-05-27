import React, { useState } from 'react';

export default function MultiResumeAnalysis() {
  const [resumeCount, setResumeCount] = useState(1);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [resumesUploaded, setResumesUploaded] = useState(false);
  const [jobDescription, setJobDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [selectedDetail, setSelectedDetail] = useState(null);

  const handleResumeCountChange = (e) => {
    const count = parseInt(e.target.value);
    setResumeCount(count);
    const updatedFiles = [...resumeFiles];
    while (updatedFiles.length < count) updatedFiles.push(null);
    setResumeFiles(updatedFiles.slice(0, count));
  };

  const handleFileChange = (index, file) => {
    const updatedFiles = [...resumeFiles];
    updatedFiles[index] = file;
    setResumeFiles(updatedFiles);
  };

  const handleFirstSubmit = async () => {
    const formData = new FormData();
    resumeFiles.forEach((file, index) => {
      if (file) {
        formData.append(`resume${index + 1}`, file);
      }
    });

    try {
      setUploading(true);
      const response = await fetch('http://localhost:5000/upload-resumes', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        setResumesUploaded(true);
      } else {
        console.error('Upload failed:', await response.text());
      }
    } catch (error) {
      console.error('Error uploading resumes:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleFinalSubmit = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/compare-multiple-resumes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobDescription })
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error submitting job description:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGoBack = () => {
    setResumesUploaded(false);
    setResults([]);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-xl mt-10">
      <h1 className="text-2xl font-bold mb-4 text-center">Multiple Resume Analysis</h1>

      <div className="mb-4">
        <label className="block mb-1 font-medium">Select number of resumes (max 4):</label>
        <select
          value={resumeCount}
          onChange={handleResumeCountChange}
          className="border border-gray-300 rounded px-3 py-2 w-full"
          disabled={resumesUploaded}
        >
          {[1, 2, 3, 4].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>

      {!resumesUploaded && (
        <>
          <div className="space-y-3 mb-4">
            {Array.from({ length: resumeCount }).map((_, i) => (
              <div key={i}>
                <label className="block mb-1 font-medium">Resume {i + 1}</label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={(e) => handleFileChange(i, e.target.files[0])}
                  className="border border-gray-300 rounded px-3 py-2 w-full"
                />
                {resumeFiles[i] && (
                  <p className="text-sm text-green-600 mt-1">Selected: {resumeFiles[i].name}</p>
                )}
              </div>
            ))}
          </div>

          <button
            onClick={handleFirstSubmit}
            disabled={uploading || resumeFiles.some(file => file === null)}
            className={`w-full px-5 py-2 font-semibold rounded transition ${
              uploading || resumeFiles.some(file => file === null)
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {uploading ? 'Uploading...' : 'Upload & Proceed to Job Description'}
          </button>
        </>
      )}

      {resumesUploaded && (
        <>
          <div className="mb-4 mt-6">
            <label className="block mb-1 font-medium">Paste Job Description</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2 w-full h-40 resize-none overflow-y-auto"
              placeholder="Enter the job description here..."
            />
          </div>

          <div className="flex gap-3 mb-4">
            <button
              onClick={handleFinalSubmit}
              className="flex-1 bg-green-600 text-white px-5 py-2 rounded hover:bg-green-700 font-semibold"
            >
              Analyze & Match Resumes
            </button>

            <button
              onClick={handleGoBack}
              className="flex-1 bg-gray-500 text-white px-5 py-2 rounded hover:bg-gray-600 font-semibold"
            >
              Go Back & Re-upload
            </button>
          </div>

          {loading && (
            <div className="flex justify-center my-4">
              <div className="w-8 h-8 border-4 border-blue-600 border-dashed rounded-full animate-spin"></div>
            </div>
          )}

          {!loading && results.length > 0 && (
            <div className="mt-6 space-y-4">
              <h2 className="text-xl font-bold">Results</h2>
              {results.map((res, idx) => (
                <div key={idx} className="p-4 border border-gray-300 rounded-md">
                  <div className="flex justify-between items-center">
                    <p><strong>{res.filename}</strong> — Similarity: <span className="font-bold">{(res.similarityScore)}%</span></p>
                    <button
                      onClick={() => setSelectedDetail(res)}
                      className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                    >
                      Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {selectedDetail && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-lg w-full relative">
            <button onClick={() => setSelectedDetail(null)} className="absolute top-2 right-2 text-gray-500 hover:text-gray-700">✕</button>
            <h3 className="text-lg font-semibold mb-4">{selectedDetail.filename} Details</h3>
            <p><strong>Similarity Score:</strong> {(selectedDetail.similarityScore).toFixed(2)}%</p>
            <div className="mt-2">
              <p className="font-semibold">Matched Skills:</p>
              {Object.entries(selectedDetail.matchedSkills).length === 0 ? (
                <p className="text-gray-500 p-2">No matched skills found.</p>
              ) :(
              <ul className="list-disc list-inside text-green-700">
                {Object.entries(selectedDetail.matchedSkills).map(([skill, [matchedSkill, confidence]], i) => (
                  <li key={i}>
                    <strong>{skill}</strong>
                  </li>
                ))}
              </ul>
              )}
            </div>
            <div className="mt-2">
              <p className="font-semibold">Unmatched Skills:</p>
              {Object.entries(selectedDetail.unmatchedSkills).length === 0 ? (
                <p className="text-gray-500 p-2">No Unmatched skills found.</p>
              ):(
              <ul className="list-disc list-inside text-red-700">
                {selectedDetail.unmatchedSkills.map((skill, i) => <li key={i}>{skill}</li>)}
              </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
