import json
import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

#--------------functions--------------------
def isEmpty(user,pas):
    if user=='' or pas=='':
        return True
    else:
        return False
def checkInfo(user,pas=False):
    if pas:
        sql=f'''SELECT * FROM users WHERE username="{user}" AND password="{pas}" '''
    else:
        sql = f'''SELECT * FROM users WHERE username="{user}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    if len(rows)<1:
        return False
    else:
        return True
def setting():

    with open ('setting.json')as f:
        gDct=json.load(f)
    gNumber = gRead()
    gList=list(gDct.keys())

    if gNumber>=int(gList[0]) and gNumber<int(gList[1]):
        btnSearch.configure(state='disabled')
    else:
        return True



def login():

    global session
    user=txtUser.get()
    pas=txtPas.get()
    if isEmpty(user,pas):
        lblMsg.configure(text='empty fields error!!!',fg='red')
        return
    if checkInfo(user,pas):
        lblMsg.configure(text='Welcome To your Account!',fg='green')
        session=user
        txtUser.delete(0,'end')
        txtPas.delete(0,'end')
        txtUser.configure(state='disabled')
        txtPas.configure(state='disabled')
        btnLogin.configure(state='disabled')
        btnDel.configure(state='active')
        btnShop.configure(state='active')
        btnMycart.configure(state='active')
        btnSearch.configure(state='active')
        setting()
    else:
        lblMsg.configure(text='Wrong Username Or Password', fg='red')

def signup():
    def signupValidate(user,pas,cpas):
        if user=='' or pas=='' or cpas=='':
            return False,'Empty Fields Error!'
        if pas!=cpas:
            return False,'password and confirmation mismatch!'
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', pas):
            return False,'password Minimum eight chars,at least one letter and one number'
        if checkInfo(user):
            return False,'Username Already Exist!!'
        return  True,''

    def save2users(user,pas):
        try:
            sql=f'INSERT INTO users (username,password,grade) VALUES ("{user}","{pas}",0)'
            cnt.execute(sql)
            cnt.commit()
            return True
        except:
            return False
    def submit():
        user=txtUser.get()
        pas=txtPas.get()
        cpas=txtCpas.get()
        result,errorMSG=signupValidate(user,pas,cpas)
        if not result:
            lblMsg.configure(text=errorMSG,fg='red')
            return
        result=save2users(user,pas)
        if not result:
            lblMsg.configure(text='something went wrong during database connection!!',fg='red')
            return
        lblMsg.configure(text='submit done successfully!',fg='green')
        txtUser.delete(0,'end')
        txtPas.delete(0, 'end')
        txtCpas.delete(0, 'end')
    winSignup=tk.Toplevel(win)
    winSignup.title('Signup Panel')
    winSignup.geometry('300x300')
    lblUser = tk.Label(winSignup, text='Username:')
    lblUser.pack()
    txtUser = tk.Entry(winSignup)
    txtUser.pack()
    lblPas = tk.Label(winSignup, text='Password:')
    lblPas.pack()
    txtPas = tk.Entry(winSignup)
    txtPas.pack()
    lblCpas = tk.Label(winSignup, text='Password confirmation:')
    lblCpas.pack()
    txtCpas = tk.Entry(winSignup)
    txtCpas.pack()
    lblMsg = tk.Label(winSignup, text='')
    lblMsg.pack()
    btnSubmit = tk.Button(winSignup, text='Submit',command=submit)
    btnSubmit.pack()
    winSignup.mainloop()

def delAccount():
    global session
    result=messagebox.askyesno(title='Confirm',message='Are You Sure?')
    if not result:
        lblMsg.configure(text='Operation Canceled By User!',fg='red')
        return
    result=delUser(session)
    if not result:
        lblMsg.configure(text='something went wrong during database connection!!', fg='red')
        return
    lblMsg.configure(text='account deleted successfully!',fg='green')
    btnDel.configure(state='disabled')
    btnLogin.configure(state='active')
    txtUser.configure(state='normal')
    txtPas.configure(state='normal')
    session=''
def delUser(user):
    try:
        sql=f'DELETE FROM users WHERE username="{user}"'
        cnt.execute(sql)
        cnt.commit()
        return True
    except:
        return False

def getProducts():
    sql="SELECT * FROM products"
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows
def fetch(sql):
    result = cnt.execute(sql)
    rows = result.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False
def idExist(pId):
    sql=f"SELECT * FROM products WHERE id={int(pId)}"
    return fetch(sql)

def enoughProducts(pid,num):
    sql=f'''SELECT * FROM products WHERE id={int(pid)} AND quantity>={int(num)} '''
    return fetch(sql)
def getId(user):
    sql=f'''SELECT id FROM users WHERE username="{user}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows[0][0]

