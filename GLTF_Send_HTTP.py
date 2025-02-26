import requests
from aiohttp import web
from server import PromptServer
import os
import hashlib

class GLTF_Send_HTTP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # The GLB file is provided as a file path (a string) from another node.
                "glb_file": ("STRING", {"default": "./model.glb"}),
                "url": ("STRING", {"default": "https://your-backend.com/upload"}),
                "method_type": (["post", "put", "patch"], {"default": "post"}),
                "request_field_name": ("STRING", {"default": "file"}),
            },
            "optional": {
                "additional_request_headers": ("DICT",)
            }
        }

    # Now we have 4 outputs: an int (status code), a string (response text), a string (debug_file_path),
    # and a string (debug_info) that we can use for additional debugging.
    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("status_code", "result_text", "debug_file_path", "debug_info")
    FUNCTION = "send_glb_file"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_glb_file(self, glb_file, url, method_type="post",
                      request_field_name="file", additional_request_headers=None):
        # Debug: show the file path being read
        print(f"[GLTF_Send_HTTP] Attempting to read file from: {glb_file}")
        
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
        print(f"[GLTF_Send_HTTP] Successfully read {file_size} bytes.")

        # Calculate SHA256 hash for additional debug info.
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Use os.path.basename to extract the filename reliably.
        filename = os.path.basename(glb_file)
        # If the filename doesn't end with .glb, append it.
        if not filename.lower().endswith(".glb"):
            print(f"[GLTF_Send_HTTP] Filename '{filename}' does not end with '.glb'; appending extension.")
            filename += ".glb"
        print(f"[GLTF_Send_HTTP] Using filename: {filename}")

        # Prepare debug info string
        abs_path = os.path.abspath(glb_file)
        debug_info = f"File size: {file_size} bytes, SHA256: {file_hash}, Absolute path: {abs_path}"

        # Prepare the file for sending with the recommended MIME type.
        files = {
            request_field_name: (filename, file_content, "model/gltf-binary")
        }

        try:
            response = requests.request(method=method_type.upper(), url=url, headers=additional_request_headers, files=files)
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text, glb_file, debug_info)

        if response.status_code != 200:
            print(f"[GLTF_Send_HTTP] Failed to send file: HTTP {response.status_code}: {response.text}")
        else:
            print(f"[GLTF_Send_HTTP] File sent successfully: HTTP {response.status_code}")
        return (response.status_code, response.text, glb_file, debug_info)


# Register the node with a unique name and display title.
NODE_CLASS_MAPPINGS = {
    "GLTF_Send_HTTP": GLTF_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLTF_Send_HTTP": "GLTF Send HTTP Node"
}
