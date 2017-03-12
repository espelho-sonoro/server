from datetime import datetime, timedelta

import logging

class QueueController(object):

    def __init__(self, app, socketio, dao):
        self.dao = dao
        self.app = app
        self.socketio = socketio
        self.assign_user_callback = lambda user: user
        self.remove_users_callback = lambda users: users
        self.update_queue_callback = lambda: None

    def queue(self, limit=10):
        queue = self.dao.list(limit)
        return [ qe.__json__() for qe in queue ]

    def current_controller_id(self):
        controller = self.dao.head()
        return controller.user_id if controller else None

    def append_queue(self, queue_element):
        try:
            self.dao.save(queue_element.id, queue_element.name, queue_element.room, datetime.now())
        except Exception as e:
            self.app.logger.error('Failed to insert user in queue: %s', e)
            return False
        else:
            return True

    def remove_users(self, users):
        if users:
            for user in users:
                self.dao.remove(user)
            self.remove_users_callback(users)
            self.update_queue_callback()


    def list_done(self, rotation_time):
        limit_time = datetime.now() - timedelta(seconds=rotation_time)
        self.app.logger.debug('Cleaning users that started before: %s', limit_time)
        return self.dao.list_done(limit_time)

    def next_candidate(self):
        return self.dao.next_candidate()

    def assign_to_control(self, user):
        self.app.logger.info('Change operator to: %s', str(user))
        user.started_control = datetime.now()
        self.assign_user_callback(user)

