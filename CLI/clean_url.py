import sys
replacement_pairs = {
    "%3A":":",
    "%2F":"/",
    "%3F":"?",
    "%23":"#",
    "%26":"&",
    "%3D":"=",
    "%2C":",",
}
raw_url = sys.argv[1]
# "https://jgctjqdn.r.eu-west-1.awstrack.me/L0/https:%2F%2Fwww.evri.com%2Ftrack%2F%23%2Fparcel%2FC00HHA0352597106%3Fpostcode=OX11%25206FU%26utm_campaign=track_and_divert%26utm_content=wevegotit_track_divert%26utm_medium=email%26utm_source=wevegotit_email_TD_CTA%26utm_term=629/1/010201876f8fefc2-4cc947e6-f5b9-45f7-ab7f-ff150bb43eeb-000000/MgmZDfKLXG83Qg4orx0eUlHl19g=317"
# "https://l.facebook.com/l.php?u=https%3A%2F%2Fbit.ly%2F3ZUTMn2%3Ffbclid%3DIwAR0AqYRVvO5cCUqQlBk2CYZKsFuuOI8P3Lkp7S-MpdytS4L5eSaBTDieGZc&h=AT3exw3gta1FiHKIQVqlV-ng5SYvZAVCGFTgf83IYZ29NmOB7bHJRWekK4EwgvVsLiWRCtTrOmGcv9170jsS58sMZTt0VTmY98a_GXECp938fT4vA-IKoRzpsh45&__tn__=%2CmH-R&c[0]=AT3WO5DCLNQ9MHhei6KjTEcVDDhBP-ObnvWGAm-1k9APouJr2GgicSi499HeY-8c43j6MKU5-ezSeuO2B2j-RfEoZE5QltmXv-YGVMxgk51NFk5FZr1p5Y3iJMdLf3PhOe4gfNq0QX-vwJV6hUFI2qDyYeA1iLbAjG6pb2AD9zAACLOuITEpXC1N3PgYDaLTVc2_AE_dCoAbXH2rDQ"
clipped_url = "http"+"http".join(raw_url.split("http")[2:])
# "https:%2F%2Fwww.evri.com%2Ftrack%2F%23%2Fparcel%2FC00HHA0352597106%3Fpostcode=OX11%25206FU%26utm_campaign=track_and_divert%26utm_content=wevegotit_track_divert%26utm_medium=email%26utm_source=wevegotit_email_TD_CTA%26utm_term=629/1/010201876f8fefc2-4cc947e6-f5b9-45f7-ab7f-ff150bb43eeb-000000/MgmZDfKLXG83Qg4orx0eUlHl19g=317"
# "https%3A%2F%2Fbit.ly%2F3ZUTMn2%3Ffbclid%3DIwAR0AqYRVvO5cCUqQlBk2CYZKsFuuOI8P3Lkp7S-MpdytS4L5eSaBTDieGZc&h=AT3exw3gta1FiHKIQVqlV-ng5SYvZAVCGFTgf83IYZ29NmOB7bHJRWekK4EwgvVsLiWRCtTrOmGcv9170jsS58sMZTt0VTmY98a_GXECp938fT4vA-IKoRzpsh45&__tn__=%2CmH-R&c[0]=AT3WO5DCLNQ9MHhei6KjTEcVDDhBP-ObnvWGAm-1k9APouJr2GgicSi499HeY-8c43j6MKU5-ezSeuO2B2j-RfEoZE5QltmXv-YGVMxgk51NFk5FZr1p5Y3iJMdLf3PhOe4gfNq0QX-vwJV6hUFI2qDyYeA1iLbAjG6pb2AD9zAACLOuITEpXC1N3PgYDaLTVc2_AE_dCoAbXH2rDQ"
decoded_url = clipped_url[:] # to be absolutely sure it's a copy (even though it's necessarily not a copy)
for key, val in replacement_pairs.items():
    decoded_url = decoded_url.replace(key, val)
# "https://www.evri.com/track/#/parcel/C00HHA0352597106?postcode=OX11%25206FU&utm_campaign=track_and_divert&utm_content=wevegotit_track_divert&utm_medium=email&utm_source=wevegotit_email_TD_CTA&utm_term=629/1/010201876f8fefc2-4cc947e6-f5b9-45f7-ab7f-ff150bb43eeb-000000/MgmZDfKLXG83Qg4orx0eUlHl19g=317"
# "https://bit.ly/3ZUTMn2?fbclid=IwAR0AqYRVvO5cCUqQlBk2CYZKsFuuOI8P3Lkp7S-MpdytS4L5eSaBTDieGZc&h=AT3exw3gta1FiHKIQVqlV-ng5SYvZAVCGFTgf83IYZ29NmOB7bHJRWekK4EwgvVsLiWRCtTrOmGcv9170jsS58sMZTt0VTmY98a_GXECp938fT4vA-IKoRzpsh45&__tn__=,mH-R&c[0]=AT3WO5DCLNQ9MHhei6KjTEcVDDhBP-ObnvWGAm-1k9APouJr2GgicSi499HeY-8c43j6MKU5-ezSeuO2B2j-RfEoZE5QltmXv-YGVMxgk51NFk5FZr1p5Y3iJMdLf3PhOe4gfNq0QX-vwJV6hUFI2qDyYeA1iLbAjG6pb2AD9zAACLOuITEpXC1N3PgYDaLTVc2_AE_dCoAbXH2rDQ"
# optional: remove all the tracking info starting from ?fbclid
print()
print(decoded_url)