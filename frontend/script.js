document.getElementById("buildBtn").addEventListener("click", async () => {
  const idea = document.getElementById("ideaInput").value;
  document.getElementById("generatedCode").textContent = "⏳ Generating...";

  const response = await fetch("/build", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea })
  });

  const data = await response.json();
  document.getElementById("generatedCode").textContent = data.code || "# No code generated.";
  Prism.highlightAll();
});

// Copy to Clipboard
document.getElementById("copyBtn").addEventListener("click", () => {
  const code = document.getElementById("generatedCode").innerText;
  navigator.clipboard.writeText(code).then(() => {
    alert("✅ Code copied to clipboard!");
  });
});

// Download as ZIP
document.getElementById("downloadBtn").addEventListener("click", () => {
  const code = document.getElementById("generatedCode").innerText;
  const zip = new JSZip();
  zip.file("tool.py", code);
  zip.generateAsync({ type: "blob" }).then(content => {
    saveAs(content, "tool.zip");
  });
});
