from rest_framework import generics
from django.db import models  # Import the models module
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
import datetime
import requests

@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            amount = data.get('amount')

            invoice_data = load_data()

            new_id = len(invoice_data["payment"]["invoices"]) + 1

            new_invoice = {
                'id': new_id,
                'name': name,
                'amount': amount,
                'time':str(datetime.datetime.now().isoformat())
            }

            invoice_data["payment"]["invoices"].append(new_invoice)

            save_data(invoice_data)

            return JsonResponse(new_invoice, status=201)  # HTTP 201 Created
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400) 
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)  
    
@csrf_exempt
def modify_invoice(request, invoice_id):
    if request.method == 'PUT':  # Use PUT method for modification
        try:
            data = json.loads(request.body)
            name = data.get('name')
            amount = data.get('amount')

            invoice_data = load_data()

            # Find the invoice with the given ID
            found = False
            for invoice in invoice_data["payment"]["invoices"]:
                if invoice['id'] == invoice_id:
                    invoice['name'] = name
                    invoice['amount'] = amount
                    invoice['time'] = str(datetime.datetime.now().isoformat())
                    found = True
                    break

            if not found:
                return JsonResponse({'error': f'Invoice with ID {invoice_id} not found'}, status=404)

            save_data(invoice_data)

            return JsonResponse(invoice, status=200)  # HTTP 200 OK, returning modified invoice
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def load_data():
    try:
        with open('invoice.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"payment": {"invoices": []}}

def save_data(data):
    with open('invoice.json', 'w') as file:
        json.dump(data, file, indent=2)
        
def reciept(request, pk):

    selected_invoice = f"Invoice {pk} has been selected."

    return render(request, 'invoice_no.html', {'selected_invoice': selected_invoice})

def invoices(request):
    invoice_data = load_data()
    invoices = invoice_data["payment"]["invoices"]
    return render(request,'invoice.html',{'invoices': invoices})

def update(request):
    voucher=""
    if request.method=="POST":
        invoice_data = load_data()
        voucher_no=request.POST.get('vrch')
        voucher=voucher_no
        name=""
        amount=""
        for i in invoice_data["payment"]["invoices"]:
            if i['id']==int(voucher_no):
                name=i['name']
                amount=i['amount']

        return render(request,'update.html',{'nameofc': name, 'amount': amount})
    
    
    
    return render(request,'update.html')



def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        print("Party Name:", name)
        print("Amount:", amount)
        if not name or not amount:  # Check if any post data is missing
            messages.error(request, 'Name and Amount are required.')  
            return render(request, 'create.html')
        url = 'http://127.0.0.1:8000/api/createinvoice/'
        
        new_invoice = {
            'name': name,
            'amount': amount,
        }

        response = requests.post(url, json=new_invoice)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx status codes)
        if response.status_code == 201:
            print("Invoice created successfully!")
            print(response.json())
            return redirect('invoices')
    return render(request, 'create.html')


# import requests
# import json

# url = 'http://127.0.0.1:8000/modifyinvoice/5/'  # Modify the URL as needed
# data = {
#     "name": "SANJU keshwarwani",
#     "amount": 113
# }
# headers = {'Content-Type': 'application/json'}

# response = requests.put(url, data=json.dumps(data), headers=headers)

# print(response.status_code)
# print(response.json())