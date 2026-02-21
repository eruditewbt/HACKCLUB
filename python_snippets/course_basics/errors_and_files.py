from pathlib import Path


def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


out = Path("tmp_course_output.txt")
out.write_text("python fundamentals complete\n", encoding="utf-8")
print("safe_div(4,2)=", safe_div(4, 2))
print("safe_div(4,0)=", safe_div(4, 0))
print("wrote", out)
