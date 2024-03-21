from tkinter import *
import mysql.connector  
from tkinter import ttk
from tkmacosx import *
from tkinter import messagebox

###########################
password = ""# db 패스워드 입력
############################

# Q1. Create a window
window = Tk()
window.geometry("1500x720")
window.title("FIFA 22 MAIN") #윈도우 사이즈
#윈도우 배경
#bg_image = PhotoImage(file="fifa22.png")
#bg_label = Label(window, image=bg_image)
#bg_label.pack()

#검색창 프레임
frame = Frame(window,  borderwidth=3)  # adding border
frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.1, anchor=N)
entry1 = Entry(frame, font=36)


# 결과창
#lower_frame = Frame(window, bg="#80c1ff", borderwidth=5)
#lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor=N)
#label = Label(lower_frame)
#label.place(relheight=1, relwidth=1)
#엔트리값 텍스트화 변수
text_entered = str(entry1.get())
lower_frame = Frame(window, bg="light gray", borderwidth=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.7, anchor=N)
label_left = Label(lower_frame,bg='light grey', relief = 'groove')
label_left.place(relheight=1, relwidth=0.4)
label_right = Canvas(lower_frame,bd=10, bg='white') ############
label_right.place(relx=0.4 ,relheight=1, relwidth=0.6)
frame_resulton = Frame(label_right,bg='white')
frame_resulton.pack()


#버튼클릭시 함수


#request event(엔터키 입력) 때 작동 함수
def entered(event):
    button_click(event)

# db연결 함수
def connect():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd= password,#패스워드 입력
        database="fifa22",
        auth_plugin='mysql_native_password'
    )
    return mydb


query = 'SELECT p1.`NAME`, p1.`height`,p1.`weight`, t.`league`,p1.`Positions`,p1.`AGE`, stat.`OVERALL`  FROM players_info_physical p1  \
JOIN team t ON  p1.club = t.`name` JOIN players_info_stats stat ON p1.`name` = stat.`name`\
WHERE p1.`fullname` like "%{0}%" and \
p1.`age` >= {1} and  \
p1.`age` <= {2} and  \
p1.`weight` >= {3} and p1.`weight` <= {4} and \
p1.`height` >= {5}   and p1.`height` <= {6} and \
stat.`overall` >= {7} and stat.`overall` <= {8}  and   \
p1.`positions` like "%{9}%" and \
t.`league` like "%{10}%"  \
{11} {12} {13} LIMIT 30'


query2='SELECT p1.*, stat.*  FROM players_info_physical p1  \
JOIN team t ON  p1.club = t.`name` JOIN players_info_stats stat ON p1.`name` = stat.`name`\
WHERE p1.`fullname` like "%{0}%" and \
p1.`age` >= {1} and  \
p1.`age` <= {2} and  \
p1.`weight` >= {3} and p1.`weight` <= {4} and \
p1.`height` >= {5}   and p1.`height` <= {6} and \
stat.`overall` >= {7} and stat.`overall` <= {8}  and   \
p1.`positions` like "%{9}%" and \
t.`league` like "%{10}%"  \
{11} {12} {13} LIMIT 50'


