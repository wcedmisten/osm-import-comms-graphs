import os
import re
import datetime
import csv

ARCHIVES_DIR = "mailing_list_archives"

lines = []

for month_archive_file in os.listdir(ARCHIVES_DIR):
    with open(os.path.join(ARCHIVES_DIR, month_archive_file)) as f:
        for line in f.readlines():
            lines.append(line)

FROM_LINE_REGEX = "From (.+ at .+)  [A-Z][a-z]{2} ([A-Z][a-z]{2} *\d{1,2} \d{2}:\d{2}:\d{2} \d{4})"

replies = []

subjects = set()

# manually classified each thread by country
subject_country_map = {
    '[talk-au] VIC Traffic Lights MapRoulette import': 'AU',
    '[Talk-us-sfbay] Proposed import of San Franciscoaddresses': 'US',
    'VIC Traffic Lights MapRoulette import': 'AU',
    'US - HIDFL (DHS) Hospital Import': 'US',
    'Share cycle ports import in Japan': 'JP',
    'Rio Branco (Brazil) addresses import': 'BR',
    'Rif: Re:  Import Civic House Numbers in Sondrio': 'IT',
    'Proposed import of San Francisco addresses': 'US',
    'Possible import of buildings in Antananarivo, Madagascar?': "MG",
    'Possible import of buildings in Antananarivo,Madagascar?': "MG",
    'Latvia-bot': 'LV',
    'LINZ Data Import - Undersea features': 'NZ',
    'Import proposal: Global ML Building Footprints forNottinghamshire, UK': 'GB',
    'Import Civic House Numbers in Sondrio': 'IT',
    'Import Civic House Numbers in Samolaco': 'IT',
    'Delikatesy Centrum - Polish supermarket chain': 'PL',
    'Conflation of London Cycle Infrastructure Database': 'GB',
    'Brisbane (Australia) Cycling Import': 'AU',
    'Address import from government open data in Serbia': 'RS',
    'A lot of nodes imported from GEOnet Names Server (GNS) were deleted in Yemen, KSA, Egypt Iraq and other countries': 'YE',
    '=?utf-8?q?=D8=B1=D8=AF=3A_A_lot_of_nodes_imported_from?==?utf-8?q?_GEOnet_Names_Server_=28GNS_=29_were_deleted_in_Yemen=2C_KSA=2C?==?utf-8?q?_Egypt_Iraq_and_other_countries?=': 'YE',
    '=?utf-8?q?=D8=B1=D8=AF=3A_A_lot_of_nodes_imported_from?==?utf-8?q?_GEOnet_Names_Server_=28GNS_=29_were_deleted_in_Yemen=2C?==?utf-8?q?_KSA=2C_Egypt_Iraq_and_other_countries?=': 'YE',
    '=?iso8859-6?q?=D1=CF=3A__A_lot_of_nodes_imported_from_?==?iso8859-6?q?GEOnet_Names_Server_=28GNS_=29_were_deleted_in_Yemen=2C_KSA?==?iso8859-6?q?=2C_Egypt_Iraq_and_other_countries?=': 'YE',
    '=?iso8859-6?q?=D1=CF=3A_A_lot_of_nodes_imported_from_G?==?iso8859-6?q?EOnet_Names_Server_=28GNS_=29_were_deleted_in_Yemen=2C_KSA?==?iso8859-6?q?=2C_Egypt_Iraq_and_other_countries?=': 'YE',
    '=?iso-8859-1?q?Data_import_at_Universidad_de_Antioquia?==?iso-8859-1?q?_=28Colombia=2C_Medell=EDn=29?=': 'YE'
}

for idx, line in enumerate(lines):
    match = re.search(FROM_LINE_REGEX, line)
    if match:
        subject_line = lines[idx+3]
        i = idx + 4
        while not re.match(r".+:", lines[i]):
            subject_line += lines[i].strip()
            i += 1

        subject_line = subject_line.replace("\n", "")

        subject = subject_line.split("Subject: [Imports] ")[1]
        subjects.add(subject)

        replies.append({
            "email": match.group(1).replace(" at ", "@"),
            "date": datetime.datetime.strptime(match.group(2), '%b %d %H:%M:%S %Y').replace(tzinfo=datetime.timezone.utc).isoformat(),
            "subject": subject,
            "country": subject_country_map[subject]
        })

with open('mailing_archive.csv', 'w', newline='') as csvfile:
    fieldnames = ['email', 'date', 'country', 'subject']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()
    for reply in replies:
        writer.writerow(reply)
