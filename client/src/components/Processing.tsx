import gifPath from "../assets/witch.gif"

const Processing = () => {
    return (
        <div className="container">
            <h1 className="title">PDF to TXT Converter</h1>
            <img src={gifPath} alt="Loading..." />
            <p className="regularText">Some magic...</p>
        </div>
    )
}

export default Processing