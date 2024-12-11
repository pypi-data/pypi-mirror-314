import erppeek
import csv

client = erppeek.Client.from_config('odoo')

ContractLine = client.model("contract.line")
Products = client.model("product.product")


with open('contract_lines_products.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        contract_line_id = row['contract_line_id']
        product_id = row['product_id']

        print("Processing contract line: ", contract_line_id)

        contract_line = ContractLine.browse([('id', '=', contract_line_id), ])

        if not contract_line:
            print("No contract_line is found with id: ", contract_line_id)
            continue

        odoo_product_id = Products.browse([('id', '=', product_id), ]).read('id')

        if not odoo_product_id:
            print("No product is found with id: ", product_id)
            continue
        else:
            odoo_product_id = odoo_product_id[0]

        contract_line.write({"product_id": odoo_product_id})

        print("Finished processing line: ", contract_line_id)
