from datetime import datetime

import logging

MINUTES_IN_CONTROL = 1
TICK_INTERVAL_IN_SECONDS = 5

class QueueController(object):

    def __init__(self, app, socketio, dao):
        self.dao = dao
        self.app = app
        self.socketio = socketio
        self.change_controll_callback = lambda user: user
        self.update_queue_callback = lambda: None

    def queue(self):
        queue = self.dao.list()
        return [ qe.__json__() for qe in queue ]

    def current_controller_id(self):
        controller = self.dao.head()
        return controller.user_id if controller else None

    def start_dequeing(self):
        return self.socketio.start_background_task(target=self.__tick)

    def append_queue(self, new_element):
        try:
            self.dao.save(new_element.id, new_element.name, datetime.now())
        except Exception as e:
            self.app.logger.error('Failed to insert user in queue: %s', e)
            return False
        else:
            return self.queue()

    def __tick(self):
        while True:
            self.move_queue()
            seconds_to_next_tick = TICK_INTERVAL_IN_SECONDS - (datetime.now().time().second % TICK_INTERVAL_IN_SECONDS)
            self.socketio.sleep(seconds_to_next_tick)

    def move_queue(self):
        done_controllers = self.dao.clear_done(MINUTES_IN_CONTROL)

        if done_controllers > 0:
            self.app.logger.info('Cleaned elements: %i', done_controllers)
            self.update_queue_callback()
        else:
            self.app.logger.debug('Not cleaned queue')

        controller = self.dao.head()
        if controller and not controller.is_controlling:
            self.assign_to_control(controller)
        else:
            self.app.logger.debug('No controller available')

    def assign_to_control(self, user):
        self.app.logger.info('Change operator to: %s', str(user))
        user.started_control = datetime.now()
        self.change_controll_callback(user.user_id)
