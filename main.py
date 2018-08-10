from google.appengine.ext import ndb
from model import PhoneBook as PhoneBook
import webapp2
import json


class CreateEntry(webapp2.RequestHandler):

    def post(self):
        input_data = json.loads(self.request.body)
        key_from_put = PhoneBook.create_entry(input_data)
        output = PhoneBook.get_entity_by_key(key_from_put)
        self.response.write(output)


class CreateEntryExp(webapp2.RequestHandler):

    def post(self):
        input_data = json.loads(self.request.body)
        key_from_put = PhoneBook.create_entry_exp(input_data)
        self.response.write(key_from_put)


class CreateChildEntry(webapp2.RequestHandler):

    def post(self):
        input_data = json.loads(self.request.body)
        key_for_inserted_entry = PhoneBook.create_child_entry(input_data)
        output = PhoneBook.get_entity_by_key(key_for_inserted_entry)
        self.response.write(output)


class CreateEntryCustomId(webapp2.RequestHandler):

    def post(self):
        input_data = json.loads(self.request.body)
        phonebook = PhoneBook(id=input_data.get('id'))
        key_from_put = phonebook.create_entry_custom_key(input_data)
        output = PhoneBook.get_entity_by_key(key_from_put)
        self.response.write(output)


class UpdateEntryWithKey(webapp2.RequestHandler):

    def post(self):
        input_data = json.loads(self.request.body)
        key_from_put = PhoneBook.update_entry_with_key(input_data)
        output = PhoneBook.get_entity_by_key(key_from_put)
        self.response.write(output)


class DeleteEntry(webapp2.RequestHandler):
    def get(self):
        self.response.write("<p>Hello World!</p>")

    def post(self):
        pass


# class GetEntry(webapp2.RequestHandler):
#     def get(self, user_id):
#         output_data = PhoneBook.get_entity_by_key(long(user_id))
#         self.response.write(output_data)

class GetEntryQuery(webapp2.RequestHandler):
    def get(self, name, email):
        output_data = PhoneBook.get_entity_by_query(name,email)
        # output_data = PhoneBook.get_entity_by_key(long(user_id))
        self.response.write(output_data)



class GetAllEntries(webapp2.RequestHandler):
    def get(self):
        output_data = PhoneBook.get_all_entries()
        self.response.write(output_data)

# ==. !=. >= <=

class QueryDB(webapp2.RequestHandler):
    def get(self):
        input_data = self.request.get('key')
        phonebook = PhoneBook()
        result = phonebook.query_db()
        self.response.write(result)


class QueryDBChildEntries(webapp2.RequestHandler):
    def get(self):
        input_data = self.request.get('key')
        result = PhoneBook.query_db_child_entities()
        self.response.write(result)


class QueryDBProjection(webapp2.RequestHandler):
    def get(self):
        phonebook = PhoneBook()
        result = phonebook.query_db_projection()
        print result
        self.response.write(result)


class QueryConstructor(webapp2.RequestHandler):
    def get(self, kind):
        query_result = PhoneBook.query_constructor(kind)
        self.response.write(query_result)


application = webapp2.WSGIApplication([
    webapp2.Route('/create_entry', CreateEntry),
    webapp2.Route('/create_entry_custom_id', CreateEntryCustomId),
    webapp2.Route('/update_entry_with_key', UpdateEntryWithKey),
    webapp2.Route('/delete_entry', DeleteEntry),
    # ('/get_entry', GetEntry),
    # webapp2.Route(r'/get_entry/<user_id:\d+>', GetEntry),
    webapp2.Route(r'/get_entry/<name:\S+>/<email:\S+>', GetEntryQuery),
    webapp2.Route('/get_all_entries', GetAllEntries),
    # webapp2.Route('/query_db/', QueryDB),
    webapp2.Route('/query_db_c/<kind:\S+>', QueryConstructor),
    webapp2.Route('/query_db_projection/', QueryDBProjection),
    webapp2.Route('/create_child_entry/', CreateChildEntry),
    webapp2.Route('/query_db_child_entries/', QueryDBChildEntries),
    webapp2.Route('/create_entry_exp/', CreateEntryExp),
], debug=True)

