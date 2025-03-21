import { useState } from "react";
import ResumeInput from "./Input";
import Submit from "./Submit";
export default function UsingGrid() {
    const [resumeText, setResumeText] = useState("");
    const [pdfFile, setPdfFile] = useState(null);

    const handleInputChange = (text, file) => {
        setResumeText(text);
        setPdfFile(file);
    };

    return (
        <div className="w-full max-w-screen overflow-hidden px-4">
            <div className="grid grid-cols-[40%_10%_50%] gap-4 mt-4 w-full">
                <div><ResumeInput onInputChange={handleInputChange} /></div>

                {resumeText.trim() !== "" || pdfFile ? 
                    <div><Submit resumeText={resumeText} pdfFile={pdfFile} /></div> 
                    : <div className='mt-[550px] font-bold text-red-400'>Please Enter your Resume</div>
                }

                <div>Third Column (50%)</div>
            </div>
        </div>
    );
}
