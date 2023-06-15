import os
import csv

def create_account():
    username = input("Enter the username:")
    password = input("Enter the password:")
    try:
        with open("Authentication", "w") as x:
            x.write(username)
            x.write(" ")
            x.write(password)
            x.close()
    except IOError:
        print("Having IO Error.")
    finally:
        print("Account created successfully.")
        return True

def login_account():
    username = input("Enter the username:")
    password = input("Enter the password:")
    try:
        with open("Authentication", "r") as x:
            x1 = x.readline()
            l = x1.split()
            u1 = l[0]
            p1 = l[1]
            x.close()
    except IOError:
        print("Error opening the file.")
    finally:
        if username == u1 and password == p1:
            print("Login Success")
            return True
        else:
            print("Given username or password is incorrect, Try Again!")
            login_account()


def loginSystem():
    user_choice = input("Need to create account? Yes/No:")
    if user_choice.lower() == "yes":
        val = create_account()
        return val
    elif user_choice.lower() == "no":
        val = login_account()
        return val
    else:
        print("Please enter the valid input!")
        loginSystem()

def create_csv(file_path, date, SID, name, monitoringStatus):
    with open(file_path, "w", newline="") as x:
        fieldname = ["SID", "Name"]
        wr = csv.DictWriter(x, fieldnames=fieldname)
        wr.writeheader()
        wr.writerow({"SID": SID, "Name": name})
        x.close()
    if monitoringStatus == "YES":
        with open("monitoring.csv", "w", newline="") as y:
            fieldname1 = ["SID"]
            wr1 = csv.DictWriter(y, fieldnames=fieldname1)
            wr1.writeheader()
            wr1.writerow({"SID":SID})
            y.close()
    else:
        pass



def addRollCall(file_path, date, SID, name, monitoringStatus):
    with open(file_path, "a") as x:
        fieldname = ["SID", "Name"]
        wr = csv.DictWriter(x, fieldnames=fieldname)
        wr.writerow({"SID": SID, "Name":name})
        x.close()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines(lines[:-1])
        file.close()
        file.close()
    if monitoringStatus == "YES":
        with open("monitoring.csv", "a") as y:
            fieldname1 = ["SID"]
            wr1 = csv.DictWriter(y, fieldnames=fieldname1)
            wr1.writerow({"SID": SID})
            y.close()
        with open("monitoring.csv", 'r') as file1:
            lines = file1.readlines()
        with open("monitoring.csv", 'w') as file1:
            file1.writelines(lines[:-1])
            file1.close()
            file1.close()
    else:
        pass

def check_csv(file_path, date, SID, name, monitoringStatus):
    if os.path.exists(file_path):
        addRollCall(file_path, date, SID, name, monitoringStatus)
    else:
        create_csv(file_path, date, SID, name, monitoringStatus)

def startRollCall():
    date = input("Enter the date:")
    course_subject = input("Enter the course subject:")
    number = input("Enter the course number:")
    n1 = course_subject +"_"+ number+".csv"
    c1 = True
    while c1:
        c1 = input("If need to continue, Enter True, else False:")
        if c1.lower() == "true":
            SID = input("Enter the Student ID:")
            name = input("Enter the Student Name:")
            monitoringStatus = input("Enter status for SMS service(yes/no):").upper()
            check_csv(n1, date, SID, name, monitoringStatus)
        else:
            break


