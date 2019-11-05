from django.db import models


class Student(models.Model):
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    batch = models.CharField(max_length=4, null=True)
    section = models.CharField(max_length=4, null=True)
    image = models.FilePathField(path="/img")

    def __str__(self):
        lv_studentdata = "id: {}, Name: {} {}, email: {}, image: {}".format(self.id, self.fname, self.lname, self.email, self.image)
        return lv_studentdata


class Faculty(models.Model):
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    admin = models.CharField(max_length=1, default=0)
    image = models.FilePathField(path="/img")

    def __str__(self):
        lv_facdata = "id: {}, Name: {} {}, email: {}, admin: {}, image: {}".format(self.id, self.fname, self.lname, self.email, self.admin, self.image)
        return lv_facdata


class Course(models.Model):
    co_name = models.CharField(max_length=100, null=False)


class Subject(models.Model):
    sub_name = models.CharField(max_length=100, null=False)
    co_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        lv_subData = "id: {}, Name: {}, Course: {}".format(self.id, self.sub_name, self.co_name)
        return lv_subData


class Test(models.Model):
    test_name = models.CharField(max_length=100, null=False)
    sub_name = models.CharField(max_length=100, null=False)
    co_name = models.CharField(max_length=100, null=False)
    qid_list = models.CharField(max_length=20000, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)


class Question(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=10000, null=False)
    tid_list = models.CharField(max_length=20000, null=True)
    option1 = models.CharField(max_length=1000, null=True)
    option2 = models.CharField(max_length=1000, null=True)
    option3 = models.CharField(max_length=1000, null=True)
    option4 = models.CharField(max_length=1000, null=True)
    option5 = models.CharField(max_length=1000, null=True)
    correct = models.CharField(max_length=1, null=True)
