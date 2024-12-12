'''
Created on 16 Jan 2024

@author: jacklok
'''

import logging
from firebase_admin import messaging
from trexconf import conf

logger = logging.getLogger('util')

def create_push_notification(
        title, 
        desc,
        device_token,
        analytics_label = None,
        image=None,
        text=None,
        action_link=None,
        ):
    
    logger.info('title=%s', title)
    logger.info('desc=%s', desc)
    logger.info('device_token=%s', device_token)
    logger.info('image=%s', image)
    logger.info('text=%s', text)
    logger.info('action_link=%s', action_link)
    
    message = messaging.Message(
        notification=messaging.Notification(
            title   = title,
            body    = desc,
            
        ),
        data={
            'image'         : image,
            'text'          : text,
            'action_link'   : action_link,
        },
        token=device_token,
        #analytics_label = analytics_label,
    )
    
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    
    logger.debug('response=%s', response)
    
def create_topic_message(
        title, 
        desc,
        topic,
        analytics_label = None,
        image=None,
        text=None,
        action_link=None,
        ):
    
    logger.info('title=%s', title)
    logger.info('desc=%s', desc)
    logger.info('topic=%s', topic)
    logger.info('image=%s', image)
    logger.info('text=%s', text)
    logger.info('action_link=%s', action_link)
    
    data = {}
    if image:
        data['image'] = image
    
    if text:
        data['text'] = text
    
    if action_link:
        data['action_link'] = action_link        
    
    message = messaging.Message(
        notification=messaging.Notification(
            title   = title,
            body    = desc,
            
        ),
        data=data,
        topic=topic,
        #analyticsLabel=analytics_label,
    )
    
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    
    logger.debug('response=%s', response)
