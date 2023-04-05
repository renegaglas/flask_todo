from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

# let flask connet to the mango database using the credential of the super user
client = MongoClient("mongodb+srv://databaseuser:zxgpmomhDD6w2xLe5bAYvcpu6X9KJJZ@cluster0.v7d4e0r.mongodb.net/?retryWrites=true&w=majority")

# load mango database
db = client.test
#
db = client.flask_db
#
todos = db.todos
blocks = db.blocks


# set index() as a response to the url '/'
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':  # true when the button submit is clicked
        # get the content and degree from the form of the index page
        content = request.form['content']
        degree = request.form['degree']
        block_id = request.form['block_id']
        # add content and degree in the mango data base
        todos.insert_one({'content': content, 'degree': degree, 'block_id': ObjectId(block_id)})
        return redirect(url_for('index'))  # reload the index page with get method

    all_todos = list(todos.find())  # load every object in the data base to display them
    all_blocks = list(blocks.find()) # we use a list because other wise we can't go two time through the element in the blocks data base
    return render_template('index.html', todos=all_todos, blocks=all_blocks)

@app.route('/create_block', methods=('GET', 'POST'))
def create_block():
    if request.method == 'POST':  # true when the button submit is clicked
        # get the content and degree from the form of the index page
        block_name = request.form['block_name']
        # add content and degree in the mango data base
        blocks.insert_one({'name': block_name})
        return redirect(url_for('create_block'))  # reload the index page with get method

    all_blocks = blocks.find() # we use a list because other wise we can't go two time through the element in the blocks data base
    return render_template('create_block.html', blocks=all_blocks)



# set delete(id) as a response to the url '/<id>/delete/' and ipose the post method
@app.post('/<id>/delete/')
def delete(id):
    # delete the object with the coresponding id in the mango date base
    print(todos.delete_one({"_id": ObjectId(id)}))
    # then reload the index page wich will reload the data base
    return redirect(url_for('index'))

# set delete(id) as a response to the url '/<id>/delete/' and ipose the post method
@app.post('/<id>/delete_block/')
def delete_block(id):
    # delete the object with the coresponding id in the mango date base
    todos.delete_many( {"block_id": ObjectId(id)} ) #delete every memo link to the block
    blocks.delete_one({"_id": ObjectId(id)}) #delete the block
    # then reload the index page wich will reload the data base
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
delete_block