import cv2
import numpy as np
import json
from skimage.feature import graycomatrix, graycoprops
from owlready2 import *

# Charger l'ontologie
onto = get_ontology("mainOntologie.owl").load()

# Fonctions pour calculer les caractéristiques

######################## Les contours ########################
def calculer_caracteristiques_contour(image_path):
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None
    
    contour = max(contours, key=cv2.contourArea)
    surface_contour = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    x, y, width, height = cv2.boundingRect(contour)
    surface_normalisée = surface_contour / (image_gray.shape[0] * image_gray.shape[1])
    perimeter_normalisé = perimeter / (2 * (image_gray.shape[0] + image_gray.shape[1]))
    rapport_aspect = width / height
    
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

######################## La couleur ########################
def calculer_caracteristiques_couleur(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean, std = cv2.meanStdDev(hsv_image)
    hue_mean, saturation_mean, value_mean = mean.flatten()
    hue_std, saturation_std, value_std = std.flatten()
    
    caracteristiques_couleur = {
        'hue_mean': float(hue_mean),
        'hue_std': float(hue_std),
        'saturation_mean': float(saturation_mean),
        'saturation_std': float(saturation_std),
        'value_mean': float(value_mean),
        'value_std': float(value_std)
    }
    
    return caracteristiques_couleur

######################## La texture ########################
def calculer_caracteristiques_texture(image_path):
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(image_gray, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    
    caracteristiques_texture = {
        'contraste': float(contrast),
        'dissimilarite': float(dissimilarity),
        'energie': float(energy),
        'homogeneite': float(homogeneity),
        'correlation': float(correlation)
    }
    
    return caracteristiques_texture

######################## Annotation ########################
def annotate_image(image_path, label, description):
    # Calculer les caractéristiques
    contour_props = calculer_caracteristiques_contour(image_path)
    color_props = calculer_caracteristiques_couleur(image_path)
    texture_props = calculer_caracteristiques_texture(image_path)
    
    # Créer une instance de l'image
    image_name = image_path.split('/')[-1]
    image_instance = onto.Image(image_name)
    image_instance.label.append(label)
    image_instance.comment.append(description)
    
    # Annoter les propriétés de contour
    if contour_props:
        image_instance.has_area.append(contour_props['surface'])
        image_instance.has_perimeter.append(contour_props['perimetre'])
        image_instance.has_width.append(contour_props['largeur'])
        image_instance.has_height.append(contour_props['hauteur'])
        image_instance.has_normalized_area.append(contour_props['surface_normalisee'])
        image_instance.has_normalized_perimeter.append(contour_props['perimetre_normalise'])
        image_instance.has_aspect_ratio.append(contour_props['rapport_aspect'])
    
    # Annoter les propriétés de couleur
    if color_props:
        image_instance.has_hue_mean.append(color_props['hue_mean'])
        image_instance.has_hue_std.append(color_props['hue_std'])
        image_instance.has_saturation_mean.append(color_props['saturation_mean'])
        image_instance.has_saturation_std.append(color_props['saturation_std'])
        image_instance.has_value_mean.append(color_props['value_mean'])
        image_instance.has_value_std.append(color_props['value_std'])
    
    # Annoter les propriétés de texture
    if texture_props:
        image_instance.has_contrast.append(texture_props['contraste'])
        image_instance.has_dissimilarity.append(texture_props['dissimilarite'])
        image_instance.has_energy.append(texture_props['energie'])
        image_instance.has_homogeneity.append(texture_props['homogeneite'])
        image_instance.has_correlation.append(texture_props['correlation'])
    
    print(f"Image '{image_name}' annotée avec succès.")

# Sauvegarder l'ontologie après avoir annoté l'image
def save_ontology():
    onto.save(file="mainOntologie_OK.owl")
    print("Ontologie sauvegardée avec succès.")

# Exemple d'utilisation
image_path = 'images/1.jpg'
label = "Example Image 1"
description = "This is an example image used for testing annotations."
annotate_image(image_path, label, description)
save_ontology()
