export async function uploadFiles(files) {
  const formData = new FormData();

  for (let file of files) {
    formData.append("file", file);
  }

  const response = await fetch("http://localhost:5000/upload", {
    method: "POST",
    body: formData
  });

  return response.json();
}
