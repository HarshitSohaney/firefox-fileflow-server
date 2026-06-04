def upload_page_html(file_id: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Send Photo to Firefox</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            text-align: center;
            max-width: 400px;
            width: 100%;
        }}
        h1 {{
            font-size: 1.4rem;
            margin-bottom: 24px;
            color: #333;
        }}
        .btn {{
            display: inline-block;
            padding: 20px 48px;
            font-size: 1.2rem;
            font-weight: 600;
            background: #0060df;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            min-height: 56px;
            width: 100%;
        }}
        .btn:active {{ background: #003eaa; }}
        label.btn {{ display: flex; justify-content: center; align-items: center; }}
        .status {{
            margin-top: 24px;
            font-size: 1rem;
            color: #666;
        }}
        .status.success {{ color: #058b00; }}
        .status.error {{ color: #d70022; }}
        .progress {{
            margin-top: 16px;
            width: 100%;
            height: 8px;
            border-radius: 4px;
            appearance: none;
        }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Send a photo to Firefox</h1>
        <label class="btn" for="fileInput">
            Tap to select a photo
        </label>
        <input type="file" id="fileInput" accept="image/jpeg" class="hidden">
        <progress id="progressBar" class="progress hidden" value="0" max="100"></progress>
        <div id="status" class="status"></div>
    </div>
    <script>
        const fileInput = document.getElementById("fileInput");
        const selectLabel = document.querySelector("label.btn");
        const progressBar = document.getElementById("progressBar");
        const statusEl = document.getElementById("status");
        const uploadUrl = "/upload/{file_id}";

        fileInput.addEventListener("change", function() {{
            if (!fileInput.files.length) return;
            upload(fileInput.files[0]);
        }});

        function upload(file) {{
            selectLabel.classList.add("hidden");
            progressBar.classList.remove("hidden");
            statusEl.textContent = "Uploading...";
            statusEl.className = "status";

            const xhr = new XMLHttpRequest();
            xhr.open("POST", uploadUrl);

            xhr.upload.onprogress = function(e) {{
                if (e.lengthComputable) {{
                    progressBar.value = (e.loaded / e.total) * 100;
                }}
            }};

            xhr.onload = function() {{
                progressBar.classList.add("hidden");
                if (xhr.status === 200) {{
                    statusEl.textContent = "Photo sent! You can close this page.";
                    statusEl.className = "status success";
                }} else {{
                    showError();
                }}
            }};

            xhr.onerror = function() {{
                progressBar.classList.add("hidden");
                showError();
            }};

            const formData = new FormData();
            formData.append("file", file);
            xhr.send(formData);
        }}

        function showError() {{
            statusEl.innerHTML = 'Upload failed. <button class="btn" onclick="location.reload()">Try again</button>';
            statusEl.className = "status error";
        }}
    </script>
</body>
</html>"""
