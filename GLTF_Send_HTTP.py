import requests
from aiohttp import web
from server import PromptServer

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
        """
        Reads the GLB file from the given file path and sends it as an HTTP request
        to an external backend.
        """
        try:
            # Open the file in binary mode
            with open(glb_file, "rb") as f:
                file_content = f.read()
        except Exception as e:
            error_text = f"Failed to open GLB file at {glb_file}: {str(e)}"
            print(error_text)
            return (0, error_text)

        # Use the file name from the provided path
        filename = glb_file.split("/")[-1]

        # Prepare the file for sending (MIME type for GLB files is "model/gltf-binary")
        files = {
            request_field_name: (filename, file_content, "application/octet-stream")
        }
        try:
            response = requests.request(method=method_type.upper(), url=url, headers=additional_request_headers, files=files)
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text)

        if response.status_code != 200:
            print(f"Failed to send file: HTTP {response.status_code}")
        return (response.status_code, response.text)


# Register the node with a unique name and display title.
NODE_CLASS_MAPPINGS = {
    "GLTF_Send_HTTP": GLTF_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLTF_Send_HTTP": "GLTF Send HTTP Node"
}
