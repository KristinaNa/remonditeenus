from django.http import request
from django.shortcuts import render, render_to_response, redirect
# Create your views here.
from django.template import RequestContext
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
import hashlib
from remont.forms import *
from remont.models import *
from django.forms import model_to_dict
import logging
import decimal
import json as simplejson
from django.contrib import messages
from remont.model_raw import MathOperations

log = logging.getLogger('MYAPP')

# autor: Kristina Nassonenko
class RegisterFormView(View):
    def post(self, request):
            fname = request.POST.get('username')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            if (password==password1):
                a=Person(first_name=fname,last_name=lname,identity_code=password, birth_date=birth)
                a.save()
                return HttpResponseRedirect("/")

    def get(self,request):
        return render(request, 'register.html', {})

# autor: Kristina Nassonenko
class LoginFormView(View):
    log.info("User logged in")
    def post(self,request):
        m = UserAccount.objects.filter(username=request.POST['username']).values()
        if(len(m))<1:
            return HttpResponse("Sellist kasutajat ei ole")
        else:
            password=request.POST.get('password', False)
            hash_object = hashlib.md5(password)
            password2=hash_object.hexdigest()
            if m[0]['passw'] == password2:
                request.session['member'] = m[0]['username']
                if m[0]['subject_type_fk'] == 4:
                    return HttpResponseRedirect("/order")
                else:
                    return HttpResponseRedirect("/")
    #            return HttpResponse("You're logged in.")
            else:
                return HttpResponse("Your username and password didn't match.")
    def get(self, request):
        return render(request, 'login.html', {})

# autor: Kristina Nassonenko
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")


# autor: Kristina Nassonenko
class Add_new_device(View):
    log.info("New device added")
    def post(self,request):
            device_type_query = DeviceType.objects.values('type_name')
            form = AddForm(request.POST)
            errors=[]
            name = request.POST.get('nimi').replace(' ', '')
            model = request.POST.get('mudel').replace(' ', '')
            description = request.POST.get('kirjeldus')
            manufacturer = request.POST.get('tootja')
            serial_num = request.POST.get('seriaalnumber')
            device_type = request.POST.get('seadmetuup')

            current_user = request.session.get('member')
            user_id = Person.objects.values('person').filter(first_name=current_user)
            id = int(user_id[0]['person'])

            if form.is_valid():
                device_type_query=DeviceType.objects.values('device_type').filter(type_name=device_type)
                device_type_fk=int(device_type_query[0]['device_type'])
                #lisamine tabelisse Device
                p = Device(name=name, description=description, reg_no=serial_num, model=model, manufacturer=manufacturer,device_type_fk=device_type_fk)
                p.save()
                #lisamine tabelisse Service_device
                #status_type = ServiceDeviceStatusType.objects.
                a = ServiceDevice(service_device_status_type_fk=1, device_fk=p.device, service_description=description )
                a.save()

                log.info("Added new service_devise")
            else:
                message="Koik valjad peavad olema sisestatud"
                return render(request, 'lisa_uus_seade.html', {'form':form,'device_type':device_type_query})
            return redirect('/')
    def get(self, request):
            form = AddForm()
            device_type_query = DeviceType.objects.values('type_name')
            return render(request, 'lisa_uus_seade.html', {'device_type':device_type_query,'form':form})


def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


# autor: Kristina Nassonenko
class Service_order(View):
    def get(self, request):
        a=Person.objects.values('first_name', 'last_name', 'person')
        b=Device.objects.values()
        return render(request, 'service_order.html', {'person':a, 'device':b})

    def post(self, request):
        select=Person.objects.values('first_name', 'last_name', 'person')
        current_user = request.session.get('member')
        klient=request.POST.get('klijendi_kirjeldus')
        tootaja=request.POST.get('vastuvotja_kirjeldus')
        customer_fk = request.POST.get('customer')

        device=request.POST.get('device')

        if customer_fk=="0":
            return HttpResponse("Klient peab olema valitud")
        else:
            a = Person.objects.values('person').filter(first_name=current_user)
            employee = int(a[0]['person'])

            service_request_query = ServiceRequest(service_desc_by_customer=klient, service_desc_by_employee=tootaja, service_request_status_type_fk=3, customer_fk=customer_fk,created_by=employee )
            service_request_query.save()
            log.info("Added new service_request")
            service_request_fk=service_request_query.service_request
            #print(service_request_fk)
            query=ServiceOrder(so_status_type_fk=1,created_by=employee, service_request_fk=service_request_fk )
            query.save()

            d = ServiceDevice.objects.filter(device_fk=device).update(service_order_fk=query.service_order)


            log.info("New service order")
            messages.success(request, 'Service order created.')


            return render(request, 'service_order.html', {'user':current_user, 'person':select})

