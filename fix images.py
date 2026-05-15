import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kotopy.settings')
django.setup()

from books.models import Book

def fix_image_paths():
    books = Book.objects.all()
    count = 0
    for book in books:
        if book.image:
            old_path = book.image.path
            filename = os.path.basename(old_path)
            if ' ' in filename:
                new_filename = filename.replace(' ', '_')
                new_path = os.path.join(os.path.dirname(old_path), new_filename)
                
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"File renamed: {filename} -> {new_filename}")
                else:
                    print(f"File not found on disk: {old_path}")
                
                relative_dir = os.path.dirname(book.image.name)
                book.image.name = os.path.join(relative_dir, new_filename).replace('\\', '/')
                book.save()
                count += 1
                print(f"Database updated for book ID {book.id}: {book.image.name}")

    print(f"Total fixed: {count}")

fix_image_paths()
