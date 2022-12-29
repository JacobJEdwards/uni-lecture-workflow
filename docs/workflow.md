---
_title: 'test'
_date: '20-28'
---

# University Scripting Workflow

I am going to create a semi-automated lecture and file organiser.
\
\
This will be used to generate my file structure for each module, and generate a **master.tex** file that will include the two most recent lecture notes.
\
\
Additionally, there will be an option to generate a complete pdf of all my lecture notes for one module.
\
\
Finally, it will symlink the current or most recent module to the current course directory.
\
\
Python and possibly shell script will be used for this process.
\
\
I may need to use cron to schedule events.

## Processes:
- Add lectures, any directories, compiled lectures, master.tex and preamble.tex to each module directory.
- Change output directory of compiled tex docs.
- Update each master.tex with the two most recent lecture notes.
- Option to compile master.tex with all the lecture notes.
- Update current module with the current module for ease of access - look into calendar API or use the day.
- Change working path based on date.
- Automatically symlink year long courses from semesters into year long directory.

## TODO
- Add latex files to directories
- Exclude master.tex from year long directory
- Add preambles
- Add master.tex to lectures
- Automatically change master.tex files
- Option to compile big master.tex
- Change tex output directory
- Path.suffix may be useful for dealing with tex files
- incorporate tex functions incase i choose to use tex still

## Alterations to the original spec
- I may take notes in markdown instead of latex
- Use github pages to host these markdown pages, in combination with jekyll
- Maybe do current module inside of lectures class
- And year long inside lectures class? Or as a module class function

# Adding markdown notes to LaTeX doc -> 
\usepackage{markdown}
\begin{document}
\markdownInput{lec1.md}
\end{document}

- Then run this command:
latexmk -cd -lualatex -silent path/master.tex
