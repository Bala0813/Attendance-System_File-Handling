import os
import csv

class Account:
    def __init__(self):
        self.username = None
        self.password = None

    def set_credentials(self):
        self.username = input("Enter the username:")
        self.password = input("Enter the password:")


class CreateAccount(Account):
    def __init__(self):
        super().__init__()

    def create_account(self):
        self.set_credentials()
        try:
            with open("Authentication", "w") as x:
                x.write(self.username)
                x.write(" ")
                x.write(self.password)
        except IOError:
            print("Having IO Error.")
        finally:
            print("Account created successfully.")
            return True


class LoginAccount(Account):
    def __init__(self):
        super().__init__()

    def login_account(self):
        self.set_credentials()
        try:
            with open("Authentication", "r") as x:
                x1 = x.readline()
                l = x1.split()
                u1 = l[0]
                p1 = l[1]
        except IOError:
            print("Error opening the file.")
        finally:
            if self.username == u1 and self.password == p1:
                print("Login Success")
                return True
            else:
                print("Given username or password is incorrect. Try again!")
                self.login_account()

class AddRollCall:
    def create_csv(self, file_path, date, SID, name, monitoringStatus):
        with open(file_path, "w", newline="") as x:
            fieldname = ["SID", "Name"]
            wr = csv.DictWriter(x, fieldnames=fieldname)
            wr.writeheader()
            wr.writerow({"SID": SID, "Name": name})

        if monitoringStatus == "YES":
            with open("monitoring.csv", "w", newline="") as y:
                fieldname1 = ["SID"]
                wr1 = csv.DictWriter(y, fieldnames=fieldname1)
                wr1.writeheader()
                wr1.writerow({"SID": SID})

    def add_roll_call(self, file_path, date, SID, name, monitoringStatus):
        with open(file_path, "a") as x:
            fieldname = ["SID", "Name"]
            wr = csv.DictWriter(x, fieldnames=fieldname)
            wr.writerow({"SID": SID, "Name": name})

        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            file.writelines(lines[:-1])

        if monitoringStatus == "YES":
            with open("monitoring.csv", "a") as y:
                fieldname1 = ["SID"]
                wr1 = csv.DictWriter(y, fieldnames=fieldname1)
                wr1.writerow({"SID": SID})

            with open("monitoring.csv", 'r') as file1:
                lines = file1.readlines()

            with open("monitoring.csv", 'w') as file1:
                file1.writelines(lines[:-1])

    def check_csv(self, file_path, date, SID, name, monitoringStatus):
        if os.path.exists(file_path):
            self.add_roll_call(file_path, date, SID, name, monitoringStatus)
        else:
            self.create_csv(file_path, date, SID, name, monitoringStatus)

    def start_roll_call(self):
        date = input("Enter the date:")
        course_subject = input("Enter the course subject:")
        number = input("Enter the course number:")
        n1 = f"{course_subject}_{number}.csv"
        c1 = True

        while c1:
            c1 = input("If need to continue, enter True, else False:")
            if c1.lower() == "true":
                SID = input("Enter the Student ID:")
                name = input("Enter the Student Name:")
                monitoringStatus = input("Enter status for SMS service (yes/no):").upper()
                self.check_csv(n1, date, SID, name, monitoringStatus)
            else:
                break