# autor: Kristina Nassonenko
def lisa_service_device(request):
    id=request.GET.get('id')

   # print(id)
    device=ServiceDevice(service_device_status_type_fk=1, device_fk=id, service_order_fk=2)
    device.save()
    return  redirect('/')


# autor: Kristina Nassonenko
def list(request):
    log.info("View device list")
    a=Device.objects.all().values()
    return render(request, 'list.html', {'a':a})




class Order(View):
    def post(self, request):
        list=[]
        request_list=[]
        id=[31]
        service_device=ServiceDevice.objects.values('service_order_fk').filter(device_fk__in=id)
        for i in service_device:
            list.append(int(i['service_order_fk']))
        print("-=================================")
        print(list)
        print("-=================================")

        service_order=ServiceOrder.objects.values('service_request_fk').filter(service_order__in=list)
        for a in service_order:
            request_list.append(int(a['service_request_fk']))
        print(request_list)

        service_request=ServiceRequest.objects.values('service_desc_by_customer').filter(service_request__in=request_list)
        print(service_request[0]['service_desc_by_customer'])

        return render(request, 'order.html',{'service_request':service_request})


    def get(self, request):
        list=[]
        list2=[]
        list3=[]

        current_user = request.session.get('member')
        user_id = Person.objects.values('person').filter(first_name=current_user)
        id = int(user_id[0]['person'])

        a = ServiceRequest.objects.filter(customer_fk=id).values()
        for i in a:
            list.append(int(i['service_request']))
        #print(list)

        query=ServiceOrder.objects.values().filter(service_request_fk__in=list)
        for k in query:
             list2.append(int(k['service_order']))
        #print(list2)
        query2=ServiceDevice.objects.values('device_fk').filter(service_order_fk__in=list2)
        for p in query2:
            list3.append(int(p['device_fk']))
        #
        # print(list3)

        device_query=Device.objects.values().filter(device__in=list3)

        return render(request, 'order.html',{'a':a, 'query':query, 'device_query':device_query})




# autor: Kristina Nassonenko ja Arsenti Morozov
def server_list(request):
    find_entries= []
    find_entries_byname=[]
    all_device_types = DeviceType.objects.all().values().order_by("device_type")

    if request.method == "POST":
        device_name = request.POST.get('name')
        device_model = request.POST.get('model')
        device_reg_no = request.POST.get('reg_no')
        device_type = request.POST.get('seadme_tyyp')
        device_client = request.POST.get('client')


        if (device_client != "" and device_type !=""):
            try:
                params = ("'" + device_client + "'", "'" + device_client + "'")
               # print(params)
                find_entries_byname = Device.objects.raw(user_devices,params)
               # print(find_entries_byname)
            except ObjectDoesNotExist:
                find_entries_byname = None


        if(device_name != ""):
            try:
                find_entries = Device.objects.filter(name__icontains=device_name)
            except ObjectDoesNotExist:
                find_entries = None
        if (device_model != ""):
            try:
                find_entries = Device.objects.filter(model__icontains=device_model)
            except ObjectDoesNotExist:
                find_entries = None
        if (device_reg_no != ""):
            try:
                find_entries = Device.objects.filter(reg_no__icontains=device_reg_no)
            except ObjectDoesNotExist:
                find_entries = None

        # if (device_type != "" and device_client == ""):
        #
        #     try:
        #         find_entries = Device.objects.filter(device_type_fk=device_type)
        #     except ObjectDoesNotExist:
        #         find_entries = None

        return render(request, 'seadme_otsing.html', {'find_entries_byname':find_entries_byname,'all_device_types':all_device_types, 'find_entries': find_entries})
    else:
        return render(request, 'seadme_otsing.html', {'all_device_types':all_device_types, 'find_entries': find_entries })



def get_json(request, device_id):
    obj = Device.objects.get(device=device_id)#.only('description','reg_no','model','manufacturer','name')
   #  obj=Device.objects.values().filter(device=device_id)
   #  a=list(obj)
    dict_obj = model_to_dict( obj )

    #data = json.dumps(list(radio_object), cls=DjangoJSONEncoder)
    #return render(request, 'edit_radio.html', {'data': data})
    #return HttpResponse(serializers.serialize("json", radio_object))

    # data = serializers.serialize('json', a)
    # return HttpResponse(data, mimetype='application/javascript')
    data = simplejson.dumps(dict_obj, default=json_encode_decimal)
    return HttpResponse(data, content_type='application/json')