query3 = "SELECT  count(*), l.League  from players_info_physical p1 \
JOIN team t ON p1.`club` = t.`name` JOIN players_info_stats stat ON p1.`name` = stat.`name` JOIN league l ON t.LeagueId = l.LeagueId \
WHERE p1.`fullname` like '%{0}%' and \
p1.`age` >= {1} and  \
p1.`age` <= {2} and  \
p1.`weight` >= {3} and p1.`weight` <= {4} and \
p1.`height` >= {5}   and p1.`height` <= {6} and \
stat.`overall` >= {7} and stat.`overall` <= {8}  and   \
p1.`positions` like '%{9}%' and \
t.`league` like '%{10}%'  \
GROUP BY l.LeagueId \
LIMIT 30"
#변수지정
Agemin = 0
Agemax = 100
hmax = 300
hmin = 0
wmax = 500
wmin = 0
option_get = ' '
dec_get = ' '
overmin = 0
overmax = 100
##############functions##################
def showdb():

    conn = connect()
    c = conn.cursor()

    #나이 입력값에 대한 if문
    if e_agemax.get() == '':
        Agemax = 100
    else:
        Agemax = e_agemax.get()

    if e_agemin.get() == '':
        Agemin = 0
    else:
        Agemin = e_agemin.get()

    #키 입력값
    if e_hmax.get() == '':
        hmax = 300
    else:
        hmax = e_hmax.get()

    if e_hmin.get() == '':
        hmin = 0
    else:
        hmin = e_hmin.get()

    #몸무게 입력값
    if e_wmax.get() == '':
        wmax = 300
    else:
        wmax = e_wmax.get()

    if e_wmin.get() == '':
        wmin = 0
    else:
        wmin = e_wmin.get()

     # 총점 입력값
    if e_ovmax.get() == '':
        overmax = 300
    else:
        overmax = e_ovmax.get()

    if e_ovmin.get() == '':
        overmin = 0
    else:
        overmin = e_ovmin.get()

    #ORDER BY check 여부에 따른 if문
    if  str(order_onoff.get()) == ' ' :
        option_get = ' '
        dec_get = ' '
    else:
        option_get = str(optioncombo.get())
        dec_get = str(descasc.get())

    c.execute(
        query.format(
        str(entry1.get()), #input value
        Agemin, Agemax, #age
        wmin,wmax, #weight
        hmin,hmax, #height
        overmin, overmax,  # overall
        str(combo_p.get()), #positions
        str(combo_lg.get()), #league
        str(order_onoff.get()),option_get,dec_get
        )
        ) #order by option
    result = c.fetchall()
    columns = c.column_names
    c.execute(
        query3.format(
        str(entry1.get()), #input value
        Agemin, Agemax, #age
        wmin,wmax, #weight
        hmin,hmax, #height
        overmin, overmax,  # overall
        str(combo_p.get()), #positions
        str(combo_lg.get()) #league
        )
        ) #order by option
    result_num = c.fetchall()
    if len(result) < 1:  # if there is no result show label_none with text in entry
        clearing()  # to prevent showing previous results with recent results
        label_none = Label(frame_resulton, bg="white",
                           text="No Search Result",font=20)
        label_none.pack(pady=150)
    # 14-2
    else:
        clearing()  # to prevent showing previous results with recent results

        list_num = []


        k = 0 #두번째 줄에 컬럼 명 입력 라벨
        for num in result_num:
            list_num.append(num)
        messagebox.showinfo("numbers of results",("{0}".format(list_num)))

        for cols in columns:
            res_label = Label(frame_resulton, text=cols, bg="white")
            res_label.grid(row=2, column=k+1)
            k = k + 1
        i = 3 #세번째줄부터 검색값 표시
        for res in result:
            globals()['Compare_{}'.format(i)] = Button(frame_resulton, text="Compare", fg="black", bg="white", font=("Arial", 12), command=lambda x=res: list(x))
            globals()['Compare_{}'.format(i)].grid(row=i, column=0, pady=1)
            for j in range(len(res)):
                res_e = Entry(frame_resulton,font=("Arial",8), width=15, fg='blue',relief='flat',bg='white',justify=CENTER)
                res_e.grid(row=i, column=j+1)
                res_e.insert(END, res[j])
            i = i + 1
        global  scrollbar
        scrollbar = ttk.Scrollbar(label_right, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill="y")
        scrollbar.config(command=label_right.yview)
        label_right.configure(yscrollcommand=scrollbar.set)
        label_right.bind("<Configure>", lambda e: label_right.configure(scrollregion=label_right.bbox("all")))
        label_right.create_window((0,0), window=frame_resulton, anchor=NW)

    conn.close()


def clearing():  # forget result_on label which contains result labels(res_label,res_label2) and make result_on label again
    global label_right, frame_resulton
    label_right.place_forget()
    label_right = Canvas(lower_frame, bd=10, bg='white')  ############
    label_right.place(relx=0.4, relheight=1, relwidth=0.6)
    frame_resulton.pack_forget()
    frame_resulton = Frame(label_right, bg='white')
    frame_resulton.pack()

def button_click(text):
    clearing()
    connect()

    try:
        showdb()
    except mysql.connector.errors.ProgrammingError as e:
        errorpopup()


def errorpopup():
    messagebox.showinfo("Message", "Option value error, Check search options")


#버튼 만들기 + 리턴 이벤트 바인드(엔터키 입력)
button = Button(frame, text="Search", fg="black", bg="white", font=36, command=lambda: button_click(entry1.get()))
button.place(relx=0.47, relheight=1, relwidth=0.1)
entry1.bind('<Return>', entered)
entry1.place(relx=0.07,relwidth=0.35, relheight=1)
#helpmanual text variables
Manualsearch="<Search> \n 1. Type players name you want to search \n\n 2. Set your search filters' options before you click 'Search' button(It is not neccessary!) \n\n \
3. Click 'Search' button \n\n 4. First pop-up message shows you how many results are in each league. \n ex) (14,English premium league) means 14 results are in EPL\n \
5. If you want to know more information about search results, Click 'Search Details' \n\n 6. If you want to use sorting function, you have to check 'order by' check box and choose columns to sort by. \n\n \
7. There is a league information box containing leagues' simple information besides league filter."
Manualupdate="<Update>\n1. Click 'Revise player information' button\n\n2. Search players who you want to revise\n\n3. Click Select button\n\n4. Choose columns you want to revise\n\n5. Type correct value to update\n(Before you update check if you write it in correct or not)\n\n6. Click 'update' button then you will see message box. "
Manualcompare = "<Compare>\n\n1. After search results, There are 'Compare' buttons on left side of players results.\n\n2. Choose two players and click 'Compare' buttons.\n\n3. On top right side of window there are compare label and there will be players' name you choose on it.\n\n4. Click 'Compare players' button\n\n5. New window will come out with selected players' data."
def helpmanual():
    helpwindow = Toplevel(window)
    helpwindow.geometry("1000x800")
    helpwindow.title("HELP")
    help_search = Label(helpwindow,bg="azure")
    help_search.place(relwidth=1,relheight=0.32)
    help_search_text = Label(help_search,bg="azure", text=Manualsearch,font=15, justify=LEFT)
    help_search_text.grid(row=0,column=0)
    help_Updating = Label(helpwindow,bg="azure")
    help_Updating.place(rely=0.33,relwidth=1,relheight=0.3)
    help_update_text = Label(help_Updating,bg="azure", text=Manualupdate,font=20, justify=LEFT)
    help_update_text.grid(row=0,column=0)
    help_Comparing = Label(helpwindow,bg="azure")
    help_Comparing.place(rely=0.64,relwidth=1,relheight=0.35)
    help_compare_text = Label(help_Comparing,bg="azure", text=Manualcompare,font=20, justify=LEFT)
    help_compare_text.grid(row=0,column=0)
