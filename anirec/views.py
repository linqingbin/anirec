# -*-coding:utf-8-*-
'''
Date:20171216
Author:linqingbin
Description:路由
'''
import pymongo
import pdb
from flask import Flask, render_template, request, \
    redirect, url_for, jsonify, abort, g, session, flash
import anzen
import urllib


app = Flask(__name__)
app.config.from_object("config")  # 创建app


@app.before_request
def setUp():
    g.const = {}
    # g.db = engine.SearchEngine()
    # URI = 'mongodb://{user}:{pwd}@{host}:{port}'.format(
    #     host=app.config["DBHOST"],
    #     port=27017,
    #     user=urllib.parse.quote_plus(anzen.BOOK["mdb"]["a"]),
    #     pwd=urllib.parse.quote_plus(anzen.BOOK["mdb"]["p"])
    # )
    # print(URI)
    # g.db = pymongo.MongoClient(URI)
    g.db = pymongo.MongoClient(host=app.config["DBHOST"],
                               port=27017)
    g.seasons = {'winter': ["01", "03"],
                 'spring': ["04", "06"],
                 'summer': ["07", "09"],
                 'autumn': ["10", "12"],
                 'all': ["01", "12"]}


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == anzen.BOOK['site']['p'] \
            and request.form['username'] == anzen.BOOK['site']['a']:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        page_num = int(request.args.get('page_num')
                       ) if 'page_num' in request.args else 1
        user_id = int(request.args.get('page_num')
                      ) if 'user_id' in request.args else 0
        if user_id == 0:
            isviewed_status = [False, None, True]
        elif user_id == 1:
            isviewed_status = [False, None]
        isviewed_status = [False, None]
        page_size = 10
        skips = page_size * (page_num - 1)
        r_content = {
            "page_num": page_num
        }

        anime = g.db['anime']
        animelist = anime.animeinfo.find({
            "isviewed": {"$in": isviewed_status}
        },
            {
                "_id": 0,
                "id": 1,
                "title_japanese": 1,
                "title_romaji": 1,
                "start_date_fuzzy": 1,
                "popularity": 1,
                "image_url_lge": 1,
                "image_url_med": 1,
                "genres": 1,
                "total_episodes": 1,
                "isviewed": 1,
                "description": 1
        }).skip(skips).limit(page_size).sort("model_score", pymongo.DESCENDING)
        return render_template('index.html',
                               animelist=list(animelist),
                               r_content=r_content)


@app.route('/isviewed_update', methods=['POST'])
def isviewed_update():
    r_data = request.json
    print(r_data)
    anime = g.db['anime']
    anime.animeinfo.update_one({'id': r_data['anime_id']}, {
                               '$set': {'isviewed': r_data['isviewed']}})
    return ('', 204)


@app.route('/animelist')
def animelist():
    page_num = int(request.args.get('page_num')
                   ) if 'page_num' in request.args else 1
    user_id = int(request.args.get('user_id')
                  ) if 'user_id' in request.args else 0
    filter_paras = ['start_year', 'end_year', 'season', 'status', 'keyword']
    start_year, end_year, season, status, keyword = [
        request.args.get(x) for x in filter_paras]

    def date_genre(start_year, end_year, season):
        # pdb.set_trace()
        if start_year == "":
            start_year = 2000
        if end_year == "":
            end_year = 2018
        # 因为anilist对于播放日未确定的动画日期的日会取0，所以这里也取0
        month_day_map = {0: "00", 1: "31"}
        month_range = g.seasons[season]
        start_date = int(str(start_year) + month_range[0] + month_day_map[0])
        end_date = int(str(end_year) + month_range[1] + month_day_map[1])
        return start_date, end_date

    startdate, enddate = date_genre(start_year, end_year, season)
    if status == 'not_viewed':
        isviewed_status = [False, None, 0, 2]
    elif status == 'marked':
        isviewed_status = [2]
    elif status == 'viewed':
        isviewed_status = [1, True]
    elif status == 'dropped':
        isviewed_status = [-1]
    elif status == 'all':
        isviewed_status = [False, None, -1, 0, 1, True, 2]
    else:
        isviewed_status = [False, None, 0, 2]
    page_size = 10
    skips = page_size * (page_num - 1)

    anime = g.db['anime']
    animelist = anime.animeinfo.find({
        "isviewed": {"$in": isviewed_status},
        "start_date_fuzzy": {"$gte": startdate, "$lt": enddate},
        "$or": [
            {"title_japanese": {
                '$regex': '.*{}.*'.format(keyword), "$options": 'i'}},
            {"title_romaji": {
                '$regex': '.*{}.*'.format(keyword), "$options": 'i'}}
        ]
    },
        {
            "_id": 0,
            "id": 1,
            "title_japanese": 1,
            "title_romaji": 1,
            "start_date_fuzzy": 1,
            "popularity": 1,
            "image_url_lge": 1,
            "image_url_med": 1,
            "genres": 1,
            "total_episodes": 1,
            "isviewed": 1,
            "description": 1
    }).skip(skips).limit(page_size).sort("model_score", pymongo.DESCENDING)
    result = list(animelist)
    # pdb.set_trace()
    return jsonify(result)
