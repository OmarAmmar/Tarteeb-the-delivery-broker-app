import re
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import db
import random
import math

current_window = None
master = Tk()


class UserInterface(Frame):
    def __init__(self):

        Frame.__init__(self)

        self.frame6 = None
        self.Entry4 = None
        self.label5 = None
        self.frame5 = None
        self.Entry3 = None
        self.label4 = None
        self.frame4 = None
        self.UpgradeType = None
        self.label3 = None
        self.frame3 = None
        self.Entry2 = None
        self.Entry1 = None
        self.frame1 = None
        self.Delivery = None
        self.ConfirmButton = None
        self.LabelsButton = None
        self.Labels = None
        self.frame2 = None
        self.newWindow = None
        self.listbox = None
        self.scrollbar = None
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Tarteeb User Interface")

        ChoiceLabels = ['Make a new order', 'Cancel Previous Order', 'Upgrade account']

        self.label1 = Label(text=" Top Users of the platform")
        self.label1.pack(padx=5, pady=5)
        # TODO ::show a list of the top ten users
        topUsers = db.listTop10Users()
        print(topUsers)

        self.text = Text(current_window, width=30, height=15)
        self.text.pack()
        self.text.insert(END, "User\t\t\tPoints " + '\n')

        for j in range(len(topUsers)):
            if topUsers[j] is not None:
                text = "{} {}\t\t\t{}".format(topUsers[j][0], topUsers[j][1], topUsers[j][2])
                self.text.insert(END, text + '\n')

        # TODO:: Show the most ordered product on the platform
        self.label2 = Label(text="The most Ordered Product")
        self.label2.pack(padx=5, pady=5)

        mostOrdered = db.listMostPopularOrder()

        self.text1 = Text(current_window, width=10, height=1)
        self.text1.pack()
        self.text1.insert(END, "{}".format(mostOrdered[0]))

        button_frame = Frame()
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button1 = Button(button_frame, text=ChoiceLabels[0], command=self.CreateNewOrder)
        self.button1.grid(row=5, column=4, sticky=W + E + N + S)

        self.button2 = Button(button_frame, text=ChoiceLabels[1], command=self.CancelOrder)
        self.button2.grid(row=5, column=5, sticky=W + E + N + S)

        self.button3 = Button(button_frame, text=ChoiceLabels[2], command=self.UpgradeAccount)
        self.button3.grid(row=5, column=6, sticky=W + E + N + S)

    def CreateNewOrder(self):
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("New Order")

        self.newWindow.geometry("400x300")

        frame1 = Frame(self.newWindow)
        frame1.pack(padx=5, pady=5)

        # A Label widget to show in toplevel
        Label(frame1, text="Choose a restaurant / Shop:").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        self.listbox.bind("<MouseWheel>", lambda event: scrolllistbox(event, listbox))
        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        Shops = db.ViewAllShops()

        # Insert elements into the
        for i in range(len(Shops)):
            self.listbox.insert(END, Shops[i][0] + "," + Shops[i][1])

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        # Add the option for reservation , pick up or delivery
        frame3 = Frame(self.newWindow)
        frame3.pack(pady=5, padx=5)

        self.Labels = ["PICK UP", "DELIVERY", "RESERVATION"]
        self.Delivery = StringVar()
        for label in self.Labels:
            self.LabelsButton = Radiobutton(frame3,
                                            text=label, value=label, variable=self.Delivery)
            self.LabelsButton.pack(side=LEFT, padx=5, pady=5)

        frame2 = Frame(self.newWindow)
        frame2.pack(padx=5, pady=5)

        confirmButton = Button(frame2, text="Confirm Restaurant", command=self.SelectItems)
        confirmButton.pack(anchor=W, side=LEFT)

        CancelButton = Button(frame2, text="Cancel Operation", command=self.cancelOperation)
        CancelButton.pack(anchor=W, side=LEFT)

    def SelectItems(self):

        self.Shop = self.listbox.get('active')
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("choose items to get in cart")

        self.newWindow.geometry("800x400")

        # get the list of products for our menu
        self.Shop = re.split(',', self.Shop)

        # shop[0] Is shopName and Shop[1] is shop location
        products = db.getAllProductsFromMenu(self.Shop[0], self.Shop[1])
        self.frame2 = Frame(self.newWindow)
        self.frame2.pack(padx=5, pady=5)

        ProductLabel = Label(self.frame2, text="Products: ")
        ProductLabel.pack(side=LEFT, padx=5, pady=5)

        self.Labels = []

        for i in range(len(products)):
            self.Labels.append(
                (products[i][0] + "\t\t" + str(products[i][1]) + "\t\t" + str(products[i][2]), BooleanVar()))

        i = 0
        for label in self.Labels:
            self.LabelsButton = Checkbutton(self.frame2,
                                            text=label[0],
                                            variable=label[1])
            self.LabelsButton.pack(side=BOTTOM, padx=5, pady=5)
            i += 1

        self.ConfirmButton = Button(self.newWindow, text="Confirm Items", command=self.FinalizePurchase)
        self.ConfirmButton.pack(side=BOTTOM, padx=5, pady=5)

    def FinalizePurchase(self):

        Shop = self.listbox.get('active')
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Sign in and confirm order")

        self.newWindow.geometry("300x200")

        self.items = []
        for item in self.Labels:
            if item[1].get():
                self.items.append(item[0])

        self.frame1 = Frame(self.newWindow)
        self.frame1.pack(padx=5, pady=5, anchor=CENTER)

        self.label1 = Label(self.frame1, text="Enter Email")
        self.label1.pack(padx=5, pady=5, side=LEFT)

        self.Entry1 = Entry(self.frame1)
        self.Entry1.pack(padx=5, pady=5, side=RIGHT)

        self.frame2 = Frame(self.newWindow)
        self.frame2.pack(padx=5, pady=5, anchor=CENTER)

        self.label2 = Label(self.frame2, text="Enter Password: ")
        self.label2.pack(padx=5, pady=5, side=LEFT)

        self.Entry2 = Entry(self.frame2)
        self.Entry2.pack(padx=5, pady=5, side=RIGHT)

        if self.Delivery.get() == 'RESERVATION':
            self.frame3 = Frame(self.newWindow)
            self.frame3.pack(padx=5, pady=5, anchor=CENTER)

            self.Cuslabel = Label(self.frame3, text="Enter No of customers: ")
            self.Cuslabel.pack(padx=5, pady=5, side=LEFT)

            self.CusEntry = Entry(self.frame3)
            self.CusEntry.pack(padx=5, pady=5, side=RIGHT)

        self.frame4 = Frame(self.newWindow)
        self.frame4.pack(padx=5, pady=5, anchor=CENTER)

        self.ConfirmButton = Button(self.frame4, text="Confirm Login", command=self.ConfirmOrder)
        self.ConfirmButton.pack(side=LEFT, padx=5, pady=5)

    def ConfirmOrder(self):
        price = 0

        # calculate the order price
        for item in self.items:
            price += int(re.split("\t\t", item)[1])

        # add the item to the order tables
        shopID = db.getShopIdfromNameLocation(self.Shop[0], self.Shop[1])
        orderID = random.randint(0, 999999)
        print(self.Delivery.get())
        if self.Delivery.get() != 'RESERVATION':
            db.AddNewOrder(type=self.Delivery.get(), orderID=orderID, totalPrice=price,
                           user_email=self.Entry1.get(), shopID=shopID[0])
        else:
            db.AddNewOrder(type=self.Delivery.get(), orderID=orderID, totalPrice=price,
                           user_email=self.Entry1.get(), shopID=shopID[0], no_customers=self.CusEntry.get())

        # add the products to the ordered products table
        for item in self.items:
            productID = re.split("\t\t", item)[0]
            db.AddProductToOrder(orderID, productID)

        # show a confirmation message at the end
        messagebox.showinfo(title="Order Confirmed!", message="Operation finished successfully")

    def cancelOperation(self):
        self.newWindow.destroy()

    def CancelOrder(self):

        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Cancel Order")

        self.newWindow.geometry("400x200")

        self.frame1 = Frame(self.newWindow)
        self.frame1.pack(padx=5, pady=5, anchor=CENTER)

        self.label1 = Label(self.frame1, text="Enter Email")
        self.label1.pack(padx=5, pady=5, side=LEFT)

        self.Entry1 = Entry(self.frame1)
        self.Entry1.pack(padx=5, pady=5, side=RIGHT)

        self.frame2 = Frame(self.newWindow)
        self.frame2.pack(padx=5, pady=5, anchor=CENTER)

        self.label2 = Label(self.frame2, text="Enter Password: ")
        self.label2.pack(padx=5, pady=5, side=LEFT)

        self.Entry2 = Entry(self.frame2)
        self.Entry2.pack(padx=5, pady=5, side=RIGHT)

        self.frame3 = Frame(self.newWindow)
        self.frame3.pack(padx=5, pady=5, anchor=CENTER)

        self.frame4 = Frame(self.newWindow)
        self.frame4.pack(padx=5, pady=5, anchor=CENTER)

        self.ConfirmButton = Button(self.frame4, text="Confirm Login", command=self.ConfirmRequest)
        self.ConfirmButton.pack(side=LEFT, padx=5, pady=5)

        CancelButton = Button(self.frame4, text="Cancel Operation", command=self.cancelOperation)
        CancelButton.pack(side=LEFT, padx=5, pady=5)

    def ConfirmRequest(self):
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Cancel Order")

        self.newWindow.geometry("500x500")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5, anchor=CENTER)

        # A Label widget to show in toplevel
        Label(frame1, text="Choose a restaurant / Shop:").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=60, height=20)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        Orders = db.getOrdersByEmail(self.Entry1.get())

        self.listbox.insert(END,
                            "OrderID" + "\t\t" + "Total Price" + "\t\t" + "Points" + "\t\t" + "Date" + "\t\t" + "Time")
        # Insert elements into the
        for i in range(len(Orders)):
            self.listbox.insert(END,
                                str(Orders[i][0]) + "\t\t\t\t" + str(Orders[i][1]) + "\t\t" + str(
                                    Orders[i][3]) + "\t\t" + str(Orders[i][
                                                                     4]) + "\t\t" + str(Orders[i][5]))

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Cancel', command=self.DeleteOrder)
        self.button3.pack(padx=5, pady=5, side=LEFT)

    def DeleteOrder(self):
        db.cancelOrder(int(re.split("\t\t", self.listbox.get('active'))[0]))
        messagebox.showinfo(title="Deleted", message="Order cancelled successfully")
        self.newWindow.destroy()
        self.ConfirmRequest()

    def UpgradeAccount(self):
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Upgrade Account")

        self.newWindow.geometry("400x200")

        self.frame1 = Frame(self.newWindow)
        self.frame1.pack(padx=5, pady=5, anchor=CENTER)

        self.label1 = Label(self.frame1, text="Enter Email")
        self.label1.pack(padx=5, pady=5, side=LEFT)

        self.Entry1 = Entry(self.frame1)
        self.Entry1.pack(padx=5, pady=5, side=RIGHT)

        self.frame2 = Frame(self.newWindow)
        self.frame2.pack(padx=5, pady=5, anchor=CENTER)

        self.label2 = Label(self.frame2, text="Enter Password: ")
        self.label2.pack(padx=5, pady=5, side=LEFT)

        self.Entry2 = Entry(self.frame2, show="*")
        self.Entry2.pack(padx=5, pady=5, side=RIGHT)

        self.frame3 = Frame(self.newWindow)
        self.frame3.pack(padx=5, pady=5, anchor=CENTER)

        self.label3 = Label(self.frame3, text="Upgrade to: ")
        self.label3.pack(padx=5, pady=5, side=LEFT)

        self.Labels = ["PREMIUM", "STUDENT"]
        self.UpgradeType = StringVar()
        for label in self.Labels:
            self.LabelsButton = Radiobutton(self.frame3,
                                            text=label, value=label, variable=self.UpgradeType)
            self.LabelsButton.pack(padx=5, pady=5, side=LEFT)

        self.frame4 = Frame(self.newWindow)
        self.frame4.pack(padx=5, pady=5, anchor=CENTER)

        self.ConfirmButton = Button(self.frame4, text="Confirm Login", command=self.ConfirmAccount)
        self.ConfirmButton.pack(side=LEFT, padx=5, pady=5)

        CancelButton = Button(self.frame4, text="Cancel Operation", command=self.cancelOperation)
        CancelButton.pack(side=LEFT, padx=5, pady=5)

    def ConfirmAccount(self):
        email = self.Entry1.get()
        password = self.Entry2.get()

        # TODO::check if the email and password are correct
        Entered = not (email == '' or password == '')

        print(Entered)

        if not Entered:
            messagebox.showerror(title="Error", message="Please Enter the email and password")
        else:
            if self.UpgradeType.get() == 'PREMIUM':
                db.upgradeAccount(updateTo=self.UpgradeType.get(), email=email)
                messagebox.showinfo(title="Success", message="Upgraded successfully")
                self.newWindow.destroy()
            elif self.UpgradeType.get() == 'STUDENT':  # upgrade to student required adding student number and school
                # name
                # Toplevel object which will
                # be treated as a new window
                self.newWindow = Toplevel(master)

                # sets the title of the
                # Toplevel widget
                self.newWindow.title("Enter Student details")

                self.newWindow.geometry("400x200")

                self.frame4 = Frame(self.newWindow)
                self.frame4.pack(pady=5, padx=5, anchor=CENTER)
                self.label4 = Label(self.frame4, text="Enter Student Number")
                self.label4.pack(pady=5, padx=5, side=LEFT)

                self.Entry3 = Entry(self.frame4)
                self.Entry3.pack(padx=5, pady=5, side=RIGHT)

                self.frame5 = Frame(self.newWindow)
                self.frame5.pack(pady=5, padx=5, anchor=CENTER)

                self.label5 = Label(self.frame5, text="Enter School Name")
                self.label5.pack(pady=5, padx=5, side=LEFT)

                self.Entry4 = Entry(self.frame5)
                self.Entry4.pack(padx=5, pady=5, side=RIGHT)

                self.frame3 = Frame(self.newWindow)
                self.frame3.pack(padx=5, pady=5, anchor=CENTER)

                self.ConfirmButton = Button(self.frame3, text="Confirm Upgrade", command=self.addStudent)
                self.ConfirmButton.pack(side=LEFT, padx=5, pady=5)

                CancelButton = Button(self.frame3, text="Cancel Operation", command=self.cancelOperation)
                CancelButton.pack(side=LEFT, padx=5, pady=5)

    def addStudent(self):
        db.upgradeAccount(updateTo=self.UpgradeType.get(), email=self.Entry1.get(), student_no=self.Entry3.get(),
                          school_name=self.Entry4.get())
        messagebox.showinfo(title="Success", message="Upgraded successfully")
        self.newWindow.destroy()


