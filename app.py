from flask import Flask, jsonify, render_template, request
from service.db.sql_client import SqlClient
import atexit
from utils import is_valid_date

app = Flask(__name__)
sql_client = SqlClient.get_instance()


@app.route('/')
def hello_word():
    return render_template('index.html')


@app.route('/MainMenu')
def get_main_menu():
    return render_template('mainmenu.html', main_menu=True)


@app.route('/Stores')
def get_store_count():
    result = sql_client.fetch_data_with_command("select * from Store;")
    result_to_dic = [dict([("store_number", store_number), ('phone_number', phone_number), ('street_address', street_address), ('city_name', city_name), ('state', state)]) for store_number,phone_number,street_address,city_name,state in result]
    return jsonify(result_to_dic)

@app.route('/Stores_Count')
def get_store_total_count():
    result = sql_client.fetch_data_with_command("select count(store_number) as count_store from Store;")
    result_to_dic = [dict([("count_store", count_store)]) for count_store in result]
    return jsonify(result_to_dic)



@app.route('/Manufacturer')
def get_manufacturer_count():
    result = sql_client.fetch_data_with_command("select * from Manufacturer;")
    result_to_dic = [dict([("manufacturer_name", manufacturer_name), ("max_discount", max_discount)]) for manufacturer_name, max_discount in result]
    return jsonify(result_to_dic)

@app.route('/Manufacturer_Count')
def get_manufacturer_total_count():
    result = sql_client.fetch_data_with_command("select count(manufacturer_name) as count_manufacturer from Manufacturer;")
    result_to_dic = [dict([("count_manufacturer", count_manufacturer)]) for count_manufacturer in result]
    return jsonify(result_to_dic)

@app.route('/Product')
def get_products_count():
    result = sql_client.fetch_data_with_command("select PID, product_name, retail_price from Product;")
    result_to_dic = [dict([("PID", PID), ("product_name", product_name), ("retail_price", retail_price)]) for PID, product_name, retail_price in result]
    return jsonify(result_to_dic)

@app.route('/Product_Count')
def get_product_total_count():
    result = sql_client.fetch_data_with_command("select count(PID) as count_product from Product;")
    result_to_dic = [dict([("count_product", count_product)]) for count_product in result]
    return jsonify(result_to_dic)


@app.route('/MembershipsSold')
def get_memberships_count():
    result = sql_client.fetch_data_with_command("SELECT m.memberID AS MemberID, d.date_time AS SignupDate FROM Membership m, Date d WHERE m.signup_date=d.dateID;")
    result_to_dic = [dict([("MemberID", MemberID), ("SignupDate", SignupDate)]) for MemberID, SignupDate in result]
    return jsonify(result_to_dic)

@app.route('/Membership_Count')
def get_membership_total_count():
    result = sql_client.fetch_data_with_command("select count(memberID) as count_membership from Membership;")
    result_to_dic = [dict([("count_membership", count_membership)]) for count_membership in result]
    return jsonify(result_to_dic)

@app.route('/api/City-Info')
def get_city_information():
    result = sql_client.fetch_data_with_command("select * from City;")
    result_to_dic = [dict([("city_name", city_name), ("state", state), ("population", population)]) for city_name, state, population in result]
    return jsonify(result_to_dic)

@app.route('/api/City-CityList', methods=['GET', 'POST'])
def get_city_citylist():
    if request.method == 'GET':
        result = sql_client.fetch_data_with_command("SELECT city_name, state FROM City")
        result_to_dic = [dict([("city_name", city_name), ("state", state)]) for city_name, state in result]
        return jsonify(result_to_dic)
    if request.method == 'POST':
        print(request.get_json())
        return jsonify(success=True)

