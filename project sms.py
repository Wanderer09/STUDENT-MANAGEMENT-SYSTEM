from tkinter import*
from tkinter import messagebox
from tkinter import scrolledtext
from cx_Oracle import*
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import numpy as np
import socket
import requests
import bs4
import sys

dimension = "1200x500+50+50"
password = "system/abc123"

def on_closing():          #for conformation while closing
    if messagebox.askokcancel("Exit", "Do you want to Exit?"):
        root.destroy()

def f1():           #add
	root.withdraw()
	adst.deiconify()
	
def f2():	    #addback
	adst.withdraw()
	root.deiconify()

def f3():	    #update
	root.withdraw()
	upst.deiconify()
	
def f4():	    #updateback
	upst.withdraw()
	root.deiconify()

def f5():	    #delete
	root.withdraw()
	dest.deiconify()
	
def f6():	    #deleteback
	dest.withdraw()
	root.deiconify()

def f7(): 	    #view
	stdataview.delete(1.0, END)
	root.withdraw()
	vist.deiconify()
	con = None
	try:
		con = connect(password)
		cursor = con.cursor()
		sql = "select * from studentpro order by rno"
		cursor.execute(sql)
		data = None
		data = cursor.fetchall()
		msgv = ""
		msgv = msgv + "Total Number of Rows : "+ str(cursor.rowcount)+"\n\n\n"
		if cursor.rowcount != 0:
			list = []
			for d in data:
				dict = {'Roll No.' : d[0], 'Name' : d[1] , 'Marks' : d[2]}
				list.append(dict)
			msgv = msgv + str(pd.DataFrame(list)) + "\n\n"#create and  Print the data
		stdataview.insert(INSERT, msgv)
	except DatabaseError as e:
		messagebox.showerror("DBerror : ",""+str(e))
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
	finally:
		if con is not None:
			con.close()
def f8():#for view to root
	vist.withdraw()
	root.deiconify()

def f9():#for addition in DB
	error = 0
	#rno validation
	try:
		rno = int(entAddRno.get())
		if rno < 0:
			messagebox.showerror("error : ","Roll No. can't be negative.")
			error += 1
			entAddRno.delete(0, END)
			entAddRno.focus()
	except ValueError as e:
		messagebox.showerror("error : ","Please Enter Integer only in Roll No..")
		error += 1
		entAddRno.delete(0, END)
		entAddRno.focus()
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
		error += 1
		entAddRno.delete(0, END)
		entAddRno.focus()
	#name validation
	name = entAddName.get()
	if len(name) < 2:
		messagebox.showerror("error : ","Please Enter at least two alphabet in Name.")
		error += 1
		entAddName.focus()
	else:
		for letter in name:
			if not letter.isalpha():
				messagebox.showerror("error : ","Please Enter alphabet only.")
				error += 1
				entAddName.delete(0, END)
				entAddName.focus()
				break
	#marks validation		
	try:
		marks = int(entAddMarks.get())
		if marks < 0 or marks > 100:
			messagebox.showerror("error : ","Marks should be lie between 0 to 100.")
			error += 1
			entAddMarks.delete(0, END)
			entAddMarks.focus()
	except ValueError as e:
		messagebox.showerror("error : ","Please Enter Integer only in Marks.")
		error += 1
		entAddMarks.delete(0, END)
		entAddMarks.focus()
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
		error += 1
		entAddMarks.delete(0, END)
		entAddMarks.focus()
	if error == 0:#if no error then conn to DB
		con = None
		try:
			con = connect(password)
			cursor = con.cursor()
			sql = "insert into studentpro values ('%d', '%s', '%d')"
			args = (rno, name, marks)
			cursor.execute(sql % args)
			con.commit()
			messagebox.showinfo("Sucess","Record Inserted.")
			entAddRno.delete(0, END)
			entAddName.delete(0, END)
			entAddMarks.delete(0, END)
			entAddRno.focus()
		except IntegrityError:
			con.rollback()
			messagebox.showerror("DBerror : ","Roll No. "+str(rno)+" is already assigned")
			entAddRno.delete(0, END)
			entAddRno.focus()
		except DatabaseError as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))	
		except Exception as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))
		finally:
			if con is not None:
				con.close()

