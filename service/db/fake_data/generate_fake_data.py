import csv
import os
import random


def generate_data_for(file_name, data_dic, field_names):
    current_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_path, file_name)
    with open(file_path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data_dic)

def generate_fake_data(fields):
    data_dic_list = []
    for count in range(random.randint(0, 20)):
        data_dic = {}
        for field in fields:
            data_dic[field] = "{}_test_{}".format(field, count) if "number" not in field else count
        data_dic_list.append(data_dic)
    return data_dic_list


# store_fields = ["store_number", "phone_number", "street_address", "city_name", "state"]
# fake_data_list = generate_fake_data(store_fields)
# generate_data_for("Store.csv", fake_data_list, store_fields)

def generate_fake_data_manufacturer():
    manufacturer_fields = ["manufacturer_name", "max_discount"]
    data_dic_list = []
    for count in range(0, 20):
        data_dic = {}
        for field in manufacturer_fields:
            data_dic[field] = "{}_test_{}".format(field, count) if "max_discount" != field else count / 100.0
        data_dic_list.append(data_dic)
    generate_data_for("Manufacturer.csv", data_dic_list, manufacturer_fields)

def generate_fake_data_date():
    date_fields = ["dateID", "date_time"]
    data_dic_list = []
    month_day_dict = {"1": 31, "3": 31, "5": 31, "7": 31, "9": 30, "11": 30,
                      "4": 30, "6": 30, "8": 31, "10": 31, "12": 31, "2": 28}
    count = 0
    year = "0000"
    # for year in range(1970, 2100):
    for month in range(1, 13):
        for day in range(1, month_day_dict[str(month)] + 1):
            data_dict = {}
            data_dict["dateID"] = count
            data_dict["date_time"] = "{}-{}-{}".format(year, month, day)
            data_dic_list.append(data_dict)
            count += 1
    generate_data_for("Date.csv", data_dic_list, date_fields)

def generate_fake_data_holiday():
    fields = ["dateID", "holiday_name"]
    data_dic_list = []
    holidays = {"0000-10-31": "Halloween",
                "0000-11-26": "Thanksgiving Day"}
    with open('Date.csv', 'r') as searchfile:
        for line in searchfile:
            if "," in line:
                date_id, date_time = line.replace("\n", "").split(",")
                if date_time in holidays:
                    data_dic_list.append({"dateID": date_id, "holiday_name": holidays[date_time]})
    generate_data_for("Holiday.csv", data_dic_list, fields)


# generate_fake_data_date()
# generate_fake_data_manufacturer()
generate_fake_data_holiday()

