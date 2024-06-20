from owlready2 import *
import json

# Load or create the ontology
onto = get_ontology("http://www.example.org/cassacadiseases.owl")

with onto:
    # Dataset
    class Dataset(Thing):
        label = ["Dataset"]
        comment = ["A collection of associated data."]

    class has_creation_date(DatatypeProperty):
        domain = [Dataset]
        range = [str]
        
    class has_url(DatatypeProperty):
        domain = [Dataset]
        range = [str]
        
    class has_size(DatatypeProperty):
        domain = [Dataset]
        range = [float]
        
    class has_author(DatatypeProperty):
        domain = [Dataset]
        range = [str]

    # Classe
    class Classe(Dataset):
        label = "Classe"
        comment = "Classe representing images."
    
    class has_name(DatatypeProperty):
        domain = [Classe]
        range = [str]

    # Image
    class Image(Classe):
        label = "Image"
        comment = "Image representing images."
        
    class has_size(DatatypeProperty):
        domain = [Image]
        range = [float]

    class has_creation_date(DatatypeProperty):
        domain = [Dataset]
        range = [str]

    #### Contour ####
    class Contour(Image):
        label = ["Contour"]
        comment = ["The contour characteristics of an image, such as area, perimeter, etc."]
        
    class has_area(DatatypeProperty):
        domain = [Contour]
        range = [float]
        
    class has_perimeter(DatatypeProperty):
        domain = [Contour]
        range = [float]

    class has_width(DatatypeProperty):
        domain = [Contour]
        range = [float]

    class has_height(DatatypeProperty):
        domain = [Contour]
        range = [float]

    class has_normalized_area(DatatypeProperty):
        domain = [Contour]
        range = [float]

    class has_normalized_perimeter(DatatypeProperty):
        domain = [Contour]
        range = [float]

    class has_aspect_ratio(DatatypeProperty):
        domain = [Contour]
        range = [float]

    #### Color ####
    class Color(Image):
        label = ["Color"]
        comment = ["The color characteristics of an image, such as hue, saturation, and value."]

    class has_hue_mean(DatatypeProperty):
        domain = [Color]
        range = [float]

    class has_hue_std(DatatypeProperty):
        domain = [Color]
        range = [float]

    class has_saturation_mean(DatatypeProperty):
        domain = [Color]
        range = [float]
        
    class has_saturation_std(DatatypeProperty):
        domain = [Color]
        range = [float]
        
    class has_value_mean(DatatypeProperty):
        domain = [Color]
        range = [float]
        
    class has_value_std(DatatypeProperty):
        domain = [Color]
        range = [float]

    #### Texture ####
    class Texture(Image):
        label = ["Texture"]
        comment = ["The texture characteristics of an image, such as contrast, dissimilarity, etc."]

    class has_contrast(DatatypeProperty):
        domain = [Texture]
        range = [float]
        
    class has_dissimilarity(DatatypeProperty):
        domain = [Texture]
        range = [float]

    class has_energy(DatatypeProperty):
        domain = [Texture]
        range = [float]

    class has_homogeneity(DatatypeProperty):
        domain = [Texture]
        range = [float]

    class has_correlation(DatatypeProperty):
        domain = [Texture]
        range = [float]

# Save the ontology
onto.save(file="mainOntologie.owl")