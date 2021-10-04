from face_recognition import face_encodings, compare_faces
from .image import base64_to_image

def get_face_similarity(face, id_card_face):
    face = base64_to_image(face)
    id_card_face = base64_to_image(id_card_face)

    face = face_encodings(face)
    id_card_face = face_encodings(id_card_face)[0]

    return compare_faces(face, id_card_face, 0.45)[0]