% FELLOWSHIP / ENGINEERING CAPSTONE REPORT CLASS
% PLEASE DO NOT MODIFY THIS FILE DIRECTLY.
% Version: 1.0
% Date: December 15, 2025
% Description: IEEE-compliant report class for Fusemachines AI Fellowship
%              capstone submissions, adapted from the Thapathali Campus
%              engineering-programs class with modern typography and
% IEEE-compliant report class for fellowship and engineering programs

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{at_fuse_aif}[2025/12/15 Fusemachines AI Fellowship report Class]

% CLASS OPTIONS
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrreprt}}
\ProcessOptions\relax

% Load base class with default options
\LoadClass[%
    fontsize=12pt,
    a4paper,
    oneside,
    captions=tableheading,
    listof=totoc,
    listof=flat,
    listof=nochaptergap,
    listof=entryprefix,
    bibliography=totoc,
    parskip=false  % Disable KOMA's paragraph spacing adjustments
]{scrreprt}

% ============================================================
% LANGUAGE SUPPORT (must be loaded early)
% ============================================================
\RequirePackage[english]{babel} % English language support - load before other packages

% ============================================================
% FONTS
% ============================================================
\RequirePackage[T1]{fontenc}    % Proper font encoding
\RequirePackage[utf8]{inputenc} % UTF-8 encoding
\RequirePackage{amsmath, amssymb, amsfonts} % Math symbols and fonts (load before newtxmath)
\RequirePackage{amsthm}

% Use Times fonts without the problematic figureversions package
\RequirePackage{times}          % Use standard Times font
\RequirePackage{newtxmath}      % Math font that matches Times for consistency

% Beautiful monospace font
% \RequirePackage{FiraMono}       % Modern, elegant monospace font with great readability
% Alternative options (comment/uncomment to switch):
% \RequirePackage{sourcecodepro}  % Adobe's elegant monospace
% \RequirePackage{inconsolata}    % Classic, highly readable
% \RequirePackage[scaled=0.95]{beramono}  % Clean, compact monospace

% ============================================================
% TYPOGRAPHY
% ============================================================
\RequirePackage[]{microtype} % Micro-typography (protrusion disabled to avoid LOA issues)
\RequirePackage[none]{hyphenat} % Disable hyphenation

\RequirePackage{xspace}

% ============================================================
% PAGE GEOMETRY
% ============================================================
\RequirePackage[a4paper, left=1.5in, right=1in, top=1in, bottom=1in]{geometry}
\setlength{\footskip}{0.5in} % Footer margin

% ============================================================
% COLORS
% ============================================================
\RequirePackage{xcolor}         % Color support
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.2,0.2,0.2}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

% ============================================================
% VISUAL ELEMENTS
% ============================================================
\RequirePackage{graphicx}       % Include images
\RequirePackage{cite}
\RequirePackage{caption}        % Caption formatting
\RequirePackage{subcaption}     % Subfigures

% ============================================================
% CAPTION FORMATTING
% ============================================================
\captionsetup{labelsep=space}
\renewcommand{\listoflofentryname}{Figure}
\renewcommand{\listoflotentryname}{Table}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{tabularx}
\RequirePackage{multirow}
\RequirePackage{listings}
\RequirePackage{siunitx}
\RequirePackage{float}
\RequirePackage{pdfpages}       % For including PDF pages
\RequirePackage{lscape}
\RequirePackage{adjustbox}
\RequirePackage{rotating}       % For rotating tables, figures
\RequirePackage{lipsum}         % Dummy text generation
\RequirePackage{csvsimple}
\RequirePackage{datetime2}      % For date management
\RequirePackage{textcase}       % For managing text-cases
\RequirePackage{multicol}       % For multi-column use
\RequirePackage[subpreambles=true]{standalone}     % Standalone figures use their own preambles

% LISTS
\RequirePackage{enumitem}
\setlist[itemize]{topsep=3pt,itemsep=0pt,parsep=2pt,leftmargin=*}
\setlist[enumerate]{topsep=3pt,itemsep=0pt,parsep=2pt,leftmargin=*}
\setlist[description]{topsep=3pt,itemsep=0pt,parsep=2pt}

% ============================================================
% KOMA-SCRIPT
% ============================================================
\RequirePackage{scrlayer-scrpage} % Recommended for KOMA-Script

% ============================================================
% ALGORITHMS
% ============================================================
\RequirePackage{algorithm}      % Algorithm floats
\RequirePackage{algpseudocode}  % Pseudocode formatting
\RequirePackage{algorithmicx}   % Algorithm constructs
\RequirePackage{scrhack}

% ============================================================
% SPACING AND PARAGRAPH FORMATTING
% ============================================================
% Must load AFTER scrhack (which loads setspaceenhanced)
\RequirePackage{setspace}       % Line spacing control
\onehalfspacing             % 1.5 line spacing
\setparsizes{0pt}{10pt}{0pt plus 1fil} % Paragraph spacing

