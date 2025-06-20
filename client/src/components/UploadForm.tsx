import { useRef } from "react";
import iconPath from "../assets/folder.png"
const UploadForm = ({ onUpload }: { onUpload: (file: File) => void }) => {
    const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleFileChange = () => {
    const file = fileInputRef.current?.files?.[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    } else {
      alert("Please select a valid PDF file.");
    }
  };
    return (
        <>
        <div className="container">
            <h1 className="title">PDF to TXT Converter</h1>
            <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                ref={fileInputRef}
                className="uploadForm"
                id="file-upload"
            />
            <label
                htmlFor="file-upload"
                className="uploadBtn"
            >
                <p>Choose your file</p>
                <img src={iconPath} alt="Folder" width={60}/>
            </label>
        </div>
        </>
    )
}

export default UploadForm