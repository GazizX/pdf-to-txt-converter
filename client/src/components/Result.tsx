import iconPath from "../assets/download.png"
const Result = ({blob, onReset}: {blob: Blob | null, onReset: React.MouseEventHandler<HTMLButtonElement> | undefined }) => {
    const downloadFile = () => {
        if (blob != null) {
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "converted.txt";
            link.click();
            URL.revokeObjectURL(url);
        }
    };
    return (
        <>
            <div className="container">
                <h1 className="title">PDF to TXT Converter</h1>
                <p className="regularText">Your .txt file is ready! Thanks for choosing our service!</p>
                <button
                    onClick={downloadFile}
                    className="downloadBtn"
                >
                    <p>Download</p>
                    <img src={iconPath} alt="Download" width={60}/>
                </button>
                <button
                    onClick={onReset}
                    className="anotherBtn"
                >
                Convert another PDF file
                </button>
            </div>
        </>
    )
}

export default Result;