from face_recognition import face_encodings, compare_faces

def get_face_similarity(face, id_card_face):
    h, w, _ = face.shape
    face = face_encodings(face, [(0, w, h, 0)])[0]
    h, w, _ = id_card_face.shape
    id_card_face = face_encodings(id_card_face, [(0, w, h, 0)])[0]

    return compare_faces([face], id_card_face, 0.45)[0]