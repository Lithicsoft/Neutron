from account.authentication import get_user_authentication
from account.userid import get_user_id

def log(cursor, username, password, job, string):
    log_file = open("./log.txt", "a", encoding='utf-8')
    log_string = "User: " + username + " (ID:" + str(get_user_id(cursor, username)) + ")/(Authentication:" + str(get_user_authentication(cursor, username, password)) + "): " + job + ": " + string
    log_file.write(log_string + '\n')
    log_file.close()
    print(log_string)
    return log_string

def db_log(log_string):
    log_file = open("./app/templates/log.txt", "a", encoding='utf-8')
    log_file.write(log_string + '\n')
    log_file.close()

def sys_log(job, string):
    log_file = open("./log.txt", "a", encoding='utf-8')
    log_string = "SYS: " + job + ": " + string
    log_file.write(log_string + '\n')
    log_file.close()
    print(log_string)
