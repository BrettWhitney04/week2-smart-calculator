# Copilot Experience Report

## What Worked Well
1. **Fast Math Logic:** Writing the comments let Copilot quickly generate the standard `if/elif` blocks for `basic_calculate()`.
2. **Menu Boilerplate:** It set up the `while True` loop and the structure for the five menu options in `main()` without needing to type it all out.
3. **Loop Stepping:** It suggested `[i * 0.1 for i in range(...)]`, which was a quick way to handle stepping by 0.1 since Python's standard `range()` only takes integers.

## Challenges
1. **Formatting Glitches:** When generating the menu, Copilot split a print statement across multiple lines and left a stray `1.` that caused a syntax error until I cleaned it up.
2. **Float Precision:** Python displayed numbers like `0.30000000000000004` during the search loop, so I had to make sure the output was rounded to look clean.
3. **Generic Answers:** For Option 4, Copilot gave a basic one-sentence dictionary definition of search instead of explaining brute force and why it is slow.

## My Judgement (What I Rejected / Changed)
* **What it suggested:** In `solve_for_x()`, Copilot suggested directly replacing `x` with the raw string: `eval(expression.replace('x', str(x)))`.
* **What was wrong with it:** If `x` is negative, plugging it straight into certain math expressions without parentheses can cause parsing issues or syntax errors in Python.
* **What I did instead:** Wrapped `x` inside parentheses (`f"({x})"`) so negative numbers evaluate cleanly without breaking `eval()`.