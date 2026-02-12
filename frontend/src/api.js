const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export async function uploadFiles(files, testTypes) {
  const formData = new FormData();

  for (const file of files) {
    formData.append("file", file);
  }

  formData.append("test_types", JSON.stringify(testTypes));

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload?.error || 'Upload request failed');
  }

  return payload;
}
