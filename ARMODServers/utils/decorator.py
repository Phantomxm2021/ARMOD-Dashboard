from Apps.ARExperiences.models import Statistics
import time
def pvCount(func):
    def wrapper(request,*args,**kwargs):
            dateObj_list = Statistics.objects.filter(date=time.strftime('%Y-%m-%d'))
            count = dateObj_list.count()
            if count == 0:
                Statistics.objects.create(pv=1,uv=0,date=str(time.strftime('%Y-%m-%d')))
            else:
                todayObj = Statistics.objects.get(date=str(time.strftime('%Y-%m-%d')))
                todayObj.pv += 1
                todayObj.save()
            return func(request, *args, **kwargs)
    return wrapper