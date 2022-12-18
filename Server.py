import socket
import threading
import re
from math import *


# records of the available users received from txt file
def userRecords():
    try:
        file = open("users.txt", "r")
    except:
        print("Error happened in opening the file")
        exit(1)

    records = file.readlines()

    users = []
    for record in records:
        temp = re.split(";", record)
        temp[2] = re.sub("\n", "", temp[2])
        users.append(temp)
    file.close()
    return users


def priceRecords():
    try:
        file = open("prices.txt", "r")
    except:
        print("Error happened in opening the file")
        exit(1)

    records = file.readlines()

    prices = []
    for record in records:
        temp = re.split(";", record)
        temp[1] = re.sub("\n", "", temp[1])
        prices.append(temp)
    file.close()
    return prices


def discountRecords():
    try:
        file = open("discountcodes.txt", "r")
    except:
        print("Error happened in opening the file")
        exit(1)

    records = file.readlines()

    discounts = []
    for record in records:
        temp = re.split(";", record)
        temp[1] = re.sub("\n", "", temp[1])
        discounts.append(temp)
    file.close()
    return discounts


def orderRecords():
    try:
        file = open("orders.txt", "r")
    except:
        print("Error happened in opening the file")
        exit(1)

    records = file.readlines()

    orders = []
    for record in records:
        temp = re.split(";", record)
        temp[len(temp) - 1] = re.sub("\n", "", temp[len(temp) - 1])
        orders.append(temp)
    file.close()
    return orders


def appendOrderRecords(newLine):
    try:
        file = open("orders.txt", "a")
    except:
        print("Error happened in opening the file")
        exit(1)
    file.write(newLine + "\n")
    file.close()


# information received from the client side is checked whether they are correct or not.
def loginCheck(username, password):
    for user in userRecords():
        if user[0] == username and user[1] == password:
            return 'loginsuccess;' + user[0] + ';' + user[2]

    return 'loginfailure'


def orderReceived(orderList):
    discountCode = orderList[0]
    baristaName = orderList[1]
    orderPrice = 0
    discountRatio= int(discountCheck(discountCode))
    for product in orderList[2:]:
        productInfo = re.split("-", product)
        orderPrice += priceCheck(productInfo)
    # Creating the string to be appended to the orders file.
    appendedLine = str(int(orderPrice - (orderPrice * (discountRatio / 100)))) + ";" + str(
        discountCheck(discountCode)) + ";" + baristaName + ";"
    for product in orderList[2:]:
        if product == orderList[2:][len(orderList[2:]) - 1]:
            appendedLine += product
        else:
            appendedLine += product + ";"
    appendOrderRecords(appendedLine)
    if (discountCode == 'nodiscountcode'):
        return orderPrice
    else:
        return orderPrice - (orderPrice * (discountRatio / 100))

# Method to check the total price of an order before discount.
def priceCheck(productInfo):
    for price in priceRecords():  # Check price records to find the product's price.
        if productInfo[0] == price[0]:
            return int(price[1]) * int(productInfo[1])  # Return product price multiplied by ordered amount.

# Method to check if given discount code is valid.
def discountCheck(discountCode):
    lineIndex = 0
    for discount in discountRecords():
        if discountCode == discount[0]:
            removeDiscount(discountCode,lineIndex)
            return discount[1]
        else:
            return 0  # If discount code isn't found then return 0 for no discount.
    lineIndex+=1

def removeDiscount(discountCode,lineIndex):
    try:
        file = open("discountcodes.txt", "r")
    except:
        print("Error happened in opening the file")
        exit(1)
    records = file.readlines()
    file.close()

    try:
        file = open("discountcodes.txt", "w")
    except:
        print("Error happened in opening the file")
        exit(1)


    for currentLine in records:
        if currentLine != records[lineIndex]:
            file.write(currentLine)

    file.close()

# Method to find the most popular coffee
def mostPopularCoffee():
    coffeeDict = {
        "latte": 0,
        "cappuccino": 0,
        "americano": 0,
        "espresso": 0
    }
    maxCoffee = [["", 0]]
    for order in orderRecords():
        for coffee in order[3:]:
            coffeeInfo = re.split("-", coffee)
            if (coffeeInfo[0] == list(coffeeDict.keys())[0] or coffeeInfo[0] == list(coffeeDict.keys())[1] or
                    coffeeInfo[0] == list(coffeeDict.keys())[2] or coffeeInfo[0] == list(coffeeDict.keys())[3]):
                coffeeDict[coffeeInfo[0]] += int(coffeeInfo[1])

    for coffeeType in list(coffeeDict.items()):
        if (coffeeType[1] == maxCoffee[0][1]):
            maxCoffee.append([coffeeType[0], coffeeType[1]])
        if (coffeeType[1] > maxCoffee[0][1]):
            maxCoffee[0][0] = coffeeType[0]
            maxCoffee[0][1] = coffeeType[1]
    return maxCoffee


