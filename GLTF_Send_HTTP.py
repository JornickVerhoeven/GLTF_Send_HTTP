import requests
from aiohttp import web
from server import PromptServer
import os

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

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("status_code", "result_text")
    FUNCTION = "send_glb_file"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_glb_file(self, glb_file, url, method_type="post", request_field_name="file", additional_request_headers=None):
        # Debug: show the file path being read
        print(f"[GLTF_Send_HTTP] Attempting to read file from: {glb_file}")
        
        if not os.path.exists(glb_file):
            error_text = f"File not found: {glb_file}"
            print(error_text)
            return (0, error_text)
        
        try:
            with open(glb_file, "rb") as f:
                file_content = f.read()
        except Exception as e:
            error_text = f"Failed to open GLB file at {glb_file}: {str(e)}"
            print(error_text)
            return (0, error_text)

        file_size = len(file_content)
        print(f"[GLTF_Send_HTTP] Successfully read {file_size} bytes.")

        # Use os.path.basename to extract the filename reliably.
        filename = os.path.basename(glb_file)
        # If the filename doesn't end with .glb, append it.
        if not filename.lower().endswith(".glb"):
            print(f"[GLTF_Send_HTTP] Filename '{filename}' does not end with '.glb'; appending extension.")
            filename += ".glb"
        print(f"[GLTF_Send_HTTP] Using filename: {filename}")

        # Prepare the file for sending with the appropriate MIME type.
        # "model/gltf-binary" is recommended for GLB files.
        files = {
            request_field_name: (filename, file_content, "model/gltf-binary")
        }

        try:
            response = requests.request(method=method_type.upper(), url=url, headers=additional_request_headers, files=files)
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text)

        if response.status_code != 200:
            print(f"[GLTF_Send_HTTP] Failed to send file: HTTP {response.status_code}: {response.text}")
        else:
            print(f"[GLTF_Send_HTTP] File sent successfully: HTTP {response.status_code}")
        return (response.status_code, response.text)

# Register the node with a unique name and display title.
NODE_CLASS_MAPPINGS = {
    "GLTF_Send_HTTP": GLTF_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLTF_Send_HTTP": "GLTF Send HTTP Node"
}
