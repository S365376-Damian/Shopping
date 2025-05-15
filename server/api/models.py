from mongoengine import Document, ListField, StringField, DateTimeField, BooleanField, IntField

################################################################
#No.1
LEVELS = (
    'Root',
    'Admin', #quản trị viên
    'Staff', #nhân viên
    'Customer', #khách hàng
    'Admin_Shop' #chủ shop
)

class User(Document):  
    phone               =  StringField()
    email               =  StringField()
    fullname            =  StringField()
    address             =  StringField()
    nameLogin           =  StringField()
    gender              =  StringField()
    password            =  StringField()
    level               =  StringField(choices=LEVELS) #, choices=LEVELS
    rank                =  StringField()
    coin                =  IntField()
    timeRegister        =  DateTimeField()
    timeUpdate          =  DateTimeField()
    viewAble            =  BooleanField(default = True)
    codeOTP             =  StringField()
    shop_pk             =  StringField()
    isDeleted           =  BooleanField(default = False)
  
################################################################

class Shop(Document):  
    phone               =  StringField()
    email               =  StringField()
    name                =  StringField()
    user_pk             =  StringField()
    user_name           =  StringField()
    address             =  StringField()
    timeRegister        =  DateTimeField()
    timeUpdate          =  DateTimeField()
    isDeleted           =  BooleanField(default = False)
  
################################################################
GENDERS = (
    'Male',
    'Female',
    'undefined',
)

################################################################

class LoginSession(Document):
    token               =  StringField()
    phone               =  StringField()
    level               =  StringField()
    fullname            =  StringField()
    loginTime           =  DateTimeField()
    logoutTime          =  DateTimeField()
    platform            =  StringField()
    purpose             =  StringField()
    validTo             =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Product(Document):
    shop_pk            =  StringField()   
    shop_name          =  StringField()           
    product_code       =  StringField()
    product_name       =  StringField()
    product_nameSlug   =  StringField()
    price              =  IntField()
    size               =  StringField()
    group              =  StringField()
    type               =  StringField()
    material           =  StringField() ##chất liệu
    color              =  StringField() ##màu sắc
    describe           =  StringField() ##mô tả
    image              =  StringField()
    imageDir           =  StringField()
    imagePaths         =  ListField(StringField())
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    check              =  BooleanField(default=False)
    isDeleted          =  BooleanField(default=False)

################################################################
    
class Type(Document):
    name               =  StringField()
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################
    
class Material(Document):
    name               =  StringField()
    nameSlug           =  StringField()
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Blog(Document):
    title              =  StringField()
    slug               =  StringField()
    content            =  StringField()
    image              =  StringField()
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################
    
class Pet(Document):
    name               =  StringField()
    breed              =  StringField()
    color              =  StringField()
    age                =  IntField()
    gender             =  StringField()
    owner              =  StringField()
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    dateStart          =  DateTimeField()
    dateEnd            =  DateTimeField()
    image              =  StringField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Activity(Document):
    email               =  StringField()
    activity            =  StringField()
    value               =  StringField()
    timeCreate          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Voucher(Document):
    name                =  StringField()
    nameSlug            =  StringField()
    code                =  StringField()
    type                =  StringField()
    value               =  IntField(default=0)
    timeCreate          =  DateTimeField()
    timeUpdate          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Order(Document):
    shop_pk            =  StringField()   
    shop_name          =  StringField()     
    product_pk         =  StringField()
    product_name       =  StringField() 
    price              =  IntField(default=0)
    user_pk            =  StringField()
    user_name          =  StringField()
    user_phone         =  StringField()
    address            =  StringField()
    note               =  StringField()
    voucher_pk         =  StringField()
    voucher_name       =  StringField() 
    status             =  StringField() 
    size               =  StringField()
    color              =  StringField() 
    quantity           =  IntField()
    timeCreate         =  DateTimeField()
    timeUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Evaluate(Document):
    product_pk         =  StringField()
    product_name       =  StringField() 
    user_pk            =  StringField()
    user_name          =  StringField()
    user_phone         =  StringField()
    content            =  StringField()
    point              =  IntField()
    timeCreate         =  DateTimeField()
    timeUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Comment(Document):
    user_pk            =  StringField()
    user_name          =  StringField()
    user_phone         =  StringField()
    content            =  StringField()
    timeCreate         =  DateTimeField()
    timeUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Message(Document):
    sender_pk          =  StringField()
    sender_name        =  StringField()
    receiver_pk        =  StringField()
    receiver_name      =  StringField()
    content            =  StringField()
    timeCreate         =  DateTimeField()
    timeUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)
   