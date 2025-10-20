# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

WebRTC for the Curious is an open-source educational book about WebRTC, written by implementers for developers who want to understand the protocols and APIs in depth. The book is multilingual, vendor-agnostic, and focuses on explaining the "why" and "how" rather than just the "what".

## Build and Development Commands

### Run Development Server
```bash
hugo server
```
The site will be available at http://localhost:1313. Hugo has live reload enabled by default.

### Build Static Site
```bash
hugo --minify
```
Builds the site to `public/` directory.

### Generate PDF/EPUB Outputs
The book is converted to PDF and EPUB using Pandoc. This happens automatically in CI, but for local generation:

```bash
# Generate English PDF
docker run --rm -v "$(pwd):/data" pandoc/latex:3.8 \
  --output=webrtc-for-the-curious.pdf \
  --resource-path=.:./content:./content/docs/images \
  --toc content/_index.md content/docs/*.md .pandoc/metadata_pdf_en.txt

# Generate English EPUB
docker run --rm -v "$(pwd):/data" pandoc/latex:3.8 \
  --output=webrtc-for-the-curious.epub \
  --resource-path=.:./content:./content/images \
  --toc content/_index.md content/docs/*.md .pandoc/metadata_en.txt
```

For Swedish translations, replace `content/` with `content.sv/` and use `.pandoc/metadata_pdf_sv.txt` or `.pandoc/metadata_sv.txt`.

### Generate Cover Images
```bash
# English cover
python3 make-cover.py

# Swedish cover
python3 make-cover-sv.py

# Chinese cover
python3 make-cover-zh-cn.py
```
These scripts use ImageMagick to generate covers based on git contribution statistics.

## Repository Structure

### Content Organization

The book is organized as a Hugo site with multilingual support:

- `content/` - English content (default language)
- `content.{lang}/` - Translated content directories (e.g., `content.sv/`, `content.ja/`, `content.zh-cn/`, `content.ru/`, etc.)
- Each language has a `docs/` subdirectory containing chapter markdown files

### Chapter Files

Chapters are numbered markdown files in `content/docs/`:
- `01-what-why-and-how.md` - Introduction to WebRTC
- `02-signaling.md` - Signaling process
- `03-connecting.md` - Connection establishment
- `04-securing.md` - Security (DTLS, SRTP)
- `05-real-time-networking.md` - Real-time networking concepts
- `06-media-communication.md` - Media transmission
- `07-data-communication.md` - Data channels
- `08-applied-webrtc.md` - Practical applications
- `09-debugging.md` - Debugging techniques
- `10-history-of-webrtc.md` - Historical context
- `11-faq.md` - Frequently asked questions
- `12-glossary.md` - Terminology
- `13-reference.md` - References

### Configuration

- `config.toml` - Hugo configuration with language settings and theme configuration
- `.pandoc/` - Pandoc metadata files for PDF/EPUB generation
- `themes/book/` - Hugo Book theme (submodule)
- `.editorconfig` - Editor configuration for consistent formatting

## Architecture and Design

### Hugo Static Site Generator

This project uses Hugo with the "book" theme. Hugo is required in its "extended" version (currently 0.131.0 in CI) to support advanced features.

### Multi-language Support

The site supports 11 languages configured in `config.toml`. Each language has:
- Its own content directory (e.g., `content.ja` for Japanese)
- Language-specific metadata in `.pandoc/`
- Same chapter structure as English version

Language codes: en, ko, ru, sv, zh, ja, fa, fr, id, es, tr

### Build Pipeline

1. **Local Development**: Hugo server with live reload
2. **Static Site**: Hugo generates HTML to `public/`
3. **PDF/EPUB Generation**: Pandoc converts markdown chapters to PDF and EPUB formats
4. **GitHub Pages Deployment**: CI publishes to webrtcforthecurious.com

### Content Structure

Each chapter follows a three-level format:
1. What problem needs to be solved?
2. How is it solved (technical details)?
3. Where to learn more

Chapters are self-contained and can be read in any order.

## Coding Standards

### Markdown Formatting

- **Indentation**: 4 spaces for markdown files
- **Line endings**: LF (Unix-style)
- **Trailing whitespace**: Preserved in markdown (see `.editorconfig`)
- **Encoding**: UTF-8

### Content Guidelines

- Focus on protocols and APIs, not specific software implementations
- Maintain vendor-agnostic approach
- Explain concepts thoroughly without assuming prior knowledge
- Include references to RFCs and specifications
- Minimize code examples (this is not a tutorial)

## Git Workflow

- **Main branch**: `master`
- **Submodules**: The `themes/book` directory is a git submodule - always update with `git submodule update --recursive --init`
- Clone with submodules: `git clone --recursive https://github.com/webrtc-for-the-curious/webrtc-for-the-curious.git`

## Deployment

The site auto-deploys to webrtcforthecurious.com via GitHub Actions when pushing to `master`. The workflow:
1. Checks out code with submodules
2. Builds site with Hugo
3. Generates PDF/EPUB files with Pandoc
4. Copies images to public directory
5. Deploys to GitHub Pages

## License

Content is licensed under CC0 (Creative Commons Zero v1.0 Universal) - no attribution required.
