import csv
import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="powerhf_pvtltd",
    user="postgres",
    password="Powerhf@123",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Path to your CSV file
csv_file = 'C:\ATC_data\project tracker.csv'
# csv_file = 'C:\ATC_data\Deaisel_filling_data.csv'
# csv_file = 'C:\ATC_data\s2\dup data\All Feb energy data.csv'
# csv_file = 'C:\ATC_data\s2\dup data\ATC odissa data march 2024.csv'

# For Energy Data:
# Open the CSV file and iterate over its rows to insert data into the database
# with open(csv_file, 'r') as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip the header row if it exists
#     for df in reader:
#         cur.execute(
#             '''INSERT INTO app_energyfuel 
#             ("Tasks", "DG_Serial_Number", "DG_HMR_Status", "DG_HMR_Reading", "DG_PIU_Status", "Current_DG_PIU_Reading", "Diesel_Filling_Done", 
#             "Date_Of_Diesel_Filling", "Diesel_Balance_Before_Filling", "Fuel_Qty_Filled", "Current_Diesel_Balance", "EB_Meter_Status", "Current_EB_MTR_KWH", 
#             "EB_PIU_Meter_Status", "Current_EB_PIU_Reading", "Total_DC_Load", "Total_EB_KWH_Reading_from_all_Channels", "Remarks", "FT_ID", "FT_name", 
#             "FT_mobile_no", "Receipt_No", "Card_Number", "Vehicle_Plate", "EB_Cumulative_KWH_Image", "EB_Running_Hours_Cumulative_Image", "DG_Running_Hours_Reading_Image",
#             "DG_Running_Hours_as_per_piu_Reading_Image", "Diesel_Bill_Number_Image", "DG_Running_HRS", "CPH_CPH_Comparison_With_Last_CPH", 
#             "CPH_as_par_HMR", "CPH_as_par_PIU","EB_KWH", "global_id_id") 
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
#             (df[0], df[1],df[2], df[3],df[4],df[5],df[6], df[7],df[8], df[9],df[10],df[11], df[12],df[13],df[14], df[15],df[16], df[17],
#              df[18],df[19],df[20],df[21],df[22], df[23],df[24],df[25], df[26], df[27], df[28], df[29], df[30], df[31], df[32], df[33], df[34])  # Adjust indices according to your CSV columns
#         )


# For Project Tracker Data:
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row if it exists
    for df in reader:
        cur.execute(
            '''INSERT INTO app_projectsmastermodel 
            ("site_id", "site_name", "customer", "project_type", "customer_expected_target_date", "assigned_to_asm", "sales_remark", "project_description", 
            "assigned_to_technician", "technician_target_date", "asm_remarks", "project_status", "completed_date", "technician_remarks", "pendings", "completed", 
            "user_id") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (df[0], df[1],df[2], df[3],df[4],df[5],df[6], df[7],df[8], df[9],df[10],df[11], df[12],df[13],df[14], df[15],df[16])  # Adjust indices according to your CSV columns
        )

# Commit the transaction
conn.commit()

# Close communication with the PostgreSQL database
cur.close()
conn.close()



