import gradio as gr
from config import USERS, ROLE_MENUS, DOCUMENT_GROUPS

# ================= LOGIN =================
def login_fn(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return (
            "✅ Đăng nhập thành công",
            True,
            username,
            user["role"],
            user["groups"],
            ROLE_MENUS[user["role"]],
        )
    return (
        "❌ Sai tài khoản hoặc mật khẩu",
        False,
        None,
        None,
        None,
        None,
    )


# ================= REQUIRE (CHECK PERMISSION) =================
def require(feature, logged_in, menus):
    if not logged_in:
        return False, "⚠️ Vui lòng đăng nhập trước"
    if feature not in (menus or []):
        return False, "⛔ Bạn không có quyền truy cập chức năng này"
    return True, ""


# ================= GROUP FILTER =================
def get_allowed_groups(groups):
    if not groups:
        return []
    if "all" in groups:
        return list(DOCUMENT_GROUPS.keys())
    return groups


# ================= USER INFO (THAY SIDEBAR) =================
def user_info(username, role, groups):
    if not username:
        return "🔒 Chưa đăng nhập"

    badge = "ADMIN" if role == "admin" else "GUEST"

    text = f"**{badge}: {username}**"

    if role == "guest":
        allowed = get_allowed_groups(groups)
        text += "\n\n📂 Nhóm: " + ", ".join(allowed)

    return text


# ================= LOGOUT =================
def logout_fn():
    return (
        "🔓 Đã đăng xuất",
        False,
        None,
        None,
        None,
        None,
    )
