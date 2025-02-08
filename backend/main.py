from fastapi                import FastAPI, UploadFile, File,Form
from pydantic               import BaseModel
from typing                 import Tuple
from PIL                    import Image
from backend.ModelProcessor import ModelProcessor
from loguru                 import logger
import uvicorn

model_processor = ModelProcessor()                          # Initialize ModelProcessor
app = FastAPI()

class ApplyTextRequest(BaseModel):                          # Define the request body schema using Pydantic for TextOverlay
    text            : str
    text_position   : Tuple[int, int]                       # (x_position, y_position) position of the text
    text_size       : int
    text_color      : Tuple[int, int, int]                  # (r, g, b) font color
    font_name       : str                                   # The font name 

################################################ generate-depth ########################################################
@app.post("/generate-depth/")
async def generate_depth(file : UploadFile = File(...), model_name : str = Form(...)):
    
    """API endpoint to set the model and generate depth for a new image."""
    try:
        image_pil = Image.open(file.file).convert("RGB")    # Load and process the image
        model_processor.set_model(model_name,image_pil)     # Set the model
        model_processor.generate_depth_map()
        model_processor.process_foreground()
        return {"message": f"Model {model_name} set and image processing successfully!"}
    except Exception as e:
        return {"error": str(e)}

################################################# apply-text #########################################################
@app.post("/apply-text/")
async def apply_text(request: ApplyTextRequest):
    
    """API endpoint to apply text on the processed image."""
    logger.info(f"request_body:{request}")
    try:
        processed_image     = model_processor.process_text(
            text            =request.text,
            text_position   =request.text_position,
            text_size       =request.text_size,
            text_color      =request.text_color,
            font_name       =request.font_name
        )
        output_path         = "utils/image/output.png"          # save image to image folder
        processed_image.save(output_path)
        return {"message": "Text applied successfully!", "output_path": output_path}
    except Exception as e:
        logger.error(f"Error in apply_text API: {e}")
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