def f10():#for update in DB
	error = 0
	#rno validation
	try:
		rno = int(entUpdateRno.get())
		if rno < 0:
			messagebox.showerror("error : ","Roll No. can't be negative.")
			error += 1
			entUpdateRno.delete(0, END)
			entUpdateRno.focus()
	except ValueError as e:
		messagebox.showerror("error : ","Please Enter Integer only in Roll No..")
		error += 1
		entUpdateRno.delete(0, END)
		entUpdateRno.focus()
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
		error += 1
		entUpdateRno.delete(0, END)
		entUpdateRno.focus()
	#name validation
	name = entUpdateName.get()
	if len(name) < 2:
		messagebox.showerror("error : ","Please Enter at least two alphabet in Name.")
		error += 1
		entUpdateName.focus()
	else:
		for letter in name:
			if not letter.isalpha():
				messagebox.showerror("error : ","Please Enter alphabet only.")
				error += 1
				entUpdateName.delete(0, END)
				entUpdateName.focus()
				break
	#marks validation		
	try:
		marks = int(entUpdateMarks.get())
		if marks < 0 or marks > 100:
			messagebox.showerror("error : ","Marks should be lie between 0 to 100.")
			error += 1
			entUpdateMarks.delete(0, END)
			entUpdateMarks.focus()
	except ValueError as e:
		messagebox.showerror("error : ","Please Enter Integer only in Marks.")
		error += 1
		entUpdateMarks.delete(0, END)
		entUpdateMarks.focus()
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
		error += 1
		entUpdateMarks.delete(0, END)
		entUpdateMarks.focus()
	if error == 0:#if no error then conn to DB
		con = None
		try:
			con = connect(password)
			cursor = con.cursor()
			sql = "select * from studentpro where rno = '%d'"
			args = (rno)
			cursor.execute(sql % args)
			row = None
			row = cursor.fetchone()
			print(row)
			if row == None:
				messagebox.showerror("Sucess","Roll No. "+str(rno)+" is not assigned")
				entUpdateRno.delete(0, END)
				entUpdateRno.focus()
			else:
				sql = "UPDATE student1 SET name = '%s' , marks = '%d' WHERE rno = '%d'"
				args = (name, marks, rno)
				cursor.execute(sql % args)
				con.commit()
				messagebox.showinfo("Sucess","Record Updated.")
				entUpdateRno.delete(0, END)
				entUpdateName.delete(0, END)
				entUpdateMarks.delete(0, END)
				entUpdateRno.focus()
		except DatabaseError as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))	
		except Exception as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))
		finally:
			if con is not None:
				con.close()

def f11():#for delete in DB
	error = 0
	#rno validation
	try:
		rno = int(entDeleteRno.get())
		if rno < 0:
			messagebox.showerror("error : ","Roll No. can't be negative.")
			error += 1
			entDeleteRno.delete(0, END)
			entDeleteRno.focus()
	except ValueError as e:
		messagebox.showerror("error : ","Please Enter Integer only in Roll No..")
		error += 1
		entDeleteRno.delete(0, END)
		entDeleteRno.focus()
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
		error += 1
		entDeleteRno.delete(0, END)
		entDeleteRno.focus()
	#if no error then conn to DB
	if error == 0:
		con = None
		try:
			con = connect(password)
			cursor = con.cursor()
			sql = "select * from studentpro where rno = '%d'"
			args = (rno)
			cursor.execute(sql % args)
			row = None
			row = cursor.fetchone()
			print(row)
			if row == None:
				messagebox.showerror("Sucess","Roll No. "+str(rno)+" is not assigned")
				entDeleteRno.delete(0, END)
				entDeleteRno.focus()
			else:
				sql = "delete from student where rno = '%d'"
				args = (rno)
				cursor.execute(sql % args)
				con.commit()
				messagebox.showinfo("Sucess","Record Deleted.")
				entDeleteRno.delete(0, END)
				entDeleteRno.focus()
		except DatabaseError as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))	
		except Exception as e:
			con.rollback()
			messagebox.showerror("DBerror : ",""+str(e))
		finally:
			if con is not None:
				con.close()
	
def f12():#for root to graph
	con = None
	try:
		con = connect(password)
		cursor = con.cursor()
		sql = "select * from studentpro order by marks desc"
		cursor.execute(sql)
		data = None
		data = cursor.fetchall()
		if cursor.rowcount >= 5:
			mlist, nlist = [], []
			for d in data:
				nlist.append(d[1])
				mlist.append(d[2])
			x = np.arange(len(nlist))
			plt.bar(nlist , mlist, label = "MARKS",width=0.45, color='red')
			plt.xticks(x, nlist, fontsize=7, rotation=30)
			plt.title("Students Graph")
			plt.xlabel("Student Name")
			plt.ylabel("Marks")
			plt.legend()
			plt.grid()
			plt.savefig('pic.png')
			plt.figsize=(4,6)
			plt.show()
			plt.close()
		else:
			messagebox.showerror("Error","Please Insert at least 5 Records")
	except DatabaseError as e:
		messagebox.showerror("DBerror : ",""+str(e))
	except Exception as e:
		messagebox.showerror("error : ","Issue "+str(e))
	finally:
		if con is not None:
			con.close()
		
try:#for City, Temperature , Msg from Internet
	socket.create_connection(("www.google.com", 80))
	res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	quote = soup.find('img', {"class":"p-qotd"})
	msg = quote['alt']
	print(msg)
	res = requests.get("http://ipinfo.io")
	data = res.json()
	city = data['city']
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res = requests.get(api_address)
	data = res.json()
	print("City : ", city)
	temp = data['main']['temp']
	print("Temperature : ",temp)
except OSError as e:
	showwarning("Check Network ", ""+str(e))

