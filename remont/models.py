
from django.db import models


class Address(models.Model):
    address = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    address_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    town_village = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class AddressType(models.Model):
    address_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address_type'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup)
#     permission = models.ForeignKey('AuthPermission')
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = ['group_id', 'permission_id']


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType')
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = ['content_type_id', 'codename']


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'



#
# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser)
#     permission = models.ForeignKey(AuthPermission)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user_id', 'permission_id'),)
#

class Contact(models.Model):
    contact = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    subject_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    contact_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    value_text = models.TextField(blank=True, null=True)
    orderby = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContactType(models.Model):
    contact_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_type'


class Customer(models.Model):
    customer = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    subject_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Device(models.Model):
    device = models.AutoField(primary_key=True)
    device_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceType(models.Model):
    device_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    super_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    level = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    employee = models.AutoField(primary_key=True)
    person_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    enterprise_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    struct_unit_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class EmployeeRole(models.Model):
    employee_role = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    employee_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    employee_role_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_role'


class EmployeeRoleType(models.Model):
    employee_role_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_role_type'


class EntPerRelationType(models.Model):
    ent_per_relation_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_per_relation_type'


class Enterprise(models.Model):
    enterprise = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    name = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    updated_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise'


class EnterprisePersonRelation(models.Model):
    enterprise_person_relation = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    person_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    enterprise_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    ent_per_relation_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_person_relation'


class Invoice(models.Model):
    invoice = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    invoice_status_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_order_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    customer_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    price_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    receiver_name = models.TextField(blank=True, null=True)
    reference_number = models.TextField(blank=True, null=True)
    receiver_accounts = models.TextField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceRow(models.Model):
    invoice_row = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    invoice_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_action_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_part_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    action_part_description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    price_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    unit_type = models.CharField(max_length=200, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    invoice_row_type = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_row'


class InvoiceStatusType(models.Model):
    invoice_status_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_status_type'


class Person(models.Model):
    person = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    identity_code = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    updated_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class ServiceAction(models.Model):
    service_action = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    service_action_status_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_device_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_order_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    price_updated = models.DateTimeField(blank=True, null=True)
    action_description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_action'


class ServiceActionStatusType(models.Model):
    service_action_status_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_action_status_type'


class ServiceDevice(models.Model):
    service_device = models.AutoField(primary_key=True)
    service_device_status_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    device_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_order_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    to_store = models.DateTimeField(blank=True, null=True)
    from_store = models.DateTimeField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    status_changed = models.DateTimeField(blank=True, null=True)
    store_status = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_device'


class ServiceDeviceStatusType(models.Model):
    service_device_status_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_device_status_type'


class ServiceNote(models.Model):
    service_note = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    customer_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    employee_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_order_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_device_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    note_author_type = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_note'


class ServiceOrder(models.Model):
    service_order = models.AutoField(primary_key=True)
    so_status_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_request_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    updated_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    status_changed = models.DateTimeField(auto_now_add=True)
    status_changed_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    price_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_order'


class ServicePart(models.Model):
    service_part = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    service_order_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    service_device_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    part_name = models.TextField(blank=True, null=True)
    serial_no = models.TextField(blank=True, null=True)
    part_count = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    part_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_part'


class ServiceRequest(models.Model):
    service_request = models.AutoField(primary_key=True)
    customer_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    service_desc_by_customer = models.TextField(blank=True, null=True)
    service_desc_by_employee = models.TextField(blank=True, null=True)
    service_request_status_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_request'


class ServiceRequestStatusType(models.Model):
    service_request_status_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_request_status_type'


class ServiceType(models.Model):
    service_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    service_unit_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    type_name = models.CharField(max_length=200, blank=True, null=True)
    service_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_type'


class ServiceUnitType(models.Model):
    service_unit_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_unit_type'


class SoStatusType(models.Model):
    so_status_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'so_status_type'


class StructUnit(models.Model):
    struct_unit = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    enterprise_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    upper_unit_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    level = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'struct_unit'


class SubjectAttribute(models.Model):
    subject_attribute = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    subject_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_attribute_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    orderby = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    value_text = models.TextField(blank=True, null=True)
    value_number = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    data_type = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_attribute'


class SubjectAttributeType(models.Model):
    subject_attribute_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    type_name = models.CharField(max_length=200, blank=True, null=True)
    data_type = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    orderby = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    required = models.CharField(max_length=1, blank=True, null=True)
    multiple_attributes = models.CharField(max_length=1, blank=True, null=True)
    created_by_default = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_attribute_type'


class SubjectType(models.Model):
    subject_type = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    type_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_type'


class UserAccount(models.Model):
    user_account = models.AutoField(primary_key=True)
    subject_type_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    subject_fk = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    passw = models.CharField(max_length=300, blank=True, null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    created_by = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    password_never_expires = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_account'
