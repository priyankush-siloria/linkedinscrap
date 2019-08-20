from django.db import models



DAYS = (
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednessday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saterday')
)

RATE = (
    ('W', 'Weekly'),
    # ('B', 'Biweekly'),
    ('M', 'Monthly'),
)
DATASTATUS = (
    ('P', 'Pending'),
    ('A', 'Approve'),
    ('R', 'Reject'),
)

class LinkedIn(models.Model):
    email = models.EmailField(max_length=255, blank=False, null=True)
    password = models.CharField(max_length=100,  blank=True, null=True)
    
    def __str__(self):
        return self.email

class Geography(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.title

class SeniorityLevel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return self.title

class YearAtCompany(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return self.title

class YearofExperience(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return self.title


class FunctionAtComapny(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return self.title


class Automations(models.Model):
    user=models.ForeignKey(LinkedIn, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=True, verbose_name='Name')
    geography = models.ForeignKey(Geography, blank=True, null=True, on_delete=models.DO_NOTHING)
    geography_status = models.BooleanField(default=True)
    srlevel = models.ForeignKey(SeniorityLevel, blank=True, null=True, on_delete=models.DO_NOTHING)
    srlevel_status = models.BooleanField(default=True)
    period = models.ForeignKey(YearAtCompany, blank=True, null=True, on_delete=models.DO_NOTHING)
    period_status = models.BooleanField(default=True)
    functionsatcompany = models.ForeignKey(FunctionAtComapny, blank=True, null=True, on_delete=models.DO_NOTHING)
    functionsatcompanyl_status = models.BooleanField(default=True)
    yearsofexperience = models.ForeignKey(YearofExperience, blank=True, null=True, on_delete=models.DO_NOTHING)
    yearsofexperience_status = models.BooleanField(default=True)
    day = models.CharField(max_length=3, choices=DAYS, default="SUN", verbose_name='Day')
    rate = models.CharField(max_length=1, choices=RATE, default="W", verbose_name='Rate')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
class ScriptInterval(models.Model):
    automation=models.ForeignKey(Automations, blank=True, null=True, on_delete=models.CASCADE)
    interval = models.DateTimeField(auto_now=True, null=True,blank=True)
    running = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.automation.name

class AutomationData(models.Model):
    companyname = models.CharField(max_length=200,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    senioritylevel = models.CharField(max_length=100,blank=True,null=True)
    function = models.CharField(max_length=200,blank=True,null=True)
    degree = models.CharField(max_length=200,blank=True,null=True)
    gradyearstart = models.CharField(max_length=200,blank=True,null=True)
    gradyearend = models.CharField(max_length=200,blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True)
    dateofentry = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    user=models.ForeignKey(LinkedIn, blank=True, null=True, on_delete=models.CASCADE)
    automation = models.ForeignKey(Automations,on_delete=models.CASCADE,blank=True,null=True)
    isduplicated = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=1, choices=DATASTATUS, default="P",  blank=True, null=True, verbose_name='Status')

    def __str__(self):
        return self.name

class Cron(models.Model):
    automation=models.ForeignKey(Automations, blank=True, null=True, on_delete=models.CASCADE)
    execution_type= models.CharField(max_length=200,default='cron')
    is_active=models.BooleanField(blank=True, null=True)
    last_exe_date = models.DateField(max_length=200, null=True, blank=True)
    execution_rate= models.CharField(max_length=200, null=True,blank=True)
    def __str__(self):
        return self.execution_type