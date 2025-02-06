import nltk
from nltk.corpus import wordnet
from PIL import Image
from django.core.exceptions import ValidationError
import pytesseract
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import easyocr
def check_image(image_path):
    nltk.download('wordnet')
    # Create an EasyOCR reader for English
    reader = easyocr.Reader(['en'])
    
    # Open the image and extract text using EasyOCR
    results = reader.readtext(image_path)
    
    # Extract text from results
    text = " ".join([result[1] for result in results])
    
    # Convert text to lowercase
    text_lower = text.lower()
    print(text_lower)
    
    # Split the text into words
    words_array = text_lower.split()
    
    # Filter out only English words of three characters or longer
    english_words = [word for word in words_array if len(word) >= 3 and wordnet.synsets(word)]
    
    # Check if the word 'room' is in the extracted text
    if 'room' not in text_lower and 'bed' not in text_lower:
        return "The image you uploaded is not a floor plan or its blur or it has low quality", 0

    
    # Print the array of English words of three characters or longer
    print(english_words)
    print(len(english_words))
    
    # Return None if there's no error
    return None, len(english_words)

def model_calculations(quality_of_construction, type_of_structure, number_of_floors, total_area,
                       construction_materials, location_of_house, construction_period, rooms, nature_of_area):
    # Define points for each quality of construction
    quality_points = {
        'Basic': 2500000,
        'Standard': 55000000,
        'Luxury': 910000000,
    }
    # Define points for each type of structure
    structure_points = {
        'Apartment Building': 45000000,
        'Single-family House': 20000000,
    }
    # Define points for each construction material
    material_points = {
        'Brick': 90000,
        'Wood': 70000,
        'Mixer': 60000,
        'Concrete': 80000,
    }
    # Define points for each location
    location_points = {
        'Mbeya': 8000000,
        'Dar': 15000000,
        'Dodoma': 11000000,
        'Mwanza': 7000000,
        'Tabora': 2000000,
        'Lindi': 2000000,
        'Songwe': 1000000,
        'Arusha': 9000000,
        'Morogoro': 6000000,
    }
    
    nature_points ={
        'Urban': 10000000,
        'Rular': 5000000,
    }

 # Print the values used to calculate total points
    print("Quality of Construction Points:", quality_points.get(quality_of_construction, 0))
    print("Type of Structure Points:", structure_points.get(type_of_structure, 0))
    print("Number of Floors Points:", int(number_of_floors) * 1000000)
    print("Total Area Points:", int(total_area) * 10)
    print("Construction Material Points:", material_points.get(construction_materials, 0))
    print("Location Points:", location_points.get(location_of_house, 0))
    print("Number of Rooms Points:", int(rooms) * 1000000)
    print("Construction Period Points:", (int(construction_period)) * -50000)
    print("Nature of Area Points:", nature_points.get(nature_of_area, 0))

 # Print the values used to calculate total points
    print("Quality of Construction Points:", quality_points.get(quality_of_construction, 0))
    print("Type of Structure Points:", structure_points.get(type_of_structure, 0))
    print("Number of Floors Points:", int(number_of_floors) * 10000)
    print("Total Area Points:", int(total_area) * 10)
    print("Construction Material Points:", material_points.get(construction_materials, 0))
    print("Location Points:", location_points.get(location_of_house, 0))
    print("Number of Rooms Points:", int(rooms) * 1000000)
    print("Construction Period Points:", (int(construction_period)) * -50000)
    print("Nature of Area Points:", nature_points.get(nature_of_area, 0))

    # Calculate total points based on user selections and number of rooms
    quality_construction_points = quality_points.get(quality_of_construction, 0)
    print(f"Quality of construction points: {quality_construction_points}")

    structure_type_points = structure_points.get(type_of_structure, 0)
    print(f"Structure type points: {structure_type_points}")

    floor_points = int(number_of_floors) * 1000000
    print(f"Floor points: {floor_points}")

    area_points = int(total_area) * 10
    print(f"Area points: {area_points}")

    material_points_value = material_points.get(construction_materials, 0)
    print(f"Construction materials points: {material_points_value}")

    location_points_value = location_points.get(location_of_house, 0)
    print(f"Location points: {location_points_value}")

    room_points = int(rooms) * 5000000
    print(f"Room points: {room_points}")

    construction_period_points = (int(construction_period)) * -50000
    print(f"Construction period points: {construction_period_points}")

    nature_area_points = nature_points.get(nature_of_area, 0)
    print(f"Nature of area points: {nature_area_points}")

    total_points = (
        quality_points.get(quality_of_construction, 0) +
        structure_points.get(type_of_structure, 0) +
        int(number_of_floors * rooms) * 1000000 +  # Each floor adds 10000000 points
        int(total_area) * 10 +  # Each 10 square meters adds 10 points
        material_points.get(construction_materials, 0) +
        location_points.get(location_of_house, 0) +
        
        (int(construction_period)) * -50000  + # Each year subtracted from 2024 adds -50000 points
        nature_points.get(nature_of_area, 0)
    )

    return total_points
