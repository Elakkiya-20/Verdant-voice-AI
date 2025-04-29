from flask import Flask, render_template, request, session, flash, send_file,jsonify

import mysql.connector

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Chat')
def Chat():
    return render_template('chat.html')


@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])

    print('User' + message)
    bot_response = english_bot.get_response(message)

    print(bot_response)

    print(bot_response.confidence)

    while True:
        if message == ("Soil") or message == ("soil"):
            bot_response = 'Soil Classification' + '<a href="http://127.0.0.1:5000/Soil">Submit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})
            break
        if message == ("Pest") or message == ("pest"):
            bot_response = 'Pest Classification' + '<a href="http://127.0.0.1:5000/FSearchP">Submit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})
            break

        if bot_response.confidence > 0.5:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})



        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break



        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})

    # return render_template("index.html")


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/FarmerLogin')
def FarmerLogin():
    return render_template('FarmerLogin.html')


@app.route('/CustomerLogin')
def CustomerLogin():
    return render_template('CustomerLogin.html')


@app.route('/NewCustomer')
def NewCustomer():
    return render_template('NewCustomer.html')


@app.route('/NewFarmer')
def NewFarmer():
    return render_template('NewFarmer.html')


@app.route("/ANewMachine")
def ANewMachine():
    return render_template('ANewMachine.html')