class AdminInterface(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.pack(expand=YES, fill=BOTH)
        self.master.title("Tarteeb Admin Interface")

        ChoiceLabels = ['View all Riders', 'View All orders', 'View All Shops']

        button_frame = Frame()
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button1 = Button(button_frame, text=ChoiceLabels[0], command=self.ViewAllRiders)
        self.button1.grid(row=5, column=4, sticky=W + E + N + S)

        self.button2 = Button(button_frame, text=ChoiceLabels[1], command=self.ViewAllOrders)
        self.button2.grid(row=5, column=5, sticky=W + E + N + S)

        self.button3 = Button(button_frame, text=ChoiceLabels[2], command=self.ViewShops)
        self.button3.grid(row=5, column=6, sticky=W + E + N + S)

    """ Creates a new prompt window to show the list of all the riders"""

    def ViewAllRiders(self):
        self.newWindow = Toplevel(master)

        self.newWindow.title("Riders Details")

        self.newWindow.geometry("600x400")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5)

        # A Label widget to show in toplevel
        Label(frame1, text="riders : ").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=80, height=15)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        riders = db.getAvailableRiders()
        # Insert elements into the
        for rider in riders:
            self.listbox.insert(END, str(rider[0]) + "\t\t" + str(rider[1]) + "\t\t" + str(rider[2]) + "\t\t" + str(
                rider[3]) + "\t\t" + str(rider[5]) + "\t\t" + str(rider[6]) + "\t\t" + str(rider[7]) + "\t\t" + str(
                rider[8]) + "\t\t")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Add New Rider', command=self.AddNewRider)
        self.button3.pack(padx=5, pady=5, side=LEFT)

        self.button4 = Button(button_frame, text='Remove Rider', command=self.DeleteRider)
        self.button4.pack(padx=5, pady=5, side=RIGHT)

    """ Creates a new prompt window to show the list of all the orders"""

    def ViewAllOrders(self):
        self.newWindow = Toplevel(master)

        self.newWindow.title("order Details")

        self.newWindow.geometry("550x400")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5)

        # A Label widget to show in toplevel
        Label(frame1, text="order : ").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=50, height=15)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        orders = db.showAllOrders()
        # Insert elements into the
        for order in orders:
            self.listbox.insert(END, str(order[0]) + "\t\t" + str(order[1]) + "\t\t" + str(order[2]) + "\t\t" + str(
                order[3]) + "\t\t" + str(order[4]) + "\t\t" + str(order[5]) + "\t\t")

            # Attaching Listbox to Scrollbar
            # Since we need to have a vertical
            # scroll we use yscrollcommand
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Close', command=self.closeWindow)
        self.button3.pack(padx=5, pady=5, side=BOTTOM)

        self.button3 = Button(button_frame, text='Calculate Profit', command=self.Profit)
        self.button3.pack(padx=5, pady=5, side=BOTTOM)

    def Profit(self):
        profit = db.calculateProfit()[0]
        messagebox.showinfo(title='profit' , message='The profit calculated:  ' + str(profit))
    """ Creates a new prompt window to show the list of all the shops"""

    def ViewShops(self):
        self.newWindow = Toplevel(master)

        self.newWindow.title("shops Details")

        self.newWindow.geometry("400x400")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5)

        # A Label widget to show in toplevel
        Label(frame1, text="shops : ").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=20, height=10)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        shops = db.ViewAllShops()
        print(shops)
        # Insert elements into the
        for shop in shops:
            self.listbox.insert(END, str(shop[0]) + "\t\t" + str(shop[1]))

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Add shop', command=self.addshop)
        self.button3.pack(padx=5, pady=5, side=LEFT)

        self.button5 = Button(button_frame, text='Remove Shop', command=self.RemoveShop)
        self.button5.pack(padx=5, pady=5, side=LEFT)

        self.button4 = Button(button_frame, text='Close', command=self.closeWindow)
        self.button4.pack(padx=5, pady=5, side=LEFT)

    def RemoveShop(self):
        db.removeShop(re.split("\t\t", self.listbox.get('active'))[0])
        messagebox.showinfo(title="Deleted", message="shop deleted successfully")
        self.newWindow.destroy()
        self.ShowMenu()
        pass

    def AddNewRider(self):
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Adding rider")

        self.newWindow.geometry("300x700")

        Frame1 = Frame(self.newWindow)
        Frame1.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel1 = Label(Frame1, text="Enter RiderID:")
        self.EntryLabel1.pack(padx=5, pady=5, side=LEFT)
        self.Entry1 = Entry(Frame1)
        self.Entry1.pack(pady=5, padx=5, side=RIGHT)

        Frame2 = Frame(self.newWindow)
        Frame2.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel2 = Label(Frame2, text="Enter Email:")
        self.EntryLabel2.pack(padx=5, pady=5, side=LEFT)
        self.Entry2 = Entry(Frame2)
        self.Entry2.pack(pady=5, padx=5, side=RIGHT)

        Frame3 = Frame(self.newWindow)
        Frame3.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel3 = Label(Frame3, text="Enter type:")
        self.EntryLabel3.pack(padx=5, pady=5, side=LEFT)
        self.Entry3 = Entry(Frame3)
        self.Entry3.pack(pady=5, padx=5, side=RIGHT)

        Frame4 = Frame(self.newWindow)
        Frame4.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel4 = Label(Frame4, text="Enter base salary:")
        self.EntryLabel4.pack(padx=5, pady=5, side=LEFT)
        self.Entry4 = Entry(Frame4)
        self.Entry4.pack(pady=5, padx=5, side=RIGHT)

        Frame5 = Frame(self.newWindow)
        Frame5.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel5 = Label(Frame5, text="Enter Name:")
        self.EntryLabel5.pack(padx=5, pady=5, side=LEFT)
        self.Entry5 = Entry(Frame5)
        self.Entry5.pack(pady=5, padx=5, side=RIGHT)

        Frame6 = Frame(self.newWindow)
        Frame6.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel6 = Label(Frame6, text="Enter Surame:")
        self.EntryLabel6.pack(padx=5, pady=5, side=LEFT)
        self.Entry6 = Entry(Frame6)
        self.Entry6.pack(pady=5, padx=5, side=RIGHT)

        Frame7 = Frame(self.newWindow)
        Frame7.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel7 = Label(Frame7, text="Enter Phone:")
        self.EntryLabel7.pack(padx=5, pady=5, side=LEFT)
        self.Entry7 = Entry(Frame7)
        self.Entry7.pack(pady=5, padx=5, side=RIGHT)

        Frame8 = Frame(self.newWindow)
        Frame8.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel8 = Label(Frame8, text="Enter Vehicle type:")
        self.EntryLabel8.pack(padx=5, pady=5, side=LEFT)
        self.Entry8 = Entry(Frame8)
        self.Entry8.pack(pady=5, padx=5, side=RIGHT)

        buttonFrame = Frame(self.newWindow)
        buttonFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(buttonFrame, text='Add rider', command=self.ap)
        self.button3.pack(padx=5, pady=5, side=BOTTOM)
        self.button4 = Button(buttonFrame, text='Close', command=self.closeWindow)
        self.button4.pack(padx=5, pady=5, side=BOTTOM)

    def DeleteRider(self):

        db.removeRider(re.split("\t\t", self.listbox.get('active'))[0])
        messagebox.showinfo(title="Deleted", message="Rider deleted successfully")
        self.newWindow.destroy()
        self.AddNewRider()

    """ Creates a new prompt window to add a new Shop"""

    def addshop(self):
        self.newWindow = Toplevel(master)

        self.newWindow.title("add shop")

        self.newWindow.geometry("370x120")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5)

        # A Label widget to show in toplevel
        Label(frame1, text="select type of shop : ").pack(anchor=W, padx=5, pady=5)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Add resturant', command=self.AddNewResturant)
        self.button3.pack(padx=5, pady=5, side=LEFT)

        self.button5 = Button(button_frame, text='add grocery', command=self.Addnewgrocery)
        self.button5.pack(padx=5, pady=5, side=LEFT)

        self.button4 = Button(button_frame, text='Close', command=self.closeWindow)
        self.button4.pack(padx=5, pady=5, side=LEFT)

    def AddNewResturant(self):
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Adding restaurant")

        self.newWindow.geometry("400x500")

        frame1 = Frame(self.newWindow)
        frame1.pack(padx=5, pady=5)

        Frame1 = Frame(self.newWindow)
        Frame1.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel1 = Label(Frame1, text="Enter restaurant ID:")
        self.EntryLabel1.pack(padx=5, pady=5, side=LEFT)
        self.Entry1 = Entry(Frame1)
        self.Entry1.pack(pady=5, padx=5, side=RIGHT)

        Frame2 = Frame(self.newWindow)
        Frame2.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel2 = Label(Frame2, text="Enter location:")
        self.EntryLabel2.pack(padx=5, pady=5, side=LEFT)
        self.Entry2 = Entry(Frame2)
        self.Entry2.pack(pady=5, padx=5, side=RIGHT)

        Frame3 = Frame(self.newWindow)
        Frame3.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel3 = Label(Frame3, text="Enter name:")
        self.EntryLabel3.pack(padx=5, pady=5, side=LEFT)
        self.Entry3 = Entry(Frame3)
        self.Entry3.pack(pady=5, padx=5, side=RIGHT)

        Frame4 = Frame(self.newWindow)
        Frame4.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel4 = Label(Frame4, text="Enter menu:")
        self.EntryLabel4.pack(padx=5, pady=5, side=LEFT)
        self.Entry4 = Entry(Frame4)
        self.Entry4.pack(pady=5, padx=5, side=RIGHT)

        Frame5 = Frame(self.newWindow)
        Frame5.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel5 = Label(Frame5, text="Enter Manger phone number:")
        self.EntryLabel5.pack(padx=5, pady=5, side=LEFT)
        self.Entry5 = Entry(Frame5)
        self.Entry5.pack(pady=5, padx=5, side=RIGHT)

        Frame6 = Frame(self.newWindow)
        Frame6.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel6 = Label(Frame6, text="Enter Cuisine Type :")
        self.EntryLabel6.pack(padx=5, pady=5, side=LEFT)
        self.Entry6 = Entry(Frame6)
        self.Entry6.pack(pady=5, padx=5, side=RIGHT)

        buttonFrame = Frame(self.newWindow)
        buttonFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)


        self.button3 = Button(buttonFrame, text='Add restaurant', command=self.ap1)
        self.button3.pack(padx=5, pady=5, side=LEFT)

        self.button4 = Button(buttonFrame, text='Close', command=self.closeWindow)
        self.button4.pack(padx=5, pady=5, side=LEFT)

    def Addnewgrocery(self):
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Adding Grocery shop")

        self.newWindow.geometry("300x450")

        EntryFrame1 = Frame(self.newWindow)
        EntryFrame1.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel1 = Label(EntryFrame1, text="Enter Grocery shop ID:")
        self.EntryLabel1.pack(padx=5, pady=5, side=LEFT)
        self.Entry1 = Entry(EntryFrame1)
        self.Entry1.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame2 = Frame(self.newWindow)
        EntryFrame2.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel2 = Label(EntryFrame2, text="Enter location:")
        self.EntryLabel2.pack(padx=5, pady=5, side=LEFT)
        self.Entry2 = Entry(EntryFrame2)
        self.Entry2.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame3 = Frame(self.newWindow)
        EntryFrame3.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel3 = Label(EntryFrame3, text="Enter name:")
        self.EntryLabel3.pack(padx=5, pady=5, side=LEFT)
        self.Entry3 = Entry(EntryFrame3)
        self.Entry3.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame4 = Frame(self.newWindow)
        EntryFrame4.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel4 = Label(EntryFrame4, text="Enter menu ID:")
        self.EntryLabel4.pack(padx=5, pady=5, side=LEFT)
        self.Entry4 = Entry(EntryFrame4)
        self.Entry4.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame5 = Frame(self.newWindow)
        EntryFrame5.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel5 = Label(EntryFrame5, text="Enter mgr phone:")
        self.EntryLabel5.pack(padx=5, pady=5, side=LEFT)
        self.Entry5 = Entry(EntryFrame5)
        self.Entry5.pack(pady=5, padx=5, side=RIGHT)

        buttonFrame = Frame(self.newWindow)
        buttonFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(buttonFrame, text='Add Grocery', command=self.ap1)
        self.button3.pack(padx=5, pady=5, side=BOTTOM)

        self.button4 = Button(buttonFrame, text='Close', command=self.closeWindow)
        self.button4.pack(padx=5, pady=5, side=BOTTOM)

    def ap1(self):
        db.addNewShop(self.Entry1.get(), self.Entry2.get(), self.Entry3.get(), self.Entry4.get(),
                      self.Entry5.get(), self.Entry6.get(), None)
        messagebox.showinfo(title="Message", message="Added successfully alhamdullah")
        self.newWindow.destroy()

    def ap(self):
        db.addRider(self.Entry1.get(), self.Entry2.get(), self.Entry3.get(), self.Entry4.get(),
                    self.Entry5.get(), self.Entry6.get(), self.Entry7.get(), self.Entry8.get())
        messagebox.showinfo(title="Message", message="Added successfully alhamdullah")
        self.newWindow.destroy()

    def closeWindow(self):
        self.newWindow.destroy()


