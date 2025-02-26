import requests
import os
import hashlib

class GLTF_Send_HTTP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "glb_file": ("STRING", {"default": "./model.glb"}),  # Path to the GLB file
                "url": ("STRING", {"default": "https://your-backend.com/upload"}),  # Backend URL
                "method_type": (["post", "put"], {"default": "post"})  # No PATCH for binary data
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")  # status_code, response_text, debug_file_path, debug_info
    RETURN_NAMES = ("status_code", "result_text", "debug_file_path", "debug_info")
    FUNCTION = "send_glb_file"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_glb_file(self, glb_file, url, method_type="post"):
        """
        Sends the GLB file as raw binary data.
        """
        if not os.path.exists(glb_file):
            error_text = f"File not found: {glb_file}"
            print(error_text)
            return (0, error_text, glb_file, error_text)

        try:
            with open(glb_file, "rb") as f:
                file_content = f.read()
        except Exception as e:
            error_text = f"Failed to open GLB file at {glb_file}: {str(e)}"
            print(error_text)
            return (0, error_text, glb_file, error_text)

        file_size = len(file_content)
        file_hash = hashlib.sha256(file_content).hexdigest()

        headers = {
            "Content-Type": "application/octet-stream",  # Binary data type
            "X-File-Name": os.path.basename(glb_file)  # Send filename as a header
        }

        try:
            response = requests.request(
                method=method_type.upper(),
                url=url,
                headers=headers,
                data=file_content  # Sending raw binary data
            )
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text, glb_file, f"File size: {file_size} bytes, SHA256: {file_hash}")

        print(f"[GLTF_Send_HTTP] File sent: HTTP {response.status_code}")
        return (response.status_code, response.text, glb_file, f"File size: {file_size} bytes, SHA256: {file_hash}")


NODE_CLASS_MAPPINGS = {
    "GLTF_Send_HTTP": GLTF_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLTF_Send_HTTP": "GLTF Send HTTP Node"
}
