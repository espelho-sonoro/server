import tweepy

class TwitterService(object):

    def __init__(self, app):
        consumer_token = app.config['TWITTER_CONSUMER_TOKEN']
        consumer_secret = app.config['TWITTER_CONSUMER_SECRET']
        access_token = app.config['TWITTER_ACCESS_TOKEN']
        access_secret = app.config['TWITTER_ACCESS_SECRET']
        self.user_id = app.config['TWITTER_USER_ID']
        self.logger = app.logger
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)

    def get_last_status_image(self):
        last_status = self.api.user_timeline(user_id=self.user_id, count=1)
        image = last_status[0].entities['media'][0]['media_url_https']
        self.logger.info('Current status: %s' % image)
        return image
