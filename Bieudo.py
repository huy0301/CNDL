# Import các thư viện cần thiết
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import streamlit as st

# Kết nối đến cơ sở dữ liệu MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="12345",  
        database="RealEstateDB_1"
    )

# Hàm tạo biểu đồ cột: Phân khúc bất động sản của một khu vực
def bieudo1(db):
    st.write("## Biểu đồ Cột: Phân khúc bất động sản")
    query = "SELECT region_id, region_name, city FROM dimension_region"
    df_region = pd.read_sql(query, db)
    
    # Hiển thị danh sách khu vực
    st.write("### Danh sách khu vực")
    st.write(df_region)
    
    # Thêm tùy chọn "Tất cả" vào danh sách các khu vực
    region_options = ["Tất cả"] + df_region['region_name'].tolist()
    selected_region_name = st.selectbox("Chọn khu vực hoặc chọn 'Tất cả' để hiển thị tất cả", region_options)
    
    # Kiểm tra nếu chọn "Tất cả" để hiển thị dữ liệu toàn bộ
    if selected_region_name == "Tất cả":
        query_segment = """
        SELECT Segment, SUM(TotalProperties) AS TotalProperties
        FROM RealEstate_Segment
        GROUP BY Segment;
        """
        title = 'Phân khúc bất động sản của tất cả các khu vực'
    else:
        query_segment = f"""
        SELECT Segment, TotalProperties
        FROM RealEstate_Segment
        WHERE Region = '{selected_region_name}';
        """
        title = f'Phân khúc bất động sản của khu vực {selected_region_name}'
    
    df_segment = pd.read_sql(query_segment, db)
    
    # Vẽ biểu đồ phân khúc
    fig, ax = plt.subplots()
    bars = ax.bar(df_segment['Segment'], df_segment['TotalProperties'], color='skyblue')
    ax.set_title(title)
    ax.set_xlabel('Phân khúc')
    ax.set_ylabel('Số lượng bất động sản')
    
    # Thêm giá trị lên đầu mỗi cột
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
    
    st.pyplot(fig)

# Hàm tạo biểu đồ tròn: Tỷ lệ tài sản cho thuê và bán theo khu vực hoặc phân khúc
def bieudo2(db):
    st.write("## Biểu đồ Tròn: Tỷ lệ tài sản cho thuê và bán")
    query = "SELECT region_name, city FROM dimension_region"
    df_region = pd.read_sql(query, db)
    
    # Hiển thị danh sách khu vực
    st.write("### Danh sách khu vực")
    st.write(df_region)
    
    # Lựa chọn hiển thị theo khu vực hoặc phân khúc
    display_choice = st.selectbox("Hiển thị theo", ["Khu vực", "Phân khúc", "Khu vực và Phân khúc"])

    # Lựa chọn khu vực
    region_options = ["Tất cả"] + df_region['region_name'].tolist()
    selected_region_name = st.selectbox("Chọn khu vực", region_options)
    
    # Truy vấn phân khúc (nếu cần)
    query_segment = "SELECT DISTINCT Segment FROM RealEstate_Segment"
    df_segment = pd.read_sql(query_segment, db)
    selected_segment = st.selectbox("Chọn phân khúc (tùy chọn)", ["Tất cả"] + df_segment['Segment'].tolist())
    
    # Xây dựng truy vấn dữ liệu cho biểu đồ tròn dựa trên lựa chọn
    if display_choice == "Khu vực":
        if selected_region_name == "Tất cả":
            query_rental_sales = """
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            GROUP BY transaction_type;
            """
            title_pie = 'Tỷ lệ tài sản cho thuê và bán trên tất cả các khu vực'
        else:
            query_rental_sales = f"""
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            WHERE RegionName = '{selected_region_name}'
            GROUP BY transaction_type;
            """
            title_pie = f'Tỷ lệ tài sản cho thuê và bán tại khu vực {selected_region_name}'
    
    elif display_choice == "Phân khúc":
        if selected_segment == "Tất cả":
            query_rental_sales = """
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            GROUP BY transaction_type;
            """
            title_pie = 'Tỷ lệ tài sản cho thuê và bán theo phân khúc trên tất cả khu vực'
        else:
            query_rental_sales = f"""
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            WHERE Segment = '{selected_segment}'
            GROUP BY transaction_type;
            """
            title_pie = f'Tỷ lệ tài sản cho thuê và bán trong phân khúc {selected_segment}'
    else:  # Kết hợp Khu vực và Phân khúc
        if selected_region_name == "Tất cả" and selected_segment == "Tất cả":
            query_rental_sales = """
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            GROUP BY transaction_type;
            """
            title_pie = 'Tỷ lệ tài sản cho thuê và bán trên tất cả khu vực và phân khúc'
        elif selected_region_name == "Tất cả":
            query_rental_sales = f"""
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            WHERE Segment = '{selected_segment}'
            GROUP BY transaction_type;
            """
            title_pie = f'Tỷ lệ tài sản cho thuê và bán trong phân khúc {selected_segment} trên tất cả khu vực'
        elif selected_segment == "Tất cả":
            query_rental_sales = f"""
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            WHERE RegionName = '{selected_region_name}'
            GROUP BY transaction_type;
            """
            title_pie = f'Tỷ lệ tài sản cho thuê và bán tại khu vực {selected_region_name} (tất cả phân khúc)'
        else:
            query_rental_sales = f"""
            SELECT IF(transaction_type = 1, 'Bán', 'Thuê') AS transaction_type, SUM(TotalTransactions) AS Total
            FROM Transaction_Count_By_Month
            WHERE RegionName = '{selected_region_name}' AND Segment = '{selected_segment}'
            GROUP BY transaction_type;
            """
            title_pie = f'Tỷ lệ tài sản cho thuê và bán tại khu vực {selected_region_name} - Phân khúc {selected_segment}'
    
    df_rental_sales = pd.read_sql(query_rental_sales, db)
    
    # Vẽ biểu đồ tròn
    fig, ax = plt.subplots()
    ax.pie(df_rental_sales['Total'], labels=df_rental_sales['transaction_type'], autopct='%1.1f%%', startangle=140)
    ax.set_title(title_pie)
    st.pyplot(fig)

