import pdfplumber
import os

def convert_pdf_to_text(pdf_path: str) -> str:
    result = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(use_text_flow=True, keep_blank_chars=True)
            tables = page.find_tables()

            table_bboxes = [table.bbox for table in tables]
            table_midpoints = [(bbox[1] + bbox[3]) / 2 for bbox in table_bboxes]

            def is_inside_table(x0, top, x1, bottom):
                for bx in table_bboxes:
                    t_x0, t_top, t_x1, t_bottom = bx
                    if (x0 >= t_x0 and x1 <= t_x1 and top >= t_top and bottom <= t_bottom):
                        return True
                return False

            # Filter out words that are inside tables
            filtered_words = [
                word for word in words
                if not is_inside_table(word['x0'], word['top'], word['x1'], word['bottom'])
            ]

            # Group words into lines
            lines_by_y = {}
            for word in filtered_words:
                y = round(word['top'], 1)
                lines_by_y.setdefault(y, []).append(word)

            sorted_ys = sorted(lines_by_y.keys())

            # Build lines and place tables as they appear
            table_inserted = [False] * len(tables)
            for y in sorted_ys:
                line_words = sorted(lines_by_y[y], key=lambda w: w['x0'])
                text = ' '.join(word['text'] for word in line_words).rstrip()
                result.append(text)

                # After this line, check if a table should go here
                mid_y = y
                for idx, midpoint in enumerate(table_midpoints):
                    if not table_inserted[idx] and midpoint < y + 5:
                        ascii_table = format_table_as_ascii(tables[idx].extract())
                        result.append(ascii_table)
                        table_inserted[idx] = True

            # Append any remaining tables
            for idx, table in enumerate(tables):
                if not table_inserted[idx]:
                    ascii_table = format_table_as_ascii(table.extract())
                    result.append(ascii_table)

    # Clean up spacing: remove excessive empty lines
    cleaned_lines = []
    blank_count = 0
    for line in result:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 1:
                cleaned_lines.append("")
        else:
            blank_count = 0
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def format_table_as_ascii(table):
    if not table:
        return ""

    col_widths = [max(len(str(cell or '')) for cell in col) for col in zip(*table)]

    def make_row(cells, sep='|'):
        return sep + sep.join(f" {str(cell or '').ljust(width)} " for cell, width in zip(cells, col_widths)) + sep

    def make_separator():
        return '+' + '+'.join('-' * (width + 2) for width in col_widths) + '+'

    lines = [make_separator()]
    for row in table:
        lines.append(make_row(row))
        lines.append(make_separator())

    return '\n'.join(lines)
    
def process_pdf_task(queue):
    while True:
        # getting a task from queue
        pdf_path, result_future = queue.get()
        try:
            # trying to convert
            text = convert_pdf_to_text(pdf_path)
            result_future.set_result(text)
        except Exception as e:
            result_future.set_exception(e)
        finally:
            # marking a task done
            queue.task_done()