count_files = 0
count_files_cur = 0


def Inc(*args):
    """
        args: count_files, count_files_cur 
    """
    if args[0] == "count_files":
        global count_files
        count_files+=1
    if args[0] == "count_files_cur":
        global count_files_cur
        count_files_cur+=1
        
def Get(what):
    if what == 'count_files':
        return count_files
    if what == 'count_files_cur':
        return count_files_cur