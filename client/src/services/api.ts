export async function uploadPDF(file:any) {
    const formData = new FormData();
    formData.append("pdfFile", file);

    const response = await fetch ("http://localhost:8080/convert", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error ("Upload failed");
    }

    return await response.blob()
}