def button_clickhelp():
    helpmanual()
button_help = Button(frame, text='Help!',fg="black", bg="white", font=36, command=lambda:button_clickhelp())
button_help.place(relheight=1, relwidth=0.05)
#검색 상세정보 창
button_all = Button(frame, text="Search more details \n (New window)", bg="white",command=lambda: button_click2(entry1.get()))
button_all.place(relx=0.58, relheight=1, relwidth=0.1)
def button_click2(text):

    connect()
    try:
        specificstat()
    except mysql.connector.errors.ProgrammingError:
        errorpopup()
def specificstat():
    specific_window = Toplevel()
    specific_window.geometry('1500x700')
    specific_window.title("Specific Search Results")
    spe_canvas = Canvas(specific_window,bg="white")
    spe_canvas.pack(expand=True,fill=BOTH)
    spe_results = Frame(spe_canvas)
    spe_results.pack()
    conn = connect()
    cc = conn.cursor()
    #나이 입력값
    if e_agemax.get() == '':
        Agemax = 100
    else:
        Agemax = e_agemax.get()

    if e_agemin.get() == '':
        Agemin = 0
    else:
        Agemin = e_agemin.get()

    #키 입력값
    if e_hmax.get() == '':
        hmax = 300
    else:
        hmax = e_hmax.get()

    if e_hmin.get() == '':
        hmin = 0
    else:
        hmin = e_hmin.get()

    #몸무게 입력값
    if e_wmax.get() == '':
        wmax = 300
    else:
        wmax = e_wmax.get()

    if e_wmin.get() == '':
        wmin = 0
    else:
        wmin = e_wmin.get()


     # 총점 입력값
    if e_ovmax.get() == '':
        overmax = 300
    else:
        overmax = e_ovmax.get()

    if e_ovmin.get() == '':
        overmin = 0
    else:
        overmin = e_ovmin.get()

    #ORDER BY check 여부에 따른 if문
    if  str(order_onoff.get()) == ' ' :
        option_get = ' '
        dec_get = ' '
    else:
        option_get = str(optioncombo.get())
        dec_get = str(descasc.get())

    cc.execute(
        query2.format(
        str(entry1.get()), #input value
        Agemin, Agemax, #age
        wmin,wmax, #weight
        hmin,hmax, #height
        overmin, overmax,  # overall
        str(combo_p.get()), #positions
        str(combo_lg.get()), #league
        str(order_onoff.get()),option_get,dec_get
        )
        ) #order by option
    result = cc.fetchall()
    columns = cc.column_names
    k = 0  # 두번째 줄에 컬럼 명 입력 라벨

    for cols in columns:
        res_label = Label(spe_results, text=cols)
        res_label.grid(row=2, column=k + 1)
        k = k + 1
    i = 3  # 세번째줄부터 검색값 표시
    for res in result:

        for j in range(len(res)):
            res_e = Entry(spe_results, font=("Arial", 8), width=15, fg='blue', relief='flat', bg='white',
                          justify=CENTER)
            res_e.grid(row=i, column=j + 1)
            res_e.insert(END, res[j])
        i = i + 1
    scrollbar2 = ttk.Scrollbar(spe_canvas, orient=VERTICAL) #y축 스크롤
    scrollbar2.pack(side=RIGHT, fill="y")
    scrollbar2.config(command=spe_canvas.yview)
    scrollbar3 = ttk.Scrollbar(spe_canvas, orient=HORIZONTAL) #x축 스크롤
    scrollbar3.pack(side=BOTTOM, fill="x")
    scrollbar3.config(command=spe_canvas.xview)
    spe_canvas.configure(yscrollcommand=scrollbar2.set, xscrollcommand=scrollbar3.set)
    spe_canvas.bind("<Configure>", lambda e: spe_canvas.configure(scrollregion=spe_canvas.bbox("all")))
    spe_canvas.create_window((0, 0), window=spe_results, anchor=NW)
#League information window
def button_click3():

    connect()
    leagueinfo()

def leagueinfo():
    leaguewindow = Toplevel(window)
    leaguewindow.geometry('1500x300')
    leaguewindow.title("League Information")
    leaguef = Canvas(leaguewindow)
    leaguef.pack(expand=True, fill="both")
    lea_re = Label(leaguef)
    lea_re.pack()
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM league")
    result = c.fetchall()
    columns = c.column_names
    k = 0  # 두번째 줄에 컬럼 명 입력 라벨

    for cols in columns:
        res_label = Label(lea_re, text=cols)
        res_label.grid(row=2, column=k )
        k = k + 1
    i = 3  # 세번째줄부터 검색값 표시
    for res in result:

        for j in range(len(res)):
            res_e = Entry(lea_re, font=("Arial", 8), width=15, fg='blue', relief='solid', bg='white',
                          justify=CENTER)
            res_e.grid(row=i, column=j)
            res_e.insert(END, res[j])
        i = i + 1

#scrollbar

