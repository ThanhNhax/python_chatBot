import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuyensinh_site.settings')
django.setup()

from chatbot.models import Intent

def load():
    print("Loading data from knowledge.json to DB...")
    with open('chatbot/data/knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data['intents']:
        # Convert list of keywords to comma separated string
        keywords_str = ', '.join(item['keywords'])
        
        obj, created = Intent.objects.get_or_create(
            tag=item['tag'],
            defaults={
                'keywords': keywords_str,
                'answer': item['answer']
            }
        )
        if not created:
            obj.keywords = keywords_str
            obj.answer = item['answer']
            obj.save()
            print(f"Updated: {item['tag']}")
        else:
            print(f"Created: {item['tag']}")
        count += 1
        
    print(f"Done! Processed {count} intents.")

if __name__ == '__main__':
    load()
