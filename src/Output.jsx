import React from "react";

const openTokenizedResume = () => {
    window.open("/tokenized-resume", "_blank");
};

const calculateSimilarityScore = () => {
    window.open("/similarityScore", "_blank");
};

export default function Output({ data }) {
    if (!data || Object.keys(data).length === 0) {
        return <p className="text-red-500 text-center">No parsed data available.</p>;
    }

    return (
        <div className="mt-4 mr-8 p-6 bg-gray-100 rounded-md w-f mx-auto shadow-md text-left min-h-[400px] max-h-[600px] overflow-y-auto">
            <h2 className="text-2xl font-semibold mb-4 text-center">Extracted Resume Data</h2>

            {/* Personal Information */}
            <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                <h3 className="text-lg font-semibold border-b pb-2">Personal Information</h3>
                <p><strong>Name:</strong> {data.name}</p>
                <p><strong>Email:</strong> {data.email}</p>
                <p><strong>Phone:</strong> {data.phone}</p>
                {data.links && data.links.length > 0 && (
                    <div className=" bg-white rounded-md">
                        <h3 className="text-base font-bold pb-2">Links</h3>
                        <ul className="list-disc ml-12">
                            {data.links.map((link, index) => (
                                <li key={index}><a href={link} className="text-blue-500 ml-2" target="_blank" rel="noopener noreferrer">
                                {link}
                            </a></li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Education */}
            {data.education && data.education.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Education</h3>
                    <ul className="list-disc ml-6">
                        {data.education.map((edu, index) => (
                            <li key={index}>    {edu.details}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Skills */}
            {data.skills && data.skills.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Skills</h3>
                    <p className="text-gray-700">{data.skills.join(", ")}</p>
                </div>
            )}

            {/* Experience */}
            {data.experience && data.experience.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Experience</h3>
                    <ul className="list-disc ml-6">
                        {data.experience.map((exp, index) => (
                            <li key={index}>
                                <strong>{exp.role}:</strong> {exp.details || exp.duration}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Projects */}
            {data.projects && data.projects.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Projects</h3>
                    {data.projects.map((project, index) => (
                        <div key={index} className="mb-2">
                            <p><strong>{project.title} ({project.duration})</strong></p>
                            <p className="text-gray-700">{project.description}</p>
                        </div>
                    ))}
                </div>
            )}

            {/* Certifications */}
            {data.certifications && data.certifications.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Certifications</h3>
                    <ul className="list-disc ml-6">
                        {data.certifications.map((cert, index) => (
                            <li key={index}>{cert}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Achievements */}
            {data.achievements && data.achievements.length > 0 && (
                <div className="mb-4 p-4 bg-white rounded-md shadow-sm">
                    <h3 className="text-lg font-semibold border-b pb-2">Achievements</h3>
                    <ul className="list-disc ml-6">
                        {data.achievements.map((ach, index) => (
                            <li key={index}>{ach}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* View Tokenized Resume */}
            <div className="mt-6 flex justify-between">
                <div>
                <button
                    className="bg-blue-500 w-[200px] text-white px-6 py-2 rounded-md hover:bg-blue-600 transition ml-4"
                    onClick={openTokenizedResume}
                >
                    View Tokenized Resume
                </button>
                </div>
                <div>
                    <button
                        className="bg-blue-500 w-[200px] text-white px-6 py-2 rounded-md hover:bg-blue-600 transition mr-4"
                        onClick={calculateSimilarityScore}
                    >
                        Calculate Similarity Score
                    </button>
                </div>
            </div>
        </div>
    );
}

