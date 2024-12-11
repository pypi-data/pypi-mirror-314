## ERPPeek scripts

This directory contains python scripts that interact with the ODOO database using an external source of data (csv). We are using the [`erppeek`](https://erppeek.readthedocs.io/en/latest/) for this purpose.


### Usage

0. Access to the server with SSH and follow the ssh-agent:
```
ssh -A user@host
```
1. Change to `odoo` user.
```
sudo su odoo
```
2. Go to `erpeek` folder.
```
cd ~/pyenv/versions/odoo/src/odoo12-addon-somconnexio/somconnexio/migrations/erpeek
```
3. Modify the `erppeek.ini` with the Odoo credentials. Use the user and password to access the Odoo via UI.
4. Activate the virtual env
```
pyenv activate odoo
```
5. Install the requirements:
```
pip install -r requirements.txt
```
6. Give execution permissions to the python script
```
chmod +x <python-script.py>
```
7. Run the script instructions

### Scripts

#### Update product from contract lines

This script loads a csv with two colums (contract_line_id, product_id) and updates the database seting to each contract_line the corresponding product.

**Usage**

0. Follow the instructions of Usage section.
1. Upload the csv data file to this server, within the erpeek folder, and name it "contract_lines_products.csv".
2. Execute the script `python update_contract_line_product_id.py > /var/log/odoo/update_contract_line_product_id.log`.
