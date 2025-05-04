import re
from fastapi import HTTPException

def validate_document_text(parsed_text: str, user_cpf: str) -> None:
    """
    Lê o texto extraído do OCR e:
    - Valida se contém um CPF
    - Valida se esse CPF bate com o do usuário
    - Opcional: detecta termos suspeitos
    """
    # Regex CPF
    match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", parsed_text)
    if not match:
        raise HTTPException(status_code=400, detail="CPF não detectado no documento")

    cpf_in_doc = match.group().replace(".", "").replace("-", "")
    cpf_from_user = user_cpf.replace(".", "").replace("-", "")

    if cpf_in_doc != cpf_from_user:
        raise HTTPException(status_code=400, detail="CPF no documento não confere com o CPF cadastrado")

    # Detecta indícios de fraude leve (simulado)
    if any(keyword in parsed_text.lower() for keyword in ["print", "tela", "screenshot"]):
        raise HTTPException(status_code=400, detail="Documento parece ser uma captura de tela")
