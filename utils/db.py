from utils.supabase_client import get_supabase
import uuid, base64, mimetypes

sb = None

def _db():
    global sb
    if sb is None:
        sb = get_supabase()
    return sb

# ────────────────────────────────────────────────
# INGREDIENTS
# ────────────────────────────────────────────────

def get_all_ingredients():
    res = _db().table("ingredients").select("*").order("category").order("name").execute()
    return res.data or []

def get_or_create_ingredient(name: str, category: str) -> str:
    """Return existing ingredient id or create new one."""
    name = name.strip()
    res = _db().table("ingredients").select("id").ilike("name", name).execute()
    if res.data:
        return res.data[0]["id"]
    new = _db().table("ingredients").insert({"name": name, "category": category}).execute()
    return new.data[0]["id"]

def update_ingredient(ing_id: str, name: str, category: str):
    _db().table("ingredients").update({"name": name, "category": category}).eq("id", ing_id).execute()

# ────────────────────────────────────────────────
# RECIPES
# ────────────────────────────────────────────────

def get_all_recipes():
    res = _db().table("recipes").select("*").order("title").execute()
    return res.data or []

def get_recipe(recipe_id: str):
    res = _db().table("recipes").select("*").eq("id", recipe_id).single().execute()
    return res.data

def get_recipe_ingredients(recipe_id: str):
    res = (
        _db().table("recipe_ingredients")
        .select("*, ingredients(id, name, category)")
        .eq("recipe_id", recipe_id)
        .execute()
    )
    return res.data or []

def create_recipe(title, description, video_url, servings, image_bytes=None, image_name=None):
    image_url = None
    if image_bytes and image_name:
        image_url = upload_image(image_bytes, image_name)
    res = _db().table("recipes").insert({
        "title": title,
        "description": description,
        "video_url": video_url,
        "servings": servings,
        "image_url": image_url,
    }).execute()
    return res.data[0]["id"]

def update_recipe(recipe_id, title, description, video_url, servings, image_bytes=None, image_name=None):
    data = {
        "title": title,
        "description": description,
        "video_url": video_url,
        "servings": servings,
    }
    if image_bytes and image_name:
        data["image_url"] = upload_image(image_bytes, image_name)
    _db().table("recipes").update(data).eq("id", recipe_id).execute()

def delete_recipe(recipe_id: str):
    _db().table("recipes").delete().eq("id", recipe_id).execute()

def save_recipe_ingredients(recipe_id: str, ingredients: list):
    """ingredients: list of dicts with name, category, quantity, unit"""
    # Delete existing
    _db().table("recipe_ingredients").delete().eq("recipe_id", recipe_id).execute()
    # Re-insert
    rows = []
    for ing in ingredients:
        ing_id = get_or_create_ingredient(ing["name"], ing["category"])
        rows.append({
            "recipe_id": recipe_id,
            "ingredient_id": ing_id,
            "quantity": ing["quantity"],
            "unit": ing["unit"],
        })
    if rows:
        _db().table("recipe_ingredients").insert(rows).execute()

# ────────────────────────────────────────────────
# IMAGE UPLOAD
# ────────────────────────────────────────────────

def upload_image(image_bytes: bytes, filename: str) -> str:
    unique_name = f"{uuid.uuid4()}_{filename}"
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    _db().storage.from_("recipe-images").upload(
        unique_name,
        image_bytes,
        {"content-type": mime}
    )
    url = _db().storage.from_("recipe-images").get_public_url(unique_name)
    return url

# ────────────────────────────────────────────────
# WEEK PLAN
# ────────────────────────────────────────────────

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

def get_week_plan():
    res = (
        _db().table("week_plan")
        .select("*, recipes(id, title)")
        .execute()
    )
    return res.data or []

def set_week_plan_entry(weekday: str, recipe_id: str):
    # Remove existing entry for this weekday
    _db().table("week_plan").delete().eq("weekday", weekday).execute()
    if recipe_id:
        _db().table("week_plan").insert({
            "weekday": weekday,
            "recipe_id": recipe_id,
            "plan_date": _weekday_to_date(weekday),
        }).execute()

def remove_week_plan_entry(weekday: str):
    _db().table("week_plan").delete().eq("weekday", weekday).execute()

def _weekday_to_date(weekday: str):
    """Return ISO date string for next occurrence of weekday."""
    from datetime import date, timedelta
    day_map = {d: i for i, d in enumerate(WEEKDAYS)}
    today = date.today()
    target = day_map.get(weekday, 0)
    days_ahead = (target - today.weekday()) % 7
    return (today + timedelta(days=days_ahead)).isoformat()

# ────────────────────────────────────────────────
# SHOPPING LIST
# ────────────────────────────────────────────────

def get_shopping_list():
    res = (
        _db().table("shopping_list")
        .select("*")
        .order("category")
        .order("item_name")
        .execute()
    )
    return res.data or []

def add_recipe_to_shopping_list(recipe_id: str):
    """Add all ingredients of a recipe, summing up duplicates."""
    ings = get_recipe_ingredients(recipe_id)
    for ri in ings:
        ing = ri["ingredients"]
        item_name = ing["name"]
        category = ing["category"]
        quantity = ri["quantity"]
        unit = ri["unit"]

        # Check if same item+unit already in list
        existing = (
            _db().table("shopping_list")
            .select("*")
            .ilike("item_name", item_name)
            .eq("unit", unit)
            .eq("checked", False)
            .execute()
        )
        if existing.data:
            ex = existing.data[0]
            new_qty = (ex["quantity"] or 0) + quantity
            _db().table("shopping_list").update({"quantity": new_qty}).eq("id", ex["id"]).execute()
        else:
            _db().table("shopping_list").insert({
                "ingredient_id": ing["id"],
                "recipe_id": recipe_id,
                "item_name": item_name,
                "quantity": quantity,
                "unit": unit,
                "category": category,
                "checked": False,
                "added_manually": False,
            }).execute()

def add_manual_item(item_name: str, quantity, unit: str, category: str):
    _db().table("shopping_list").insert({
        "item_name": item_name,
        "quantity": quantity,
        "unit": unit,
        "category": category,
        "checked": False,
        "added_manually": True,
    }).execute()

def toggle_shopping_item(item_id: str, checked: bool):
    _db().table("shopping_list").update({"checked": checked}).eq("id", item_id).execute()

def remove_shopping_item(item_id: str):
    _db().table("shopping_list").delete().eq("id", item_id).execute()

def clear_checked_items():
    _db().table("shopping_list").delete().eq("checked", True).execute()

def clear_all_shopping_list():
    _db().table("shopping_list").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()