# Method to find the barista with the highest order
def highestOrderBarista():
    baristaDict = {
        "greg": 0,
        "dave": 0
    }
    maxBarista = [["", 0]]
    for order in orderRecords():
        for barista in order[2:3]:
            baristaDict[barista] += 1
    for baristaInfo in list(baristaDict.items()):
        if (baristaInfo[1] == maxBarista[0][1]):
            maxBarista.append([baristaInfo[0], baristaInfo[1]])
        if (baristaInfo[1] > maxBarista[0][1]):
            maxBarista[0][0] = baristaInfo[0]
            maxBarista[0][1] = baristaInfo[1]
    return maxBarista


# Method to find the most popular product bought with discount code
def mostPopularDiscountProduct():
    productDict = {
        "latte": 0,
        "cappuccino": 0,
        "americano": 0,
        "espresso": 0,
        "sansebastian": 0,
        "mosaic": 0,
        "carrot": 0
    }
    maxProduct = [["", 0]]
    for order in orderRecords():
        if (int(order[1:2][0]) != 0):
            for product in order[3:]:
                productInfo = re.split("-", product)
                productDict[productInfo[0]] += int(productInfo[1])
    for productType in list(productDict.items()):

        if (productType[1] == maxProduct[0][1]):
            maxProduct.append([productType[0], productType[1]])
        if (productType[1] > maxProduct[0][1]):
            maxProduct[0][0] = productType[0]
            maxProduct[0][1] = productType[1]

    return maxProduct


# Method to find the most popular cake bought with espresso.
def mostPopularEspresso():
    cakeDict = {
        "sansebastian": 0,
        "mosaic": 0,
        "carrot": 0
    }
    maxCake = [["", 0]]
    for order in orderRecords():
        if (wordExists("espresso", order)):
            for product in order[3:]:
                cakeInfo = re.split("-", product)
                if (cakeInfo[0] == list(cakeDict.keys())[0] or cakeInfo[0] == list(cakeDict.keys())[1] or cakeInfo[0] ==
                        list(cakeDict.keys())[2]):
                    cakeDict[cakeInfo[0]] += int(cakeInfo[1])
    for productType in list(cakeDict.items()):

        if (productType[1] == maxCake[0][1]):
            maxCake.append([productType[0], productType[1]])
        if (productType[1] > maxCake[0][1]):
            maxCake[0][0] = productType[0]
            maxCake[0][1] = productType[1]

    return maxCake


# Method to find if a word exists in an order. Used in report 4 to find if order has espresso.
def wordExists(keyword, order):
    for product in order[3:]:
        productInfo = re.split("-", product)
        if productInfo[0] == "espresso":
            return True
    return False


class ClientThread(threading.Thread):
    def __init__(self, clientsocket, clientaddress):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        print("Connection from ", clientaddress)

    def run(self):
        while True:
            receive = self.clientsocket.recv(1024).decode()
            temp = re.split(";", receive)
            if (temp[0] == 'login'):
                response = loginCheck(temp[1], temp[2])
                self.clientsocket.send(response.encode())

                while re.split(";", response)[0] == 'loginfailure':
                    receive = self.clientsocket.recv(1024).decode()
                    temp = re.split(";", receive)

                    response = loginCheck(temp[1], temp[2])
                    self.clientsocket.send(response.encode())
            elif (temp[0] == 'order'):
                response = "orderconfirmation;" + str(orderReceived(temp[1:]))
                self.clientsocket.send(response.encode())
            elif (temp[0] == 'report1'):
                response = "report1"
                result = mostPopularCoffee()
                for i in result:
                    response += ";" + i[0]
                self.clientsocket.send(response.encode())
            elif (temp[0] == 'report2'):
                response = "report2"
                result = highestOrderBarista()
                for i in result:
                    response += ";" + i[0]
                self.clientsocket.send(response.encode())
            elif (temp[0] == 'report3'):
                response = "report3"
                result = mostPopularDiscountProduct()
                for i in result:
                    response += ";" + i[0]
                self.clientsocket.send(response.encode())
            elif (temp[0] == 'report4'):
                response = "report4"
                result = mostPopularEspresso()
                for i in result:
                    response += ";" + i[0]
                self.clientsocket.send(response.encode())

            # after all operations are completed, close signal from client side stops clients, server side session
            if receive == 'close':
                break

        self.clientsocket.close()


HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started")
print("Waiting for connection requests")

while True:
    server.listen()
    clientsocket, clientaddress = server.accept()
    newThread = ClientThread(clientsocket, clientaddress)
    newThread.start()
