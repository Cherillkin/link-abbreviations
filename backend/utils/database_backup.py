from typing import Dict, Any

def database_backup(db_name: str, user: str, output_dir: str, host: str, port: int) -> Dict[str, Any]:
    import os
    import subprocess
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{db_name}_backup_{timestamp}.sql"
    output_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    try:
        pg_dump_path = "pg_dump"

        subprocess.run(
            [
                pg_dump_path,
                "-h", host,
                "-p", str(port),
                "-U", user,
                "-F", "c",
                "-f", output_path,
                db_name,
            ],
            env={**os.environ, "PGPASSWORD": os.getenv("POSTGRES_PASSWORD", "")},
            check=True
        )
        return {"status": "success", "path": output_path}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
    except FileNotFoundError:
        return {"status": "error", "message": "pg_dump not found. Install postgresql-client in container."}
