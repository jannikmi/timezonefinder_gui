from .models import TimezoneStatistics
from os import rename


def compile_string():
    list_of_all_entries = []
    for entry in TimezoneStatistics.objects.all().iterator():
        list_of_all_entries.append((entry.tz_name, entry.api_hits, entry.info_hits, entry.geometry_hits,))

    list_of_all_entries = sorted(list_of_all_entries, key=lambda x: x[1])
    template = '{0:30s} | {1:10s} | {2:10s} | {3:10s}\n'
    output_string = 'Statistics of the timezonefinderL API/GUI\n\n'
    output_string += template.format('timezone name', 'api hits', 'info hits', 'geometry hits')

    output_string += 63 * '_' + '\n'
    api_sum = 0
    info_sum = 0
    geo_sum = 0
    for name, api, info, geo in list_of_all_entries:
        if name is None:
            output_string += template.format('None', str(api), str(info), str(geo))
        else:
            output_string += template.format(name, str(api), str(info), str(geo))
        api_sum += api
        info_sum += info
        geo_sum += geo

    output_string += 63 * '_' + '\n'
    output_string += (template.format('TOTAL', str(api_sum), str(info_sum), str(geo_sum)))
    return output_string


def print_statistics_to_file(path='hit_statistics.txt'):
    new_filename = path + '_new'
    file = open(new_filename, 'w')
    file.write(compile_string())
    file.close()
    rename(new_filename, path)


if __name__ == '__main__':
    print_statistics_to_file(path='hit_statistics.txt')
    print(compile_string())
