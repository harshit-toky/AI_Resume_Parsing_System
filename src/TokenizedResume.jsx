import { useEffect, useState } from "react";

export default function TokenizedResume() {
    const [resumeText, setResumeText] = useState("");

    useEffect(() => {
        document.title = "Tokenized Resume Viewer"; 
        fetch("http://127.0.0.1:5000/download-tokenized-resume")
            .then((response) => response.text())
            .then((text) => setResumeText(text))
            .catch((error) => console.error("Error fetching tokenized resume:", error));
    }, []);

    return (
        <div className="p-6 text-left">
            <h2 className="text-2xl mb-4 font-bold text-center">Tokenized Resume</h2>
            <pre className="bg-gray-100 p-4 rounded-md whitespace-pre-wrap">
                {resumeText}
            </pre>
            <a
                href="http://127.0.0.1:5000/download-tokenized-resume"
                className="mt-4 inline-block bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition"
                download
            >
                Download
            </a>
        </div>
    );
}
