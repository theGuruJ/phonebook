from google.appengine.ext import ndb
import webapp2
import json
import copy



#============ Models ==================================


#============Separate Models - Experimental ==================

class Phone_Exp(ndb.Model):
    phone_no_type = ndb.StringProperty()
    phone_number = ndb.StringProperty()

class PhoneBook_Exp(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone_exp_key = ndb.KeyProperty(kind='Phone_Exp', repeated=True)
    street_address = ndb.StringProperty()
    city = ndb.StringProperty()
    pin = ndb.StringProperty()
    state = ndb.StringProperty()
    country = ndb.StringProperty()



#==========Initial Model, with structured property ===========


class Phone(ndb.Model):
    phone_no_type = ndb.StringProperty()
    phone_number = ndb.StringProperty()


class PhoneBook(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone = ndb.StructuredProperty(Phone,repeated=True)
    street_address = ndb.StringProperty()
    city = ndb.StringProperty()
    pin = ndb.StringProperty()
    state = ndb.StringProperty()
    country = ndb.StringProperty()

    @staticmethod
    def create_entry(user_details):

        phonebook = PhoneBook()
        phone_data = user_details.get('phone')
        phonebook_data = user_details.get('phonebook')
        phonebook.populate(**phonebook_data)
        if phone_data is not None:
            for key, value in phone_data.iteritems():
                phonebook.phone.append(Phone(phone_no_type=key, phone_number=value))
        return phonebook.put().id()

    @staticmethod
    @ndb.transactional(xg=True)
    def create_entry_exp(user_details):
        '''
        code is incomplete, do not use until completed
        :param user_details:
        creating entry in the new DB model.
        create a phone book entity, save it and read the key,
        update phone model with the phone number details and also read its key and write the same to the phonebook.
        use transactions to complete this.
        :return:
        '''

        phone_data = user_details.get('phone')
        phonebook_data = user_details.get('phonebook')

        if phone_data is not None:
            phonelist = []
            for key, value in phone_data.iteritems():
                phonelist.append(Phone_Exp(phone_no_type=key, phone_number=value))
        phone_keys_multi = ndb.put_multi(phonelist)

        phonebook_exp = PhoneBook_Exp()
        phonebook_exp.populate(**phonebook_data)
        print phonebook_exp
        phonebook_key = phonebook_exp.put()
        print phonebook_key
        phonebook_exp.phone_exp_key = phone_keys_multi
        phonebook_exp.put()
        return phonebook_key.id()


    @staticmethod
    def create_child_entry(user_details):
        '''
        :param user_details:
        :return:
        '''
        key_for_parent = ndb.Key('PhoneBook', 4644337115725824)
        phonebook = PhoneBook(parent=key_for_parent)
        phonebook.name=user_details.get('name')
        phonebook.email=user_details.get('email')
        for key, value in user_details.get('phone').iteritems():
            phonebook.phone.append(Phone(phone_no_type=key, phone_number=value))
        phonebook.street_address = user_details.get('street_address')
        phonebook.city = user_details.get('city')
        phonebook.pin = user_details.get('pin')
        phonebook.state = user_details.get('state')
        phonebook.country = user_details.get('country')
        print phonebook
        return phonebook.put().id()


    @staticmethod
    def get_entity_by_key(key):
        phone_book_key = ndb.Key(PhoneBook, key)
        phone_book_entry = phone_book_key.get()
        output = {phone_book_entry.key.id(): phone_book_entry.to_dict() }
        # output_obj = {}
        # output_obj.update({'name': phone_book_entry.name})
        # output_obj.update({'email': phone_book_entry.email})
        # phone = {}
        # if phone_book_entry.phone is not None:
        #     for i in phone_book_entry.phone:
        #         phone.update({i.phone_no_type: i.phone_number})
        # print phone
        # output_obj.update({'phone': phone})
        # output_obj.update({'street_address': phone_book_entry.street_address})
        # output_obj.update({'city': phone_book_entry.city})
        # output_obj.update({'pin': phone_book_entry.pin})
        # output_obj.update({'state': phone_book_entry.state})
        # output_obj.update({'country': phone_book_entry.country})
        # print "this is the output object", output_obj
        # print phone_book_entry.key.id()
        # output.update({phone_book_entry.key.id(): output_obj})
        return json.dumps(output)


    @staticmethod
    def get_entity_by_query( name, email):
        query_result = PhoneBook.query(PhoneBook.name=='Thor_7654', PhoneBook.email=='thor_34567@avengers.com').fetch()
        # print len(query_result)
        output = {}
        for entity in query_result:
            output.update({entity.key.id(): entity})
        print output
        # phone_book_entry = phone_book_key.get()
        # output = {}
        # output_obj = {}
        # # print value
        # output_obj.update({'name': phone_book_entry.name})
        # output_obj.update({'email': phone_book_entry.email})
        # phone = {}
        # # print value.phone
        # if phone_book_entry.phone is not None:
        #     # print len(value.phone)
        #     for i in phone_book_entry.phone:
        #         phone.update({i.phone_no_type: i.phone_number})
        # print phone
        # output_obj.update({'phone': phone})
        # output_obj.update({'street_address': phone_book_entry.street_address})
        # output_obj.update({'city': phone_book_entry.city})
        # output_obj.update({'pin': phone_book_entry.pin})
        # output_obj.update({'state': phone_book_entry.state})
        # output_obj.update({'country': phone_book_entry.country})
        # print "this is the output object", output_obj
        # print phone_book_entry.key.id()
        # output.update({phone_book_entry.key.id(): output_obj})
        return json.dumps(output)



    @staticmethod
    def get_all_entries():
        output_to_send = PhoneBook.query()
        output_obj = {}
        # print type(output_to_send)
        if output_to_send is not None:
            counter = 0
            for value in output_to_send:
                counter = counter + 1
                # print counter
                # print "This is the value ------------>", value, "\n\n\n\n"

                output_sub_obj = {}
                # print value.__dict__.get('_values')
                # print value
                print value._properties
                output_sub_obj.update({'name': value.name})
                output_sub_obj.update({'email': value.email})
                phone = {}
                # print value.phone
                if value.phone is not None:
                    # print len(value.phone)
                    for i in value.phone:
                        phone.update({i.phone_no_type: i.phone_number})
                # print phone
                output_sub_obj.update({'phone': phone})
                output_sub_obj.update({'street_address': value.street_address})
                output_sub_obj.update({'city': value.city})
                output_sub_obj.update({'pin': value.pin})
                output_sub_obj.update({'state': value.state})
                output_sub_obj.update({'country': value.country})
                # print "this is the output sub object", output_sub_obj
                # print value.key.id()
                output_obj.update({value.key.id(): output_sub_obj})
        return json.dumps(output_obj)


    def query_db(self):
        query_result = self.query(PhoneBook.phone.phone_no_type == "other").fetch()
        output_obj = {}
        print type(query_result)
        if query_result is not None:
            counter = 0
            for value in query_result:
                output_sub_obj = value.to_dict()
                # output_sub_obj.update({'name': value.name})
                # output_sub_obj.update({'email': value.email})
                phone = {}
                if value.phone is not None:
                    for i in value.phone:
                        phone.update({i.phone_no_type: i.phone_number})
                # output_sub_obj.update({'phone': phone})
                # output_sub_obj.update({'street_address': value.street_address})
                # output_sub_obj.update({'city': value.city})
                # output_sub_obj.update({'pin': value.pin})
                # output_sub_obj.update({'state': value.state})
                # output_sub_obj.update({'country': value.country})
                output_obj.update({value.key.id(): output_sub_obj})
        return json.dumps(output_obj)


    @staticmethod
    def query_db_child_entities():
        query_result = Phone_Exp.query(ancestor=ndb.Key('PhoneBook_Exp', 5205088045891584)).fetch()
        output_obj = {}
        print type(query_result)
        print len(query_result)
        if query_result is not None:
            counter = 0
            for value in query_result:
                counter = counter + 1
                print value
                # print counter
                # print "This is the value ------------>", value, "\n\n\n\n"

                # output_sub_obj = {}
                # # print value
                # output_sub_obj.update({'name': value.name})
                # output_sub_obj.update({'email': value.email})
                # phone = {}
                # # print value.phone
                # if value.phone is not None:
                #     # print len(value.phone)
                #     for i in value.phone:
                #         phone.update({i.phone_no_type: i.phone_number})
                # # print phone
                # output_sub_obj.update({'phone': phone})
                # output_sub_obj.update({'street_address': value.street_address})
                # output_sub_obj.update({'city': value.city})
                # output_sub_obj.update({'pin': value.pin})
                # output_sub_obj.update({'state': value.state})
                # output_sub_obj.update({'country': value.country})
                # # print "this is the output sub object", output_sub_obj
                # # print value.key.id()
                # output_obj.update({value.key.id(): output_sub_obj})
        return json.dumps(output_obj)


    def query_db_projection(self):
        query_result = PhoneBook.query().fetch(projection=[PhoneBook.name, PhoneBook.email, PhoneBook.country])
        output_obj = {}
        print len(query_result)
        print query_result
        if query_result is not None:
            counter = 0
            for value in query_result:
                counter = counter + 1
                print counter
                # print "This is the value ------------>", value, "\n\n\n\n"

                output_sub_obj = {}
                # print value
                # print vars(value)
                # print value
                output_sub_obj.update({'name': value.name})
                output_sub_obj.update({'email': value.email})
                # phone = {}
                # print value.phone
                # if value.phone is not None:
                #     print len(value.phone)
                #     for i in value.phone:
                #         phone.update({i.phone_no_type: i.phone_number})
                # print phone
                # output_sub_obj.update({'phone': phone})
                # output_sub_obj.update({'street_address': value.street_address})
                # output_sub_obj.update({'city': value.city})
                # output_sub_obj.update({'pin': value.pin})
                # output_sub_obj.update({'state': value.state})
                output_sub_obj.update({'country': value.country})
                print "this is the output sub object", output_sub_obj
                print type(value.key.id())
                output_obj.update({value.key.id(): output_sub_obj})
        return json.dumps(output_obj)


    def create_entry_custom_key(self,user_details):
        # user_details.get()
        self.name=user_details.get('name')
        self.email=user_details.get('email')
        for key, value in user_details.get('phone').iteritems():
            self.phone.append(Phone(phone_no_type=key, phone_number=value))
            # print key
            # print value
            # print phonebook.phone

            # phone=[Phone(phone_no_type=user_details.get('phone_no_type'),
            #     phone_number=user_details.get('phone_number'))],

        self.street_address = user_details.get('street_address')
        self.city = user_details.get('city')
        self.pin = user_details.get('pin')
        self.state = user_details.get('state')
        self.country = user_details.get('country')

        print self
        return self.put().id()


    @staticmethod
    def update_entry_with_key(user_details):
        key_to_update_in_db = ndb.Key(PhoneBook, int(user_details.get('id')))
        print key_to_update_in_db
        entry_retrieved_by_key = key_to_update_in_db.get()
        print entry_retrieved_by_key
        # key_to_update_in_db.get()
        entry_retrieved_by_key.name=user_details.get('name')
        entry_retrieved_by_key.email=user_details.get('email')
        for key, value in user_details.get('phone').iteritems():
            entry_retrieved_by_key.phone.append(Phone(phone_no_type=key, phone_number=value))
            # print key
            # print value
            # print phonebook.phone

            # phone=[Phone(phone_no_type=user_details.get('phone_no_type'),
            #     phone_number=user_details.get('phone_number'))],

        entry_retrieved_by_key.street_address = user_details.get('street_address')
        entry_retrieved_by_key.city = user_details.get('city')
        entry_retrieved_by_key.pin = user_details.get('pin')
        entry_retrieved_by_key.state = user_details.get('state')
        entry_retrieved_by_key.country = user_details.get('country')

        print entry_retrieved_by_key
        return entry_retrieved_by_key.put().id()

    @staticmethod
    def query_constructor(kind_str, prop, value):
        query = ndb.Query(kind=kind_str, filters=ndb.GenericProperty(prop) == value)
        print query
        query_result = query.fetch()
        result_object = {}
        if query_result is not None:
            for item in query_result:
                result_object.update({item.key.id():item.to_dict()})
        return result_object

