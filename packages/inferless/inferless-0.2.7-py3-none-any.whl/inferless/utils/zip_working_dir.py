import base64
import zipfile
from io import BytesIO
from pathlib import Path
import pathspec
import rich


def list_qualified_files(base_path, ignore_file):
    base_path = Path(base_path)
    files_data = {}
    total_size = 0

    if ignore_file:
        gitignore_path = Path(ignore_file)
    else:
        gitignore_path = Path(base_path) / '.gitignore'

    if gitignore_path.exists():
        lines = gitignore_path.read_text().splitlines()
        lines.append("\n.git")
    else:
        lines = ["\n.git\n", "*.pyc\n", "__pycache__\n", "venv\n"]

    spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
    all_files = list(base_path.rglob('*'))

    for file_path in all_files:
        if spec.match_file(str(file_path)) or not file_path.is_file():
            continue

        file_size = file_path.stat().st_size

        if total_size + file_size > 10 * 1024 * 1024:  # 10MB limit
            rich.print("[red]Total size of files exceeds 10MB limit[/red]")
            rich.print(f"[red]Please add more files to the ignore file to reduce the size[/red]")
            raise SystemExit

        with open(file_path, 'rb') as f:
            files_data[str(file_path.relative_to(base_path))] = f.read()

        total_size += file_size

    return files_data


def compress_files(files_data):
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for relative_path, file_data in files_data.items():
            zip_file.writestr(relative_path, file_data)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def get_working_dir_zip(base_path=".", ignore_file=None):
    try:
        files_data = list_qualified_files(base_path, ignore_file)
        return compress_files(files_data)
    except Exception as e:
        rich.print(f"[red]Failed to package the working directory[/red]")
        raise SystemExit