@app.route('/api/Update-City-Population', methods=['POST'])
def get_city_population_update():
    if request.method == 'POST':
        data = request.get_json()
        selectedState = data['selectedState']
        selectedCity = data['selectedCity']
        newCityPopulation = data['InputPopulation']
        if selectedState == 'State':
            return "Please Select City & State Information.", 500
        if newCityPopulation == '':
            return "Please Input New Population Data.", 500
        sql_client.exec_command(("UPDATE City SET population = '%s' WHERE city_name = '%s' AND state = '%s' ")%(newCityPopulation, selectedCity, selectedState))
        return jsonify(selectedState, selectedCity, newCityPopulation)

@app.route('/Holiday', methods=['GET', 'POST'])
def view_update_holidays():
    # GET request
    if request.method == 'GET':
        result = sql_client.fetch_data_with_command("select date_time, holiday_name "
                                                    "from Holiday, Date "
                                                    "where Holiday.dateID = Date.dateID;")
        result_to_dic = [dict([("date_time", date_time.strftime("%Y-%m-%d")), ("holiday_name", holiday_name)]) for date_time, holiday_name in result]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        data = request.get_json()
        if is_valid_date(month=data["month"], day=data["day"]) is False:
            return "invalid date."
        # operations if user click add holiday button
        if data["mode"] == "add":
            sql_command = "select dateID, date_time from Date where date_time=\"{}-{}-{}\";".format(data["year"], data["month"], data["day"])
            result = sql_client.fetch_data_with_command(sql_command)
            date_id, date_time = result[0]
            if len(sql_client.fetch_data_with_command("select dateID from Holiday where dateID={};".format(date_id))) > 0:
                return 'Already has this date.', 500
            sql_client.exec_command("insert into Holiday(dateID, holiday_name) values ({},\'{}\');".format(date_id, data["holiday_name"]))
            return jsonify(success=True)
        # operations if user click update holiday button
        elif data["mode"] == "update":
            sql_command = "select dateID, date_time from Date where date_time=\"{}-{}-{}\";".format(data["year"], data["month"], data["day"])
            result = sql_client.fetch_data_with_command(sql_command)
            date_id, date_time = result[0]
            if len(sql_client.fetch_data_with_command(
                    "select dateID from Holiday where dateID={};".format(date_id))) == 0:
                return 'Does not has this date in database.', 500
            sql_client.exec_command(
                "update Holiday set holiday_name=\'{}\' where dateID={};".format(data["holiday_name"], date_id))
            return jsonify(success=True)
        # operations if user click delete holiday button
        elif data["mode"] == "delete":
            sql_command = "select dateID, date_time from Date where date_time=\"{}-{}-{}\";".format(data["year"], data["month"], data["day"])
            result = sql_client.fetch_data_with_command(sql_command)
            date_id, date_time = result[0]
            if len(sql_client.fetch_data_with_command(
                    "select dateID from Holiday where dateID={};".format(date_id))) == 0:
                return 'Does not has this date in database.', 500
            sql_client.exec_command(
                "delete from Holiday where dateID={};".format(date_id))
            return jsonify(success=True)


@app.route('/Report1')
def get_report1():
    return render_template('report1.html', report1=True)


