from datetime import datetime

class QueueController(object):

    def __init__(self, dao):
        self.dao = dao

    def queue(self):
        return self.dao.list()

    def append_queue(self, new_element):
        self.dao.save(new_element.id, new_element.name, datetime.now())
        return self.dao.list()