###조건창
l_sc = Label(label_left, text="<Search Options>",font=12, bg="light grey")
l_sc.grid(row=0, column=0)
#AGE
l_age = Label(label_left, text="Age",font=12, bg="light grey")
l_age.grid(row=1, column=0, sticky=W)
l_agemin = Label(label_left,padx=0,text="Min",bg="light grey")
l_agemin.grid(row=1,column=1)
e_agemin = Entry(label_left,bg="white",relief='groove',width=5)
e_agemin.bind('<Return>', entered)
e_agemin.grid(row=1, column=2)
l_agemax = Label(label_left,text="Max",bg="light grey")
l_agemax.grid(row=1,column=3)
e_agemax = Entry(label_left,bg="white",relief='groove',width=5)
e_agemax.bind('<Return>', entered)
e_agemax.grid(row=1, column=4)
#Height
l_height = Label(label_left, text="Height(cm)",font=12, bg="light grey")
l_height.grid(row=2, column=0, sticky=W)
l_hmin = Label(label_left,padx=0,text="Min",bg="light grey")
l_hmin.grid(row=2,column=1)
e_hmin = Entry(label_left,bg="white",relief='groove',width=5)
e_hmin.bind('<Return>', entered)
e_hmin.grid(row=2, column=2)
l_hmax = Label(label_left,text="Max",bg="light grey")
l_hmax.grid(row=2,column=3)
e_hmax = Entry(label_left,bg="white",relief='groove',width=5)
e_hmax.bind('<Return>', entered)
e_hmax.grid(row=2, column=4)

#Weight
l_weight = Label(label_left, text="Weight(kg)",font=12, bg="light grey")
l_weight.grid(row=3, column=0, sticky=W)
l_wmin = Label(label_left,padx=0,text="Min",bg="light grey")
l_wmin.grid(row=3,column=1)
e_wmin = Entry(label_left,bg="white",relief='groove',width=5)
e_wmin.bind('<Return>', entered)
e_wmin.grid(row=3, column=2)
l_wmax = Label(label_left,text="Max",bg="light grey")
l_wmax.grid(row=3,column=3)
e_wmax = Entry(label_left,bg="white",relief='groove',width=5)
e_wmax.bind('<Return>', entered)
e_wmax.grid(row=3, column=4)




#####OVERALL
l_over = Label(label_left, text="Overall",font=12, bg="light grey")
l_over.grid(row=4, column=0, sticky=W)
l_ovmin = Label(label_left,padx=0,text="Min",bg="light grey")
l_ovmin.grid(row=4,column=1)
e_ovmin = Entry(label_left,bg="white",relief='groove',width=5)
e_ovmin.bind('<Return>', entered)
e_ovmin.grid(row=4, column=2)
l_ovmax = Label(label_left,text="Max",bg="light grey")
l_ovmax.grid(row=4,column=3)
e_ovmax = Entry(label_left,bg="white",relief='groove',width=5)
e_ovmax.bind('<Return>', entered)
e_ovmax.grid(row=4, column=4)
#Position
l_position = Label(label_left, text="Position",font=12, bg="light grey")
l_position.grid(row=5, column=0, sticky=W)
P_list =["","ST","GK","CM","CAM","CDM","RM","LM", "LW", "CB", "RW","LB","RB","CF","RWB","LWB"]
def changeposition():
    combo_p["values"] = P_list
combo_p =ttk.Combobox(label_left, values=P_list, postcommand=changeposition)
combo_p.config(width=10)
combo_p.set("")
combo_p.grid(row=5,column=2)
combo_pget = str(combo_p.get())


#### League
l_league = Label(label_left, text="Leagues",font=12, bg="light grey")
l_league.grid(row=6, column=0, sticky=W)
Lg_list =["","English Premier League","French Ligue 1","Bundesliga","Italian Serie A","Spain Primera Division","Belgian Jupiler Pro League","Korean K League"]
def changeleague():
    combo_lg["values"] = Lg_list
combo_lg =ttk.Combobox(label_left, values=Lg_list, postcommand=changeleague)
combo_lg.config(width=10)
combo_lg.set("")
combo_lg.grid(row=6,column=2)
b_leauge = Button(label_left, text="League Info", command=button_click3)
b_leauge.grid(row=6, column=3)

##### ORDERBY
l_option = Label(label_left, text="Sort option", font=12, bg="light grey")
l_option.grid(row=7, column=0, sticky=W)

columnlist= ["Positions","AGE", "Height", "Weight","stat.Overall"]
optioncombo = ttk.Combobox(label_left, values=columnlist)
optioncombo.set(columnlist[0])
optioncombo.config(width=10)
optioncombo.grid(row=7,column=2)

#ORDERBY - desc
descasc = StringVar()
dec = Checkbutton(label_left, text="Descending order", variable=descasc, onvalue="Desc",
offvalue="Asc")
dec.deselect()
dec.config(bg="light grey")
dec.grid(row=7, column=4)
dec_get = str(descasc.get())
#ORDERBY - onoff
order_onoff = StringVar()
onoff = Checkbutton(label_left, text="Order by", variable=order_onoff, onvalue="ORDER BY",
offvalue=" ")
onoff.deselect()
onoff.config(bg="light grey")
onoff.grid(row=7, column=3)
onoff_get= str(order_onoff.get())

#Nationality
#l_nationality = Label(label_left, text="Nationality",font=12, bg="light grey")
#l_nationality.grid(row=8, column=0, sticky=W)



### Compare Function ###
label_compare=Label(frame, text="Compare", fg="black", bg="white", font=("Arial bold", 12), anchor="nw")
label_compare.place(relx=0.72, relheight=1, relwidth=0.3)
label_compare2=Label(label_compare, bg="white", anchor="w")
label_compare2.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

