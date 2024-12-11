import streamlit as st
from manager import PromptManager
from openai import OpenAI


def init_session_state():
    """Initialize session state variables"""
    if "show_delete_confirm" not in st.session_state:
        st.session_state.show_delete_confirm = False
        st.session_state.version_to_delete = None

        oai_client = OpenAI(
            base_url="http://localhost:9999/v1",
            api_key="empty",
        )
        st.session_state.oai_client = oai_client

        st.session_state.messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "{user_input}"},
        ]


def add_message(multimodal=False):
    if multimodal:
        st.session_state.messages.append({"role": "mm_user",
                                          "content": [
                                              {"text": ""},
                                              {"type": "image_url",
                                               "image_url": "https://"}
                                          ]
                                          })
    else:
        st.session_state.messages.append({"role": "user", "content": ""})


def delete_message(index):
    st.session_state.messages.pop(index)


def render_sidebar():
    """Render sidebar and return selected mode"""
    st.sidebar.header("功能区")
    return st.sidebar.radio("选择模式", ["创建或更新 Prompt", "加载已有 Prompt", "批量测试"])


def update_message_content(index):
    st.session_state.messages[index]["content"] = st.session_state[f"message_{index}"]

def update_multimodal_message_content(index, content_type, inner_index):
    st.session_state.messages[index].setdefault("content", [])
    if content_type == "text":
        st.session_state.messages[index]["content"].append({"text": st.session_state[f"multimodal_text_{index}_{inner_index}"]})
    else:
        st.session_state.messages[index]["content"].append({"type": content_type, content_type: st.session_state[f"multimodal_{content_type}_{index}_{inner_index}"]})


@st.fragment
def add_one_multimodal_message(message, i):
    ROLES = ["user", "assistant", "mm_user"]
    cols = st.columns([0.2, 0.70, 0.1])

    with cols[0]:
        st.session_state.messages[i]["role"] = st.selectbox(
            "角色",
            options=ROLES,
            key=f"role_{i}",
            index=ROLES.index(message["role"]),
        )

    with cols[1]:
        if st.session_state.messages[i]["role"] == "mm_user":

            def add_mm_content():
                # 显示一个列表输入区域，一个text 一个 image_url
                for idx, _content in enumerate(message['content']):
                    st.text_area(
                        "text",
                        value=_content['text'],
                        key=f"multimodal_text_{i}_{idx}",
                        placeholder="请输入文本",
                        on_change=update_multimodal_message_content,
                        args=(i, 'text', idx),
                    )
                    cols_inner = st.columns([0.2, 0.70, 0.1])
                    # with cols_inner[0]:
                    #     _content["type"] = st.selectbox(
                    #         "媒体类型",
                    #         options=['image_url', "video_url", "image"],
                    #         key=f"multimodal_text_{i}_idx",
                    #         index=0,
                    #     )
                    st.text_area(
                        "image_url",
                        value=_content['image_url'],
                        key=f"multimodal_image_url_{i}_{idx}",
                        placeholder="请输入图片url",
                        on_change=update_multimodal_message_content,
                        args=(i,'image_url', idx),
                    )
                add_mm_content()
        else:
            st.text_area(
                "content",
                value=message["content"],
                key=f"message_{i}",
                placeholder="请输入内容",
                on_change=update_message_content,
                args=(i,),
            )

    with cols[2]:
        if st.button("删除", key=f"delete_{i}"):
            delete_message(i)
            st.rerun()

def add_one_message(message, i):
    ROLES = ["user", "assistant"]
    cols = st.columns([0.2, 0.70, 0.1])

    with cols[0]:
        st.session_state.messages[i]["role"] = st.selectbox(
            "角色",
            options=ROLES,
            key=f"role_{i}",
            index=ROLES.index(message["role"]),
        )

    with cols[1]:
        st.text_area(
            "content",
            value=message["content"],
            key=f"message_{i}",
            placeholder="请输入内容",
            on_change=update_message_content,
            args=(i,),
        )
        # 这里也可以不用on_change的方式，可以直接通过
        # st.session_state.messages[i]["content"] = st.session_state[f"message_{i}"]
        # 进行更简单的更新

    with cols[2]:
        if st.button("删除", key=f"delete_{i}"):
            delete_message(i)
            st.rerun()

