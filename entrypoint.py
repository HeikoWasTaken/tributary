import json
import redis as redis
from flask import Flask, request
from loguru import logger


HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"


app = Flask(__name__)

@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200


@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    # payload = request.get_json(force=True)
    # logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    engine_temperatures = [float(r) for r in database.lrange(DATA_KEY, 0, -1)]
    logger.info(f"engine temperature list retrieved from redis: {engine_temperatures}")

    latest_temperature = engine_temperatures[0]
    logger.info(f"current engine temperature: {latest_temperature}")

    mean_temperature = round(sum(engine_temperatures)/len(engine_temperatures), 2)
    logger.info(f"average engine temperature: {mean_temperature}")

    logger.info(f"collect request successful")
    response = {
        "success": True,
        "current_engine_temperature": latest_temperature,
        "average_engine_temperature": mean_temperature
    }, 200
    return response
