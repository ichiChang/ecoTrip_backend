# resources/stop.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.stop import StopModel
from models.place import PlaceModel
from models.day import DayModel
from Schema import StopSchema, AddStopSchema, UpdateStopSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, make_response

blp = Blueprint("Stop", __name__, url_prefix="/stops")


@blp.route("/")
class StopList(MethodView):

    @blp.arguments(AddStopSchema)
    @jwt_required()
    def post(self, stop_data):
        place = PlaceModel.objects(id=stop_data["PlaceId"]).first()
        day = DayModel.objects(id=stop_data["DayId"]).first()
        if not place or not day:
            abort(404, description="Place or Day not found")

        stop = StopModel(
            Name=stop_data["Name"],
            StartTime=stop_data["StartTime"],
            EndTime=stop_data["EndTime"],
            note=stop_data["note"],
            PlaceId=place,
            DayId=day,
        )
        stop.save()
        data = jsonify({"message": f'Stop {stop_data["Name"]} created successfully'})
        return make_response(data,201)
        

    @jwt_required()
    def get(self):
        stops = StopModel.objects()

        data = jsonify(stops)
        return make_response(data,200)
        


@blp.route("/<string:stop_id>")
class StopItem(MethodView):

    @jwt_required()
    def get(self, stop_id):
        stop = StopModel.objects(id=stop_id).first()
        if not stop:
            abort(404, description="Stop not found")

        data = jsonify(stop)
        return make_response(data,200)
        

    @blp.arguments(UpdateStopSchema)
    @jwt_required()
    def put(self, update_data, stop_id):
        StopModel.objects(id=stop_id).update(**update_data)

        data = jsonify({"message": "Stop updated successfully"})
        return make_response(data,200)
        


    @jwt_required()
    def delete(self, stop_id):
        stop = StopModel.objects(id=stop_id).delete()
        if not stop:
            abort(404, description="Stop not found")
        data = jsonify({"message": "Stop deleted successfully"})
        return make_response(data,200)
        
