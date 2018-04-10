from tkinter import *
import serial
import time
import requests
import json
import serial.tools.list_ports

class data:
    def loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2):
        
        try:
            
            voltage = ser.readline().decode().replace('\n', '')
            voltage2 = ser.readline().decode().replace('\n', '')
            
            if start == 0 and (voltage != "" and voltage2 != ""):
                print("Voltage is " + voltage)
                print("Voltage2 is " + voltage2)
                start = 1
                modifier = voltage
                modifier2 = voltage2
                print("Modifier is " + str(modifier))
                print("Modifier2 is " + str(modifier2))
            
            
            if voltage != "" and voltage2 != "":
                
                distance = str((int(voltage) - int(modifier))*0.00248756)
                distance2 = str((int(voltage2) - int(modifier2))*0.00248756)
            
                time_hhmmss = time.strftime('%H:%M:%S')
                date_mmddyyyy = time.strftime('%d/%m/%Y')
                
                time_hhmmss = time.strftime('%H:%M:%S')
                date_mmddyyyy = time.strftime('%d/%m/%Y')
                
                object.change(voltage, distance, voltage2, distance2)
                
                print ('V1: ' + voltage + ', ' + 'D1: ' + distance + ', ' + 'V2: ' + voltage2 + ', ' + 'D2: ' + distance2 + ', ' + time_hhmmss + ', ' + date_mmddyyyy)
                
                if count == 0 and sendTime != -1 :
                    ser.write(b'0')
                    print("LED turned on!")
                
                if sendTime == count:
                    ser.write(b'0')
                    print("LED turned off!")
                
                if count%30 == 0:
                    
                    data = {'date':date_mmddyyyy,'time':time_hhmmss,'value':voltage,'dist':distance,'value2':voltage2,'dist2':distance2}
                    result = requests.post(firebaseURL + '/' + urlAddition +'.json', data=json.dumps(data))
                    print("Sent!")
                
                count+=1
            
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2))
        
        except IOError:
            print('Error! Something went wrong.')
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2))

    def startTest(self, connections, buttons, entryTestName, entryTestLength):
    
        firebaseURL = "https://work-5b7b6.firebaseio.com/"
        
        #ser = serial.Serial('/dev/cu.usbmodem1461', 9600, timeout=0)
        connected = 0
        
        for i in range(0, len(connections)):
            if connections[i]["text"]=="Connected.":
                ser = serial.Serial(buttons[i]["text"], 9600, timeout=0)
                connected = 1
                print(connections[i]["text"])
            i=+1
        
        if connected == 0:
            ser = serial.Serial('/dev/cu.usbmodem1461', 9600, timeout=0)
        
        sendTime = -1
        urlAddition = 'voltage'
        count = 0
        start = 0
        modifier = 0
        modifier2 = 0
        
        try:
            urlAddition = str(entryTestName.get())
        except (ValueError):
            print("Not a valid test name, voltage will be used.")
        
        try:
            sendTime = int(entryTestLength.get())
        except (ValueError):
            print("Invalid time recieved, LED will not go off")
        
        data.loop(data, self, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2)