def search():

    def Psearch():
        search=txtSearch.get()
        if search=='':
            return
        searchBox.delete(0,'end')
        sql = f''' SELECT * FROM products WHERE pname LIKE '%{search}%' '''
        result = cnt.execute(sql)
        rows = result.fetchall()

        for product in rows:
            item = f'''Id={product[0]} , Name={product[1]} , Price={product[2]} , QNT={product[3]}'''
            searchBox.insert('end', item)

    winSearch=tk.Toplevel(win)
    winSearch.title('Search')
    winSearch.geometry('600x400')
    lblSearch=tk.Label(winSearch,text='Search:')
    lblSearch.pack()
    txtSearch=tk.Entry(winSearch)
    txtSearch.pack()
    btnOk=tk.Button(winSearch,text='Ok',command=Psearch)
    btnOk.pack()
    searchBox= tk.Listbox(winSearch, width=80)
    searchBox.pack()

    btnBuy = tk.Button(winSearch, text='Buy!',command=shopPanel)

    btnBuy.pack()

    winSearch.mainloop()
def gRead():
    global session
    id = getId(session)
    sql = f''' SELECT * FROM users WHERE id={id}'''
    result = cnt.execute(sql)
    rows = result.fetchall()
    gNumber = rows[0][3]
    return gNumber
def gUpdate(gNumber):
    global session
    id = getId(session)
    sql = f''' UPDATE users SET grade={int(gNumber)} WHERE id={id}'''
    cnt.execute(sql)
    cnt.commit()
def grade():
    gNumber=gRead()
    gNumber+=1
    gUpdate(gNumber)





def shopPanel():
    def discont():
        global session
        id = getId(session)
        gNumber = gRead()
        if gNumber < 3:
            lblmsg3.configure(text='your buy doesnt have discont!',fg='red')
        elif gNumber < 10 and gNumber > 3 :
            lblmsg3.configure(text='your buy has 5% discont!',fg='green')
        elif gNumber>10:
            lblmsg3.configure(text=' your buy has 10% discont!', fg='green')


    def save2cart(pId,pNumber):
        discont()
        grade()
        try:
            global session
            id=getId(session)
            sql=f'''INSERT INTO cart (uid,pid,number) VALUES ({id},{int(pId)},{int(pNumber)})'''
            cnt.execute(sql)
            cnt.commit()
            return True
        except:
            return False

    def updateQNT(pId,pNumber):
        try:
            pNumber=int(pNumber)
            pId=int(pId)
            sql=f'''UPDATE products SET quantity=quantity-{pNumber} WHERE id={pId}'''
            cnt.execute(sql)
            cnt.commit()
            return True,''
        except Exception as e:
            return False,e

    def buy():
        pId=txtid.get()
        pNumber=txtqnt.get()
        if pId=='' or pNumber=='':
            lblmsg2.configure(text='Fill the blanks!',fg='red')
            return
        if (not pId.isdigit()) or (not(pNumber.isdigit())):
            lblmsg2.configure(text='Invalid input!', fg='red')
            return
        if not idExist(pId):
            lblmsg2.configure(text='Wrong Product Id!', fg='red')
            return
        if not enoughProducts(pId,pNumber):
            lblmsg2.configure(text='Not enough Products!', fg='red')
            return
        result,msg=updateQNT(pId,pNumber)
        if not result:
            lblmsg2.configure(text=f'ERROR while connecting database=>\n{msg}', fg='red')
            return
        result=save2cart(pId,pNumber)
        if not result:
            lblmsg2.configure(text='ERROR while connecting database', fg='red')
            return
        lblmsg2.configure(text='products saved to your cart!',fg='green')
        txtid.delete(0,'end')
        txtqnt.delete(0,'end')
        lstBox.delete(0,'end')
        products = getProducts()
        for product in products:
            item = f'''Id={product[0]} , Name={product[1]} , Price={product[2]} , QNT={product[3]}'''
            lstBox.insert('end', item)
    winShop=tk.Toplevel(win)
    winShop.title('Shop Panel')
    winShop.geometry('500x400')
    lstBox=tk.Listbox(winShop,width=80)
    lstBox.pack()
    lblid=tk.Label(winShop,text='Id:')
    lblid.pack()
    txtid=tk.Entry(winShop)
    txtid.pack()
    lblqnt = tk.Label(winShop, text='numbers:')
    lblqnt.pack()
    txtqnt = tk.Entry(winShop)
    txtqnt.pack()
    lblmsg2=tk.Label(winShop,text='')
    lblmsg2.pack()
    lblmsg3 = tk.Label(winShop, text='')
    lblmsg3.pack()
    btnBuy=tk.Button(winShop,text='Buy!',command=buy)
    btnBuy.pack()
    products=getProducts()
    for product in products:
        item=f'''Id={product[0]} , Name={product[1]} , Price={product[2]} , QNT={product[3]}'''
        lstBox.insert('end',item)
    winShop.mainloop()