# Hàm tạo biểu đồ 3: Sản lượng giao dịch theo khu vực và thời gian
def bieudo3(db):
    st.write("## Biểu đồ 2: Sản lượng giao dịch theo thời gian")
    query_region = "SELECT DISTINCT RegionName FROM Transaction_Count_By_Month"
    df_region = pd.read_sql(query_region, db)
    st.write("### Danh sách khu vực", df_region)
    
    choice = st.selectbox("Chọn lọc theo", ["Khu vực", "Thời gian", "Thời gian không khu vực"])
    
    if choice == 'Khu vực':
        region_options = ["Tất cả"] + df_region['RegionName'].tolist()
        selected_region_name = st.selectbox("Chọn khu vực", region_options)
        
        if selected_region_name == "Tất cả":
            query_transactions = """
            SELECT TransactionMonth, SUM(TotalTransactions) AS TotalTransactions
            FROM Transaction_Count_By_Month
            GROUP BY TransactionMonth
            ORDER BY TransactionMonth;
            """
            title = 'Sản lượng giao dịch theo thời gian (Tất cả khu vực)'
        else:
            query_transactions = f"""
            SELECT TransactionMonth, SUM(TotalTransactions) AS TotalTransactions
            FROM Transaction_Count_By_Month
            WHERE RegionName = '{selected_region_name}'
            GROUP BY TransactionMonth
            ORDER BY TransactionMonth;
            """
            title = f'Sản lượng giao dịch tại khu vực {selected_region_name} theo thời gian'
    
    elif choice == 'Thời gian':
        start_date = st.date_input("Ngày bắt đầu")
        end_date = st.date_input("Ngày kết thúc")
        region_options = ["Tất cả"] + df_region['RegionName'].tolist()
        selected_region_name = st.selectbox("Chọn khu vực", region_options)
        
        if selected_region_name == "Tất cả":
            query_transactions = f"""
            SELECT TransactionMonth, SUM(TotalTransactions) AS TotalTransactions
            FROM Transaction_Count_By_Month
            WHERE TransactionMonth BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY TransactionMonth
            ORDER BY TransactionMonth;
            """
            title = f'Sản lượng giao dịch từ {start_date} đến {end_date} (Tất cả khu vực)'
        else:
            query_transactions = f"""
            SELECT TransactionMonth, SUM(TotalTransactions) AS TotalTransactions
            FROM Transaction_Count_By_Month
            WHERE RegionName = '{selected_region_name}' 
              AND TransactionMonth BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY TransactionMonth
            ORDER BY TransactionMonth;
            """
            title = f'Sản lượng giao dịch tại khu vực {selected_region_name} từ {start_date} đến {end_date}'
    
    else:  # 'Thời gian không khu vực'
        start_date = st.date_input("Ngày bắt đầu")
        end_date = st.date_input("Ngày kết thúc")
        query_transactions = f"""
        SELECT TransactionMonth, SUM(TotalTransactions) AS TotalTransactions
        FROM Transaction_Count_By_Month
        WHERE TransactionMonth BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY TransactionMonth
        ORDER BY TransactionMonth;
        """
        title = f'Sản lượng giao dịch từ {start_date} đến {end_date} (Không lọc theo khu vực)'
    
    # Thực thi truy vấn và xử lý dữ liệu
    df_transactions = pd.read_sql(query_transactions, db)

    # Loại bỏ các hàng có giá trị None hoặc NaN
    df_transactions = df_transactions.dropna(subset=['TransactionMonth', 'TotalTransactions'])

    # Vẽ biểu đồ
    fig, ax = plt.subplots()
    ax.plot(df_transactions['TransactionMonth'], df_transactions['TotalTransactions'], marker='o', linestyle='-')
    ax.set_title(title)
    ax.set_xlabel('Tháng')
    ax.set_ylabel('Số lượng giao dịch')
    ax.set_xticks(df_transactions['TransactionMonth'])
    ax.set_xticklabels(df_transactions['TransactionMonth'], rotation=45, ha='right')
    st.pyplot(fig)


