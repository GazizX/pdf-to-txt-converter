
import { useState } from 'react';
import './App.css'
import Processing from './components/Processing'
import UploadForm from './components/UploadForm';
import Result from './components/Result';
import { uploadPDF } from './services/api';

function App() {
  const [stage, setStage] = useState("upload"); // 'upload', 'processing', 'result'
  const [txtBlob, setTxtBlob] = useState<Blob | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const handleUpload = async (file: any) => {
    setStage("processing");
    try {
      const [blob, fileName] = await uploadPDF(file);
      setTxtBlob(blob);
      setFileName(fileName)
      setStage("result");
    } catch (error) {
      console.log(error)
      alert("Conversion failed. Try again.");
      setStage("upload");
    }
  };

  const reset = () => {
    setTxtBlob(null);
    setStage("upload");
  };

  return (
    <>
      {stage === "upload" && <UploadForm onUpload={handleUpload} />}
      {stage === "processing" && <Processing />}
      {stage === "result" && <Result blob={txtBlob} fileName={fileName} onReset={reset} />}
    </>
  )
}

export default App