def compare(x):
    label_compare3 = Label(label_compare2, text=list_compare[0][0][0], fg="black", bg="white", font=("Arial", 12), relief="ridge")
    label_compare3.grid(row=0, column=0)
    label_compare4 = Label(label_compare2, text=list_compare[1][0][0], fg="black", bg="white", font=("Arial", 12), relief="ridge")
    label_compare4.grid(row=0, column=1)

list_compare=[]
def list(x):
    try:
        list_compare.append([x])
        compare(x)
    except:
        pass

button_compare=Button(label_compare, text="Compare\nPlayers", font=36, command=lambda:openNewWindow())
button_compare.place(relx=0.94, relheight=1, relwidth=0.3, anchor="ne")

def openNewWindow():
    new = Toplevel(window)
    new.title("Compare Players")
    new.geometry("800x1000")

    conn = connect()
    c=conn.cursor()
    query4="SELECT name, positions, nationality, club, age, height, weight, preferredFoot FROM players_info_physical WHERE name='{0}'"
    c.execute(query4.format(str(list_compare[0][0][0])))
    myResult = c.fetchall()
    c.execute(query4.format(str(list_compare[1][0][0])))
    myResult2 = c.fetchall()

    # left_frame
    left_frame = Frame(new, bg="white")
    left_frame.place(relx=0.0125, rely=0.01, relheight=0.15, relwidth=0.48125, anchor="nw")
    left_middle_frame = Frame(left_frame, bg="white")
    left_middle_frame.place(relx=0.5, rely=0.5, anchor="center")
    # left_label
    left_name_label=Label(left_middle_frame, text=myResult[0][0], bg="white", font=("Arial bold",14))
    left_name_label.grid(row=0, column=0, columnspan=6)
    left_positions_label=Label(left_middle_frame, text="Positions", bg="white", font=("Arial bold",12))
    left_positions_label.grid(row=1, column=0)
    left_positions_label2=Label(left_middle_frame, text=myResult[0][1], bg="white")
    left_positions_label2.grid(row=1, column=1)
    left_nationality_label=Label(left_middle_frame, text="Nationality", bg="white", font=("Arial bold",12))
    left_nationality_label.grid(row=2, column=0)
    left_nationality_label2=Label(left_middle_frame, text=myResult[0][2], bg="white")
    left_nationality_label2.grid(row=2, column=1)
    left_club_label=Label(left_middle_frame, text="Club", bg="white", font=("Arial bold",12))
    left_club_label.grid(row=2, column=2)
    left_club_label2=Label(left_middle_frame, text=myResult[0][3], bg="white")
    left_club_label2.grid(row=2, column=3)
    left_age_label=Label(left_middle_frame, text="Age", bg="white", font=("Arial bold",12))
    left_age_label.grid(row=3, column=0)
    left_age_label2=Label(left_middle_frame, text=myResult[0][4], bg="white")
    left_age_label2.grid(row=4, column=0)
    left_height_label=Label(left_middle_frame, text="Height", bg="white", font=("Arial bold",12))
    left_height_label.grid(row=3, column=1)
    left_height_label2=Label(left_middle_frame, text=(str(myResult[0][5])+"cm"), bg="white")
    left_height_label2.grid(row=4, column=1)
    left_weight_label=Label(left_middle_frame, text="Weight", bg="white", font=("Arial bold",12))
    left_weight_label.grid(row=3, column=2)
    left_weight_label2=Label(left_middle_frame, text=(str(myResult[0][6])+"kg"), bg="white")
    left_weight_label2.grid(row=4, column=2)  
    left_preferredfoot_label=Label(left_middle_frame, text="PreferredFoot", bg="white", font=("Arial bold",12))
    left_preferredfoot_label.grid(row=3, column=3)
    left_preferredfoot_label2=Label(left_middle_frame, text=myResult[0][7], bg="white")
    left_preferredfoot_label2.grid(row=4, column=3)  

    # right_frame
    right_frame = Frame(new, bg="white")
    right_frame.place(relx=0.50625, rely=0.01, relheight=0.15, relwidth=0.48125, anchor="nw")
    right_middle_frame = Frame(right_frame, bg="white")
    right_middle_frame.place(relx=0.5, rely=0.5, anchor="center")
    # right_label
    right_name_label=Label(right_middle_frame, text=myResult2[0][0], bg="white", font=("Arial bold",14))
    right_name_label.grid(row=0, column=0, columnspan=6)
    right_positions_label=Label(right_middle_frame, text="Positions", bg="white", font=("Arial bold",12))
    right_positions_label.grid(row=1, column=0)
    right_positions_label2=Label(right_middle_frame, text=myResult2[0][1], bg="white")
    right_positions_label2.grid(row=1, column=1)
    right_nationality_label=Label(right_middle_frame, text="Nationality", bg="white", font=("Arial bold",12))
    right_nationality_label.grid(row=2, column=0)
    right_nationality_label2=Label(right_middle_frame, text=myResult2[0][2], bg="white")
    right_nationality_label2.grid(row=2, column=1)
    right_club_label=Label(right_middle_frame, text="Club", bg="white", font=("Arial bold",12))
    right_club_label.grid(row=2, column=2)
    right_club_label2=Label(right_middle_frame, text=myResult2[0][3], bg="white")
    right_club_label2.grid(row=2, column=3)
    right_age_label=Label(right_middle_frame, text="Age", bg="white", font=("Arial bold",12))
    right_age_label.grid(row=3, column=0)
    right_age_label2=Label(right_middle_frame, text=myResult2[0][4], bg="white")
    right_age_label2.grid(row=4, column=0)
    right_height_label=Label(right_middle_frame, text="Height", bg="white", font=("Arial bold",12))
    right_height_label.grid(row=3, column=1)
    right_height_label2=Label(right_middle_frame, text=(str(myResult2[0][5])+"cm"), bg="white")
    right_height_label2.grid(row=4, column=1)
    right_weight_label=Label(right_middle_frame, text="Weight", bg="white", font=("Arial bold",12))
    right_weight_label.grid(row=3, column=2)
    right_weight_label2=Label(right_middle_frame, text=(str(myResult2[0][6])+"kg"), bg="white")
    right_weight_label2.grid(row=4, column=2)  
    right_preferredfoot_label=Label(right_middle_frame, text="PreferredFoot", bg="white", font=("Arial bold",12))
    right_preferredfoot_label.grid(row=3, column=3)
    right_preferredfoot_label2=Label(right_middle_frame, text=myResult2[0][7], bg="white")
    right_preferredfoot_label2.grid(row=4, column=3)

    query4="SELECT overall, PaceTotal, ShootingTotal, PassingTotal, DribblingTotal, DefendingTotal, PhysicalityTotal, Crossing, Finishing, HeadingAccuracy, \
        ShortPassing, Volleys, Dribbling, Curve, FKAccuracy, LongPassing, BallControl, Acceleration, SprintSpeed, Agility, Reactions, Balance, ShotPower, \
        Jumping, Stamina, Strength, LongShots, Aggression, Interceptions, Positioning, Vision, Penalties, Composure, Marking, StandingTackle, SlidingTackle, \
        GKDiving, GKHandling, GKKicking, GKPositioning, GKReflexes, STRating, LWRating, LFRating, CFRating, RFRating, RWRating, CAMRating, LMRating, CMRating, \
        RMRating, LWBRating, CDMRating, RWBRating, LBRating, CBRating, RBRating, GKRating FROM players_info_stats WHERE name='{0}'"
    c.execute(query4.format(str(list_compare[0][0][0])))
    myResult = c.fetchall()
    c.execute(query4.format(str(list_compare[1][0][0])))
    myResult2 = c.fetchall()

    # bottom_left_frame
    bottom_left_frame = Frame(new, bg="white")
    bottom_left_frame.place(relx=0.0125, rely=0.17, relheight= 0.82, relwidth=0.48125, anchor="nw")
    bottom_left_middle_frame = Frame(bottom_left_frame, bg="white")
    bottom_left_middle_frame.place(relx=0.5, rely=0, anchor="n")
    # bottom_left_label
    front=["Overall", "PaceTotal",	"ShootingTotal", "PassingTotal", "DribblingTotal", "DefendingTotal", "PhysicalityTotal", "Crossing", \
        "Finishing", "HeadingAccuracy",	"ShortPassing", "Volleys", "Dribbling",	"Curve", "FKAccuracy", "LongPassing", "BallControl", "Acceleration", \
        "SprintSpeed",	"Agility",	"Reactions", "Balance",	"ShotPower", "Jumping", "Stamina",	"Strength",	"LongShots", "Aggression",	"Interceptions"]
    for i in range(29):
        if myResult[0][i]>myResult2[0][i]:
            res=myResult[0][i]-myResult2[0][i]
            Label(bottom_left_middle_frame, text=(res), fg="green", bg="white").grid(row=i, column=0)
            Label(bottom_left_middle_frame, text=("▲"), fg="green", bg="white").grid(row=i, column=1)
            Label(bottom_left_middle_frame, text=("▼"), fg="red", bg="white").grid(row=i, column=5)
            Label(bottom_left_middle_frame, text=(res), fg="red", bg="white").grid(row=i, column=6)
        elif myResult[0][i]<myResult2[0][i]:
            res=myResult2[0][i]-myResult[0][i]
            Label(bottom_left_middle_frame, text=(res), fg="red", bg="white").grid(row=i, column=0)
            Label(bottom_left_middle_frame, text=("▼"), fg="red", bg="white").grid(row=i, column=1)        
            Label(bottom_left_middle_frame, text=("▲"), fg="green", bg="white").grid(row=i, column=5)      
            Label(bottom_left_middle_frame, text=(res), fg="green", bg="white").grid(row=i, column=6)
        else:
            Label(bottom_left_middle_frame, text="-", fg="grey", bg="white").grid(row=i, column=1)        
            Label(bottom_left_middle_frame, text="-", fg="grey", bg="white").grid(row=i, column=5)
        Label(bottom_left_middle_frame, text=myResult[0][i], bg="white").grid(row=i, column=2)
        Label(bottom_left_middle_frame, text=myResult2[0][i], bg="white").grid(row=i, column=4)
        Label(bottom_left_middle_frame, text=front[i], bg="white", font=("Arial bold",12)).grid(row=i, column=3)
    
    # bottom_right_frame
    bottom_right_frame = Frame(new, bg="white")
    bottom_right_frame.place(relx=0.50625, rely=0.17, relheight=0.82, relwidth=0.48125, anchor="nw")
    bottom_right_middle_frame = Frame(bottom_right_frame, bg="white")
    bottom_right_middle_frame.place(relx=0.5, rely=0, anchor="n")
    # bottom_left_label
    back=["Positioning", "Vision", "Penalties", "Composure", "Marking", "StandingTackle", "SlidingTackle", "GKDiving", "GKHandling", "GKKicking", \
        "GKPositioning", "GKReflexes", "STRating", "LWRating", "LFRating", "CFRating", "RFRating", "RWRating", "CAMRating", "LMRating", "CMRating", \
        "RMRating", "LWBRating", "CDMRating", "RWBRating", "LBRating", "CBRating", "RBRating", "GKRating"]
    for i in range(29):
        if myResult[0][29+i]>myResult2[0][29+i]:
            res=myResult[0][29+i]-myResult2[0][29+i]
            Label(bottom_right_middle_frame, text=(res), fg="green", bg="white").grid(row=i, column=0)
            Label(bottom_right_middle_frame, text=("▲"), fg="green", bg="white").grid(row=i, column=1)
            Label(bottom_right_middle_frame, text=("▼"), fg="red", bg="white").grid(row=i, column=5)
            Label(bottom_right_middle_frame, text=(res), fg="red", bg="white").grid(row=i, column=6)
        elif myResult[0][29+i]<myResult2[0][29+i]:
            res=myResult2[0][29+i]-myResult[0][29+i]
            Label(bottom_right_middle_frame, text=(res), fg="red", bg="white").grid(row=i, column=0)
            Label(bottom_right_middle_frame, text=("▼"), fg="red", bg="white").grid(row=i, column=1)        
            Label(bottom_right_middle_frame, text=("▲"), fg="green", bg="white").grid(row=i, column=5)      
            Label(bottom_right_middle_frame, text=(res), fg="green", bg="white").grid(row=i, column=6)
        else:
            Label(bottom_right_middle_frame, text="-", fg="grey", bg="white").grid(row=i, column=1)        
            Label(bottom_right_middle_frame, text="-", fg="grey", bg="white").grid(row=i, column=5)
        Label(bottom_right_middle_frame, text=myResult[0][29+i], bg="white").grid(row=i, column=2)
        Label(bottom_right_middle_frame, text=myResult2[0][29+i], bg="white").grid(row=i, column=4)
        Label(bottom_right_middle_frame, text=back[i], bg="white", font=("Arial bold",12)).grid(row=i, column=3)

    bottom_middle_frame = Frame(new, bg="white")
    bottom_middle_frame.place(relx=0.49375, rely=0.17, relheight=0.82, relwidth=0.0125, anchor="nw")
    conn.close()