class GUI(Frame):
    
    def connect(self, i):
        print(self.buttons[i]["text"])
        self.connections[i]["text"] = "Connected."
        
        for j in range(0, len(self.connections)):
            if j==i:
                continue
            else:
                self.connections[j]["text"]=""

    def closeWindow(self):
        root.destroy()
        exit()
    
    def __init__(self, master):
        super(GUI, self).__init__()
        self.grid()
        
        self.buttons = []
        self.connections = []
        
        self.labelTitle = Label(self, text = "Sash Testing With Sound")
        self.labelTitle.grid(row=0, column = 1)
        
        self.labelVoltageStay = Label(self, text = "Voltage: ")
        self.labelDistanceStay = Label(self, text = "Distance: ")
        self.labelLEDStay = Label(self, text = "LED: ")
        
        self.labelVoltageStay.grid(row=1, column=3, sticky=E)
        self.labelDistanceStay.grid(row=2, column=3, sticky = E)
        self.labelLEDStay.grid(row=3,column=3, sticky = E)
        
        self.labelVoltage = Label(self, text = "Value")
        self.labelDistance = Label(self, text = "Value")
        self.labelLED = Label(self, text = "Green")
        
        self.labelVoltage.grid(row=1, column=4, sticky=W)
        self.labelDistance.grid(row=2, column=4,sticky=W)
        self.labelLED.grid(row=3, column=4, sticky=W)
        
        #Repeat of labels
        self.labelVoltageStay2 = Label(self, text = "Volts2: ")
        self.labelDistanceStay2 = Label(self, text = "Distance2: ")
        self.labelLEDStay2 = Label(self, text = "LED2: ")

        self.labelVoltageStay2.grid(row=1, column=6, sticky=E)
        self.labelDistanceStay2.grid(row=2, column=6, sticky = E)
        self.labelLEDStay2.grid(row=3,column=6, sticky = E)

        self.labelVoltage2 = Label(self, text = "Value")
        self.labelDistance2 = Label(self, text = "Value")
        self.labelLED2 = Label(self, text = "Red")

        self.labelVoltage2.grid(row=1, column=7, sticky=W)
        self.labelDistance2.grid(row=2, column=7,sticky=W)
        self.labelLED2.grid(row=3, column=7, sticky=W)

        self.labelSpace0b = Label(self, text = "             ")
        self.labelSpace1b = Label(self, text = "             ")
        self.labelSpace2b = Label(self, text = "             ")

        self.labelSpace0b.grid(row=1, column = 5)
        self.labelSpace0b.grid(row=2, column = 5)
        self.labelSpace0b.grid(row=3, column = 5)
        #End of repeat
        
        self.labelTestName = Label(self, text = "Test Name: ")
        self.labelTestLength = Label(self, text = "Length of Test: ")
        self.entryTestName = Entry(self)
        self.entryTestLength = Entry(self)
        
        self.labelTestName.grid(row=1, column=0, sticky=E)
        self.labelTestLength.grid(row=2, column=0, sticky=E)
        self.entryTestName.grid(row=1, column=1, sticky=W)
        self.entryTestLength.grid(row=2, column=1, sticky=W)
        
        self.buttonStart = Button(self, text="Start", command = lambda:data.startTest(self, self.connections, self.buttons, self.entryTestName, self.entryTestLength))
        self.buttonStart.grid(row=3, column = 0)
        
        self.labelSpace0 = Label(self, text = "             ")
        self.labelSpace1 = Label(self, text = "             ")
        self.labelSpace2 = Label(self, text = "             ")
        
        self.labelSpace0.grid(row=1, column = 2)
        self.labelSpace0.grid(row=2, column = 2)
        self.labelSpace0.grid(row=3, column = 2)
        
        #Space repeat
        self.labelSpace0c = Label(self, text = "             ")
        self.labelSpace1c = Label(self, text = "             ")
        self.labelSpace2c = Label(self, text = "             ")
        
        self.labelSpace0c.grid(row=1, column = 8)
        self.labelSpace0c.grid(row=2, column = 8)
        self.labelSpace0c.grid(row=3, column = 8)
        #End of repeat
        
        self.buttonExit = Button(self, text="Exit", command = self.closeWindow)
        self.buttonExit.grid(row=4, column = 0)
    
    def ports(self):
        
        
        self.ports = list(serial.tools.list_ports.comports())
        
        i=0
        for self.p in self.ports:
            
            self.port = (str(self.p)).split(" ")
            self.buttons.append(Button(self, text=self.port[0], command=lambda i=i: self.connect(i)))
            self.connections.append(Label(self, text=""))
            self.connections[i].grid(column=10, row=i+1, sticky=W)
            self.buttons[i].grid(column=9, row=i+1, sticky=W)
            print(self.p)
            i+=1

    def change(self, voltage, distance, voltage2, distance2):
        self.labelVoltage.config(text=voltage)
        self.labelDistance.config(text=distance)
        self.labelVoltage2.config(text=voltage2)
        self.labelDistance2.config(text=distance2)

root = Tk()
my_gui = GUI(root)
my_gui.ports()
root.mainloop()

