import os
import re
import sys
from pprint import pprint
from tkinter import Tk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename
from collections import namedtuple

Student = namedtuple('Student', ['row', 'name', 'admission_number', 'age', 'scores', 'psychomotors', 'remarks'])
students = []
headers = ""
row_num = 0
others =  list(map(str.lower, iter(['Punctuality', 'Attendance', 'Emmotional Stability', 'Neatness', 'Politeness',
         'Honesty', 'Relationship with others', 'Self Control', 'Attitude to School work', 
         'Handwriting', 'Games', 'Sports', 'Drawing and Painting', 'Crafts', 'Musical skills', 
         'Days Present', 'Days Absent'])))
filename = None


def show_message(msg: str):
    """Show error message"""
    
    mb.showerror("Error", msg)
    sys.exit(0)


def validate_score(val: str):
    """Check score is either "N,N" or "int,int" """
    
    try:
        x, y = val.split(",")

        if int(x)+ int(y) >= 0 or  x == "N" and y == "N":
            return True, f"{x},{y}"
        else:
            return False, None
        if len(x) == 2:

            if (x[0] =="N") and (x[1] == "N"): 
                print('hit me')
                p, q = "N", "N"
                # remove one from the length of subjects
                global num_of_sub_reg
                num_of_sub_reg -= 1
            else:
                p, q = int(x[0]), int(x[1])
            return True, f"{p},{q}"
            if val == "0,0":
                return True, "0,0"
            elif val.strip == "N,N":
                x = val.split(",")
                return True, "N,N"

            elif len(val) < 5:
                return False, None
            else:
                if all(list(map(lambda x: int(x)*0 == 0, iter(val.strip().split(","))))):
                    return True, ",".join([str(int(val.split(",")[0])), str(int(val.split(",")[1]))])    
        else:
            print(val)
            show_message(f"Review the Scores in all subjects on liiiiiiine {row_num}")



    except ValueError:
        return False, None


def get_file():
    """Get file name"""

    Tk().withdraw()
    global filename
    filename = askopenfilename() 

    if not str(filename).endswith(".csv"):
       show_message("You can only verify csv files \n Try a csv file (GTA examination format).")

    return filename


def read_lines(filename: str):

    """Yield a new line excluding 
    the first line column description
    """

    with open(filename, "r") as f:
        for _,i in enumerate(f.readlines()):
            
            if _ == 0: 
                global headers
                headers = list(map(str.strip, iter(i.split(",")))) 
                headers = list(map(str.lower, headers))

            else:
                global row_num
                row_num = _+1
                yield i



def get_remarks(line):

    for j,i in enumerate(reversed(line.split(","))):
        try:
            if type(int(i)) == type(1):
                remarks = line.split(",")[-j::]
                if type(int(remarks[0])) == type(1):
                    remarks.pop(0)
                remarks = ",".join(remarks).strip()
                break
        except ValueError:
            continue
    return remarks or show_message(f"Review the Admission Number on line {row_num}")  



def get_psychomotors(line):
    ll = line.split(",")
    psychomotors = []
    y = 0
    for j,i in enumerate(reversed(line.split(","))):
        try:
            if type(int(i)) == type(1):
                x = len(line.split(",")[-j:])

                a = ll[-(len(others)+x):-x]
                if len(a) == len(others):
                    return [int(i) for i in ll[-(len(others)+x):-x]]

        except ValueError: 
            y += 1
            continue


def validate_values(line: str):

    """ Check each data type is correct"""

    global headers
    global others
    global subjects
    global num_of_sub_reg

    subjects = headers[3: headers.index(others[0].lower())]
    num_of_sub_reg = len(subjects)
    
    name = line.split(",")[0].strip()
    if len(name.split(" ")) < 2:
        show_message(f"Name can't be less than two words\nError on row number: {row_num}")  

    admission_number = line.split(",")[1].strip()
    if admission_number[0:4] and len(admission_number) == 10:
        try:
            if int(admission_number.split("/")[1]) * 0 == 0 and\
                int(admission_number.split("/")[2]) * 0 == 0: ...
        except ValueError:
            show_message(f"Review the Admission Number on line {row_num}")  

    else:
        show_message(f"Review the Admission Number on line {row_num}")  

    age = line.split(",")[2].strip()
    for i in age:
        try:
            if int(age)*0 == 0 and int(age) > 0: ...
            else: show_message(f"Review the Age Number on line {row_num}")
        except ValueError:
            show_message(f"Review the Age Number on line {row_num}")

    #Exam scores
    # print(line.split("\"")[1:])
    # temp = list(filter(lambda x: validate_score(x)[0], iter(line.split("\"")[1:])))
    # temp = temp[0:len(subjects)]
    # if len(scores) > len(subjects): print(111)
    scores = []
    # sys.exit()
    # for i in temp[0:len(subjects)]: 
    #     a = i.split(",")
    #     scores.append(f"{int(a[0])},{int(a[1])}")

    # if len(scores) != num_of_sub_reg:
    #     print(len(scores) , len(subjects))
    #     print(subjects)
    #     show_message(f"Review the Scoressss in all subjects on line {row_num}")

    
    remarks = get_remarks(line)

    psychomotors = get_psychomotors(line)

    students.append(Student(row_num, name, admission_number, age, scores, psychomotors, remarks))

    
def to_csv(x):
    return ""
    s = f"{x.name}, {x.admission_number}, {x.age},"
    for i in x.scores:
        s += f"\"{i}\","
    for i in x.psychomotors:
        s += f"{i},"
    s += x.remarks
    return s


if __name__ == "__main__":

    for i in read_lines(get_file()):
        validate_values(i)
    subjects = headers[3: headers.index(others[0].lower())]
    # mb.showinfo("Info", "Your file is ready to upload")
    with open(f"{filename[0:-4]}_Verified.csv", 'w+') as f:
        f.writelines(str(" ,".join(headers))[0:-1]+"\n")
        for j,i in enumerate(students):
            if j == len(students)-1:
                f.writelines(to_csv(i))
            else:
                f.writelines(to_csv(i)+"\n")

    # for i in students:

    sys.exit(0)