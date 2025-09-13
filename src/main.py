from copy_files import copy_files
from generate_page import generate_pages_recursive


def main():
    print(f"\n\n====COPYING STATIC FILES====")
    copy_files("static", "public")
    print(f"\n\n====GENERATING PAGES====")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