### Revise Function ###
update_button=Button(label_left, text="Revise Player Information", font=("Arial bold", 25), command=lambda: openNewWindow2())
update_button.place(relx=0.5, rely=0.98, relwidth=0.95, relheight=0.2, anchor="s")

def openNewWindow2():
    new2 = Toplevel(window)
    new2.title("Revise Player Information")
    new2.geometry("500x800")

    top_frame=Frame(new2, bg="white")
    top_frame.place(relx=0.016, rely=0.01, relwidth=0.968, relheight=0.1, anchor="nw")
    result_frame=Frame(new2, bg="white")
    result_frame.place(relx=0.016, rely=0.12, relwidth=0.968, relheight=0.81, anchor="nw")
    result_middle_frame=Frame(result_frame, bg="white")
    result_middle_frame.place(relx=0.5, rely=0.5, anchor="center")
    bottom_frame=Frame(new2)
    bottom_frame.place(relx=0.016, rely=0.94, relwidth=0.968, relheight=0.05, anchor="nw")

    label=Label(top_frame, text="Enter the player's name.", font=("Arial bold", 20), bg="white")
    label.place(relx=0.5, rely=0, relwidth=1, relheight=0.5, anchor="n")
    entry = Entry(top_frame, font=("Arial bold", 15), textvariable=StringVar())
    button = Button(bottom_frame, text="clear", command=lambda: clearing2())
    button.pack(side="right")

    def clearing2():
    # Clear the result frame
        for widgets in result_middle_frame.winfo_children():
            widgets.destroy()

    def result(event):
        clearing2()
        global c
        conn = connect()
        c=conn.cursor()
        query5="SELECT name FROM players_info_physical WHERE Fullname LIKE '%{0}%'"
        c.execute(query5.format(str(entry.get())))
        myResult = c.fetchall()
        if len(myResult) != 0:
            Label(result_middle_frame, text="Name", bg="white", font=("Arial bold", 12)).grid(row=0, column=0)
            Label(result_middle_frame, text="Update", bg="white", font=("Arial bold", 12)).grid(row=0, column=1)
            n=1
            for i in myResult:
                locals()['button_return_{}'.format(n)] = Button(result_middle_frame, text="Select", command=lambda x=i: openNewWindow3(x))
                locals()['button_return_{}'.format(n)].grid(row=n, column=1)
                Label(result_middle_frame, text=i[0], bg="white").grid(row=n, column=0)
                n=n+1
        elif len(myResult) == 0:
            label = Label(result_middle_frame, text='Player "{0}" could not be found.'.format(str(entry.get())), bg="white")
            label.grid(row=0, column=0)
        conn.close()
    entry.bind("<Return>", result)
    entry.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.45, anchor="n")

