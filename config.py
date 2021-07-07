import ssl

ssl._create_default_https_context = ssl._create_unverified_context

default_constr = "mysql+pymysql://fmmanager:Zzkj3333@rm-bp1x76yga76x16n4ybo.mysql.rds.aliyuncs.com:3306/cmpdw"
kw_topk = 20
kw_topk_image = 5
root_dir = r'D:\filedata'
test_username = 'uname'
nlpserver = 'http://localhost:9027/chlangs'

backendserver = 'http://cloudtest.ibuildingsh.com'
n_for_project_in_loop = 1000
exclude_projects = [685, 434]

skip_file_types = ['jpg', 'png', 'mp4', 'xls', 'xlsx',
                   'css', 'js', 'html', 'gif', 'js',
                   'qm', 'mov', 'mts',
                   'vob', 'avi', 'wav', 'exe', 'iso']

batch_file_upload_root = r'F:\402\testupload'

token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjEiLCJOYW1lIjoicm9vdCIsIlVzZXJUeXBlIjoi' \
        '6LaF57qn566h55CG5ZGYIiwiQ29tcGFueSI6Iua1i-ivleWFrOWPuCIsIkNvbXBhbnlJZCI6IjEiLCJuYmYiOjE1ODkyND' \
        'Y5OTYsImV4cCI6MTY4OTg1MTc5NiwiaWF0IjoxNTg5MjQ2OTk2LCJpc3MiOiJTQ0M0In0.grzJjGbVp7YtC5yVajMJV' \
        'GNICfkP0wLNbuM6hurm7ys'

analyzing_projects = [4]
web_keywords_num = 5

CONSTR = {
    'test': "mysql+pymysql://root:Bim54519518@testdb.ibuildingsh.com:3306/ibuildingcloud-test",
}
