import sys
import MySQLdb
from multiprocessing import Pool

db = None
try:
    db = MySQLdb.connect("127.0.0.1", "root", "mHsJ33lF+1FZ", "rmtest")
except:
    db = MySQLdb.connect("db", "root", "mHsJ33lF+1FZ", "rmtest")


cursor = db.cursor()

tenant_names = sys.argv[1]
if tenant_names == 'ALL':
    cursor.execute("select name from tenants")
    tenant_names = ''
    for row in cursor.fetchall():
        tenant_names += row[0]+','

# delete the last ','
tenant_names = tenant_names.strip(',')

migration_name = sys.argv[2]


t_names_list = tenant_names.split(',')

worker_cnt = 5


def one_worker(worker):
    cursor.execute("INSERT INTO migrations(tenant_id, name) VALUES ((select id from tenants where name ='{0}'),'{1}')".format(
        worker, migration_name))
    


def parallel():
    # put tenants into different groups
    worker_groups = list()
    for i in range(0, len(t_names_list), worker_cnt):
        worker_groups.append(t_names_list[i:i+worker_cnt])
    # document for multiprocessing: https://docs.python.org/2/library/multiprocessing.html
    
    for one_group in worker_groups:
        p = Pool(worker_cnt)
        p.map(one_worker, one_group)
        db.commit()
        #import time
        # time.sleep(1)
    print('parallel done!')


def sequential():
    for item in t_names_list:
        cursor.execute("INSERT INTO migrations(tenant_id, name) VALUES ((select id from tenants where name ='{0}'),'{1}')".format(
            item, migration_name))
        db.commit()
    print('sequential done!')
    
def main():
    if len(sys.argv) < 4:
        print('please provide correct parameters')
        return 1
    run_type = sys.argv[3]
    if run_type == 'sequential':
        sequential()
    elif run_type == 'parallel':
        parallel()


if __name__ == "__main__":
    main()
