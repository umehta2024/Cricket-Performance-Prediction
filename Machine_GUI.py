import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import time
from Tkinter import *
import tkMessageBox
import ttk


class GUI():

	def __init__(self):	
		self.root = Tk()
		self.root.geometry("800x600+80+30")
		self.root.title("Player Performance Prediction")
		self.root.resizable(width=False, height=False)
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(0, weight=1)
		self.panel1 = Frame(self.root,borderwidth=2,
            width=200,
            height=570,
            relief=GROOVE)
		self.panel1.grid(column= 0, row = 0, sticky=(N, S, E, W))
		self.panel2 = None
		self.best11=[]
		self.batsman=[]
		self.bowler=[]
		self.allrounder=[]
		self.oppobest=StringVar()
		
		bottom_panel= Frame(self.root, borderwidth=1, height=10, relief=SUNKEN)
		bottom_panel.grid(column=0, columnspan=2, row=1, sticky=(S,W,E))
		bottom_panel.columnconfigure(0, weight=1)
		bottom_label = Label(bottom_panel, font="Times 13")
		bottom_label.config(text="CPPP Portal " + u"\u00a9" + "2018",)
		bottom_label.grid(row=0, column=1) 
		
		self.status_label = Label(bottom_panel,font="Times 14")
		self.status_label.grid(row=0, column=0, sticky=W)
		self.welcome()
		self.root.mainloop()
	
	def welcome(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		self.panel2 = Frame(self.root,borderwidth=2,width=650,height=570,relief=GROOVE)    
		self.panel2.grid(column=1, row=0, sticky=(N, S, E, W))
		welcome_text = "\nWelcome to Cricet Player \nPerformance Prediction Portal"
		welcome_label = Label(self.panel2, text=welcome_text, font="Times 28")
		welcome_label.place(x=80, y=200)
		
		self.continue_button=Button(self.panel2,text="Continue",width=30,command=self.afterwelcome)
		self.continue_button.place(x=150, y=380)

	def afterwelcome(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)

		Label(addform, text='Menu', font="Times 28").grid(row=1, column=0,padx=180,pady=10)
		
		Button(addform, text='Overall Player Performance', font="16",width=30,command=self.overallplayerselection).grid(row=2, column=0, sticky=E,pady=5)
		Button(addform, text='Performance Against Particular Team', font="16",width=30,command=self.RunsAgainstteamselection).grid(row=3, column=0,sticky=E,pady=5)
		Button(addform, text='Find Best Playing 11', font="16",width=30,command=self.findbestplayingeleven).grid(row=4, column=0, sticky=E,pady=5)
		
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
	def RunsAgainstteamselection(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		global player1
		global opponent
		player1=StringVar()
		opponent=StringVar()
		player1.set("Player")
		opponent.set("Opponent")
		
		a=['Virat Kohli','Rohit Sharma','Shikhar Dhawan','MS Dhoni','KL Rahul','Dinesh Kartik','Ajinkya Rahane']
		b=['South Africa','England','West Indies','Australia','Srilanka','Bangladesh','Pakistan','New Zealand']
		Label(addform, text="Select Player :", font="16").grid(row=1, column=0, sticky=E)
		OptionMenu(addform, player1,*a).grid(row=1, column=1, sticky=W, pady=5, columnspan=2)
		
		Label(addform, text="Select Opponent :", font="16").grid(row=2, column=0, sticky=E)
		OptionMenu(addform, opponent,*b).grid(row=2, column=1, sticky=W, pady=5, columnspan=2)
		
		Button(addform, text='Predict', font="16",width=30,command=self.RunsAgainstteam).grid(row=3, column=0,sticky=E,pady=5)
		
		Button(addform, text='Back', font="16",width=30,command=self.afterwelcome).grid(row=4, column=0,sticky=E,pady=5)
	
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		

	
	def RunsAgainstteam(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		player_dict={'Virat Kohli':'vk.csv','Rohit Sharma':'rohit.csv','Shikhar Dhawan':'sd.csv','Ajinkya Rahane':'ar.csv','MS Dhoni':'msd.csv','KL Rahul':'kl.csv'}
		pdataset=pd.read_csv(str(player_dict[player1.get()]))
		opponent_dict={'South Africa':1,'England':2,'West Indies':3,'Australia':4,'Srilanka':5,'Bangladesh':6,'Pakistan':7,'New Zealand':8}
		oppoval=pdataset.loc[pdataset['Oppo'] == opponent_dict[opponent.get()]]
		X=oppoval.iloc[:,4:7].values
		y=oppoval.iloc[:,3].values
		X_train,X_test,y_train,y_test = train_test_split(X, y,test_size = 0.3,random_state=0)
		from sklearn.preprocessing import StandardScaler
		sc_x = StandardScaler()
		X_train = sc_x.fit_transform(X_train)
		X_test = sc_x.transform(X_test)
		sc_y = StandardScaler()
		y_train = sc_y.fit_transform([y_train])
		from sklearn.linear_model import LinearRegression
		regressor=LinearRegression()
		regressor.fit(X,y)
		y_pred=regressor.predict(X_test)
		
		
		Label(addform, text='Player Performance Prediction', font="24").grid(row=1, column=0, sticky=E,pady=10)
		Label(addform, text='Player : '+str(player1.get()), font="16").grid(row=2, column=0, sticky=E,pady=10)
		Label(addform, text="Runs : "+str(abs(int(y_pred[0]))), font="16").grid(row=3, column=0, sticky=E,pady=10)
		Label(addform, text="Strike Rate : "+str(abs(int(y_pred[1]))), font="16").grid(row=4, column=0, sticky=E,pady=10)
		Label(addform, text="Accuracy : "+str(regressor.score(X,y)*100), font="16").grid(row=5, column=0, sticky=E,pady=10)	
		Button(addform, text='Back', font="16",width=30,command=self.RunsAgainstteamselection).grid(row=6, column=0,sticky=E,pady=5)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
	def overallplayerselection(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		global player2
		player2=StringVar()
		player2.set("Player")	
		a1=['Virat Kohli','Rohit Sharma']
		
		Label(addform, text="Select Player :", font="16").grid(row=1, column=0, sticky=E)
		OptionMenu(addform, player2,*a1).grid(row=1, column=1, sticky=W, pady=5, columnspan=2)
		

		Button(addform, text='Predict', font="16",width=30,command=self.overallplayerperfomace).grid(row=3, column=0,sticky=E,pady=5)
		
		Button(addform, text='Back', font="16",width=30,command=self.afterwelcome).grid(row=4, column=0,sticky=E,pady=5)
	
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
			
		
	def overallplayerperfomace(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		
		player_dict={'Virat Kohli':'vk.csv','Rohit Sharma':'rohit.csv'}
		
		dataset=pd.read_csv(player_dict[player2.get()])

		X=dataset.iloc[:,4:7].values
		y=dataset.iloc[:,3].values
		X_train,X_test,y_train,y_test = train_test_split(X, y,test_size = 0.3,random_state=0)

		from sklearn.preprocessing import StandardScaler
		sc_x = StandardScaler()
		X_train = sc_x.fit_transform(X_train)
		X_test = sc_x.transform(X_test)
		sc_y = StandardScaler()
		y_train = sc_y.fit_transform([y_train])

		from sklearn.linear_model import LinearRegression
		regressor=LinearRegression()
		regressor.fit(X,y)
		y_pred=regressor.predict(X_test)
		print y_pred 
		Label(addform, text='Overall Player Performance \nPrediction for Next Match', font="24").grid(row=1, column=0, sticky=E,pady=10)
		Label(addform, text='Runs'+str(y_pred[0]), font="16").grid(row=2, column=0, sticky=E,pady=10)
		Label(addform, text='Strike Rate'+str(y_pred[1]), font="16").grid(row=3, column=0, sticky=E,pady=10)
		Label(addform, text='Accuracy : '+str(regressor.score(X,y)*100), font="16").grid(row=4, column=0, sticky=E,pady=10)
		
		Button(addform, text='Back', font="16",width=30,command=self.overallplayerselection).grid(row=5, column=0,sticky=E,pady=5)
		
		

		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
	def findbestplayingeleven(self):
		def bestteam():
			if len(self.batsman)==0 or len(self.bowler)==0 or len(self.allrounder)==0:
				tkMessageBox.showinfo("Warning","Please Provide All Details", icon='warning')
			else:
				self.interation_for_best()
				self.printfinalteam()
				
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Button(addform, text='Select Batsman', font="16",width=30,command=self.findbatsman).grid(row=2, column=0, sticky=E,pady=5)
		Button(addform, text='Select Bowler', font="16",width=30,command=self.findbowler).grid(row=3, column=0,sticky=E,pady=5)
		Button(addform, text='Select All rounder', font="16",width=30,command=self.findallrounder).grid(row=4, column=0, sticky=E,pady=5)
		Label(addform, text='Select Opponent Team : ', font="16").grid(row=5, column=0, sticky=E,pady=10)
		opponent_team=['South Africa','England','West Indies','Australia','Srilanka','Bangladesh','Pakistan','New Zealand']
		OptionMenu(addform,self.oppobest,*opponent_team).grid(row=6, column=0, sticky=W, pady=5, columnspan=2)
		Button(addform, text='Find Best Team', font="16",width=30,command=bestteam).grid(row=8, column=0, sticky=E,pady=5)
		Button(addform, text='Back', font="16",width=30,command=self.afterwelcome).grid(row=9, column=0, sticky=E,pady=5)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
	
				
		
	def findbatsman(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		global opt
		opt = []
		def chkbox_checked():
			for ix, item in enumerate(cb):
				opt[ix]=(cb_v[ix].get())
		mylist = ['Virat Kohli','Rohit Sharma','Shikhar Dhawan','Ajinkya Rahane','KL Rahul' ,'MS Dhoni','Rishabh Pant','Dinesh Kartik']
		cb = []
		cb_v = []
		for ix, text in enumerate(mylist):
			cb_v.append(StringVar())
			off_value=0
			cb.append(Checkbutton(addform, text=text, onvalue=text,offvalue=off_value,
				                     variable=cb_v[ix],
				                     command=chkbox_checked))
			cb[ix].grid(row=ix, column=0, sticky='w')
			opt.append(off_value)
			cb[-1].deselect() #uncheck the boxes initially.		

		def finalsub():
			avail={'Virat Kohli':'vk.csv','Rohit Sharma':'rohit.csv','Shikhar Dhawan':'Sd.csv','KL Rahul':'kl.csv','Ajinkya Rahane':'ar.csv','Rishabh Pant':'rp.csv','Dinesh Kartik':'dk.csv','MS Dhoni':'msd.csv'}
			search_list=[]
			for i in opt:
				if i != '0' :
					search_list.append(avail[i])
					self.findbestplayingeleven()
				else:
					continue
			self.batsman=self.batsman+search_list
			
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
		
		Button(addform, text='Submit', font="16",width=30,command=finalsub).grid(row=len(mylist)+1, column=0, sticky=E,pady=5)
		Button(addform, text='Back', font="16",width=30,command=self.findbestplayingeleven).grid(row=len(mylist)+2, column=0, sticky=E,pady=5)
		
	def findbowler(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		global opt
		opt = []
		def chkbox_checked():
			for ix, item in enumerate(cb):
				opt[ix]=(cb_v[ix].get())
		mylist = ['Jasprit Bumrah','Bhuvneshvar Kumar','Mohhamad Shami','Umesh Yadav','Ishant Sharma','Kuldeep Yadav','Yuzevendra Chahal','Ravi Jadeja','Ravi Ashvin']
		cb = []
		cb_v = []
		for ix, text in enumerate(mylist):
			cb_v.append(StringVar())
			off_value=0
			cb.append(Checkbutton(addform, text=text, onvalue=text,offvalue=off_value,
				                     variable=cb_v[ix],
				                     command=chkbox_checked))
			cb[ix].grid(row=ix, column=0, sticky='w')
			opt.append(off_value)
			cb[-1].deselect() #uncheck the boxes initially.		

		def finalsub():
			avail={'Jasprit Bumrah':'jb.csv','Bhuvneshvar Kumar':'bk.csv','Mohhamad Shami':'ms.csv','Umesh Yadav':'uy.csv','Ishant Sharma':'Is.csv','Kuldeep Yadav':'ky.csv','Yuzevendra Chahal':'yc.csv','Ravi Jadeja':'rj.csv','Ravi Ashvin':'ra.csv'}
			search_list=[]
			for i in opt:
				if i != '0' :
					search_list.append(avail[i])
					self.findbestplayingeleven()
				else:
					continue
			self.bowler=self.bowler+search_list
			
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		Button(addform, text='Submit', font="16",width=30,command=finalsub).grid(row=len(mylist)+1, column=0, sticky=E,pady=5)
		Button(addform, text='Back', font="16",width=30,command=self.findbestplayingeleven).grid(row=len(mylist)+2, column=0, sticky=E,pady=5)

	def findallrounder(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		global opt
		opt = []
		def chkbox_checked():
			for ix, item in enumerate(cb):
				opt[ix]=(cb_v[ix].get())
		mylist = ['Hardik Pandya','Krunal Pandya','Washington Sundar','Hanuma Vihari',]
		cb = []
		cb_v = []
		for ix, text in enumerate(mylist):
			cb_v.append(StringVar())
			off_value=0
			cb.append(Checkbutton(addform, text=text, onvalue=text,offvalue=off_value,
				                     variable=cb_v[ix],
				                     command=chkbox_checked))
			cb[ix].grid(row=ix, column=0, sticky='w')
			opt.append(off_value)
			cb[-1].deselect() #uncheck the boxes initially.		

		def finalsub():
			avail={'Hardik Pandya':'hp.csv','Krunal Pandya':'kp.csv','Hanuma Vihari':'hv.csv','Washington Sundar':'ws.csv'}
			search_list=[]
			for i in opt:
				if i != '0' :
					search_list.append(avail[i])
					self.findbestplayingeleven()
				else:
					continue
			self.allrounder=self.allrounder+search_list
			
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		Button(addform, text='Submit', font="16",width=30,command=finalsub).grid(row=len(mylist)+1, column=0, sticky=E,pady=5)
		Button(addform, text='Back', font="16",width=30,command=self.findbestplayingeleven).grid(row=len(mylist)+2, column=0, sticky=E,pady=5)

	def interation_for_best(self):
		def selectbestteam(player_name,oppo_id):
			print player_name
			print oppo_id
			pdataset=pd.read_csv(player_name)
			opponent_dict={'South Africa':1,'England':2,'West Indies':3,'Australia':4,'Srilanka':5,'Bangladesh':6,'Pakistan':7,'New Zealand':8}
			oppoval=pdataset.loc[pdataset['Oppo'] == opponent_dict[oppo_id]]
			X=oppoval.iloc[:,4:7].values
			y=oppoval.iloc[:,3].values
			X_train,X_test,y_train,y_test = train_test_split(X, y,test_size = 0.3,random_state=0)
			from sklearn.preprocessing import StandardScaler
			sc_x = StandardScaler()
			X_train = sc_x.fit_transform(X_train)
			X_test = sc_x.transform(X_test)
			sc_y = StandardScaler()
			y_train = sc_y.fit_transform([y_train])
			from sklearn.linear_model import LinearRegression
			regressor=LinearRegression()
			regressor.fit(X,y)
			y_pred=regressor.predict(X_test)
			return y_pred[0]
			
		finalbatsman={}
		finalbowler={}
		finalallrounder={}
		"""
		for i in range(0,2):
			val=selectbestteam(self.batsman[i],self.oppobest.get())
			finalbatsman[i]=val
		for i in (0,1):
			val=selectbestteam(self.bowler[i],self.oppobest.get())
			finalbowler[i]=val
		"""
		self.printfinalteam()
	
	
	def printfinalteam(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		convert_dicto={'jb.csv':'Jasprit Bumrah','bk.csv':'Bhuvneshwar Kumar','ms.csv':'Mohhamad Shami','uy.csv':'Umesh Yadav','Is.csv':'Ishant Sharma','ky.csv':'Kuldeep Yadav','yc.csv':'Yuzavendra Chahal','rj.csv':'Ravi Jadeja','ra.csv':'Ravi Ashwin','ws.csv':'Washington Sunder','hv.csv':'Hanuma Vihari','hp.csv':'Hardik Pandya','kp.csv':'Krunal Pandya','vk.csv': 'Virat Kohli','rohit.csv':'Rohit Sharma','Sd.csv':'Shikhar Dhawan','kl.csv':'KL Rahul','ar.csv':'Ajinkya Rahane','rp.csv':'Rishab Pant','dk.csv':'Dinesh Kartik','msd.csv':'MS Dhoni'}
		
		Label(addform, text='Final Team ', font="16").grid(row=0, column=0, sticky=E,pady=10)
		z=1
		for i in range(0,5):
			Label(addform, text=convert_dicto[str(self.batsman[i])], font="16").grid(row=z, column=0, sticky=E,pady=10)
			z=z+1
		uh=z+1
		for i in range(0,2):
			Label(addform, text=convert_dicto[str(self.allrounder[i])], font="16").grid(row=uh, column=0, sticky=E,pady=10)
			uh=uh+1
			
		uh1=uh+1
		for i in range(0,4):
			Label(addform, text=convert_dicto[str(self.bowler[i])], font="16").grid(row=uh1, column=0, sticky=E,pady=10)
			uh1=uh1+1
			
		Button(addform, text='Home', font="16",width=30,command=self.afterwelcome).grid(row=uh1+1, column=0, sticky=E,pady=5)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
		
if __name__ == '__main__':
    g = GUI()
    	
	
	
	
	
