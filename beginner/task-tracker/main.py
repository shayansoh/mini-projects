import sys
import argparse
from task_tracker.cli import TaskCLI

def main():
    parser = argparse.ArgumentParser(prog="task-cli")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_p = subparsers.add_parser("add")
    add_p.add_argument("description")


    # update
    update_p = subparsers.add_parser("update")
    update_p.add_argument("id", type=int)
    update_p.add_argument("description")

    # delete
    delete_p = subparsers.add_parser("delete")
    delete_p.add_argument("id", type=int)

    # mark-in-progress
    mip = subparsers.add_parser("mark-in-progress")
    mip.add_argument("id", type=int)

    # mark-done
    md = subparsers.add_parser("mark-done")
    md.add_argument("id", type=int)

    # list
    list_p = subparsers.add_parser("list")
    list_p.add_argument("--status", choices=["todo", "in-progress", "done"])

    args = parser.parse_args()
    cli = TaskCLI()

    try:
        match args.command:
            case "add":                 cli.add(args.description) 
            case "update":              cli.update(args.id, args.description)
            case "delete":              cli.delete(args.id)
            case "mark-in-progress":    cli.mark_in_progress(args.id)
            case "mark-done":           cli.mark_done(args.id)
            case "list":                cli.list_tasks(args.status)
            case _:                     parser.print_help()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()