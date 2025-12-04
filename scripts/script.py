import pandas as pd
import matplotlib.pyplot as plt
import os

# ====================================
# CREATE OUTPUT FOLDER
# ====================================
# Buat folder 'outputs' jika belum ada
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"✓ Folder '{output_folder}' created")
else:
    print(f"✓ Folder '{output_folder}' already exists")

# ====================================
# 1. LOAD DATA
# ====================================
print("=" * 50)
print("LOADING DATA")
print("=" * 50)

# Baca semua file CSV
# Sesuaikan path dengan lokasi file Anda:

# Jika file di folder 'data':
customers = pd.read_csv('data/customer.csv')
products = pd.read_csv('data/product.csv')
transactions = pd.read_csv('data/transaction.csv')

# Atau jika file di folder yang sama dengan script:
# customers = pd.read_csv('customers.csv')
# products = pd.read_csv('products.csv')
# transactions = pd.read_csv('transactions.csv')

# Atau jika file di folder 'dataset':
# customers = pd.read_csv('dataset/customers.csv')
# products = pd.read_csv('dataset/products.csv')
# transactions = pd.read_csv('dataset/transactions.csv')

print(f"✓ Customers: {len(customers)} rows")
print(f"✓ Products: {len(products)} rows")
print(f"✓ Transactions: {len(transactions)} rows")
print()

# ====================================
# 2. DATA PREPARATION
# ====================================
print("=" * 50)
print("DATA PREPARATION")
print("=" * 50)

# Filter hanya transaksi yang completed
transactions_completed = transactions[transactions['status'] == 'Completed'].copy()
print(f"Completed transactions: {len(transactions_completed)}")

# Join transactions dengan products untuk mendapatkan harga
sales_data = transactions_completed.merge(products, on='product_id')

# Join dengan customers untuk mendapatkan info pelanggan
sales_data = sales_data.merge(customers, on='customer_id')

# Hitung total penjualan (price * quantity)
sales_data['total_sales'] = sales_data['price'] * sales_data['quantity']

print(f"Sales data shape: {sales_data.shape}")
print()

# ====================================
# 3. TOTAL REVENUE
# ====================================
print("=" * 50)
print("TOTAL REVENUE ANALYSIS")
print("=" * 50)

total_revenue = sales_data['total_sales'].sum()
total_transactions = len(sales_data)
avg_transaction_value = sales_data['total_sales'].mean()

print(f"Total Revenue: Rp {total_revenue:,.0f}")
print(f"Total Transactions: {total_transactions}")
print(f"Average Transaction Value: Rp {avg_transaction_value:,.0f}")
print()

# ====================================
# 4. SALES BY CATEGORY
# ====================================
print("=" * 50)
print("SALES BY CATEGORY")
print("=" * 50)

sales_by_category = sales_data.groupby('category').agg({
    'total_sales': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).round(0)

sales_by_category.columns = ['Total Sales', 'Transactions', 'Quantity Sold']
sales_by_category = sales_by_category.sort_values('Total Sales', ascending=False)

print(sales_by_category)
print()

# ====================================
# 5. TOP 10 PRODUCTS
# ====================================
print("=" * 50)
print("TOP 10 BEST SELLING PRODUCTS")
print("=" * 50)

top_products = sales_data.groupby(['product_id', 'product_name']).agg({
    'total_sales': 'sum',
    'quantity': 'sum'
}).round(0)

top_products.columns = ['Total Sales', 'Quantity Sold']
top_products = top_products.sort_values('Total Sales', ascending=False).head(10)

print(top_products)
print()

# ====================================
# 6. SALES BY CITY
# ====================================
print("=" * 50)
print("SALES BY CITY")
print("=" * 50)

sales_by_city = sales_data.groupby('city').agg({
    'total_sales': 'sum',
    'customer_id': 'nunique',
    'transaction_id': 'count'
}).round(0)

sales_by_city.columns = ['Total Sales', 'Unique Customers', 'Transactions']
sales_by_city = sales_by_city.sort_values('Total Sales', ascending=False)

print(sales_by_city)
print()

# ====================================
# 7. SALES BY PAYMENT METHOD
# ====================================
print("=" * 50)
print("SALES BY PAYMENT METHOD")
print("=" * 50)

sales_by_payment = sales_data.groupby('payment_method').agg({
    'total_sales': 'sum',
    'transaction_id': 'count'
}).round(0)

sales_by_payment.columns = ['Total Sales', 'Transactions']
sales_by_payment['Avg Transaction'] = (sales_by_payment['Total Sales'] / 
                                        sales_by_payment['Transactions']).round(0)
sales_by_payment = sales_by_payment.sort_values('Total Sales', ascending=False)

print(sales_by_payment)
print()

# ====================================
# 8. TOP CUSTOMERS
# ====================================
print("=" * 50)
print("TOP 10 CUSTOMERS BY SPENDING")
print("=" * 50)

top_customers = sales_data.groupby(['customer_id', 'name']).agg({
    'total_sales': 'sum',
    'transaction_id': 'count'
}).round(0)

top_customers.columns = ['Total Spending', 'Transactions']
top_customers['Avg per Transaction'] = (top_customers['Total Spending'] / 
                                         top_customers['Transactions']).round(0)
top_customers = top_customers.sort_values('Total Spending', ascending=False).head(10)

print(top_customers)
print()

# ====================================
# 9. DAILY SALES TREND
# ====================================
print("=" * 50)
print("DAILY SALES TREND")
print("=" * 50)

# Convert transaction_date to datetime
# Format: DD/MM/YYYY (dayfirst=True untuk format Indonesia/Eropa)
sales_data['transaction_date'] = pd.to_datetime(sales_data['transaction_date'], dayfirst=True)

daily_sales = sales_data.groupby('transaction_date').agg({
    'total_sales': 'sum',
    'transaction_id': 'count'
}).round(0)

daily_sales.columns = ['Total Sales', 'Transactions']
print(daily_sales.head(10))
print()

# ====================================
# 10. VISUALIZATION (Optional)
# ====================================
print("=" * 50)
print("CREATING VISUALIZATIONS")
print("=" * 50)

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Sales Analysis Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Sales by Category
sales_by_category['Total Sales'].plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Sales by Category')
axes[0, 0].set_ylabel('Total Sales (Rp)')
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Top 5 Products
top_products.head(5)['Total Sales'].plot(kind='barh', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Top 5 Products by Sales')
axes[0, 1].set_xlabel('Total Sales (Rp)')

# Plot 3: Sales by City
sales_by_city['Total Sales'].plot(kind='bar', ax=axes[1, 0], color='lightgreen')
axes[1, 0].set_title('Sales by City')
axes[1, 0].set_ylabel('Total Sales (Rp)')
axes[1, 0].tick_params(axis='x', rotation=45)

# Plot 4: Sales by Payment Method
sales_by_payment['Total Sales'].plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%')
axes[1, 1].set_title('Sales Distribution by Payment Method')
axes[1, 1].set_ylabel('')

plt.tight_layout()

# Simpan di folder 'outputs'
output_path = os.path.join(output_folder, 'sales_analysis_dashboard.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Dashboard saved as '{output_path}'")
print()

print("=" * 50)
print("ANALYSIS COMPLETED!")
print("=" * 50)
