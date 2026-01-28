export async function uploadFiles(files, testTypes) {
  const formData = new FormData();

  for (let file of files) {
    formData.append("file", file);
  }
  
  formData.append("test_types", JSON.stringify(testTypes));

  const response = await fetch("http://localhost:5000/upload", {
    method: "POST",
    body: formData
  });

  return response.json();
}
