import cv2
import numpy as np
import json
from skimage.feature import graycomatrix, graycoprops

######################## La couleur ########################
def calculer_caracteristiques_couleur(image_path):
    # Charger l'image en utilisant OpenCV
    image = cv2.imread(image_path)
    
    # Convertir l'image en espace de couleur HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculer les statistiques de couleur moyenne et d'écart type
    mean, std = cv2.meanStdDev(hsv_image)
    
    # Mettre en forme les résultats
    hue_mean, saturation_mean, value_mean = mean.flatten()
    hue_std, saturation_std, value_std = std.flatten()
    
    caracteristiques_couleur = {
        'hue_mean': hue_mean,
        'hue_std': hue_std,
        'saturation_mean': saturation_mean,
        'saturation_std': saturation_std,
        'value_mean': value_mean,
        'value_std': value_std
    }
    
    return caracteristiques_couleur

# Exemple d'utilisation
image_path = 'images/1.jpg'
resultats = calculer_caracteristiques_couleur(image_path)
print("Caractéristiques de couleur :")
# Imprimer les résultats en format JSON avec indentation
print(json.dumps(resultats, indent=4))
