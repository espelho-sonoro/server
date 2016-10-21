from datetime import datetime

import logging

class QueueController(object):

    def __init__(self, app, socketio, dao):
        self.dao = dao
        self.app = app
        self.socketio = socketio

    def queue(self):
        queue = self.dao.list()
        return [ qe.__json__() for qe in queue ]

    def start_dequeing(self):
        return self.socketio.start_background_task(target=self.__tick)

    def append_queue(self, new_element):
        self.dao.save(new_element.id, new_element.name, datetime.now())
        return self.queue()

    def __tick(self):
        while True:
            self.move_queue()
            seconds_to_next_tick = 5 - (datetime.now().time().second % 5)
            self.socketio.sleep(seconds_to_next_tick)

    def move_queue(self):
        dones = self.dao.clear_done(1)
        if dones:
            self.app.logger.info('Cleaned elements: ' + str(dones))
            head = self.dao.head()
            self.assign_to_control(head)
        else:
            self.app.logger.debug('Not cleaned queue')

    def assign_to_control(self, user):
        if user and not user.started_control:
            self.app.logger.info('Assigned ' + str(user) + ' to operate camera')
            user.started_control = datetime.now()
