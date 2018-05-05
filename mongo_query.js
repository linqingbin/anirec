
// 查询带有"Slice of Life"的未看过的动画作品，并根据受欢迎度降序排序
db.getCollection('animeinfo').find(
    {
        genres:"Slice of Life",
        isviewed:false
    }
    ).sort({popularity:-1})




// 统计动画类别的分布情况

db.getCollection('animeinfo').aggregate([
    {
       $unwind : "$genres"
    },
    {
       $group : {_id:"$genres",numbers:{"$sum":1}}
    },
    {
       $sort : {numbers:-1}
    }
])

// unwind是可以将数组分离为分散的数值
// addToSet是可以在汇总中将分散的数值合并为去重的数组，即集合。因为distinct不能用于aggregate内部，所以可以用这个实现。


// 用于输出的查询
db.getCollection('animeinfo').find(
    {
        isviewed: {$in: [false]}
    },
    {
        id:1,title_japanese:1,start_date_fuzzy:1,popularity:1,image_url_lge:1,genres:1,total_episodes:1,isviewed:1,description:1
    }
    )

// 动画推荐基础数据的查询

db.getCollection('animeinfo').aggregate([
    {
       $project:{id:1,title_japanese:1,start_date_fuzzy:1,popularity:1,genres:1,total_episodes:1,isviewed:1}
    },
    {
       $unwind : "$genres"
    }])

// 删除字段
db.getCollection('animeinfo').updateMany({isviewed:false},{$unset:{random_score:""}})


// 添加字段
db.getCollection('animeinfo').update({"id":100},{$set:{"viewed_users":[]}})

// 给列表字段添加值
db.getCollection('animeinfo').update({"id":100},{$addToSet:{"viewed_users":"0"}})

// 日期筛选
db.getCollection('animeinfo').find({start_date_fuzzy:{$gte:20180101,$lt:20190101}})