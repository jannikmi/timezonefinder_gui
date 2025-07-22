from datetime import datetime
from json import dumps

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from pytz import timezone, utc
from pytz.exceptions import UnknownTimeZoneError
from timezonefinder import TimezoneFinder, TimezoneFinderL

from .models import register_api_hit, register_geometry_hit, register_info_hit
from .print_statistics import compile_string as statistic_string

tf = TimezoneFinder()
tfL = TimezoneFinderL()

# 0: TimezoneFinder.timezone_at()
# 1: TimezoneFinder.certain_timezone_at()
# 2: removed in 6.0.0
# 3: TimezoneFinderL.timezone_at()
# 4: TimezoneFinderL.timezone_at_land()
# 5: TimezoneFinder.timezone_at_land()
function_map = {
    0: tf.timezone_at,
    1: tf.certain_timezone_at,
    # 2: tf.closest_timezone_at, removed in 6.0.0
    3: tfL.timezone_at,
    4: tfL.timezone_at_land,
    5: tf.timezone_at_land,
}

# dictionary for all queried geometries:
stored_geometries = {}

import pkg_resources

package_version = pkg_resources.get_distribution("timezonefinder").version


# TODO
#  update directly with git
#  show version, data, package
# user guide api


def json_response(something):
    return HttpResponse(
        dumps(something),
        content_type='application/javascript; charset=utf8'
    )


def main_gui_view_fresh(request):
    print('sending out fresh gui view')
    # send empty main gui page
    context = {
        'lng': '',
        'lat': '',
        'mode': None,
        'package_version': package_version,
    }
    return render(request, 'main_gui_map_view.html', context)


def redirect2fresh_gui(request):
    return HttpResponseRedirect('/gui')


def main_gui_view(request, lng='0', lat='0', mode='0'):
    try:
        lat = float(lat)
        lng = float(lng)
        mode = int(mode)
    except ValueError:
        lat = None
        lng = None
        mode = 0

    context = {
        'lng': lng,
        'lat': lat,
        'mode': mode,
        'package_version': package_version,
    }
    return render(request, 'main_gui_map_view.html', context)


def convert_polygon(polygon):
    # leaflet.js requires (lat,lng) pairs instead of (lng,lat)
    return [(lat, lng) for (lng, lat) in polygon]


def convert_multipolygon(multipolygon):
    # leaflet.js requires (lat,lng) pairs instead of (lng,lat)
    return [convert_polygon(polygon) for polygon in multipolygon]


def convert_geometry(geometry):
    return [convert_multipolygon(multipolygon) for multipolygon in geometry]


# Views with JSON Response
def gui_get_geometry(request, tz_name):
    try:
        geometry = stored_geometries[tz_name]
        register_geometry_hit(tz_name)
        # print('already had this geometry stored.')
    except KeyError:
        # there is no entry for this tz yet
        # print('trying to add geometry for tz:', tz_name)
        # TODO
        # try:
        geometry_vanilla = tf.get_geometry(tz_name, coords_as_pairs=True)
        geometry = convert_geometry(geometry_vanilla)
        stored_geometries[tz_name] = geometry
        # print('successfully added.')
        # print('stored geometries for zones:', stored_geometries.keys())
        register_geometry_hit(tz_name)
        # except ValueError:
        #     geometry = None
        #     register_geometry_hit('*invalid*')

    return json_response({
        'tz_name': tz_name,
        'geometry': geometry,
    })


def gui_get_info(request, tz_name):
    # tzinfo has to be None (means naive)
    # get current time UTC 0:00
    current_utc_time = datetime.utcnow()
    try:
        tz = timezone(tz_name)
        current_datetime_in_timezone = current_utc_time.replace(tzinfo=utc).astimezone(tz)
        tz_abbreviation = current_datetime_in_timezone.strftime('%Z')
        current_offset = current_datetime_in_timezone.tzinfo.utcoffset(current_datetime_in_timezone)
        s = current_offset.total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, remainder = divmod(remainder, 60)
        current_offset = "%d:%02d" % (int(hours), int(minutes))
        # current_offset = timedelta(hours=(current_offset.total_seconds()/3600))
        # if current_offset.days == -1:
        #     # current_offset = timedelta(hours=current_offset.hours - 24)
        #     current_offset = timedelta(days=1, hours=-24)

        # current_offset = current_offset.__str__()
        current_datetime_in_timezone = current_datetime_in_timezone.strftime('%Y-%m-%d %H:%M:%S')

        register_info_hit(tz_name)

    except UnknownTimeZoneError:
        current_datetime_in_timezone = None
        tz_abbreviation = None
        current_offset = None
        register_info_hit('*invalid*')

    return json_response({
        'tz_name': tz_name,
        'current_datetime_in_tz': current_datetime_in_timezone,
        'tz_abbreviation': tz_abbreviation,
        'current_offset': current_offset,
    })


def api_request(request, mode='0', lng='0', lat='0'):
    tz_name = None
    try:
        lat = float(lat)
        lng = float(lng)
        mode = int(mode)
        tz_function = functions[mode]
        # note: ValueError is also raised when coords are out of bound
        tz_name = tz_function(lng=lng, lat=lat)
        register_api_hit(tz_name)
        if tz_name is None:
            status_code = 204  # http standard: No Content
        else:
            status_code = 200  # OK
    except ValueError:
        # the statistics should differentiate between 'no tz found' and invalid query
        register_api_hit('*invalid*')
        status_code = 422  # Unprocessable Entity

    return json_response({
        'tz_name': tz_name,
        'status_code': status_code,
    })


def api_bad_request(request):
    return json_response({
        'tz_name': None,
        'status_code': 400  # Bad request
    })


def statistic_view(request):
    return HttpResponse(statistic_string(), content_type='text/plain')


api_guide_content = open('static_api_guide.txt', 'r').read()


def static_api_guide_view(request):
    return HttpResponse(api_guide_content, content_type='text/plain')
