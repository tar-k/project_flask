from flask import Flask, request, jsonify
from flask.views import MethodView
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

class Links(MethodView):

    def get(self):
        return jsonify(links), HTTPStatus.ACCEPTED

    def post(self):
        r = request.get_json()
        title = r['title']
        url = r['url']
        new_link = {'id': len(links)+1,'title': title, 'url': url}
        links.append(new_link)
        return jsonify({'message': "Success!"}), HTTPStatus.CREATED

class Link(MethodView):

    def get(self, id):
        for i in links:
            if i['id'] == id:
                return jsonify(i), HTTPStatus.ACCEPTED 
        return jsonify({'message': 'not found'}), HTTPStatus.NOT_FOUND

    def put(self, id):
        for ix, el in enumerate(links):
            if el['id'] == id:
                r = request.get_json()
                for i in r:
                    if i not in ('title', 'url'):
                        return jsonify({'message': 'invalid payload'}), HTTPStatus.BAD_REQUEST
                links[ix].update(r)
                return jsonify({'message': 'success'}), 201
        return jsonify({'message': 'not found'}), HTTPStatus.NOT_FOUND

app.add_url_rule('/links', view_func=Links.as_view('links'))
app.add_url_rule('/link/<int:id>', view_func=Link.as_view('link'))

if __name__ == '__main__':
    app.run()