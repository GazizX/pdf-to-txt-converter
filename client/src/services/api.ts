export async function uploadPDF(file: File): Promise<[Blob, string]> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8080/convert", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Upload failed");
    }

    const contentDisposition = response.headers.get("Content-Disposition");
    let fileName = "convertedFile";

    if (contentDisposition) {
        const utf8Match = contentDisposition.match(/filename\*=UTF-8''(.+?)(?:;|$)/i);
        const plainMatch = contentDisposition.match(/filename="(.+?)"/i);
        
        if (utf8Match && utf8Match[1]) {
            fileName = decodeURIComponent(utf8Match[1]);
        } else if (plainMatch && plainMatch[1]) {
            fileName = plainMatch[1];
        }
    }

    const blob = await response.blob();
    
    return [blob, fileName];
}
