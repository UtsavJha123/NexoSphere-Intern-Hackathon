import os
import random
from datetime import datetime, timezone

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI missing")

client = MongoClient(MONGO_URI)
db = client["linkedin_mvp"]
profiles = db["UserProfiles"]
posts = db["Posts"]

# abort if already seeded
if profiles.count_documents({"contact_info.email": "jordan.lee@samplemail.com"}):
    print("↩︎  Demo data already exists – nothing to do.")
    quit()

now = datetime.now(timezone.utc)

users = [
    {
        "_id": ObjectId(),
        "name": "Jordan Lee",
        "headline": "Senior Backend Engineer | Go • Kubernetes",
        "contact_info": {"email": "jordan.lee@samplemail.com"},
        "password": "pw1",
        "created_at": now,
        "updated_at": now,
    },
    {
        "_id": ObjectId(),
        "name": "Priyanka Desai",
        "headline": "Product Manager • B2B SaaS",
        "contact_info": {"email": "priyanka.desai@samplemail.com"},
        "password": "pw2",
        "created_at": now,
        "updated_at": now,
    },
    {
        "_id": ObjectId(),
        "name": "Miguel Alvarez",
        "headline": "Data Scientist | NLP • Generative AI",
        "contact_info": {"email": "miguel.alvarez@samplemail.com"},
        "password": "pw3",
        "created_at": now,
        "updated_at": now,
    },
    {
        "_id": ObjectId(),
        "name": "Sophie Müller",
        "headline": "UX Designer | Fintech • Mobile",
        "contact_info": {"email": "sophie.mueller@samplemail.com"},
        "password": "pw4",
        "created_at": now,
        "updated_at": now,
    },
    {
        "_id": ObjectId(),
        "name": "Noah Carter",
        "headline": "DevOps Engineer | Cloud • IaC",
        "contact_info": {"email": "noah.carter@samplemail.com"},
        "password": "pw5",
        "created_at": now,
        "updated_at": now,
    },
]

profiles.insert_many(users)
print("✓ 5 users inserted")

# Assign connections randomly (each user connects to 1-3 others, not self)
user_ids = [str(u["_id"]) for u in users]
for user in users:
    possible_connections = [uid for uid in user_ids if uid != str(user["_id"])]
    num_connections = random.randint(1, min(3, len(possible_connections)))
    connections = random.sample(possible_connections, num_connections)
    profiles.update_one({"_id": user["_id"]}, {"$set": {"connections": connections}})

author_id = str(users[0]["_id"])
contents = [
    "Just upgraded our Kubernetes cluster to 1.31—zero downtime! 🚀",
    "Deployed a new micro-service stack; latency down 18 %.",
    "Exploring operators for smarter cluster self-healing.",
    "Mentoring junior devs on Go concurrency patterns.",
    "Back from KubeCon—so many ideas for the next release!",
]
posts.insert_many([
    {
        "post_id": str(ObjectId()),
        "author_id": author_id,
        "post_content": txt,
        "likes": random.randint(5, 40),
        "comments": [],
        "timestamp": now,
    }
    for txt in contents
])
print("✓ 5 posts inserted for Jordan Lee")

