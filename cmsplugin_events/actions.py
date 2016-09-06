from django.http import HttpResponse


def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=event.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Event"),
        smart_str(u"Name"),
        smart_str(u"Email"),
        smart_str(u"Registration Date"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.event.title),
            smart_str(obj.name),
            smart_str(obj.email),
            smart_str(obj.date),
        ])
    return response


export_csv.short_description = u"Export CSV"
