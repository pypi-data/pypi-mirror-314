DEFAULT_SPACING = 40
PROMPT_GENERATE_COMMIT_MESSAGE = "Generate a commit message based on this git diff with the \
    conventional commits standard: \
    https://www.conventionalcommits.org/en/v1.0.0. \
    Only give me the commit message as I will copy-paste your answer directly into the commit message. \
    A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., fix(parser).\
    The scope should not be a filename. \
    Prefer a fix (or other like refactor etc) over a feat. Unless its adding a feature, then its not a feat. \
    I want to prevent bumping minor and major versions as much as possible, however a \
    feature is a feature and should be treated as such. \
    I only want one commit message. \
    \n\
    The first line in the commit message should not exceed 72 characters. \
    Another best practice to help you write good Git commit messages is to use imperative verb form. \
    Using imperative verb form ensures that potential verbs used in your commit messages, like “fixed” \
    or “updated” are written in the correct tense to “fix” and “updated”.  \
    \n\
    Some examples (but not limited to): \n\
    1:\n\
    feat: allow provided config object to extend other configs\n\
    \n\
    BREAKING CHANGE: `extends` key in config file is now used for extending other config files\n\
    \n\
    2:\n\
    docs: correct spelling of CHANGELOG\n\
    3:\n\
    fix: prevent racing of requests\n\
    \n\
    Introduce a request id and a reference to latest request. Dismiss\n\
    incoming responses other than from latest request.\n\
    \n\
    Remove timeouts which were used to mitigate the racing issue but are\n\
    obsolete now.\n\
    \n\
    4:\n\
    chore!: drop support for Node 6\n\
    \n\
    BREAKING CHANGE: use JavaScript features not available in Node 6.\n\
    \n\
    "

PROMPT_GENERATE_COMMIT_MESSAGE_HELP = (
    "Prompt to AI model. Context (git diff and/or others) will be added as well."
)

PROMPT_EXTRA_PROMPT_HELP = "Extra prompt in addition to the regular prompt and context added by the tool. \
        Will be added after regular prompt, before context."

OPTION_NO_ADD_HELP = "If set skips the step where running git add DIRECTORY.\n"

OPTION_GIT_DIRECTORY_HELP = (
    "Path to git repoistory, can be a subdir in repoistory as well."
)
