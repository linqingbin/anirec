from anirec import dbmanage
from anirec import anime_info_get
from anirec import recommand

json_dp = 'anirec/data/anime_info/'
db_host = 'localhost'
db_port = 27017
# anime_info_get.main(min_year=2017,max_year=2018)
# db = dbmanage.Mongodb(db_host,db_port) 
# db.json2db(json_dp)
recommand.main()


