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
import json
import logging


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
            name = request.POST.get('nimi')
            model = request.POST.get('mudel')
            description = request.POST.get('kirjeldus')
            manufacturer = request.POST.get('tootja')
            serial_num = request.POST.get('seriaalnumber')
            device_type = request.POST.get('seadmetuup')
            #get device_type.id
            # if(len(name)<2  or len(model)<2 or len(manufacturer)<2 or len(description)<2 or len(serial_num)<2 or len(device_type)<2):
            #     return HttpResponse("ei voi olla tuhi string")
            if form.is_valid():
                device_type_query=DeviceType.objects.values('device_type').filter(type_name=device_type)
                device_type_fk=int(device_type_query[0]['device_type'])
                #lisamine tabelisse Device
                p = Device(name=name, description=description, reg_no=serial_num, model=model, manufacturer=manufacturer,device_type_fk=device_type_fk)
                p.save()
                #lisamine tabelisse Service_device
                #status_type = ServiceDeviceStatusType.objects.
                a = ServiceDevice(service_device_status_type_fk=1, device_fk=p.device, service_order_fk=9, service_description=description )
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

# autor: Kristina Nassonenko
class Service_order(View):
    def get(self, request):
        a=Person.objects.values('first_name', 'last_name', 'person')
        return render(request, 'service_order.html', {'person':a})

    def post(self, request):
        select=Person.objects.values('first_name', 'last_name', 'person')
        current_user = request.session.get('member')
        klient=request.POST.get('klijendi_kirjeldus')
        tootaja=request.POST.get('vastuvotja_kirjeldus')
        customer_fk = request.POST.get('customer')

        if customer_fk=="0":
            return HttpResponse("Klient peab olema valitud")
        else:
            a = Person.objects.values('person').filter(first_name=current_user)
            employee = int(a[0]['person'])

            service_request_query = ServiceRequest(service_desc_by_customer=klient, service_desc_by_employee=tootaja, service_request_status_type_fk=3, customer_fk=customer_fk,created_by=employee )
            service_request_query.save()
            log.info("Added new service_request")
            service_request_fk=service_request_query.service_request
            print(service_request_fk)
            query=ServiceOrder(so_status_type_fk=1,created_by=employee, service_request_fk=service_request_fk )
            query.save()
            log.info("New service order")

            return render(request, 'service_order.html', {'user':current_user, 'person':select})

# autor: Kristina Nassonenko
def lisa_service_device(request):
    id=request.GET.get('id')

    print(id)
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
        return redirect('/')
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
        print(list3)

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
                print(params)
                find_entries_byname = Device.objects.raw(
                    "select distinct device.device,device.name,device.model,device.reg_no from device,"+
                    "service_device,service_order,invoice,customer,person,enterprise where "+
                    "device.device=service_device.device_fk AND service_device.service_order_fk=service_order.service_order "+
                    "And invoice.service_order_fk=service_order.service_order And customer.customer=invoice.customer_fk and"+
                    " person.person = customer.subject_fk and person.first_name = %s or enterprise.name = %s",
                    params)
                print(find_entries_byname)
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
    obj = Device.objects.get(device=device_id)
   #  obj=Device.objects.values().filter(device=device_id)
   #  a=list(obj)
    dict_obj = model_to_dict( obj )

    #data = json.dumps(list(radio_object), cls=DjangoJSONEncoder)
    #return render(request, 'edit_radio.html', {'data': data})
    #return HttpResponse(serializers.serialize("json", radio_object))

    # data = serializers.serialize('json', a)
    # return HttpResponse(data, mimetype='application/javascript')
    data = json.dumps(dict_obj)
    return HttpResponse(data, content_type='application/json')