class ShopInterface(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.scrollbar = None
        self.listbox = None
        self.newWindow = None
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Tarteeb Shop Interface")

        ChoiceLabels = ['Show current menu', 'Show Orders']

        EntryFrame = Frame()
        EntryFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel = Label(EntryFrame, text="Enter shopID:")
        self.EntryLabel.pack(padx=5, pady=5, side=LEFT)

        self.IDEntry = Entry(EntryFrame)
        self.IDEntry.pack(pady=5, padx=5, side=RIGHT)

        button_frame = Frame()
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button1 = Button(button_frame, text=ChoiceLabels[0], command=self.ShowMenu)
        self.button1.grid(row=5, column=4, sticky=W + E + N + S)

        self.button2 = Button(button_frame, text=ChoiceLabels[1], command=self.ShowOrders)
        self.button2.grid(row=5, column=5, sticky=W + E + N + S)

    """ A function to show the menu of a certain restuarant"""

    def ShowMenu(self):
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Menu Details")

        self.newWindow.geometry("500x300")

        frame1 = Frame(self.newWindow)
        frame1.pack(padx=5, pady=5)

        # A Label widget to show in toplevel
        Label(frame1, text="Choose a restaurant / Shop:").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=40, height=10)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        products = db.showMenu(self.IDEntry.get())
        print(products)
        # Insert elements into the
        for i in range(len(products)):
            self.listbox.insert(END, products[i][0] + "\t\t" + str(products[i][1]) + "\t\t" + products[i][2])

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Add Product', command=self.AddProduct)
        self.button3.pack(padx=5, pady=5, side=LEFT)

        self.button4 = Button(button_frame, text='Delete Product', command=self.deleteProduct)
        self.button4.pack(padx=5, pady=5, side=RIGHT)

    """ Show a prompt to add a new product to the resturants menu"""

    def AddProduct(self):
        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Adding Products")

        self.newWindow.geometry("300x400")

        frame1 = Frame(self.newWindow)
        frame1.pack(padx=5, pady=5)

        EntryFrame = Frame(self.newWindow)
        EntryFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel = Label(EntryFrame, text="Enter productID:")
        self.EntryLabel.pack(padx=5, pady=5, side=LEFT)
        self.IDEntry1 = Entry(EntryFrame)
        self.IDEntry1.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame1 = Frame(self.newWindow)
        EntryFrame1.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel = Label(EntryFrame1, text="Enter price:")
        self.EntryLabel.pack(padx=5, pady=5, side=LEFT)
        self.IDEntry2 = Entry(EntryFrame1)
        self.IDEntry2.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame2 = Frame(self.newWindow)
        EntryFrame2.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel = Label(EntryFrame2, text="Enter description:")
        self.EntryLabel.pack(padx=5, pady=5, side=LEFT)
        self.IDEntry3 = Entry(EntryFrame2)
        self.IDEntry3.pack(pady=5, padx=5, side=RIGHT)

        EntryFrame3 = Frame(self.newWindow)
        EntryFrame3.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.EntryLabel = Label(EntryFrame3, text="Enter menuID:")
        self.EntryLabel.pack(padx=5, pady=5, side=LEFT)
        self.IDEntry4 = Entry(EntryFrame3)
        self.IDEntry4.pack(pady=5, padx=5, side=RIGHT)

        buttonFrame = Frame(self.newWindow)
        buttonFrame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(buttonFrame, text='Add Product', command=self.ap)
        self.button3.pack(padx=5, pady=5, side=BOTTOM)

    def ap(self):
        db.addNewProduct(self.IDEntry1.get(), self.IDEntry2.get(), self.IDEntry3.get(), self.IDEntry4.get())
        messagebox.showinfo(title="Message", message="Added successfully alhamdullah")
        self.newWindow.destroy()

    """ Show a prompt to delete a product to the resturants menu"""

    def deleteProduct(self):
        db.deleteProduct(re.split("\t\t", self.listbox.get('active'))[0])
        messagebox.showinfo(title="Deleted", message="Product deleted successfully")
        self.newWindow.destroy()
        self.ShowMenu()

    """ show a prompt with all the orders from a certain resturant"""

    def ShowOrders(self):

        # Toplevel object which will
        # be treated as a new window
        self.newWindow = Toplevel(master)

        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Adding Products")

        self.newWindow.geometry("600x300")

        frame1 = Frame(self.newWindow)
        frame1.pack(pady=5, padx=5)

        # A Label widget to show in toplevel
        Label(frame1, text="Orders : ").pack(anchor=W, padx=5, pady=5)

        # Creating a Listbox and
        # attaching it to root window
        self.listbox = Listbox(frame1, width=50, height=10)

        # Adding Listbox to the left
        # side of root window
        self.listbox.pack(side=LEFT, anchor=CENTER, fill="both", expand=True)

        # Creating a Scrollbar and
        # attaching it to root window
        self.scrollbar = Scrollbar(frame1)

        # Adding Scrollbar to the right
        # side of root window
        self.scrollbar.pack(side=LEFT, anchor=CENTER)

        orders = db.getAllShopOrders(self.IDEntry.get())
        # Insert elements into the
        for listOrders in orders:
            for order in listOrders:
                self.listbox.insert(END, str(order[0]) + "\t\t" + str(order[1]) + "\t\t" + order[2] + "\t\t" + str(
                    order[3]) + "\t\t" + str(order[4]) + "\t\t" + str(order[5]) + "\t\t")

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        self.scrollbar.config(command=self.listbox.yview)

        button_frame = Frame(self.newWindow)
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button3 = Button(button_frame, text='Close', command=self.closeWindow)
        self.button3.pack(padx=5, pady=5, side=LEFT)

    def closeWindow(self):
        self.newWindow.destroy()