def sendMessage(mrow, date, n1, n2):
    key = ""
    with open(n1, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        rows = list(csv_reader)
        header_row = rows[0]
        in1 = header_row.index(date)
        for row in rows:
            if row[0] == mrow:
                key = row[in1]
        file.close()
    key1 = ""
    if key == "P" or key == "1":
        key1 = "present"
    elif key == "A" or key == "0":
        key1 = "absent"
    elif key == "-1":
        key1 = "tardy"

    try:
        with open(mrow+".txt", "w") as x:
            x.write(f"Your {n2} attendance for {date} was changed to {key1}")
            x.write("\n")
            x.close()

    except IOError:
        print("Having IO Error.")

def rollCall():
    date = input("Enter the date:")
    course_subject = input("Enter the course subject:")
    number = input("Enter the course number:")
    n1 = course_subject + "_" + number + ".csv"
    n2 = course_subject + "_" + number
    if os.path.exists(n1):
        with open(n1, "r")as x:
            csv_reader = csv.reader(x, delimiter=",")
            rows = list(csv_reader)
            line_count = 0
            presentCount = 0
            absentCount = 0
            for row in rows:
                if line_count == 0:
                    row.append(date)
                    line_count += 1
                else:
                    print("Please Enter 'P' for present and 'A' for absent.")
                    census = input(f"{row[0]} - {row[1]}:").upper()
                    row.append(census)
                    if census == "P":
                        presentCount += 1
                    elif census == "A":
                        absentCount += 1
                    line_count += 1
            x.close()
        with open(n1, "w", newline="") as x1:
            writer = csv.writer(x1)
            writer.writerows(rows)
            x1.close()
        totalCount = len(rows) - 1
        totalPresent = (presentCount/totalCount)*100
        totalAbsent = (absentCount/totalCount)*100
        print(f"Attendance Summary for {date}:")
        print(f"Total Students: {totalCount}")
        print(f"Present: {presentCount} ({totalPresent:.2f}%)")
        print(f"Absent: {absentCount} ({totalAbsent:.2f}%)")
        with open("monitoring.csv", "r") as f3:
            csv_reader1 = csv.reader(f3, delimiter=",")
            m_rows = list(csv_reader1)
            for mrow in m_rows:
                sendMessage(mrow[0], date, n1, n2)
            f3.close()
    else:
        print("The given file is not exits, please create a new file.")
        startRollCall()

def updateAttendance():
    date = input("Enter the date:")
    course_subject = input("Enter the course subject:")
    number = input("Enter the course number:")
    n1 = course_subject + "_" + number + ".csv"
    n2 = course_subject + "_" + number
    if os.path.exists(n1):
        with open(n1, "r")as x:
            csv_reader = csv.reader(x, delimiter=",")
            rows = list(csv_reader)
            line_count = 0
            header_row = rows[0]
            in1 = header_row.index(date)
            print(f"Update the attendance record for the {date}:")
            for row in rows:
                if line_count == 0:
                    line_count += 1
                else:
                    print("Please Enter '1' for present, '0' for absent and '-1' for tardy.")
                    census = input(f"{row[0]} - {row[1]}: {row[in1]} ")
                    row[in1] = census
                    line_count += 1
            x.close()
        with open(n1, "w", newline="") as x1:
            writer = csv.writer(x1)
            writer.writerows(rows)
            x1.close()
        with open("monitoring.csv", "r") as f3:
            csv_reader1 = csv.reader(f3, delimiter=",")
            m_rows = list(csv_reader1)
            for mrow in m_rows:
                sendMessage(mrow[0], date, n1, n2)
            f3.close()
    else:
        print("The given file is not exits, please create a new file.")
        startRollCall()

def modifyAttendance():
    date = input("Enter the date:")
    course_subject = input("Enter the course subject:")
    number = input("Enter the course number:")
    n1 = course_subject + "_" + number + ".csv"
    n2 = course_subject + "_" + number
    if os.path.exists(n1):
        with open(n1, "r") as x:
            csv_reader = csv.reader(x, delimiter=",")
            rows = list(csv_reader)
            header_row = rows[0]
            in1 = header_row.index(date)
            print(f"Modify the student's attendance record for the {date}:")
            student_id = input("Enter the student ID to modify:")
            for row in rows:
                if row[0] == student_id:
                    print("Enter the modification:")
                    census = input(f"{row[0]} - {row[1]}: {row[in1]} ")
                    row[in1] = census
            x.close()
        with open(n1, "w", newline="") as x1:
            writer = csv.writer(x1)
            writer.writerows(rows)
            x1.close()
        with open(n1, "r") as x:
            csv_reader = csv.reader(x, delimiter=",")
            rows = list(csv_reader)
            for row in rows:
                with open("monitoring.csv", "r") as f3:
                    csv_reader1 = csv.reader(f3, delimiter=",")
                    m_rows = list(csv_reader1)
                    for mrow in m_rows:
                        if mrow[0] == row[0]:
                            sendMessage(mrow[0], date, n1, n2)
                    f3.close()
            x.close()
    else:
        print("The given file is not exits, please create a new file.")
        startRollCall()

access_point = loginSystem()
while access_point:
    print("Options:")
    print("1: start Roll Call")
    print("2: Roll Call")
    print("3: Update")
    print("4: modify")
    print("5: Save")
    choice = int(input("Enter your choice(1-5):"))
    if choice == 1:
        startRollCall()
    if choice == 2:
        rollCall()
    if choice == 3:
        updateAttendance()
    if choice == 4:
        modifyAttendance()
    if choice == 5:
        access_point = False