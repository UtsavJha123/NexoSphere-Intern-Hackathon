import os
from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import uvicorn
from faker import Faker

# ── load env ───────────────────────────────────────────────────
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found.  Copy .env.example → .env and edit.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
client.server_info()  # raises if Atlas is unreachable
db = client["linkedin_mvp"]
profiles = db["UserProfiles"]
posts = db["Posts"]

fake = Faker()

# ── helpers ────────────────────────────────────────────────────
def oid() -> ObjectId:
    return ObjectId()

def serialize(doc: dict) -> dict:
    """Recursively convert ObjectIds to str and _id → id."""
    def conv(v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, list):
            return [conv(i) for i in v]
        if isinstance(v, dict):
            return {k: conv(i) for k, i in v.items()}
        return v
    data = conv(doc)
    if "_id" in data:
        data["id"] = data.pop("_id")
    return data

# ── Pydantic models ────────────────────────────────────────────
class Location(BaseModel):
    city: str
    country: str

class ContactInfo(BaseModel):
    email: EmailStr
    website: Optional[str] = None

class Experience(BaseModel):
    experience_id: str
    title: str
    start_date: datetime
    end_date: Optional[datetime] = None
    current_company: Optional[str] = None  # Add current_company field

class Comment(BaseModel):
    comment_id: str
    author_id: str
    content: str
    timestamp: datetime

class Post(BaseModel):
    post_id: str
    author_id: str
    post_content: str
    likes: int = 0
    comments: List[Comment] = []
    timestamp: datetime

class ProfileBase(BaseModel):
    name: str
    headline: str
    pronouns: Optional[str] = None
    about: Optional[str] = None
    location: Optional[Location] = None
    contact_info: ContactInfo
    experience: List[Experience] = []
    analytics: Optional[dict] = None
    skills: Optional[List[str]] = None
    connections: List[str] = []
    posts: List[str] = []  # New field for post IDs

class ProfileCreate(ProfileBase):
    password: str

class ProfileOut(ProfileBase):
    id: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    headline: Optional[str] = None
    pronouns: Optional[str] = None
    about: Optional[str] = None
    location: Optional[Location] = None
    skills: Optional[List[str]] = None
    connections: Optional[List[str]] = None
    posts: Optional[List[str]] = None  # Allow updating posts

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ── FastAPI app ────────────────────────────────────────────────
app = FastAPI(title="Nexosphere API")

def user_header(x_user_id: str = Header(...)) -> str:
    return x_user_id

