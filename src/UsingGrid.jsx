import { useState, useEffect } from "react";
import ResumeInput from "./Input";
import Submit from "./Submit";
import Output from "./Output";
export default function UsingGrid() {
    const [resumeText, setResumeText] = useState("");
    const [pdfFile, setPdfFile] = useState(null);
    const [parsedData, setParsedData] = useState(null);

    const handleInputChange = (text, file) => {
        setResumeText(text);
        setPdfFile(file);
    };
    useEffect(() => {
        if (!resumeText.trim() && !pdfFile) {
            setParsedData(null);
        }
    }, [resumeText, pdfFile]);
    

    return (
        <div className="w-full max-w-screen overflow-hidden px-4">
            <div className="grid grid-cols-[40%_10%_50%] gap-4 mt-4 w-full">
                <div className="min-h-[400px] max-h-[600px] overflow-y-auto"><ResumeInput onInputChange={handleInputChange} /></div>

                {resumeText.trim() !== "" || pdfFile ? 
                    <>
                    <div className="mt-[500px]"><Submit resumeText={resumeText} pdfFile={pdfFile} setParsedData={setParsedData}/></div> 
                    <div>
                        {parsedData && <Output data={parsedData} />}
                    </div>
                    </>
                    : <div className='mt-[550px] font-bold text-red-400'>Please Enter your Resume</div>
                }

                
            </div>
        </div>
    );
}
