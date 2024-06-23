import os
import shutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from win32com import client

app = FastAPI()

class Paths(BaseModel):
    input_folder: str
    output_folder: str

# Hàm chuyển đổi file DOC, DOCX sang PDF
def convert_doc_to_pdf(doc_path, pdf_path):
    try:
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close()
        word.Quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert")
def convert_files(paths: Paths):
    input_folder = paths.input_folder
    output_folder = paths.output_folder

    if not os.path.exists(input_folder):
        raise HTTPException(status_code=400, detail="Input folder does not exist.")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        file_base, file_ext = os.path.splitext(filename)

        if file_ext.lower() in ['.doc', '.docx']:
            pdf_output_path = os.path.join(output_folder, file_base + '.pdf')
            convert_doc_to_pdf(file_path, pdf_output_path)
        elif file_ext.lower() == '.pdf':
            shutil.copy(file_path, output_folder)
        else:
            continue

    return {"message": "Conversion and copying process completed successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ToPDF:app", host="localhost", port=8091, reload=True)
