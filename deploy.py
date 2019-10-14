import sys
import MySQLdb

db = None
try:
    db = MySQLdb.connect("127.0.0.1", "root", "mHsJ33lF+1FZ", "rmtest")
except:
    db = MySQLdb.connect("db", "root", "mHsJ33lF+1FZ", "rmtest")

cursor = db.cursor()


def check_migration():

    if len(sys.argv) < 3:
        print('Please provide a correct parameter. You need provide a migation name, such as "migr2"')
        return
    migr_name = sys.argv[2]

    sql = "SELECT a.name,  IF(b.id IS NULL,'missing','OK') FROM tenants a left JOIN (SELECT * FROM migrations WHERE NAME ='{0}') b ON a.id=b.tenant_id".format(
        migr_name)

    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row[0]+':'+row[1])


def count_migrations():
    sql = 'SELECT a.name, b.cnt FROM tenants a LEFT JOIN (SELECT tenant_id,count(1) cnt FROM migrations GROUP BY tenant_id) b ON a.id=b.tenant_id'
    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row[0]+':'+str(row[1]))


def main():
    if (len(sys.argv)<2):
        print('please provide a parameter')
        return
    para = sys.argv[1]
    if para == 'check-migration' or para == 'check-migrations' or para == 'check':
        check_migration()
    elif para == 'count-migrations' or  para == 'count-migration' or  para == 'count':
        count_migrations()
    else:
        print('please provide correct parameters')


if __name__ == "__main__":
    main()
