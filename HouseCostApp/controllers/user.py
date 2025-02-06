from django.shortcuts import render,redirect
from django.contrib import messages
from HouseCostApp.models import House
from .priceModel import check_image,model_calculations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tempfile
from django.core.files.storage import FileSystemStorage
def history_view(request):
    house_list = House.objects.filter(user=request.user)
    paginator = Paginator(house_list,10)  # Show 10 houses per page

    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        houses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        houses = paginator.page(paginator.num_pages)
        
    if request.user.is_authenticated:
        houses = House.objects.filter(user=request.user)
    

    return render(request, 'history.html', {'houses': houses})

def historyview(request):
    houses = House.objects.all()
    return render(request, 'admin_history.html', {'houses': houses})

def predict(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if file:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                print(file_path)

                # Check the uploaded image
                error_message, length_of_words = check_image(file_path)
                # If there's an error message, display it and return
                if error_message:
                    messages.error(request, error_message)
                    return render(request, 'predict.html')

                # If the image passes the check, proceed with calculating the total points
                quality_of_construction = request.POST['qualityOfConstruction']
                type_of_structure = request.POST['typeOfStructure']
                construction_material = request.POST['constructionMaterials']
                location_of_house = request.POST['locationOfHouse']
                location_nature = request.POST['locationnature']
                construction_period = int(request.POST['constructionPeriod'])
               
                numberfloor=1
                
            
                try:
                    numberfloor = request.POST.get('numberfloor', '1')
                except ValueError:
                    messages.error(request, numberfloor)
                    return render(request, 'predict.html')
                
                if (numberfloor==""):
                    numberfloor=1

                if (construction_period < 14):
                    messages.error(request,"Costruction period  cannot be less than 14 days")
                    return render(request,"predict.html")

                # Calculate total points based on user selections and length of words
                total_points = model_calculations(
                    quality_of_construction,
                    type_of_structure,
                    int(numberfloor),  # Assume 1 floor
                    length_of_words * 250,  # Adjusted total area based on length of words
                    construction_material,
                    location_of_house,
                    construction_period,
                    length_of_words,  # Pass the length of words
                    location_nature
                )
                formatted_price = "{:,.0f}/=".format(total_points)

                # Save the house details along with the calculated points
                house = House(
                    user=request.user,
                    file=file,
                    quality_of_construction=quality_of_construction,
                    type_of_structure=type_of_structure,
                    construction_material=construction_material,
                    location_of_house=location_of_house,
                    location_nature=location_nature,
                    numberfloor=numberfloor,
                    construction_period=construction_period,
                    predicted_price=total_points
                )
                house.save()
                recent_house = house
                messages.success(request, 'House details submitted successfully!')
                return render(request, 'prediction.html', {'recent_house': recent_house, 'price': formatted_price})
        except Exception as e:
            messages.error(request, f'Error submitting house details: {e}')
    return render(request, 'predict.html')

def prediction(request):
    last_house = House.objects.filter(user=request.user).last()    
    return render(request, 'prediction.html', {'last_house': last_house})


