import cv2
import numpy as np
import json
from skimage.feature import graycomatrix, graycoprops

######################## Les contour ########################
def calculer_caracteristiques_contour(image_path):
    # Charger l'image en niveaux de gris
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Appliquer un seuillage pour obtenir une image binaire
    _, thresh = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    
    # Trouver les contours dans l'image seuillée
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Si aucun contour n'est trouvé, retourner None
    if len(contours) == 0:
        return None
    
    # Sélectionner le contour le plus grand (assumant qu'il s'agit du contour de l'objet principal)
    contour = max(contours, key=cv2.contourArea)
    
    # Calculer les caractéristiques de contour
    surface_contour = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    x, y, width, height = cv2.boundingRect(contour)
    surface_normalisée = surface_contour / (image_gray.shape[0] * image_gray.shape[1])
    perimeter_normalisé = perimeter / (2 * (image_gray.shape[0] + image_gray.shape[1]))
    rapport_aspect = width / height
    
    # Mettre en forme les résultats
    caracteristiques_contour = {
        'surface': surface_contour,
        'perimetre': perimeter,
        'largeur': width,
        'hauteur': height,
        'surface_normalisee': surface_normalisée,
        'perimetre_normalise': perimeter_normalisé,
        'rapport_aspect': rapport_aspect
    }
    
    return caracteristiques_contour

# Exemple d'utilisation
image_path = 'images/1.jpg'
resultats_contour = calculer_caracteristiques_contour(image_path)
if resultats_contour:
    print("Caractéristiques de contour :")
    print(json.dumps(resultats_contour, indent=4))
else:
    print("Aucun contour trouvé dans l'image.")
