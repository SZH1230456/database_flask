from flask import Flask,redirect, url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/mimic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db.create_all()


# 路由localhost:5000,输出为Hello World!
@app.route('/')
def index():
    return 'Hello World!'


# 路由localhost:5000,输出为一号字体的Hello World!,这里的<h1>和html中的效果相同
@app.route('/hello')
def hello():
    return '<h1>Hello World!<h1>'


# 路由localhost:5000/hi,重定向至localhost:5000/hello,输出一号字体的Hello World!
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))  # 重定向到/hello


# 路由localhost:5000/hello/<输入的名字>，输出一号字体的Hello World!输入的名字
@app.route('/hello/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# （1）查询：路由localhost:5000/get/all/movies,
# 查询得到所有的movies,展示watchlist.html中的页面。
@app.route('/get/all/movies', methods=['GET'])
def get_all_movies():
    movies = Movies.query.all()
    return render_template('watchlist.html', movies=movies)


# (2) 增加一条记录：路由localhost:5000/add/movie,
# 添加结束之后重定向至localhost:5000/get/all/movies,可以看到已经添加记录
@app.route('/add/movie', methods=['POST'])
def add_movies():
    name = request.form.get('name')
    year = request.form.get('year')
    movie = Movies(name=name, year=year)
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('get_all_movies'))


# (3) 更新一条记录，路由：localhost:5000/update/movie,把CoCo的年份改为0000
# 重定向为localhost:5000/get/all/movies,可以看到此电影上映年份已经修改
@app.route('/update/movie')
def update_movies():
    movie = Movies.query.get("CoCo")
    movie.year = '0000'
    db.session.commit()
    return redirect(url_for('get_all_movies'))


# （4）删除一条记录，路由：localhost:5000/delete/movie,把CoCo这条记录删除，
# 重定向为localhost:5000/get/all/movies,可以看到此记录已经删除
@app.route('/delete/movie')
def delete_movies():
    movie = Movies.query.get("CoCo")
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('get_all_movies'))


# movies类，和数据库中的movies表的字段保持一致
class Movies(db.Model):
    def __name__(self):
        return self.name

    def __year__(self):
        return self.year

    name = db.Column(db.String, primary_key=True)
    year = db.Column(db.String)


# 程序总入口
if __name__ == '__main__':
    app.run()
