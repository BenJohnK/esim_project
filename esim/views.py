from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST
import json
from .models import User, Plan, UserPlanMapping
from django.db import IntegrityError, transaction


@csrf_exempt
@require_POST
def activate_esim(request: HttpRequest):
    """
    A Django function-based view that only accepts POST requests.
    """
    try:
        # Check if the content type is JSON and parse the body
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            # Otherwise assume form data (handled automatically by request.POST)
            data = request.POST

        # Access arguments (keys) from the parsed data
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        request_id = data.get('request_id')

        if UserPlanMapping.objects.filter(request_id=request_id).exists():
            return JsonResponse(
                {'error': f'Request {request_id} has already been processed.'}, 
                status=409
            )

        if UserPlanMapping.objects.filter(plan_id=plan_id).exists():
            return JsonResponse(
                {'error': f'Plan {plan_id} is already assigned to a user and cannot be reused.'}, 
                status=400
            )
        
        try:
            with transaction.atomic():
                # Fetch related objects first
                user = User.objects.get(user_id=user_id)
                plan = Plan.objects.get(id=plan_id)

                already_has_plan_in_country = UserPlanMapping.objects.filter(
                    user=user, 
                    plan__country=plan.country
                ).exists()

                if already_has_plan_in_country:
                    return JsonResponse({
                        'error': f'User already has an active plan in {plan.country}.'
                    }, status=400)

                if plan.status == "INACTIVE":
                    return JsonResponse({"message": "Plan is not active"})

                # Attempt to create the mapping
                mapping = UserPlanMapping.objects.create(
                    user=user,
                    plan=plan,
                    request_id=request_id
                )

                # Try calling the external API partner service (preferrably a celery task) to activate the sim for the user. with 3 retries with backoff timings using a try except block. If failed, use logger to log the reason.

                
            return JsonResponse({'message': 'eSIM activated successfully', 'id': mapping.id}, status=201)

        except IntegrityError:
            # This triggers if request_id already exists
            return JsonResponse({'error': f'Request ID {request_id} has already been processed.'}, status=409)
        

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)