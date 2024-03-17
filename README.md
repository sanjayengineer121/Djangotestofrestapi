# Djangotestofrestapi

Assignment Details -

You need to create a single url /invoices/ for thisCreate a Django application (Django Rest Framework) using the given information:

You need to create a single url /invoices/ for this

/invoices/
/invoices/<int:pk>/

- Create two Django models viz. Invoice and Invoice Detail.
- Invoice model fields -> Date, Invoice CustomerName.
- InvoiceDetail model fields -> invoice (ForeignKey), description, quantity, unit_price, price.
- Create APIs using Django Rest Framework for all the HTTP methods for the invoice models. 
- The API should also accept invoice_details in the payload and create/update the associated invoice details too 

- Create test cases to test all the API endpoints.