# Hàm tạo biểu đồ 4: Bất động sản chưa bán và chưa thuê
# Hàm tạo biểu đồ 4: Bất động sản chưa bán và chưa thuê
def bieudo4(db):
    st.write("## Biểu đồ 3: Bất động sản chưa bán và chưa thuê")
    query_region = "SELECT DISTINCT Region AS region_name FROM Unsold_Unrented_RealEstate"
    df_region = pd.read_sql(query_region, db)
    st.write("### Danh sách khu vực", df_region)
    
    choice = st.selectbox("Chọn lọc theo", ["Khu vực", "Phân khúc"])
    
    if choice == 'Khu vực':
        region_options = ["Tất cả"] + df_region['region_name'].tolist()
        selected_region_name = st.selectbox("Chọn khu vực", region_options)
        
        if selected_region_name == "Tất cả":
            query_unsold_rented = """
            SELECT Segment, SUM(TotalUnsold) AS TotalUnsold, SUM(TotalUnrented) AS TotalUnrented
            FROM Unsold_Unrented_RealEstate
            GROUP BY Segment;
            """
            x_column = 'Segment'
            title = 'Bất động sản chưa bán và chưa thuê tại tất cả khu vực'
        else:
            query_unsold_rented = f"""
            SELECT Segment, TotalUnsold, TotalUnrented
            FROM Unsold_Unrented_RealEstate
            WHERE Region = '{selected_region_name}';
            """
            x_column = 'Segment'
            title = f'Bất động sản chưa bán và chưa thuê tại khu vực {selected_region_name}'
    else:
        selected_segment = st.text_input("Nhập tên phân khúc")
        if selected_segment:
            query_unsold_rented = f"""
            SELECT Region, TotalUnsold, TotalUnrented
            FROM Unsold_Unrented_RealEstate
            WHERE Segment = '{selected_segment}';
            """
            x_column = 'Region'
            title = f'Bất động sản chưa bán và chưa thuê trong phân khúc {selected_segment}'
        else:
            st.warning("Vui lòng nhập tên phân khúc.")
            return
        
    df_unsold_rented = pd.read_sql(query_unsold_rented, db)

    # Tăng kích thước biểu đồ để có thêm không gian
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Vẽ biểu đồ đường cho số lượng bất động sản chưa bán và chưa thuê
    ax.plot(df_unsold_rented[x_column], df_unsold_rented['TotalUnsold'], marker='o', linestyle='-', label='Chưa bán')
    ax.plot(df_unsold_rented[x_column], df_unsold_rented['TotalUnrented'], marker='o', linestyle='-', label='Chưa thuê')
    
    ax.set_title(title)
    ax.set_xlabel(x_column)
    ax.set_ylabel('Số lượng bất động sản')
    ax.legend()

    # Xoay nhãn trục x nếu lựa chọn là "Phân khúc"
    if x_column == 'Region':
        ax.set_xticks(range(len(df_unsold_rented[x_column])))
        ax.set_xticklabels(df_unsold_rented[x_column], rotation=90, ha='right')
    else:
        ax.set_xticks(range(len(df_unsold_rented[x_column])))
        ax.set_xticklabels(df_unsold_rented[x_column])

    # Hiển thị biểu đồ
    st.pyplot(fig)



