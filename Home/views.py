from django.shortcuts import render, redirect
import pandas as pd
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
import sqlite3
import json
from django.contrib import messages
from .models import UserSignUpDetails
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'index.html',)

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            # Save user input to UserSignUpDetails model
            user = UserSignUpDetails.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),  # Updated to match the form field name
            rep_password=request.POST.get('rep_password'),  # Updated to match the form field name
            )
            user.save()

            messages.success(request, f'Account created successfully for {user.name}. Please login.')
            return redirect('login')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)

                # Retrieve user input from UserInput model
                user_input = UserSignUpDetails.objects.get(user=user)

                messages.success(request, f'Welcome, {user.username}!')

                return redirect('welcome')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url="login")
def welcome(request):
    return render(request, 'welcome.html')


def documentation(request):
    return render(request, 'documentation.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def dev(request):
    return render(request, 'dev.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['data']:
        uploaded_file = request.FILES['data']
        # Check file type and read into DataFrame (CSV or Excel)
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            # Handle unsupported file types
            return render(request, 'unsupported_file.html')

        # Convert DataFrame to a list of dictionaries
        data_as_dicts = df.to_dict(orient='records')

        # Convert the list of dictionaries to JSON string
        data_json = json.dumps(data_as_dicts)

        # Store the JSON string in the session
        request.session['uploaded_data'] = data_json

        # Redirect to the DataFrame summary page
        return HttpResponseRedirect('/dataframe_summary/')
    
    return render(request, 'dev.html')

#================== HELPER FUNCTION ==================#

def get_common_context(request):
    df_preview = None
    save_success = request.GET.get('save_success', False)

    data_json = request.session.get('uploaded_data')
    uploaded_data_exists = data_json is not None

    context = {
        'save_success': save_success,
        'uploaded_data_exists': uploaded_data_exists,
    }

    if uploaded_data_exists:
        data_as_dicts = json.loads(data_json)
        df = pd.DataFrame(data_as_dicts)
        df_preview = df.head(10).to_html(classes='table table-striped')

        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

        context.update({
            'preview_html': df_preview,
            'save_success': save_success,
            'num_rows': df.shape[0],
            'num_cols': df.shape[1],
            'numerical_cols': numerical_cols,
            'num_numerical_cols': len(numerical_cols),
            'num_cat_cols': len(cat_cols),
            'num_datetime_cols': len(date_cols),
            'cat_cols': cat_cols,
            'datetime_cols': date_cols
        })

        if len(date_cols) == 0:
            context['datetime_cols'] = 'None'
            context['num_datetime_cols'] = 0

    return context

def dataframe_summary(request):
    context = get_common_context(request)
    return render(request, 'dataframe_summary.html', context)

def enable_dashboard_items(request):
    from_summary_page = request.POST.get('from_summary_page', False)

    if from_summary_page:
        # Logic to enable components for users coming from summary page
        # You can set a flag in the context and use it in the template

        context = get_common_context(request)
        context.update({
            'enable_components': True,
        })

        # Add any additional context you need here

        return render(request, 'dashboard.html', context)
    else:
        # Logic for users accessing dev.html directly without coming from summary page
        # Set the flag to False or omit it from the context

        context = {
            'enable_components': False,
        }

        return render(request, 'dashboard.html', context)
    
def save_to_database(request):
    save_success = False  # Default to False if not successful

    if request.method == 'POST':
        dbName = request.POST.get('dbName')
        tableName = request.POST.get('tableName')
        data_as_dicts = request.session.get('uploaded_data')

        if data_as_dicts is not None:
            try:
                # Convert the list of dictionaries back to a DataFrame for saving to SQLite
                df = pd.DataFrame(data_as_dicts)
                
                # Create a connection to the SQLite database
                conn = sqlite3.connect(f"{dbName}.db")
                
                # Save the DataFrame to the SQLite database as a table
                df.to_sql(tableName, conn, index=False, if_exists='replace')
                
                # Close the connection
                conn.close()
                
                # Set save_success flag to True on successful save
                save_success = True
            except Exception as e:
                print(e)  # Handle the exception appropriately
                # In case of an exception/error, save_success remains False

    # Redirect to dataframe_summary with save_success flag in the URL
    return HttpResponseRedirect(f'/dataframe_summary/?save_success={save_success}')

           


    
    
