from django.shortcuts import render
from django.http import HttpResponse
from rateprofessors.models import Section, Instructor, Classes
import json

def search(request):
	if request.is_ajax():
		query = request.GET['term']
		results = Classes.objects.filter(class_short_name__icontains = query )[:20]
		result_list = []
		for result in results:
			class_name = result.class_short_name[:-6] + " - " + result.class_long_name
			result_json = {'id' : result.id, 'label' : class_name, 'value' : result.class_short_name[:-6]}
			result_list.append(result_json)
		return HttpResponse(json.dumps(result_list), 'application/json')
	elif 'query' in request.GET:
		query = request.GET['query']
		if query:
			results = Section.objects.filter(class_id__class_short_name__icontains = query)
			for result in results:
				result.class_id.class_short_name = result.class_id.class_short_name[:-6]
		else:
			results = []
		return render(request, 'rateprofessors/search.html', {'results': results})
	else:
		return render(request, 'rateprofessors/search.html', {'results': []})
