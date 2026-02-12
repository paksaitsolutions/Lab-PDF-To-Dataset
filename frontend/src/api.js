const ENV_API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim();

export const API_BASE_URL = ENV_API_BASE_URL || (import.meta.env.DEV ? "http://localhost:5000" : "");

function buildUrl(path) {
  if (!API_BASE_URL) return path;
  return `${API_BASE_URL}${path}`;
}

export function getDownloadUrl(filename) {
  return buildUrl(`/download/${encodeURIComponent(filename)}`);
}

export async function uploadFiles(files, testTypes) {
  const formData = new FormData();

  for (const file of files) {
    formData.append("file", file);
  }

  formData.append("test_types", JSON.stringify(testTypes));

  const response = await fetch(buildUrl('/upload'), {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload?.error || 'Upload request failed');
  }

  return payload;
}
