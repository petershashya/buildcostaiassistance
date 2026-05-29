from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from HouseCostApp.models import House,CustomUser,HouseCost
from .controllers.login import login_view
from .controllers.register import register_view
from .controllers.user import history_view,predict,prediction,historyview
from django.contrib.auth import logout
from .controllers.admin import admin_page,admin_report,admin_users
from django.contrib import messages
from django.contrib.auth import get_user_model


#for new housemodal links
import os
from PIL import Image

import google.generativeai as genai
# import google as genai

from .forms import HouseMapForm
from .models import HouseMap
import json
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def house_list(request):
 
    houses = House.objects.select_related('user').all() 
    return render(request, 'admin_history.html', {'houses': houses})

def admin_history(request):
    return render(request, 'admin_history.html')

def loader_view(request):
    return render(request, 'layouts/loader.html')



User = get_user_model()

# deleting function

def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('admin-users')  # Redirect to a relevant page after deletion
    else:
        # Handle GET request or other methods as needed
        pass
# Create your views here.




# Old Gemini API KEY attach method
# API_KEY = "AIzaSyB-TW9G7FfZf8kWMjUDDUFu8wQMSGEMlKg"
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# New Gemini API KEY attach method
# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )
# model = client.models


@login_required
def scan_house_map(request):
    result = None
    image_url = None
    image_id = None
    if request.method == 'POST':

        form = HouseMapForm(request.POST, request.FILES)
        if form.is_valid():

            # ✅ SAVE WITHOUT COMMIT FIRST
            house_map = form.save(commit=False)
            house_map.user = request.user
            house_map.save()   # ✔ correct save

            # image path
            image_path = house_map.map_image.path
            image_url = house_map.map_image.url
            image_id = house_map.id

            img = Image.open(image_path)
            # Prompt to Gemini AI
            prompt = """
            Analyze this uploaded image carefully.
            Return ONLY valid JSON.
            Do not return explanation outside JSON.

            STEP 1:
            Check if image is really:
            - house map
            - floor plan
            - blueprint
            - building layout

            If NOT house map return:
            {
                "house_map": false
            }
            If it IS house map return structured JSON like this:
            {
                "house_map": true,
                "total_rooms": 0,
                "total_bedrooms": 0,
                "total_bathrooms": 0,
                "total_kitchens": 0,
                "total_corridors": 0,
                "total_doors": 0,
                "total_windows": 0,
                "total_floors": 1,
                "total_house_square_meters": 0,
                "total_house_volume_m3": 0,
                "roof_structure_visible": false,
                "garage_detection": false,
                "stair_detection": false,
                "balcony_detection": false,
                "rooms_details": [
                    {
                        "room_name": "",
                        "estimated_width_ft": 0,
                        "estimated_length_ft": 0,
                        "area_sq_ft": 0,
                        "area_sq_meters": 0,
                        "estimated_volume_m3": 0
                    }
                ]
            }

            IMPORTANT:
            1. Detect EVERY room separately.
            2. Calculate estimated width and length for each room.
            3. Calculate area in square feet.
            4. Calculate area in square meters.
            5. Calculate estimated room volume in cubic meters.
            6. Include all rooms inside rooms_details array.
            7. Return ONLY clean JSON.
            """

            # Send image + prompt to Gemini
            response = model.generate_content(model = "gemini-3-flash-preview", contents= [prompt, img])

            raw_result = response.text

            # clean JSON
            raw_result = raw_result.replace("```json", "").replace("```", "").strip()

            try:
                result_data = json.loads(raw_result)

                if result_data.get("house_map") == True:

                    # ✅ SAVE JSON STRING TO DB
                    house_map.result = json.dumps(result_data)
                    house_map.save()

                    # ✅ SEND DICT TO TEMPLATE
                    result = result_data

                else:

                    result = {
                        "error": "This image is not recognized as house map."
                    }

            except Exception as e:

                print("JSON ERROR:", e)

                result = {
                    "error": "Invalid AI response",
                    "raw": raw_result
                }

    else:
        form = HouseMapForm()

    return render(request, 'scan_map.html', {
        'form': form,
        'result': result,
        'image_url': image_url,
        'image_id':image_id
    })


