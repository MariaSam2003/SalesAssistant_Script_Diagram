import subprocess
import tempfile
from PIL import Image
import io
import os

def generate_flowchart_image(diagram_dot_code: str, format: str = "png") -> io.BytesIO:
    assert format in ["png", "svg", "pdf"], "Unsupported format"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as dotfile:
        dotfile.write(diagram_dot_code.encode("utf-8"))
        dot_path = dotfile.name

    output_path = dot_path.replace(".dot", f".{format}")

    try:
        subprocess.run(["dot", f"-T{format}", dot_path, "-o", output_path], check=True)
        if format == "png":
            img = Image.open(output_path)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
        else:
            # For svg or pdf just read the file bytes
            buf = io.BytesIO(open(output_path, "rb").read())
        buf.seek(0)
        return buf

    finally:
        os.remove(dot_path)
        if os.path.exists(output_path):
            os.remove(output_path)