class MessageSender:
    @staticmethod
    def send_message(student_id, date, n1, n2):
        key = ""
        with open(n1, "r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            rows = list(csv_reader)
            header_row = rows[0]
            in1 = header_row.index(date)
            line_count = 0
            for row in rows:
                if row == 0:
                    line_count += 1
                else:
                    if row[0] == student_id:
                        key = row[in1]
                    line_count += 1
        key1 = ""
        if key == "P" or key == "1":
            key1 = "present"
        elif key == "A" or key == "0":
            key1 = "absent"
        elif key == "-1":
            key1 = "tardy"

        try:
            with open(f"{student_id}.txt", "w") as x:
                x.write(f"Your {n2} attendance for {date} was changed to {key1}")
                x.write("\n")

        except IOError:
            print("Having IO Error.")


class AttendanceSettings:
    def roll_call(self):
        date = input("Enter the date:")
        course_subject = input("Enter the course subject:")
        number = input("Enter the course number:")
        n1 = f"{course_subject}_{number}.csv"
        n2 = f"{course_subject}_{number}"
        if os.path.exists(n1):
            with open(n1, "r") as x:
                csv_reader = csv.reader(x, delimiter=",")
                rows = list(csv_reader)
                line_count = 0
                present_count = 0
                absent_count = 0
                for row in rows:
                    if line_count == 0:
                        row.append(date)
                        line_count += 1
                    else:
                        print("Please Enter 'P' for present and 'A' for absent.")
                        census = input(f"{row[0]} - {row[1]}:").upper()
                        row.append(census)
                        if census == "P":
                            present_count += 1
                        elif census == "A":
                            absent_count += 1
                        line_count += 1
            with open(n1, "w", newline="") as x1:
                writer = csv.writer(x1)
                writer.writerows(rows)

            totalCount = len(rows) - 1
            total_present = (present_count / totalCount) * 100
            total_absent = (absent_count / totalCount) * 100

            print(f"Attendance Summary for {date}:")
            print(f"Total Students: {totalCount}")
            print(f"Present: {present_count} ({total_present:.2f}%)")
            print(f"Absent: {absent_count} ({total_absent:.2f}%)")

            with open("monitoring.csv", "r") as f3:
                csv_reader1 = csv.reader(f3, delimiter=",")
                m_rows = list(csv_reader1)
                line_count = 0
                for mrow in m_rows:
                    if line_count == 0:
                        line_count += 1
                    else:
                        MessageSender.send_message(mrow[0], date, n1, n2)
                        line_count += 1

        else:
            print("The given file does not exist, please create a new file.")
            AddRollCall().start_roll_call()

    def update_attendance(self):
        date = input("Enter the date:")
        course_subject = input("Enter the course subject:")
        number = input("Enter the course number:")
        n1 = f"{course_subject}_{number}.csv"
        n2 = f"{course_subject}_{number}"
        if os.path.exists(n1):
            with open(n1, "r") as x:
                csv_reader = csv.reader(x, delimiter=",")
                rows = list(csv_reader)
                line_count = 0
                header_row = rows[0]
                in1 = header_row.index(date)
                print(f"Update the attendance record for {date}:")
                for row in rows:
                    if line_count == 0:
                        line_count += 1
                    else:
                        print("Please Enter '1' for present, '0' for absent, and '-1' for tardy.")
                        census = input(f"{row[0]} - {row[1]}: {row[in1]} ")
                        row[in1] = census
                        line_count += 1

            with open(n1, "w", newline="") as x1:
                writer = csv.writer(x1)
                writer.writerows(rows)

            with open("monitoring.csv", "r") as f3:
                csv_reader1 = csv.reader(f3, delimiter=",")
                m_rows = list(csv_reader1)
                line_count = 0
                for mrow in m_rows:
                    if line_count == 0:
                        line_count += 1
                    else:
                        MessageSender.send_message(mrow[0], date, n1, n2)
                        line_count += 1

        else:
            print("The given file does not exist, please create a new file.")
            AddRollCall().start_roll_call()

    def modify_attendance(self):
        date = input("Enter the date:")
        course_subject = input("Enter the course subject:")
        number = input("Enter the course number:")
        n1 = f"{course_subject}_{number}.csv"
        n2 = f"{course_subject}_{number}"
        if os.path.exists(n1):
            with open(n1, "r") as x:
                csv_reader = csv.reader(x, delimiter=",")
                rows = list(csv_reader)
                header_row = rows[0]
                in1 = header_row.index(date)
                print(f"Modify the student's attendance record for {date}:")
                student_id = input("Enter the student ID to modify:")
                for row in rows:
                    if row[0] == student_id:
                        print("Please Enter '1' for present, '0' for absent, and '-1' for tardy.")
                        print("Enter the modification:")
                        census = input(f"{row[0]} - {row[1]}: {row[in1]} ")
                        row[in1] = census

            with open(n1, "w", newline="") as x1:
                writer = csv.writer(x1)
                writer.writerows(rows)

            with open(n1, "r") as x:
                csv_reader = csv.reader(x, delimiter=",")
                rows = list(csv_reader)
                for row in rows:
                    with open("monitoring.csv", "r") as f3:
                        csv_reader1 = csv.reader(f3, delimiter=",")
                        m_rows = list(csv_reader1)
                        for mrow in m_rows:
                            if mrow[0] == row[0]:
                                MessageSender.send_message(mrow[0], date, n1, n2)
                        f3.close()
                x.close()

        else:
            print("The given file does not exist, please create a new file.")
            AddRollCall().start_roll_call()

def loginSystem():
    user_choice = input("Need to create an account? Yes/No:")
    if user_choice.lower() == "yes":
        account = CreateAccount()
        return account.create_account()
    elif user_choice.lower() == "no":
        account = LoginAccount()
        return account.login_account()
    else:
        print("Please enter a valid input!")
        return loginSystem()


access_point = loginSystem()
while access_point:
    print("Options:")
    print("1: Start Roll Call")
    print("2: Roll Call")
    print("3: Update")
    print("4: Modify")
    print("5: Save")
    choice = int(input("Enter your choice (1-5):"))
    addrollcall = AddRollCall()
    settings = AttendanceSettings()
    if choice == 1:
        addrollcall.start_roll_call()
        # pass
        # startRollCall()
    if choice == 2:
        settings.roll_call()
        # pass
        # rollCall()
    if choice == 3:
        settings.update_attendance()
        # pass
        # updateAttendance()
    if choice == 4:
        settings.modify_attendance()
        # pass
        # modifyAttendance()
    if choice == 5:
        access_point = False
