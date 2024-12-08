from resources import BookListResource, BookResource


def init_routes(api, book_model):
    api.add_resource(BookResource, '/books/<string:book_id>', resource_class_args=[book_model])
    api.add_resource(BookListResource, '/books', resource_class_args=[book_model])