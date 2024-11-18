import pandas as pd
import mysql.connector
from mysql.connector import Error

# Hàm kết nối tới cơ sở dữ liệu MySQL
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='realestatedb_1'
        )
        print("Kết nối thành công tới MySQL")
    except Error as e:
        print(f"Lỗi '{e}' xảy ra")
    return connection

# Hàm kiểm tra và lấy hoặc chèn region_id
def get_or_insert_region_id(connection, region_name, city):
    cursor = connection.cursor()
    cursor.execute("SELECT region_id FROM dimension_region WHERE region_name = %s", (region_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO dimension_region (region_name, city) VALUES (%s, %s)", (region_name, city))
        connection.commit()
        return cursor.lastrowid

# Hàm kiểm tra và lấy hoặc chèn type_id
def get_or_insert_type_id(connection, type_name):
    cursor = connection.cursor()
    cursor.execute("SELECT type_id FROM dimension_real_estate_type WHERE type_name = %s", (type_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO dimension_real_estate_type (type_name) VALUES (%s)", (type_name,))
        connection.commit()
        return cursor.lastrowid

# Hàm kiểm tra và lấy hoặc chèn status_id
def get_or_insert_status_id(connection, status_name):
    cursor = connection.cursor()
    cursor.execute("SELECT status_id FROM dimension_real_estate_status WHERE status_name = %s", (status_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO dimension_real_estate_status (status_name) VALUES (%s)", (status_name,))
        connection.commit()
        return cursor.lastrowid

def get_or_insert_customer_id(connection, customer_name, phone, encryption_key):
    cursor = connection.cursor()
    # Sử dụng AES_DECRYPT để giải mã và so sánh số điện thoại trong truy vấn SELECT
    cursor.execute("""
        SELECT customer_id 
        FROM dimension_customer 
        WHERE customer_name = %s AND AES_DECRYPT(phone, %s) = %s
    """, (customer_name, encryption_key, phone))
    
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        # Sử dụng AES_ENCRYPT để mã hóa số điện thoại trước khi chèn vào
        cursor.execute("""
            INSERT INTO dimension_customer (customer_name, phone) 
            VALUES (%s, AES_ENCRYPT(%s, %s))
        """, (customer_name, phone, encryption_key))
        connection.commit()
        return cursor.lastrowid


# Hàm chuẩn hóa giá tiền
def normalize_price(price_str):
    if isinstance(price_str, str):
        price_str = price_str.replace(' triệu/tháng', ' triệu').replace(' tr/m²', ' triệu')
        price_str = price_str.replace(',', '.')  # Thay dấu phẩy bằng dấu chấm
        try:
            if 'tỷ' in price_str:
                price_value = float(price_str.replace(' tỷ', '').strip())
                return price_value * 1000000000
            elif 'triệu' in price_str:
                price_value = float(price_str.replace(' triệu', '').strip())
                return price_value * 1000000
            else:
                return float(price_str)
        except ValueError:
            return None
    return None

# Hàm chuẩn hóa diện tích
def normalize_area(area_str):
    if isinstance(area_str, str):
        area_str = area_str.replace(' m²', '').replace(' ', '')
        try:
            return float(area_str)
        except ValueError:
            return None
    return None

# Hàm chuẩn hóa và chuyển đổi ngày tháng
def normalize_date(date_str):
    if isinstance(date_str, pd.Timestamp):
        return date_str.strftime('%Y-%m-%d')
    return None

# Hàm để chèn dữ liệu vào bảng fact_real_estate_transaction
def insert_real_estate_transaction(connection, data, encryption_key):
    cursor = connection.cursor()
    query = """
    INSERT INTO fact_real_estate_transaction (title, transaction_date, type_id, status_id, region_id, customer_id, price, rental_price, price_per_sqm, total_area)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for index, row in data.iterrows():
        region_id = get_or_insert_region_id(connection, row['Địa chỉ'], row['Thành phố']) if 'Địa chỉ' in row else None
        type_id = get_or_insert_type_id(connection, row['Loại tài sản']) if 'Loại tài sản' in row else None
        status_id = get_or_insert_status_id(connection, row['Trạng thái']) if 'Trạng thái' in row else None
        customer_id = get_or_insert_customer_id(connection, row['Tên khách hàng'], row['Số điện thoại'], encryption_key ) if pd.notnull(row['Tên khách hàng']) else None

        cursor.execute(query, (
            row['Tiêu đề'],  
            normalize_date(row['Thời gian giao dịch']),
            type_id,
            status_id,
            region_id,
            customer_id,
            normalize_price(row['Giá']) if 'Giá' in row else None,
            normalize_price(row['Giá tiền 1 tháng']) if 'Giá tiền 1 tháng' in row else None,
            normalize_price(row['Giá trên 1 mét vuông']) if 'Giá trên 1 mét vuông' in row else None,
            normalize_area(row['Tổng diện tích']) if 'Tổng diện tích' in row else None
        ))
    connection.commit()
    print("Dữ liệu đã được chèn vào bảng fact_real_estate_transaction")

# Kết nối tới cơ sở dữ liệu
connection = create_connection("localhost", "root", "12345", "realestatedb_1")

# Đọc dữ liệu từ file Excel
rental_data = pd.read_excel(r'C:\Users\MSI\Documents\RealEstateStarDB\bat_dong_san_Cho_Thue.xlsx')
sales_data = pd.read_excel(r'C:\Users\MSI\Documents\RealEstateStarDB\bat_dong_san_Mua_Ban.xlsx')

# Khóa bí mật cho mã hóa AES
encryption_key = '12345'

# Nhập dữ liệu vào bảng fact_real_estate_transaction
insert_real_estate_transaction(connection, rental_data , encryption_key)
insert_real_estate_transaction(connection, sales_data , encryption_key)

# Đóng kết nối
if connection:
    connection.close()