class MainWindow(Frame):

    def __init__(self):
        Frame.__init__(self)

        self.pack(expand=YES, fill=BOTH)
        self.master.title("Tarteeb Main Interface")

        ChoiceLabels = ['User', 'Admin', 'Shop']

        button_frame = Frame()
        button_frame.pack(anchor=CENTER, fill=BOTH, padx=15, pady=15)

        self.button1 = Button(button_frame, text=ChoiceLabels[0], command=self.UserWindow)
        self.button1.grid(row=5, column=4, sticky=W + E + N + S)

        self.button2 = Button(button_frame, text=ChoiceLabels[1], command=self.AdminWindow)
        self.button2.grid(row=5, column=5, sticky=W + E + N + S)

        self.button3 = Button(button_frame, text=ChoiceLabels[2], command=self.ShopWindow)
        self.button3.grid(row=5, column=6, sticky=W + E + N + S)

    # for all of the following functions destroy the old window and show the current window
    def UserWindow(self):
        current_window = UserInterface()
        current_window.mainloop()

    def AdminWindow(self):
        current_window = AdminInterface()
        current_window.mainloop()

    def ShopWindow(self):
        current_window = ShopInterface()
        current_window.mainloop()


def replace_window(root):
    """Destroy current window, create new window"""
    global current_window
    if current_window is not None:
        current_window.destroy()
    current_window = tkinter.Toplevel(root)

    # if the user kills the window via the window manager,
    # exit the application.
    current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)

    return current_window


if __name__ == "__main__":
    current_window = AdminInterface()
    current_window.mainloop()
