
def check_availability(start, end, queryset):
    booked = False
    for x in queryset:
        if start > x.end:
            pass
        elif end < x.start:
            pass
        else:
            booked = True
    return booked



