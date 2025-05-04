import httpx
import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)



OCR_API_URL = "https://api.ocr.space/parse/image"
OCR_API_KEY = os.getenv("OCR_API_KEY")  


async def extract_text_from_file_bytes(file_bytes: bytes, filename: str) -> str:


    files = {"file": (filename, file_bytes, "image/jpeg")}
    headers = {"apikey": OCR_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.post(OCR_API_URL, files=files, headers=headers)

    if response.status_code != 200:
        raise Exception("Erro na API OCR")

    result = response.json()
    print("OCR result:", result)
    if (
    result.get("IsErroredOnProcessing")
    or not result.get("ParsedResults")
    or not result["ParsedResults"][0].get("ParsedText")
    ):
        raise Exception("Não foi possível extrair texto do OCR")

    return result["ParsedResults"][0]["ParsedText"]



