import socket
from tkinter import *
from tkinter import messagebox
import re


class managerPanel(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Manager Panel")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=W + E + N + S)

        self.SizeLabel = Label(self, text="REPORTS")
        self.SizeLabel.grid(row=0, column=0, sticky=W + E + N + S)

        self.items = ["(1) What is the most popular coffee overall?",
                      "(2) Which barista has the highest number of orders?",
                      "(3) What is the most popular product for the orders with the discount code?",
                      "(4) What is the most popular cake that is bought with espresso?"]

        self.reportOption = IntVar()

        counter = 1
        for item in self.items:
            self.reportSelection = Radiobutton(self, text=item, value=counter, variable=self.reportOption)
            self.reportSelection.grid(row=counter, column=0, sticky=W)
            counter += 1

        self.createButton = Button(self, text="Create", command=self.createPressed)
        self.closeButton = Button(self, text="Close", command=self.closePressed)

        self.createButton.grid(row=counter + 1, column=0, columnspan=2, sticky=W + E + N + S)
        self.closeButton.grid(row=counter + 1, column=2, sticky=W + E + N + S)

    def createPressed(self):

        if(self.reportOption.get()==1):
            self.msg="report1"
        elif(self.reportOption.get()==2):
            self.msg = "report2"
        elif (self.reportOption.get() == 3):
            self.msg = "report3"
        elif (self.reportOption.get() == 4):
            self.msg = "report4"

        self.response = networkBoot(self.msg)
        shownMessage = re.split(";",self.response)
        messagebox.showinfo(self.msg, shownMessage[1:])
    def closePressed(self):
        self.quit()
        self.destroy()


class baristaPanel(Frame):
    def __init__(self,baristaName):
        Frame.__init__(self)
        self.baristaName=baristaName
        self.master.title("Barista Panel")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=W + E + N + S)

        self.coffeLabel = Label(self, text="COFFEE")
        self.coffeLabel.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S)

        self.coffees = [("Latte", BooleanVar(),IntVar()), ("Cappuccino", BooleanVar(),IntVar()),
                       ("Americano", BooleanVar(),IntVar()), ("Espresso", BooleanVar(),IntVar())]
        self.discountCode = StringVar()

        counter = 1
        for coffee in self.coffees:
            self.coffeeSelection = Checkbutton(self, text=coffee[0], variable=coffee[1])
            self.coffeeQuantity = Entry(self,textvariable=coffee[2])


            self.coffeeSelection.grid(row=counter, column=0, sticky=W)
            self.coffeeQuantity.grid(row=counter, column=1, sticky=W + E + N + S)
            counter += 1

        counter += 1
        self.cakesLabel = Label(self, text="CAKES")
        self.cakesLabel.grid(row=counter, column=0, columnspan=2, sticky=W + E + N + S)

        self.cakes = [("San Sebastian Cheesecake", BooleanVar(),IntVar()), ("Mosaic Cake", BooleanVar(),IntVar()),
                      ("Carrot Cake", BooleanVar(),IntVar())]

        counter += 1
        for cake in self.cakes:
            self.cakeSelection = Checkbutton(self, text=cake[0], variable=cake[1])
            self.cakeQuantity = Entry(self,textvariable=cake[2])

            self.cakeSelection.grid(row=counter, column=0, sticky=W)
            self.cakeQuantity.grid(row=counter, column=1, sticky=W + E + N + S)
            counter += 1

        self.discountLabel = Label(self, text="Discount code, if any:")
        self.discount = Entry(self,textvariable=self.discountCode)

        self.discountLabel.grid(row=counter, padx=20, column=0, sticky=W)
        self.discount.grid(row=counter, column=1, sticky=W + E + N + S)

        counter += 1
        self.createButton = Button(self, text="Create", command=self.buttonPressed)
        self.closeButton = Button(self, text="Close", command=self.closePressed)

        self.createButton.grid(row=counter + 1, column=0, sticky=W + E + N + S)
        self.closeButton.grid(row=counter + 1, column=1, sticky=W + E + N + S)

    def buttonPressed(self):
        coffeeSelections = ""
        cakeSelections = ""
        ordercoffeeSelections = ""
        ordercakeSelections = ""
        if (self.discountCode.get()!=""):
            self.msg = "order;"+self.discountCode.get()+";"+self.baristaName
        elif(self.discountCode.get()==""):
            self.msg = "order;nodiscount;"+self.baristaName
        for coffee in self.coffees:
            if coffee[1].get():
                coffeeSelections+="\t" + coffee[0] + ": " + str(coffee[2].get()) + "\n"
                ordercoffeeSelections +=";"+coffee[0] + "-" + str(coffee[2].get())
        for cake in self.cakes:
            if cake[1].get():
                cakeSelections +="\t" + cake[0] + ": " + str(cake[2].get()) + "\n"
                if (cake[0] == "San Sebastian Cheesecake"):
                    ordercakeSelections += ";sansebastian" + "-" + str(cake[2].get())
                elif(cake[0] == "Mosaic Cake"):
                    ordercakeSelections += ";mosaic" + "-" + str(cake[2].get())
                elif(cake[0] == "Carrot Cake"):
                    ordercakeSelections += ";carrot" + "-" + str(cake[2].get())

        messagebox.showinfo("Message", "Coffees:\n " + coffeeSelections + "\nCakes:\n" + cakeSelections)
        self.msg += (ordercoffeeSelections + ordercakeSelections).lower()
        self.response = networkBoot(self.msg)
        messagebox.showinfo("Message", self.response)
    def closePressed(self):
        self.quit()
        self.destroy()


class authentication(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.response = None
        self.pack()
        self.master.title("Login")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)
        self.master.bind('<Return>', self.loginPressed)

        self.UserNameLabel = Label(self.frame1, text="Username")
        self.UserNameLabel.pack(side=LEFT, padx=5, pady=5)

        self.UserName = Entry(self.frame1, name="username")
        self.UserName.pack(side=LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.PasswordLabel = Label(self.frame2, text="Password")
        self.PasswordLabel.pack(side=LEFT, padx=5, pady=5)

        self.Password = Entry(self.frame2, name="password", show="*")
        self.Password.pack(side=LEFT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.LoginButton = Button(self.frame3, text="Login", command=self.loginPressed)
        self.LoginButton.pack(padx=5, pady=5)

    # as login button pressed username % password will be packed to send server, then recive a response massage to
    # see username & password are valid
    def loginPressed(self, event=None):
        username = self.UserName.get()
        password = self.Password.get()
        msg = ('login;'+username + ';' + password)
        self.response = networkBoot(msg)
        messagebox.showinfo("Message", self.response)
        self.quit()

    def getResponse(self):
        return self.response


SERVER = "127.0.0.1"
PORT = 5000

#to establieh client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


# out_data received from login panel will be sent to server in order to evaluate authorization
def networkBoot(out_data):
    client.send(out_data.encode())
    response = client.recv(1024).decode()
    return response


global authorizer

if __name__ == "__main__":

    # open login panel
    window = authentication()
    window.mainloop()
    response = re.split(";", window.getResponse())
    window.destroy()
    while(response[0]=="loginfailure"):
        window = authentication()
        window.mainloop()
        response = re.split(";", window.getResponse())
        window.destroy()



    if response[0] == 'loginsuccess':
        if response[2] == 'barista':
            baristaWindow = baristaPanel(response[1])
            baristaWindow.mainloop()
        elif response[2] == 'manager':
            managerWindow = managerPanel()
            managerWindow.mainloop()




    # close the client socket
    client.send('close'.encode())
    client.close()
