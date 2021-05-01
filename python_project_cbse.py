import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
import json
import sys
import time


with open('report_card_details.json', 'r') as txt:
    overall_details = json.load(txt)


'''The format of the stored dictionary will look something like: 

{"A": {"Math": [1.0, "F"], "Physics": [1.0, "F"], "Chemistry": [1.0, "F"], "CS": [1.0, "F"], "English": [1.0, "F"]}, "Ajay": {"Math": [100.0, "A"], "Physics": [98.0, "A"], "Chemistry": [87.0, "B"], "CS": [100.0, "A"], "English": [99.0, "A"]}}

'''



summ = 0
grade_cons = {'100 >= x>=91':'A', '91 > x >=81':'B', '81 > x >= 71':'C', '71 > x >= 61' : 'D', '61 > x >= 51' : 'E', 'x < 51' : 'F'}
indi_marks = []
grades = []
sub_list = ['Math', 'Physics', 'Chemistry', 'CS', 'English']


def input_verification():

    
    '''Function which handles any issues that may arise from inputs'''

    
    global name_student
    name_student = input("Enter name of student ")
    while name_student in overall_details:
        yn = input(f"Would you like to change {name_student}'s already existing marks? Y/N ")
        if yn == 'Y':
            name = name_student
            return 
        elif yn == 'N':
            name_student = input("Enter name of student ")
        else:
            print("Unrecognized character")
            raise SystemExit('Unrecognized Character')
    return 



def calculate_grades_and_marks():

    '''Function which maps the marks of a subject to a grade'''
        
    for i in range(len(sub_list)):
        x = float(input(f"Enter the marks for subject {sub_list[i]}: "))
        indi_marks.append(x)
        for i in grade_cons.keys():
            if eval(i):
                grades.append(grade_cons[i])
        


            
def show_results(name):

    '''Function which serves as the main output platform'''
    
    fig = plt.figure(figsize = (12,8))
    ax = fig.add_subplot(111)
    ax.set_title("Marks per subject")
    ax.set_ylabel('Marks')
    ax.set_xlabel('Subject')

    subs = [x for x in overall_details[name].keys()]
    marks = [x[0] for x in overall_details[name].values()]
    grades =[x[1] for x in overall_details[name].values()]
    print('\n\n\nSubject' + ' '*50 + 'Marks' + ' '*50 + 'Grades\n')
    for l in range(len(marks)):
        print(subs[l] + ' ' * (57 - len(subs[l])) + str(marks[l]) + ' ' * (59- len(str(marks[l]))) + grades[l]+'\n')
        
    avg = statistics.mean(marks)
    x = avg

    for m in grade_cons:
        if eval(m):
            print(f'\n\n\n{grade_cons[m]} is your average grade\n\n')
    print(f'{avg} is your average marks')

    labelr = mpatches.Patch(color = 'red', label = 'Class Average')
    plt.plot(subs, overall_results(), 'r')
    plt.legend(handles = [labelr])
    ax.bar(subs, marks)
    b = plt.gca()
    b.set_ylim([0,100])
    plt.show()


    
def overall_results():

    '''Helper function which will assist in calculating class average'''

    
    mean_marks = []
    mean_overall = []
    names = [x for x in overall_details]
    subjects = sub_list
    for i in subjects:
        for b in names:
            mean_marks.append(overall_details[b][i][0])
        mean_overall.append(statistics.mean(mean_marks))
        mean_marks = []
    return mean_overall
    



while True:
    
    m = input("Would you like to see a result or add a student or remove a student or leave? (Res/Add/Remove/Leave)")

    if m == 'Res':
        name_res = input("\nWhose result would you like to see? ")
        if name_res in overall_details:
            show_results(name_res)
        else:
            print(f"Name not in database:\nNames currently in database are {[x for x in overall_details]} ")

    elif m == 'Add':
        indi_marks = []
        grades = []
        
        input_verification()
        
        calculate_grades_and_marks()
        
        overall_details[name_student] = dict(zip(sub_list, list(zip(indi_marks, grades))))
        with open('report_card_details.json', 'w') as txt:  
            json.dump(overall_details, txt)
            print(f"\nDetails of {name_student} successfully added to the database!")

    elif m == 'Remove':
        name_rem = input("Enter name to be removed from the list: ")
        if name_rem in overall_details:
            x = overall_details.pop(name_rem)
            with open('report_card_details.json', 'w') as txt:
                json.dump(overall_details, txt)
                print(f"\nDetails of {name_rem} successfully removed from the database!")
        else:
            print(f"{name_rem}'s details have not been stored yet")
    

    elif m == 'Leave':
        print("Now exitting: ")
        time.sleep(10)
        raise SystemExit('Now exitting')
                

    else:
        print("Unrecognized character") 


        