# Hàm tạo biểu đồ 5: Giá thuê trung bình theo khu vực
def bieudo5(db):
    st.write("## Biểu đồ 4: Giá thuê trung bình")
    choice = st.selectbox("Chọn lọc theo", ["Thành phố", "Phân khúc"])
    
    if choice == 'Thành phố':
        city = st.text_input("Nhập tên thành phố")
        query_average_rent_city = f"""
        SELECT Region AS KhuVuc, AVG(AverageRentalPrice) AS GiaThueTrungBinh
        FROM RealEstate_Segment
        WHERE City = '{city}'
        GROUP BY Region;
        """
        df_average_rent = pd.read_sql(query_average_rent_city, db)
    else:
        segment = st.text_input("Nhập tên phân khúc")
        city = st.text_input("Nhập tên thành phố")
        query_average_rent_segment_city = f"""
        SELECT Region AS KhuVuc, AVG(AverageRentalPrice) AS GiaThueTrungBinh
        FROM RealEstate_Segment
        WHERE City = '{city}' AND Segment = '{segment}'
        GROUP BY Region;
        """
        df_average_rent = pd.read_sql(query_average_rent_segment_city, db)
    
    fig, ax = plt.subplots(figsize=(20, 12))
    bars = ax.bar(df_average_rent['KhuVuc'], df_average_rent['GiaThueTrungBinh'], color='skyblue')
    ax.set_title(f'Giá thuê trung bình tại {city}')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,.0f}', ha='center', va='bottom')
    # Thiết lập nhãn trục x để không chồng lên nhau
    ax.set_xticks(range(len(df_average_rent['KhuVuc'])))
    ax.set_xticklabels(df_average_rent['KhuVuc'], rotation=45, ha='right')
    st.pyplot(fig)

# Hàm tạo biểu đồ 6: Giá bán trung bình theo khu vực
def bieudo6(db):
    st.write("## Biểu đồ 6: Giá bán trung bình")
    choice = st.selectbox("Chọn lọc theo", ["Thành phố", "Phân khúc"])
    
    if choice == 'Thành phố':
        city = st.text_input("Nhập tên thành phố")
        query_average_sale_city = f"""
        SELECT Region AS KhuVuc, AVG(AverageSellingPrice) AS GiaBanTrungBinh
        FROM RealEstate_Segment
        WHERE City = '{city}'
        GROUP BY Region;
        """
        df_average_sale = pd.read_sql(query_average_sale_city, db)
    else:
        segment = st.text_input("Nhập tên phân khúc")
        city = st.text_input("Nhập tên thành phố")
        query_average_sale_segment_city = f"""
        SELECT Region AS KhuVuc, AVG(AverageSellingPrice) AS GiaBanTrungBinh
        FROM RealEstate_Segment
        WHERE City = '{city}' AND Segment = '{segment}'
        GROUP BY Region;
        """
        df_average_sale = pd.read_sql(query_average_sale_segment_city, db)
    
    fig, ax = plt.subplots(figsize=(20, 12))
    bars = ax.bar(df_average_sale['KhuVuc'], df_average_sale['GiaBanTrungBinh'], color='salmon')
    ax.set_title(f'Giá bán trung bình tại {city}')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,.0f}', ha='center', va='bottom')
    # Thiết lập nhãn trục x để không chồng lên nhau
    ax.set_xticks(range(len(df_average_sale['KhuVuc'])))
    ax.set_xticklabels(df_average_sale['KhuVuc'], rotation=45, ha='right')
    st.pyplot(fig)

# Thiết lập giao diện Streamlit
st.title("Ứng dụng Phân tích Bất Động Sản")
db = connect_db()

# Giao diện lựa chọn loại biểu đồ
option = st.sidebar.selectbox(
    "Chọn loại biểu đồ bạn muốn xem",
    ("Biểu đồ 1: Phân khúc bất động sản (Cột)",
     "Biểu đồ 2: Tỷ lệ cho thuê và bán (Tròn)",
     "Biểu đồ 3: Sản lượng giao dịch",
     "Biểu đồ 4: Bất động sản chưa bán và chưa thuê",
     "Biểu đồ 5: Giá thuê trung bình",
     "Biểu đồ 6: Giá bán trung bình")
)

# Gọi các hàm để hiển thị biểu đồ dựa trên lựa chọn
if option == "Biểu đồ 1: Phân khúc bất động sản (Cột)":
    bieudo1(db)
elif option == "Biểu đồ 2: Tỷ lệ cho thuê và bán (Tròn)":
    bieudo2(db)
elif option == "Biểu đồ 3: Sản lượng giao dịch":
    bieudo3(db)
elif option == "Biểu đồ 4: Bất động sản chưa bán và chưa thuê":
    bieudo4(db)
elif option == "Biểu đồ 5: Giá thuê trung bình":
    bieudo5(db)
elif option == "Biểu đồ 6: Giá bán trung bình":
    bieudo6(db)


# Đóng kết nối
db.close()