@login_required
def predict_house_cost(request):
    if request.method == "POST":
        quality_of_construction = request.POST['qualityOfConstruction']
        type_of_structure = request.POST['typeOfStructure']
        door_material = request.POST['doorMaterials']
        window_material = request.POST['windowMaterials']
        construction_material = request.POST['constructionMaterials']
        location_of_house = request.POST['locationOfHouse']
        location_nature = request.POST['locationnature']
        construction_period = int(request.POST['constructionPeriod'])

        if construction_period < 14:
            messages.error(
                request,
                "Construction period cannot be less than 14 days"
            )
            return render(request, 'scan_map.html')

        # GET LATEST HOUSEMAP
        latest_house_map = HouseMap.objects.filter(
            user=request.user,
            result__isnull=False
        ).order_by('-date_created').first()

        if not latest_house_map:
            messages.error(request, "No scanned house map found")
            return render(request, 'scan_map.html')

        # CONVERT JSON RESULT
        try:
            map_result = json.loads(latest_house_map.result)
        except Exception:
            messages.error(request, "Invalid house map data")
            return render(request, 'scan_map.html')

        # CHECK HOUSE MAP
        if map_result.get("house_map") != True:
            messages.error(request, "Invalid house map")
            return render(request, 'scan_map.html')

        # GET VALUES
        total_rooms = map_result.get("total_rooms", 0)
        total_bedrooms = map_result.get("total_bedrooms", 0)
        total_bathrooms = map_result.get("total_bathrooms", 0)
        total_kitchens = map_result.get("total_kitchens", 0)
        total_windows = map_result.get("total_windows", 0)
        total_doors = map_result.get("total_doors", 0)
        total_corridors = map_result.get("total_corridors", 0)
        total_floors = map_result.get("total_floors", 0)
        # total_floors = map_result.get("total_floors", 1)
        total_area = map_result.get(
            "total_house_square_meters",
            0
        )

        total_volume = map_result.get(
            "total_house_volume_m3",
            0
        )

        rooms_details = map_result.get(
            "rooms_details",
            []
        )

        # ROOF
        roof_type = "Normal"
        if map_result.get("roof_structure_visible"):
            roof_type = "Visible Roof"

        # GEMINI PROMPT
        prompt = f"""
        You are professional Tanzania construction engineer.

        Analyze this complete house map and predict complete
        construction materials and total house costs in TZS.

        HOUSE MAP ANALYSIS
        
        Total Rooms: {total_rooms}
        Total Bedrooms: {total_bedrooms}
        Total Bathrooms: {total_bathrooms}
        Total Kitchens: {total_kitchens}
        Total Doors: {total_doors}
        Total Windows: {total_windows}
        Total Corridos: {total_corridors}
        Total Floors: {total_floors}
        Roof Type: {roof_type}
        Total Floor Area:
        {total_area} square meters
        Total Volume:
        {total_volume} cubic meters
        ROOM DETAILS:
        {rooms_details}

        USER CONSTRUCTION DETAILS
    
        Quality of Construction:
        {quality_of_construction}
        Type of Structure:
        {type_of_structure}
        Door Material:
        {door_material}
        Window Material:
        {window_material}
        Construction Material:
        {construction_material}
        House Location:
        {location_of_house}
        Location Nature:
        {location_nature}
        Construction Period:
        {construction_period} days

        Return professional construction analysis with:

        1. Total cement blocks
        2. Cement bags
        3. Iron sheets
        4. Woods
        5. Paint buckets
        6. Tiles
        7. Glass windows
        8. Gypsum boards
        9. Sand
        10. Gravel
        11. Labor costs
        12. Electrical costs
        13. Plumbing costs
        14. Total construction cost in Tanzania Shillings (TZS)

        Also include:
        - Estimated foundation costs
        - Roofing costs
        - Finishing costs
        - Interior costs
        - Exterior costs

        Give results in professional documentation format.
        """

        # GEMINI RESPONSE
        response = model.generate_content(prompt)
        result = response.text.strip()

        # CLEAN ONLY (NO JSON PARSING)
        result = result.replace("```json", "").replace("```", "").strip()

        # SAVE AS TEXT (NO JSON CONVERSION)
        ai_result = result

        # CREATE HOUSE COST
        house_cost = HouseCost.objects.create(
            user=request.user,
            house_map=latest_house_map,
            quality_of_construction=quality_of_construction,
            type_of_structure=type_of_structure,
            door_material=door_material,
            window_material=window_material,
            construction_material=construction_material,
            location_of_house=location_of_house,
            location_nature=location_nature,
            construction_period=construction_period,
            numberfloor=total_floors,
            ai_result=ai_result
        )
        
        
        context = {
            "recent_house": house_cost,
            "map_result": map_result,
            "ai_result":  ai_result, 
        }

        return render(
            request,
            "house_cost.html",
            context
        )
    else:
        return render(request, 'house_cost.html', )


#for get house image and ai_result
def get_house_data(request):
    house_id = request.GET.get("id")
    data_type = request.GET.get("type")
    house = HouseCost.objects.get(id=house_id)
    # RETURN IMAGE ONLY
    if data_type == "image":
        return JsonResponse({
            "image_url": house.house_map.map_image.url
        })
    # RETURN AI RESULT ONLY
    elif data_type == "ai":
        return JsonResponse({
            "ai_result": house.ai_result
        })
    # fallback
    return JsonResponse({
        "error": "Invalid request"
    })