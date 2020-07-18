# -*- coding: utf-8 -*-
import falcon

from app import log, config

from apscheduler.schedulers.background import BackgroundScheduler

from app.api.common import base
from app.api.v1 import didtx, servicecount
from app.errors import AppError

from mongoengine import connect

from app.middleware import AuthMiddleware
from app.model import Didtx
from app.model import Didstate
from app.service import DidPublish

from app.cronjob import send_tx_to_did_sidechain, reset_didpublish_daily_limit

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("API Server is starting")

        # Simple endpoint for base
        self.add_route("/", base.BaseResource())
        # Retrieves all the rows
        self.add_route("/v1/didtx", didtx.Collection())
        # Retrieves the row according to confirmation ID
        self.add_route("/v1/didtx/confirmation_id/{confirmation_id}", didtx.ItemFromConfirmationId())
        # Retreives all rows belonging to a particular DID
        self.add_route("/v1/didtx/did/{did}", didtx.ItemFromDid())
        # Retreives recent 5 rows belonging to a particular DID
        self.add_route("/v1/didtx/recent/did/{did}", didtx.RecentItemsFromDid())
        # Creates a new row 
        self.add_route("/v1/didtx/create", didtx.Create())
        # Retrieves the service count for a particular DID
        self.add_route("/v1/service_count/{service}/{did}", servicecount.GetServiceCount())
         # Retrieves Service Statistics
        self.add_route("/v1/service_count/statistics", servicecount.GetServiceStatistics())
        
        self.add_error_handler(AppError, AppError.handle)


# Connect to mongodb
LOG.info("Connecting to mongodb...")
if config.PRODUCTION:
    connect(
        config.MONGO['DATABASE'],
        host="mongodb+srv://" + config.MONGO['USERNAME'] + ":" + config.MONGO['PASSWORD'] + "@" +
             config.MONGO['HOST'] + "/?retryWrites=true&w=majority"
    )
else:
    connect(
        config.MONGO['DATABASE'],
        host="mongodb://" + config.MONGO['USERNAME'] + ":" + config.MONGO['PASSWORD'] + "@" +
             config.MONGO['HOST'] + ":" + str(config.MONGO['PORT']) + "/?authSource=admin"
    )

LOG.info("Initializing the Falcon REST API service...")
application = App(middleware=[
    AuthMiddleware(),
])


# Start cron scheduler
if not config.PRODUCTION:
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_tx_to_did_sidechain, 'interval', seconds=config.CRON_INTERVAL)
    scheduler.add_job(reset_didpublish_daily_limit, 'interval', hours=24)
    scheduler.start()