@app.route("/ANewProduct")
def ANewProduct():
    return render_template('ANewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AFarmerInfo")
def AFarmerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb  ")
    data = cur.fetchall()
    return render_template('AFarmerInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/anewproduct", methods=['GET', 'POST'])
def anewproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']

        Disease = request.form['Disease']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO   protb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" +
            savename + "','leaf','" + Disease + "')")
        conn.commit()
        conn.close()

    flash('New Product Register successfully')
    return render_template('ANewProduct.html')


@app.route("/AMachineInfo")
def AMachineInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data1 = cur.fetchall()

    return render_template('AMachineInfo.html', data1=data1)


@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from mechinetb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Machine  info Remove Successfully!')
    return AMachineInfo()


@app.route("/APRemove")
def APRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from protb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')
    return AMachineInfo()


@app.route("/newfarmer", methods=['GET', 'POST'])
def newfarmer():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmertb VALUES ('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')
    return render_template('FarmerLogin.html')


@app.route("/flogin", methods=['GET', 'POST'])
def flogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['fname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from farmertb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('FarmerLogin.html')
        else:

            session['mob'] = data[2]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM farmertb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('FarmerHome.html', data=data)


@app.route("/FarmerHome")
def FarmerHome():
    fname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb where UserName='" + fname + "'  ")
    data = cur.fetchall()
    return render_template('FarmerHome.html', data=data)


@app.route("/FSearchM")
def FSearchM():
    return render_template('FSearchM.html')


@app.route("/fsm", methods=['GET', 'POST'])
def fsm():
    if request.method == 'POST':
        file = request.files['file']
        file.save('static/Out/Test.jpg')

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('Citrusmodel.h5')

        import numpy as np
        from keras.preprocessing import image

        test_image = image.load_img('static/Out/Test.jpg', target_size=(200, 200))

        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        print(result)
        pre = ''
        resu = ''

        if result[0][0] == 1:
            pre = "Citrus_Black_spot"

        elif result[0][1] == 1:
            pre = "Citrus_Canker"
        elif result[0][2] == 1:
            pre = "Citrus_Greening"
        elif result[0][3] == 1:
            pre = "Citrus_healthy"
        elif result[0][4] == 1:
            pre = "Citrus_Scab"

        sendmsg(session['mob'], "Prediction Result" + str(pre))

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where  Disease ='" + pre + "' and  Type='fruit'")
        data = cur.fetchall()
        return render_template('FSearchM.html', data=data)


@app.route("/Addm")
def Addm():
    id = request.args.get('id')
    session['mid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mechinetb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('FMachineBook.html', data=data)


@app.route("/FSearchP")
def FSearchP():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('FSearchP.html', data=data)


@app.route("/fsp", methods=['GET', 'POST'])
def fsp():
    if request.method == 'POST':
        file = request.files['file']
        file.save('static/Out/Test.jpg')

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('leafmodel.h5')

        import numpy as np
        from keras.preprocessing import image

        test_image = image.load_img('static/Out/Test.jpg', target_size=(200, 200))

        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        print(result)
        pre = ''
        resu = ''
        out =""

        if result[0][0] == 1:
            print("Citrus_Black_spot")
            out = "Citrus_Black_spot"
            pre = "You can reduce your risk by drinking plenty of water and making sure you use less than 2,300 mg of sodium a day"
        elif result[0][1] == 1:
            print("Citrus_canker")
            out = "Citrus_canker"
            pre = "Afinitor (Everolimus),Afinitor Disperz (Everolimus)"
        elif result[0][2] == 1:
            print("Citrus_greening")
            out = "Citrus_greening"
            pre = "You can reduce your risk by drinking plenty of water and making sure you use less than 2,300 mg of sodium a day"

        elif result[0][3] == 1:
            print("Citrus_healthy")
            out = "Citrus_healthy"

        elif result[0][4] == 1:
            print("Citrus_Melanose")
            out = "Citrus_Melanose"
            pre = "Use sprays containing organic copper compounds to treat D. citri. Initial application should take place at petal fall, followed by a secondary treatment 6-8 weeks later."

        elif result[0][5] == 1:
            print("Rice_Bacterial_leaf_blight")
            out = "Rice_Bacterial_leaf_blight"
            pre = "Bacterial blight can be severe in susceptible rice varieties under high nitrogen fertilization"

        elif result[0][6] == 1:
            print("Rice_Brown_spot")
            out = "Rice_Brown_spot"
            pre = "Always consider an integrated approach with both preventive measures and biological treatments if available. The best way to prevent the disease is to use fungicides (e.g., iprodione, propiconazole, azoxystrobin, trifloxystrobin) as seed treatments."
        elif result[0][7] == 1:
            print("Rice_Leaf_smut")
            out = "Rice_Leaf_smut"
            pre = "Cleaning up debris at the end of each growing season can prevent spread of leaf smut. Keeping a good nutrient balance is also important,"



        elif result[0][8] == 1:
            print("Tomato_Bacterial_spot")
            out = "Tomato_Bacterial_spot"
            pre = "Treat seeds with dilute bleach, hydrochloric acid, or hot water to reduce the potential for seedling infection"
        elif result[0][9] == 1:
            print("Tomato_Early_blight")
            out = "Tomato_Early_blight"
            pre = "Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable"
        elif result[0][10] == 1:
            print("Tomato_healthy")
            out = "Tomato_healthy"

        elif result[0][11] == 1:
            print("Tomato_Late_blight")
            out = "Tomato_Late_blight"
            pre = "Treat seeds with dilute bleach, hydrochloric acid, or hot water to reduce the potential for seedling infection"
        elif result[0][12] == 1:
            print("Tomato_Leaf_Mold")
            out = "Tomato_Leaf_Mold"
            pre = "Apply a fungicide according to the manufacturer’s instructions at the first sign of infectio"
        elif result[0][13] == 1:
            print("Tomato_Septoria_leaf_spot")
            out = "Tomato_Septoria_leaf_spot"
            pre = "One of the least toxic and most effective is chlorothalonil (sold under the names Fungonil and Daconil)"

        sendmsg(session['mob'], "Prediction Result" + str(out))

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where  Disease ='" + out + "'  and Type='leaf'")
        data = cur.fetchall()
        return render_template('FSearchP.html', data=data,res=out)


@app.route("/Addp")
def Addp():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('FAddCart.html', data=data)


@app.route("/Faddcart", methods=['GET', 'POST'])
def Faddcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['fname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            cQty = data[4]

            Image = data[6]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)

        clqty = float(cQty) - float(qty)

        if clqty < 0:
            flash('Low  Product ')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fcarttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','0','')")
            conn.commit()
            conn.close()

            flash('Add To Cart  Successfully')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('FAddCart.html', data=data)


@app.route("/FCart")
def FCart():
    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('FCart.html', data=data, tprice=tprice)


@app.route("/FRemoveCart")
def FemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from fcarttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('FCart.html', data=data, tprice=tprice)


@app.route("/fppayment", methods=['GET', 'POST'])
def fppayment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['fname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM fbooktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "update   fcarttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fbooktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()

    return FReport()


@app.route("/FReport")
def FReport():
    uname = session['fname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fbooktb where username='" + uname + "'")
    data2 = cur.fetchall()
    return render_template('FReport.html', data1=data1, data2=data2)


@app.route("/FNewProduct")
def FNewProduct():
    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
    data = cur.fetchall()
    return render_template('FNewProduct.html', data=data)


@app.route("/FSales")
def FSales():
    uname = session['fname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where fname='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()
    return render_template('FSales.html', data1=data1)


@app.route("/fnewproduct", methods=['GET', 'POST'])
def fnewproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']
        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        uname = session['fname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO   uprotb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" + savename + "','" + uname + "')")
        conn.commit()
        conn.close()

    flash('New Product Register successfully')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
    data = cur.fetchall()
    return render_template('FNewProduct.html', data=data)


@app.route("/FPRemove")
def FPRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from uprotb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')
    return FNewProduct()


@app.route("/newcust", methods=['GET', 'POST'])
def newcust():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('NewCustomer.html')


@app.route("/clogin", methods=['GET', 'POST'])
def clogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['cname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('CustomerLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('CustomerHome.html', data=data)


@app.route("/CustomerHome")
def CustomerHome():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('CustomerHome.html', data=data)


@app.route("/CSearch")
def CSearch():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb ")
    data = cur.fetchall()
    return render_template('CSearch.html', data=data)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM uprotb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('CSearch.html', data=data)


@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('AddCart.html', data=data)


@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['cname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM uprotb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            cQty = data[4]

            Image = data[6]
            fname = data[7]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)

        clqty = float(cQty) - float(qty)

        if clqty < 0:

            flash('Low  Product ')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM uprotb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','0','','" + fname + "')")
            conn.commit()
            conn.close()

            flash('Add To Cart  Successfully')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM uprotb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)


@app.route("/Cart")
def Cart():
    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['cname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "update   carttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


@app.route("/CBookInfo")
def CBookInfo():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


@app.route("/ABookingInfo")
def ABookingInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where   Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fbooktb ")
    data2 = cur.fetchall()
    return render_template('ABookingInfo.html', data1=data1, data2=data2)


@app.route("/ESalesInfo")
def ESalesInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2leafdiseasedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('ESalesInfo.html', data1=data1, data2=data2)


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
