def sys_log(job, string):
    log_file = open("./log.txt", "a")
    log_string = "SYS: " + job + ": " + string
    log_file.write(log_string + '\n')
    log_file.close()