def showCart():
    def getMycart():
        global session
        id=getId(session)
        sql=f'''
                SELECT products.pname,products.price,cart.number
                FROM cart INNER JOIN products
                ON cart.pid=products.id
                WHERE cart.uid={id}
            '''
        result=cnt.execute(sql)
        rows=result.fetchall()
        return rows
    winCart=tk.Toplevel(win)
    winCart.title('Cart Panel')
    winCart.geometry('400x400')
    lstbox2=tk.Listbox(winCart,width=80)
    lstbox2.pack()
    cart=getMycart()
    for product in cart:
        text=f'Name:{product[0]}  Number:{product[2]}  Total price:{product[1]*product[2]} '
        lstbox2.insert(0,text)
    winCart.mainloop()


#-------------- database codes ---------------
cnt=sqlite3.connect('shop.db')
# sql='''CREATE TABLE users (
#         id INTEGER PRIMARY KEY,
#         username VARCHAR(30) NOT NULL,
#         password VARCHAR(30) NOT NULL,
#         grade INTEGER NOT NULL
#         )'''
# cnt.execute(sql)

# sql='''INSERT INTO users (username,password,grade)
#         VALUES('admin','123456789',0)'''
# cnt.execute(sql)
# cnt.commit()

# sql='''CREATE TABLE products (
#         id INTEGER PRIMARY KEY,
#         pname VARCHAR(50) NOT NULL,
#         price REAL NOT NULL,
#         quantity INTEGER NOT NULL,
#         date VARCHAR
#         )'''
# cnt.execute(sql)
# sql='''INSERT INTO products (pname,price,quantity)
#         VALUES('PHONE SAMSUNG MODEL: A20','12000000',180)'''
# cnt.execute(sql)
# cnt.commit()


# sql='''CREATE TABLE cart (
#         id INTEGER PRIMARY KEY,
#         uid INTEGER NOT NULL,
#         pid INTEGER NOT NULL,
#         number INTEGER NOT NULL
#         )'''
# cnt.execute(sql)



#---------------- main -----------------------
session=''
win=tk.Tk()
win.title('Shop Project')
win.geometry('400x400')
lblUser=tk.Label(win,text='Username:')
lblUser.pack()
txtUser=tk.Entry(win)
txtUser.pack()
lblPas=tk.Label(win,text='Password:')
lblPas.pack()
txtPas=tk.Entry(win)
txtPas.pack()
lblMsg=tk.Label(win,text='')
lblMsg.pack()
btnLogin=tk.Button(win,text='Login',command=login)
btnLogin.pack()
btnSignup=tk.Button(win,text='Signup',command=signup)
btnSignup.pack()
btnDel=tk.Button(win,text='Delete Account!',state='disabled',command=delAccount)
btnDel.pack()
btnShop=tk.Button(win,text='Shop Panel',state='disabled',command=shopPanel)
btnShop.pack()
btnMycart=tk.Button(win,text='My Cart',state='disabled',command=showCart)
btnMycart.pack()
btnSearch=tk.Button(win,text='Search',state='disabled',command=search)
btnSearch.pack()

win.mainloop()