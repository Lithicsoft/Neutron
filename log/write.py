from account.reliability import get_user_reliability
from account.userid import get_user_id

def log(cursor, username, password, job, string):
    log_file = open("./log.txt", "a", encoding='utf-8')
    log_string = "User: " + username + " (ID:" + str(get_user_id(cursor, username)) + ")/(Reliability:" + str(get_user_reliability(cursor, username, password)) + "): " + job + ": " + string
    log_file.write(log_string + '\n')
    log_file.close()

def sys_log(job, string):
    log_file = open("./log.txt", "a", encoding='utf-8')
    log_string = "SYS: " + job + ": " + string
    log_file.write(log_string + '\n')
    log_file.close()
