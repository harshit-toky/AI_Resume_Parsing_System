import { useState } from "react";

function ResumeInput({onInputChange}) {
    const [input_type, change_input_type] = useState("text");
    const [pdfFile, setPdfFile] = useState(null);
    const [resumeText, setResumeText] = useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type === "application/pdf") {
            setPdfFile(URL.createObjectURL(file)); // Generate a preview URL
            onInputChange("", file); // Notify parent about PDF upload
        } else {
            alert("Please upload a valid PDF file.");
            setPdfFile(null);
            onInputChange("", null);
        }
    };
    
    const handleTextChange = (e) => {
        const textarea = e.target;
        textarea.style.height = "auto"; // Reset height
        textarea.style.height = `${textarea.scrollHeight}px`; 
        setResumeText(e.target.value);
        onInputChange(e.target.value, null); // Notify parent about text input
    };
    

    return (
        <div className="p-4 w-[100%] flex flex-col">
            {/* Resume Type Selection */}
            <div className="border-[3px] border-black p-4 rounded-md">
                <label htmlFor="resume_input" className="font-medium">Select Resume Type</label>
                <select 
                    style={{ margin: "10px" }} 
                    onChange={(e) => {change_input_type(e.target.value); setPdfFile(null); onInputChange("",null);}} 
                    className="border-[1px] border-blue-200 p-1 rounded-md">
                    <option value="text">Text</option>
                    <option value="pdf">PDF</option>
                </select>
            </div>

            {/* Resume Input Field */}
            <div className="mt-4">
                {input_type === "text" ? (
                    <textarea 
                        name="resume_text" 
                        id="resume_text" 
                        rows={10} 
                        cols={100} 
                        placeholder="Paste Resume here" 
                        className="border p-2 rounded-md w-full min-h-[400px] max-h-[600px] overflow-hidden transition-all duration-200 ease-in-out"
                        value={resumeText}
                        onChange={handleTextChange}
                    />
                ) : (
                    <div className="flex flex-col">
                        <input 
                            type="file" 
                            accept=".pdf" 
                            onChange={handleFileChange}
                            className="border p-2 rounded-md mb-2"
                        />
                        {pdfFile && (
                            <iframe 
                                src={pdfFile} 
                                title="PDF Preview" 
                                className="w-full h-[600px] border rounded-md"
                            ></iframe>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default ResumeInput;
