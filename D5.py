from tkinter import *  #For designing GUI
from tkcalendar import Calendar #For taking date input from a calendar
import mysql.connector #For using mysql database

# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Sample Text ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Sample Text ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #

centralDb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="goodpassword",
    database="InstituteA"
)

dbCursor = centralDb.cursor() #dbCursor will be our agent to execute all the sql commands here

background_login= 'tomato'
background_student = 'lime'
background_faculty = 'cyan'
background_admin = 'green'
HEIGHT = 700
WIDTH = 900

loginDic = {    #I'm using this to make the code easier to understand
    'id' : 0,
    'password' : 1,
    'name' : 2,
    'type' : 3
}

root = Tk()
root.title("Student Attendance Management")
root.geometry(f"{WIDTH}x{HEIGHT}+300+50") #The '+300+50' is used to modify the position of the main window when the program starts

showAxis = True

class User:
    id = 'null'
    password = 'null'
    name = 'null'
    type = 'null'

class SearchResult:
    id = 'null'
    password = 'null'
    name = 'null'
    type = 'null'
    course = ''

class Attendance:
    cid = 'null'
    sid = 'null'
    fid = 'null'
    att = 0
    date = 'dd-mm-yyyy'

def DoesUserExist(inputLoginId):
    query = "select exists(select Password from Credentials where Id = %s)" #Query to check if given use id exists
    val = (inputLoginId, )
    dbCursor.execute(query, val) #Chekc if Id given by user exists

    for x in dbCursor:
            idExistance = x

    if idExistance[0] == 1:
        return 1
    else:
        return 0
    


# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Loging Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
def printStuff(inputLoginId, inputLoginPassword):
        print("Id: ",inputLoginId, "\nPassword: ",inputLoginPassword)

class LoginFrame:
    def GetAndCheckCredentials(self):
        global user1

        #Get Credentials
        inputLoginId = self.entryLoginId.get()
        inputLoginPassword = self.entryLoginPass.get()

        self.labelWrongUser.place_forget()
        self.labelWrongPassword.place_forget()
        val = (inputLoginId, )

        if DoesUserExist(inputLoginId) == 1: #If user id exists then proceed
            query = "SELECT * FROM Credentials WHERE Id = %s" #Get all the information about the user id from Credentials table
            dbCursor.execute(query, val)

            for y in dbCursor:
                temp = y
            user1.id = temp[loginDic['id']]
            user1.name = temp[loginDic['name']]
            user1.password = temp[loginDic['password']]
            user1.type = temp[loginDic['type']]

            if user1.password == inputLoginPassword: #Check if given password is correct
                inputLoginId = 'null'
                inputLoginPassword = 'null'
                self.frameLogin.destroy()
                
                if user1.type == 'student':
                    studentFrame = StudentFrame()
                    studentFrame.Create()
                elif user1.type == 'faculty':
                    facultyFrame = FacultyFrame()
                    facultyFrame.Create()
                elif user1.type == 'admin':
                    adminFrame = AdminFrame()
                    adminFrame.Create()
                else:
                    exit()
            else:
                print("Wrong2")
                self.labelWrongPassword.place(relx = 0.37, rely = 0.61) #Shows the message that wrong password
        else:
            print("Wrong1")
            self.labelWrongUser.place(relx = 0.46, rely = 0.61) # Shows the message that user does not exist
                
        printStuff(inputLoginId, inputLoginPassword)
    
    def Create(self): #Creates and places all the widgets of this frame. Didn't use constructor because then I would have to delete the object and create it again to place this widgets again.Insted I will just delete the widgetand create them again using this function. Kind of same thing I guess.
        self.frameLogin = Frame(root, bg = background_login, height = HEIGHT, width = WIDTH)
        self.frameLogin.place(relx = 0, rely = 0)

        self.labelLogingId = Label(self.frameLogin, text='Login ID', bg = background_login)
        self.labelLogingId.place(relx = 0.4, rely = 0.45)
        self.entryLoginId = Entry(self.frameLogin, width = 20)
        self.entryLoginId.place(relx = 0.47, rely = 0.45)

        self.labelLogingPass = Label(self.frameLogin, text='Password', bg = background_login)
        self.labelLogingPass.place(relx = 0.4, rely = 0.5)
        self.entryLoginPass = Entry(self.frameLogin, width = 20)
        self.entryLoginPass.place(relx = 0.47, rely = 0.5)

        self.labelWrongUser = Label(self.frameLogin, text = 'User does not exist!', bg = background_login)
        self.labelWrongPassword = Label(self.frameLogin, text = 'Wrong Password!\nPlease contact the admin if you forgot the password.', bg = background_login)

        self.buttonLoginSubmit = Button(self.frameLogin, text = 'Login', command  = self.GetAndCheckCredentials)
        self.buttonLoginSubmit.place(relx = 0.50, rely = 0.55)
