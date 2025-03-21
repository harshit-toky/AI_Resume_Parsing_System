export default function Submit({ resumeText, pdfFile }) {
    const handleSubmit = async () => {
        const formData = new FormData();
    
        if (pdfFile) {
            formData.append("pdfFile", pdfFile);
    
            const response = await fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json();
            console.log("Extracted Text:", result.extractedText);
        } else {
            const response = await fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ resumeText }),
            });
    
            const result = await response.json();
            console.log("Submitted Text:", result.resumeText);
        }
    };
    

    return (
        <div className="mt-[550px]">
            <button 
                className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition" 
                onClick={handleSubmit}
            >
                Submit
            </button>
        </div>
    );
}