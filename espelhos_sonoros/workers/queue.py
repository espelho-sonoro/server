from datetime import datetime

class QueueWorker(object):

    def __init__(self, app, socketio, controller):
        self.app = app
        self.socketio = socketio
        self.controller = controller

    def start_dequeing(self):
        tick_interval = self.app.config['TICK_INTERVAL']
        rotation_time = self.app.config['USER_ROTATION_TIME']
        self.app.logger.debug('Ticking in interval: %d', tick_interval)
        self.app.logger.debug('Rotating users with time: %d', rotation_time)

        def dequeue():
            while True:
                self.move_queue(rotation_time)
                seconds_to_next_tick = tick_interval - (datetime.now().time().second % tick_interval)
                self.app.logger.trace('Next tick in: %d seconds', seconds_to_next_tick)
                self.socketio.sleep(seconds_to_next_tick)

        self.socketio.start_background_task(target=dequeue)

    def move_queue(self, rotation_time):
        done_users = self.controller.list_done(rotation_time)
        if done_users:
            self.app.logger.info('Cleaned elements: %s', done_users)
            self.controller.remove_users(done_users)
        else:
            self.app.logger.trace('Not cleaned queue')

        candidate = self.controller.next_candidate()

        if candidate and not candidate.is_controlling:
            self.controller.assign_to_control(candidate)
            self.app.logger.debug('Next controller is: %s', candidate)
        else:
            self.app.logger.trace('Not changed controller')
