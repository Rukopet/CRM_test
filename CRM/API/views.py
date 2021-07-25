import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

from .models import ClientModel, BidModel
from rest_framework.decorators import api_view


# def bids_list(request):
#     name = ["Oleg", "Vasya", "Petya"]
#     return render(request, 'API/index.html', context={'names': name})
#
#


def documentation(request):
    return render(request, 'API/documentation.html')


class Bids:
    @staticmethod
    @api_view(['GET'])
    def show_all(request):
        try:
            qs = BidModel.objects.all()
            qs_json = serializers.serialize('json', qs)
            return HttpResponse(qs_json, content_type='application/json')
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)


class Clients:

    _clients_fields = ["client_name", "client_telegram_user_id"]

    @staticmethod
    def json_answer(success: bool, description: str, status: int):
        return HttpResponse(json.dumps({"success": success, "description": description}), status=status,
                            content_type='application/json')

    @staticmethod
    @api_view(['GET'])
    def show_all(request):
        try:
            qs = ClientModel.objects.all()
            qs_json = serializers.serialize('json', qs)
            return HttpResponse(qs_json, content_type='application/json')
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET'])
    def show_one(request, client_id: int):
        try:
            qs = [ClientModel.objects.get(client_id=f"{client_id}")]
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        qs_json = serializers.serialize('json', qs)
        return HttpResponse(qs_json, content_type='application/json')

    @staticmethod
    @api_view(['DELETE'])
    def remove_client(request, client_id: int):
        try:
            client = ClientModel.objects.get(client_id=f"{client_id}")
            client.delete()
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)
        else:
            return Clients.json_answer(True, "delete successful", 200)

    @staticmethod
    @api_view(['POST'])
    def create_client(request, name: str, telegram: str):
        tg_id = Clients.validate_telegram_id(telegram)
        if name.isspace() or not tg_id:
            return Clients.json_answer(True, "Bad name format, or telegram id", 400)

        try:
            ClientModel(client_name=name, client_telegram_user_id=tg_id).save()
        except Exception as e:
            return Clients.json_answer(True, "unknown error: {}".format(e), 400)
        return Clients.json_answer(True, "create successful", 200)

    @staticmethod
    @api_view(['PUT'])
    def change_client(request, client_id: int, field: str, value: str):
        try:
            obj = ClientModel.objects.get(client_id=f"{client_id}")

            if field not in Clients._clients_fields:
                return Clients.json_answer(False, "Bad field names, or telegram id user", 404)
            if field == "client_telegram_user_id":
                if Clients.validate_telegram_id(value) in [False, "null"]:
                    return Clients.json_answer(False, "Bad telegram id, pls check it", 404)
            obj[field] = str(value)
            obj.save([field])
            return Clients.show_one(request, obj["id"])
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(True, "unknown error: {}".format(e), 400)

    @staticmethod
    def bad_request_check_documents(request):
        return Clients.json_answer(False, "bad request, pls check documentation with format", 404)

    @staticmethod
    def validate_telegram_id(tg_id: str):
        if not tg_id == "None" and not tg_id == "0":
            return False if not tg_id.isdigit() or len(tg_id) != 9 else tg_id
        else:
            return "null"
