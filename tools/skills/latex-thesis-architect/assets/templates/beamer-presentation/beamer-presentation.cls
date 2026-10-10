\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{beamer-presentation}[Academic Beamer Presentation Template]

% Base class
\LoadClass[aspectratio=169]{beamer}

% Completely plain theme
\usetheme{default}
\usecolortheme{default}

% Required Packages
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{helvet}  % Helvetica (sans-serif) font
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage{graphicx}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{booktabs}
\RequirePackage{tikz}
\RequirePackage{listings}
\RequirePackage{hyperref}

% Legacy color names (kept for backward compatibility)
\definecolor{Engineering FacultyRed}{RGB}{165,30,55}
\definecolor{Engineering FacultyBlue}{RGB}{0,51,102}

% Pure black-on-white for everything
\setbeamercolor{structure}{fg=black}
\setbeamercolor{frametitle}{fg=black,bg=white}
\setbeamercolor{title}{fg=black}
\setbeamercolor{normal text}{fg=black,bg=white}
\setbeamercolor{block title}{fg=black,bg=black!8}
\setbeamercolor{block body}{bg=black!3}
\setbeamercolor{item}{fg=black}
\setbeamercolor{itemize item}{fg=black}
\setbeamercolor{itemize subitem}{fg=black}
\setbeamercolor{enumerate item}{fg=black}

% Large bold font for frame titles, centered
\setbeamerfont{frametitle}{series=\bfseries,size=\LARGE}
\setbeamertemplate{frametitle}{
    \vspace{0.5cm}
    \begin{center}
        \insertframetitle
    \end{center}
}

% Filled circle bullets (matching the reference)
\setbeamertemplate{itemize item}{\large\textbullet}
\setbeamertemplate{itemize subitem}{\textbullet}

% No header
\setbeamertemplate{headline}{}

% Remove all frame decorations (lines at top/bottom of frames)
\setbeamertemplate{frame begin}{}
\setbeamertemplate{frame end}{}
\setbeamercolor{upper separation line head}{bg=white}
\setbeamercolor{lower separation line head}{bg=white}
\setbeamercolor{upper separation line foot}{bg=white}
\setbeamercolor{lower separation line foot}{bg=white}

% Remove TOC section circles/balls
\setbeamertemplate{section in toc}{\inserttocsectionnumber.~\inserttocsection\par}

% ============================================
% CUSTOMIZABLE VARIABLES
% ============================================
\newcommand{\projecttitle}[1]{\def\@projecttitle{#1}}
\newcommand{\projectsubtitle}[1]{\def\@projectsubtitle{#1}}
\newcommand{\presentername}[1]{\def\@presentername{#1}}
\newcommand{\studentroll}[1]{\def\@studentroll{#1}}
\newcommand{\supervisorname}[1]{\def\@supervisorname{#1}}
\newcommand{\supervisortitle}[1]{\def\@supervisortitle{#1}}
\newcommand{\departmentname}[1]{\def\@departmentname{#1}}
\newcommand{\institutionname}[1]{\def\@institutionname{#1}}
\newcommand{\presentationdate}[1]{\def\@presentationdate{#1}}
\newcommand{\academicyear}[1]{\def\@academicyear{#1}}

% Default values
\projecttitle{Your Project Title Here}
\projectsubtitle{A Brief Subtitle of Your Project}
\presentername{Student Name}
\studentroll{Roll Number: 075/BCT/XXX}
\supervisorname{Dr. Supervisor Name}
\supervisortitle{Associate Professor}
\departmentname{Department of Engineering}
\institutionname{Faculty of Engineering, Campus / Institution}
\presentationdate{\today}
\academicyear{Academic Year: 2024/2025}

% ============================================
% Public getters
% ============================================
\newcommand{\ProjectTitle}{\@projecttitle}
\newcommand{\ProjectSubtitle}{\@projectsubtitle}
\newcommand{\PresenterName}{\@presentername}
\newcommand{\StudentRoll}{\@studentroll}
\newcommand{\SupervisorName}{\@supervisorname}
\newcommand{\SupervisorTitle}{\@supervisortitle}
\newcommand{\DepartmentName}{\@departmentname}
\newcommand{\InstitutionName}{\@institutionname}
\newcommand{\PresentationDate}{\@presentationdate}
\newcommand{\AcademicYear}{\@academicyear}

% Footer: light gray date on left, page number on right (matching reference)
\setbeamertemplate{footline}{
    \leavevmode%
    \hbox{%
        \begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1ex,left]{author in head/foot}%
            \hspace*{1em}{\color{black!40}\footnotesize \PresentationDate}%
        \end{beamercolorbox}%
        \begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1ex,right]{date in head/foot}%
            {\color{black!40}\footnotesize \insertframenumber}\hspace*{1em}%
        \end{beamercolorbox}%
    }%
    \vskip0pt%
}

% Hide navigation symbols
\setbeamertemplate{navigation symbols}{}

\endinput