% Override KOMA-Script's automatic single spacing in TOC, LOF, LOT
\AfterTOCHead{\onehalfspacing}
\AfterStartingTOC{\onehalfspacing}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}

\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{note}[theorem]{Note}

% GLOSSARIES
\RequirePackage[acronym,symbols,nomain,nonumberlist,nopostdot,translate=false,nogroupskip,toc]{glossaries}
\makeglossaries

% Custom glossary style with uniform spacing
\newglossarystyle{uniformlist}{%
    \setglossarystyle{long}% base this style on the long style
    \renewenvironment{theglossary}%
    {\renewcommand{\arraystretch}{1.3}%
        \begin{longtable}{@{}p{0.15\textwidth}p{0.75\textwidth}@{}}}%
            {\end{longtable}}%
    \renewcommand*{\glossaryheader}{}%
    \renewcommand*{\glsgroupheading}[1]{}%
    \renewcommand*{\glsgroupskip}{}%
    \renewcommand{\glossentry}[2]{%
        \glsentryitem{##1}\glstarget{##1}{\glossentryname{##1}} &
        \glossentrydesc{##1}\tabularnewline[2pt]
    }%
    \renewcommand*{\subglossentry}[3]{%
        & \glssubentryitem{##2}%
        \glstarget{##2}{\strut}\glossentrydesc{##2}\tabularnewline[2pt]
    }%
}

% Set the style for acronyms
\setglossarystyle{uniformlist}

% HYPERREF (load late in package chain)
% Use hidelinks option to hide link borders (can be overridden in document)
\RequirePackage{url}
\RequirePackage[hidelinks]{hyperref}
\hypersetup{
    colorlinks=false,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue,
    filecolor=black,
    anchorcolor=black,
    menucolor=black,
    runcolor=black,
    bookmarksnumbered=true,
    pdfstartview={FitH},
    breaklinks=true,
    pdftitle={Fusemachines AI Fellowship Report},
    pdfauthor={},
    pdfsubject={Engineering report},
    pdfkeywords={LaTeX, IEEE, report, engineering}
}
\urlstyle{tt}

% CLEVEREF (load after hyperref)
\RequirePackage[capitalize,noabbrev,nameinlink]{cleveref}

% IEEE-style cleveref configuration
\crefname{figure}{Fig.}{Figs.}
\Crefname{figure}{Figure}{Figures}
\crefname{table}{Table}{Tables}
\Crefname{table}{Table}{Tables}
\crefname{equation}{Eq.}{Eqs.}
\Crefname{equation}{Equation}{Equations}
\crefname{section}{Section}{Sections}
\Crefname{section}{Section}{Sections}
\crefname{chapter}{Chapter}{Chapters}
\Crefname{chapter}{Chapter}{Chapters}
\crefname{algorithm}{Algorithm}{Algorithms}
\Crefname{algorithm}{Algorithm}{Algorithms}

% IEEE FORMATTING SETTINGS
% Math preferences
\allowdisplaybreaks[4]
\interdisplaylinepenalty=2500

% ============================================================
% TABLE OF CONTENTS STYLING
% ============================================================
\setkomafont{chapterentry}{\normalfont\bfseries}
\setkomafont{chapterentrydots}{\normalfont\bfseries}
\KOMAoptions{chapterentrydots=true}
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{2}

% ============================================================
% TYPESETTING
% ============================================================
\sloppy % Justify text
\hbadness=10000

% Prevent widows and orphans
\clubpenalty = 100000       % Paragraph does not start on the last line of a page
\widowpenalty = 100000      % Paragraph does not end on the first line of a page
\displaywidowpenalty = 100000 % Paragraph does not end on the first line of a page

% ============================================================
% PAGE NUMBERING
% ============================================================
\cfoot{\pagemark} % Center the page number

% Bibliography heading
\renewcommand{\bibname}{REFERENCES}

% List title renaming (IEEE uppercase style)
\renewcommand{\contentsname}{TABLE OF CONTENTS}
\renewcommand{\listfigurename}{LIST OF FIGURES}
\renewcommand{\listtablename}{LIST OF TABLES}
\renewcommand{\listalgorithmname}{LIST OF ALGORITHMS}

% Table formatting - IEEE style with booktabs
\setlength{\heavyrulewidth}{0.08em}
\setlength{\lightrulewidth}{0.05em}
\setlength{\aboverulesep}{0.4ex}
\setlength{\belowrulesep}{0.4ex}
% Note: \tabcolsep uses LaTeX default (6pt) for automatic column spacing

% ============================================================
% HEADING STYLES (Fusemachines AI Fellowship Theme)
% ============================================================
\setkomafont{chapter}{\normalfont \bfseries \MakeUppercase}
\setkomafont{section}{\normalfont\bfseries}
\setkomafont{subsection}{\normalfont\bfseries}
\setkomafont{subsubsection}{\normalfont\bfseries}
\setkomafont{paragraph}{\normalfont\bfseries}
\setkomafont{subparagraph}{\normalfont\bfseries}

% ============================================================
% SECTION SPACING
% ============================================================
\RedeclareSectionCommand[beforeskip=0sp,afterskip=1sp plus 12pt]{chapter}
\RedeclareSectionCommand[beforeskip=0sp,afterskip=1sp plus 10pt]{section}
\RedeclareSectionCommand[beforeskip=0sp,afterskip=1sp plus 8pt]{subsection}
\RedeclareSectionCommand[beforeskip=0sp,afterskip=1sp plus 6pt]{subsubsection}
\RedeclareSectionCommand[beforeskip=0sp,afterskip=1sp plus 18pt]{paragraph}

% ============================================================
% NUMBERING FORMATS
% ============================================================
\renewcommand\thefigure{\thechapter-\arabic{figure}}
\renewcommand\thetable{\thechapter-\arabic{table}}
\renewcommand{\theequation}{\thechapter-\arabic{equation}}

% ============================================================
% CODE LISTING STYLE
% ============================================================
\lstset{
    language=Python,
    breaklines=true,
    breakautoindent=true,
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
    breakatwhitespace=true,
    basicstyle=\ttfamily\scriptsize\color{black},  % \ttfamily now uses Fira Mono
    keywordstyle=\color{black}\bfseries,
    commentstyle=\color{black}\itshape,
    stringstyle=\color{black},
    captionpos=b,
    frame=shadowbox,
    rulesepcolor=\color{black},
    showstringspaces=false,
    tabsize=4,
    numbers=left,
    numberstyle=\tiny\color{black},
    numbersep=5pt,
    backgroundcolor=\color{backcolour},
    xleftmargin=15pt,
    xrightmargin=15pt
}

% CUSTOM COMMANDS
% =============================================================================
% CROSS-REFERENCING: Use cleveref package (\cref and \Cref)
% =============================================================================
% Instead of manual \ref, use \cref{label} or \Cref{label} for automatic
% formatting with proper names and hyperlinks.
%
% LABEL NAMING CONVENTIONS:
%   \label{fig:name}   - for figures
%   \label{tab:name}   - for tables
%   \label{eq:name}    - for equations
%   \label{alg:name}   - for algorithms
%   \label{sec:name}   - for sections
%   \label{chap:name}  - for chapters
%
% USAGE EXAMPLES:
%   \cref{fig:architecture}     → "Fig. 1"
%   \Cref{fig:architecture}     → "Figure 1"
%   \cref{tab:results,eq:loss}  → "Table 1 and Eq. 2"
%   \cref{sec:method}           → "Section 3"
% =============================================================================

% Math operators
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}

% IEEE notation helpers
\newcommand{\set}[1]{\mathcal{#1}}
\newcommand{\vect}[1]{\mathbf{#1}}
\newcommand{\matr}[1]{\mathbf{#1}}

% IEEE abbreviations
\newcommand{\ie}{i.e.,\xspace}
\newcommand{\eg}{e.g.,\xspace}
\newcommand{\etc}{etc.\xspace}
\newcommand{\etal}{et~al.\xspace}
\newcommand{\vs}{vs.\xspace}

% Path helpers
\newcommand{\vectorpath}{src/images/diagrams}
\newcommand{\imgpath}{src/images/figures}

% DYNAMIC AUTHOR MANAGEMENT (1-4 authors supported)
% Supports 1, 2, 3, or 4 authors automatically
% Define only what you need in vars.tex, leave others empty
% Author I is required (minimum 1 author), II/III/IV are optional

\newcommand{\cSubmittedI}{}
\newcommand{\cSubmittedII}{}
\newcommand{\cSubmittedIII}{}
\newcommand{\cSubmittedIV}{}
\newcommand{\cSubmittedIRoll}{}
\newcommand{\cSubmittedIIRoll}{}
\newcommand{\cSubmittedIIIRoll}{}
\newcommand{\cSubmittedIVRoll}{}

% Dynamic author table - centered, one name (with optional roll) per line
\newcommand{\authorTable}{%
    \begin{center}
        \cSubmittedI\ifx\cSubmittedIRoll\@empty\else\ ~~\cSubmittedIRoll\fi\\
        \ifx\cSubmittedII\@empty\else
        \cSubmittedII\ifx\cSubmittedIIRoll\@empty\else\ ~~\cSubmittedIIRoll\fi\\
        \fi
        \ifx\cSubmittedIII\@empty\else
        \cSubmittedIII\ifx\cSubmittedIIIRoll\@empty\else\ ~~\cSubmittedIIIRoll\fi\\
        \fi
        \ifx\cSubmittedIV\@empty\else
        \cSubmittedIV\ifx\cSubmittedIVRoll\@empty\else\ ~~\cSubmittedIVRoll\fi\\
        \fi
    \end{center}%
}

% Dynamic comma-separated author list
\newcommand{\authorList}{%
    \cSubmittedI%
    \ifx\cSubmittedII\@empty\else, \cSubmittedII\fi%
    \ifx\cSubmittedIII\@empty\else, \cSubmittedIII\fi%
    \ifx\cSubmittedIV\@empty\else, \cSubmittedIV\fi%
}


\endinput
