from django.http import request
from django.shortcuts import render, render_to_response, redirect
# Create your views here.
from django.template import RequestContext
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout


from remont.models import *



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



class LoginFormView(View):
    def post(self,request):
        m = UserAccount.objects.get(username=request.POST['username'])
        if m.passw == request.POST.get('password', False):
            request.session['member'] = m.username
            if m.subject_type_fk == 4:
                return HttpResponseRedirect("/invoice")
            else:
                return HttpResponseRedirect("/")

#            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Your username and password didn't match.")

    def get(self, request):
        return render(request, 'login.html', {})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")



class Add_new_device(View):
    def post(self,request):
            name = request.POST.get('nimi')
            model = request.POST.get('mudel')
            description = request.POST.get('kirjeldus')
            manufacturer = request.POST.get('tootja')
            serial_num = request.POST.get('seriaalnumber')
            device_type = request.POST.get('seadmetuup')
            #get device_type.id

            device_type_query=DeviceType.objects.values('device_type').filter(type_name=device_type)
            device_type_fk=int(device_type_query[0]['device_type'])
            #lisamine tabelisse Device
            p = Device(name=name, description=description, reg_no=serial_num, model=model, manufacturer=manufacturer,device_type_fk=device_type_fk)
            p.save()
            #lisamine tabelisse Service_device
            #status_type = ServiceDeviceStatusType.objects.

            a = ServiceDevice(service_device_status_type_fk=1, device_fk=p.device, service_order_fk=2, service_description=description )
            a.save()
            return redirect('/')
    def get(self, request):
            device_type_query = DeviceType.objects.values('type_name')
            return render(request, 'lisa_uus_seade.html', {'device_type':device_type_query})




def list(request):
    a=Device.objects.all().values()
    return render(request, 'list.html', {'a':a})






class Invoice(View):
    def post(self, request):
        return redirect('/')
    def get(self, request):
        return render(request, 'invoice.html', {})


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

        if (device_type != "" and device_client == ""):

            try:
                find_entries = Device.objects.filter(device_type_fk=device_type)
            except ObjectDoesNotExist:
                find_entries = None

        return render(request, 'seadme_otsing.html', {'find_entries_byname':find_entries_byname,'all_device_types':all_device_types, 'find_entries': find_entries})
    else:
        return render(request, 'seadme_otsing.html', {'all_device_types':all_device_types, 'find_entries': find_entries})