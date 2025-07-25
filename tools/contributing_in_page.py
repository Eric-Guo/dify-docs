import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_contributing_section(
    repo_owner, repo_name, target_dir_relative, filename, language
):
    repo_url = f"https://github.com/{repo_owner}/{repo_name}"
    report_issue_url = "https://github.com/langgenius/dify-docs/issues/new?template=docs.yml"
    if language == "zh":
        contributing_section = f"""
{{/*
Contributing Section
DO NOT edit this section!
It will be automatically generated by the script.
*/}}

---

[编辑此页面]({repo_url}/edit/main/{target_dir_relative}/{filename}) | [提交问题]({report_issue_url})

"""
    elif language == "en":
        contributing_section = f"""
{{/*
Contributing Section
DO NOT edit this section!
It will be automatically generated by the script.
*/}}

---

[Edit this page]({repo_url}/edit/main/{target_dir_relative}/{filename}) | [Report an issue]({report_issue_url})

"""
    elif language == "ja":
        contributing_section = f"""
{{/*
Contributing Section
DO NOT edit this section!
It will be automatically generated by the script.
*/}}

---

[このページを編集する]({repo_url}/edit/main/{target_dir_relative}/{filename}) | [問題を報告する]({report_issue_url})

"""
    else:
        raise ValueError(
            "Unsupported language. Supported languages are 'zh', 'en', and 'ja'."
        )

    return contributing_section


def append_content_to_files(
    target_dir_relative,
    repo_owner,
    repo_name,
    language,
    base_dir=BASE_DIR,
    file_extension=".mdx",
):
    target_path = os.path.join(base_dir, target_dir_relative)

    if not os.path.isdir(target_path):
        print(f"Error: Directory '{target_path}' not found.")
        return
    fix_md_endings(target_dir_relative, base_dir, file_extension)
    appended_count = 0
    error_count = 0
    for root, dirs, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                current_dir_relative = os.path.relpath(root, base_dir)
                try:
                    # Check if contributing section already exists
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Only append if contributing section doesn't exist
                    if "Contributing Section" not in content:
                        with open(filepath, "a", encoding="utf-8") as f:
                            f.write(
                                generate_contributing_section(
                                    repo_owner,
                                    repo_name,
                                    current_dir_relative,
                                    filename,
                                    language,
                                )
                            )
                        appended_count += 1
                except (IOError, OSError) as e:
                    print(f"Error processing file {filepath}: {e}")
                    error_count += 1
    print(
        f"Finished processing directory tree starting at '{target_path}'. "
        f"Appended to {appended_count} files. Encountered {error_count} errors."
    )


def remove_contributing_section(
    target_dir_relative, base_dir=BASE_DIR, file_extension=".mdx"
):
    target_path = os.path.join(base_dir, target_dir_relative)
    if not os.path.isdir(target_path):
        print(f"Error: Directory '{target_path}' not found.")
        return
    removed_count = 0
    error_count = 0
    for root, dirs, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Match the contributing section from comment start to the end of the links
                    pattern = re.compile(
                        r"\{\/\*\s*Contributing Section[\s\S]*?\*\/\}[\s\S]*?---[\s\S]*?\[[^\]]*\]\([^\)]*\)\s*\|\s*\[[^\]]*\]\([^\)]*\)\s*",
                        re.DOTALL,
                    )
                    new_content = re.sub(pattern, "", content)
                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        removed_count += 1
                except (IOError, OSError) as e:
                    print(f"Error processing file {filepath}: {e}")
                    error_count += 1
    fix_md_endings(target_dir_relative, base_dir, file_extension)
    print(
        f"Finished processing directory tree starting at '{target_path}'. "
        f"Removed from {removed_count} files. Encountered {error_count} errors."
    )


def fix_md_endings(target_dir_relative, base_dir=BASE_DIR, file_extension=".mdx"):
    target_path = os.path.join(base_dir, target_dir_relative)
    if not os.path.isdir(target_path):
        print(f"Error: Directory '{target_path}' not found.")
        return
    fixed_count = 0
    error_count = 0
    for root, dirs, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    processed_content = content.replace("\r\n", "\n")
                    processed_content = processed_content.rstrip()
                    processed_content += "\n"
                    if processed_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(processed_content)
                        fixed_count += 1
                except (IOError, OSError) as e:
                    print(f"Error processing file {filepath}: {e}")
                    error_count += 1
    print(
        f"Finished processing directory tree starting at '{target_path}'. "
        f"Fixed line endings and trailing lines in {fixed_count} files. Encountered {error_count} errors."
    )


def refresh(
    target_dir_relative,
    repo_owner,
    repo_name,
    language,
    base_dir=BASE_DIR,
    file_extension=".mdx",
):
    remove_contributing_section(target_dir_relative, base_dir, file_extension)
    append_content_to_files(
        target_dir_relative, repo_owner, repo_name, language, base_dir, file_extension
    )


def loop(dict):
    for config_name, config_data in dict.items():
        refresh(
            target_dir_relative=config_data["target_dir_relative"],
            repo_owner=config_data["repo_owner"],
            repo_name=config_data["repo_name"],
            language=config_data["language"],
        )


def main_contributing_in_page():
    process = {
        # Help Documentation
        "zh_help": {
            "target_dir_relative": "zh-hans",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "zh",
        },
        "en_help": {
            "target_dir_relative": "en",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "en",
        },
        "ja_help": {
            "target_dir_relative": "ja-jp",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "ja",
        },
        # Plugin Development
        "zh_plugin_dev": {
            "target_dir_relative": "plugin-dev-zh",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "zh",
        },
        "en_plugin_dev": {
            "target_dir_relative": "plugin-dev-en",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "en",
        },
        "ja_plugin_dev": {
            "target_dir_relative": "plugin-dev-ja",
            "repo_owner": "langgenius",
            "repo_name": "dify-docs",
            "language": "ja"
        },
    }
    try:
        loop(process)
        return "success"
    except Exception as e:
        return (f"{str(e)}")
    
if __name__ == "__main__":
    result_message = main_contributing_in_page()
    print("\n--- Script Execution Result ---")
    print(result_message)
