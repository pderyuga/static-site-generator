from copy_files import copy_files
from generate_page import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 0:
        basepath = sys.argv[0]

    print(f"\n\n====COPYING STATIC FILES====")
    copy_files("static", "docs")
    print(f"\n\n====GENERATING PAGES====")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