@app.route('/api/Report1-Table1', methods=['GET', 'POST'])
def get_report1_table1():
    # GET request
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("SELECT m.manufacturer_name AS ManufacturerName,  count(p.PID) AS ProductCount,  round(avg(p.retail_price),2) AS AvgRetailPrice,  min(p.retail_price) AS MinRetailPrice, max(p.retail_price) AS MaxRetailPrice FROM cs6400.Manufacturer m  INNER JOIN cs6400.Product p  ON m.manufacturer_name = p.manufacturer_name GROUP BY m.manufacturer_name ORDER BY avg(p.retail_price) DESC LIMIT 100;")
        result_to_dic = [dict([("ManufacturerName", ManufacturerName), ("ProductCount", ProductCount), ("AvgRetailPrice", AvgRetailPrice), ("MinRetailPrice", MinRetailPrice), ("MaxRetailPrice", MaxRetailPrice)]) for ManufacturerName, ProductCount, AvgRetailPrice, MinRetailPrice, MaxRetailPrice in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200


@app.route('/api/Report1-ManufacturerList', methods=['GET', 'POST'])
def get_report1_manufacturerlist():
    # GET request
    #result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT manufacturer_name FROM cs6400.Manufacturer;")
    #result_to_dic = [dict([("manufacturer_name", manufacturer_name)]) for manufacturer_name in result_sql]
    #print(result_to_dic)
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT manufacturer_name FROM cs6400.Manufacturer;")
        result_to_dic = [dict([("manufacturer_name", manufacturer_name)]) for manufacturer_name in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200


@app.route('/api/Report1-Table2', methods=['GET', 'POST'])
def get_report1_table2():
    if request.method == 'GET':
        selectedManufacturer = request.args.get('selected_manufacturer')
        result_sql = sql_client.fetch_data_with_command(("SELECT m.manufacturer_name AS ManufacturerName, m.max_discount AS MaxDiscount FROM cs6400.Manufacturer m WHERE m.manufacturer_name = '%s'")%(selectedManufacturer))
        result_to_dic = [dict([("ManufacturerName", ManufacturerName), ('MaxDiscount', MaxDiscount)]) for ManufacturerName, MaxDiscount in result_sql]
        return jsonify(result_to_dic)


@app.route('/api/Report1-Table3', methods=['GET', 'POST'])
def get_report1_table3():
    if request.method == 'GET':
        selectedManufacturer = request.args.get('selected_manufacturer')
        result_sql = sql_client.fetch_data_with_command(("""SELECT DISTINCT
                                                    m.manufacturer_name AS ManufacturerName,
                                                    m.max_discount AS MaxDiscount,
                                                    p.PID,
                                                    p.product_name AS ProductName,
                                                    p.retail_price AS RetailPrice,
                                                    c.category_name AS CategoryName
                                                    FROM cs6400.Manufacturer m
                                                    INNER JOIN cs6400.Product p
                                                    ON m.manufacturer_name = p.manufacturer_name
                                                    LEFT JOIN cs6400.CategorizedBy c
                                                    ON p.PID = c.PID
                                                    WHERE m.manufacturer_name = '%s'
                                                    ORDER BY p.retail_price DESC
                                                    """)%(selectedManufacturer))
        result_to_dic = [dict([("ManufacturerName", ManufacturerName), ("MaxDiscount", MaxDiscount), ("PID", PID), ("ProductName", ProductName), ("RetailPrice", RetailPrice), ("CategoryName", CategoryName)]) for ManufacturerName, MaxDiscount, PID, ProductName, RetailPrice, CategoryName in result_sql]
        return jsonify(result_to_dic)


@app.route('/Report2')
def get_report2():
    return render_template('report2.html', report2=True)


@app.route('/api/Report2-Table1', methods=['GET', 'POST'])
def get_report2_table1():
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("""SELECT
                                                    c.category_name AS CategoryName,
                                                    COUNT(p.PID) AS ProductCount,
                                                    COUNT(DISTINCT m.manufacturer_name) AS ManufacturerCount,
                                                    ROUND(AVG(p.retail_price),2) AS AvgRetailPrice
                                                    FROM cs6400.Category c
                                                    LEFT JOIN cs6400.CategorizedBy cb
                                                    ON c.category_name = cb.category_name
                                                    LEFT JOIN cs6400.Product p
                                                    ON cb.PID = p.PID
                                                    LEFT JOIN cs6400.Manufacturer m
                                                    ON p.manufacturer_name = m.manufacturer_name
                                                    GROUP BY c.category_name
                                                    ORDER BY c.category_name
                                                    """)
        result_to_dic = [dict([("CategoryName", CategoryName), ("ProductCount", ProductCount), ("ManufacturerCount", ManufacturerCount), ("AvgRetailPrice", AvgRetailPrice)]) for CategoryName, ProductCount, ManufacturerCount, AvgRetailPrice in result_sql]
        return jsonify(result_to_dic)


@app.route('/Report3')
def get_report3():
    return render_template('report3.html', report3=True)

@app.route('/api/Report3-Table1', methods=['GET', 'POST'])
def get_report3_table1():
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("""SELECT
                                                    Product.PID AS ProductID,
                                                    Product.product_name AS ProductName,
                                                    Product.retail_price AS RetailPrice,
                                                    SUM(Sold.quantity) AS UnitsEverSold,
                                                    SUM(CASE
                                                            WHEN OnSale.discount_percentage > 0 THEN Sold.quantity
                                                            ELSE 0
                                                        END
                                                    ) AS UnitSoldOnDiscount,
                                                    ROUND(SUM(Product.retail_price*(1.0-OnSale.discount_percentage)*Sold.quantity), 2) AS ActualRevenue,
                                                    ROUND(SUM(Product.retail_price*Sold.quantity), 2) AS PredictedRevenue,
                                                    ROUND(ABS(SUM(Product.retail_price*(1.0-OnSale.discount_percentage)*Sold.quantity) - SUM(Product.retail_price*Sold.quantity)), 2) AS RevenueDiff
                                                    FROM cs6400.Product
                                                    INNER JOIN cs6400.Sold ON Product.PID = Sold.PID
                                                    INNER JOIN cs6400.OnSale ON Product.PID=OnSale.PID AND Sold.dateID=OnSale.dateID
                                                    INNER JOIN cs6400.CategorizedBy ON CategorizedBy.PID=Product.PID
                                                    WHERE CategorizedBy.category_name="GPS"
                                                    GROUP BY Product.PID
                                                    HAVING RevenueDiff > 5000
                                                    ORDER BY RevenueDiff DESC
                                                    """)
        result_to_dic = [dict([("ProductID", ProductID), ("ProductName", ProductName), ("RetailPrice", RetailPrice), ("UnitsEverSold", int(UnitsEverSold)), ("UnitSoldOnDiscount", int(UnitSoldOnDiscount)), ("ActualRevenue", ActualRevenue), ("PredictedRevenue", PredictedRevenue), ("RevenueDiff", RevenueDiff)]) for ProductID,ProductName, RetailPrice, UnitsEverSold, UnitSoldOnDiscount, ActualRevenue, PredictedRevenue, RevenueDiff in result_sql]
        return jsonify(result_to_dic)

@app.route('/Report4')
def get_report4():
    return render_template('report4.html', report4=True)

@app.route('/api/Report4-StateList', methods=['GET', 'POST'])
def get_report4_statelist():
    # GET request
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT state FROM cs6400.City;")
        result_to_dic = [dict([("state", state)]) for state in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200


@app.route('/api/Report4-Table2', methods=['GET', 'POST'])
def get_report4_table2():
    if request.method == 'GET':
        selectedState = request.args.get('selected_state')
        result_sql = sql_client.fetch_data_with_command(("""SELECT
                                                Store.store_number AS StoreNumber,
                                                Store.street_address AS StreetAddress,
                                                Store.city_name AS CityName,
                                                EXTRACT(YEAR FROM Date.date_time) AS year_sold,
                                                ROUND(SUM(Sold.quantity*(1.0-OnSale.discount_percentage)*Product.retail_price), 2) AS revenue
                                                FROM cs6400.Store
                                                INNER JOIN cs6400.Sold ON Store.store_number=Sold.store_number
                                                INNER JOIN cs6400.Product ON Product.PID=Sold.PID
                                                INNER JOIN cs6400.Date ON Sold.dateID=Date.dateID
                                                INNER JOIN cs6400.OnSale ON OnSale.PID=Sold.PID
                                                WHERE Store.state='%s'
                                                GROUP BY StoreNumber, StreetAddress, CityName, year_sold
                                                ORDER BY year_sold ASC, revenue DESC
                                                """)%(selectedState))
        result_to_dic = [dict([("StoreNumber", StoreNumber), ('StreetAddress', StreetAddress), ('CityName', CityName), ('year_sold', year_sold), ('revenue', revenue)]) for StoreNumber, StreetAddress, CityName, year_sold, revenue in result_sql]
        return jsonify(result_to_dic)

@app.route('/Report5')
def get_report5():
    return render_template('report5.html', report5=True)

@app.route('/api/Report5-Table1', methods=['GET'])
def get_report5_table1():
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("""SELECT
                                                        YEAR(Date.date_time) AS year,
                                                        COUNT(DISTINCT Product.PID) AS totalPerYear,
                                                        SUM(Sold.quantity)/365 AS averagePerDay
                                                        FROM Sold
                                                        INNER JOIN Date ON Date.dateID = Sold.dateID
                                                        INNER JOIN Product ON Product.PID = Sold.PID
                                                        INNER JOIN CategorizedBy ON CategorizedBy.PID = Product.PID
                                                        INNER JOIN Category ON CategorizedBy.category_name = Category.category_name
                                                        WHERE Category.category_name = "Air Conditioner"
                                                        GROUP BY YEAR(Date.date_time)
                                                        ORDER BY YEAR(Date.date_time)
                                                        ;
                                                        """)
        result_to_dic = [dict([("Year", Year), ("totalPerYear", totalPerYear), ("averagePerDay", float(averagePerDay))]) for Year, totalPerYear, averagePerDay in result_sql]

        result_sql_2 = sql_client.fetch_data_with_command("""SELECT
                                                        SUM(Sold.quantity) AS soldOnGroundhogDay
                                                        FROM Sold
                                                        INNER JOIN Date ON Date.dateID = Sold.dateID
                                                        INNER JOIN Product ON Product.PID = Sold.PID
                                                        INNER JOIN CategorizedBy ON CategorizedBy.PID = Product.PID
                                                        INNER JOIN Category ON CategorizedBy.category_name = Category.category_name
                                                        WHERE Category.category_name = "Air Conditioner"
                                                        AND MONTH(Date.date_time) = 2
                                                        AND DAY(Date.date_time) = 2
                                                        GROUP BY YEAR(Date.date_time)
                                                        ORDER BY YEAR(Date.date_time)
                                                        ;
                                                        """)
        result_to_dic_2 = [dict([("soldOnGroundhogDay", int(soldOnGroundhogDay[0]))]) for soldOnGroundhogDay in result_sql_2]

        # Combined the two lists into one list
        result_dic = []
        for i in range(len(result_to_dic)):
            result_dic.append(dict(result_to_dic[i], **result_to_dic_2[i]))
        return jsonify(result_dic)

@app.route('/Report6')
def get_report6():
    return render_template('report6.html', report6=True)

@app.route('/Report6/view', methods=['POST'])
def get_report6_table():
    data = request.get_json()
    sql_command = "drop view if exists category_state_sold;"
    sql_client.exec_command(sql_command)
    sql_command = """
    create view category_state_sold as
    select distinct Category.category_name as category_name, Store.state as state, sum(Sold.quantity) as sold_quantity
    from Category
    join CategorizedBy on Category.category_name = CategorizedBy.category_name
    join Product on CategorizedBy.PID = Product.PID
    join Sold on Product.PID = Sold.PID
    join (select dateID from Date
          where Year(date_time) = {}
          and Month(date_time) = {}) as DateSelect
    on Sold.dateID = DateSelect.dateID
    join Store on Sold.store_number = Store.store_number
    group by Category.category_name, Store.state;""".format(data["year"], data["month"])
    sql_client.exec_command(sql_command)
    sql_command = """
    select t1.category_name, t1.state, t1.sold_quantity
    from category_state_sold as t1
    inner join ( select category_name, max(sold_quantity) as max_sold_quantity
           from category_state_sold
           group by category_name) as t2
    on t1.category_name = t2.category_name
    and t1.sold_quantity = t2.max_sold_quantity;"""
    result = sql_client.fetch_data_with_command(sql_command)
    result_to_dic = [dict([("category_name", category_name), ("state", state), ("sold_quantity", int(sold_quantity))]) for category_name, state, sold_quantity in result]
    return jsonify(result_to_dic)


@app.route('/Report7')
def get_report7():
    return render_template('report7.html', report7=True)


@app.route('/api/Report7-Table1', methods=['GET', 'POST'])
def get_report7_table1():
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("""SELECT CityCategory, YEAR(d.date_time) as Year, ROUND(AVG(p.retail_price * so.quantity * (1 - o.discount_percentage)),2) as Revenue
    FROM Store AS s
    JOIN (SELECT c.city_name, c.state,
     (CASE WHEN c.population < 3700000 THEN \"Small\" WHEN 3700000 <= c.population AND c.population < 6700000 THEN \"Medium\" WHEN 6700000 <= c.population AND c.population < 9000000 THEN \"Large\" ELSE \"Extra Large\" END) AS CityCategory FROM City AS c) AS cc ON cc.city_name = s.city_name
    JOIN Sold AS so ON s.store_number = so.store_number
    JOIN OnSale AS o ON so.PID = o.PID AND so.dateID = o.dateID
    JOIN Date AS d ON so.dateID = d.dateID
    JOIN Product AS p ON so.PID = p.PID
    GROUP BY CityCategory, YEAR(d.date_time)
    ORDER BY CityCategory, YEAR(d.date_time);""")
        result_to_dic = [dict([("CityCategory", CityCategory), ("Year", Year), ("Revenue", float(Revenue))]) for CityCategory, Year, Revenue in result_sql]
        return jsonify(result_to_dic)
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200





@app.route('/Report8')
def get_report8():
    return render_template('report8.html', report8=True)



@app.route('/api/Report8-Table1', methods=['GET', 'POST'])
def get_report8_table1():
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("""SELECT YEAR(d.date_time) AS Year, COUNT(m.memberID) AS CountMemberID
        FROM Membership AS m JOIN Date AS d ON m.signup_date = d.dateID GROUP BY YEAR(d.date_time)
        ORDER BY YEAR(d.date_time) DESC;""")
        result_to_dic = [dict([("Year", Year), ('CountMemberID', CountMemberID)]) for Year, CountMemberID in result_sql]
        return jsonify(result_to_dic)
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200



@app.route('/api/Report8-YearList', methods=['GET', 'POST'])
def get_report8_yearlist():
    # GET request
    #result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT YEAR(date_time) FROM cs6400.Date;")
    #result_to_dic = [dict([("Year", Year)]) for Year in result_sql]
    #print(result_to_dic)
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT YEAR(date_time) FROM cs6400.Date;")
        result_to_dic = [dict([("Year", Year)]) for Year in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200





@app.route('/api/Report8-Table2', methods=['GET', 'POST'])
def get_report8_table2():
    if request.method == 'GET':
        selectedYear = request.args.get('selected_year')
        selectedYear = int(selectedYear)
        result_sql = sql_client.fetch_data_with_command(("""SELECT s.city_name AS CityName, s.state AS State, COUNT(m.memberID) AS CountMember
    FROM Membership AS m JOIN Store AS s ON m.store_number = s.store_number JOIN City AS c ON s.city_name = c.city_name AND s.state = c.state
    JOIN Date AS d ON m.signup_date = d.dateID
    WHERE YEAR(d.date_time) = %i
    GROUP BY s.city_name, s.state
    ORDER BY COUNT(m.memberID) DESC
    LIMIT 25;""")%(selectedYear))
        result_to_dic = [dict([("CityName", CityName), ('State', State), ('CountMemberID', CountMemberID)]) for CityName, State, CountMemberID in result_sql]
    return jsonify(result_to_dic)


@app.route('/api/Report8-Table3', methods=['GET', 'POST'])
def get_report8_table3():
    if request.method == 'GET':
        selectedYear = request.args.get('selected_year')
        selectedYear = int(selectedYear)
        result_sql = sql_client.fetch_data_with_command(("""SELECT s.city_name AS CityName, s.state AS State, COUNT(m.memberID) AS CountMemberID
    FROM Membership AS m JOIN Store AS s ON m.store_number = s.store_number JOIN City AS c ON s.city_name = c.city_name AND s.state = c.state
    JOIN Date AS d ON m.signup_date = d.dateID
    WHERE YEAR(d.date_time) = %i
    GROUP BY s.city_name, s.state
    ORDER BY COUNT(m.memberID)
    LIMIT 25;""")%(selectedYear))
        result_to_dic = [dict([("CityName", CityName), ('State', State), ('CountMemberID', CountMemberID)]) for CityName, State, CountMemberID in result_sql]
    return jsonify(result_to_dic)



@app.route('/api/Report8-CityStateList', methods=['GET', 'POST'])
def get_report8_citylist():
    # GET request
    #result_sql = sql_client.fetch_data_with_command("SELECT DISTINCT YEAR(date_time) FROM cs6400.Date;")
    #result_to_dic = [dict([("Year", Year)]) for Year in result_sql]
    #print(result_to_dic)
    if request.method == 'GET':
        result_sql = sql_client.fetch_data_with_command("SELECT city_name, state FROM cs6400.City;")
        result_to_dic = [dict([("CityName", city_name), ("State", state)]) for city_name, state in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200



@app.route('/api/Report8-Table4', methods=['GET', 'POST'])
def get_report8_table4():
    if request.method == 'GET':
        selectedYear = int(request.args.get('selected_year'))
        selectedCityState = request.args.get('selected_citystate')
        selectedCityState = selectedCityState.split(', ')
        selectedCity = selectedCityState[0]
        selectedState = selectedCityState[1]
        result_sql = sql_client.fetch_data_with_command(("""SELECT COUNT(memberID) AS CountMemberID, s.city_name AS CityName, s.state AS State, s.store_number AS StoreNumber, s.street_address AS StreetAddress FROM Membership AS m JOIN Store AS s ON m.store_number = s.store_number JOIN (SELECT City.city_name, City.state FROM City JOIN Store ON City.city_name = Store.city_name AND City.state = Store.state GROUP BY City.city_name, City.state HAVING count(store_number) >= 2) AS cs
    ON s.city_name = cs.city_name AND s.state = cs.state
    JOIN Date AS d ON m.signup_date = d.dateID
    WHERE YEAR(d.date_time) = %i AND s.city_name = '%s' AND s.state = '%s'
    GROUP BY s.city_name, s.state, s.store_number, s.street_address;""")%(selectedYear, selectedCity, selectedState))
        result_to_dic = [dict([("CountMemberID", CountMemberID), ('CityName', CityName),('State', State), ('StoreNumber', StoreNumber), ('StreetAddress', StreetAddress)]) for CountMemberID, CityName, State, StoreNumber, StreetAddress in result_sql]
        return jsonify(result_to_dic)
    # POST request
    if request.method == 'POST':
        print(request.get_json()) # parse as JSON
        return 'Successs', 200

#defining function to run on shutdown
def close_running():
    print("closing sql connection.")
    sql_client.close_db_connection()


if __name__ == '__main__':
    sql_client.init_database(init_from_backup=True)
    #Register the function to be called on exit
    atexit.register(close_running)
    #get_report8_yearlist()
    app.run(debug=True, threaded=True)