# ^^^^^^^^^^^^^ Loging Frame ^^^^^^^^^^^^^ #


# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Student Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
class StudentFrame:
    def Create(self):
        self.frameStudent = Frame(root, bg = background_student, height = HEIGHT, width = WIDTH)
        self.frameStudent.place(relx = 0, rely = 0)

        self.buttonGenReport = Button(self.frameStudent, text = 'Generate Report')
        self.buttonGenReport.place(relx = 0.45, rely = 0.45)

        self.buttonLeaveApp = Button(self.frameStudent, text = 'Leave Application')
        self.buttonLeaveApp.place(relx = 0.445, rely = 0.50)
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Student Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #


# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Faculty Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
class FacultyFrame:
    def ChangeToAttendanceFrame(self, sourceFrame): 
        sourceFrame.destroy()
        attendanceFrame = AttendanceFrame()
        attendanceFrame.Create()

    def Create(self):
        self.frameFaculty = Frame(root, bg = background_faculty, height = HEIGHT, width = WIDTH)
        self.frameFaculty.place(relx = 0, rely = 0)

        self.buttonGenReport = Button(self.frameFaculty, text = 'Generate Report')
        self.buttonGenReport.place(relx = 0.45, rely = 0.45)

        self.attendance = Button(self.frameFaculty, text = 'Take Attendance', command = lambda: self.ChangeToAttendanceFrame(self.frameFaculty))
        self.attendance.place(relx = 0.448, rely = 0.50)
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Faculty Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #


# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Admin Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
class AdminFrame:
    def ChangeToARMFrame(self, sourceFrame):
        sourceFrame.destroy()
        armFrame = ARMFrame()
        armFrame.Create()
    
    def Create(self):
        self.frameAdmin = Frame(root, bg = background_admin, height = HEIGHT, width = WIDTH)
        self.frameAdmin.place(relx = 0, rely = 0)

        self.buttonGenReport = Button(self.frameAdmin, text = 'Generate Report')
        self.buttonGenReport.place(relx = 0.45, rely = 0.45)

        self.addMembers = Button(self.frameAdmin, text = 'Add/Remove/Modify Members', command = lambda: self.ChangeToARMFrame(self.frameAdmin))
        self.addMembers.place(relx = 0.40, rely = 0.50)

        #self.modifyMembers = Button(self.frameAdmin, text = 'Modify Members')
        #self.modifyMembers.place(relx = 0.445, rely = 0.55)

        self.backup = Button(self.frameAdmin, text = 'Backup Database')
        self.backup.place(relx = 0.445, rely = 0.55)
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Admin Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #


# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Add/Remove/Modyfy User Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
class ARMFrame:
    def ChangeToAdminFrame(self, sourceFrame):
        sourceFrame.destroy()
        adminFrame = AdminFrame()
        adminFrame.Create()

    def updateListbox(self):
            self.entryARMCourse.delete(0, END)  #Emptying the current listing in the listbox
            query = "select CourseReg.Cid, Cname from CourseReg inner join CourseAlloc on CourseAlloc.Cid = CourseReg.Cid where CourseReg.Sid = %s"
            val = (sr1.id, )
            dbCursor.execute(query, val)
            temp2 = []
            for y in dbCursor:
                #print(y)
                temp2.append(y[0])
                temp2.append(y[1])
            for x in range(0, len(temp2), 2):
                sr1.course = "[" + temp2[x] + "]" + " " + temp2[x+1]
                self.entryARMCourse.insert(END, sr1.course)
            print(sr1.course)

    def ShowCourses(self):
            self.listboxARMCourseList.delete(0, END)  #Emptying the current listing in the listbox
            query = "select Cid, Cname from CourseAlloc"
            val = ()
            dbCursor.execute(query, val)
            temp2 = []
            for y in dbCursor:
                print(y)
                temp2.append(y[0])
                temp2.append(y[1])
            for x in range(0, len(temp2), 2):
                sr1.course = "[" + temp2[x] + "]" + " " + temp2[x+1]
                self.listboxARMCourseList.insert(END, sr1.course)

    def ClearSearch(self):
        self.entryARMId.delete(0, END)
        self.entryARMPassword.delete(0, END)
        self.entryARMName.delete(0, END)
        self.entryARMType.delete(0, END)
            
    
    def SearchId(self):
        qid = self.entryARMSearch.get()
        print("___________________")
        print(type(qid))

        if DoesUserExist(qid) == 1:
            query = "SELECT * FROM Credentials WHERE Id = %s" #Get all the information about the user id from Credentials table
            val = (qid, )
            dbCursor.execute(query, val)

            for y in dbCursor:
                temp = y
            sr1.id = temp[loginDic['id']]
            sr1.name = temp[loginDic['name']]
            sr1.password = temp[loginDic['password']]
            sr1.type = temp[loginDic['type']]

            self.ClearSearch()
            self.entryARMId.insert(0, sr1.id)
            self.entryARMPassword.insert(0, sr1.password)
            self.entryARMName.insert(0, sr1.name)
            self.entryARMType.insert(0, sr1.type)

            self.updateListbox()
            self.ShowCourses()
            
            #self.entryARMCourse.delete("1.0", END)
            #self.entryARMCourse.insert(END, sr1.course)
        else:
            self.labelARMMessage.config(text = "User does not exist!")
            self.labelARMMessage.after(2000, lambda: self.labelARMMessage.config(text=''))
    
    def RemoveCourse(self):
        index = self.entryARMCourse.curselection()
        if index:
            temp1 = self.entryARMCourse.get(index)
            courseCode = temp1[temp1.find("[")+1:temp1.find("]")]
            query = "delete from CourseReg where Sid = %s and Cid = %s"
            val = (sr1.id, courseCode, )
            dbCursor.execute(query, val)
            self.updateListbox()

    def AddCourse(self):
        if sr1.type == 'student':
            index = self.listboxARMCourseList.curselection()
            if index:
                temp1 = self.listboxARMCourseList.get(index)
                courseCode = temp1[temp1.find("[")+1:temp1.find("]")]
                query = "insert into CourseReg (Sid, Cid) values(%s, %s)"
                val = (sr1.id, courseCode, )
                dbCursor.execute(query, val)
                self.updateListbox()
        else:
            self.labelARMMessage.config(text = "Only students can register for courses!")
            self.labelARMMessage.after(2000, lambda: self.labelARMMessage.config(text=''))
    def ClearSearchResult(self):
        sr1.id = 'null'
        sr1.name = 'null'
        sr1.password = 'null'
        sr1.type = 'null'

    def AddId(self):
        sr1.id = self.entryARMId.get()
        sr1.password = self.entryARMPassword.get()
        sr1.name = self.entryARMName.get()
        sr1.type = self.entryARMType.get()
        query = "insert into Credentials (Id, Password, Name, UserType) values(%s, %s, %s, %s)"
        val = (sr1.id, sr1.password, sr1.name, sr1.type, )
        dbCursor.execute(query, val)
        self.ShowCourses()

        self.labelARMMessage.config(text = "ID created successfully!")
        self.labelARMMessage.after(2000, lambda: self.labelARMMessage.config(text=''))
    
    def RemoveID(self):
        sr1.id = self.entryARMId.get()

        query1 = "delete from Credentials where Id = %s"
        query2 = "delete from CourseReg where Sid = %s"
        val = (sr1.id, )

        if sr1.type == 'student':
            dbCursor.execute(query2, val)
            print("Hello")
        dbCursor.execute(query1, val)
        self.ClearSearch()
        self.ClearSearchResult()
            
    
    def ARMCommitChange(self):
        centralDb.commit()
    
    def Create(self):
        self.frameARM = Frame(root, bg = background_admin, height = HEIGHT, width = WIDTH)
        self.frameARM.place(relx = 0, rely = 0)

        self.labelARMSearch = Label(self.frameARM, text='Search', bg = background_admin)
        self.labelARMSearch.place(relx = 0.05, rely = 0.2)
        self.entryARMSearch = Entry(self.frameARM, width = 20)
        self.entryARMSearch.place(relx = 0.12, rely = 0.2)
        self.buttonARMSearch = Button(self.frameARM, text = 'Go', command = self.SearchId)
        self.buttonARMSearch.place(relx = 0.27, rely = 0.195)

        self.labelARMId = Label(self.frameARM, text='Id', bg = background_admin)
        self.labelARMId.place(relx = 0.08, rely = 0.3)
        self.entryARMId = Entry(self.frameARM, width = 25)
        self.entryARMId.place(relx = 0.1, rely = 0.3)

        self.labelARMPassword = Label(self.frameARM, text='Password', bg = background_admin)
        self.labelARMPassword.place(relx = 0.035, rely = 0.35)
        self.entryARMPassword = Entry(self.frameARM, width = 25)
        self.entryARMPassword.place(relx = 0.1, rely = 0.35)

        self.labelARMName = Label(self.frameARM, text='Name', bg = background_admin)
        self.labelARMName.place(relx = 0.055, rely = 0.4)
        self.entryARMName = Entry(self.frameARM, width = 25)
        self.entryARMName.place(relx = 0.1, rely = 0.4)

        self.labelARType = Label(self.frameARM, text='User Type', bg = background_admin)
        self.labelARType.place(relx = 0.035, rely = 0.45)
        self.entryARMType = Entry(self.frameARM, width = 25)
        self.entryARMType.place(relx = 0.1, rely = 0.45)

        self.labelARCourse = Label(self.frameARM, text='Courses', bg = background_admin)
        self.labelARCourse.place(relx = 0.01, rely = 0.5)
        self.entryARMCourse = Listbox(self.frameARM, width = 28, height = 9)
        self.entryARMCourse.place(relx = 0.07, rely = 0.5)

        self.buttonARMUpdate = Button(self.frameARM, text = 'Update Data')
        self.buttonARMUpdate.place(relx = 0.3, rely = 0.32, width = 100)

        self.buttonARMAdd = Button(self.frameARM, text = 'Add Id', command = self.AddId)
        self.buttonARMAdd.place(relx = 0.3, rely = 0.37, width = 100)

        self.buttonARMRemove = Button(self.frameARM, text = 'Remove Id', command = self.RemoveID)
        self.buttonARMRemove.place(relx = 0.3, rely = 0.42, width = 100)

        self.buttonARMApplyChanges = Button(self.frameARM, text = 'Apply Changes', width = 25, command = self.ARMCommitChange)
        self.buttonARMApplyChanges.place(relx = 0.4, rely = 0.9)

        self.buttonARMBack = Button(self.frameARM, text = 'Back', command = lambda: self.ChangeToAdminFrame(self.frameARM))
        self.buttonARMBack.place(relx = 0.01, rely = 0.01)

        self.buttonARMRemoveCourse = Button(self.frameARM, text = 'Remove', command = self.RemoveCourse)
        self.buttonARMRemoveCourse.place(relx = 0.175, rely = 0.75)

        self.listboxARMCourseList = Listbox(self.frameARM, width = 30, height = 9)
        self.listboxARMCourseList.place(relx = 0.28, rely = 0.5)

        self.buttonARMAddCourse = Button(self.frameARM, text = 'Add', command = self.AddCourse)
        self.buttonARMAddCourse.place(relx = 0.35, rely = 0.75)

        self.labelARMMessage = Label(self.frameARM, text = '', bg = background_login)
        self.labelARMMessage.place(relx = 0.01, rely = 0.95)

        self.labelARMCourseId = Label(self.frameARM, text='Course Id', bg = background_admin)
        self.labelARMCourseId.place(relx = 0.6, rely = 0.4)
        self.entryARMCourseId = Entry(self.frameARM, width = 25)
        self.entryARMCourseId.place(relx = 0.7, rely = 0.4)

        self.labelARMCourseName = Label(self.frameARM, text='Course Name', bg = background_admin)
        self.labelARMCourseName.place(relx = 0.6, rely = 0.5)
        self.entryARCourseMName = Entry(self.frameARM, width = 25)
        self.entryARCourseMName.place(relx = 0.7, rely = 0.5)
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Add/Remove/Modyfy User Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #




# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Attendance Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #

class AttendanceFrame:
    def ChangeToAttendanceFrame(self, sourceFrame):
        sourceFrame.destroy()
        attendanceFrame = ARMFrame()
        attendanceFrame.Create()

    def ShowCalendar(self):
        def InsertDate(self):
            att1.date = self.cal.get_date()
            print(att1.date)
            self.labelShowDate.config(text = att1.date)
            self.topLevelCalendarWindow.destroy()

        self.topLevelCalendarWindow = Toplevel(root)
        self.topLevelCalendarWindow.geometry("+600+100")
        self.cal = Calendar(self.topLevelCalendarWindow, selectMode='day', data_pattern='dd-mm-yyyy')
        self.cal.pack()

        self.buttonSelectDateC = Button(self.topLevelCalendarWindow, text = 'Select', command = lambda: InsertDate(self))
        self.buttonSelectDateC.pack()

    def TakeAttendance(self):
        index = self.listboxSelectCourse.curselection()
        if index:
            temp1 = self.listboxSelectCourse.get(index)
            att1.cid = temp1[temp1.find("[")+1:temp1.find("]")]

        self.listboxListStudents.delete(0, END)  #Emptying the current listing in the listbox
        query = "select temp2.Id, temp2.Name from (select Sid from CourseReg where Cid = %s) as temp1 join (select Id, Name from Credentials where UserType = 'student') as temp2 where temp1.Sid = temp2.Id;"
        val = (att1.cid, )
        dbCursor.execute(query, val)
        temp2 = []
        for y in dbCursor:
            print(y)
            temp2.append(y[0])
            temp2.append(y[1])
        for x in range(0, len(temp2), 2):
            sr1.course = "[" + temp2[x] + "]" + " " + temp2[x+1]
            self.listboxListStudents.insert(END, sr1.course)

    def Create(self):
        #att1.fid = user1.id
        att1.fid = 'F3'

        self.frameAttendance = Frame(root, bg = background_login, height = HEIGHT, width = WIDTH)
        self.frameAttendance.place(relx = 0, rely = 0)

        self.buttonSelectDate = Button(self.frameAttendance, text = 'Select Date', command = self.ShowCalendar)
        self.buttonSelectDate.place(relx = 0.46, rely = 0.3)

        self.labelShowDate = Label(self.frameAttendance, text='dd-mm-yyyy', bg = 'white', width='15')
        self.labelShowDate.place(relx = 0.43, rely = 0.36)

        self.labelSelecCourse = Label(self.frameAttendance, text='Select Course', bg = background_admin)
        self.labelSelecCourse.place(relx = 0.45, rely = 0.1)

        self.listboxSelectCourse = Listbox(self.frameAttendance, width = 30, height = 5)
        self.listboxSelectCourse.place(relx = 0.4, rely = 0.15)

        self.buttonSelectDate = Button(self.frameAttendance, text = 'Take Attendance', command = self.TakeAttendance)
        self.buttonSelectDate.place(relx = 0.46, rely = 0.45)

        self.listboxListStudents = Listbox(self.frameAttendance, width = 30, height = 15, selectmode=MULTIPLE)
        self.listboxListStudents.place(relx = 0.4, rely = 0.55)

        self.listboxSelectCourse.delete(0, END)  #Emptying the current listing in the listbox
        query = "select Cid, Cname from CourseAlloc where Fac1 = %s or Fac2 = %s or Fac3 = %s"
        val = (att1.fid, att1.fid, att1.fid, )
        dbCursor.execute(query, val)
        temp2 = []
        for y in dbCursor:
            print(y)
            temp2.append(y[0])
            temp2.append(y[1])
        for x in range(0, len(temp2), 2):
            sr1.course = "[" + temp2[x] + "]" + " " + temp2[x+1]
            self.listboxSelectCourse.insert(END, sr1.course)

        
        #att1.cid = self.listboxSelectCourse.get()
# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Attendance Frame ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #


global user1
user1 = User()

global sr1
sr1 = SearchResult()

global att1
att1 = Attendance()
logingFrame = LoginFrame()
logingFrame.Create()

#adminFrame = AdminFrame()
#adminFrame.Create()

#armFrame = ARMFrame()
#armFrame.Create()

#attendanceFrame = AttendanceFrame()
#attendanceFrame.Create()

#facultyFrame = FacultyFrame()
#facultyFrame.Create()

# ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ Drawing X and Y axis for ease of placeing widgets ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄ #
if showAxis == False:
    yFrame = Frame(root, height = HEIGHT, width = 1, bg = 'white')
    yFrame.place(relx = 0.5, rely = 0)
    xFrame = Frame(root, height = 1, width = WIDTH, bg = 'white')
    xFrame.place(relx = 0, rely = 0.5)
# ^^^^^^^^^^^^^ Drawing X and Y axis for ease of placeing widgets ^^^^^^^^^^^^^ # 

root.mainloop()
