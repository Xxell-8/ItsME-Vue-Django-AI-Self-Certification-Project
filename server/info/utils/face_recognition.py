from face_recognition import face_encodings, compare_faces

def get_face_similarity(face, id_card_face):
    face = face_encodings(face)
    id_card_face = face_encodings(id_card_face)[0]

    return compare_faces(face, id_card_face, 0.45)[0]