def openNewWindow3(x):
    new3 = Toplevel(window)
    new3.title("Revise Player Information")
    new3.geometry("500x250")

    conn = connect()
    c=conn.cursor()
    
    # new3_top_frame
    new3_top_frame=Frame(new3, bg="white")
    new3_top_frame.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.2, anchor="nw")
    name_label=Label(new3_top_frame, text=x[0], font=("Arial bold",30), bg="white")
    name_label.place(relx=0.5, rely=0.5, anchor="center")
    # new3_middle_frame
    new3_middle_frame=Frame(new3, bg="white")
    new3_middle_frame.place(relx=0.01, rely=0.24, relwidth=0.98, relheight=0.62, anchor="nw")
    new3_middle_middle_frame=Frame(new3_middle_frame, bg="white")
    new3_middle_middle_frame.place(relx=0.5, rely=0.5, anchor="center")

    label_conditions=Label(new3_middle_middle_frame, text="Conditions", font=("Arial bold", 20), bg="white")
    label_conditions.grid(row=0, column=0)
    conditions=["playersID", "name", "Fullname", "age", "height", "weight", "nationality", "positions", "bestposition", "club", "valueEUR", "wageEUR", \
        "ReleaseClause", "ClubPosition", "contractuntil", "clubnumber", "ClubJoined", "Nationalteam", "nationalposition", "NationalNumber", "preferredFoot", \
        "IntReputation", "WeakFoot", "SkillMoves", "AttackingWorkRate", "DefensiveWorkRate", "overall", "potential", "growth", "TotalStats", "BaseStats", \
        "PaceTotal", "ShootingTotal", "PassingTotal", "DribblingTotal", "DefendingTotal", "PhysicalityTotal", "Crossing", "Finishing", "HeadingAccuracy", \
        "ShortPassing", "Volleys", "Dribbling", "Curve", "FKAccuracy", "LongPassing", "BallControl", "Acceleration", "SprintSpeed", "Agility", "Reactions", \
        "Balance", "ShotPower", "Jumping", "Stamina", "Strength", "LongShots", "Aggression", "Interceptions", "Positioning", "Vision", "Penalties", \
        "Composure", "Marking", "StandingTackle", "SlidingTackle", "GKDiving", "GKHandling", "GKKicking", "GKPositioning", "GKReflexes", "STRating", "LWRating", \
        "LFRating", "CFRating", "RFRating", "RWRating", "CAMRating", "LMRating", "CMRating", "RMRating", "WBRating", "CDMRating", "RWBRating", "LBRating", \
        "CBRating", "RBRating", "GKRating"]
    option = StringVar()
    option.set("")
    def show(event):
        global res
        query6='SELECT {0} FROM players_info_physical JOIN players_info_stats USING(name) WHERE name="{1}"'
        c.execute(query6.format(str(option.get()), str(x[0])))
        res=c.fetchall()
        label_value_existing2=Label(new3_middle_middle_frame, text=res[0][0], relief="raised")
        label_value_existing2.grid(row=1, column=1)

    drop_conditions = OptionMenu(new3_middle_middle_frame, option, *conditions, command=show)
    drop_conditions.grid(row=0, column=1)

    label_value_existing=Label(new3_middle_middle_frame, text="Value(existing)", font=("Arial bold", 20), bg="white")
    label_value_existing.grid(row=1, column=0)

    label_value_update=Label(new3_middle_middle_frame, text="Value(update)", font=("Arial bold", 20), bg="white")
    label_value_update.grid(row=2, column=0)
    new3_entry=Entry(new3_middle_middle_frame, width=25)
    new3_entry.grid(row=2, column=1)

    # new3_button
    new3_button=Button(new3, text="update", font=("Arial bold", 10), command=lambda:update())
    new3_button.place(relx=0.6, rely=0.88, relwidth=0.2, relheight=0.1, anchor="nw")
    def update():
        try:
            query7='UPDATE players_info_physical JOIN players_info_stats USING(name) SET {0}={1} WHERE name="{2}"'
            c.execute(query7.format(str(option.get()), new3_entry.get(), str(x[0])))
            conn.commit()
            open_popup()
        except:
            query7='UPDATE players_info_physical JOIN players_info_stats USING(name) SET {0}="{1}" WHERE name="{2}"'
            c.execute(query7.format(str(option.get()), new3_entry.get(), str(x[0])))
            conn.commit()
            open_popup()

    def open_popup():
        top= Toplevel(new3)
        top.geometry("500x150")
        top.title("Update Completed")
        top_top_frame=Frame(top)
        top_top_frame.place(relx=0.5, rely=0.25, anchor="center")
        top_bottom_frame=Frame(top)
        top_bottom_frame.place(relx=0.5, rely=0.75, anchor="center")
        Label(top_top_frame, text=('Player "{0}" Update Completed!!'.format(x[0])), font=('Arial bold', 20)).grid(row=0, column=0)
        Label(top_bottom_frame, text=str(option.get()), font=('Arial', 20)).grid(row=0, column=0)
        Label(top_bottom_frame, text="  ", font=('Arial', 20)).grid(row=0, column=1)
        Label(top_bottom_frame, text=":", font=('Arial', 20)).grid(row=0, column=2)
        Label(top_bottom_frame, text="  ", font=('Arial', 20)).grid(row=0, column=3)
        Label(top_bottom_frame, text=res[0][0], font=('Arial', 20)).grid(row=0, column=4)
        Label(top_bottom_frame, text="  ", font=('Arial', 20)).grid(row=0, column=5)
        Label(top_bottom_frame, text="→", font=('Arial', 20)).grid(row=0, column=6)
        Label(top_bottom_frame, text="  ", font=('Arial', 20)).grid(row=0, column=7)
        Label(top_bottom_frame, text=new3_entry.get(), font=('Arial', 20)).grid(row=0, column=8)

window.mainloop()