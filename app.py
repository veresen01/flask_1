from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r}>' % self.id

@app.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    # return render_template('posts.html', articles=articles)
    return render_template('index.html', articles=articles)
    # return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    return render_template('posts.html')


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/create_article' , methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            # flash('Статья добавлена', category='success')
            return redirect('/')

        except:
            # flash('При добавлении статьи произошла ошибка', category='error')
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_article.html')


@app.route('/posts/<int:id>/del')
def post_del(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/posts/<int:id>/update',methods=['POST','GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title=request.form['title']
        article.intro=request.form['intro']
        article.text=request.form['text']


        try:

            db.session.commit()
            return redirect('/')
        except:
            return 'ошибка при редактировании статьи'
    else:

        return render_template('post_update.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)