# @st.fragment
def render_prompt_creation(pm):
    """Render prompt creation/update interface"""
    st.header("创建或更新 Prompt")
    prompts = pm.list_prompts()

    def render_prompt_name_input():
        col1, col2 = st.columns([1, 1])
        with col1:
            selected_prompt_name = st.selectbox("选择已有 Prompt 名称", ["<🆕 🪶 新建prompt>"] + prompts)
        with col2:
            if selected_prompt_name == "<🆕 🪶 新建prompt>":
                new_prompt_name = st.text_input("新建 Prompt 名称")
                messages = [
                    {"role": "system", "content": "你是一个有用的助手。"},
                    {"role": "user", "content": "{user_input}"},
                ]
                current_prompt_name = new_prompt_name
            else:
                new_prompt_name = ""
                messages = pm.get_prompt_messages(selected_prompt_name)
                current_prompt_name = selected_prompt_name
        if st.button(f"加载: {current_prompt_name}", use_container_width=True, icon="🔥"):
            st.session_state.messages = messages
        return selected_prompt_name, new_prompt_name

    def save_prompt_data(prompt_name, messages, tags, comment):
        if prompt_name and messages:
            tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
            if pm.save_prompt(prompt_name, messages, tags_list, comment):
                st.success(f"Prompt '{prompt_name}' 已保存!")
            else:
                st.info("内容未发生变化，无需保存新版本")
        else:
            st.error("请填写名称和消息内容!")

    selected_prompt_name, new_prompt_name = render_prompt_name_input()
    prompt_name = new_prompt_name.strip() if selected_prompt_name == "<🆕 🪶 新建prompt>" else selected_prompt_name
    print(st.session_state.messages)

    "---"
    # 系统消息输入
    st.subheader("Prompt构建")
    is_multimodal_prompt = st.toggle("多模态prompt", value=False)
    st.write("### messages")

    if not is_multimodal_prompt:
        st.session_state.messages[0]["content"] = st.text_area(
            "System Content",
            value=st.session_state.messages[0]["content"],
            key="system",
        )
        for i, message in enumerate(st.session_state.messages[1:], 1):
            add_one_message(message, i)

        # Add message button
        if st.button("添加角色消息", use_container_width=True):
            add_message()
            st.rerun()
    else:
        "---"
        "### 敬请期待"
        "---"
        st.session_state.messages[0]["content"] = st.text_area(
            "System Content",
            value=st.session_state.messages[0]["content"],
            key="system",
        )
        for i, message in enumerate(st.session_state.messages[1:], 1):
            add_one_multimodal_message(message, i)

        # Add message button
        if st.button("添加角色消息", use_container_width=True):
            add_message(multimodal=True)
            st.rerun()


    prompt_tags = st.text_input("标签 (用逗号分隔)", key="tags", value="v0.1,dev,效果优化")
    commit_comment = st.text_input("版本说明", placeholder="请输入版本说明", key="commit_comment")

    if st.button("保存该版本", use_container_width=True, icon="🔥"):
        save_prompt_data(prompt_name, st.session_state.messages, prompt_tags, commit_comment)


def render_prompt_delete(pm):
    """Render prompt deletion interface"""
    st.header("删除 Prompt")
    prompts = pm.list_prompts()
    selected_prompt = st.selectbox("选择要删除的 Prompt", prompts)
    print(selected_prompt)

    if pm.delete_prompt(selected_prompt):
        st.success(f"Prompt '{selected_prompt}' 已删除!")
    else:
        st.error(f"无法删除 Prompt '{selected_prompt}'")


def render_version_info(version, timestamp):
    """Render version information"""
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.text(f"版本: {version}")
    with col_info2:
        st.text(f"创建时间: {timestamp[:16]}")
    with col_info3:
        st.text(f"最后更新: {timestamp[:16]}")


def render_version_controls(pm, selected_prompt, selected_version, versions):
    """Render version control buttons and confirmation dialog"""
    col3, col4, col5 = st.columns([1, 1, 2])

    with col3:
        if st.button("设为当前版本"):
            if pm.restore_version(selected_prompt, selected_version["version"]):
                st.success(f"已将版本 {selected_version['version']} 设置为当前版本")

    with col4:
        if st.button("删除此版本"):
            if len(versions) > 1:
                st.session_state.show_delete_confirm = True
                st.session_state.version_to_delete = selected_version["version"]
            else:
                st.error("无法删除最后一个版本")
    # with col5:
    #     if st.button("删除prompt"):
    #         render_prompt_delete(pm)

    render_delete_confirmation(pm, selected_prompt)


def render_delete_confirmation(pm, selected_prompt):
    """Render delete confirmation dialog"""
    if st.session_state.show_delete_confirm:
        st.warning(f"确定要删除版本 {st.session_state.version_to_delete} 吗？此操作不可撤销。")
        col8, col9 = st.columns([1, 1])
        with col8:
            if st.button("确认删除"):
                if pm.delete_version(selected_prompt, st.session_state.version_to_delete):
                    st.success(f"已删除版本 {st.session_state.version_to_delete}")
                    st.session_state.show_delete_confirm = False
                    st.session_state.version_to_delete = None
                    st.rerun()
        with col9:
            if st.button("取消"):
                st.session_state.show_delete_confirm = False
                st.session_state.version_to_delete = None
                st.rerun()