# ── login (auto-create) ───────────────────────────────────────
@app.post("/api/login", response_model=ProfileOut)
def login(body: LoginRequest):
    user = profiles.find_one({"contact_info.email": body.email})
    if user:
        return serialize(user)

    # Create 5 dummy posts for the new user, each with random comments
    post_ids = []
    for _ in range(5):
        post_id = str(oid())
        # Generate random comments for each post
        comments = []
        for _ in range(fake.random_int(min=1, max=4)):
            comment = {
                "comment_id": str(oid()),
                "author_id": str(oid()),
                "content": fake.sentence(nb_words=10),
                "timestamp": datetime.now(timezone.utc),
            }
            comments.append(comment)
        post = {
            "post_id": post_id,
            "author_id": None,  # Will set after user is created
            "post_content": fake.sentence(nb_words=12),
            "likes": fake.random_int(min=0, max=100),
            "comments": comments,
            "timestamp": datetime.now(timezone.utc),
        }
        posts.insert_one(post)
        post_ids.append(post_id)

    new_profile = {
        "_id": oid(),
        "name": body.email.split("@")[0].replace(".", " ").title(),
        "headline": fake.job(),
        "pronouns": fake.random_element(["he/him", "she/her", "they/them", None]),
        "about": fake.text(max_nb_chars=120),
        "location": {"city": fake.city(), "country": fake.country()},
        "contact_info": {"email": body.email, "website": fake.url()},
        "experience": [
            {
                "experience_id": str(oid()),
                "title": fake.job(),
                "start_date": fake.date_time_this_decade(tzinfo=timezone.utc),
                "end_date": None if fake.boolean() else fake.date_time_this_year(tzinfo=timezone.utc),
                "current_company": fake.company() if fake.boolean() else None,
            }
            for _ in range(fake.random_int(min=1, max=3))
        ],
        "analytics": {"views": fake.random_int(min=0, max=1000)},
        "skills": [fake.job().split()[0] for _ in range(fake.random_int(min=3, max=7))],
        "connections": [],
        "posts": post_ids,
        "password": body.password,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    profiles.insert_one(new_profile)

    # Update the author_id for the posts to the new user's id
    user_id = str(new_profile["_id"])
    posts.update_many({"post_id": {"$in": post_ids}}, {"$set": {"author_id": user_id}})

    # --- Mutual connections logic ---
    # Get all existing users except the new user
    existing_users = list(profiles.find({"_id": {"$ne": new_profile["_id"]}}))
    if existing_users:
        import random
        # Pick 1-3 random users to connect with, ensure no duplicates
        num_connections = min(len(existing_users), fake.random_int(min=1, max=3))
        selected_users = random.sample(existing_users, num_connections)
        selected_user_ids = list({str(u["_id"]) for u in selected_users})  # set to ensure uniqueness
        # Update new user's connections (no duplicates)
        profiles.update_one({"_id": new_profile["_id"]}, {"$set": {"connections": selected_user_ids}})
        # Update each selected user's connections to include the new user (mutual, no duplicates)
        for u in selected_users:
            uid = u["_id"]
            # Fetch current connections, add if not present
            user_doc = profiles.find_one({"_id": uid})
            current_conns = set(user_doc.get("connections", []))
            current_conns.add(user_id)
            profiles.update_one({"_id": uid}, {"$set": {"connections": list(current_conns)}})
        # Also update the in-memory new_profile for return
        new_profile["connections"] = selected_user_ids

    # Ensure no duplicate post IDs in user's posts
    new_profile["posts"] = list(dict.fromkeys(new_profile["posts"]))

    # Ensure no duplicate skills
    new_profile["skills"] = list(dict.fromkeys(new_profile["skills"]))

    # Ensure no duplicate experience titles
    seen_titles = set()
    unique_experience = []
    for exp in new_profile["experience"]:
        if exp["title"] not in seen_titles:
            unique_experience.append(exp)
            seen_titles.add(exp["title"])
    new_profile["experience"] = unique_experience

    return serialize(new_profile)

# ── User CRUD ─────────────────────────────────────────────────
@app.post("/api/users", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_user(body: ProfileCreate):
    if profiles.find_one({"contact_info.email": body.contact_info.email}):
        raise HTTPException(409, "email already exists")
    doc = body.model_dump()
    doc["_id"] = oid()
    doc["created_at"] = doc["updated_at"] = datetime.now(timezone.utc)
    profiles.insert_one(doc)
    return serialize(doc)

@app.get("/api/users", response_model=List[ProfileOut])
def list_users():
    return [serialize(u) for u in profiles.find({})]

@app.get("/api/users/{user_id}", response_model=ProfileOut)
def get_user(user_id: str):
    doc = profiles.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(404, "user not found")
    return serialize(doc)

@app.put("/api/users/{user_id}", response_model=ProfileOut)
def update_user(user_id: str, body: ProfileUpdate, caller: str = Depends(user_header)):
    # Security: Ensure users can only update their own profile
    if user_id != caller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile."
        )

    update_data = body.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body cannot be empty."
        )

    update_data["updated_at"] = datetime.now(timezone.utc)
    result = profiles.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    updated_user = profiles.find_one({"_id": ObjectId(user_id)})
    return serialize(updated_user)

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, caller: str = Depends(user_header)):
    # Security: Ensure users can only delete their own profile
    if user_id != caller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own profile."
        )

    # First, delete all posts associated with the user
    posts.delete_many({"author_id": user_id})

    # Then, delete the user profile
    result = profiles.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

# ── Post CRUD (author-restricted) ─────────────────────────────
@app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(body: Post, caller: str = Depends(user_header)):
    body.author_id = caller
    body.post_id = str(oid())
    body.timestamp = datetime.now(timezone.utc)
    posts.insert_one(body.model_dump())
    return body

@app.get("/api/users/{user_id}/posts", response_model=List[Post])
def list_user_posts(user_id: str):
    return [serialize(p) for p in posts.find({"author_id": user_id})]

@app.get("/api/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    post = posts.find_one({"post_id": post_id})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return serialize(post)

@app.put("/api/posts/{post_id}", response_model=Post)
def update_post(post_id: str, body: Post, caller: str = Depends(user_header)):
    existing = posts.find_one({"post_id": post_id})
    if not existing:
        raise HTTPException(404, "post not found")
    if existing["author_id"] != caller:
        raise HTTPException(403, "not the author")

    update = body.model_dump(exclude_unset=True)
    posts.update_one({"post_id": post_id}, {"$set": update})
    existing.update(update)
    return serialize(existing)

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, caller: str = Depends(user_header)):
    result = posts.delete_one({"post_id": post_id, "author_id": caller})
    if result.deleted_count == 0:
        raise HTTPException(404, "post not "
                                 "found or not owner")

# ── root redirect to swagger ─────────────────────────────────
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🌐  API docs: http://127.0.0.1:8080/docs")
    print(db.list_collection_names())
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

