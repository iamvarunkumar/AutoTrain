from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect
import sqlite3


# Create your views here.
def index(request):
    return render(request, 'index.html',)

def login(request):
    return render(request, 'signup.html')

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

        # Store the list of dictionaries in the session
        request.session['uploaded_data'] = data_as_dicts

        # Redirect to the DataFrame summary page
        return HttpResponseRedirect('/dataframe_summary/')
    
    return render(request, 'dev.html')
    
def dataframe_summary(request):
    df_preview = None
    save_success = request.GET.get('save_success', False)

    # Retrieve the list of dictionaries from the session
    data_as_dicts = request.session.get('uploaded_data')
    
    if data_as_dicts is not None:
        # Convert the list of dictionaries back to a DataFrame for display
        df = pd.DataFrame(data_as_dicts)
        # Generate HTML for displaying first 10 rows of DataFrame
        df_preview = df.head(10).to_html(classes='table table-striped')

        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

        context = {
            'preview_html':df_preview,
            'save_success':save_success,
            'num_rows':df.shape[0],
            'num_cols':df.shape[1],
            'numerical_cols':numerical_cols,
            'num_numerical_cols':len(numerical_cols),
            'num_cat_cols':len(cat_cols),
            'num_datetime_cols':len(date_cols),
            'cat_cols':cat_cols,
            'datetime_cols':date_cols
            }
        
        if len(date_cols)==0:
            context['datetime_cols'] = 'None'
            context['num_datetime_cols'] = 0
        

    return render(request, 'dataframe_summary.html', context)
    
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
            


    
    
