import sys
import argparse
default_line_width_range = 67 # min=67, max=82

parg = argparse.ArgumentParser(description="Read",
    usage="""Info:
Use file by 'pdftotext pdf.pdf - | python merge_pdf_lines.py',
or 'python merge_pdf_lines.py' and then paste in the required text,
    then press ctrl+D to terminate the input and begin the conversion.""",)
parg.add_argument('-w', '--min-width',
    type=int, default=default_line_width_range,
    help="number of characters that is typically within a single line.",)
parg.add_argument('-s', '--sample-line',
    type=str, help = """a sample full-width line,
            provided so that the program can estimate the lower limit of the number of characters in a full line.""")

if __name__=="__main__":
    cl_arg = parg.parse_args()
    output = ""
    if cl_arg.sample_line:
        cl_arg.min_width = int(0.9 * len(cl_arg.sample_line))
        print(f"(--min-width has been reset to *{cl_arg.min_width}* for this session in accordance to --sample-line input.)")
    for line in sys.stdin.readlines():
        if len(line) > cl_arg.min_width:
            if line[-2] in "‒–-—-‐‑‧⁃﹣－" and line[-1]=="\n": # broken up word, joined to the next line.
                output += line[:-2]
            elif line[-2:] == ".\n": # actual end of line which just happens to be exactly this wide.
                output += line
                output += "\n"
            else: # full line, incomplete sentence.
                output += line.rstrip("\n") + " "

        else: # undefull lines.
            output += line # keep the \n at the end
            output += "\n"

    print("_"*cl_arg.min_width)
    print(output)