import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import ClientModel, BidModel, StaffModel
from .serializers import BidModelSerializer, ClientModelSerializer, StaffModelSerializer
from .tg_hook import telegram_notification

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required


# def bids_list(request):
#     name = ["Oleg", "Vasya", "Petya"]
#     return render(request, 'API/index.html', context={'names': name})
#
#

def documentation(request):
    return render(request, 'API/documentation.html')


class Bids(LoginRequiredMixin, APIView):
    raise_exception = True

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_date(request, date: datetime):
        try:
            serializer = BidModelSerializer(BidModel.objects.filter(date_create=date), many=True)
            return Response(serializer.data)
        except BidModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error, probably wrong format: {}".format(e), 400)

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_dates(request, date: datetime, up_date: datetime):
        try:
            bids = BidModel.objects.filter(date_create__gte=date, date_create__lte=up_date)
            serializer = BidModelSerializer(bids, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_all(request):
        try:
            serializer = BidModelSerializer(BidModel.objects.all(), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @login_required(redirect_field_name='login_url')
    def create_bid(request, type_bid: int, client_id: int, body: str, title_bid: str, notifications: int):
        try:
            creator = ClientModel.objects.get(client_id=int(client_id))
            bid = BidModel(type_bid=int(type_bid), text_bid=body, title=title_bid,
                           notifications=bool(notifications))
            bid.save()
            bid.creator.set([creator])
            bid.save()
            return Clients.json_answer(True, "Bid create successful", 200)
        except Exception as e:
            return Clients.json_answer(False, "unknown error, probably wrong format: {}".format(e), 400)

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_one(request, bid: int):
        try:
            serializer = BidModelSerializer(BidModel.objects.get(id=bid), many=False)
            return Response(serializer.data)
        except BidModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error, probably wrong format: {}".format(e), 400)

    @staticmethod
    @login_required(redirect_field_name='login_url')
    def show_category(request, category: str):
        try:
            # take index for database
            idx = ["fix", "consultation", "service", "open", "in work", "finished"].index(category)
            if idx < 3:
                bids = BidModel.objects.filter(type_bid=idx + 1)
            else:
                bids = BidModel.objects.filter(status=idx - 2)
            qs_json = BidModelSerializer(bids)
            return Response(qs_json.data)
        except ValueError:
            return Clients.json_answer(False, "Bad sort type check docs", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    # TODO adding notifications if bid status changed or if staff be do work
    @staticmethod
    @api_view(['POST', 'GET'])
    @login_required(redirect_field_name='login_url')
    def change_one(request, bid: int, field: str, value: str):
        try:
            obj = BidModel.objects.get(id=bid)
            if field == "creator":
                creator_id = ClientModel.objects.get(client_id=int(value))
                obj.creator.set([creator_id])
            elif field == "staff_id":
                staff_id = StaffModel.objects.get(id=int(value))
                obj.staff_id.set([staff_id])
            elif field != "id":
                # anti pattern for exception if bad field
                obj.__dict__[field] = value
            else:
                raise ValueError("Cant change id number")
            obj.save()

            if field == "status" or field == "staff_id":
                if obj.notifications and obj.creator.all()[0].client_telegram_user_id not in [0, None]:
                    telegram_notification.send_message(
                        "Your bid has `changed` status" if field == "status"
                        else "An executor has been assigned to your bid",
                        obj.creator.all()[0].client_telegram_user_id)

            return Response(status=200)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    def post(self, request):
        try:
            bid = BidModelSerializer(data=request.data)
            if bid.is_valid():
                bid.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except Exception as e:
            return Clients.json_answer(True, "unknown error: {}".format(e), 400)


class Clients(LoginRequiredMixin, APIView):
    raise_exception = True

    _clients_fields = ["client_name", "client_telegram_user_id"]

    @staticmethod
    def json_answer(success: bool, description: str, status: int):
        return HttpResponse(json.dumps({"success": success, "description": description}), status=status,
                            content_type='application/json')

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_all(request):
        try:
            serializer = ClientModelSerializer(ClientModel.objects.all(), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET'])
    @login_required(redirect_field_name='login_url')
    def show_one(request, client_id: int):
        try:
            serializer = ClientModelSerializer(ClientModel.objects.get(client_id=client_id), many=False)
            return Response(serializer.data)
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['DELETE'])
    @login_required(redirect_field_name='login_url')
    def remove_client(request, client_id: int):
        try:
            client = ClientModel.objects.get(creator=f"{client_id}")
            client.delete()
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)
        else:
            return Clients.json_answer(True, "delete successful", 200)

    @staticmethod
    @api_view(['POST', 'GET'])
    @login_required(redirect_field_name='login_url')
    def create_client(request, name: str, telegram: str):
        tg_id = Clients.validate_telegram_id(telegram)
        if name.isspace() or not tg_id:
            return Clients.json_answer(True, "Bad name format, or telegram id", 400)

        try:
            ClientModel(client_name=name, client_telegram_user_id=tg_id).save()
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)
        return Clients.json_answer(True, "create successful", 200)

    def post(self, request):
        try:
            client = ClientModelSerializer(data=request.data)
            if client.is_valid():
                client.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except Exception as e:
            return Clients.json_answer(True, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['PUT'])
    @login_required(redirect_field_name='login_url')
    def change_client(request, client_id: int, field: str, value: str):
        try:
            obj = ClientModel.objects.get(creator=f"{client_id}")
            if field == "client_id" or field == "client_date_registration":
                raise ValueError("Cant change main fields")
            if field == "client_telegram_user_id":
                if Clients.validate_telegram_id(value) in [False, "null"]:
                    return Clients.json_answer(False, "Bad telegram id, pls check it", 404)
            # anti pattern for exception
            obj.__dict__[field] = value
            obj.save([field])
            return Response(status=200)
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


class Staff(LoginRequiredMixin, APIView):
    raise_exception = True

    @staticmethod
    @api_view(['GET', 'POST'])
    @login_required(redirect_field_name='login_url')
    def change_one(request, staff_id: int, field: str, value: str):
        try:
            obj = StaffModel.objects.get(id=f"{staff_id}")
            obj.__dict__[field] = value
            obj.save([field])
            return Response(status=200)
        except ClientModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET', 'POST'])
    @login_required(redirect_field_name='login_url')
    def show_all(request):
        try:
            serializer = StaffModelSerializer(StaffModel.objects.all(), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    def post(self, request):
        try:
            staff = StaffModelSerializer(data=request.data)
            if staff.is_valid():
                staff.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except Exception as e:
            return Clients.json_answer(True, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET', 'POST'])
    @login_required(redirect_field_name='login_url')
    def show_one(request, staff_id: int):
        try:
            serializer = StaffModelSerializer(StaffModel.objects.get(id=staff_id), many=False)
            return Response(serializer.data)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET', 'POST'])
    @login_required(redirect_field_name='login_url')
    def create_one(request, slug: str):
        try:
            StaffModel.objects.create(name=slug)
            return Clients.json_answer(True, "element successful create", 200)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)

    @staticmethod
    @api_view(['GET', 'POST'])
    @login_required(redirect_field_name='login_url')
    def delete_one(request, staff_id: int):
        try:
            staff = StaffModel.objects.get(id=staff_id)
            staff.delete()
        except StaffModel.DoesNotExist:
            return Clients.json_answer(False, "element not found", 404)
        except Exception as e:
            return Clients.json_answer(False, "unknown error: {}".format(e), 400)
        else:
            return Response(status=200)