def render_version_comparison(pm, selected_prompt, versions):
    """Render version comparison interface"""
    st.subheader("版本比较")
    col6, col7 = st.columns([1, 1])
    if len(versions) < 2:
        st.warning("至少需要两个版本才能进行比较")
    else:
        with col6:
            compare_version1 = st.selectbox(
                "选择比较版本 1",
                range(len(versions)),
                index=len(versions) - 2,
                format_func=lambda x: f"版本 {versions[x]['version']}",
            )
        with col7:
            compare_version2 = st.selectbox(
                "选择比较版本 2",
                range(len(versions)),
                index=len(versions) - 1,
                format_func=lambda x: f"版本 {versions[x]['version']}",
            )

        v1 = versions[compare_version1]["version"]
        v2 = versions[compare_version2]["version"]
        diff_html = pm.compare_versions(selected_prompt, v1, v2)
        if diff_html:
            render_diff_styles()
            st.components.v1.html(diff_html, height=500, scrolling=True)


def render_diff_styles():
    """Render CSS styles for diff display"""
    st.markdown("""
        <style>
            .diff_header {background-color: #e6e6e6;}
            .diff_next {background-color: #f8f9fa;}
            .diff_add {background-color: #e6ffe6;}
            .diff_sub {background-color: #ffe6e6;}
            .diff_chg {background-color: #e6e6ff;}
        </style>
    """, unsafe_allow_html=True)


def render_prompt_loading(pm):
    """Render prompt loading interface"""
    st.header("加载已有 Prompt")
    prompts = pm.list_prompts()

    if not prompts:
        st.info("还没有保存的 Prompt")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_prompt = st.selectbox("选择 Prompt", prompts)

    if selected_prompt:
        prompt_data, current_version = pm.load_prompt(selected_prompt)
        if prompt_data:
            versions = [v for v in prompt_data["versions"] if not v.get("deleted", False)]
            selected_version = render_version_selector(versions, col2)
            render_version_details(selected_version)
            render_version_info(selected_version["version"], prompt_data["created_at"])
            st.text("标签: " + ", ".join(prompt_data["tags"]))
            render_version_controls(pm, selected_prompt, selected_version, versions)
            render_version_comparison(pm, selected_prompt, versions)
            # 预览prompt
            if st.button("Prompt code 展示" ):
                messages = selected_version["messages"]
                st.code(f"{messages=}")
                st.write(messages)


def render_version_selector(versions, col):
    """Render version selection dropdown"""
    version_list = [f"版本 {v['version']}: {v['timestamp'][:16]}" for v in versions]
    with col:
        selected_version_idx = st.selectbox(
            "选择版本",
            range(len(version_list)),
            format_func=lambda x: version_list[x],
            index=len(version_list) - 1,
        )
    return versions[selected_version_idx]


def render_version_details(version):
    """Render version details and content"""
    with st.expander("版本说明", expanded=True):
        if version["comment"]:
            st.markdown(f"""
            **版本 {version['version']} 说明**:

            {version['comment']}

            *更新时间: {version['timestamp'][:16]}*
            """)
        else:
            st.info("该版本没有版本说明")

    messages = version["messages"]
    st.subheader("Messages")
    system_content = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
    st.chat_message(name="system").write(system_content)

    conversation_messages = [msg for msg in messages if msg["role"] != "system"]
    role_name_map = {
        "user": "U",
        "assistant": "A",
        "system": "S",
    }
    for i, msg in enumerate(conversation_messages):
        # st.chat_message(name=role_name_map[msg["role"]]).write(f"{msg['role']}:\n{msg['content']}")
        st.chat_message(name=msg["role"]).write(f"{msg['role']}: {msg['content']}")


def render_ai_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def render_ai_response(messages: list[dict], append_to_history=False):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        client: OpenAI = st.session_state.oai_client
        for response in client.chat.completions.create(
                model="Qwen2.5-7B",
                messages=messages,
                stream=True,
        ):
            full_response += response.choices[0].delta.content
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
        if append_to_history:
            st.session_state.messages.append({"role": "assistant", "content": full_response})


def render_debug_section():
    """Render debug section"""
    st.header("Prompt 调试区")

    if st.toggle("追加至prompt历史", value=False):
        if prompt := st.chat_input("测试输入"):
            render_ai_history()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            render_ai_response(st.session_state.messages, append_to_history=True)
    elif prompt := st.chat_input("测试输入"):
        render_ai_history()
        messages = [{"role": "user", "content": prompt}]
        with st.chat_message("user"):
            st.write(prompt)
        render_ai_response(st.session_state.messages + messages, append_to_history=False)


def main():
    st.title("Prompt 工程开发工具")
    init_session_state()
    pm = PromptManager()

    mode = render_sidebar()

    if mode == "创建或更新 Prompt":
        render_prompt_creation(pm)
        render_debug_section()
    elif mode == "加载已有 Prompt":
        render_prompt_loading(pm)
    else:
        st.header("敬请期待")
        st.write("todo")


if __name__ == "__main__":
    main()
