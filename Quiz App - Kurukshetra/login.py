import csv


def init_user_file():
    columns = ["Name", "Roll Number", "Score"]
    with open('users.csv', 'w', newline='') as userfile:
        csv_writer = csv.writer(userfile)
        csv_writer.writerow(columns)


def create_csv(data):

    try:
        with open('users.csv', 'a', newline='') as userfile:
            csv_writer = csv.writer(userfile)
            csv_writer.writerow(data)
        return 0
    except Exception as e:
        return -1


init_user_file()
create_csv(["Jishnu", "241EE121"])
