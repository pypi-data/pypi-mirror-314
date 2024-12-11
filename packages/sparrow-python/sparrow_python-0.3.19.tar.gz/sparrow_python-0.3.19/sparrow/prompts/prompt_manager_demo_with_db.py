import hashlib
import json
import sqlite3
import uuid

import streamlit as st


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("prompt_manager.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # 用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Prompt表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            current_version INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        # Prompt版本表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id TEXT PRIMARY KEY,
            prompt_id TEXT NOT NULL,
            version INTEGER NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prompt_id) REFERENCES prompts(id)
        )
        """)

        self.conn.commit()

class UserManager:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        cursor = self.db.conn.cursor()
        user_id = str(uuid.uuid4())
        try:
            cursor.execute(
                "INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
                (user_id, username, self.hash_password(password)),
            )
            self.db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,),
        )
        result = cursor.fetchone()
        if result and result[1] == self.hash_password(password):
            return result[0]
        return None

class PromptManager:
    def __init__(self, db):
        self.db = db

    def save_prompt(self, user_id, name, content, tags=None):
        cursor = self.db.conn.cursor()

        # 检查是否已存在
        cursor.execute("SELECT id, current_version FROM prompts WHERE user_id = ? AND name = ?",
                       (user_id, name))
        existing_prompt = cursor.fetchone()

        if existing_prompt:
            prompt_id = existing_prompt[0]
            new_version = existing_prompt[1] + 1

            # 更新当前版本号
            cursor.execute("UPDATE prompts SET current_version = ? WHERE id = ?",
                           (new_version, prompt_id))
        else:
            prompt_id = str(uuid.uuid4())
            new_version = 1

            # 创建新的prompt记录
            cursor.execute("""
                INSERT INTO prompts (id, user_id, name, current_version)
                VALUES (?, ?, ?, ?)
            """, (prompt_id, user_id, name, new_version))

        # 保存新版本
        version_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO prompt_versions (id, prompt_id, version, content, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (version_id, prompt_id, new_version, content, json.dumps(tags or [])))

        self.db.conn.commit()
        return prompt_id, new_version

    def get_prompt_versions(self, prompt_id):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT version, content, tags, created_at
            FROM prompt_versions
            WHERE prompt_id = ?
            ORDER BY version DESC
        """, (prompt_id,))
        return cursor.fetchall()

    def get_prompt_by_version(self, prompt_id, version):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT content, tags, created_at
            FROM prompt_versions
            WHERE prompt_id = ? AND version = ?
        """, (prompt_id, version))
        return cursor.fetchone()

    def list_prompts(self, user_id):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, p.current_version, p.created_at
            FROM prompts p
            WHERE p.user_id = ?
            ORDER BY p.created_at DESC
        """, (user_id,))
        return cursor.fetchall()

def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None

def login_page(user_manager):
    st.title("登录")

    # 登录表单
    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")

        if submit:
            user_id = user_manager.verify_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.success("登录成功!")
                st.rerun()
            else:
                st.error("用户名或密码错误")

    # 注册链接
    if st.button("还没有账号？点击注册"):
        st.session_state.show_register = True
        st.rerun()

def register_page(user_manager):
    st.title("注册")

    with st.form("register_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        password_confirm = st.text_input("确认密码", type="password")
        submit = st.form_submit_button("注册")

        if submit:
            if password != password_confirm:
                st.error("两次输入的密码不一致")
            elif len(password) < 6:
                st.error("密码长度至少为6位")
            elif user_manager.register_user(username, password):
                st.success("注册成功！请返回登录")
                st.session_state.show_register = False
                st.rerun()
            else:
                st.error("用户名已存在")

    if st.button("返回登录"):
        st.session_state.show_register = False
        st.rerun()

def main_page(prompt_manager):
    st.title(f"Prompt 工程开发工具 - 欢迎, {st.session_state.username}!")

    # 登出按钮
    if st.sidebar.button("登出"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()

    # 主要功能区
    st.sidebar.header("功能区")
    mode = st.sidebar.selectbox("选择模式", ["新建 Prompt", "管理 Prompts"])

    if mode == "新建 Prompt":
        st.header("创建新的 Prompt")

        prompt_name = st.text_input("Prompt 名称")
        prompt_content = st.text_area("Prompt 内容", height=300)
        prompt_tags = st.text_input("标签 (用逗号分隔)")

        if st.button("保存"):
            if prompt_name and prompt_content:
                tags = [tag.strip() for tag in prompt_tags.split(",")] if prompt_tags else []
                prompt_id, version = prompt_manager.save_prompt(
                    st.session_state.user_id,
                    prompt_name,
                    prompt_content,
                    tags,
                )
                st.success(f"Prompt '{prompt_name}' (版本 {version}) 已保存!")
            else:
                st.error("请填写名称和内容!")

    else:
        st.header("管理 Prompts")

        prompts = prompt_manager.list_prompts(st.session_state.user_id)
        if not prompts:
            st.info("还没有保存的 Prompt")
        else:
            selected_prompt = st.selectbox(
                "选择 Prompt",
                prompts,
                format_func=lambda x: f"{x[1]} (版本 {x[2]})",
            )

            if selected_prompt:
                prompt_id = selected_prompt[0]
                versions = prompt_manager.get_prompt_versions(prompt_id)

                # 显示版本历史
                selected_version = st.selectbox(
                    "选择版本",
                    versions,
                    format_func=lambda x: f"版本 {x[0]} ({x[3]})",
                )

                if selected_version:
                    content = selected_version[1]
                    tags = json.loads(selected_version[2])

                    st.text_area("Prompt 内容", content, height=300)
                    st.text("标签: " + ", ".join(tags))
                    st.text(f"创建时间: {selected_version[3]}")

def main():
    st.set_page_config(page_title="Prompt 工程开发工具", layout="wide")

    # 初始化
    init_session_state()
    db = Database()
    user_manager = UserManager(db)
    prompt_manager = PromptManager(db)

    # 处理页面显示
    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    if not st.session_state.user_id:
        if st.session_state.show_register:
            register_page(user_manager)
        else:
            login_page(user_manager)
    else:
        main_page(prompt_manager)

if __name__ == "__main__":
    main()