root = Tk()
root.title("Student. Management .System")
root.geometry(dimension)
btnAdd = Button(root, text = "Add", font = ("arial", 16, 'bold'), width = 16, command = f1)
btnView = Button(root, text = "View", font = ("arial", 16, 'bold'), width = 16, command = f7)
btnUpdate = Button(root, text = "Update", font = ("arial", 16, 'bold'), width = 16, command = f3)
btnDelete = Button(root, text = "Delete", font = ("arial", 16, 'bold'), width = 16, command = f5)
btnGraph = Button(root, text = "Graph", font = ("arial", 16, 'bold'), width = 16, command = f12)
lblCity = Label(root, text = "City : " + city, font = ("Book Antiqua", 16, 'bold'))
lblTemp = Label(root, text = "Temperature : " + str(temp) + " C", font = ("Book Antiqua", 16, 'bold'))
lblQotd = Label(root, text = msg, font = ("Chopin Script", 12, 'bold'))
btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnGraph.pack(pady = 10)
lblCity.pack(side = LEFT, padx = 10, pady = 10)
lblTemp.pack(side = RIGHT, padx = 10, pady = 10)
lblQotd.pack(side = BOTTOM)

adst = Toplevel(root)
adst.title("Add Student")
adst.geometry(dimension)
lblAddRno = Label(adst, text = "Enter Roll No. : ", font = ("arial", 16, 'bold'))
entAddRno = Entry(adst, bd = 5, font = ("arial", 16, 'bold'))
lblAddName = Label(adst, text = "Enter Name : ", font = ("arial", 16, 'bold'))
entAddName = Entry(adst, bd = 5, font = ("arial", 16, 'bold'))
lblAddMarks = Label(adst, text = "Enter Marks : ", font = ("arial", 16, 'bold'))
entAddMarks = Entry(adst, bd = 5, font = ("arial", 16, 'bold'))
btnAddSave = Button(adst, text = "Save", font = ("arial", 16, 'bold'), width = 16, command = f9)
btnAddBack = Button(adst, text = "Back", font = ("arial", 16, 'bold'), width = 16, command = f2)
lblAddRno.pack(pady = 10)
entAddRno.pack(pady = 10)
lblAddName.pack(pady = 10)
entAddName.pack(pady = 10)
lblAddMarks.pack(pady = 10)
entAddMarks.pack(pady = 10)
btnAddSave.pack(pady = 10)
btnAddBack.pack(pady = 10)
adst.protocol("WM_DELETE_WINDOW", on_closing)
adst.withdraw()

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry(dimension)
lblUpdateRno = Label(upst, text = "Enter Roll No. : ", font = ("arial", 16, 'bold'))
entUpdateRno = Entry(upst, bd = 5, font = ("comic sans ms", 16, 'bold'))
lblUpdateName = Label(upst, text = "Enter Name : ", font = ("arial", 16, 'bold'))
entUpdateName = Entry(upst, bd = 5, font = ("comic sans ms", 16, 'bold'))
lblUpdateMarks = Label(upst, text = "Enter Marks : ", font = ("arial", 16, 'bold'))
entUpdateMarks = Entry(upst, bd = 5, font = ("comic sans ms", 16, 'bold'))
btnUpdateSave = Button(upst, text = "Update", font = ("arial", 16, 'bold'), width = 16, command = f10)
btnUpdateBack = Button(upst, text = "Back", font = ("arial", 16, 'bold'), width = 16, command = f4)
lblUpdateRno.pack(pady = 10)
entUpdateRno.pack(pady = 10)
lblUpdateName.pack(pady = 10)
entUpdateName.pack(pady = 10)
lblUpdateMarks.pack(pady = 10)
entUpdateMarks.pack(pady = 10)
btnUpdateSave.pack(pady = 10)
btnUpdateBack.pack(pady = 10)
upst.protocol("WM_DELETE_WINDOW", on_closing)
upst.withdraw()

dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry(dimension)
lblDeleteRno = Label(dest, text = "Enter Roll No. : ", font = ("arial", 16, 'bold'))
entDeleteRno = Entry(dest, bd = 5, font = ("arial", 16, 'bold'))
btnDeleteSave = Button(dest, text = "Delete", font = ("arial", 16, 'bold'), width = 16, command = f11)
btnDeleteBack = Button(dest, text = "Back", font = ("arial", 16, 'bold'), width = 16, command = f6)
lblDeleteRno.pack(pady = 10)
entDeleteRno.pack(pady = 10)
btnDeleteSave.pack(pady = 10)
btnDeleteBack.pack(pady = 10)
dest.protocol("WM_DELETE_WINDOW", on_closing)
dest.withdraw()

vist = Toplevel(root)
vist.title("View Student")
vist.geometry(dimension)
stdataview = scrolledtext.ScrolledText(vist, height = 20, font = ("arial", 10, 'bold'))
btnViewBack = Button(vist, text = "Back", font = ("arial", 16, 'bold'), width = 16, command = f8)
stdataview.pack(pady = 10)
btnViewBack.pack(side = BOTTOM, pady = 10)
vist.protocol("WM_DELETE_WINDOW", on_closing)
vist.withdraw()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
