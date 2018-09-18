# Redirect checker for Docs Italia

This tool can be used to check that a document published on readthedocs is
properly redirecting to Docs Italia.

## Preconditions

In order to use this tool you need:

- A document published on readthedocs (optionally versioned) [original document]
  A copy of the first document where each page redirects to Docs Italia
  [redirect document]

## Usage

- Clone this repo
- Install python requirements: `pip install -r requirements.txt`
- Edit docs-italia-documents.yml to meet your needs
- Run the script `python check_redirects.py`

## Caveats

Since 301 redirects are not supported on readthedocs, you need to use html/js to
achieve the same result. This tool does not check if your html/js code is
actually redirecting, but instead checks that every page in each version of your
original document exists in your redirect document. Additionally it checks for
the existence of an html link (`<a>` tag), with `redirect` as `id` attribute, in
each page of your redirect document.
