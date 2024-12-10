import fitz


def count_pages_in_pdf(pdf_file_path):
    try:
        with fitz.open(pdf_file_path) as f:
            return f.page_count
    except (FileNotFoundError, IOError) as e:
        print(f"Không thể đọc file {pdf_file_path}: {e}")
    except Exception as e:
        print(f"Có lỗi xảy ra với file {pdf_file_path}: {e}")
    return 0

