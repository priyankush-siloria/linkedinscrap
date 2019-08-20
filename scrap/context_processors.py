from .models import Automations, AutomationData
def automations_count(request):
	total_automations=Automations.objects.all().count()
	total_scraped=AutomationData.objects.all().count()
	total_apporoved=AutomationData.objects.filter(status="A").count()
	total_rejected=AutomationData.objects.filter(status="R").count()
	return {
	'total_automations':total_automations,
	'total_scraped':total_scraped,
	'total_apporoved':total_apporoved,
	'total_rejected':total_rejected,
	}