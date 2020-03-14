from flask import Flask, request, jsonify
from  http import  HTTPStatus

links = [{
            'id':1,
            'url': 'htttp://',
            'title': 'oop basics'
        },
        {
            'id':2,
            'url': 'htttp://hadr.com/',
            'title': 'frontend'
        },
        ]

app = Flask(__name__)

@app.route('/links', methods=['GET'])
def get_all_links():
    return jsonify(links), HTTPStatus.ACCEPTED

@app.route('/links', methods=['POST'])
def post_link():
    r = request.get_json()
    title = r['title']
    url = r['url']
    new_link = {'id': len(links)+1,'title': title, 'url': url}
    links.append(new_link)
    return jsonify({'message': "Success!"}), HTTPStatus.CREATED

@app.route('/link/<int:id>', methods=['GET'])
def get_link(id):
    for i in links:
        if i['id'] == id:
            return jsonify(i), HTTPStatus.ACCEPTED 
    return jsonify({'message': 'not found'}), HTTPStatus.NOT_FOUND

@app.route('/link/<int:id>', methods=['PUT'])
def update_link(id):
    for ix, el in enumerate(links):
        if el['id'] == id:
            r = request.get_json()
            for i in r:
                if i not in ('title', 'url'):
                   return jsonify({'message': 'invalid payload'}), HTTPStatus.BAD_REQUEST
            links[ix].update(r)
            return jsonify({'message': 'success'}), 201
    return jsonify({'message': 'not found'}), HTTPStatus.NOT_FOUND

if __name__ == '__main__':
    app.run()