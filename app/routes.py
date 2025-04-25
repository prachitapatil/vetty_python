from flask import Blueprint, request, jsonify, Flask
from datetime import datetime
import requests 
from .utils import token_required
from .coin_service import get_all_coins, get_categories, get_filtered_coins
from flasgger import Swagger, swag_from

app = Flask(__name__)


main_bp = Blueprint("main", __name__)

APP_VERSION = "1.0.0"
API_VERSION = "1.0.0"
BUILD_TIME = "2025-04-12"  


def check_third_party_services():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking third-party service: {e}")
        return False

@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check for the application and third-party services.
    ---
    responses:
        200:
            description: Application and third-party service status
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "OK"
                    timestamp:
                        type: string
                        example: "2025-04-12T15:03:00Z"
                    third_party_status:
                        type: string
                        example: "Healthy"
    """
    app_health = {"status": "OK", "timestamp": datetime.utcnow().isoformat()}
    third_party_health = check_third_party_services()
    app_health["third_party_status"] = "Healthy" if third_party_health else "Unhealthy"
    return jsonify(app_health), 200



@main_bp.route('/version', methods=['GET'])
def version_info():
    """
    Version information for the application and API.
    ---
    responses:
        200:
            description: Version details
            schema:
                type: object
                properties:
                    app_version:
                        type: string
                        example: "1.0.0"
                    api_version:
                        type: string
                        example: "1.0.0"
                    build_time:
                        type: string
                        example: "2025-04-12"
                    timestamp:
                        type: string
                        example: "2025-04-12T15:03:00Z"
    """
    version_data = {
        "app_version": APP_VERSION,
        "api_version": API_VERSION,
        "build_time": BUILD_TIME,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(version_data), 200



@main_bp.route("/coins", methods=["GET"])
@token_required
def coins():
    """
    Get a paginated list of all coins.
    ---
    parameters:
        - name: page_num
          in: query
          type: integer
          required: false
          default: 1
        - name: per_page
          in: query
          type: integer
          required: false
          default: 10
    security:
        - Bearer: []
    responses:
        200:
            description: Paginated list of coins
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: string
                            example: "bitcoin"
                        symbol:
                            type: string
                            example: "btc"
                        name:
                            type: string
                            example: "Bitcoin"
    """
    all_coins = get_all_coins()
    if not isinstance(all_coins, list):
        return jsonify({"error": "Unexpected response format"}), 500
    page = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(all_coins[start:end])


@main_bp.route("/categories", methods=["GET"])
@token_required
def categories():
    """
    Get the list of available coin categories.
    ---
    security:
        - Bearer: []
    responses:
        200:
            description: A list of categories
            schema:
                type: array
                items:
                    type: object
                    properties:
                        category_id:
                            type: string
                            example: "decentralized-finance-defi"
                        name:
                            type: string
                            example: "Decentralized Finance (DeFi)"
    """
    return jsonify(get_categories())


@main_bp.route("/filtered-coins", methods=["GET"])
@token_required
def filtered():
    """
    Get filtered coins by coin ID (with pagination).
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: false
          description: The CoinGecko coin ID (e.g., "bitcoin,ethereum")
        - name: page_num
          in: query
          type: integer
          required: false
          default: 1
        - name: per_page
          in: query
          type: integer
          required: false
          default: 10
    security:
        - Bearer: []
    responses:
        200:
            description: Paginated list of filtered coins
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: string
                            example: "bitcoin"
                        symbol:
                            type: string
                            example: "btc"
                        name:
                            type: string
                            example: "Bitcoin"
                        current_price:
                            type: number
                            example: 65847.23
    """
    coin_id = request.args.get("id")
    page = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    data = get_filtered_coins(ids=coin_id)
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format, expected a list."}), 400
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(data[start:end])
