from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import base64 
import os
from google import genai
from google.genai import types
from django.conf import settings

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.email.endswith('@uap-bd.edu'):
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Only Students with UAP Mail can login.')
                return redirect('login')  
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')  
    return render(request, 'login.html')




# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')  

        if not email.endswith('@uap-bd.edu'):
            messages.error(request, 'Only Students with UAP Mail can register.')
            return redirect('register')  

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  
        except ValidationError as e:
            messages.error(request, f'Error: {e.message}')
            return redirect('register') 
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            return redirect('register')  

    return render(request, 'register.html')

# Configure Gemini API
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Authority login view
def authority_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                authority = Authority.objects.get(user=user)
                auth_login(request, user)  
                return redirect("authority_dashboard")
            except Authority.DoesNotExist:
                messages.error(request, "You are not registered as an authority.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "authority_login.html")


# Authority logout view
@login_required(login_url='authority_login')
def authority_logout(request):
    auth_logout(request)
    return redirect("login")

# Home view
@login_required(login_url='login')
def home(request):
    complaints = Complaint.objects.all().order_by("-created_at")

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        action = request.POST.get("action")

        complaint = get_object_or_404(Complaint, id=complaint_id)

        if action == "upvote":
            complaint.total_upvotes += 1
            messages.success(request, "You upvoted the complaint.")
        elif action == "downvote":
            complaint.total_downvotes += 1
            messages.warning(request, "You downvoted the complaint.")

        complaint.total_views += 1 
        complaint.save()

        return redirect("home")

    return render(request, "home.html", {"complaints": complaints, 'page_name': 'dashboard'})



# Post complaint view
@login_required(login_url='login')
def post_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        department = request.POST.get("department")
        is_anonymous = request.POST.get("is_anonymous") == "on"
        image = request.FILES.get("image")

        complaint = Complaint(
            user=request.user,
            title=title,
            description=description,
            department=department,
            is_anonymous=is_anonymous,
            image=image
        )
        complaint.save()
        messages.success(request, "Your complaint has been submitted successfully.")
        return redirect("home")

    return render(request, "post_complaint.html",{'page_name': 'new_complaint'} )


@login_required(login_url='login')
def complaint_responses_and_feedback(request):
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by("-created_at")

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        rating = int(request.POST.get("rating", 0))
        comments = request.POST.get("comments", "")

        complaint = get_object_or_404(Complaint, id=complaint_id, user=user)

        if Feedback.objects.filter(complaint=complaint).exists():
            messages.warning(request, "You've already given feedback for this complaint.")
        else:
            Feedback.objects.create(
                complaint=complaint,
                user=user,
                rating=rating,
                comments=comments
            )
            messages.success(request, "Thank you for your feedback!")

        return redirect("complaint_responses")

    return render(request, "complaint_responses.html", {
        "complaints": complaints,
        "page_name": "responses"
    })


@login_required(login_url='login')
def university_faq(request):
    answer = None
    raw_response = None
    error = None

    if request.method == "POST":
        user_question = request.POST.get("question")

        if user_question:
            try:
                
                prompt = f"""You are the official AI assistant for University of Asia Pacific (UAP). Answer questions accurately and thoroughly based on the following sources:

            Main sources:
            - UAP official website: https://www.uap-bd.edu/
            - CSE department website: https://cse.uap-bd.edu/
            - UAP Wikipedia page: https://en.wikipedia.org/wiki/University_of_Asia_Pacific
            - Tuition fees information: https://www.uap-bd.edu/undergraduate.php
            - Admission information: https://www.uap-bd.edu/admission_info_undergraduate.php

            Instructions:
            1. Provide detailed, comprehensive information - don't be superficial
            2. Include specific facts, figures, dates, and names when available
            3. For academic questions, mention course codes, credit hours, and prerequisites if relevant
            4. For faculty questions, include their positions, qualifications, and research areas
            5. Structure your response with clear sections using bullet points where appropriate
            6. When discussing facilities, be specific about what equipment or resources are available
            7. For contact information questions, provide exact details including room numbers, phone numbers, and email addresses if available
            8. If answering about research, mention specific research areas, labs, and notable projects

            Question: {user_question}
            Remember to provide a thorough, well-structured answer that would satisfy a student or faculty member who needs complete information."""

                contents = [
                    types.Content(
                        role="user",
                        parts=[{"text": prompt}]  
                    ),
                ]

                generate_content_config = types.GenerateContentConfig(
                    response_mime_type="text/plain",
                )

               
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=contents,
                        config=generate_content_config,
                    )
                    answer = response.text
                    raw_response = response.text
                    # print("Raw Response:", raw_response)
                
                except Exception as e:
                    print(f"Non-streaming request failed: {e}")
                    
                    response_chunks = client.models.generate_content_stream(
                        model="gemini-2.0-flash",
                        contents=contents,
                        config=generate_content_config,
                    )
                    
                    
                    raw_response = []
                    answer = ""
                    
                    
                    for chunk in response_chunks:
                        if hasattr(chunk, 'text') and chunk.text:
                            raw_response.append(chunk.text)
                            answer += chunk.text

                    # print("Raw Response (streaming):", raw_response)

            except Exception as e:
                error = f"Gemini API Error: {str(e)}"
                # print(f"Error: {error}")
                messages.error(request, error)

    return render(request, "university_faq.html", {
        "answer": answer,
        "raw_response": raw_response,
        "error": error
    })


@login_required(login_url='authority_login')
def authority_dashboard(request):
    try:
        authority = Authority.objects.get(user=request.user)
    except Authority.DoesNotExist:
        return redirect("authority_login")

    complaints = Complaint.objects.filter(department=authority.department).order_by("-created_at")

    return render(request, "authority_dashboard.html", {
        "complaints": complaints,
        "authority": authority,
    })




