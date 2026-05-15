import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from empathy_engine.storage.interaction_store import InteractionStore


def main():
    store = InteractionStore()
    deleted = store.delete_all()
    print(f"deleted_records: {deleted}")


if __name__ == "__main__":
    main()
