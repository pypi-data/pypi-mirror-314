import datetime
import json
from difflib import HtmlDiff
from pathlib import Path

import diff_match_patch as dmp_module


class PromptManager:
    def __init__(self):
        self.save_path = Path("prompts")
        self.save_path.mkdir(exist_ok=True)
        self.dmp = dmp_module.diff_match_patch()

    def save_prompt(self, name, messages, tags=None, comment=""):
        file_path = self.save_path / f"{name}.json"

        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                prompt_data = json.load(f)
            # 比较新旧版本是否相同
            if prompt_data["versions"][-1]["messages"] == messages:
                return False
            new_version = len(prompt_data["versions"])
        else:
            prompt_data = {
                "name": name,
                "tags": tags or [],
                "created_at": datetime.datetime.now().isoformat(),
                "versions": [],
            }
            new_version = 0

        version_data = {
            "version": new_version,
            "messages": messages,
            "timestamp": datetime.datetime.now().isoformat(),
            "comment": comment,
            "deleted": False,
        }

        if new_version > 0:
            prev_messages = prompt_data["versions"][-1]["messages"]
            # 将消息列表转换为字符串以计算差异
            prev_str = json.dumps(prev_messages, ensure_ascii=False)
            curr_str = json.dumps(messages, ensure_ascii=False)
            patches = self.dmp.patch_make(prev_str, curr_str)
            version_data["diff"] = self.dmp.patch_toText(patches)

        prompt_data["versions"].append(version_data)
        prompt_data["updated_at"] = datetime.datetime.now().isoformat()
        prompt_data["current_version"] = new_version

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=2)
        return True

    def delete_prompt(self, name):
        print(f"Deleting prompt: {name}")
        file_path = self.save_path / f"{name}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def delete_version(self, name, version):
        file_path = self.save_path / f"{name}.json"
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            if 0 <= version < len(data["versions"]):
                data["versions"][version]["deleted"] = True

                if data["current_version"] == version:
                    # 找到最新的未删除版本
                    for i in range(len(data["versions"]) - 1, -1, -1):
                        if not data["versions"][i]["deleted"]:
                            data["current_version"] = i
                            break

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        return False

    def restore_version(self, name, version):
        data, _ = self.load_prompt(name)
        if data and 0 <= version < len(data["versions"]):
            data["current_version"] = version
            file_path = self.save_path / f"{name}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False

    def compare_versions(self, name, version1, version2):
        data, _ = self.load_prompt(name)
        if data and version1 < len(data["versions"]) and version2 < len(data["versions"]):
            # 将消息列表转换为格式化的字符串进行比较
            messages1 = data["versions"][version1]["messages"]
            messages2 = data["versions"][version2]["messages"]

            content1 = json.dumps(messages1, ensure_ascii=False, indent=2)
            content2 = json.dumps(messages2, ensure_ascii=False, indent=2)

            diff = HtmlDiff()
            diff_html = diff.make_file(
                content1.splitlines(),
                content2.splitlines(),
                f"版本 {version1}",
                f"版本 {version2}",
                True,
            )
            return diff_html
        return None

    def load_prompt(self, name, version=None):
        file_path = self.save_path / f"{name}.json"
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                if version is None:
                    version = data["current_version"]
                return data, version
        return None, None

    def list_prompts(self):
        return [f.stem for f in self.save_path.glob("*.json")]

    def get_prompt_messages(self, name, version=None):
        """获取指定版本的messages内容"""
        data, current_version = self.load_prompt(name)
        if data:
            version = version if version is not None else current_version
            if 0 <= version < len(data["versions"]):
                return data["versions"][version]["messages"]
        return None

    def get_system_message(self, name, version=None):
        """获取system message"""
        messages = self.get_prompt_messages(name, version)
        if messages:
            for msg in messages:
                if msg["role"] == "system":
                    return msg["content"]
        return ""

    def get_conversation_messages(self, name, version=None):
        """获取对话消息(除system message外)"""
        messages = self.get_prompt_messages(name, version)
        if messages:
            return [msg for msg in messages if msg["role"] != "system"]
        return []
