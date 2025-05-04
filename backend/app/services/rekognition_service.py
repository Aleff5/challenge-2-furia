import boto3
import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)

def compare_faces_from_s3(doc_key: str, selfie_key: str) -> float:
    """Compara imagens do S3 com Rekognition e retorna similaridade"""
    response = rekognition.compare_faces(
        SourceImage={"S3Object": {"Bucket": S3_BUCKET, "Name": doc_key}},
        TargetImage={"S3Object": {"Bucket": S3_BUCKET, "Name": selfie_key}},
        SimilarityThreshold=70
    )

    if not response["FaceMatches"]:
        return 0.0

    return response["FaceMatches"][0]["Similarity"]
