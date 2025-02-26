import requests
import os
import hashlib

class GLTF_Send_HTTP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "glb_file": ("STRING", {"default": "./model.glb"}),
                "url": ("STRING", {"default": "https://your-backend.com/upload"}),
                "method_type": (["post", "put", "patch"], {"default": "post"}),
            },
            "optional": {
                "additional_request_headers": ("DICT",)
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("status_code", "result_text", "debug_file_path", "debug_info")
    FUNCTION = "send_glb_file"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_glb_file(self, glb_file, url, method_type="post", additional_request_headers=None):
        # Debug: Verify file exists
        if not os.path.exists(glb_file):
            error_text = f"File not found: {glb_file}"
            print(error_text)
            return (0, error_text, glb_file, error_text)
        
        try:
            with open(glb_file, "rb") as f:
                file_content = f.read()
        except Exception as e:
            error_text = f"Failed to open GLB file: {str(e)}"
            print(error_text)
            return (0, error_text, glb_file, error_text)

        file_size = len(file_content)
        file_hash = hashlib.sha256(file_content).hexdigest()
        filename = os.path.basename(glb_file)

        # Debug info
        debug_info = f"Size: {file_size} bytes, SHA256: {file_hash}, Path: {os.path.abspath(glb_file)}"
        print(f"[GLTF_Send_HTTP] Sending {filename} ({file_size} bytes)")

        # --- 🔥 FIX: Send Raw Binary Instead of Multipart Form ---
        headers = {
            "Content-Type": "application/octet-stream"
        }

        # Merge additional headers (if any)
        if additional_request_headers:
            headers.update(additional_request_headers)

        try:
            response = requests.request(
                method=method_type.upper(),
                url=url,
                headers=headers,
                data=file_content  # 🔥 Send as raw binary instead of form-data
            )
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text, glb_file, debug_info)

        if response.status_code != 200:
            print(f"[GLTF_Send_HTTP] ❌ Upload failed: {response.status_code} - {response.text}")
        else:
            print(f"[GLTF_Send_HTTP] ✅ Upload success: {response.status_code}")

        return (response.status_code, response.text, glb_file, debug_info)


# Register the node with a unique name and display title.
NODE_CLASS_MAPPINGS = {
    "GLTF_Send_HTTP": GLTF_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLTF_Send_HTTP": "GLTF Send HTTP Node"
}
