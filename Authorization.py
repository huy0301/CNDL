import mysql.connector
from mysql.connector import Error

# Hàm kết nối tới cơ sở dữ liệu MySQL
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user='restricted',  
            password='restricted123',  
            database="RealEstateDB_1"
        )
        print(f"Kết nối thành công tới MySQL với người dùng: {user_name}")
    except Error as e:
        print(f"Lỗi '{e}' xảy ra")
    return connection

# Hiển thị danh sách khu vực từ bảng dimension_region
def display_regions(connection):
    cursor=connection.cursor()
    query = "SELECT region_id, region_name, city FROM dimension_region;"
    cursor.execute(query)
    regions = cursor.fetchall()
    print("\nDanh sách khu vực hiện tại:")
    for region in regions:
        print(f"ID: {region[0]}, Tên khu vực: {region[1]}, Thành phố: {region[2]}")
    print()  

# Hàm thêm dữ liệu vào bảng dimension_region
def insert_region(connection, region_name, city):
    if connection is None:
        print("Không thể thêm dữ liệu vì không có kết nối.")
        return
    cursor = connection.cursor()
    query = "INSERT INTO dimension_region (region_name, city) VALUES (%s, %s);"
    data = (region_name, city)
    cursor.execute(query, data)
    connection.commit()
    print("Dữ liệu đã được thêm vào bảng dimension_region.")
    display_regions(connection)

# Hàm sửa dữ liệu trong bảng dimension_region
def update_region(connection, region_id, new_region_name, new_city):
    cursor = connection.cursor()
    query = "UPDATE dimension_region SET region_name = %s, city = %s WHERE region_id = %s;"
    data = (new_region_name, new_city, region_id)
    cursor.execute(query, data)
    connection.commit()
    print("Dữ liệu đã được cập nhật trong bảng dimension_region.")
    display_regions(connection)

# Hàm xóa dữ liệu trong bảng dimension_region
def delete_region(connection, region_id):
    cursor = connection.cursor()
    query = "DELETE FROM dimension_region WHERE region_id = %s;"
    data = (region_id,)
    cursor.execute(query, data)
    connection.commit()
    print("Dữ liệu đã được xóa trong bảng dimension_region.")
    display_regions(connection)

# Kết nối tới cơ sở dữ liệu
connection = create_connection("localhost", "restricted", "restricted123", "RealEstateDB_1")

# Thực hiện các thao tác
try:
    # Hiển thị khu vực
    #display_regions(connection)

    # Thêm một khu vực mới
    insert_region(connection,'Huyện Chương Mỹ', 'Hà Nội')

    # Cập nhật tên và thành phố của khu vực
    #update_region(connection,37 , 'Huyện Vĩnh Phúc' , 'Vĩnh Phúc')

    # Xóa một khu vực
    #delete_region(connection,37)
except Error as e:
    print(f"Lỗi: {e}")
finally:
    if connection:
        connection.close()
