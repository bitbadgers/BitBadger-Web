from django.db import models

class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key= True, auto_created= True)
    user_fName = models.CharField(max_length= 50, null= False)
    user_sName = models.CharField(max_length= 50, null= False)
    user_other_Name = models.CharField(max_length= 50, null= True)
    user_pWord = models.CharField(max_length = 200, null = False)
    user_email = models.EmailField(unique = True, null = False)
    user_name = models.CharField(max_length= 30, null = False, unique = True)
    user_image = models.ImageField(upload_to= 'static/profpics')