def get_note_json(request, id):
        list=[]
        request_list=[]
        service_device=ServiceDevice.objects.values('service_order_fk').filter(device_fk=id)
        for i in service_device:
            list.append(int(i['service_order_fk']))
        service_order=ServiceOrder.objects.values('service_request_fk').filter(service_order__in=list)
        for a in service_order:
            request_list.append(int(a['service_request_fk']))
       # service_request=ServiceRequest.objects.values('service_desc_by_customer').filter(service_request__in=request_list)
        service_request=ServiceRequest.objects.get(service_request__in=request_list)
        dict_obj = model_to_dict( service_request )
        data = simplejson.dumps(dict_obj, default=json_encode_decimal)
        return HttpResponse(data, content_type='application/json')



        # print(service_request[0]['service_desc_by_customer'])
        # return render(request, 'order.html',{'service_request':service_request})

def save_note(request, id):
    desc=request.GET.get("message")
    d = ServiceRequest.objects.filter(service_request=id).update(service_desc_by_customer=desc)

    return HttpResponse(status=201)


# autor: Arsenti Morozov
x = MathOperations()
devices = x.all_devices()
devices_service_actions = x.devices_in_raw()
devices_service_parts = x.devices_parts()
devices_find_byorder = x.find_rows_byorder()
devices_part_find_byorder = x.find_parts_byorder()

def service_action(request):
    all_devices = []
    devices_in_raw = []
    devices_parts = []
    total_price_work = 0
    total_price_part = 0
    if 'submit_user' in request.POST:
        try:
            user_name = request.POST.get('user')
            if (request.POST.get('selected_device') != ""):
                device_user= Person.objects.filter(last_name=user_name).values('person')
                device_person = int(device_user[0]['person'])
                print(device_person)
                print("00000000000000000000")
                if not device_user:
                    return render(request, 'service_action.html',
                                      {'devices_parts': devices_parts,
                                       'devices_in_raw': devices_in_raw, 'all_devices': all_devices})

                # params = (((x.person) for x in device_user))
                # print(params)
                all_devices = Device.objects.raw("select distinct device.device,device.name,device.model,device.reg_no from device,service_device,service_order,invoice,customer,person,enterprise where device.device=service_device.device_fk AND service_device.service_order_fk=service_order.service_order And invoice.service_order_fk=service_order.service_order And customer.customer=invoice.customer_fk and person.person = customer.subject_fk and person.person = %s",[device_person])
        except ObjectDoesNotExist:
            all_devices = []
        except RuntimeError:
            all_devices = []
    if 'save_data' in request.POST:
        print(request.POST.get('price'))
    if 'submit_device' in request.POST:
        try:
            service_type = ServiceType.objects.all()
            selected_device = request.POST.get('selected_device')

            selected_device_name = Device.objects.filter(device=selected_device)

            devices_in_raw = Device.objects.raw("select distinct service_unit_type.type_name as op, service_action.action_description, service_action.service_action,service_action_status_type.type_name, service_type.type_name, device.device , service_action.service_order_fk , service_action.service_amount , service_action.price from service_unit_type,device,service_action,service_action_status_type,service_type,service_device,service_order where service_action.service_action_status_type_fk=service_action_status_type.service_action_status_type and service_action.service_type_fk=service_type.service_type and service_unit_type.service_unit_type=service_type.service_unit_type_fk and device.device=service_device.device_fk and service_device.service_device=service_action.service_device_fk and device.device=%s",selected_device)
            devices_parts = Device.objects.raw("select distinct service_part.service_order_fk, service_part.service_part,service_part.part_name, service_part.part_count, service_part.part_price, device.device from service_part,service_device,device where service_part.service_device_fk = service_device.service_device and service_device.device_fk=device.device and device.device=%s",selected_device)

            for device_for_price_work in devices_in_raw:
                total_price_work =device_for_price_work.price*device_for_price_work.service_amount+total_price_work
            for device_for_price_part in devices_parts:
                total_price_part = device_for_price_part.part_price*device_for_price_part.part_count+total_price_part
            total_price = total_price_work+total_price_part
        except ObjectDoesNotExist:
            devices_in_raw = None
        return render(request, 'service_action.html', {'service_type':service_type,'total_price':total_price,'selected_device_name':selected_device_name,'devices_parts': devices_parts, 'devices_in_raw': devices_in_raw,'all_devices': all_devices})
    else:
        return render(request, 'service_action.html', {'devices_parts': devices_parts, 'devices_in_raw': devices_in_raw,'all_devices': all_devices})



def service_device(request):
    if 'submit_oder' in request.POST:
        selected_order = request.POST.get('submit_oder')
        devices_byorder=Device.objects.raw(devices_find_byorder,selected_order)
        selected_order_for_price =ServiceOrder.objects.filter(service_order=selected_order)
        parts_byorder=Device.objects.raw(devices_part_find_byorder,selected_order)
        print(parts_byorder)
        return render(request,'service_device.html',{'selected_order_for_price':selected_order_for_price,'devices_byorder':devices_byorder,'parts_byorder':parts_byorder})
    else:
        return render(request, 'service_device.html', {})
































