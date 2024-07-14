import requests
import os
from dotenv import load_dotenv
import config
from datetime import datetime, timedelta
import schedule
import time

load_dotenv()
def get_next_service():
    url = 'https://api.planningcenteronline.com/services/v2/service_types/1582/plans?filter=future'
    app_id = os.getenv('APP_ID')
    app_secret = os.getenv('APP_SECRET')
    auth = (app_id, app_secret)
    response = requests.get(url, auth=auth)

    data = response.json()['data']


    next_service = None
    for plan in data:
        date = datetime.strptime(plan['attributes']['dates'], "%B %d, %Y").date()
        if date >= datetime.now().date():
            next_service = plan
            break

    if next_service:
        plan_id = next_service['id']
        url = f'https://api.planningcenteronline.com/services/v2/service_types/1582/plans/{plan_id}/team_members'
        response = requests.get(url, auth=auth)
        team_members = response.json()['data']
    else:
        print('No upcoming services')
    count_updated = 0
    for member in team_members:
        if member['attributes']['team_position_name'][0].isdigit():
            slot_num = int(member['attributes']['team_position_name'][0])
            attributes = member['attributes']
            name = attributes['name']
            img_url = attributes['photo_thumbnail'].split('?')[0]
            img_name = f'{name}.jpg'.lower().replace(' ', '_')
            img_path = os.path.join(config.get_gif_dir(),img_name)
            print(img_path)
            if not os.path.exists(img_path):
                response = requests.get(img_url).content
                with open(img_path, 'wb') as f:
                    f.write(response)
            else:
                print(f'{img_name} already exists')
            config.update_slot({"extended_name":name,"slot":slot_num})
            count_updated += 1
    if count_updated > 0:
        config.save_current_config()
        print(f'Updated {count_updated} slots')


def scheduled_job():
    schedule.every(1).hour.do(get_next_service)

    while True:
        schedule.run_pending()
        time.sleep(60)