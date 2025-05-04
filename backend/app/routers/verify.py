from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.models.user import User
from app.core.security import get_current_user
from app.services.ocr_service import extract_text_from_file_bytes
from app.services.document_analyzer import validate_document_text
from app.services.s3service import upload_to_s3, delete_from_s3
from app.services.rekognition_service import compare_faces_from_s3
from app.services.score_service import add_score
import io
from PIL import Image

router = APIRouter()

def compress_image(image_bytes: bytes, max_size_kb=1000) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))

    # Conversão para JPEG, mesmo se for PNG
    with io.BytesIO() as output:
        img.save(output, format="JPEG", optimize=True, quality=85)
        compressed_data = output.getvalue()

        # Recursivamente reduzir qualidade se necessário
        quality = 80
        while len(compressed_data) > max_size_kb * 1024 and quality > 10:
            output.seek(0)
            output.truncate(0)
            img.save(output, format="JPEG", optimize=True, quality=quality)
            compressed_data = output.getvalue()
            quality -= 10

        return compressed_data


@router.post("/check")
async def verify_user(document: UploadFile = File(...), selfie: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        doc_bytes = await document.read()
        selfie_bytes = await selfie.read()

        # 1. Upload das imagens para S3
        doc_key = upload_to_s3(doc_bytes, document.filename, "documents")
        selfie_key = upload_to_s3(selfie_bytes, selfie.filename, "selfies")
        
        compressed_doc_bytes = compress_image(doc_bytes)
        # 2. OCR + validação documento
        text = await extract_text_from_file_bytes(compressed_doc_bytes, document.filename)
        doc_type = validate_document_text(text, current_user.cpf)

        # 3. Comparação facial com Rekognition
        similarity = compare_faces_from_s3(doc_key, selfie_key)

        if similarity < 80:
            raise HTTPException(400, "Reconhecimento facial falhou")

        # 4. Atualizar usuário
        current_user.is_verified = True

        await add_score(current_user, 200)

        current_user.document_type = doc_type
        await current_user.save()

        return {
            "status": "Conta verificada com sucesso",
            "tipo_documento": doc_type,
            "similaridade": f"{similarity:.2f}%",
            "score_atual": current_user.score
        }

    finally:
        try:
            if 'doc_key' in locals():
                delete_from_s3(doc_key)
            if 'selfie_key' in locals():
                delete_from_s3(selfie_key)
        except Exception as e:
            print(f"Erro ao deletar do S3: {e}")
