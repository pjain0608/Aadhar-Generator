from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Aadhar
from django.conf import settings
import random

# View for handling the home page and form submission
def home(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        email = request.POST['email']
        gender = request.POST['gender']
        address = request.POST['address']
        fathers_name = request.POST['fathers_name']
        mothers_name = request.POST['mothers_name']

        # Handle the uploaded image
        img = request.FILES['img']

        try:
            # Generate a unique 12-digit Aadhar number starting from 350060070001
            last_aadhar = Aadhar.objects.order_by('-aadhar').first()
            if last_aadhar:
                new_aadhar_number = last_aadhar.aadhar + 1
            else:
                new_aadhar_number = 350060070001

            # Save the data to the database
            aadhar_entry = Aadhar(
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                dob=dob,
                email=email,
                gender=gender,
                address=address,
                fathers_name=fathers_name,
                mothers_name=mothers_name,
                aadhar=new_aadhar_number,
                img=img
            )
            aadhar_entry.save()

            # Send a confirmation email to the user
            subject = 'Aadhar Enrollment Successful'
            message = f'Dear {first_name} {last_name},\n\nYour Aadhar enrollment has been successfully submitted.\nYour Aadhar Number is {new_aadhar_number}.\n\nThank you for using our service.\n\nBest regards,\nAadhar Portal Team'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            # Success message to display on the template
            return render(request, 'home.html', {'success_message': 'Enrollment successful! A confirmation email has been sent.'})

        except Exception as e:
            # Handle errors (e.g., duplicate entries)
            return render(request, 'home.html', {'error_message': f'Error: {str(e)}'})

    return render(request, 'home.html')

def view(request):
    context = {
        'error_message': None,  # Default value for error message
        'success_message': None,  # Default value for success message
    }

    if request.method == 'POST':
        # Step 1: Handle Aadhar number input and send OTP
        if 'step' not in request.POST or request.POST['step'] == 'input_aadhar':
            aadhar_number = request.POST.get('aadhar_number')
            try:
                user = Aadhar.objects.get(aadhar=aadhar_number)

                # Generate OTP
                otp = random.randint(100000, 999999)
                user.otp = otp
                user.save()

                # Send OTP to user's email
                subject = 'Your Aadhar OTP'
                message = f'Dear {user.first_name},\n\nYour OTP for viewing Aadhar details is {otp}. Please do not share this with anyone.\n\nBest regards,\nAadhar Portal Team'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)

                # Update context to show OTP entry step
                context['step'] = 'enter_otp'
                context['aadhar_number'] = aadhar_number
                context['success_message'] = 'OTP sent to your registered email.'
            
            except Aadhar.DoesNotExist:
                context['step'] = 'input_aadhar'  # Stay on the current step
                context['error_message'] = 'Invalid Aadhar number. Please try again.'

        # Step 2: Handle OTP validation and display details
        elif request.POST['step'] == 'enter_otp':
            aadhar_number = request.POST.get('aadhar_number')
            entered_otp = request.POST.get('otp')

            try:
                user = Aadhar.objects.get(aadhar=aadhar_number)

                if str(user.otp) == entered_otp:
                    # Clear OTP for security
                    user.otp = None
                    user.save()

                    # Pass user details to the template
                    context['step'] = 'view_details'
                    context['user'] = user
                else:
                    # Invalid OTP
                    context['step'] = 'enter_otp'
                    context['aadhar_number'] = aadhar_number
                    context['error_message'] = 'Invalid OTP. Please try again.'
            except Aadhar.DoesNotExist:
                context['error_message'] = 'Invalid Aadhar number. Please try again.'

    else:
        # Default step: Input Aadhar
        context['step'] = 'input_aadhar'

    return render(request, 'view.html', context)
