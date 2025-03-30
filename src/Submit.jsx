import { useState } from "react";

export default function Submit({ resumeText, pdfFile, setParsedData }) {
    const [loading, setLoading] = useState(false); // State for progress meter
    // const [result, setResult] = useState(null);   // State for extracted data

    const handleSubmit = async () => {
        setLoading(true); // Start loading
        const formData = new FormData();
    
        let response;
        if (pdfFile) {
            formData.append("pdfFile", pdfFile);
            response = await fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                body: formData,
            });
        } else {
            response = await fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ resumeText }),
            });
        }
    
        await response.json(); // Ensure request completes
    
        // 🔥 Fetch parsed JSON resume
        try {
            const resultResponse = await fetch("http://127.0.0.1:5000/get-parsed-resume", {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            });
    
            if (!resultResponse.ok) {
                throw new Error("Failed to fetch parsed resume data");
            }
    
            const responseData = await resultResponse.json(); // ✅ Parse JSON response
            setParsedData(responseData); // ✅ Store parsed data
            console.log("Parsed Resume Data:", responseData);
        } catch (error) {
            console.error("Error fetching parsed resume:", error);
        }
    
        setLoading(false); // Stop loading
    };
    


    return (
        <div className="mt-10 flex flex-col items-center">
            <button
                className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition"
                onClick={handleSubmit}
                disabled={loading} // Disable button when processing
            >
                {loading ? "Processing..." : "Submit"}
            </button>

            {/* Progress Bar */}
            {loading && (
                <div className="w-1/2 mt-4 bg-gray-200 rounded-full">
                    <div className="bg-green-500 text-xs font-medium text-center p-1 leading-none rounded-full animate-pulse" style={{ width: "80%" }}>
                        Processing...
                    </div>
                </div>
            )}
        </div>
    );
}
