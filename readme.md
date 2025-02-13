**create `venv`**
```
python -m venv venv

venv\Scripts\activate.bat
```
**Choose the Python interpreter**
- Press `Ctrl + Shift + P` to open the command palette.
- Search for "`Python: Select Interpreter`".
- Choose the Python interpreter inside `venv`.

**Install dependencies**
```
pip install streamlit pillow

pip install torch torchvision numpy opencv-python pillow

pip install fastapi uvicorn

pip install python-multipart

pip install timm
```
**To run the fast api**
```
uvicorn backend.main:app --reload
```
**To run the streamlit**
```
streamlit run frontend/app.py
```


